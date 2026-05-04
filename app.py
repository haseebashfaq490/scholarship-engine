import streamlit as st
from groq import Groq
from dotenv import load_dotenv
import os

load_dotenv()

st.set_page_config(
    page_title="Global Scholarship Engine",
    page_icon="🎓",
    layout="centered"
)

# --- PREMIUM MODERN CSS STYLING ---
st.markdown("""
<style>
    /* Hide default Streamlit clutter */
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    header {visibility: hidden;}

    /* Professional Dark Theme Background */
    .stApp {
        background-color: #0f172a;
        background-image: radial-gradient(circle at 50% -20%, #1e293b 0%, #0f172a 80%);
        color: #f8fafc;
    }

    .block-container {
        padding-top: 2rem;
        padding-bottom: 3rem;
        max-width: 850px;
    }

    /* ---------------------------------
       MODERN GLOWING TABS
       --------------------------------- */
    div[data-baseweb="tab_list"] {
        background-color: rgba(30, 41, 59, 0.8);
        border-radius: 20px;
        padding: 5px;
        border: 1px solid rgba(56, 189, 248, 0.2);
        box-shadow: 0 4px 20px rgba(0, 0, 0, 0.2);
        display: flex;
        justify-content: center;
        margin-bottom: 2.5rem;
    }
    button[data-baseweb="tab"] {
        border-radius: 15px !important;
        padding: 12px 24px !important;
        margin: 0 4px !important;
        background-color: transparent !important;
        color: #94a3b8 !important;
        font-size: 1rem !important;
        font-weight: 600 !important;
        border: none !important;
        transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1) !important;
    }
    button[data-baseweb="tab"]:hover {
        color: #f1f5f9 !important;
        background-color: rgba(255, 255, 255, 0.05) !important;
    }
    button[data-baseweb="tab"][aria-selected="true"] {
        background: linear-gradient(135deg, #0ea5e9 0%, #6366f1 100%) !important;
        color: white !important;
        box-shadow: 0 4px 15px rgba(99, 102, 241, 0.4) !important;
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
        font-size: 3.8rem;
        font-weight: 900;
        letter-spacing: -0.02em;
        background: linear-gradient(to right, #ffffff, #e0f2fe, #bae6fd);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        margin-bottom: 0.5rem;
        line-height: 1.1;
    }
    .hero-subtitle {
        font-size: 1.15rem;
        color: #cbd5e1;
        max-width: 650px;
        margin: 0 auto 1.5rem auto;
        line-height: 1.6;
    }
    .viral-hook {
        color: #38bdf8;
        font-weight: 800;
        font-size: 1.35rem;
        display: block;
        margin-bottom: 0.5rem;
        letter-spacing: 0.01em;
    }

    /* ---------------------------------
       INPUT FIELDS & HIGH CONTRAST
       --------------------------------- */
    div[data-baseweb="input"] > div,
    div[data-baseweb="textarea"] > div {
        background-color: #1e293b !important; 
        border: 2px solid #334155 !important;
        border-radius: 16px;
        transition: all 0.3s ease;
    }
    div[data-baseweb="input"] > div:focus-within,
    div[data-baseweb="textarea"] > div:focus-within {
        border-color: #0ea5e9 !important;
        box-shadow: 0 0 0 4px rgba(14, 165, 233, 0.15) !important;
        background-color: #0f172a !important;
    }
    input, textarea {
        color: #ffffff !important;
        font-size: 1.05rem !important;
        padding: 1.2rem !important;
    }
    input::placeholder, textarea::placeholder {
        color: #94a3b8 !important;
        opacity: 1 !important;
    }

    /* ---------------------------------
       BUTTONS
       --------------------------------- */
    button[kind="primary"] {
        background: linear-gradient(135deg, #0ea5e9 0%, #6366f1 100%) !important;
        color: white !important;
        border: none !important;
        border-radius: 12px !important;
        padding: 1.5rem !important;
        font-size: 1.2rem !important;
        font-weight: 700 !important;
        letter-spacing: 0.02em !important;
        transition: all 0.3s ease !important;
        box-shadow: 0 4px 15px rgba(99, 102, 241, 0.3) !important;
        margin-top: 1rem !important;
    }
    button[kind="primary"]:hover {
        transform: translateY(-2px) !important;
        box-shadow: 0 8px 25px rgba(14, 165, 233, 0.4) !important;
        background: linear-gradient(135deg, #0284c7 0%, #4f46e5 100%) !important;
    }

    /* Output Markdown Styling */
    .stMarkdown h2 {
        color: #bae6fd !important;
        font-size: 1.3rem !important;
        font-weight: 700 !important;
        margin-top: 2rem !important;
        border-bottom: 1px solid rgba(56, 189, 248, 0.2) !important;
        padding-bottom: 0.5rem !important;
    }
    
    .input-label {
        font-size: 0.95rem;
        font-weight: 600;
        color: #e2e8f0;
        margin-bottom: 0.5rem;
        display: block;
        letter-spacing: 0.05em;
        text-transform: uppercase;
    }

    @keyframes fadeIn {
        from { opacity: 0; transform: translateY(15px); }
        to { opacity: 1; transform: translateY(0); }
    }
</style>
""", unsafe_allow_html=True)

# --- APP LAYOUT (TABS) ---
tab1, tab2 = st.tabs(["🔍 Scholarship Deep Dive", "🌍 Profile Matcher"])

# ==========================================
# TAB 1: DEEP DIVE (Search by Name)
# ==========================================
with tab1:
    st.markdown("""
    <div class="hero-container">
        <div class="hero-title">Scholarship Deep Dive</div>
        <div class="hero-subtitle">
            <span class="viral-hook">Decode the exact requirements. 🔎</span>
            Have a specific scholarship in mind? Enter the name below and the AI will break down the eligibility, what it covers, and the insider tips you need to win it.
        </div>
    </div>
    """, unsafe_allow_html=True)

    st.markdown('<span class="input-label">🎓 ENTER SCHOLARSHIP NAME</span>', unsafe_allow_html=True)
    scholarship_name = st.text_input(
        label="scholarship_name",
        placeholder="e.g., 'Chevening Scholarship', 'Erasmus Mundus', 'Rhodes Scholarship'...",
        label_visibility="collapsed"
    )

    search_btn = st.button("Decode this Scholarship 🚀", type="primary", use_container_width=True)

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

# ==========================================
# TAB 2: PROFILE MATCHER (Search by Profile)
# ==========================================
with tab2:
    st.markdown("""
    <div class="hero-container">
        <div class="hero-title">Smart Profile Matcher</div>
        <div class="hero-subtitle">
            <span class="viral-hook">Fund your education without the debt. 💸</span>
            Tell the AI about your background, nationality, target country, and desired degree. It will act as a search engine to find the hidden grants and scholarships you actually qualify for.
        </div>
    </div>
    """, unsafe_allow_html=True)

    st.markdown('<span class="input-label">🌍 ENTER YOUR PROFILE & GOALS</span>', unsafe_allow_html=True)
    student_profile = st.text_area(
        label="student_profile",
        height=200,
        placeholder="e.g., 'I am a student from Pakistan looking to do a Masters in Computer Science in Canada or the UK. I have a 3.8 GPA and 2 years of work experience.'",
        label_visibility="collapsed"
    )

    match_btn = st.button("Find My Scholarships 🎯", type="primary", use_container_width=True)

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