import streamlit as st
import pandas as pd
import random
from datetime import datetime, timezone

st.set_page_config(page_title="RIASEC Career Guidance", page_icon="🎯", layout="centered")

st.title("🎯 Career Guidance Survey for Higher Education Students")
st.markdown(
    "This survey explores students’ interests and preferences using the RIASEC framework "
    "to provide general career-interest guidance. Please answer honestly. There are no right "
    "or wrong answers. These suggestions support reflection and career exploration; they are not "
    "a definitive psychological assessment."
)

RIASEC = {
    "R — Realistic": [
        "I enjoy repairing machines or equipment.",
        "I like working with tools or mechanical devices.",
        "I enjoy building or assembling things.",
        "I prefer practical activities over theoretical discussions.",
        "I enjoy working outdoors.",
        "I like operating machinery or equipment.",
        "I enjoy solving practical problems with my hands.",
    ],
    "I — Investigative": [
        "I enjoy solving complex scientific problems.",
        "I like conducting research.",
        "I enjoy analysing data.",
        "I like mathematics and logical reasoning.",
        "I enjoy carrying out experiments.",
        "I like reading scientific literature.",
        "I enjoy finding solutions through analysis.",
    ],
    "A — Artistic": [
        "I enjoy drawing or designing.",
        "I like expressing myself through art or music.",
        "I enjoy creative writing.",
        "I like developing original ideas.",
        "I enjoy artistic performances.",
        "I like imaginative activities.",
        "I prefer work that allows creativity.",
    ],
    "S — Social": [
        "I enjoy helping people solve problems.",
        "I like teaching others.",
        "I enjoy working in teams.",
        "I like volunteering to help others.",
        "I enjoy counselling or advising people.",
        "I am a good listener when people share concerns.",
        "I enjoy motivating others.",
    ],
    "E — Enterprising": [
        "I enjoy leading a group.",
        "I like persuading others about an idea.",
        "I enjoy starting projects.",
        "I am comfortable taking calculated risks.",
        "I enjoy negotiating with people.",
        "I like making business decisions.",
        "I enjoy influencing or motivating people to take action.",
    ],
    "C — Conventional": [
        "I enjoy organising files or records.",
        "I prefer following established procedures.",
        "I like working with numbers or data.",
        "I prefer structured and organised work.",
        "I enjoy planning and scheduling activities.",
        "I pay attention to small details.",
        "I like keeping accurate records.",
    ],
}

BACKGROUND_QUESTIONS = {
    "Stream": ["Engineering / Technology", "Arts / Humanities", "Science", "Commerce / Management", "Other"],
    "Family Business Background": ["Yes", "No"],
    "Have you attended entrepreneurship-related courses?": ["Yes", "No"],
    "Do you have startup or incubation-centre exposure?": ["Yes", "No"],
    "Have you participated in innovation competitions?": ["Yes", "No"],
    "Native Place": ["Rural", "Semi-urban", "Urban"],
    "Do you regularly read news/current affairs?": ["Yes", "No"],
}

CAREER_GUIDANCE = {
    "R — Realistic": ("You may enjoy practical, hands-on tasks and working with tools, equipment, or physical systems.",
                      "engineering, robotics, manufacturing, automotive technology, agriculture, hardware/networking, field operations, or technical maintenance"),
    "I — Investigative": ("You may enjoy analysis, research, logical reasoning, and understanding how things work.",
                          "data science, AI/ML, research, scientific analysis, software development, health sciences, cybersecurity, or engineering research"),
    "A — Artistic": ("You may enjoy creativity, self-expression, design, and developing original ideas.",
                     "graphic/UI/UX design, media, animation, content creation, architecture, creative technology, writing, or product design"),
    "S — Social": ("You may enjoy supporting, teaching, guiding, and collaborating with people.",
                   "teaching, counselling, healthcare, human resources, social work, training, student support, or community development"),
    "E — Enterprising": ("You may enjoy leadership, persuasion, initiative, decision-making, and organising projects.",
                         "entrepreneurship, business management, marketing, sales, product management, event management, consulting, or project leadership"),
    "C — Conventional": ("You may enjoy structured tasks, accuracy, organisation, records, and working with data or procedures.",
                         "accounting, finance, administration, operations, quality assurance, data management, compliance, logistics, or business analytics"),
}

def get_supabase_client():
    try:
        url = st.secrets["SUPABASE_URL"]
        key = st.secrets["SUPABASE_KEY"]
    except Exception:
        return None
    try:
        from supabase import create_client
        return create_client(url, key)
    except Exception as exc:
        st.error(f"Could not initialize database connection: {exc}")
        return None

# Use Streamlit multipage-style step navigation with session state.
if "survey_step" not in st.session_state:
    st.session_state.survey_step = 0
if "personal_data" not in st.session_state:
    st.session_state.personal_data = {}
if "background_data" not in st.session_state:
    st.session_state.background_data = {}
if "riasec_data" not in st.session_state:
    st.session_state.riasec_data = {}
if "shuffled_questions" not in st.session_state:
    # Shuffle once per respondent/session; keep this order while they move between pages.
    all_questions = [
        (category, qnum, question)
        for category, statements in RIASEC.items()
        for qnum, question in enumerate(statements, start=1)
    ]
    random.SystemRandom().shuffle(all_questions)
    st.session_state.shuffled_questions = all_questions

step = st.session_state.survey_step

if step == 0:
    with st.form("personal_form"):
        st.header("Section 1: Personal Information")
        st.caption("Page 1 of 3 — Please enter the details requested by your institution.")
        col1, col2 = st.columns(2)
        with col1:
            name = st.text_input("Name *", value=st.session_state.personal_data.get("name", ""))
            reg_no = st.text_input("Registration Number *", value=st.session_state.personal_data.get("reg_no", ""))
            gender = st.selectbox("Gender", ["Prefer not to say", "Female", "Male", "Other"], index=["Prefer not to say", "Female", "Male", "Other"].index(st.session_state.personal_data.get("gender", "Prefer not to say")))
            email = st.text_input("Email ID", value=st.session_state.personal_data.get("email", ""))
        with col2:
            mobile = st.text_input("Mobile Number", value=st.session_state.personal_data.get("mobile", ""))
            college = st.text_input("School / College *", value=st.session_state.personal_data.get("college", ""))
            department = st.text_input("Department *", value=st.session_state.personal_data.get("department", ""))
            section = st.text_input("Section", value=st.session_state.personal_data.get("section", ""))
        years = ["Select", "1st Year", "2nd Year", "3rd Year", "4th Year", "5th Year", "Other"]
        year = st.selectbox("Year of Study *", years, index=years.index(st.session_state.personal_data.get("year", "Select")))
        next_personal = st.form_submit_button("Next →", type="primary")
    if next_personal:
        missing = []
        if not name.strip(): missing.append("Name")
        if not reg_no.strip(): missing.append("Registration Number")
        if not college.strip(): missing.append("School / College")
        if not department.strip(): missing.append("Department")
        if year == "Select": missing.append("Year of Study")
        if missing:
            st.error("Please complete the required fields: " + ", ".join(missing) + ".")
        else:
            st.session_state.personal_data = {
                "name": name, "reg_no": reg_no, "gender": gender, "email": email,
                "mobile": mobile, "college": college, "department": department,
                "section": section, "year": year
            }
            st.session_state.survey_step = 1
            st.rerun()

elif step == 1:
    with st.form("background_form"):
        st.header("Section 2: Student Background")
        st.caption("Page 2 of 3 — Select the option that best describes you.")
        background_answers = {}
        for q, options in BACKGROUND_QUESTIONS.items():
            prior = st.session_state.background_data.get(q, options[0])
            background_answers[q] = st.radio(q, options, horizontal=True, key=f"bg_{q}", index=options.index(prior))
        role_model_question = "Who inspires you in your career or entrepreneurial journey, and how have they influenced your goals or decisions?"
        background_answers[role_model_question] = st.text_area(
            role_model_question + " (Optional)",
            value=st.session_state.background_data.get(role_model_question, ""),
            placeholder="You may mention a family member, teacher, entrepreneur, or another person—and how they inspire you.",
            key="bg_role_model_open_ended"
        )
        prev_col, next_col = st.columns(2)
        with prev_col:
            previous_background = st.form_submit_button("← Previous")
        with next_col:
            next_background = st.form_submit_button("Next →", type="primary")
    if previous_background:
        st.session_state.background_data = background_answers
        st.session_state.survey_step = 0
        st.rerun()
    if next_background:
        st.session_state.background_data = background_answers
        st.session_state.survey_step = 2
        st.rerun()

elif step == 2:
    # Seven questionnaire pages, six questions per page. Keep the same section title on every page.
    if "question_page" not in st.session_state:
        st.session_state.question_page = 0
    question_page = st.session_state.question_page
    # Show six randomly ordered questions per page. The order is shuffled once per respondent.
    start_index = question_page * 6
    questions_this_page = st.session_state.shuffled_questions[start_index:start_index + 6]

    with st.form(f"riasec_form_page_{question_page}"):
        st.header("Section 3: RIASEC Interest Questionnaire")
        st.caption(f"Page {question_page + 1} of 7 — Answer all six questions on this page. The question order is randomly shuffled for each respondent.")
        st.write("Answer **Yes** if the statement generally describes your interests, or **No** if it does not. Yes = 1 mark; No = 0 marks.")
        page_answers = {}
        for category, qnum, question in questions_this_page:
            key = f"{category}_{qnum}"
            previous_answer = st.session_state.riasec_data.get(key)
            options = ["Yes", "No"]
            page_answers[key] = st.radio(
                question, options, horizontal=True, key=f"answer_{key}",
                index=options.index(previous_answer) if previous_answer in options else None
            )
        prev_col, next_col = st.columns(2)
        with prev_col:
            previous_questions = st.form_submit_button("← Previous")
        with next_col:
            if question_page < 6:
                next_questions = st.form_submit_button("Next →", type="primary")
                submit_all = False
            else:
                next_questions = False
                submit_all = st.form_submit_button("Submit and View Career Guidance", type="primary")

    if previous_questions:
        st.session_state.riasec_data.update(page_answers)
        if question_page == 0:
            st.session_state.survey_step = 1
        else:
            st.session_state.question_page = question_page - 1
        st.rerun()

    if next_questions:
        missing_answers = [key for key, value in page_answers.items() if value is None]
        if missing_answers:
            st.error("Please answer all six questions on this page before continuing.")
        else:
            st.session_state.riasec_data.update(page_answers)
            st.session_state.question_page = question_page + 1
            st.rerun()

    if submit_all:
        missing_answers = [key for key, value in page_answers.items() if value is None]
        if missing_answers:
            st.error("Please answer all six questions on this page before submitting.")
        else:
            st.session_state.riasec_data.update(page_answers)
            st.session_state.survey_submitted = True
            st.rerun()

# Process the completed questionnaire from session state so answers persist across pages.
submitted = st.session_state.get("survey_submitted", False)
if submitted:
    personal = st.session_state.personal_data
    name = personal["name"]
    reg_no = personal["reg_no"]
    gender = personal["gender"]
    email = personal["email"]
    mobile = personal["mobile"]
    college = personal["college"]
    department = personal["department"]
    section = personal["section"]
    year = personal["year"]
    background_answers = st.session_state.background_data
    riasec_answers = st.session_state.riasec_data

if submitted:
    required_missing = []
    if not name.strip(): required_missing.append("Name")
    if not reg_no.strip(): required_missing.append("Registration Number")
    if not college.strip(): required_missing.append("School / College")
    if not department.strip(): required_missing.append("Department")
    if year == "Select": required_missing.append("Year of Study")
    unanswered = [key for key, value in riasec_answers.items() if value is None]

    if required_missing or unanswered:
        if required_missing:
            st.error("Please complete the required fields: " + ", ".join(required_missing) + ".")
        if unanswered:
            st.error(f"Please answer all 42 RIASEC questions. {len(unanswered)} question(s) remain unanswered.")
    else:
        scores = {
            category: sum(1 for qnum in range(1, 8) if riasec_answers[f"{category}_{qnum}"] == "Yes")
            for category in RIASEC
        }
        ranked = sorted(scores.items(), key=lambda x: (-x[1], list(RIASEC.keys()).index(x[0])))
        highest = ranked[0][1]
        top_categories = [category for category, score in ranked if score == highest]

        row = {
            "submitted_at": datetime.now(timezone.utc).isoformat(),
            "student_name": name.strip(),
            "registration_number": reg_no.strip(),
            "gender": gender,
            "email": email.strip(),
            "mobile": mobile.strip(),
            "college": college.strip(),
            "department": department.strip(),
            "section": section.strip(),
            "year_of_study": year,
            "background_responses": background_answers,
            "riasec_answers": riasec_answers,
            "riasec_scores": scores,
            "top_interest_categories": top_categories,
        }

        client = get_supabase_client()
        saved = False
        if client is not None:
            try:
                client.table("riasec_responses").insert(row).execute()
                saved = True
            except Exception:
                st.error("Your results were calculated, but the response could not be saved to the database. Please contact the app administrator and try again later.")
        else:
            st.warning("Database connection is not configured yet. Your results are shown below, but this submission has not been saved centrally.")

        if saved:
            st.success("Your response has been saved successfully.")

        st.header("Your RIASEC Scores")
        score_df = pd.DataFrame([{"Interest Category": cat, "Score (out of 7)": score} for cat, score in scores.items()])
        st.bar_chart(score_df.set_index("Interest Category"))
        st.dataframe(score_df, hide_index=True, use_container_width=True)

        st.header("Your Career-Interest Suggestions")
        st.write("Your strongest interest area(s): **" + ", ".join(top_categories) + "**")
        for category, score in ranked:
            if category in top_categories or score >= max(4, highest - 1):
                description, suggestions = CAREER_GUIDANCE[category]
                st.subheader(f"{category} — {score}/7")
                st.write(description)
                st.write("**Areas to explore:** " + suggestions)
        st.info("These suggestions are a starting point for exploration, not a final career decision. Consider your skills, values, academic performance, opportunities, and advice from a career counsellor.")

        csv_data = pd.DataFrame([{
            "Submitted At": row["submitted_at"],
            "Student Name": name,
            "Registration Number": reg_no,
            "Gender": gender,
            "Email": email,
            "Mobile": mobile,
            "College": college,
            "Department": department,
            "Section": section,
            "Year of Study": year,
            **{f"Background: {k}": v for k, v in background_answers.items()},
            **{f"Answer: {k}": v for k, v in riasec_answers.items()},
            **{f"Score: {k}": v for k, v in scores.items()},
            "Top Interest Categories": ", ".join(top_categories),
        }]).to_csv(index=False).encode("utf-8-sig")
        st.download_button("Download My Result (CSV)", data=csv_data, file_name="riasec_career_result.csv", mime="text/csv")

st.caption("Privacy note: Student responses may contain personal information. Collect only what is necessary, explain how responses will be used, and restrict database access to authorised staff.")
