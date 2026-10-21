import streamlit as st
import pandas as pd
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
    "Have you had startup or incubation-centre exposure?": ["Yes", "No"],
    "Have you participated in innovation competitions?": ["Yes", "No"],
    "Native Place": ["Rural", "Semi-urban", "Urban"],
    "Do you regularly read news/current affairs?": ["Yes", "No"],
    "Do you have a role model who inspires your career goals?": ["Yes", "No"],
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

with st.form("career_survey"):
    st.header("Section 1: Personal Information")
    st.caption("Please enter the details requested by your institution.")
    col1, col2 = st.columns(2)
    with col1:
        name = st.text_input("Name *")
        reg_no = st.text_input("Registration Number *")
        gender = st.selectbox("Gender", ["Prefer not to say", "Female", "Male", "Other"])
        email = st.text_input("Email ID")
    with col2:
        mobile = st.text_input("Mobile Number")
        college = st.text_input("School / College *")
        department = st.text_input("Department *")
        section = st.text_input("Section")
    year = st.selectbox("Year of Study *", ["Select", "1st Year", "2nd Year", "3rd Year", "4th Year", "5th Year", "Other"])

    st.divider()
    st.header("Section 2: Student Background")
    st.caption("Select the option that best describes you.")
    background_answers = {}
    for q, options in BACKGROUND_QUESTIONS.items():
        background_answers[q] = st.radio(q, options, horizontal=True, key=f"bg_{q}")

    st.divider()
    st.header("Section 3: RIASEC Interest Questionnaire")
    st.write("Answer **Yes** if the statement generally describes your interests, or **No** if it does not. Yes = 1 mark; No = 0 marks.")
    st.info("The 42 questions are arranged in seven groups of six. Each group contains one question from each RIASEC category.")
    riasec_answers = {}
    for group_num in range(7):
        st.subheader(f"Question group {group_num + 1} of 7")
        for category, questions in RIASEC.items():
            question = questions[group_num]
            key = f"{category}_{group_num + 1}"
            riasec_answers[key] = st.radio(question, ["Yes", "No"], horizontal=True, key=key, index=None)
        if group_num < 6:
            st.divider()

    submitted = st.form_submit_button("Submit and View Career Guidance", type="primary")

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
