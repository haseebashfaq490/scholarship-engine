import streamlit as st
from groq import Groq
from dotenv import load_dotenv
import os
import PyPDF2

load_dotenv()

# --- BRANDED PAGE CONFIG ---
st.set_page_config(
    page_title="Aik Kadam Decoder | Global Opportunity AI",
    page_icon="🌍",
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
       BRANDED GLOWING TABS (FIXED OVERFLOW)
       --------------------------------- */
    div[data-testid="stTabs"] > div > div > div {
        overflow: visible !important; 
    }
    div[data-baseweb="tab_list"] {
        background-color: rgba(20, 20, 20, 0.8);
        border-radius: 25px;
        padding: 8px;
        border: 1px solid rgba(245, 166, 35, 0.2);
        display: flex;
        flex-wrap: wrap;
        justify-content: center;
        gap: 8px;
        margin-bottom: 2.5rem;
    }
    button[data-baseweb="tab"] {
        border-radius: 50px !important;
        padding: 10px 18px !important;
        margin: 0 !important;
        background-color: transparent !important;
        color: #a1a1aa !important;
        font-size: 0.95rem !important;
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

    /* --- FILE UPLOADER CSS --- */
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

# --- APP LAYOUT (4 TABS) ---
tab1, tab2, tab3, tab4 = st.tabs(["🏛️ Program Finder", "🎓 Program Deep Dive", "🌍 Scholarship Matcher", "🔍 Scholarship Deep Dive"])

# ==========================================
# TAB 1: PROGRAM FINDER
# ==========================================
with tab1:
    st.markdown("""
    <div class="hero-container">
        <div class="hero-title">Aik Kadam <span>Decoder</span></div>
        <div class="hero-subtitle">
            <span class="viral-hook">Map out your academic future.</span>
            Upload your resume and tell the AI your goals and budget. We will evaluate your GPA and experience to recommend the perfect degree level and programs.
        </div>
    </div>
    """, unsafe_allow_html=True)

    st.markdown('<span class="input-label">📄 UPLOAD YOUR RESUME/CV (PDF)</span>', unsafe_allow_html=True)
    uploaded_resume = st.file_uploader("resume_uploader", type=["pdf"], label_visibility="collapsed")

    st.markdown('<span class="input-label" style="margin-top: 1.5rem;">🎯 WHAT ARE YOUR GOALS & BUDGET?</span>', unsafe_allow_html=True)
    career_goals = st.text_area(
        label="career_goals",
        height=150,
        placeholder="e.g., 'I want to study AI in Europe or North America. My max budget is $15k/year. (Mention your GPA here if it is not on your resume)'",
        label_visibility="collapsed"
    )

    program_btn = st.button("Evaluate Profile & Find Programs 🏛️", type="primary", use_container_width=True, key="btn_programs")

    if program_btn:
        if not uploaded_resume or not career_goals.strip():
            st.error("⚠️ Please provide both your PDF resume and a brief description of your goals.")
        else:
            pdf_reader = PyPDF2.PdfReader(uploaded_resume)
            resume_text = ""
            for page in pdf_reader.pages:
                resume_text += page.extract_text()

            api_key = os.getenv("GROQ_API_KEY")
            client = Groq(api_key=api_key)
            prompt = f"""You are an elite Higher Education and Admissions Counselor. 
Analyze the student's resume and goals to determine the best degree level and recommend 3-4 specific academic programs globally.

Format your response EXACTLY as:
## 📊 Profile Evaluation
* **Current Standing:** [Brief assessment of GPA and readiness]
* **Recommended Degree Level:** [e.g., Masters, PhD] and WHY.

## 🎓 Top Program Recommendations
[List programs with University, why it fits, cost range, and scholarships to target]

---
CONTEXT: {career_goals}
RESUME: {resume_text}
"""
            with st.spinner("Analyzing credentials... 🏛️"):
                try:
                    response = client.chat.completions.create(
                        model="llama-3.3-70b-versatile",
                        messages=[{"role": "user", "content": prompt}],
                        max_tokens=1500
                    )
                    st.success("Evaluation Complete!")
                    st.markdown(response.choices[0].message.content)
                except Exception as e:
                    st.error(f"Error: {str(e)}")

# ==========================================
# TAB 2: PROGRAM DEEP DIVE
# ==========================================
with tab2:
    st.markdown("""
    <div class="hero-container">
        <div class="hero-title">Program <span>Deep Dive</span></div>
        <div class="hero-subtitle">
            <span class="viral-hook">Decode the exact syllabus & requirements.</span>
            Enter a specific university program to see the core curriculum, admission requirements, costs, and career outcomes.
        </div>
    </div>
    """, unsafe_allow_html=True)

    st.markdown('<span class="input-label">🎓 ENTER UNIVERSITY & PROGRAM NAME</span>', unsafe_allow_html=True)
    target_program = st.text_input(label="target_program", placeholder="e.g., 'MSc in Data Science at ETH Zurich'...", label_visibility="collapsed")

    prog_deep_btn = st.button("Decode this Program 🚀", type="primary", use_container_width=True)

    if prog_deep_btn:
        if not target_program.strip():
            st.error("⚠️ Please enter a program name.")
        else:
            api_key = os.getenv("GROQ_API_KEY")
            client = Groq(api_key=api_key)
            prompt = f"Provide a detailed breakdown of the academic program: {target_program}. Include Admission Requirements, Curriculum, Estimated Costs, and Career Outcomes."
            with st.spinner("Retrieving data..."):
                try:
                    response = client.chat.completions.create(
                        model="llama-3.3-70b-versatile",
                        messages=[{"role": "user", "content": prompt}],
                        max_tokens=1500
                    )
                    st.success("Breakdown Complete!")
                    st.markdown(response.choices[0].message.content)
                except Exception as e:
                    st.error(f"Error: {str(e)}")

# ==========================================
# TAB 3: SCHOLARSHIP MATCHER
# ==========================================
with tab3:
    st.markdown("""
    <div class="hero-container">
        <div class="hero-title">Scholarship <span>Matcher</span></div>
        <div class="hero-subtitle">
            <span class="viral-hook">Fund your education without the debt.</span>
            Tell the AI about your background to find the hidden grants and scholarships you qualify for.
        </div>
    </div>
    """, unsafe_allow_html=True)

    st.markdown('<span class="input-label">🌍 ENTER YOUR PROFILE & GOALS</span>', unsafe_allow_html=True)
    student_profile = st.text_area(label="student_profile", height=200, placeholder="e.g., 'Student from Pakistan, 3.8 GPA, seeking Masters in UK'...", label_visibility="collapsed")

    match_btn = st.button("Find My Scholarships 🎯", type="primary", use_container_width=True)

    if match_btn:
        if not student_profile.strip():
            st.error("⚠️ Please enter profile details.")
        else:
            api_key = os.getenv("GROQ_API_KEY")
            client = Groq(api_key=api_key)
            prompt = f"Find 4-5 eligible scholarships for this profile: {student_profile}. Include coverage and why they match."
            with st.spinner("Scanning global database..."):
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
# TAB 4: SCHOLARSHIP DEEP DIVE
# ==========================================
with tab4:
    st.markdown("""
    <div class="hero-container">
        <div class="hero-title">Scholarship <span>Deep Dive</span></div>
        <div class="hero-subtitle">
            <span class="viral-hook">Decode the exact requirements.</span>
            Enter a scholarship name to see exactly what it covers and the insider tips to win it.
        </div>
    </div>
    """, unsafe_allow_html=True)

    st.markdown('<span class="input-label">🎓 ENTER SCHOLARSHIP NAME</span>', unsafe_allow_html=True)
    scholarship_name = st.text_input(label="scholarship_name_deep", placeholder="e.g., 'Chevening Scholarship'...", label_visibility="collapsed")

    schol_deep_btn = st.button("Decode this Scholarship 🚀", type="primary", use_container_width=True)

    if schol_deep_btn:
        if not scholarship_name.strip():
            st.error("⚠️ Please enter a name.")
        else:
            api_key = os.getenv("GROQ_API_KEY")
            client = Groq(api_key=api_key)
            prompt = f"Provide a breakdown for scholarship: {scholarship_name}. Include Eligibility, Coverage, Timeline, and Tips to Win."
            with st.spinner("Accessing database..."):
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