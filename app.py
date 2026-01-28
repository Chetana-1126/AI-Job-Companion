import streamlit as st
import google.generativeai as genai
import PyPDF2
import time

# ================= GEMINI API =================
GOOGLE_API_KEY = "AIzaSyB1R2K912xQjdiL2lNVMdIBfGEGa9TDUc4"  
genai.configure(api_key=GOOGLE_API_KEY)

def ask_gemini(prompt):
    model = genai.GenerativeModel("gemini-2.5-flash")
    response = model.generate_content(prompt)
    return response.text


JOB_SOURCES = {
    "Software Engineer": [
        ("Google Careers", "https://careers.google.com/jobs"),
        ("Microsoft Careers", "https://careers.microsoft.com"),
        ("Amazon Jobs", "https://www.amazon.jobs"),
        ("Indeed – Software Engineer", "https://in.indeed.com/q-software-engineer-jobs.html")
    ],
    "Data Scientist": [
        ("Amazon – Data Science Jobs", "https://www.amazon.jobs"),
        ("Indeed – Data Scientist", "https://in.indeed.com/q-data-scientist-jobs.html"),
        ("LinkedIn Jobs", "https://www.linkedin.com/jobs")
    ],
    "Machine Learning Engineer": [
        ("Google AI Careers", "https://careers.google.com/jobs"),
        ("Microsoft AI Jobs", "https://careers.microsoft.com"),
        ("Indeed – ML Engineer", "https://in.indeed.com/q-machine-learning-engineer-jobs.html")
    ],
    "Web Developer": [
        ("Wellfound (AngelList)", "https://wellfound.com/jobs"),
        ("Indeed – Web Developer", "https://in.indeed.com/q-web-developer-jobs.html")
    ],
    "Python Developer": [
        ("Indeed – Python Developer", "https://in.indeed.com/q-python-developer-jobs.html"),
        ("LinkedIn Jobs", "https://www.linkedin.com/jobs")
    ],
    "Data Analyst": [
        ("Indeed – Data Analyst", "https://in.indeed.com/q-data-analyst-jobs.html"),
        ("LinkedIn Jobs", "https://www.linkedin.com/jobs")
    ]
}

# ================= SESSION STATE INIT =================
for key in ["job_analysis", "improved_resume", "career_roadmap"]:
    if key not in st.session_state:
        st.session_state[key] = None

# ================= PAGE CONFIG =================
st.set_page_config(
    page_title="AI Job Companion",
    layout="wide"
)

# ================= HEADER =================
st.markdown("""
<h2>💼 AI Job Companion</h2>
<p style="color:gray;">
AI-powered job analysis, recommendations & official application links
</p>
<hr>
""", unsafe_allow_html=True)

# ================= TABS =================
tab1, tab2, tab3 = st.tabs(
    ["🎯 Job Matching", "✍ Resume Improvement", "📊 Career Roadmap"]
)

# ================= TAB 1: JOB MATCHING =================
with tab1:
    col1, col2 = st.columns([1.2, 1.8])

    with col1:
        st.markdown("### 👤 Candidate Profile")

        career_goal = st.text_area(
            "Career Goal",
            "Get a full-time software engineering job"
        )

        role = st.selectbox(
            "Target Job Role",
            list(JOB_SOURCES.keys())
        )

        skills = st.text_area(
            "Skills",
            "Python, Data Structures, SQL, Machine Learning"
        )

        experience = st.selectbox(
            "Experience Level",
            ["Fresher", "1–3 Years", "3–5 Years", "5+ Years"]
        )

        location = st.text_input(
            "Preferred Location",
            "India / Remote"
        )

        resume = st.file_uploader(
            "Upload Resume (PDF)",
            type=["pdf"]
        )

        analyze = st.button("🚀 Analyze Job Fit", use_container_width=True)

    with col2:
        st.markdown("### 🧠 AI Job Analysis")

        if analyze:
            resume_text = ""
            if resume:
                reader = PyPDF2.PdfReader(resume)
                for page in reader.pages:
                    resume_text += page.extract_text()

            prompt = f"""
You are an AI job advisor.

Candidate Details:
Career Goal: {career_goal}
Target Role: {role}
Skills: {skills}
Experience Level: {experience}
Preferred Location: {location}

Resume:
{resume_text}

Provide:
- Job fit score (0–100)
- Skill gaps
- ATS readiness
- Interview readiness
- Job-specific improvement tips
"""

            with st.spinner("Analyzing job fit using AI..."):
                time.sleep(0.5)
                st.session_state.job_analysis = ask_gemini(prompt)

        if st.session_state.job_analysis:
            st.subheader("📌 Job Fit Analysis")
            st.write(st.session_state.job_analysis)

            st.subheader("💼 Recommended Jobs & Official Links")
            for name, link in JOB_SOURCES.get(role, []):
                st.markdown(f"🔗 **[{name}]({link})**")

            explain_prompt = f"""
Explain why these jobs are suitable for a candidate with:
Role: {role}
Skills: {skills}
Experience: {experience}
"""
            st.markdown("### 🤖 Why These Jobs?")
            st.write(ask_gemini(explain_prompt))

# ================= TAB 2: RESUME IMPROVEMENT =================
with tab2:
    st.markdown("### ✍ AI Resume Improvement (Job-Focused)")

    if st.button("✨ Improve Resume for Jobs"):
        with st.spinner("Optimizing resume for job roles..."):
            prompt = """
Rewrite the resume for full-time job roles.
Make it ATS-optimized, achievement-focused, and impact-driven.
"""
            st.session_state.improved_resume = ask_gemini(prompt)

    if st.session_state.improved_resume:
        st.text_area(
            "Improved Resume",
            st.session_state.improved_resume,
            height=350
        )

# ================= TAB 3: CAREER ROADMAP =================
with tab3:
    st.markdown("### 📊 Job Readiness Roadmap")

    if st.button("🧭 Generate Career Roadmap"):
        with st.spinner("Generating roadmap..."):
            prompt = """
Create a 60-day job preparation roadmap.
Include skills, projects, interview prep, and job search strategy.
"""
            st.session_state.career_roadmap = ask_gemini(prompt)

    if st.session_state.career_roadmap:
        st.markdown("#### 📚 Personalized Job Roadmap")
        st.write(st.session_state.career_roadmap)
