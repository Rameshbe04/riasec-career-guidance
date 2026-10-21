import streamlit as st
from datetime import date

st.set_page_config(page_title='College Career Interest Survey', page_icon='🎓', layout='centered')

DIMENSIONS = {
    'R': ('Realistic', 'Practical, hands-on, technical, or applied work.'),
    'I': ('Investigative', 'Research, analysis, science, logical reasoning, and problem-solving.'),
    'A': ('Artistic', 'Creativity, design, original ideas, and expressive work.'),
    'S': ('Social', 'Teaching, helping, counselling, collaboration, and supporting people.'),
    'E': ('Enterprising', 'Leadership, persuasion, initiative, business, and decision-making.'),
    'C': ('Conventional', 'Organisation, accuracy, records, structured processes, and working with data.'),
}
QUESTIONS = [
('I enjoy repairing machines or equipment.','R'),('I like working with tools and mechanical devices.','R'),('I enjoy building or assembling objects.','R'),('I prefer practical tasks over theoretical discussions.','R'),('I enjoy working outdoors.','R'),('I like operating machinery or equipment.','R'),('I enjoy solving practical problems with my hands.','R'),
('I enjoy solving complex scientific problems.','I'),('I like conducting research.','I'),('I enjoy analysing data.','I'),('I enjoy mathematics and logical reasoning.','I'),('I like experimenting to discover new knowledge.','I'),('I enjoy reading scientific literature.','I'),('I enjoy finding solutions through analysis.','I'),
('I enjoy drawing or designing creative works.','A'),('I like expressing myself through art or music.','A'),('I enjoy writing creative stories or poems.','A'),('I enjoy creating original ideas.','A'),('I appreciate artistic performances.','A'),('I enjoy imaginative activities.','A'),('I prefer work that allows creativity.','A'),
('I enjoy helping people solve their problems.','S'),('I enjoy teaching others.','S'),('I like working in teams.','S'),('I enjoy volunteering for community service.','S'),('I enjoy counselling people.','S'),('I enjoy listening to others.','S'),('I enjoy motivating people.','S'),
('I enjoy leading a group.','E'),('I like persuading others.','E'),('I enjoy starting new projects.','E'),('I like taking calculated risks.','E'),('I enjoy negotiating with people.','E'),('I enjoy making business decisions.','E'),('I like influencing others to achieve goals.','E'),
('I enjoy organising files and records.','C'),('I like following established procedures.','C'),('I enjoy working with numbers and data.','C'),('I prefer structured work environments.','C'),('I enjoy planning and scheduling activities.','C'),('I pay attention to details.','C'),('I enjoy maintaining accurate records.','C')]
CAREERS = {
'R':['Engineering and applied technology','Robotics, electronics, or hardware support','Manufacturing, operations, or technical services','Field engineering or practical technical roles'],
'I':['Data Analyst or Business Intelligence Analyst','Research Assistant or Research Analyst','AI / Machine Learning pathway','Scientific, laboratory, or analytical roles'],
'A':['UI/UX or visual design','Content creation, communication, or media','Product design or creative technology','Writing, animation, or digital arts'],
'S':['Teaching, training, or academic support','Human resources or learning and development','Counselling-related study or student support','Healthcare, community, or public-service pathways'],
'E':['Entrepreneurship or startup development','Marketing, sales, or business development','Project coordination or product management','Leadership, consulting, or management pathways'],
'C':['Business, operations, or project administration','Accounting, finance, or audit-related pathways','Data quality, reporting, or documentation','Process coordination or information management']}
SKILLS = {
'R':['Build practical projects','Learn tools relevant to your branch','Develop troubleshooting and safety practices'],
'I':['Practise Python or another relevant programming language','Strengthen statistics and analytical reasoning','Complete a small research or data project'],
'A':['Build a portfolio of creative work','Practise design and communication tools','Complete a project that demonstrates original thinking'],
'S':['Develop communication and teamwork skills','Join peer mentoring or volunteering activities','Practise presentation and listening skills'],
'E':['Lead a student activity or project','Practise pitching ideas and negotiation','Learn project planning and basic business concepts'],
'C':['Practise spreadsheets and data organisation','Develop documentation and quality-checking habits','Learn planning, reporting, and workflow tools']}
LIKERT = {'Strongly disagree':1,'Disagree':2,'Neither agree nor disagree':3,'Agree':4,'Strongly agree':5}

st.title('🎓 College Career Interest Survey')
st.write('Explore your interests and receive career ideas and suggested next steps using the six RIASEC dimensions.')
st.info('This is an interest-exploration tool, not a psychological diagnosis or a guarantee of career success. Use the result as a starting point for further research and guidance.')
with st.form('student_profile'):
    st.subheader('About you')
    name = st.text_input('Name (optional)')
    programme = st.text_input('Degree / programme (e.g., B.Tech CSE)')
    year = st.selectbox('Year of study',['Select','1st year','2nd year','3rd year','4th year','Other'])
    interests = st.text_input('Subjects or activities you enjoy (optional)')
    st.subheader('Rate each statement')
    st.caption('Choose the response that best reflects your interest. There are no right or wrong answers.')
    answers=[]
    for idx,(question,code) in enumerate(QUESTIONS,1):
        response=st.radio(f'{idx}. {question}',list(LIKERT.keys()),index=2,horizontal=True,key=f'q_{idx}')
        answers.append((code,LIKERT[response]))
    submitted=st.form_submit_button('Calculate my career-interest profile',type='primary')

if submitted:
    scores={c:0 for c in DIMENSIONS}
    for code,value in answers: scores[code]+=value
    ordered=sorted(scores,key=lambda c:(-scores[c],c))
    top3=ordered[:3]
    interest_code=''.join(top3)
    st.success('Your career-interest profile is ready!')
    if name.strip(): st.subheader(f'{name.strip()}’s results')
    st.write(f"**Programme:** {programme or 'Not provided'}  |  **Year:** {year if year!='Select' else 'Not provided'}")
    st.metric('Your three-letter interest code',interest_code)
    st.caption('Each dimension has 7 statements. Scores range from 7 to 35. Higher scores indicate stronger self-reported interest in that area.')
    st.subheader('Your six interest scores')
    for code in DIMENSIONS:
        st.write(f"**{code} — {DIMENSIONS[code][0]}: {scores[code]}/35**")
        st.progress(scores[code]/35)
    st.subheader('Your leading interests')
    for code in top3:
        label,description=DIMENSIONS[code]
        st.markdown(f'### {code} — {label}')
        st.write(description)
        st.write('**Career areas to explore:**')
        for item in CAREERS[code]: st.write(f'- {item}')
        st.write('**Suggested next steps:**')
        for item in SKILLS[code]: st.write(f'- {item}')
    st.subheader('A practical next-step plan')
    for item in ['Choose two career areas above and read about their day-to-day work.','Speak with a faculty mentor, career counsellor, or professional in the field.','Complete one small project, course, internship, or club activity related to your preferred area.','Revisit your options after gaining experience; interests can change over time.']:
        st.write('• '+item)
    if interests.strip(): st.write('**Your stated interests:** '+interests.strip())
    report=[ 'COLLEGE CAREER INTEREST PROFILE',f'Date: {date.today().isoformat()}',f'Name: {name.strip() or "Not provided"}',f'Programme: {programme or "Not provided"}',f'Year: {year if year!="Select" else "Not provided"}',f'Interest code: {interest_code}','','RIASEC SCORES (each dimension out of 35)']
    for code in DIMENSIONS: report.append(f'{code} - {DIMENSIONS[code][0]}: {scores[code]}/35')
    report.extend(['','CAREER AREAS TO EXPLORE'])
    for code in top3:
        report.append(f'{code} - {DIMENSIONS[code][0]}')
        report.extend('- '+x for x in CAREERS[code])
        report.append('Suggested next steps:')
        report.extend('- '+x for x in SKILLS[code]); report.append('')
    report.append('Important: This report is an exploratory aid based on self-reported interests. It is not a validated prediction of ability or career success. Consider academic performance, skills, values, opportunities, and advice from a qualified career counsellor.')
    st.download_button('Download results as a text report',data='\n'.join(report).encode('utf-8'),file_name='career_interest_report.txt',mime='text/plain')
    st.caption('Privacy: This starter app does not save responses to a database. Avoid collecting unnecessary personal data.')
