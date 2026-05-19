import streamlit as st
import pdfplumber
import re

# =========================
# PAGE CONFIG
# =========================

st.set_page_config(
    page_title="AI Resume Analyzer",
    page_icon="📄",
    layout="centered"
)

# =========================
# TITLE
# =========================

st.title("📄 AI Resume Analyzer & ATS Checker")

st.write(
    "Upload your resume and compare it with a job description using AI-style ATS analysis."
)

# =========================
# JOB DESCRIPTION INPUT
# =========================

job_description = st.text_area(
    "📌 Paste Job Description Here",
    height=200
)

# =========================
# FILE UPLOAD
# =========================

uploaded_file = st.file_uploader(
    "📤 Upload Resume PDF",
    type=["pdf"]
)

# =========================
# EXTRACT TEXT FROM PDF
# =========================

def extract_text(pdf_file):

    text = ""

    with pdfplumber.open(pdf_file) as pdf:

        for page in pdf.pages:

            page_text = page.extract_text()

            if page_text:
                text += page_text + " "

    return text


# =========================
# SKILL EXTRACTION
# =========================

def extract_skills(text):

    skills_db = [

        "python",
        "java",
        "c",
        "c++",
        "html",
        "css",
        "javascript",
        "sql",
        "mysql",
        "git",
        "machine learning",
        "artificial intelligence",
        "ai",
        "streamlit",
        "pandas",
        "numpy",
        "aws",
        "flask",
        "django",
        "react",
        "nodejs",
        "mongodb"
    ]

    text = text.lower()

    found_skills = []

    for skill in skills_db:

        pattern = r"\b" + re.escape(skill.lower()) + r"\b"

        if re.search(pattern, text):
            found_skills.append(skill)

    return list(set(found_skills))


# =========================
# MAIN LOGIC
# =========================

if uploaded_file is not None:

    # Extract resume text
    resume_text = extract_text(uploaded_file)

    # Show resume text
    st.subheader("📑 Resume Text")

    st.write(resume_text)

    # Extract skills
    resume_skills = extract_skills(resume_text)

    # Display detected skills
    st.subheader("🧠 Detected Skills")

    if resume_skills:
        st.success(", ".join(resume_skills))
    else:
        st.error("No skills detected")

    # =========================
    # ATS ANALYSIS
    # =========================

    if job_description:

        # Extract job skills
        job_skills = extract_skills(job_description)

        # Find matched skills
        matched_skills = list(
            set(resume_skills) & set(job_skills)
        )

        # Find missing skills
        missing_skills = list(
            set(job_skills) - set(resume_skills)
        )

        # Calculate ATS Score
        if len(job_skills) > 0:

            ats_score = int(
                (len(matched_skills) / len(job_skills)) * 100
            )

        else:
            ats_score = 0

        # =========================
        # DISPLAY ATS SCORE
        # =========================

        st.subheader("📊 ATS Match Score")

        st.progress(ats_score / 100)

        st.success(f"ATS Score: {ats_score}%")

        # =========================
        # MATCHED SKILLS
        # =========================

        st.subheader("✅ Matched Skills")

        if matched_skills:

            st.success(", ".join(matched_skills))

        else:

            st.warning("No matched skills found")

        # =========================
        # MISSING SKILLS
        # =========================

        st.subheader("❌ Missing Skills")

        if missing_skills:

            st.error(", ".join(missing_skills))

        else:

            st.success("No Missing Skills")

        # =========================
        # FINAL ANALYSIS
        # =========================

        st.subheader("📌 Final Analysis")

        if ats_score >= 80:

            st.success(
                "Excellent Resume! Very strong match for this job."
            )

        elif ats_score >= 50:

            st.warning(
                "Good Resume but needs some improvements."
            )

        else:

            st.error(
                "Low ATS Match. Add more relevant skills."
            )

    else:

        st.info(
            "Paste a Job Description to calculate ATS Score."
        )

# =========================
# FOOTER
# =========================

st.markdown("---")

st.write(
    "Built with ❤️ using Python & Streamlit"
)
