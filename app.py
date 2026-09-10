import streamlit as st
import requests
import re
import json
import base64

# =========================================================
# PAGE CONFIG
# =========================================================

st.set_page_config(
    page_title="CareerCompanionAI",
    page_icon="✨",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# =========================================================
# HIDDEN IBM CONFIGURATION
# =========================================================

API_KEY = st.secrets.get("IBM_API_KEY", "")
PROJECT_ID = st.secrets.get("IBM_PROJECT_ID", "")

REGION_URL = st.secrets.get(
    "IBM_REGION_URL",
    "https://us-south.ml.cloud.ibm.com"
)

MODEL_ID = st.secrets.get(
    "IBM_MODEL_ID",
    "ibm/granite-4-h-small"
)

# =========================================================
# CUSTOM CSS
# =========================================================

st.markdown(
    """
<style>

/* =====================================================
   GLOBAL
===================================================== */

.stApp {
    background:
        radial-gradient(circle at 10% 10%, #e9e7ff 0%, transparent 28%),
        radial-gradient(circle at 90% 20%, #dff5ff 0%, transparent 28%),
        linear-gradient(135deg, #f8f9ff, #eef5ff);
    color: #172554;
}

#MainMenu {
    visibility: hidden;
}

footer {
    visibility: hidden;
}

header {
    visibility: hidden;
}

.block-container {
    max-width: 1180px;
    padding-top: 30px;
    padding-bottom: 50px;
}


/* =====================================================
   HERO
===================================================== */

.hero {
    position:relative;
    background: linear-gradient(
        120deg,
        #3730a3 0%,
        #4f46e5 35%,
        #7c3aed 70%,
        #9333ea 100%
    );

    padding: 55px 40px;
    border-radius: 32px;
    text-align: center;
    color: white;

    box-shadow:
        0 20px 50px rgba(67, 56, 202, 0.25);

    margin-bottom: 35px;
}

div.hero h1,
div.hero h1 * {
    color: white !important;
    -webkit-text-fill-color: white !important;
    font-size: clamp(22px,8vw,48px) !important;
    font-weight: 850 !important;
    margin: 0 !important;
    letter-spacing: -1px;
}

div.hero p,
div.hero p * {
    color: #eef2ff !important;
    -webkit-text-fill-color: #eef2ff !important;
    font-size: clamp(13px,4vw,19px) !important;
    margin-top: 12px !important;
}
@media (max-width: 480px) {
    .hero {
        padding: 30px 18px !important;
    }

    div.hero h1,
    div.hero h1 * {
        font-size: 26px !important;
        line-height: 1.2 !important;
        word-break: break-word;
    }

    div.hero p,
    div.hero p * {
        font-size: 15px !important;
    }
}


/* =====================================================
   SECTION TITLES
===================================================== */

.section-title {
    color: #172554 !important;
    font-size: 27px;
    font-weight: 800;
    margin-top: 30px;
    margin-bottom: 16px;
}


/* =====================================================
   INFO CARD
===================================================== */

.info-card {
    background: rgba(255,255,255,0.96);
    border: 1px solid #dfe5ff;
    border-radius: 24px;
    padding: 28px;
    margin-bottom: 25px;

    box-shadow:
        0 10px 30px rgba(30,41,100,0.07);
}

.info-card h3 {
    color: #1e1b4b !important;
    margin-top: 0;
}

.info-card p {
    color: #64748b !important;
}

/* ============================================================
   TEXT INPUTS
   ============================================================ */

.stTextInput label,
.stTextArea label,
.stMultiSelect label,
.stRadio label {
    color: #1e293b !important;
    font-weight: 700 !important;
}

/* Input boxes */
[data-baseweb="input"] {
    background: white !important;
    border: 2px solid #dbe4ff !important;
    border-radius: 15px !important;
}

/* Input text + cursor */
[data-baseweb="input"] input,
[data-baseweb="textarea"] textarea {
    color: #222222 !important;
    caret-color: #222222 !important;
}

/* Text area */
[data-baseweb="textarea"] {
    background: white !important;
    border: 2px solid #dbe4ff !important;
    border-radius: 15px !important;
}

/* Placeholder text */
[data-baseweb="input"] input::placeholder,
[data-baseweb="textarea"] textarea::placeholder {
    color: #94a3b8 !important;
    opacity: 1 !important;
}

/* Input when selected */
[data-baseweb="input"]:focus-within,
[data-baseweb="textarea"]:focus-within {
    border-color: #6366f1 !important;
    box-shadow: 0 0 0 2px rgba(99, 102, 241, 0.15) !important;
}

/* Multiselect */
[data-baseweb="select"] > div {
    background: white !important;
    border: 2px solid #dbe4ff !important;
    border-radius: 15px !important;
}

/* Multiselect text */
[data-baseweb="select"] input {
    color: #222222 !important;
    caret-color: #222222 !important;
}

/* Multiselect placeholder */
[data-baseweb="select"] input::placeholder {
    color: #94a3b8 !important;
}

/* Radio text */
.stRadio label {
    color: #1e293b !important;
}

/* Dropdown popover (the options list that opens) */
[data-baseweb="popover"] [data-baseweb="menu"],
[data-baseweb="popover"] ul[role="listbox"] {
    background: white !important;
    border: 1px solid #dbe4ff !important;
    border-radius: 12px !important;
    box-shadow: 0 12px 30px rgba(30,41,100,0.15) !important;
}

[data-baseweb="popover"] li,
[data-baseweb="popover"] [role="option"] {
    background: white !important;
    color: #172554 !important;
}

[data-baseweb="popover"] li:hover,
[data-baseweb="popover"] [role="option"]:hover,
[data-baseweb="popover"] [aria-selected="true"] {
    background: #eef2ff !important;
    color: #4338ca !important;
}

/* Even, consistent widths for form fields */
.stTextInput,
.stTextInput > div,
.stMultiSelect,
.stMultiSelect > div {
    width: 100% !important;
}

.stTextInput input {
    min-height: 44px !important;
    font-weight: 600 !important;
}
/* FINAL INPUT FIX */
.stTextInput input,
.stTextArea textarea {
    background-color: white !important;
    color: #222222 !important;
    caret-color: #222222 !important;
    -webkit-text-fill-color: #222222 !important;
}

.stTextInput input::placeholder,
.stTextArea textarea::placeholder {
    color: #64748b !important;
    -webkit-text-fill-color: #64748b !important;
}

/* =====================================================
   TEXT AREA
===================================================== */

[data-baseweb="textarea"] {
    background: white !important;
    border: 2px solid #dbe4ff !important;
    border-radius: 15px !important;
}

[data-baseweb="textarea"] textarea {
    background: white !important;
    color: #172554 !important;
    -webkit-text-fill-color: #172554 !important;
}

[data-baseweb="textarea"]:focus-within {
    border-color: #6366f1 !important;
}


/* =====================================================
   MULTI SELECT
===================================================== */

/* MULTI SELECT INPUT BOX ONLY */

.stMultiSelect div[data-baseweb="select"] > div:first-child {
    background-color: #FFFFFF !important;
    background: #FFFFFF !important;
    border: 2px solid #dbe4ff !important;
    border-radius: 15px !important;
}

.stMultiSelect div[data-baseweb="select"] > div:first-child input {
    background-color: #FFFFFF !important;
    color: #172554 !important;
    -webkit-text-fill-color: #172554 !important;
    font-weight:600 !important;
}
.stMultiSelect input::placeholder {
    font-weight: 600 !important;
    color: #64748b !important;
    -webkit-text-fill-color: #64748b !important;
}

/* Selected chips */

[data-baseweb="tag"] {
    background: linear-gradient(
        135deg,
        #6366f1,
        #8b5cf6
    ) !important;

    border-radius: 10px !important;
}

[data-baseweb="tag"] span {
    color: white !important;
}


/* =====================================================
   RADIO OPTIONS - TEXT FIX
===================================================== */

[data-testid="stRadio"] label {
    background: white !important;
    border: 2px solid #e0e7ff !important;
    border-radius: 14px !important;
    padding: 12px 16px !important;
    margin-right: 8px !important;
    color: #172554 !important;
}

[data-testid="stRadio"] label div {
    color: #172554 !important;
}

[data-testid="stRadio"] label p {
    color: #172554 !important;
    -webkit-text-fill-color: #172554 !important;
    font-weight: 600 !important;
    opacity: 1 !important;
}

[data-testid="stRadio"] label span {
    color: #172554 !important;
}

[data-testid="stRadio"] label:hover {
    background: #f5f3ff !important;
    border-color: #6366f1 !important;
}


/* =====================================================
   BUTTON
===================================================== */

.stButton > button {
    width: 100%;
    min-height: 55px !important;

    border-radius: 17px !important;
    border: none !important;

    background: linear-gradient(
        135deg,
        #4f46e5,
        #7c3aed
    ) !important;

    color: white !important;

    font-size: 17px !important;
    font-weight: 800 !important;

    box-shadow:
        0 10px 25px rgba(79,70,229,0.25);

    transition: all 0.2s ease;
}

.stButton > button:hover {
    transform: translateY(-2px);

    box-shadow:
        0 15px 32px rgba(79,70,229,0.32);
}


/* =====================================================
   CAREER CARD
===================================================== */

.career-card {
    background: white;

    border-radius: 24px;

    padding: 28px;

    margin: 18px 0;

    border: 1px solid #e2e8ff;

    box-shadow:
        0 12px 30px rgba(30,41,100,0.09);
}

.career-card h3 {
    color: #4338ca !important;
    margin-top: 0;
}

.career-card h4 {
    color: #312e81 !important;
}

.career-card p,
.career-card li {
    color: #334155 !important;
    line-height: 1.65;
}


/* =====================================================
   RECOMMENDATION OUTPUT
===================================================== */

.result-box {
    background: white;
    color:#222222;
    border-radius: 25px;

    padding: 30px;

    border: 1px solid #e0e7ff;

    box-shadow:
        0 12px 35px rgba(30,41,100,0.09);
}
/* AI RESULT TEXT */
.stMarkdown h1,
.stMarkdown h2,
.stMarkdown h3,
.stMarkdown h4 {
    color: #3730a3 !important;
}

.stMarkdown p,
.stMarkdown li {
    color: #334155 !important;
}


/* =====================================================
   STAT CARDS
===================================================== */

.stat-card {
    background: white;
    border-radius: 20px;

    padding: 24px;

    text-align: center;

    border: 1px solid #e0e7ff;

    box-shadow:
        0 8px 25px rgba(30,41,100,0.07);
}

.stat-number {
    color: #4f46e5 !important;

    font-size: 31px;

    font-weight: 850;
}

.stat-label {
    color: #64748b !important;

    font-size: 14px;
}


/* =====================================================
   SUCCESS / WARNING
===================================================== */
[data-testid="stAlert"] {
    border-radius: 15px !important;
}

[data-testid="stAlert"] p,
[data-testid="stAlert"] div,
[data-testid="stAlert"] span {
    color: #14532d !important;
    -webkit-text-fill-color: #14532d !important;
}


/* =====================================================
   FOOTER
===================================================== */

.footer-card {
    text-align: center;

    background:
        linear-gradient(
            135deg,
            #eef2ff,
            #f5f3ff,
            #eff6ff
        );

    border-radius: 24px;

    padding: 32px;

    margin-top: 45px;
}

.footer-card h3 {
    color: #312e81 !important;
}

.footer-card p {
    color: #64748b !important;
}
/* ONLY THE MULTISELECT INPUT BOXES */
[data-testid="stMultiSelect"] [data-baseweb="select"] {
    background: white !important;
}

[data-testid="stMultiSelect"] [data-baseweb="select"] > div {
    background: white !important;
    background-color: white !important;
}

[data-testid="stMultiSelect"] [data-baseweb="select"] > div > div {
    background: white !important;
    background-color: white !important;
}

[data-testid="stMultiSelect"] [data-baseweb="select"] input {
    background: white !important;
    color: #172554 !important;
    -webkit-text-fill-color: #172554 !important;
}

</style>
""",
    unsafe_allow_html=True
)

# =========================================================
# IBM AUTHENTICATION
# =========================================================

def get_iam_token():
    token_url = "https://iam.cloud.ibm.com/oidc/token"

    token_data = {
        "grant_type": "urn:ibm:params:oauth:grant-type:apikey",
        "apikey": API_KEY,
    }

    token_headers = {
        "Content-Type": "application/x-www-form-urlencoded"
    }

    response = requests.post(
        token_url,
        data=token_data,
        headers=token_headers,
        timeout=30
    )

    if response.status_code != 200:
        raise RuntimeError(
            f"IAM authentication failed ({response.status_code}): "
            f"{response.text[:500]}"
        )

    return response.json()["access_token"]


def call_granite(prompt):
    access_token = get_iam_token()

    endpoint = (
        f"{REGION_URL}/ml/v1/text/chat"
        "?version=2025-10-25"
    )

    headers = {
        "Accept": "application/json",
        "Content-Type": "application/json",
        "Authorization": f"Bearer {access_token}",
    }

    body = {
        "messages": [
            {
                "role": "user",
                "content": prompt
            }
        ],
        "project_id": PROJECT_ID,
        "model_id": "ibm/granite-4-h-small",
        "max_completion_tokens": 2000,
        "temperature": 0,
    }

    response = requests.post(
        endpoint,
        headers=headers,
        json=body,
        timeout=120
    )

    if response.status_code != 200:
        raise RuntimeError(
            f"Granite API failed ({response.status_code}): "
            f"{response.text[:1000]}"
        )

    data = response.json()

    return data["choices"][0]["message"]["content"]

# =========================================================
# BUILD AI PROMPT
# =========================================================

def build_prompt(
    name,
    education,
    strengths,
    weak_areas,
    interests,
    skills,
    preference
):

    return f"""

You are an expert AI career counselor helping a college student.

Analyze the student's complete profile.

STUDENT PROFILE

Name:
{name}

Education:
{education}

Strengths:
{strengths}

Areas to improve:
{weak_areas}

Interests:
{interests}

Current skills:
{skills}

Career preference:
{preference}


Give exactly THREE career recommendations.

Respond with ONLY valid JSON. No markdown, no code fences, no
commentary, no text before or after the JSON. The JSON must match
this exact schema:

{{
  "careers": [
    {{
      "title": "Career title",
      "match_score": 85,
      "why_it_fits": "2-3 sentence explanation",
      "skills_to_learn": ["skill", "skill", "skill", "skill"],
      "beginner_project": "One practical project, one sentence",
      "entry_level_roles": ["role", "role", "role"],
      "roadmap": ["step", "step", "step", "step"],
      "industry_outlook": "1-2 sentence explanation"
    }}
  ],
  "best_match": {{
    "title": "Chosen career title",
    "reason": "1 sentence on why this is the best match",
    "thirty_day_plan": {{
      "week_1": "focus for week 1",
      "week_2": "focus for week 2",
      "week_3": "focus for week 3",
      "week_4": "focus for week 4"
    }}
  }}
}}

The "careers" array must contain exactly 3 objects. match_score
must be an integer between 70 and 98. Use a friendly, encouraging,
practical tone in the text fields. Do not mention AI model names,
cloud services, APIs, technical backend systems, or implementation
details anywhere in the text.

"""


# =========================================================
# DEMO RESPONSE
# =========================================================

def demo_response(name, education="", strengths="", weak_areas="",
                   interests="", skills="", preference=""):

    strengths_txt = strengths if strengths else "your analytical thinking"
    interests_txt = interests if interests else "technology"
    skills_txt = skills if skills else "your current skill set"
    education_txt = education if education else "your studies"

    return {
        "careers": [
            {
                "title": "AI / Machine Learning Engineer",
                "match_score": 94,
                "why_it_fits": (
                    f"Based on your background in {education_txt} and "
                    f"strengths in {strengths_txt}, combined with your "
                    f"interest in {interests_txt}, this path can build "
                    f"well on {skills_txt}."
                ),
                "skills_to_learn": [
                    "Python", "Statistics", "NumPy", "Pandas",
                    "Machine Learning", "SQL"
                ],
                "beginner_project": "Build a student performance prediction system.",
                "entry_level_roles": ["AI Intern", "Junior ML Engineer", "Data Analyst"],
                "roadmap": [
                    "Learn Python",
                    "Learn statistics and data handling",
                    "Learn Machine Learning",
                    "Build 2-3 projects"
                ],
                "industry_outlook": "AI and ML skills are in high demand across nearly every industry."
            },
            {
                "title": "Software Developer",
                "match_score": 89,
                "why_it_fits": (
                    f"Software development is a strong option given your "
                    f"interest in {interests_txt} and strengths in "
                    f"{strengths_txt}, and it builds naturally on {skills_txt}."
                ),
                "skills_to_learn": ["Programming", "DSA", "Git", "SQL", "Web development"],
                "beginner_project": "Build a career guidance web application.",
                "entry_level_roles": ["Software Developer", "Web Developer", "Graduate Engineer"],
                "roadmap": [
                    "Learn programming",
                    "Practice DSA",
                    "Build applications",
                    "Prepare for placements"
                ],
                "industry_outlook": "Software roles remain one of the most consistently in-demand career paths."
            },
            {
                "title": "Data Scientist",
                "match_score": 85,
                "why_it_fits": (
                    f"Your strengths in {strengths_txt} and interest in "
                    f"{interests_txt} can lead toward data science, "
                    f"especially alongside {skills_txt}."
                ),
                "skills_to_learn": [
                    "Python", "SQL", "Statistics", "Pandas",
                    "Data visualization", "Machine Learning"
                ],
                "beginner_project": "Analyze a real-world student or placement dataset.",
                "entry_level_roles": ["Data Analyst", "Junior Data Scientist", "BI Analyst"],
                "roadmap": [
                    "Learn Python",
                    "Learn SQL",
                    "Learn statistics",
                    "Build a data portfolio"
                ],
                "industry_outlook": "Data science continues to grow across nearly every sector."
            }
        ],
        "best_match": {
            "title": "AI / Machine Learning Engineer",
            "reason": "It offers the strongest match to your current strengths and interests.",
            "thirty_day_plan": {
                "week_1": "Python fundamentals",
                "week_2": "NumPy, Pandas and SQL",
                "week_3": "Machine learning basics",
                "week_4": "Build your first AI project"
            }
        }
    }


# =========================================================
# HERO
# =========================================================

# =========================================================
# HERO
# =========================================================

import base64
import streamlit.components.v1 as components

with open("LOGO.jpeg", "rb") as f:
    logo = base64.b64encode(f.read()).decode()

components.html(f"""
<div style="
    position:relative;
    width:100%;
    height:220px;
    border-radius:32px;
    background:linear-gradient(120deg,#3730a3,#4f46e5,#7c3aed,#9333ea);
    color:white;
    display:flex;
    align-items:center;
    justify-content:center;
    text-align:center;
    box-sizing:border-box;
">
    <img src="data:image/jpeg;base64,{logo}"
         style="
         position:absolute;
         left:30px;
         top:50%;
         transform:translateY(-50%);
         width:160px;
         height:160px;
         object-fit:contain;
         border-radius:15px;
         mix-blend-mode:screen;
         ">

    <div>
        <h1 style="margin:0;font-size:48px;color:white;">
            CareerCompanionAI
        </h1>
        <p style="font-size:19px;color:#eef2ff;">
            Discover your strengths. Explore careers. Build your future.
        </p>
    </div>
</div>
""", height=240)
# =========================================================
# INTRO
# =========================================================

st.markdown(
    """
<div class="section-title">
🚀 Let's build your career path
</div>
""",
    unsafe_allow_html=True
)

st.markdown(
    """
<div class="info-card">

<h3>✨ Tell us about yourself</h3>

<p>
Answer a few simple questions and get a personalized career
roadmap based on your interests, strengths and goals.
</p>

</div>
""",
    unsafe_allow_html=True
)


# =========================================================
# BASIC PROFILE
# =========================================================

col1, col2 = st.columns(2)

with col1:

    name = st.text_input(
        "👤 Your name",
        placeholder="Example: Vivek"
    )

with col2:

    education = st.text_input(
        "🎓 Education",
        placeholder="Example: B.Tech CSE 4th Year"
    )


# =========================================================
# INTERESTS
# =========================================================

st.markdown(
    '<div class="section-title">💡 What are you interested in?</div>',
    unsafe_allow_html=True
)

interest_options = [

    "🤖 AI & Machine Learning",

    "💻 Software Development",

    "📊 Data Science",

    "🎨 UI / UX Design",

    "☁️ Cloud Computing",

    "🔐 Cybersecurity",

    "🌐 Web Development",

    "📱 Mobile App Development",

    "🔬 Research",

    "📈 Business & Management"
]


interests_selected = st.multiselect(
    "Choose the areas that interest you",
    interest_options,
    placeholder="Select one or more interests, or type your own",
    accept_new_options=True
)

interests = ", ".join(interests_selected)


# =========================================================
# STRENGTHS
# =========================================================

st.markdown(
    '<div class="section-title">💪 What are you good at?</div>',
    unsafe_allow_html=True
)

strength_options = [

    "Logical Thinking",

    "Problem Solving",

    "Programming",

    "Mathematics",

    "Analytical Thinking",

    "Communication",

    "Creativity",

    "Leadership",

    "Research",

    "Teamwork"
]

strengths_selected = st.multiselect(
    "Select your strengths",
    strength_options,
    placeholder="Choose your strongest areas, or type your own",
    accept_new_options=True
)

strengths = ", ".join(strengths_selected)


# =========================================================
# CURRENT SKILLS
# =========================================================

st.markdown(
    '<div class="section-title">🧩 Your current skills</div>',
    unsafe_allow_html=True
)

skills = st.text_input(
    "What skills do you already know?",
    placeholder="Example: Python, Java, SQL, AWS, Linux"
)


# =========================================================
# IMPROVEMENT
# =========================================================

st.markdown(
    '<div class="section-title">📈 What would you like to improve?</div>',
    unsafe_allow_html=True
)

weak_options = [

    "Programming",

    "DSA",

    "Communication",

    "Public Speaking",

    "Technical Skills",

    "Interview Skills",

    "Mathematics",

    "English",

    "Leadership",

    "Project Building"
]


weak_selected = st.multiselect(
    "Select areas you want to improve",
    weak_options,
    placeholder="Choose areas, or type your own",
    accept_new_options=True
)

weak_areas = ", ".join(weak_selected)


# =========================================================
# CAREER PREFERENCE
# =========================================================

st.markdown(
    '<div class="section-title">🎯 What type of career do you want?</div>',
    unsafe_allow_html=True
)

preference = st.radio(
    "Choose the option closest to your goal",
    [
        "🚀 High-growth technology career",

        "💼 Stable software career",

        "🎨 Creative career",

        "🔬 Research / advanced technology",

        "🌍 Flexible / remote career",

        "🤔 I'm not sure yet"
    ],

    horizontal=True
)


# =========================================================
# GENERATE BUTTON
# =========================================================

st.markdown("<br>", unsafe_allow_html=True)

generate = st.button(
    "✨ Discover My Career Path",
    type="primary",
    use_container_width=True
)


# =========================================================
# GENERATE RECOMMENDATIONS
# =========================================================

if generate:

    if not name.strip():

        st.warning(
            "👤 Please enter your name first."
        )

        st.stop()

    if not education.strip():

        st.warning(
            "🎓 Please enter your education."
        )

        st.stop()

    prompt = build_prompt(
        name,
        education,
        strengths,
        weak_areas,
        interests,
        skills,
        preference
    )

    with st.spinner(
        "✨ Your career companion is analyzing your profile..."
    ):

        try:

            if API_KEY and PROJECT_ID:

                raw_output = call_granite(prompt)

                # Clean up in case the model wraps JSON in code fences
                cleaned = raw_output.strip()
                cleaned = re.sub(r'^```(?:json)?', '', cleaned).strip()
                cleaned = re.sub(r'```$', '', cleaned).strip()

                data = json.loads(cleaned)

                live = True

            else:

                data = demo_response(
                    name, education, strengths, weak_areas,
                    interests, skills, preference
                )

                live = False

        except Exception as e:
            print("IBM ERROR:",repr(e))
            data = demo_response(
                name, education, strengths, weak_areas,
                interests, skills, preference
            )

            live = False

            st.warning(
                "We couldn't connect to the career guidance "
                "service right now. Showing a sample recommendation "
                "so you can continue testing."
            )


    # =====================================================
    # RESULTS
    # =====================================================

    st.markdown(
        '<div class="section-title">🌟 Your Career Matches</div>',
        unsafe_allow_html=True
    )

    if live:

        st.success(
            "✨ Your personalized career guidance is ready!"
        )


    # -----------------------------------------------------
    # Display career data (built directly from structured
    # JSON — no text guessing, so it always renders correctly)
    # -----------------------------------------------------
    careers = data.get("careers", [])

    for i, career in enumerate(careers, 1):
        title = career.get("title", "Career option")
        score = career.get("match_score", 0)

        st.markdown(
            f'<div class="career-card" style="padding:14px 18px;margin-bottom:6px;">'
            f'<div style="display:flex;justify-content:space-between;">'
            f'<h3 style="margin:0;">{i}. {title}</h3>'
            f'<span style="color:#4338ca;font-weight:700;">{score}%</span></div>'
            f'<div style="height:6px;background:#e0e7ff;border-radius:4px;margin-top:8px;">'
            f'<div style="width:{score}%;height:100%;background:#4f46e5;border-radius:4px;"></div>'
            f'</div></div>',
            unsafe_allow_html=True
        )

        with st.expander(f"{i}. {title}  ·  {score}% match"):
            st.markdown(f"**Why it fits**\n\n{career.get('why_it_fits', '')}")

            skills = career.get("skills_to_learn", [])
            if skills:
                st.markdown(
                    "**Skills to learn**\n\n"
                    + "\n".join(f"- {s}" for s in skills)
                )

            if career.get("beginner_project"):
                st.markdown(f"**Beginner project**\n\n{career['beginner_project']}")

            roles = career.get("entry_level_roles", [])
            if roles:
                st.markdown(
                    "**Entry-level roles**\n\n"
                    + "\n".join(f"- {r}" for r in roles)
                )

            roadmap = career.get("roadmap", [])
            if roadmap:
                st.markdown(
                    "**Roadmap**\n\n"
                    + "\n".join(f"{n}. {step}" for n, step in enumerate(roadmap, 1))
                )

            if career.get("industry_outlook"):
                st.markdown(f"**Industry outlook**\n\n{career['industry_outlook']}")

    best_match = data.get("best_match", {})
    if best_match:
        plan = best_match.get("thirty_day_plan", {})
        week_labels = [
            ("Week 1", plan.get("week_1", "")),
            ("Week 2", plan.get("week_2", "")),
            ("Week 3", plan.get("week_3", "")),
            ("Week 4", plan.get("week_4", "")),
        ]

        week_html = ""
        for i, (label, text) in enumerate(week_labels, 1):
            if not text:
                continue
            week_html += (
                f'<div style="display:flex;gap:10px;margin-bottom:8px;">'
                f'<div style="width:26px;height:26px;border-radius:50%;background:#e0e7ff;'
                f'color:#4338ca;display:flex;align-items:center;justify-content:center;'
                f'font-weight:700;flex-shrink:0;">{i}</div>'
                f'<p style="margin:0;"><b>{label}:</b> {text}</p></div>'
            )

        bm_title = best_match.get("title", "Best match")
        bm_reason = best_match.get("reason", "")

        st.markdown(
            f'<div class="career-card">'
            f'<span style="background:#e0e7ff;color:#4338ca;font-size:12px;'
            f'padding:3px 10px;border-radius:8px;">Best match</span>'
            f'<h2 style="margin:10px 0 4px;">{bm_title}</h2>'
            f'<p style="color:#64748b;margin:0 0 12px;font-size:14px;">{bm_reason}</p>'
            f'<p style="font-weight:600;margin:0 0 10px;">First 30-day plan</p>'
            f'{week_html}'
            f'</div>',
            unsafe_allow_html=True
        )
    # =====================================================
    # SNAPSHOT
    # =====================================================

    st.markdown(
        '<div class="section-title">📊 Your Career Snapshot</div>',
        unsafe_allow_html=True
    )

    c1, c2, c3, c4 = st.columns(4)

    with c1:

        st.markdown(
            """
            <div class="stat-card">

            <div class="stat-number">
            3
            </div>

            <div class="stat-label">
            Career Matches
            </div>

            </div>
            """,
            unsafe_allow_html=True
        )

    with c2:

        st.markdown(
            """
            <div class="stat-card">

            <div class="stat-number">
            10+
            </div>

            <div class="stat-label">
            Profile Factors
            </div>

            </div>
            """,
            unsafe_allow_html=True
        )

    with c3:

        st.markdown(
            """
            <div class="stat-card">

            <div class="stat-number">
            30
            </div>

            <div class="stat-label">
            Day Starter Plan
            </div>

            </div>
            """,
            unsafe_allow_html=True
        )

    with c4:

        st.markdown(
            """
            <div class="stat-card">

            <div class="stat-number">
            ∞
            </div>

            <div class="stat-label">
            Growth Potential
            </div>

            </div>
            """,
            unsafe_allow_html=True
        )


# =========================================================
# BOTTOM SECTION
# =========================================================

st.markdown(
    """
<div class="footer-card">

<h3>🌱 Your future starts with one decision.</h3>

<p>
Explore. Learn. Build. Grow.
</p>

</div>
""",
    unsafe_allow_html=True
)
