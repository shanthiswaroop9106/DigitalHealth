#prompt for activity tracking : Add activity tracking and daily progress functionality to my existing HealthSync website.

IMPORTANT: Do not redesign the existing UI/UX or disturb the current Diet Tracking and AI Assistant features.

ACTIVITY TRACKING:

1. Display a checkbox next to every recommended daily activity.
2. Allow users to mark an activity as completed or incomplete.
3. Save each activity's completion status in the existing SQLite database.
4. Save completion date and completion time.
5. Show a daily Activity Completion Percentage at the top of the Activities page.
6. Display a visual progress bar.
7. Calculate progress automatically:

Activity Progress = (Completed Activities / Total Recommended Activities) × 100

Examples:

- 0/4 = 0%
- 1/4 = 25%
- 2/4 = 50%
- 3/4 = 75%
- 4/4 = 100%

8. Update the percentage immediately whenever a checkbox is clicked.
9. Preserve completion status after refreshing or reopening the website.
10. Keep previous days' activity records without overwriting them.
11. Show date-wise activity completion history.
12. If activities change on a new day, calculate progress using that day's recommended activities only.
13. Allow users to mark activities as completed or undo completion.
14. Save all activity data separately for each logged-in user.

DASHBOARD INTEGRATION:

1. Show Diet Completion Percentage on the dashboard.
2. Show Activity Completion Percentage on the dashboard.
3. Display Overall Daily Progress using both diet and activity completion percentages.

Overall Progress = (Diet Completion Percentage + Activity Completion Percentage) / 2.

4. Update dashboard progress immediately when users mark meals or activities completed.

DATABASE AND TESTING:

- Reuse the existing Flask backend and SQLite database.
- Create or modify tables only when necessary.
- Ensure each user's records are private.
- Do not delete existing data.
- Test checkboxes, percentage calculations, date-wise history, page refresh and dashboard updates.

Inspect the existing project before making changes. Implement the complete functionality without breaking existing features. Do not create duplicate pages or redesign the website.
