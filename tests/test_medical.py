import io
import json
import os
import tempfile
import unittest
from pathlib import Path
from unittest.mock import patch

import app as healthsync


class MedicalWorkflowTests(unittest.TestCase):
    def setUp(self):
        self.temp_dir = tempfile.TemporaryDirectory()
        self.original_db_path = healthsync.DB_PATH
        self.original_private_dir = healthsync.MEDICAL_PRIVATE_DIR
        self.original_reports_dir = healthsync.MEDICAL_REPORTS_DIR
        healthsync.DB_PATH = Path(self.temp_dir.name) / "test-healthsync.db"
        healthsync.MEDICAL_PRIVATE_DIR = Path(self.temp_dir.name) / "private-data"
        healthsync.MEDICAL_REPORTS_DIR = Path(self.temp_dir.name) / "private-reports"
        healthsync.app.config.update(TESTING=True, MAX_CONTENT_LENGTH=10 * 1024 * 1024 + 100 * 1024)
        healthsync.init_db()
        self.patient = healthsync.app.test_client()
        self.other_patient = healthsync.app.test_client()
        for client, email in (
            (self.patient, "patient-one@example.test"),
            (self.other_patient, "patient-two@example.test"),
        ):
            response = client.post(
                "/api/auth/signup",
                json={"email": email, "password": "test-password-123", "firstName": "Test"},
            )
            self.assertEqual(response.status_code, 200)

    def tearDown(self):
        healthsync.DB_PATH = self.original_db_path
        healthsync.MEDICAL_PRIVATE_DIR = self.original_private_dir
        healthsync.MEDICAL_REPORTS_DIR = self.original_reports_dir
        healthsync.app.config.update(TESTING=False)
        self.temp_dir.cleanup()

    def upload_report(self, client, name, category, extracted_text):
        with patch.object(healthsync, "extract_report_text", return_value=extracted_text):
            response = client.post(
                "/api/medical/reports",
                data={
                    "category": category,
                    "reportName": name,
                    "testDate": "",
                    "facilityName": "Test laboratory",
                    "report": (io.BytesIO(b"%PDF-1.4 local test fixture"), f"{name}.pdf"),
                },
                content_type="multipart/form-data",
            )
        self.assertEqual(response.status_code, 201, response.get_json())
        return response.get_json()

    def verify_report(self, client, report_id, test_date, values):
        response = client.put(
            f"/api/medical/reports/{report_id}/verify",
            json={
                "testDate": test_date,
                "facilityName": "Test laboratory",
                "otherResults": "",
                "confirmed": {kind: True for kind in values},
                **values,
            },
        )
        self.assertEqual(response.status_code, 200, response.get_json())
        return response.get_json()

    def test_private_medical_record_lifecycle_and_local_ai_context(self):
        self.assertEqual(self.patient.get("/api/medical").status_code, 200)
        history = self.patient.put(
            "/api/medical/history",
            json={
                "hasPreviousDiabetes": True,
                "hasPreviousTreatment": True,
                "diagnosisDate": "2018-05-12",
                "yearsWithDiabetes": 8,
                "diabetesCategory": "Type 2",
                "complications": "Patient-reported history",
            },
        )
        self.assertEqual(history.status_code, 200)

        treatment = self.patient.post(
            "/api/medical/treatments",
            json={
                "details": "Previous care history",
                "provider": "Local clinic",
                "startedOn": "2019-01-01",
                "endedOn": "2020-01-01",
            },
        ).get_json()
        self.assertEqual(
            self.patient.put(
                f"/api/medical/treatments/{treatment['id']}",
                json={
                    "details": "Updated care history",
                    "provider": "Community clinic",
                    "startedOn": "2019-01-01",
                    "endedOn": "2020-02-01",
                },
            ).status_code,
            200,
        )

        medication = self.patient.post(
            "/api/medical/medications",
            json={
                "name": "Patient-entered medicine",
                "dosage": "10 mg",
                "frequency": "Once daily",
                "startedOn": "2020-01-01",
                "duration": "6 months",
                "isCurrent": False,
                "discontinuedOn": "2020-07-01",
                "discontinuationReason": "Patient-reported",
            },
        ).get_json()
        updated_medication = self.patient.put(
            f"/api/medical/medications/{medication['id']}",
            json={
                "name": "Patient-entered medicine",
                "dosage": "10 mg",
                "frequency": "Once daily",
                "startedOn": "2020-01-01",
                "duration": "6 months",
                "isCurrent": True,
                "discontinuedOn": "",
                "discontinuationReason": "",
            },
        )
        self.assertEqual(updated_medication.status_code, 200)

        no_consent = self.patient.post(
            "/api/medical/reports",
            data={"report": (io.BytesIO(b"%PDF-1.4"), "report.pdf")},
            content_type="multipart/form-data",
        )
        self.assertEqual(no_consent.status_code, 400)
        consent = self.patient.put("/api/medical/consent", json={"consent": True})
        self.assertEqual(consent.status_code, 200)

        previous = self.upload_report(
            self.patient,
            "previous",
            "before_treatment",
            "Fasting glucose: 145 mg/dL\nPP glucose: 210 mg/dL\nHbA1c: 8.2%",
        )
        report_id = previous["report"]["id"]
        self.assertEqual(previous["extraction"]["values"]["fasting"], 145.0)
        self.assertEqual(self.patient.get("/api/medical").get_json()["readings"], [])
        private_file = next(healthsync.MEDICAL_REPORTS_DIR.iterdir())
        self.assertEqual(os.stat(private_file).st_mode & 0o777, 0o600)
        self.assertEqual(
            self.other_patient.get(f"/api/medical/reports/{report_id}/file").status_code,
            404,
        )
        owner_file = self.patient.get(f"/api/medical/reports/{report_id}/file")
        self.assertEqual(owner_file.status_code, 200)
        self.assertIn("no-store", owner_file.headers["Cache-Control"])
        owner_file.close()

        self.verify_report(
            self.patient,
            report_id,
            "2022-05-20",
            {"fasting": 145, "postprandial": 210, "hba1c": 8.2},
        )
        latest = self.upload_report(
            self.patient,
            "latest",
            "after_treatment",
            "Fasting glucose: 120 mg/dL\nPP glucose: 180 mg/dL\nHbA1c: 7.1%",
        )
        latest_id = latest["report"]["id"]
        self.verify_report(
            self.patient,
            latest_id,
            "2025-06-11",
            {"fasting": 120, "postprandial": 180, "hba1c": 7.1},
        )
        unverified = self.upload_report(
            self.patient, "unverified", "after_treatment", "Fasting glucose: 999 mg/dL"
        )
        self.assertEqual(self.other_patient.get("/api/medical").get_json()["reports"], [])
        self.assertEqual(
            self.other_patient.put(
                f"/api/medical/reports/{latest_id}/verify",
                json={"testDate": "2025-06-11", "confirmed": {"fasting": True}, "fasting": 1},
            ).status_code,
            404,
        )

        reading = self.patient.post(
            "/api/medical/readings",
            json={"type": "random", "value": 130, "measuredAt": "2025-06-11T18:30"},
        ).get_json()
        corrected = self.patient.put(
            f"/api/medical/readings/{reading['id']}",
            json={"value": 131, "measuredAt": "2025-06-11T19:00"},
        )
        self.assertEqual(corrected.status_code, 200)
        payload = self.patient.get("/api/medical").get_json()
        self.assertEqual(len(payload["reports"]), 3)
        self.assertEqual(len(payload["readings"]), 7)
        self.assertIn("diagnosis", [item["kind"] for item in payload["timeline"]])
        self.assertIn("treatment", [item["kind"] for item in payload["timeline"]])
        self.assertEqual(
            next(item for item in payload["reports"] if item["id"] == report_id)["testDate"],
            "2022-05-20",
        )
        self.assertNotIn("999", json.dumps(payload["readings"]))

        fake_ollama_response = unittest.mock.Mock()
        fake_ollama_response.json.return_value = {"response": "These recorded results need clinical context."}
        with patch.object(healthsync, "ensure_ollama_ready"), patch.object(
            healthsync.requests, "post", return_value=fake_ollama_response
        ) as local_post:
            explanation = self.patient.post(
                "/api/medical/assistant", json={"question": "Explain the change."}
            )
        self.assertEqual(explanation.status_code, 200, explanation.get_json())
        self.assertTrue(explanation.get_json()["localProcessing"])
        self.assertIn("145.0", local_post.call_args.kwargs["json"]["prompt"])
        self.assertNotIn("999", local_post.call_args.kwargs["json"]["prompt"])
        self.assertIn("Do not diagnose", local_post.call_args.kwargs["json"]["prompt"])

        self.patient.post("/api/auth/logout")
        self.assertEqual(self.patient.get("/api/medical").status_code, 401)
        self.patient.post(
            "/api/auth/login",
            json={"email": "patient-one@example.test", "password": "test-password-123"},
        )
        persisted = self.patient.get("/api/medical").get_json()
        self.assertEqual(len(persisted["reports"]), 3)
        self.assertEqual(persisted["history"]["diagnosisDate"], "2018-05-12")

        deleted = self.patient.delete(f"/api/medical/reports/{report_id}")
        self.assertEqual(deleted.status_code, 200)
        remaining = self.patient.get("/api/medical").get_json()
        self.assertNotIn(report_id, [report["id"] for report in remaining["reports"]])
        self.assertFalse(private_file.exists())

    def test_report_validation_and_unverified_extraction_are_not_saved(self):
        self.patient.put("/api/medical/consent", json={"consent": True})
        wrong_signature = self.patient.post(
            "/api/medical/reports",
            data={
                "category": "before_treatment",
                "report": (io.BytesIO(b"not a PDF"), "report.pdf"),
            },
            content_type="multipart/form-data",
        )
        self.assertEqual(wrong_signature.status_code, 400)
        self.assertEqual(self.patient.get("/api/medical").get_json()["reports"], [])

        invalid_reading = self.patient.post(
            "/api/medical/readings",
            json={"type": "fasting", "value": 12, "measuredAt": "not-a-date"},
        )
        self.assertEqual(invalid_reading.status_code, 400)
        self.assertEqual(self.patient.get("/api/medical").get_json()["readings"], [])


if __name__ == "__main__":
    unittest.main()
