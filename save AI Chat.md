MASTER PROMPT – HEALTHSYNC

Personalized Diabetes Health Assistant – Complete Full-Stack Web Application

ROLE

Act as a Senior Full-Stack Developer, Python Flask Backend Developer, AI/ML Engineer and Professional UI/UX Designer.

Build, integrate, debug and test my existing web application called HealthSync – Personalized Diabetes Health Assistant.

The goal is to create a complete, functional, user-friendly diabetes health management platform with a locally running AI assistant.

IMPORTANT PROJECT INSTRUCTIONS

1. First inspect my entire existing project structure and all source files.
2. Understand the existing frontend, backend, database, authentication and AI integration.
3. Reuse existing files and functionality wherever possible.
4. Do not unnecessarily create duplicate files, functions, API routes or database tables.
5. Do not delete existing working features.
6. Do not redesign or replace my existing UI/UX.
7. Fix actual problems instead of adding duplicate code.
8. Implement all features completely, not just create sample or incomplete files.
9. Test the functionality before declaring the work complete.

My development environment:

- Operating System: macOS
- Device: MacBook
- Python: 3.13
- Editor: VS Code

---

1. TECHNOLOGY STACK

Use the following technologies:

Frontend

- HTML5
- CSS3
- Vanilla JavaScript
- No React
- No unnecessary frontend frameworks

Backend

- Python 3.13
- Flask

Database

- SQLite

Local AI

- Ollama
- Model: llama3.2:3b

Avoid unnecessary libraries and complex architecture.

2. UI/UX DESIGN

Maintain my existing HealthSync design.

Design requirements:

- Clean, modern healthcare interface.
- White/light background.
- Teal and green healthcare theme.
- Rounded cards.
- Soft shadows.
- Modern typography.
- Responsive layout for laptop, tablet and mobile.
- Consistent navigation and buttons.
- Simple and user-friendly interface.

Do not change existing colors, layouts, components or visual identity unnecessarily.

3. REQUIRED APPLICATION PAGES

Maintain and integrate these pages:

1. Landing / Home
2. Login
3. Signup
4. User Onboarding / Health Information
5. Dashboard
6. Diet Planner
7. Activities
8. Progress / History
9. AI Assistant
10. Profile / Settings

All navigation links, buttons and page interactions must work correctly.

4. FLASK BACKEND AND SQLITE DATABASE

Create or integrate the backend using Python Flask and SQLite.

Automatically initialize the existing database if it does not exist.

Create or update the following tables as required:

Users

- id
- name
- email
- password_hash
- preferred_language
- created_at

Health Profiles

- id
- user_id
- age
- gender
- height
- weight
- bmi
- diabetes_status
- food_preference

Daily Health Records

- id
- user_id
- record_date
- glucose
- blood_pressure
- weight
- notes

Daily Diet Plans

- id
- user_id
- plan_date
- breakfast
- lunch
- snacks
- dinner
- alternative_meals

Daily Activities

- id
- user_id
- activity_date
- activity_name
- duration
- completed

Health History

- id
- user_id
- record_date
- bmi
- diabetes_status
- notes

AI Conversations

- id
- user_id
- conversation_title
- created_at
- updated_at

AI Chat Messages

- id
- conversation_id
- user_id
- role
- message
- created_at

Diet Completion Tracking

- id
- user_id
- plan_date
- meal_type
- selected_meal
- completed
- updated_at

Use:

- Primary keys
- Foreign keys
- Proper database relationships
- Appropriate indexes
- Unique constraints where necessary

Do not create duplicate tables if equivalent tables already exist. Use database migrations or safe schema updates without losing existing user data.

5. USER AUTHENTICATION

Implement complete authentication:

- User signup
- User login
- User logout
- Secure password hashing
- Flask session management
- Protected application pages
- User-specific data access

Requirements:

- Users should remain logged in while their valid session is active.
- Passwords must never be stored as plain text.
- Prevent unauthorized access to personal information.
- Each user must access only their own records.

Use secure session settings and validate all user inputs.

6. USER HEALTH PROFILE

Allow users to save and update:

- Name
- Age
- Gender
- Height
- Weight
- BMI
- Diabetes category
- Food preferences
- Preferred language
- Available health conditions and relevant health information

Support diabetes categories such as:

- Type 1 Diabetes
- Type 2 Diabetes
- Prediabetes
- Gestational Diabetes
- No Diabetes / General Health

Calculate BMI automatically using height and weight.

Save profile changes in SQLite.

Do not assume a user has diabetes simply because they use this application.

7. DASHBOARD

Create a personalized dashboard displaying:

- Diabetes status / risk information
- BMI
- Today's diet summary
- Today's activities
- Daily diet completion
- Activity completion
- Overall progress
- Health summary

All information must come from the logged-in user's actual database records.

Update dashboard information whenever the user completes meals, activities or updates their health profile.

8. PERSONALIZED DAILY DIET PLANNER

Implement a personalized Indian diet planner.

Include:

- Breakfast
- Lunch
- Snacks
- Dinner

Food recommendations should include:

- Andhra cuisine
- South Indian homemade food
- Common Indian household meals
- Healthy and affordable alternatives

For each meal:

- Show the recommended food.
- Provide 2–3 alternative meal options.
- Allow users to select an alternative.
- Save the selected meal.
- Preserve previous days' diet plans.

Recommendations should consider:

- Diabetes category
- BMI
- Food preferences
- Available health information
- Individual dietary requirements

Do not force users to prepare completely separate meals from their family.

Provide practical alternatives using commonly available household ingredients.

Where suitable, provide food purchasing links through available food delivery platforms, without inventing product availability or links.

9. DAILY DIET TRACKING AND COMPLETION PERCENTAGE

Implement a complete meal completion tracking system.

Add a checkbox next to:

1. Breakfast
2. Lunch
3. Snacks
4. Dinner

Functionality:

- Users can tick a checkbox after consuming a meal.
- Users can untick it if necessary.
- Save checkbox status in SQLite.
- Track each user's meals separately for each date.
- Save the selected alternative meal.
- Allow the selected alternative to be marked completed.
- Preserve completion status after refreshing or reopening the website.

Diet completion calculation:

Percentage = (Completed meals / Total meals) × 100

Examples:

- 0/4 = 0%
- 1/4 = 25%
- 2/4 = 50%
- 3/4 = 75%
- 4/4 = 100%

Display:

- Completion percentage at the top of the Diet page.
- A visual progress bar.
- Immediate percentage updates whenever a checkbox changes.

Save previous days' completion records.

For a new date, start a new tracking record without deleting previous records.

Display previous diet completion percentages in the history section.

10. DAILY ACTIVITIES AND EXERCISE TRACKING

Implement personalized daily activities.

Include:

- Walking suggestions
- Basic exercises
- Physical activity recommendations
- Activity duration
- Completion checkboxes

Allow users to:

- View recommended activities.
- Mark activities as completed.
- Unmark activities.
- Track completed activities.
- View daily activity progress.
- View previous activity history.

Update activity completion percentage immediately.

Personalize recommendations using available health profile information.

Do not suggest unsafe exercise targets. Account for individual limitations and recommend professional guidance where appropriate.

11. LOCAL AI ASSISTANT – OLLAMA LLAMA 3.2

Integrate the existing HealthSync AI Assistant with my locally installed Ollama model.

Required model: llama3.2:3b

Requirements:

1. Use Ollama locally.
2. Connect Ollama through the existing Flask backend.
3. Do not use external AI APIs.
4. Do not use paid API keys.
5. Reuse the existing AI Assistant UI.
6. Do not create another AI Assistant page.
7. Check whether Ollama is installed and running.
8. Check whether llama3.2:3b is already available.
9. Do not download or reinstall unnecessarily.
10. If the model is unavailable, provide clear instructions.

The Flask backend should communicate with the local Ollama service.

12. PERSONALIZED AI HEALTH CONTEXT

The AI Assistant must retrieve relevant information from SQLite for the currently logged-in user.

Include available information such as:

- Age
- Gender
- BMI
- Diabetes category
- Health conditions
- Food preferences
- Health profile
- Recent glucose records
- Blood pressure records
- Daily diet
- Selected alternative meals
- Completed meals
- Daily activities
- Activity progress

Use this information to generate personalized responses.

Important:

- Never invent missing health details.
- Never access another user's information.
- Never expose private database records.
- Retrieve only relevant information.
- Maintain strict user authentication and authorization.

13. AI ASSISTANT CHAT FUNCTIONALITY

Fix and implement complete chat functionality.

The following must work:

- Chat input
- Send button
- Enter key
- Quick Action buttons
- Loading indicator
- AI response display
- Error messages

Quick Actions:

Every existing Quick Action button must work.

When clicked:

1. Identify the selected question.
2. Display the question in the chat window.
3. Send it to the Flask backend.
4. Pass relevant user health context.
5. Generate a response using local Ollama.
6. Display the actual generated response.

Fix all existing JavaScript event listeners and functions.

Check:

- API routes
- Fetch URLs
- JSON request and response formats
- Backend errors
- Browser console errors
- Ollama connectivity

Show a loading indicator while generating a response.

Display friendly error messages if Flask or Ollama is unavailable.

Do not display fake success messages instead of actual AI responses.

14. AI ASSISTANT CHAT HISTORY

Implement persistent AI conversation history.

Requirements:

1. Save every user message.
2. Save every AI response.
3. Save timestamps.
4. Assign conversation IDs.
5. Link every conversation to its user ID.
6. Display previous conversations in a Chat History section.
7. Allow users to open previous conversations.
8. Allow users to continue existing conversations.
9. Allow users to start a new chat.
10. Allow users to delete conversations.
11. Preserve chat history after logout, browser refresh and reopening the website.
12. Show only the currently logged-in user's conversations.

When continuing a previous conversation, retrieve its relevant messages and maintain conversation context.

The AI should not mix different users' conversations.

15. AI RESPONSE BEHAVIOUR AND SAFETY

The assistant must support:

- Diabetes-related questions
- Food and diet questions
- Exercise questions
- BMI explanations
- General health education
- HealthSync feature assistance
- Normal general questions

It should behave like a helpful general-purpose assistant while prioritizing the user's health context when relevant.

Health safety rules:

- Provide safe, evidence-informed information.
- Never diagnose diseases.
- Never prescribe medicines.
- Never recommend changing medication dosages.
- Never replace professional medical advice.
- Encourage consultation with qualified healthcare professionals when appropriate.
- Clearly communicate uncertainty.
- Do not make up glucose readings, diagnoses or medical history.

16. LANGUAGE SUPPORT

Support these languages:

1. English
2. Telugu
3. Hindi

Requirements:

- Add a language selector.
- Save each user's preferred language in SQLite.
- Display application content according to the selected language.
- Generate AI responses in the selected language.
- Maintain the selected language when the user logs in again.

Use natural and understandable language.

If the user selects Telugu, the AI should respond in Telugu rather than unnecessarily switching to English.

17. PROGRESS AND HISTORY PAGE

Create a personalized history section.

Display:

- Previous BMI records
- Diabetes status history
- Daily diet completion percentages
- Previous diet plans
- Completed activities
- Daily activity progress
- Available glucose records
- Blood pressure records

Allow users to view previous dates.

Do not overwrite or delete historical records when new daily records are created.

Display progress using clear cards, percentages and simple visual indicators.

18. PROFILE AND SETTINGS

Allow users to:

- View and edit personal details.
- Update health information.
- Update food preferences.
- Change preferred language.
- View account information.
- Save profile changes.

Ensure changes are stored in SQLite and reflected across the application.

19. FRONTEND AND BACKEND INTEGRATION

Integrate all existing frontend components with Flask.

Implement or update appropriate API routes for:

- Signup
- Login
- Logout
- User profile
- Health information
- Dashboard
- Diet plans
- Alternative meals
- Diet completion tracking
- Activities
- Activity completion
- Progress history
- AI chat
- AI conversation history
- Delete conversation
- Language preferences

Use proper HTTP methods and JSON responses.

Ensure JavaScript fetch requests correctly communicate with the backend.

Do not create duplicate frontend pages or unnecessary APIs.

20. SECURITY AND DATA PROTECTION

Implement:

- Secure password hashing
- Input validation
- SQL parameterized queries
- Protected Flask routes
- Secure session cookies
- User-specific database queries
- Proper error handling
- Safe handling of AI prompts and responses
- Protection against unauthorized access

Every database query involving personal information must enforce the logged-in user's ID.

Do not expose passwords, password hashes, secret keys or private health information.

21. PROJECT STRUCTURE AND ENVIRONMENT

First inspect the current project structure.

Reuse the existing structure wherever possible.

Use Python 3.13 on macOS.

Create a virtual environment named:

.venv

Activate it using:

source .venv/bin/activate

Create or update requirements.txt.

Install only necessary compatible dependencies.

Use macOS-compatible Terminal commands.

Do not use Windows commands or Windows file paths.

Avoid unnecessary frameworks, libraries and duplicate files.

22. TESTING AND DEBUGGING

After implementation, test the complete application.

Authentication

- Signup
- Login
- Logout
- Session persistence
- Protected pages

Database

- Automatic database creation
- Table relationships
- Saving and retrieving user data
- User data separation

Health Profile

- Saving health information
- BMI calculation
- Updating profile

Diet

- Breakfast checkbox
- Lunch checkbox
- Snacks checkbox
- Dinner checkbox
- Alternative meal selection
- Completion percentage
- Page refresh persistence
- Previous-day history

Activities

- Activity completion
- Unchecking activities
- Progress percentage
- Previous activity history

AI Assistant

- Ollama connection
- llama3.2:3b model availability
- Normal chat messages
- Enter key
- Send button
- Every Quick Action button
- Actual AI responses
- Loading indicator
- Error handling
- Personalized health context
- English, Telugu and Hindi responses

AI Chat History

- Saving conversations
- Retrieving conversations
- Opening previous conversations
- Continuing previous chats
- Starting new chats
- Deleting conversations
- User-specific chat history

Frontend

- All navigation
- All buttons
- Responsive design
- Browser console errors
- Backend integration

Fix all identified errors before completion.

Do not claim something works unless it has actually been tested.

23. FINAL DELIVERY

After completing the implementation, provide:

1. Summary of completed features.
2. Existing files modified.
3. New files created, if any.
4. Database tables created or updated.
5. API routes implemented.
6. Ollama integration details.
7. Testing results.
8. Any remaining limitations.

Provide exact macOS Terminal commands for:

- Opening the project folder.
- Activating the virtual environment.
- Installing dependencies.
- Checking Ollama status.
- Checking the llama3.2:3b model.
- Starting the Flask application.
- Opening HealthSync in the browser.

Also explain how to stop and restart the application.

FINAL INSTRUCTION:

Do not just provide instructions or sample code. Work directly with my existing project files, implement the required functionality, fix errors, integrate the frontend and backend, and test the complete HealthSync application.

Preserve all existing working features and UI/UX.

The final result must be a functional, professional, responsive HealthSync application running locally on my MacBook with Flask, SQLite and Ollama llama3.2:3b.
