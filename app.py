import streamlit as st
from groq import Groq
from dotenv import load_dotenv
import os
import PyPDF2

load_dotenv()

st.set_page_config(
    page_title="Global Scholarship Engine",
    page_icon="🎓",
    layout="centered"
)

# --- AIK KADAM BRAND STYLING ---
st.markdown("""
<style>
    /* Hide default Streamlit clutter */
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    header {visibility: hidden;}

    /* Aik Kadam Dark Theme Background */
    .stApp {
        background-color: #050505;
        background-image: radial-gradient(circle at 15% 40%, rgba(245, 166, 35, 0.15) 0%, #050505 70%);
        color: #f3f4f6;
    }

    .block-container {
        padding-top: 2rem;
        padding-bottom: 3rem;
        max-width: 850px;
    }

    /* ---------------------------------
       BRANDED GLOWING TABS
       --------------------------------- */
    div[data-baseweb="tab_list"] {
        background-color: rgba(20, 20, 20, 0.8);
        border-radius: 50px;
        padding: 6px;
        border: 1px solid rgba(245, 166, 35, 0.2);
        display: flex;
        justify-content: center;
        margin-bottom: 2.5rem;
    }
    button[data-baseweb="tab"] {
        border-radius: 50px !important;
        padding: 12px 28px !important;
        margin: 0 4px !important;
        background-color: transparent !important;
        color: #a1a1aa !important;
        font-size: 1rem !important;
        font-weight: 600 !important;
        border: none !important;
        transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1) !important;
    }
    button[data-baseweb="tab"]:hover {
        color: #ffffff !important;
        background-color: rgba(255, 255, 255, 0.05) !important;
    }
    button[data-baseweb="tab"][aria-selected="true"] {
        background: #f5a623 !important;
        color: #000000 !important;
        box-shadow: 0 4px 15px rgba(245, 166, 35, 0.25) !important;
    }

    /* ---------------------------------
       HERO SECTION & TYPOGRAPHY
       --------------------------------- */
    .hero-container {
        text-align: center;
        margin-bottom: 2.5rem;
        animation: fadeIn 0.8s ease-out;
    }
    .hero-title {
        font-size: 4rem;
        font-weight: 900;
        letter-spacing: -0.02em;
        color: #ffffff;
        margin-bottom: 0.5rem;
        line-height: 1.1;
    }
    .hero-title span {
        color: #f5a623;
    }
    .hero-subtitle {
        font-size: 1.15rem;
        color: #a1a1aa;
        max-width: 650px;
        margin: 0 auto 1.5rem auto;
        line-height: 1.6;
    }
    .viral-hook {
        color: #f5a623;
        font-weight: 800;
        font-size: 1.25rem;
        display: block;
        margin-bottom: 0.8rem;
        letter-spacing: 0.05em;
        text-transform: uppercase;
    }

    /* ---------------------------------
       INPUT FIELDS & HIGH CONTRAST
       --------------------------------- */
    div[data-baseweb="input"] > div,
    div[data-baseweb="textarea"] > div {
        background-color: #0f0f0f !important; 
        border: 1px solid #333333 !important;
        border-radius: 12px;
        transition: all 0.3s ease;
    }
    div[data-baseweb="input"] > div:focus-within,
    div[data-baseweb="textarea"] > div:focus-within {
        border-color: #f5a623 !important;
        box-shadow: 0 0 0 2px rgba(245, 166, 35, 0.2) !important;
        background-color: #141414 !important;
    }
    input, textarea {
        color: #ffffff !important;
        font-size: 1.05rem !important;
        padding: 1.2rem !important;
    }
    input::placeholder, textarea::placeholder {
        color: #71717a !important;
        opacity: 1 !important;
    }

    /* --- FILE UPLOADER CSS FIX (Aik Kadam Theme) --- */
    [data-testid="stFileUploader"] > section {
        background-color: #0f0f0f !important;
        border: 2px dashed #333333 !important;
        border-radius: 12px !important;
    }
    [data-testid="stFileUploader"] div, 
    [data-testid="stFileUploader"] span, 
    [data-testid="stFileUploader"] small {
        color: #d4d4d8 !important;
    }
    [data-testid="stFileUploader"] button {
        background: linear-gradient(135deg, #333333 0%, #141414 100%) !important;
        color: #ffffff !important;
        border: 1px solid #333333 !important;
        border-radius: 50px !important;
        font-weight: 600 !important;
        padding: 0.5rem 1.5rem !important;
    }
    [data-testid="stFileUploader"] button:hover {
        border-color: #f5a623 !important;
        color: #f5a623 !important;
    }

    /* ---------------------------------
       BUTTONS
       --------------------------------- */
    button[kind="primary"] {
        background: #f5a623 !important;
        color: #000000 !important;
        border: none !important;
        border-radius: 50px !important;
        padding: 1.5rem !important;
        font-size: 1.15rem !important;
        font-weight: 800 !important;
        letter-spacing: 0.02em !important;
        transition: all 0.3s ease !important;
        margin-top: 1rem !important;
    }
    button[kind="primary"]:hover {
        transform: translateY(-2px) !important;
        box-shadow: 0 8px 25px rgba(245, 166, 35, 0.3) !important;
        background: #fbbf24 !important;
    }

    /* Output Markdown Styling */
    .stMarkdown h2 {
        color: #f5a623 !important;
        font-size: 1.3rem !important;
        font-weight: 700 !important;
        margin-top: 2rem !important;
        border-bottom: 1px solid rgba(245, 166, 35, 0.2) !important;
        padding-bottom: 0.5rem !important;
    }
    .stMarkdown h3 {
        color: #ffffff !important;
        font-size: 1.15rem !important;
    }
    
    .input-label {
        font-size: 0.85rem;
        font-weight: 700;
        color: #d4d4d8;
        margin-bottom: 0.5rem;
        display: block;
        letter-spacing: 0.1em;
        text-transform: uppercase;
    }

    @keyframes fadeIn {
        from { opacity: 0; transform: translateY(15px); }
        to { opacity: 1; transform: translateY(0); }
    }
</style>
""", unsafe_allow_html=True)

# --- APP LAYOUT (3 TABS REORDERED) ---
tab1, tab2, tab3 = st.tabs(["🏛️ Program Finder", "🌍 Scholarship Matcher", "🔍 Scholarship Deep Dive"])

# ==========================================
# TAB 1: PROGRAM FINDER (Resume + Credentials)
# ==========================================
with tab1:
    st.markdown("""
    <div class="hero-container">
        <div class="hero-title">Academic <span>Program Finder</span></div>
        <div class="hero-subtitle">
            <span class="viral-hook">Map out your academic future.</span>
            Upload your resume and tell the AI your goals and budget. We will evaluate your GPA and experience, recommend the correct degree level, and find programs and scholarships that fit your profile.
        </div>
    </div>
    """, unsafe_allow_html=True)

    st.markdown('<span class="input-label">📄 UPLOAD YOUR RESUME/CV (PDF)</span>', unsafe_allow_html=True)
    uploaded_resume = st.file_uploader("resume_uploader", type=["pdf"], label_visibility="collapsed")

    st.markdown('<span class="input-label" style="margin-top: 1.5rem;">🎯 WHAT ARE YOUR GOALS & BUDGET?</span>', unsafe_allow_html=True)
    career_goals = st.text_area(
        label="career_goals",
        height=150,
        placeholder="e.g., 'I want to study AI in Europe or North America. My max budget is $15k/year but I need scholarships. (Note: Mention your GPA here if it is not on your resume)'",
        label_visibility="collapsed"
    )

    program_btn = st.button("Evaluate Profile & Find Programs 🏛️", type="primary", use_container_width=True, key="btn_programs")

    if program_btn:
        if not uploaded_resume or not career_goals.strip():
            st.error("⚠️ Please provide both your PDF resume and a brief description of your goals and budget.")
        else:
            pdf_reader = PyPDF2.PdfReader(uploaded_resume)
            resume_text = ""
            for page in pdf_reader.pages:
                resume_text += page.extract_text()

            api_key = os.getenv("GROQ_API_KEY")
            if not api_key:
                st.error("⚠️ System Error: GROQ_API_KEY is not set.")
                st.stop()
                
            client = Groq(api_key=api_key)
            prompt = f"""You are an elite Higher Education, Admissions, and Financial Aid Counselor. 
I am providing you with a student's RESUME and their PERSONAL CONTEXT (Goals, Budget, Preferences). 

Your task is to:
1. Analyze their GPA, academic history, and professional experience from the resume/context.
2. Determine the most appropriate degree level (e.g., Undergraduate, Masters, PhD, Post-Doc, or specialized diploma) based strictly on their credentials.
3. Recommend the top 3-4 specific academic programs globally that fit their profile, goals, AND stated financial budget/constraints.

Format your response EXACTLY like this:

## 📊 Profile Evaluation
* **Current Standing:** [Brief assessment of their academic history, GPA, and professional readiness]
* **Recommended Degree Level:** [e.g., Masters, PhD, etc.] and WHY this is the most logical next step.

## 🎓 Top Program Recommendations

### 1. [Name of Academic Program] at [University Name]
* **Why it fits:** [Explain alignment with their resume, credentials, and career goals]
* **Estimated Average Cost:** [Provide a realistic tuition/fee range in USD, keeping their budget in mind]
* **Relevant Scholarships:** [Name 1-2 specific scholarships applicable to this program or university to offset costs]

[Repeat for the other programs]

## 🚀 Next Strategic Step
Provide 1 crucial, actionable piece of advice for their application strategy based on the weaknesses or strengths in their resume.

---
PERSONAL CONTEXT & BUDGET:
{career_goals}

RESUME TEXT:
{resume_text}
"""
            with st.spinner("Evaluating credentials and scanning global universities... 🏛️"):
                try:
                    response = client.chat.completions.create(
                        model="llama-3.3-70b-versatile",
                        messages=[{"role": "user", "content": prompt}],
                        max_tokens=1500
                    )
                    st.success("Evaluation Complete!")
                    st.markdown(response.choices[0].message.content)
                except Exception as e:
                    st.error(f"Error reading or analyzing: {str(e)}")


# ==========================================
# TAB 2: SCHOLARSHIP MATCHER (Search by Profile)
# ==========================================
with tab2:
    st.markdown("""
    <div class="hero-container">
        <div class="hero-title">Scholarship <span>Matcher</span></div>
        <div class="hero-subtitle">
            <span class="viral-hook">Fund your education without the debt.</span>
            Tell the AI about your background, nationality, target country, and desired degree. It will act as a search engine to find the hidden grants and scholarships you actually qualify for.
        </div>
    </div>
    """, unsafe_allow_html=True)

    st.markdown('<span class="input-label">🌍 Enter Your Profile & Goals</span>', unsafe_allow_html=True)
    student_profile = st.text_area(
        label="student_profile",
        height=200,
        placeholder="e.g., 'I am a student from Pakistan looking to do a Masters in Computer Science in Canada or the UK. I have a 3.8 GPA and 2 years of work experience.'",
        label_visibility="collapsed"
    )

    match_btn = st.button("Find My Scholarships 🎯", type="primary", use_container_width=True, key="btn_matcher")

    if match_btn:
        if not student_profile.strip():
            st.error("⚠️ Please enter your profile details first.")
        else:
            api_key = os.getenv("GROQ_API_KEY")
            if not api_key:
                st.error("⚠️ System Error: GROQ_API_KEY is not set.")
                st.stop()
                
            client = Groq(api_key=api_key)
            prompt = f"""You are an expert International Admissions and Financial Aid Advisor.
Based on the student profile below, generate a list of the top 4-5 specific scholarships, grants, or fellowships they are most likely eligible for. 

Do not suggest generic student loans. Only suggest actual funding opportunities.

Format your response EXACTLY like this:

## 🎯 Top Scholarship Matches

### 1. [Name of Scholarship]
* **Target Region/University:** [Where is this valid?]
* **Why it's a match:** [1 sentence on why this fits their specific profile]
* **Coverage:** [Briefly state what it pays for - e.g., Full Tuition + Living Stipend]

[Repeat for the other scholarships]

## ⚠️ Action Plan
Give the student 2 highly specific steps they should take this week to start preparing their profile for these applications.

STUDENT PROFILE:
{student_profile}
"""
            with st.spinner("Scanning global scholarship opportunities... 🌍"):
                try:
                    response = client.chat.completions.create(
                        model="llama-3.3-70b-versatile",
                        messages=[{"role": "user", "content": prompt}],
                        max_tokens=1500
                    )
                    st.success("Matches Found!")
                    st.markdown(response.choices[0].message.content)
                except Exception as e:
                    st.error(f"Error: {str(e)}")


# ==========================================
# TAB 3: DEEP DIVE (Search by Name)
# ==========================================
with tab3:
    st.markdown("""
    <div class="hero-container">
        <div class="hero-title">Scholarship <span>Deep Dive</span></div>
        <div class="hero-subtitle">
            <span class="viral-hook">Decode the exact requirements.</span>
            Have a specific scholarship in mind? Enter the name below and the AI will break down the eligibility, what it covers, and the insider tips you need to win it.
        </div>
    </div>
    """, unsafe_allow_html=True)

    st.markdown('<span class="input-label">🎓 Enter Scholarship Name</span>', unsafe_allow_html=True)
    scholarship_name = st.text_input(
        label="scholarship_name",
        placeholder="e.g., 'Chevening Scholarship', 'Erasmus Mundus', 'Rhodes Scholarship'...",
        label_visibility="collapsed"
    )

    search_btn = st.button("Decode this Scholarship 🚀", type="primary", use_container_width=True, key="btn_deep_dive")

    if search_btn:
        if not scholarship_name.strip():
            st.error("⚠️ Please enter a scholarship name first.")
        else:
            api_key = os.getenv("GROQ_API_KEY")
            if not api_key:
                st.error("⚠️ System Error: GROQ_API_KEY is not set.")
                st.stop()
                
            client = Groq(api_key=api_key)
            prompt = f"""You are an expert International Admissions and Financial Aid Advisor. 
Provide a detailed, highly structured breakdown of the following scholarship: {scholarship_name}.

If you do not have reliable information on this specific scholarship, please state honestly that you do not know.

Otherwise, format your response EXACTLY using these headings:

## 📋 Overview
What is this scholarship, who funds it, and what is its main goal?

## ✅ Eligibility Criteria
Use bullet points to list the exact requirements (nationality, GPA, work experience, degree level, etc.).

## 💰 What it Covers
Does it cover full tuition? Stipend? Flights? Be specific.

## 📅 General Application Timeline
When does it typically open and close? (Note: Remind the user to check the official website for exact current dates).

## 💡 Insider Tips to Win
What are the reviewers actually looking for in the essay/interview? Give 2-3 specific, actionable tips to make an application stand out.
"""
            with st.spinner("Accessing global funding database... 📚"):
                try:
                    response = client.chat.completions.create(
                        model="llama-3.3-70b-versatile",
                        messages=[{"role": "user", "content": prompt}],
                        max_tokens=1500
                    )
                    st.success("Analysis Complete!")
                    st.markdown(response.choices[0].message.content)
                except Exception as e:
                    st.error(f"Error: {str(e)}")