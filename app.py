import json
import math
import os
import re
import shutil
import sqlite3
import subprocess
import uuid
from datetime import datetime
from pathlib import Path

import requests
from flask import Flask, jsonify, request, send_file, session
from pypdf.errors import PdfReadError
from werkzeug.utils import secure_filename
from werkzeug.security import check_password_hash, generate_password_hash

app = Flask(__name__, static_folder="", static_url_path="")
app.secret_key = os.environ.get("SESSION_SECRET", "healthsync-dev-secret-change-me")
app.config["MAX_CONTENT_LENGTH"] = 10 * 1024 * 1024 + 100 * 1024

BASE_DIR = Path(__file__).resolve().parent
DB_PATH = BASE_DIR / "healthsync.db"
MEDICAL_PRIVATE_DIR = Path.home() / ".healthsync"
MEDICAL_REPORTS_DIR = MEDICAL_PRIVATE_DIR / "medical_reports"
OLLAMA_URL = "http://localhost:11434/api/generate"
ELLAMA_MODEL = "llama3.2:3b"
MAX_MEDICAL_REPORT_BYTES = 10 * 1024 * 1024
MEDICAL_REPORT_TYPES = {
    ".pdf": ("application/pdf", b"%PDF-"),
    ".jpg": ("image/jpeg", b"\xff\xd8\xff"),
    ".jpeg": ("image/jpeg", b"\xff\xd8\xff"),
    ".png": ("image/png", b"\x89PNG\r\n\x1a\n"),
}


def get_db_connection():
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    return conn


def now_iso():
    return datetime.utcnow().strftime("%Y-%m-%d %H:%M:%S")


def init_db():
    conn = get_db_connection()
    conn.execute(
        """
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            email TEXT UNIQUE NOT NULL,
            first_name TEXT,
            last_name TEXT,
            password_hash TEXT NOT NULL,
            language TEXT NOT NULL DEFAULT 'en',
            reminders_enabled INTEGER NOT NULL DEFAULT 1,
            notifications_enabled INTEGER NOT NULL DEFAULT 1,
            private_mode INTEGER NOT NULL DEFAULT 0,
            created_at TEXT NOT NULL DEFAULT CURRENT_TIMESTAMP
        )
        """
    )
    conn.execute(
        """
        CREATE TABLE IF NOT EXISTS profiles (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id INTEGER UNIQUE NOT NULL,
            age INTEGER,
            gender TEXT,
            height_cm REAL,
            weight_kg REAL,
            bmi REAL,
            diabetes_category TEXT,
            health_conditions TEXT,
            food_preferences TEXT,
            activity_level TEXT,
            lifestyle TEXT,
            goals TEXT,
            notes TEXT,
            created_at TEXT NOT NULL DEFAULT CURRENT_TIMESTAMP,
            updated_at TEXT NOT NULL DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY(user_id) REFERENCES users(id)
        )
        """
    )

    conn.execute(
        """
        CREATE TABLE IF NOT EXISTS health_records (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id INTEGER NOT NULL,
            record_date TEXT,
            blood_glucose REAL,
            bmi REAL,
            steps INTEGER,
            hydration_liters REAL,
            sleep_hours REAL,
            notes TEXT,
            created_at TEXT NOT NULL DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY(user_id) REFERENCES users(id)
        )
        """
    )

    conn.execute(
        """
        CREATE TABLE IF NOT EXISTS diet_entries (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id INTEGER NOT NULL,
            meal_name TEXT,
            food_items TEXT,
            calories INTEGER,
            created_at TEXT NOT NULL DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY(user_id) REFERENCES users(id)
        )
        """
    )

    conn.execute(
        """
        CREATE TABLE IF NOT EXISTS activity_entries (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id INTEGER NOT NULL,
            activity_name TEXT,
            duration_minutes INTEGER,
            steps INTEGER,
            created_at TEXT NOT NULL DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY(user_id) REFERENCES users(id)
        )
        """
    )

    conn.execute(
        """
        CREATE TABLE IF NOT EXISTS chat_sessions (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id INTEGER NOT NULL,
            title TEXT NOT NULL DEFAULT 'New chat',
            created_at TEXT NOT NULL DEFAULT CURRENT_TIMESTAMP,
            updated_at TEXT NOT NULL DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY(user_id) REFERENCES users(id)
        )
        """
    )

    conn.execute(
        """
        CREATE TABLE IF NOT EXISTS chat_messages (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            session_id INTEGER NOT NULL,
            sender TEXT NOT NULL,
            message TEXT NOT NULL,
            created_at TEXT NOT NULL DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY(session_id) REFERENCES chat_sessions(id)
        )
        """
    )

    conn.execute(
        """
        CREATE TABLE IF NOT EXISTS diet_daily_status (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id INTEGER NOT NULL,
            status_date TEXT NOT NULL,
            meal_name TEXT NOT NULL,
            completed INTEGER NOT NULL DEFAULT 0,
            updated_at TEXT NOT NULL DEFAULT CURRENT_TIMESTAMP,
            UNIQUE(user_id, status_date, meal_name),
            FOREIGN KEY(user_id) REFERENCES users(id)
        )
        """
    )

    conn.execute(
        """
        CREATE TABLE IF NOT EXISTS activity_daily_status (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id INTEGER NOT NULL,
            status_date TEXT NOT NULL,
            activity_name TEXT NOT NULL,
            completed INTEGER NOT NULL DEFAULT 0,
            updated_at TEXT NOT NULL DEFAULT CURRENT_TIMESTAMP,
            UNIQUE(user_id, status_date, activity_name),
            FOREIGN KEY(user_id) REFERENCES users(id)
        )
        """
    )

    conn.execute(
        """
        CREATE TABLE IF NOT EXISTS patient_medical_history (
            user_id INTEGER PRIMARY KEY,
            has_previous_diabetes INTEGER NOT NULL DEFAULT 0,
            has_previous_treatment INTEGER NOT NULL DEFAULT 0,
            diagnosis_date TEXT,
            years_with_diabetes REAL,
            diabetes_category TEXT,
            complications TEXT NOT NULL DEFAULT '',
            reports_consent INTEGER NOT NULL DEFAULT 0,
            consent_updated_at TEXT,
            updated_at TEXT NOT NULL DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY(user_id) REFERENCES users(id)
        )
        """
    )
    medical_history_columns = {
        column[1] for column in conn.execute("PRAGMA table_info(patient_medical_history)")
    }
    if "has_previous_treatment" not in medical_history_columns:
        conn.execute(
            "ALTER TABLE patient_medical_history ADD COLUMN has_previous_treatment INTEGER NOT NULL DEFAULT 0"
        )
    conn.execute(
        """
        CREATE TABLE IF NOT EXISTS treatment_history (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id INTEGER NOT NULL,
            treatment_details TEXT NOT NULL,
            provider_name TEXT NOT NULL DEFAULT '',
            started_on TEXT,
            ended_on TEXT,
            created_at TEXT NOT NULL DEFAULT CURRENT_TIMESTAMP,
            updated_at TEXT NOT NULL DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY(user_id) REFERENCES users(id)
        )
        """
    )
    conn.execute(
        """
        CREATE TABLE IF NOT EXISTS medication_history (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id INTEGER NOT NULL,
            medication_name TEXT NOT NULL,
            dosage TEXT NOT NULL DEFAULT '',
            frequency TEXT NOT NULL DEFAULT '',
            started_on TEXT,
            duration TEXT NOT NULL DEFAULT '',
            is_current INTEGER NOT NULL DEFAULT 0,
            discontinued_on TEXT,
            discontinuation_reason TEXT NOT NULL DEFAULT '',
            created_at TEXT NOT NULL DEFAULT CURRENT_TIMESTAMP,
            updated_at TEXT NOT NULL DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY(user_id) REFERENCES users(id)
        )
        """
    )
    conn.execute(
        """
        CREATE TABLE IF NOT EXISTS medical_reports (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id INTEGER NOT NULL,
            stored_name TEXT NOT NULL UNIQUE,
            report_name TEXT NOT NULL,
            category TEXT NOT NULL CHECK(category IN ('before_treatment', 'after_treatment')),
            test_date TEXT,
            facility_name TEXT NOT NULL DEFAULT '',
            other_results TEXT NOT NULL DEFAULT '',
            verified INTEGER NOT NULL DEFAULT 0,
            uploaded_at TEXT NOT NULL,
            verified_at TEXT,
            FOREIGN KEY(user_id) REFERENCES users(id)
        )
        """
    )
    conn.execute(
        """
        CREATE TABLE IF NOT EXISTS blood_glucose_readings (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id INTEGER NOT NULL,
            report_id INTEGER,
            measurement_type TEXT NOT NULL CHECK(measurement_type IN ('fasting', 'postprandial', 'random', 'hba1c')),
            value REAL NOT NULL,
            unit TEXT NOT NULL,
            measurement_date TEXT NOT NULL,
            measurement_time TEXT,
            source TEXT NOT NULL DEFAULT 'manual' CHECK(source IN ('manual', 'report')),
            created_at TEXT NOT NULL DEFAULT CURRENT_TIMESTAMP,
            updated_at TEXT NOT NULL DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY(user_id) REFERENCES users(id),
            FOREIGN KEY(report_id) REFERENCES medical_reports(id),
            UNIQUE(report_id, measurement_type)
        )
        """
    )

    conn.execute(
        "CREATE INDEX IF NOT EXISTS idx_chat_sessions_user ON chat_sessions(user_id, updated_at DESC)"
    )
    conn.execute(
        "CREATE INDEX IF NOT EXISTS idx_diet_daily_status_user_date ON diet_daily_status(user_id, status_date)"
    )
    conn.execute(
        "CREATE INDEX IF NOT EXISTS idx_medical_reports_user_date ON medical_reports(user_id, test_date DESC)"
    )
    conn.execute(
        "CREATE INDEX IF NOT EXISTS idx_glucose_readings_user_date ON blood_glucose_readings(user_id, measurement_date DESC, measurement_time DESC)"
    )

    chat_columns = conn.execute("PRAGMA table_info(chat_sessions)").fetchall()
    if not any(column[1] == "title" for column in chat_columns):
        conn.execute("ALTER TABLE chat_sessions ADD COLUMN title TEXT NOT NULL DEFAULT 'New chat'")

    user_columns = {column[1] for column in conn.execute("PRAGMA table_info(users)")}
    user_migrations = {
        "language": "TEXT NOT NULL DEFAULT 'en'",
        "reminders_enabled": "INTEGER NOT NULL DEFAULT 1",
        "notifications_enabled": "INTEGER NOT NULL DEFAULT 1",
        "private_mode": "INTEGER NOT NULL DEFAULT 0",
    }
    for column, definition in user_migrations.items():
        if column not in user_columns:
            conn.execute(f"ALTER TABLE users ADD COLUMN {column} {definition}")

    profile_columns = {column[1] for column in conn.execute("PRAGMA table_info(profiles)")}
    for column in ("lifestyle", "goals"):
        if column not in profile_columns:
            conn.execute(f"ALTER TABLE profiles ADD COLUMN {column} TEXT")

    conn.commit()

    existing_user = conn.execute(
        "SELECT id FROM users WHERE email = ?", ("demo@healthsync.local",)
    ).fetchone()

    if existing_user is None:
        demo_password = generate_password_hash("demo123")
        user_id = conn.execute(
            """
            INSERT INTO users (email, first_name, last_name, password_hash)
            VALUES (?, ?, ?, ?)
            """,
            ("demo@healthsync.local", "Demo", "User", demo_password),
        ).lastrowid

        conn.execute(
            """
            INSERT INTO profiles (
                user_id, age, gender, height_cm, weight_kg, bmi, diabetes_category,
                health_conditions, food_preferences, activity_level, notes
            ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            """,
            (
                user_id,
                36,
                "Female",
                168,
                73,
                25.9,
                "Type 2 diabetes",
                "Mild hypertension; fatigue during busy weeks",
                "Vegetarian, low sugar, moderate carbs",
                "Moderate",
                "Prefers consistent meals and evening walks.",
            ),
        )

        conn.execute(
            """
            INSERT INTO health_records (
                user_id, record_date, blood_glucose, bmi, steps, hydration_liters, sleep_hours, notes
            ) VALUES (?, ?, ?, ?, ?, ?, ?, ?)
            """,
            (
                user_id,
                "2026-10-20",
                118.0,
                25.9,
                7800,
                2.1,
                7.5,
                "Stable blood sugar after lunch; good hydration.",
            ),
        )

        conn.execute(
            """
            INSERT INTO diet_entries (user_id, meal_name, food_items, calories)
            VALUES (?, ?, ?, ?)
            """,
            (user_id, "Breakfast", "Oatmeal, berries, yogurt", 360),
        )
        conn.execute(
            """
            INSERT INTO diet_entries (user_id, meal_name, food_items, calories)
            VALUES (?, ?, ?, ?)
            """,
            (user_id, "Lunch", "Grilled chicken, brown rice, greens", 540),
        )
        conn.execute(
            """
            INSERT INTO diet_entries (user_id, meal_name, food_items, calories)
            VALUES (?, ?, ?, ?)
            """,
            (user_id, "Dinner", "Salmon, quinoa, vegetables", 470),
        )

        conn.execute(
            """
            INSERT INTO activity_entries (user_id, activity_name, duration_minutes, steps)
            VALUES (?, ?, ?, ?)
            """,
            (user_id, "Morning walk", 30, 4200),
        )
        conn.execute(
            """
            INSERT INTO activity_entries (user_id, activity_name, duration_minutes, steps)
            VALUES (?, ?, ?, ?)
            """,
            (user_id, "Mobility routine", 15, 0),
        )

    conn.commit()
    conn.close()
    try:
        os.chmod(DB_PATH, 0o600)
    except OSError:
        app.logger.warning("Could not restrict permissions on the HealthSync database file.")


def get_chat_session_for_user(session_id, user_id):
    conn = get_db_connection()
    row = conn.execute(
        "SELECT * FROM chat_sessions WHERE id = ? AND user_id = ?",
        (session_id, user_id),
    ).fetchone()
    conn.close()
    return row


def get_user_chat_sessions(user_id):
    conn = get_db_connection()
    rows = conn.execute(
        "SELECT * FROM chat_sessions WHERE user_id = ? ORDER BY updated_at DESC, created_at DESC",
        (user_id,),
    ).fetchall()
    conn.close()
    return [dict(row) for row in rows]


def get_chat_history(session_id):
    conn = get_db_connection()
    rows = conn.execute(
        "SELECT sender, message, created_at FROM chat_messages WHERE session_id = ? ORDER BY created_at ASC",
        (session_id,),
    ).fetchall()
    conn.close()
    return rows


def save_chat_message(session_id, sender, message):
    conn = get_db_connection()
    conn.execute(
        "INSERT INTO chat_messages (session_id, sender, message, created_at) VALUES (?, ?, ?, ?)",
        (session_id, sender, message, now_iso()),
    )
    conn.execute(
        "UPDATE chat_sessions SET updated_at = ? WHERE id = ?",
        (now_iso(), session_id),
    )
    conn.commit()
    conn.close()


def create_chat_session(user_id, title="New chat"):
    conn = get_db_connection()
    cursor = conn.execute(
        "INSERT INTO chat_sessions (user_id, title, created_at, updated_at) VALUES (?, ?, ?, ?)",
        (user_id, title, now_iso(), now_iso()),
    )
    session_id = cursor.lastrowid
    conn.commit()
    conn.close()
    return session_id


def get_user_diet_status(user_id, status_date):
    conn = get_db_connection()
    rows = conn.execute(
        "SELECT meal_name, completed FROM diet_daily_status WHERE user_id = ? AND status_date = ?",
        (user_id, status_date),
    ).fetchall()
    conn.close()
    return {row["meal_name"]: bool(row["completed"]) for row in rows}


def get_user_diet_history(user_id):
    conn = get_db_connection()
    rows = conn.execute(
        "SELECT status_date, meal_name, completed, updated_at FROM diet_daily_status WHERE user_id = ? ORDER BY status_date DESC, meal_name ASC",
        (user_id,),
    ).fetchall()
    conn.close()
    return [dict(row) for row in rows]


def update_diet_status(user_id, status_date, meal_name, completed):
    conn = get_db_connection()
    conn.execute(
        """
        INSERT INTO diet_daily_status (user_id, status_date, meal_name, completed, updated_at)
        VALUES (?, ?, ?, ?, ?)
        ON CONFLICT(user_id, status_date, meal_name)
        DO UPDATE SET completed = excluded.completed, updated_at = excluded.updated_at
        """,
        (user_id, status_date, meal_name, 1 if completed else 0, now_iso()),
    )
    conn.commit()
    conn.close()


def get_user_activity_status(user_id, status_date):
    conn = get_db_connection()
    rows = conn.execute(
        "SELECT activity_name, completed FROM activity_daily_status WHERE user_id = ? AND status_date = ?",
        (user_id, status_date),
    ).fetchall()
    conn.close()
    return {row["activity_name"]: bool(row["completed"]) for row in rows}


def update_activity_status(user_id, status_date, activity_name, completed):
    conn = get_db_connection()
    conn.execute(
        """
        INSERT INTO activity_daily_status (user_id, status_date, activity_name, completed, updated_at)
        VALUES (?, ?, ?, ?, ?)
        ON CONFLICT(user_id, status_date, activity_name)
        DO UPDATE SET completed = excluded.completed, updated_at = excluded.updated_at
        """,
        (user_id, status_date, activity_name, 1 if completed else 0, now_iso()),
    )
    conn.commit()
    conn.close()


def get_current_user():
    user_id = session.get("user_id")
    if not user_id:
        return None

    conn = get_db_connection()
    user = conn.execute(
        "SELECT * FROM users WHERE id = ?", (user_id,)
    ).fetchone()
    conn.close()
    return user


def get_user_profile_context(user_id):
    conn = get_db_connection()
    profile = conn.execute(
        "SELECT * FROM profiles WHERE user_id = ?", (user_id,)
    ).fetchone()

    if not profile:
        conn.close()
        return "No health profile is available for this user yet."

    recent_record = conn.execute(
        "SELECT * FROM health_records WHERE user_id = ? ORDER BY record_date DESC LIMIT 1",
        (user_id,),
    ).fetchone()

    diet_rows = conn.execute(
        "SELECT * FROM diet_entries WHERE user_id = ? ORDER BY created_at DESC LIMIT 3",
        (user_id,),
    ).fetchall()

    activity_rows = conn.execute(
        "SELECT * FROM activity_entries WHERE user_id = ? ORDER BY created_at DESC LIMIT 3",
        (user_id,),
    ).fetchall()

    conn.close()

    diet_summary = "; ".join(
        [f"{row['meal_name']}: {row['food_items']} ({row['calories']} kcal)" for row in diet_rows]
    ) if diet_rows else "No recent diet data available."

    activity_summary = "; ".join(
        [f"{row['activity_name']}: {row['duration_minutes']} mins" for row in activity_rows]
    ) if activity_rows else "No recent activity data available."

    blood_glucose = recent_record["blood_glucose"] if recent_record and recent_record["blood_glucose"] is not None else "Not available"
    bmi = profile["bmi"] if profile["bmi"] is not None else "Not available"
    steps = recent_record["steps"] if recent_record and recent_record["steps"] is not None else "Not available"
    hydration = recent_record["hydration_liters"] if recent_record and recent_record["hydration_liters"] is not None else "Not available"
    sleep = recent_record["sleep_hours"] if recent_record and recent_record["sleep_hours"] is not None else "Not available"

    return (
        "User health context:\n"
        f"- Age: {profile['age'] if profile['age'] is not None else 'Not available'}\n"
        f"- Gender: {profile['gender'] if profile['gender'] else 'Not available'}\n"
        f"- Height: {profile['height_cm'] if profile['height_cm'] is not None else 'Not available'} cm\n"
        f"- Weight: {profile['weight_kg'] if profile['weight_kg'] is not None else 'Not available'} kg\n"
        f"- BMI: {bmi}\n"
        f"- Diabetes category: {profile['diabetes_category'] if profile['diabetes_category'] else 'Not available'}\n"
        f"- Health conditions: {profile['health_conditions'] if profile['health_conditions'] else 'Not available'}\n"
        f"- Food preferences: {profile['food_preferences'] if profile['food_preferences'] else 'Not available'}\n"
        f"- Activity level: {profile['activity_level'] if profile['activity_level'] else 'Not available'}\n"
        f"- Lifestyle: {profile['lifestyle'] if profile['lifestyle'] else 'Not available'}\n"
        f"- Goals: {profile['goals'] if profile['goals'] else 'Not available'}\n"
        f"- Notes: {profile['notes'] if profile['notes'] else 'Not available'}\n"
        f"- Recent blood glucose: {blood_glucose}\n"
        f"- Recent steps: {steps}\n"
        f"- Recent hydration: {hydration} L\n"
        f"- Recent sleep: {sleep} hours\n"
        f"- Recent diet: {diet_summary}\n"
        f"- Recent activities: {activity_summary}\n"
    )


def ensure_ollama_ready():
    ollama_path = shutil.which("ollama")
    if not ollama_path:
        raise RuntimeError(
            "Ollama is not installed or not available on your PATH. Install it from https://ollama.com and restart the app."
        )

    result = subprocess.run(
        ["ollama", "list"],
        capture_output=True,
        text=True,
        timeout=30,
    )

    if result.returncode != 0:
        raise RuntimeError(
            "Ollama could not be reached. Please start the Ollama service locally before using the assistant."
        )

    model_names = []
    for line in result.stdout.splitlines():
        if not line.strip():
            continue
        parts = line.split()
        if parts and parts[0] != "NAME":
            model_names.append(parts[0])

    if "llama3.2:3b" not in model_names:
        raise RuntimeError(
            "The required Ollama model 'llama3.2:3b' is not installed. Run: `ollama pull llama3.2:3b` and then try again."
        )

    return True

def generate_assistant_reply(message, language, user_id):
    ensure_ollama_ready()

    session_id = session.get("chat_session_id")
    conv_history = []
    if session_id:
        hist_rows = get_chat_history(session_id)
        conv_history = [f"{row['sender']}: {row['message']}" for row in hist_rows]

    health_context = get_user_profile_context(user_id)

    lang_instruction = {
        "en": "Write the entire answer in English.",
        "te": "మీ సమాధానం మొత్తం తెలుగులోనే రాయండి. తెలుగు లిపిని ఉపయోగించండి. వైద్య కొలతలు, సరైన పేర్లు తప్ప ఆంగ్ల పదాలు ఉపయోగించవద్దు.",
        "hi": "अपना पूरा उत्तर हिंदी में लिखें। देवनागरी लिपि का उपयोग करें। चिकित्सा माप और उचित नामों को छोड़कर अंग्रेज़ी शब्दों का उपयोग न करें।",
    }[language]

    prompt = f"""
You are HealthSync AI assistant.
{lang_instruction}

Safety policy:
- Do not diagnose diseases, prescribe medication, or claim to replace a doctor.
- Use only the health information provided below and never invent missing details.
- If details are missing, say so and provide general, safe wellness guidance.
- Keep answers supportive, practical, and non-judgmental.
- Always follow the requested response language, even if earlier messages used a different language.

User health context:
{health_context}

Recent conversation:
{chr(10).join(conv_history) if conv_history else 'No previous messages.'}

User question: {message}

Give a concise but helpful answer based on the user's actual health context.
"""

    payload = {
        "model": ELLAMA_MODEL,
        "prompt": prompt,
        "stream": False,
        "options": {"temperature": 0.4},
    }

    try:
        response = requests.post(OLLAMA_URL, json=payload, timeout=120)
        response.raise_for_status()
    except requests.exceptions.RequestException as exc:
        raise RuntimeError(
            "The local Ollama service is unavailable right now. Please make sure Ollama is running and the model is installed."
        ) from exc

    data = response.json()
    reply = data.get("response", "").strip()

    if not reply:
        raise RuntimeError("Ollama returned an empty response. Please try again.")

    return reply


@app.route("/", endpoint="home_page")
def index_page():
    return send_file(BASE_DIR / "index.html")


PAGES = [
    "index",
    "login",
    "signup",
    "onboarding",
    "dashboard",
    "diet",
    "activities",
    "progress",
    "ai",
    "profile",
    "medical",
]


for page_name in PAGES:
    app.add_url_rule(
        f"/{page_name}.html",
        endpoint=f"{page_name}_page",
        view_func=lambda page_name=page_name: send_file(BASE_DIR / f"{page_name}.html"),
    )


@app.route("/styles.css")
def styles_route():
    return send_file(BASE_DIR / "styles.css")


@app.route("/script.js")
def script_route():
    return send_file(BASE_DIR / "script.js")


@app.route("/api/auth/signup", methods=["POST"])
def api_signup():
    data = request.get_json(silent=True) or {}
    first_name = (data.get("firstName") or "").strip()
    last_name = (data.get("lastName") or "").strip()
    email = (data.get("email") or "").strip().lower()
    password = (data.get("password") or "").strip()
    goal = (data.get("goal") or "").strip()
    language = (data.get("language") or "en").strip().lower()

    if not email or not password:
        return jsonify({"success": False, "error": "Email and password are required."}), 400
    if language not in {"en", "te", "hi"}:
        return jsonify({"success": False, "error": "Choose a supported language."}), 400

    conn = get_db_connection()
    existing = conn.execute("SELECT id FROM users WHERE email = ?", (email,)).fetchone()
    if existing:
        conn.close()
        return jsonify({"success": False, "error": "An account with this email already exists."}), 409

    user_id = conn.execute(
        "INSERT INTO users (email, first_name, last_name, password_hash, language) VALUES (?, ?, ?, ?, ?)",
        (email, first_name, last_name, generate_password_hash(password), language),
    ).lastrowid

    conn.execute(
        "INSERT INTO profiles (user_id, age, gender, height_cm, weight_kg, bmi, diabetes_category, health_conditions, food_preferences, activity_level, goals, notes) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)",
        (user_id, None, None, None, None, None, "Not specified", "", "", "Not specified", goal, ""),
    )
    conn.commit()
    conn.close()

    session.clear()
    session["user_id"] = user_id
    return jsonify({"success": True, "redirect": "/onboarding.html"})


@app.route("/api/auth/login", methods=["POST"])
def api_login():
    data = request.get_json(silent=True) or {}
    email = (data.get("email") or "").strip().lower()
    password = (data.get("password") or "").strip()

    if not email or not password:
        return jsonify({"success": False, "error": "Email and password are required."}), 400

    conn = get_db_connection()
    user = conn.execute("SELECT * FROM users WHERE email = ?", (email,)).fetchone()
    conn.close()

    if not user or not check_password_hash(user["password_hash"], password):
        return jsonify({"success": False, "error": "Invalid email or password."}), 401

    session.clear()
    session["user_id"] = user["id"]
    session["first_name"] = user["first_name"] or "User"
    return jsonify({"success": True, "redirect": "/dashboard.html", "language": user["language"] or "en"})


@app.route("/api/auth/logout", methods=["POST"])
def api_logout():
    session.clear()
    return jsonify({"success": True})


def parse_optional_number(value, label, *, integer=False, minimum=None, maximum=None):
    if value in (None, ""):
        return None
    try:
        number = int(value) if integer else float(value)
    except (TypeError, ValueError):
        raise ValueError(f"{label} must be a valid number.")
    if isinstance(number, float) and not math.isfinite(number):
        raise ValueError(f"{label} must be a valid number.")
    if minimum is not None and number < minimum:
        raise ValueError(f"{label} must be at least {minimum}.")
    if maximum is not None and number > maximum:
        raise ValueError(f"{label} must be no more than {maximum}.")
    return number


@app.route("/api/onboarding", methods=["POST"])
def api_onboarding():
    user = get_current_user()
    if not user:
        return jsonify({"success": False, "error": "Please log in to complete onboarding."}), 401

    data = request.get_json(silent=True) or {}
    age = data.get("age")
    gender = (data.get("gender") or "").strip() or None
    height_cm = data.get("height")
    weight_kg = data.get("weight")
    diabetes_category = (data.get("diabetesCategory") or "").strip() or "Not specified"
    activity_level = (data.get("activityLevel") or "").strip() or "Not specified"
    health_conditions = (data.get("healthConditions") or "").strip() or "Not provided"
    food_preferences = (data.get("foodPreferences") or "").strip() or "Not provided"
    lifestyle = (data.get("lifestyle") or "").strip() or "Not provided"
    goals = (data.get("goals") or "").strip() or "Goal not specified"
    notes = (data.get("notes") or "").strip() or "No extra notes provided."

    try:
        age_value = parse_optional_number(age, "Age", integer=True, minimum=1, maximum=120)
        height_value = parse_optional_number(height_cm, "Height", minimum=30, maximum=300)
        weight_value = parse_optional_number(weight_kg, "Weight", minimum=1, maximum=700)
    except ValueError as exc:
        return jsonify({"success": False, "error": str(exc)}), 400

    bmi_value = None
    if height_value is not None and weight_value is not None:
        bmi_value = round(weight_value / ((height_value / 100) ** 2), 1)

    conn = get_db_connection()
    existing = conn.execute("SELECT id FROM profiles WHERE user_id = ?", (user["id"],)).fetchone()
    if existing:
        conn.execute(
            """
            UPDATE profiles
            SET age = ?, gender = ?, height_cm = ?, weight_kg = ?, bmi = ?, diabetes_category = ?,
                health_conditions = ?, food_preferences = ?, activity_level = ?, lifestyle = ?, goals = ?,
                notes = ?, updated_at = ?
            WHERE user_id = ?
            """,
            (
                age_value,
                gender,
                height_value,
                weight_value,
                bmi_value,
                diabetes_category,
                health_conditions,
                food_preferences,
                activity_level,
                lifestyle,
                goals,
                notes,
                now_iso(),
                user["id"],
            ),
        )
    else:
        conn.execute(
            """
            INSERT INTO profiles (
                user_id, age, gender, height_cm, weight_kg, bmi, diabetes_category,
                health_conditions, food_preferences, activity_level, lifestyle, goals, notes
            ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            """,
            (
                user["id"],
                age_value,
                gender,
                height_value,
                weight_value,
                bmi_value,
                diabetes_category,
                health_conditions,
                food_preferences,
                activity_level,
                lifestyle,
                goals,
                notes,
            ),
        )
    conn.commit()
    conn.close()

    return jsonify({"success": True, "redirect": "/dashboard.html"})


@app.route("/api/me", methods=["GET"])
def api_current_user():
    user = get_current_user()
    if not user:
        return jsonify({"success": False, "error": "User not logged in."}), 401

    conn = get_db_connection()
    profile = conn.execute("SELECT * FROM profiles WHERE user_id = ?", (user["id"],)).fetchone()
    latest_record = conn.execute(
        "SELECT * FROM health_records WHERE user_id = ? ORDER BY record_date DESC, id DESC LIMIT 1",
        (user["id"],),
    ).fetchone()
    conn.close()

    return jsonify({
        "success": True,
        "user": {
            "id": user["id"],
            "email": user["email"],
            "firstName": user["first_name"],
            "lastName": user["last_name"],
            "language": user["language"] or "en",
        },
        "settings": {
            "reminders": bool(user["reminders_enabled"]),
            "notifications": bool(user["notifications_enabled"]),
            "privateMode": bool(user["private_mode"]),
        },
        "profile": dict(profile) if profile else None,
        "latestRecord": dict(latest_record) if latest_record else None,
    })


@app.route("/api/profile", methods=["PUT"])
def api_update_profile():
    user = get_current_user()
    if not user:
        return jsonify({"success": False, "error": "Please log in to update your profile."}), 401

    data = request.get_json(silent=True)
    if not isinstance(data, dict):
        return jsonify({"success": False, "error": "Profile details are required."}), 400

    first_name = (data.get("firstName") or "").strip()
    last_name = (data.get("lastName") or "").strip()
    email = (data.get("email") or "").strip().lower()
    if not first_name or not email:
        return jsonify({"success": False, "error": "First name and email are required."}), 400
    if "@" not in email or len(email) > 254:
        return jsonify({"success": False, "error": "Enter a valid email address."}), 400

    try:
        age = parse_optional_number(data.get("age"), "Age", integer=True, minimum=1, maximum=120)
        height = parse_optional_number(data.get("height"), "Height", minimum=30, maximum=300)
        weight = parse_optional_number(data.get("weight"), "Weight", minimum=1, maximum=700)
    except ValueError as exc:
        return jsonify({"success": False, "error": str(exc)}), 400

    bmi = round(weight / ((height / 100) ** 2), 1) if height and weight else None
    profile_values = (
        age,
        (data.get("gender") or "").strip(),
        height,
        weight,
        bmi,
        (data.get("diabetesCategory") or "").strip(),
        (data.get("healthConditions") or "").strip(),
        (data.get("foodPreferences") or "").strip(),
        (data.get("activityLevel") or "").strip(),
        (data.get("lifestyle") or "").strip(),
        (data.get("goals") or "").strip(),
        (data.get("notes") or "").strip(),
    )

    conn = get_db_connection()
    duplicate = conn.execute(
        "SELECT id FROM users WHERE email = ? AND id != ?",
        (email, user["id"]),
    ).fetchone()
    if duplicate:
        conn.close()
        return jsonify({"success": False, "error": "An account with this email already exists."}), 409

    conn.execute(
        "UPDATE users SET first_name = ?, last_name = ?, email = ? WHERE id = ?",
        (first_name, last_name, email, user["id"]),
    )
    conn.execute(
        """
        INSERT INTO profiles (
            user_id, age, gender, height_cm, weight_kg, bmi, diabetes_category,
            health_conditions, food_preferences, activity_level, lifestyle, goals, notes, updated_at
        ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        ON CONFLICT(user_id) DO UPDATE SET
            age = excluded.age, gender = excluded.gender, height_cm = excluded.height_cm,
            weight_kg = excluded.weight_kg, bmi = excluded.bmi,
            diabetes_category = excluded.diabetes_category,
            health_conditions = excluded.health_conditions,
            food_preferences = excluded.food_preferences, activity_level = excluded.activity_level,
            lifestyle = excluded.lifestyle, goals = excluded.goals, notes = excluded.notes,
            updated_at = excluded.updated_at
        """,
        (user["id"], *profile_values, now_iso()),
    )
    conn.commit()
    conn.close()

    return jsonify({"success": True})


@app.route("/api/settings/language", methods=["PUT"])
def api_update_language():
    user = get_current_user()
    if not user:
        return jsonify({"success": False, "error": "Please log in to save your settings."}), 401

    data = request.get_json(silent=True) or {}
    language = (data.get("language") or "").strip().lower()
    if language not in {"en", "te", "hi"}:
        return jsonify({"success": False, "error": "Choose a supported language."}), 400

    conn = get_db_connection()
    conn.execute("UPDATE users SET language = ? WHERE id = ?", (language, user["id"]))
    conn.commit()
    conn.close()
    return jsonify({"success": True, "language": language})


@app.route("/api/settings", methods=["PUT"])
def api_update_settings():
    user = get_current_user()
    if not user:
        return jsonify({"success": False, "error": "Please log in to save your settings."}), 401

    data = request.get_json(silent=True)
    setting_columns = {
        "reminders": "reminders_enabled",
        "notifications": "notifications_enabled",
        "privateMode": "private_mode",
    }
    if not isinstance(data, dict) or not data:
        return jsonify({"success": False, "error": "Settings are required."}), 400
    if any(key not in setting_columns for key in data):
        return jsonify({"success": False, "error": "Unsupported setting."}), 400
    if any(not isinstance(value, bool) for value in data.values()):
        return jsonify({"success": False, "error": "Setting values must be true or false."}), 400

    assignments = ", ".join(f"{setting_columns[key]} = ?" for key in data)
    conn = get_db_connection()
    conn.execute(
        f"UPDATE users SET {assignments} WHERE id = ?",
        (*[int(value) for value in data.values()], user["id"]),
    )
    conn.commit()
    conn.close()
    return jsonify({"success": True})


@app.route("/api/chat", methods=["POST"])
def api_chat():
    user = get_current_user()
    if not user:
        return jsonify({"success": False, "error": "Please log in to use the AI assistant."}), 401

    data = request.get_json(silent=True) or {}
    message = (data.get("message") or "").strip()
    language = (data.get("language") or user["language"] or "en").strip().lower()
    if language not in {"en", "te", "hi"}:
        language = user["language"] or "en"

    if not message:
        return jsonify({"success": False, "error": "Please enter a message for the assistant."}), 400

    session_id = session.get("chat_session_id")
    if session_id:
        session_row = get_chat_session_for_user(session_id, user["id"])
        if session_row is None:
            session_id = None

    if not session_id:
        session_id = create_chat_session(user["id"], "New chat")
        session["chat_session_id"] = session_id

    title = message.strip()
    if len(title) > 40:
        title = title[:37] + "..."
    conn = get_db_connection()
    current_title = conn.execute(
        "SELECT title FROM chat_sessions WHERE id = ?",
        (session_id,),
    ).fetchone()
    if current_title and current_title["title"] == "New chat":
        conn.execute(
            "UPDATE chat_sessions SET title = ?, updated_at = ? WHERE id = ?",
            (title, now_iso(), session_id),
        )
    conn.execute(
        "INSERT INTO chat_messages (session_id, sender, message, created_at) VALUES (?, ?, ?, ?)",
        (session_id, "user", message, now_iso()),
    )
    conn.commit()
    conn.close()

    try:
        reply = generate_assistant_reply(message, language, user["id"])
    except RuntimeError as exc:
        return jsonify({"success": False, "error": str(exc)}), 503

    save_chat_message(session_id, "assistant", reply)

    return jsonify({"success": True, "reply": reply, "language": language, "session_id": session_id})


@app.route("/api/chat/history", methods=["GET", "POST"])
def api_chat_history():
    user = get_current_user()
    if not user:
        return jsonify({"success": False, "error": "Please log in to use the AI assistant."}), 401

    data = request.get_json(silent=True) or {}
    action = (data.get("action") or "").strip().lower()
    session_id = data.get("session_id")

    if request.method == "GET":
        conversations = []
        for row in get_user_chat_sessions(user["id"]):
            messages = [dict(item) for item in get_chat_history(row["id"])]
            conversations.append({
                "id": row["id"],
                "title": row["title"],
                "created_at": row["created_at"],
                "updated_at": row["updated_at"],
                "messages": messages,
                "preview": messages[-1]["message"] if messages else "No messages yet.",
            })
        return jsonify({"success": True, "conversations": conversations})

    if action == "new":
        new_session_id = create_chat_session(user["id"], "New chat")
        session["chat_session_id"] = new_session_id
        return jsonify({"success": True, "session_id": new_session_id, "messages": []})

    if action == "open":
        if not session_id:
            return jsonify({"success": False, "error": "Conversation ID is required."}), 400
        session_row = get_chat_session_for_user(session_id, user["id"])
        if not session_row:
            return jsonify({"success": False, "error": "Conversation not found."}), 404
        session["chat_session_id"] = session_id
        messages = [dict(item) for item in get_chat_history(session_id)]
        return jsonify({"success": True, "session_id": session_id, "messages": messages})

    if action == "delete":
        if not session_id:
            return jsonify({"success": False, "error": "Conversation ID is required."}), 400
        session_row = get_chat_session_for_user(session_id, user["id"])
        if not session_row:
            return jsonify({"success": False, "error": "Conversation not found."}), 404
        conn = get_db_connection()
        conn.execute("DELETE FROM chat_messages WHERE session_id = ?", (session_id,))
        conn.execute(
            "DELETE FROM chat_sessions WHERE id = ? AND user_id = ?",
            (session_id, user["id"]),
        )
        conn.commit()
        conn.close()
        if session.get("chat_session_id") == session_id:
            session.pop("chat_session_id", None)
        return jsonify({"success": True})

    return jsonify({"success": False, "error": "Unsupported action."}), 400


@app.route("/api/diet/status", methods=["GET", "POST"])
def api_diet_status():
    user = get_current_user()
    if not user:
        return jsonify({"success": False, "error": "Please log in to view your diet status."}), 401

    payload = request.get_json(silent=True) or {}
    status_date = request.args.get("date") or payload.get("date") or datetime.utcnow().strftime("%Y-%m-%d")

    meal_names = ["Breakfast", "Lunch", "Snacks", "Dinner"]
    status_map = get_user_diet_status(user["id"], status_date)

    if request.method == "POST":
        data = request.get_json(silent=True) or {}
        meal_name = (data.get("meal") or "").strip()
        if meal_name not in meal_names:
            return jsonify({"success": False, "error": "Choose a valid meal."}), 400
        completed = bool(data.get("completed"))
        update_diet_status(user["id"], status_date, meal_name, completed)
        status_map = get_user_diet_status(user["id"], status_date)

    completed_count = sum(1 for meal_name in meal_names if status_map.get(meal_name, False))
    total_meals = len(meal_names)
    percentage = int(round((completed_count / total_meals) * 100)) if total_meals else 0

    history = []
    seen_dates = set()
    for row in get_user_diet_history(user["id"]):
        record_date = row["status_date"]
        if record_date in seen_dates:
            continue
        seen_dates.add(record_date)
        date_status = get_user_diet_status(user["id"], record_date)
        date_completed = sum(1 for meal_name in meal_names if date_status.get(meal_name, False))
        date_percentage = int(round((date_completed / total_meals) * 100)) if total_meals else 0
        history.append({
            "date": record_date,
            "percentage": date_percentage,
            "completed": date_completed,
            "total": total_meals,
        })

    return jsonify({
        "success": True,
        "date": status_date,
        "mealNames": meal_names,
        "status": {meal_name: bool(status_map.get(meal_name, False)) for meal_name in meal_names},
        "completed": completed_count,
        "total": total_meals,
        "percentage": percentage,
        "history": history,
    })


@app.route("/api/activity/status", methods=["GET", "POST"])
def api_activity_status():
    user = get_current_user()
    if not user:
        return jsonify({"success": False, "error": "Please log in to view your activity status."}), 401

    payload = request.get_json(silent=True) or {}
    status_date = request.args.get("date") or payload.get("date") or datetime.utcnow().strftime("%Y-%m-%d")
    activity_names = ["Morning walk", "Stretch and mobility", "Strength work"]

    if request.method == "POST":
        activity_name = (payload.get("activity") or "").strip()
        if activity_name not in activity_names:
            return jsonify({"success": False, "error": "Choose a valid activity."}), 400
        update_activity_status(
            user["id"],
            status_date,
            activity_name,
            bool(payload.get("completed")),
        )

    status_map = get_user_activity_status(user["id"], status_date)
    completed_count = sum(1 for name in activity_names if status_map.get(name, False))
    return jsonify({
        "success": True,
        "date": status_date,
        "activityNames": activity_names,
        "status": {name: bool(status_map.get(name, False)) for name in activity_names},
        "completed": completed_count,
        "total": len(activity_names),
        "percentage": int(round(completed_count / len(activity_names) * 100)),
    })


@app.route("/api/health-context")
def api_health_context():
    user = get_current_user()
    if not user:
        return jsonify({"success": False, "error": "User not logged in."}), 401

    context = get_user_profile_context(user["id"])
    return jsonify({"success": True, "context": context})


def medical_json_error(message, status=400):
    return jsonify({"success": False, "error": message}), status


def validate_medical_date(value, label, *, required=False):
    value = (value or "").strip() if isinstance(value, str) else ""
    if not value:
        if required:
            raise ValueError(f"{label} is required.")
        return None
    try:
        datetime.strptime(value, "%Y-%m-%d")
    except ValueError as exc:
        raise ValueError(f"{label} must be a valid date.") from exc
    return value


def validate_medical_datetime(value):
    value = (value or "").strip() if isinstance(value, str) else ""
    if not value:
        raise ValueError("Measurement date and time are required.")
    try:
        parsed = datetime.fromisoformat(value)
    except ValueError as exc:
        raise ValueError("Enter a valid measurement date and time.") from exc
    return parsed.strftime("%Y-%m-%d"), parsed.strftime("%H:%M")


def validate_reading_value(measurement_type, value):
    if measurement_type not in {"fasting", "postprandial", "random", "hba1c"}:
        raise ValueError("Choose a valid measurement type.")
    number = parse_optional_number(value, "Measurement value", minimum=1, maximum=2000)
    if number is None:
        raise ValueError("A measurement value is required.")
    if measurement_type == "hba1c" and number > 30:
        raise ValueError("HbA1c value must be no more than 30%.")
    return number, "%" if measurement_type == "hba1c" else "mg/dL"


def owned_report(report_id, user_id):
    conn = get_db_connection()
    report = conn.execute(
        "SELECT * FROM medical_reports WHERE id = ? AND user_id = ?",
        (report_id, user_id),
    ).fetchone()
    conn.close()
    return report


def public_report(report):
    return {
        "id": report["id"],
        "name": report["report_name"],
        "category": report["category"],
        "testDate": report["test_date"],
        "facilityName": report["facility_name"],
        "otherResults": report["other_results"],
        "verified": bool(report["verified"]),
        "uploadedAt": report["uploaded_at"],
        "verifiedAt": report["verified_at"],
    }


def extract_report_text(file_path, extension):
    if extension == ".pdf":
        from pypdf import PdfReader

        reader = PdfReader(str(file_path))
        if reader.is_encrypted:
            raise RuntimeError("This PDF is password protected. Upload an unlocked copy or enter results manually.")
        text = "\n".join(page.extract_text() or "" for page in reader.pages)
        if len(text.strip()) >= 20:
            return text

    swift_ocr = shutil.which("swift")
    if not swift_ocr:
        raise RuntimeError("Local OCR is unavailable. You can still enter report values manually.")

    swift_source = r'''
import AppKit
import Foundation
import PDFKit
import Vision

let fileURL = URL(fileURLWithPath: CommandLine.arguments[1])
let extensionName = fileURL.pathExtension.lowercased()
let request = VNRecognizeTextRequest()
request.recognitionLevel = .accurate
request.usesLanguageCorrection = true
request.recognitionLanguages = ["en-US"]
var output: [String] = []

func recognize(_ image: CGImage) throws {
    let handler = VNImageRequestHandler(cgImage: image)
    try handler.perform([request])
    output.append(contentsOf: (request.results ?? []).compactMap { $0.topCandidates(1).first?.string })
}

if extensionName == "pdf" {
    guard let document = PDFDocument(url: fileURL) else { throw NSError(domain: "HealthSyncOCR", code: 1) }
    for index in 0..<document.pageCount {
        guard let page = document.page(at: index),
              let image = page.thumbnail(of: NSSize(width: 2400, height: 3200), for: .mediaBox)
                .cgImage(forProposedRect: nil, context: nil, hints: nil) else { continue }
        try recognize(image)
    }
} else {
    guard let image = NSImage(contentsOf: fileURL),
          let cgImage = image.cgImage(forProposedRect: nil, context: nil, hints: nil) else {
        throw NSError(domain: "HealthSyncOCR", code: 2)
    }
    try recognize(cgImage)
}
print(output.joined(separator: "\n"))
'''
    try:
        result = subprocess.run(
            [swift_ocr, "-e", swift_source, str(file_path)],
            capture_output=True,
            text=True,
            timeout=90,
            check=False,
        )
    except subprocess.TimeoutExpired as exc:
        raise RuntimeError("Local report text extraction timed out. You can enter the values manually.") from exc
    if result.returncode != 0:
        raise RuntimeError("Local report text extraction failed. You can enter the values manually.")
    if not result.stdout.strip():
        raise RuntimeError("No readable report text was found. You can enter the values manually.")
    return result.stdout


def extract_report_values(text):
    labels = {
        "fasting": r"(?:fasting(?:\s+blood)?\s+(?:glucose|sugar)|fbs)",
        "postprandial": r"(?:post[\s-]?prandial(?:\s+blood)?(?:\s+glucose|sugar)?|after[\s-]?meal(?:\s+glucose)?|pp(?:bs)?)",
        "random": r"(?:random(?:\s+blood)?\s+(?:glucose|sugar)|rbs)",
        "hba1c": r"(?:hba1c|hb\s*a1c|a1c|glycated\s+ha?emoglobin)",
    }
    values = {}
    reported_values = {}
    for kind, label in labels.items():
        match = re.search(
            rf"{label}[\s\S]{{0,32}}?(\d{{1,4}}(?:\.\d+)?)\s*(mg\s*/?\s*dL|mmol\s*/?\s*L|mmol\s*/?\s*mol|%)?",
            text,
            re.IGNORECASE,
        )
        reported_values[kind] = (
            {"value": float(match.group(1)), "unit": re.sub(r"\s+", "", match.group(2) or "")}
            if match else None
        )
        value = reported_values[kind]
        expected_unit = "%" if kind == "hba1c" else "mg/dl"
        unit = value["unit"].lower() if value else ""
        values[kind] = value["value"] if value and unit == expected_unit else None

    iso_date = re.search(r"\b(20\d{2}-\d{2}-\d{2})\b", text)
    values["testDate"] = None
    if iso_date:
        try:
            values["testDate"] = validate_medical_date(iso_date.group(1), "Report date")
        except ValueError:
            pass
    values["reportedValues"] = reported_values
    return values


def medical_timeline(user_id, history, treatments, medications, reports, readings):
    events = []
    if history["has_previous_diabetes"] and history["diagnosis_date"]:
        events.append({
            "date": history["diagnosis_date"],
            "kind": "diagnosis",
            "title": "Diabetes diagnosis",
            "detail": history["diabetes_category"] or "",
        })
    for treatment in treatments:
        events.append({
            "date": treatment["started_on"] or treatment["created_at"][:10],
            "kind": "treatment",
            "title": "Treatment history",
            "detail": treatment["treatment_details"],
        })
    for medication in medications:
        events.append({
            "date": medication["started_on"] or medication["created_at"][:10],
            "kind": "medication",
            "title": "Medication started",
            "detail": medication["medication_name"],
        })
        if medication["discontinued_on"]:
            events.append({
                "date": medication["discontinued_on"],
                "kind": "medication",
                "title": "Medication discontinued",
                "detail": medication["medication_name"],
            })
    for report in reports:
        events.append({
            "date": report["test_date"] or report["uploaded_at"][:10],
            "kind": "report",
            "title": "Medical report",
            "detail": report["report_name"],
        })
    reading_types = {
        "fasting": "Fasting blood glucose",
        "postprandial": "Postprandial blood glucose",
        "random": "Random blood glucose",
        "hba1c": "HbA1c",
    }
    for reading in readings:
        events.append({
            "date": reading["measurement_date"],
            "kind": "reading",
            "title": reading_types[reading["measurement_type"]],
            "detail": f'{reading["value"]:g} {reading["unit"]}',
        })
    return sorted(events, key=lambda event: (event["date"], event["kind"]), reverse=True)


@app.route("/api/medical", methods=["GET"])
def api_medical_data():
    user = get_current_user()
    if not user:
        return medical_json_error("Please log in to view medical history.", 401)

    conn = get_db_connection()
    conn.execute(
        "INSERT OR IGNORE INTO patient_medical_history (user_id) VALUES (?)",
        (user["id"],),
    )
    history = conn.execute(
        "SELECT * FROM patient_medical_history WHERE user_id = ?", (user["id"],)
    ).fetchone()
    treatments = conn.execute(
        "SELECT * FROM treatment_history WHERE user_id = ? ORDER BY COALESCE(started_on, created_at) DESC, id DESC",
        (user["id"],),
    ).fetchall()
    medications = conn.execute(
        "SELECT * FROM medication_history WHERE user_id = ? ORDER BY COALESCE(started_on, created_at) DESC, id DESC",
        (user["id"],),
    ).fetchall()
    reports = conn.execute(
        "SELECT * FROM medical_reports WHERE user_id = ? ORDER BY COALESCE(test_date, uploaded_at) DESC, id DESC",
        (user["id"],),
    ).fetchall()
    readings = conn.execute(
        "SELECT * FROM blood_glucose_readings WHERE user_id = ? ORDER BY measurement_date DESC, measurement_time DESC, id DESC",
        (user["id"],),
    ).fetchall()
    conn.commit()
    conn.close()

    report_items = [public_report(report) for report in reports]
    reading_items = [dict(reading) for reading in readings]
    treatment_items = [dict(item) for item in treatments]
    medication_items = [dict(item) for item in medications]
    return jsonify({
        "success": True,
        "history": {
            "hasPreviousDiabetes": bool(history["has_previous_diabetes"]),
            "hasPreviousTreatment": bool(history["has_previous_treatment"]),
            "diagnosisDate": history["diagnosis_date"],
            "yearsWithDiabetes": history["years_with_diabetes"],
            "diabetesCategory": history["diabetes_category"] or "",
            "complications": history["complications"],
            "reportsConsent": bool(history["reports_consent"]),
            "updatedAt": history["updated_at"],
        },
        "treatments": treatment_items,
        "medications": medication_items,
        "reports": report_items,
        "readings": reading_items,
        "timeline": medical_timeline(
            user["id"], history, treatment_items, medication_items, reports, readings
        ),
    })


@app.route("/api/medical/history", methods=["PUT"])
def api_medical_history():
    user = get_current_user()
    if not user:
        return medical_json_error("Please log in to update medical history.", 401)
    data = request.get_json(silent=True)
    if not isinstance(data, dict):
        return medical_json_error("Medical history details are required.")

    diagnosed = data.get("hasPreviousDiabetes")
    if not isinstance(diagnosed, bool):
        return medical_json_error("Choose whether you have a previous diabetes diagnosis.")
    has_previous_treatment = data.get("hasPreviousTreatment")
    if not isinstance(has_previous_treatment, bool):
        return medical_json_error("Choose whether you have previously received treatment.")
    try:
        diagnosis_date = validate_medical_date(data.get("diagnosisDate"), "Diagnosis date")
        years = parse_optional_number(
            data.get("yearsWithDiabetes"), "Years with diabetes", minimum=0, maximum=120
        )
    except ValueError as exc:
        return medical_json_error(str(exc))
    if not diagnosed:
        diagnosis_date = None
        years = None

    category = (data.get("diabetesCategory") or "").strip()
    allowed_categories = {
        "", "Type 1", "Type 2", "Prediabetes", "Gestational Diabetes", "Other"
    }
    if category not in allowed_categories:
        return medical_json_error("Choose a valid diabetes category.")
    complications = (data.get("complications") or "").strip()
    if len(complications) > 4000:
        return medical_json_error("Complications must be no more than 4,000 characters.")

    conn = get_db_connection()
    conn.execute(
        """
        INSERT INTO patient_medical_history (
            user_id, has_previous_diabetes, diagnosis_date, years_with_diabetes,
            has_previous_treatment, diabetes_category, complications, updated_at
        ) VALUES (?, ?, ?, ?, ?, ?, ?, ?)
        ON CONFLICT(user_id) DO UPDATE SET
            has_previous_diabetes = excluded.has_previous_diabetes,
            has_previous_treatment = excluded.has_previous_treatment,
            diagnosis_date = excluded.diagnosis_date,
            years_with_diabetes = excluded.years_with_diabetes,
            diabetes_category = excluded.diabetes_category,
            complications = excluded.complications,
            updated_at = excluded.updated_at
        """,
        (
            user["id"], int(diagnosed), diagnosis_date, years, int(has_previous_treatment),
            category, complications, now_iso()
        ),
    )
    conn.commit()
    conn.close()
    return jsonify({"success": True})


@app.route("/api/medical/consent", methods=["PUT"])
def api_medical_consent():
    user = get_current_user()
    if not user:
        return medical_json_error("Please log in to update report consent.", 401)
    data = request.get_json(silent=True)
    if not isinstance(data, dict) or not isinstance(data.get("consent"), bool):
        return medical_json_error("Choose whether to allow private report storage and local processing.")
    conn = get_db_connection()
    conn.execute(
        """
        INSERT INTO patient_medical_history (user_id, reports_consent, consent_updated_at, updated_at)
        VALUES (?, ?, ?, ?)
        ON CONFLICT(user_id) DO UPDATE SET
            reports_consent = excluded.reports_consent,
            consent_updated_at = excluded.consent_updated_at,
            updated_at = excluded.updated_at
        """,
        (user["id"], int(data["consent"]), now_iso(), now_iso()),
    )
    conn.commit()
    conn.close()
    return jsonify({"success": True, "consent": data["consent"]})


@app.route("/api/medical/treatments", methods=["POST"])
def api_medical_add_treatment():
    user = get_current_user()
    if not user:
        return medical_json_error("Please log in to add treatment history.", 401)
    data = request.get_json(silent=True)
    if not isinstance(data, dict):
        return medical_json_error("Treatment details are required.")
    details = (data.get("details") or "").strip()
    provider = (data.get("provider") or "").strip()
    if not details or len(details) > 2000 or len(provider) > 300:
        return medical_json_error("Enter treatment details and keep each field within its length limit.")
    try:
        started_on = validate_medical_date(data.get("startedOn"), "Treatment start date")
        ended_on = validate_medical_date(data.get("endedOn"), "Treatment end date")
        if started_on and ended_on and ended_on < started_on:
            raise ValueError("Treatment end date cannot be before its start date.")
    except ValueError as exc:
        return medical_json_error(str(exc))
    conn = get_db_connection()
    cursor = conn.execute(
        """
        INSERT INTO treatment_history (user_id, treatment_details, provider_name, started_on, ended_on)
        VALUES (?, ?, ?, ?, ?)
        """,
        (user["id"], details, provider, started_on, ended_on),
    )
    treatment_id = cursor.lastrowid
    conn.commit()
    conn.close()
    return jsonify({"success": True, "id": treatment_id})


@app.route("/api/medical/treatments/<int:treatment_id>", methods=["PUT", "DELETE"])
def api_medical_treatment(treatment_id):
    user = get_current_user()
    if not user:
        return medical_json_error("Please log in to update treatment history.", 401)
    conn = get_db_connection()
    existing = conn.execute(
        "SELECT id FROM treatment_history WHERE id = ? AND user_id = ?",
        (treatment_id, user["id"]),
    ).fetchone()
    if not existing:
        conn.close()
        return medical_json_error("Treatment record not found.", 404)
    if request.method == "DELETE":
        conn.execute(
            "DELETE FROM treatment_history WHERE id = ? AND user_id = ?",
            (treatment_id, user["id"]),
        )
        conn.commit()
        conn.close()
        return jsonify({"success": True})
    data = request.get_json(silent=True)
    if not isinstance(data, dict):
        conn.close()
        return medical_json_error("Treatment details are required.")
    details = (data.get("details") or "").strip()
    provider = (data.get("provider") or "").strip()
    if not details or len(details) > 2000 or len(provider) > 300:
        conn.close()
        return medical_json_error("Enter treatment details and keep each field within its length limit.")
    try:
        started_on = validate_medical_date(data.get("startedOn"), "Treatment start date")
        ended_on = validate_medical_date(data.get("endedOn"), "Treatment end date")
        if started_on and ended_on and ended_on < started_on:
            raise ValueError("Treatment end date cannot be before its start date.")
    except ValueError as exc:
        conn.close()
        return medical_json_error(str(exc))
    conn.execute(
        """
        UPDATE treatment_history SET treatment_details = ?, provider_name = ?,
            started_on = ?, ended_on = ?, updated_at = ?
        WHERE id = ? AND user_id = ?
        """,
        (details, provider, started_on, ended_on, now_iso(), treatment_id, user["id"]),
    )
    conn.commit()
    conn.close()
    return jsonify({"success": True})


def medication_values(data):
    name = (data.get("name") or "").strip()
    dosage = (data.get("dosage") or "").strip()
    frequency = (data.get("frequency") or "").strip()
    duration = (data.get("duration") or "").strip()
    reason = (data.get("discontinuationReason") or "").strip()
    current = data.get("isCurrent")
    if not name or len(name) > 200 or len(dosage) > 200 or len(frequency) > 200 or len(duration) > 200:
        raise ValueError("Enter a medicine name and keep medication details within their length limits.")
    if not isinstance(current, bool):
        raise ValueError("Choose whether you are currently taking this medicine.")
    started_on = validate_medical_date(data.get("startedOn"), "Medication start date")
    discontinued_on = validate_medical_date(
        data.get("discontinuedOn"), "Medication discontinuation date"
    )
    if current and discontinued_on:
        raise ValueError("A current medicine cannot have a discontinuation date.")
    if not current and discontinued_on and started_on and discontinued_on < started_on:
        raise ValueError("Medication discontinuation date cannot be before its start date.")
    if len(reason) > 2000:
        raise ValueError("Discontinuation reason must be no more than 2,000 characters.")
    return name, dosage, frequency, started_on, duration, int(current), discontinued_on, reason


@app.route("/api/medical/medications", methods=["POST"])
def api_medical_add_medication():
    user = get_current_user()
    if not user:
        return medical_json_error("Please log in to add medication history.", 401)
    data = request.get_json(silent=True)
    if not isinstance(data, dict):
        return medical_json_error("Medication details are required.")
    try:
        values = medication_values(data)
    except ValueError as exc:
        return medical_json_error(str(exc))
    conn = get_db_connection()
    cursor = conn.execute(
        """
        INSERT INTO medication_history (
            user_id, medication_name, dosage, frequency, started_on, duration,
            is_current, discontinued_on, discontinuation_reason
        ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
        """,
        (user["id"], *values),
    )
    medication_id = cursor.lastrowid
    conn.commit()
    conn.close()
    return jsonify({"success": True, "id": medication_id})


@app.route("/api/medical/medications/<int:medication_id>", methods=["PUT", "DELETE"])
def api_medical_medication(medication_id):
    user = get_current_user()
    if not user:
        return medical_json_error("Please log in to update medication history.", 401)
    conn = get_db_connection()
    existing = conn.execute(
        "SELECT id FROM medication_history WHERE id = ? AND user_id = ?",
        (medication_id, user["id"]),
    ).fetchone()
    if not existing:
        conn.close()
        return medical_json_error("Medication record not found.", 404)
    if request.method == "DELETE":
        conn.execute(
            "DELETE FROM medication_history WHERE id = ? AND user_id = ?",
            (medication_id, user["id"]),
        )
        conn.commit()
        conn.close()
        return jsonify({"success": True})

    data = request.get_json(silent=True)
    if not isinstance(data, dict):
        conn.close()
        return medical_json_error("Medication details are required.")
    try:
        values = medication_values(data)
    except ValueError as exc:
        conn.close()
        return medical_json_error(str(exc))
    conn.execute(
        """
        UPDATE medication_history SET medication_name = ?, dosage = ?, frequency = ?,
            started_on = ?, duration = ?, is_current = ?, discontinued_on = ?,
            discontinuation_reason = ?, updated_at = ?
        WHERE id = ? AND user_id = ?
        """,
        (*values, now_iso(), medication_id, user["id"]),
    )
    conn.commit()
    conn.close()
    return jsonify({"success": True})


@app.route("/api/medical/reports", methods=["POST"])
def api_medical_upload_report():
    user = get_current_user()
    if not user:
        return medical_json_error("Please log in to upload medical reports.", 401)

    conn = get_db_connection()
    consent = conn.execute(
        "SELECT reports_consent FROM patient_medical_history WHERE user_id = ?",
        (user["id"],),
    ).fetchone()
    conn.close()
    if not consent or not consent["reports_consent"]:
        return medical_json_error("Confirm private report storage and local processing before uploading.")

    uploaded_file = request.files.get("report")
    if not uploaded_file or not uploaded_file.filename:
        return medical_json_error("Choose a PDF, JPG, JPEG, or PNG report to upload.")
    original_name = secure_filename(uploaded_file.filename)
    extension = Path(original_name).suffix.lower()
    if extension not in MEDICAL_REPORT_TYPES:
        return medical_json_error("Only PDF, JPG, JPEG, and PNG reports are supported.")
    category = request.form.get("category", "").strip()
    if category not in {"before_treatment", "after_treatment"}:
        return medical_json_error("Choose a valid report category.")
    report_name = (request.form.get("reportName") or original_name).strip()[:180]
    facility = (request.form.get("facilityName") or "").strip()[:300]
    if not report_name:
        report_name = f"Medical report {datetime.utcnow().strftime('%Y-%m-%d')}"
    try:
        test_date = validate_medical_date(request.form.get("testDate"), "Test date")
    except ValueError as exc:
        return medical_json_error(str(exc))
    content = uploaded_file.read(MAX_MEDICAL_REPORT_BYTES + 1)
    if not content:
        return medical_json_error("The selected report is empty.")
    if len(content) > MAX_MEDICAL_REPORT_BYTES:
        return medical_json_error("Report files must be 10 MB or smaller.")
    _, signature = MEDICAL_REPORT_TYPES[extension]
    if not content.startswith(signature):
        return medical_json_error("The file contents do not match the selected report format.")

    MEDICAL_PRIVATE_DIR.mkdir(parents=True, exist_ok=True, mode=0o700)
    MEDICAL_REPORTS_DIR.mkdir(parents=True, exist_ok=True, mode=0o700)
    os.chmod(MEDICAL_PRIVATE_DIR, 0o700)
    os.chmod(MEDICAL_REPORTS_DIR, 0o700)
    stored_name = f"{uuid.uuid4().hex}{extension}"
    stored_path = MEDICAL_REPORTS_DIR / stored_name
    file_descriptor = os.open(stored_path, os.O_WRONLY | os.O_CREAT | os.O_EXCL, 0o600)
    with os.fdopen(file_descriptor, "wb") as private_file:
        private_file.write(content)
    uploaded_at = now_iso()
    conn = get_db_connection()
    cursor = conn.execute(
        """
        INSERT INTO medical_reports (
            user_id, stored_name, report_name, category, test_date, facility_name, uploaded_at
        ) VALUES (?, ?, ?, ?, ?, ?, ?)
        """,
        (user["id"], stored_name, report_name, category, test_date, facility, uploaded_at),
    )
    report_id = cursor.lastrowid
    conn.commit()
    conn.close()

    try:
        report_text = extract_report_text(stored_path, extension)
        extracted = extract_report_values(report_text)
        extraction = {"success": True, "values": extracted, "error": ""}
    except (PdfReadError, RuntimeError, OSError, subprocess.SubprocessError, ValueError) as exc:
        extraction = {"success": False, "values": {}, "error": str(exc)}
    return jsonify({
        "success": True,
        "report": {
            "id": report_id,
            "name": report_name,
            "category": category,
            "testDate": test_date,
            "facilityName": facility,
            "uploadedAt": uploaded_at,
            "verified": False,
        },
        "extraction": extraction,
    }), 201


@app.route("/api/medical/reports/<int:report_id>/verify", methods=["PUT"])
def api_medical_verify_report(report_id):
    user = get_current_user()
    if not user:
        return medical_json_error("Please log in to verify report results.", 401)
    report = owned_report(report_id, user["id"])
    if not report:
        return medical_json_error("Medical report not found.", 404)
    data = request.get_json(silent=True)
    if not isinstance(data, dict):
        return medical_json_error("Verified report details are required.")
    try:
        test_date = validate_medical_date(data.get("testDate"), "Test date", required=True)
        measurements = []
        confirmed = data.get("confirmed")
        if not isinstance(confirmed, dict):
            raise ValueError("Confirm each measurement you reviewed.")
        for kind in ("fasting", "postprandial", "random", "hba1c"):
            if confirmed.get(kind) is True:
                value, unit = validate_reading_value(kind, data.get(kind))
                measurements.append((kind, value, unit))
        if not measurements and not (data.get("otherResults") or "").strip():
            raise ValueError("Confirm at least one measurement or enter other test results.")
    except ValueError as exc:
        return medical_json_error(str(exc))
    facility = (data.get("facilityName") or "").strip()[:300]
    other_results = (data.get("otherResults") or "").strip()
    if len(other_results) > 4000:
        return medical_json_error("Other test results must be no more than 4,000 characters.")

    conn = get_db_connection()
    conn.execute(
        """
        UPDATE medical_reports SET test_date = ?, facility_name = ?, other_results = ?,
            verified = 1, verified_at = ?
        WHERE id = ? AND user_id = ?
        """,
        (test_date, facility, other_results, now_iso(), report_id, user["id"]),
    )
    for kind, value, unit in measurements:
        conn.execute(
            """
            INSERT INTO blood_glucose_readings (
                user_id, report_id, measurement_type, value, unit, measurement_date,
                measurement_time, source, created_at, updated_at
            ) VALUES (?, ?, ?, ?, ?, ?, NULL, 'report', ?, ?)
            ON CONFLICT(report_id, measurement_type) DO UPDATE SET
                value = excluded.value, unit = excluded.unit,
                measurement_date = excluded.measurement_date, updated_at = excluded.updated_at
            """,
            (user["id"], report_id, kind, value, unit, test_date, now_iso(), now_iso()),
        )
    conn.commit()
    conn.close()
    return jsonify({"success": True, "confirmedMeasurements": len(measurements)})


@app.route("/api/medical/reports/<int:report_id>/file", methods=["GET"])
def api_medical_report_file(report_id):
    user = get_current_user()
    if not user:
        return medical_json_error("Please log in to view medical reports.", 401)
    report = owned_report(report_id, user["id"])
    if not report:
        return medical_json_error("Medical report not found.", 404)
    extension = Path(report["stored_name"]).suffix.lower()
    expected_mime, _ = MEDICAL_REPORT_TYPES[extension]
    file_path = MEDICAL_REPORTS_DIR / report["stored_name"]
    if not file_path.is_file():
        return medical_json_error("The private report file is unavailable.", 404)
    response = send_file(
        file_path,
        mimetype=expected_mime,
        as_attachment=request.args.get("download") == "1",
        download_name=report["report_name"] + extension,
        conditional=False,
        max_age=0,
    )
    response.headers["Cache-Control"] = "private, no-store"
    response.headers["X-Content-Type-Options"] = "nosniff"
    response.headers["Content-Security-Policy"] = "default-src 'none'; sandbox"
    return response


@app.route("/api/medical/reports/<int:report_id>", methods=["DELETE"])
def api_medical_delete_report(report_id):
    user = get_current_user()
    if not user:
        return medical_json_error("Please log in to delete medical reports.", 401)
    report = owned_report(report_id, user["id"])
    if not report:
        return medical_json_error("Medical report not found.", 404)
    file_path = MEDICAL_REPORTS_DIR / report["stored_name"]
    conn = get_db_connection()
    conn.execute(
        "DELETE FROM blood_glucose_readings WHERE report_id = ? AND user_id = ?",
        (report_id, user["id"]),
    )
    conn.execute(
        "DELETE FROM medical_reports WHERE id = ? AND user_id = ?",
        (report_id, user["id"]),
    )
    conn.commit()
    conn.close()
    file_path.unlink(missing_ok=True)
    return jsonify({"success": True})


@app.route("/api/medical/readings", methods=["POST"])
def api_medical_add_reading():
    user = get_current_user()
    if not user:
        return medical_json_error("Please log in to add blood glucose readings.", 401)
    data = request.get_json(silent=True)
    if not isinstance(data, dict):
        return medical_json_error("Measurement details are required.")
    try:
        measurement_date, measurement_time = validate_medical_datetime(data.get("measuredAt"))
        measurement_type = (data.get("type") or "").strip()
        value, unit = validate_reading_value(measurement_type, data.get("value"))
    except ValueError as exc:
        return medical_json_error(str(exc))
    conn = get_db_connection()
    cursor = conn.execute(
        """
        INSERT INTO blood_glucose_readings (
            user_id, measurement_type, value, unit, measurement_date, measurement_time,
            source, created_at, updated_at
        ) VALUES (?, ?, ?, ?, ?, ?, 'manual', ?, ?)
        """,
        (user["id"], measurement_type, value, unit, measurement_date, measurement_time, now_iso(), now_iso()),
    )
    reading_id = cursor.lastrowid
    conn.commit()
    conn.close()
    return jsonify({"success": True, "id": reading_id}), 201


@app.route("/api/medical/readings/<int:reading_id>", methods=["PUT", "DELETE"])
def api_medical_reading(reading_id):
    user = get_current_user()
    if not user:
        return medical_json_error("Please log in to update blood glucose readings.", 401)
    conn = get_db_connection()
    existing = conn.execute(
        "SELECT * FROM blood_glucose_readings WHERE id = ? AND user_id = ?",
        (reading_id, user["id"]),
    ).fetchone()
    if not existing:
        conn.close()
        return medical_json_error("Blood glucose reading not found.", 404)
    if request.method == "DELETE":
        if existing["report_id"] is not None:
            conn.close()
            return medical_json_error("Delete or re-verify the medical report to change its confirmed results.")
        conn.execute(
            "DELETE FROM blood_glucose_readings WHERE id = ? AND user_id = ?",
            (reading_id, user["id"]),
        )
        conn.commit()
        conn.close()
        return jsonify({"success": True})
    data = request.get_json(silent=True)
    if not isinstance(data, dict):
        conn.close()
        return medical_json_error("Measurement details are required.")
    try:
        measurement_date, measurement_time = validate_medical_datetime(data.get("measuredAt"))
        value, unit = validate_reading_value(existing["measurement_type"], data.get("value"))
    except ValueError as exc:
        conn.close()
        return medical_json_error(str(exc))
    conn.execute(
        """
        UPDATE blood_glucose_readings SET value = ?, unit = ?, measurement_date = ?,
            measurement_time = ?, updated_at = ? WHERE id = ? AND user_id = ?
        """,
        (value, unit, measurement_date, measurement_time, now_iso(), reading_id, user["id"]),
    )
    conn.commit()
    conn.close()
    return jsonify({"success": True})


@app.route("/api/medical/assistant", methods=["POST"])
def api_medical_assistant():
    user = get_current_user()
    if not user:
        return medical_json_error("Please log in to use the medical report assistant.", 401)
    data = request.get_json(silent=True)
    if not isinstance(data, dict):
        return medical_json_error("Ask a question about your confirmed report results.")
    question = (data.get("question") or "").strip()
    if len(question) > 1000:
        return medical_json_error("Questions must be no more than 1,000 characters.")

    conn = get_db_connection()
    consent = conn.execute(
        "SELECT reports_consent FROM patient_medical_history WHERE user_id = ?",
        (user["id"],),
    ).fetchone()
    readings = conn.execute(
        """
        SELECT measurement_type, value, unit, measurement_date, measurement_time
        FROM blood_glucose_readings WHERE user_id = ? AND
            (report_id IS NULL OR report_id IN (
                SELECT id FROM medical_reports WHERE user_id = ? AND verified = 1
            ))
        ORDER BY measurement_date DESC, measurement_time DESC LIMIT 80
        """,
        (user["id"], user["id"]),
    ).fetchall()
    verified_reports = conn.execute(
        """
        SELECT report_name, category, test_date, facility_name, other_results
        FROM medical_reports WHERE user_id = ? AND verified = 1
        ORDER BY COALESCE(test_date, uploaded_at) DESC LIMIT 10
        """,
        (user["id"],),
    ).fetchall()
    conn.close()
    if not consent or not consent["reports_consent"]:
        return medical_json_error("Enable report processing consent before using the report assistant.")

    language = user["language"] or "en"
    language_instruction = {
        "en": "Answer in English.",
        "te": "Answer entirely in Telugu using Telugu script.",
        "hi": "Answer entirely in Hindi using Devanagari script.",
    }.get(language, "Answer in English.")
    confirmed_context = {
        "confirmed_readings": [dict(row) for row in readings],
        "verified_reports": [dict(row) for row in verified_reports],
    }
    prompt = f"""
You are the HealthSync local medical report explainer. {language_instruction}
Explain medical terms in plain, supportive language and compare only the confirmed values below.
Never invent or infer missing values, dates, units, diagnoses, or trends. State when information is absent.
Explain that measurements require interpretation by a qualified healthcare professional in clinical context.
Do not diagnose, prescribe, recommend changing or stopping medicine, or say a person is cured.
Do not treat a lower reading as automatically better. Mention change direction only, not clinical improvement.
The uploaded document contents are not available to you; use only the confirmed structured details below.

Confirmed patient data:
{json.dumps(confirmed_context, ensure_ascii=False)}

Patient question:
{question or "Explain the confirmed results and recorded changes in simple language."}
"""
    try:
        ensure_ollama_ready()
        response = requests.post(
            OLLAMA_URL,
            json={"model": ELLAMA_MODEL, "prompt": prompt, "stream": False, "options": {"temperature": 0.2}},
            timeout=120,
        )
        response.raise_for_status()
    except (RuntimeError, requests.exceptions.RequestException) as exc:
        return medical_json_error(str(exc), 503)
    try:
        reply = response.json().get("response", "").strip()
    except (ValueError, AttributeError):
        return medical_json_error("The local Ollama model returned an invalid response. Please try again.", 502)
    if not reply:
        return medical_json_error("The local Ollama model returned an empty explanation. Please try again.", 502)
    return jsonify({"success": True, "answer": reply, "localProcessing": True})


@app.errorhandler(413)
def medical_upload_too_large(_error):
    if request.path.startswith("/api/medical/"):
        return medical_json_error("Report files must be 10 MB or smaller.", 413)
    return "Request too large.", 413


init_db()


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)
