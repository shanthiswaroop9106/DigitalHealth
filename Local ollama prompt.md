#Connect the existing HealthSync website AI Assistant to my locally installed Ollama Llama model.

Requirements:

1. Use Ollama with the local model "llama3.2:3b".
2. Connect Ollama through the existing Python Flask backend.
3. Do not use external AI APIs or paid API keys.
4. Do not redesign or modify the existing HealthSync UI/UX.
5. Connect the existing AI Assistant chat interface to the backend.
6. Retrieve the currently logged-in user's health profile and relevant health records from SQLite.
7. Include available details such as age, BMI, diabetes category, health conditions, food preferences, daily diet and activities in the AI context.
8. Give personalized answers based on the logged-in user's available health information.
9. Support both health-related questions and general questions.
10. Support English, Telugu and Hindi based on the user's selected website language.
11. Maintain conversation context during the chat.
12. Protect user data. Never access or expose another user's health information.
13. If health details are missing, do not invent them.
14. Provide safe, evidence-informed health information. Never claim to diagnose diseases, prescribe medicines or replace a doctor.
15. Show a loading indicator while the assistant generates a response and display friendly error messages if Ollama is unavailable.
16. Check whether Ollama and the requested model are installed before running. Do not download or reinstall unnecessarily.
17. Inspect the existing project files first. Reuse the current frontend, Flask backend, database and authentication system. Do not delete existing features or create duplicate files unnecessarily.

Implement the complete integration and test the chat functionality. Finally, give me the exact terminal commands to run the project on my Mac.
