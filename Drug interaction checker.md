#copilot prompt:Act as a senior full-stack developer and healthcare application designer.

I want to enhance my existing web application HealthSync – Personalized Diabetes Health Assistant by adding two important medical features.

IMPORTANT:

- Do not redesign or remove existing features.
- Maintain the current UI/UX design, colors, layout, and navigation.
- Integrate these features into the existing application.
- Make all buttons and functionalities properly working.
- Ensure responsive design for desktop and mobile.

1. Medical Report Upload & Comparison System

Improve the existing Medical Reports section.

A. Report Upload

- Allow patients to upload medical reports in PDF, JPG, JPEG, and PNG formats.
- Maximum file size: 10 MB.
- Provide two clearly separated upload options:
  1. Earlier Report
  2. Later Report
- Allow users to select and upload reports independently.
- Automatically extract relevant medical information from uploaded reports using local processing wherever possible.
- Extract test names, values, units, reference ranges, and test dates.
- Store uploaded reports with their original test dates, not just upload dates.
- Display uploaded reports in a report history section.

B. Report Comparison

When a patient uploads two reports, allow them to select:

- Earlier Report (Previous Checkup)
- Later Report (Recent Checkup)

Add a working button called "Compare Reports".

Display a comparison dashboard showing:

- Previous test values.
- Current test values.
- Difference between values.
- Whether the value increased or decreased.
- Whether the value is within the normal reference range.
- Improvements and values that need attention.

Include comparisons for diabetes-related tests such as:

- Fasting Blood Sugar
- Postprandial Blood Sugar
- HbA1c
- Random Blood Sugar
- Cholesterol
- Creatinine and other available tests.

Use simple charts and visual indicators to make changes easy to understand.

IMPORTANT:
Do not assume that an increased value is always bad or a decreased value is always good. Interpret results according to the specific test and its reference range.

Show a disclaimer that report comparisons are informational and must be reviewed by a healthcare professional.

2. Drug Interaction Checker

Create a new feature called Drug Interaction Checker.

This feature should help patients identify potential interactions between multiple medicines and food items.

A. Multiple Medicine Input

Allow patients to:

- Add 4–5 or more medicines.
- Enter medicine name or brand name.
- Enter dosage and frequency (optional).
- Add or remove medicines dynamically.
- Select medicines from suggestions if a verified medicine database is available.

Add a button: "Check Drug Interactions".

B. Medicine-to-Medicine Interaction

Check whether any two or more medicines interact with each other.

For example:
If a patient takes 5 different medicines, analyze possible interactions between all the medicines.

Display:

- Medicine combinations that may interact.
- Interaction severity: Minor, Moderate, Major, or Contraindicated.
- Why the interaction may occur.
- Possible side effects or risks.
- Recommended precautions.
- When the patient should consult their doctor or pharmacist.

Do not invent interactions. Use a verified drug interaction database or trusted medical information source.

C. Medicine-to-Food Interaction

Add a separate section called "Food & Medicine Interactions".

Identify foods, beverages, or dietary items that may interact with the patient's medicines.

For example:

- Grapefruit and certain medicines.
- Vitamin K-rich foods and warfarin.
- Dairy products and certain antibiotics.
- Alcohol and medicines that have alcohol-related warnings.

For each interaction, show:

- Medicine name.
- Food or beverage involved.
- Type of interaction.
- Possible health risks.
- Whether the food should be avoided, limited, or consumed with precautions.

Do not give blanket food restrictions. Recommendations must depend on the particular medicine and verified evidence.

D. Interaction Results Dashboard

Display results in a clean dashboard with:

- Total medicines analyzed.
- Number of potential interactions found.
- Severity indicators.
- Medicine-to-medicine interactions.
- Medicine-to-food interactions.
- Safety precautions.

Allow patients to save and view previous interaction check results.

3. Safety and Reliability

This is a healthcare application, so accuracy is extremely important.

- Never generate fake drug interaction information.
- If reliable interaction data is unavailable, clearly display "Interaction information unavailable".
- Do not treat AI-generated responses as medically verified information.
- Do not recommend stopping, starting, or changing medicine dosages.
- Advise patients to consult their doctor or pharmacist before making medication changes.
- Clearly highlight serious interactions and urgent warning signs.
- Protect patient medical reports and medication information.
- Do not send sensitive medical documents to external AI services without explicit patient consent.

4. UI/UX Requirements

Maintain HealthSync's existing professional healthcare dashboard.

Add two sections:

1. Medical Reports & Comparison
2. Drug Interaction Checker

Use:

- Modern cards.
- Clear labels.
- Simple charts.
- Responsive layouts.
- Easy-to-understand medical explanations.
- Loading indicators and error messages.
- Empty states when no reports or medicines are available.

5. Functional Requirements

- Every upload button must work.
- Report comparison must use actual extracted values.
- Medicine input must support multiple entries.
- Interaction checking must use verified information.
- Save and retrieve previous reports and interaction history.
- Validate uploaded file types and sizes.
- Handle missing or unreadable report data gracefully.

Before implementing, inspect the existing project structure and reuse the current technologies and architecture. Do not unnecessarily replace existing files or break existing functionality.

First implement the complete frontend and working interactions. If a verified medical database or backend integration is required, clearly identify that requirement instead of displaying fake results.
