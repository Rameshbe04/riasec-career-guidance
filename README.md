# RIASEC Career Guidance App — Supabase storage

## Features
- Section 1: Personal information
- Section 2: Eight background questions
- Section 3: 42 RIASEC Yes/No questions
- Seven groups of six questions, one from each category per group
- Yes = 1, No = 0; scores out of 7 for R, I, A, S, E, C
- Career-interest suggestions after submission
- Saves responses and scores to Supabase when configured
- CSV result download

## Setup
1. Create a project at https://supabase.com/.
2. In Supabase, open SQL Editor and run `supabase_schema.sql`.
3. Find the Project URL and a server-side secret key in Supabase project settings/API keys.
4. In Streamlit Community Cloud, open your app settings and add these secrets:
   SUPABASE_URL = "https://YOUR_PROJECT_ID.supabase.co"
   SUPABASE_KEY = "YOUR_PRIVATE_SERVER_SIDE_KEY"
5. Upload `app.py` and `requirements.txt` to your existing GitHub repository root.
6. Redeploy/reboot the Streamlit app.
7. Test with a sample response and verify it appears in `riasec_responses`.

Never put database passwords or API keys in GitHub or in chat. Do not expose a service-role/secret key in client-side code. Keep database access restricted to authorised staff.

## Privacy and research note
This stores personal information and survey responses. Explain data use to participants, restrict access, and follow institutional ethics/privacy requirements. The output is general career-interest guidance, not a definitive psychological assessment. Confirm the Yes/No scale is suitable before using it for formal research.
