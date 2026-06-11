import streamlit as st
import json
from pathlib import Path
from datetime import datetime
import base64
from fpdf import FPDF
import tempfile
import os

# Page configuration
st.set_page_config(
    page_title="CoActions - Career Guidance",
    page_icon="🎯",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# Custom CSS for Professional App with Background Image
st.markdown("""
<style>

    /* Background Image with Overlay */
    .stApp {
        background-image: url("https://images.unsplash.com/photo-1557683304-673a230ec87c?q=80&w=2029&auto=format&fit=crop");
        background-size: cover;
        background-position: center;
        background-attachment: fixed;
        background-repeat: no-repeat;
    }
    
    /* Dark Overlay for better readability */
    .stApp::before {
        content: "";
        position: fixed;
        top: 0;
        left: 0;
        right: 0;
        bottom: 0;
        background: linear-gradient(135deg, rgba(0,0,0,0.5), rgba(0,0,0,0.3));
        z-index: -1;
    }
    
    /* Main Card - Glassmorphism Effect */
    .main-card {
        background: rgba(255, 255, 255, 0.94);
        backdrop-filter: blur(12px);
        border-radius: 28px;
        padding: 2rem;
        box-shadow: 0 25px 50px -12px rgba(0,0,0,0.3);
        border: 1px solid rgba(255,255,255,0.3);
        margin-bottom: 1rem;
    }
    
    /* App Title with Gradient */
    .app-title {
        font-size: 2.5rem;
        font-weight: 800;
        background: linear-gradient(135deg, #667eea, #764ba2);
        -webkit-background-clip: text;
        background-clip: text;
        color: transparent;
    }
    
    /* Welcome Heading */
    .welcome-heading {
        background: linear-gradient(135deg, #667eea, #764ba2);
        -webkit-background-clip: text;
        background-clip: text;
        color: transparent;
        font-size: 2rem;
        font-weight: 700;
        margin-bottom: 0.5rem;
        text-align: center;
    }
    
    /* User Cards - Frosted Glass */
    .user-card {
        background: rgba(255, 255, 255, 0.85);
        backdrop-filter: blur(8px);
        border-radius: 24px;
        padding: 1.8rem;
        text-align: center;
        transition: all 0.3s ease;
        border: 2px solid rgba(102, 126, 234, 0.3);
        margin: 0.5rem;
        cursor: pointer;
    }
    .user-card:hover {
        transform: translateY(-6px);
        border-color: #667eea;
        background: rgba(255, 255, 255, 0.95);
        box-shadow: 0 20px 40px -12px rgba(102,126,234,0.4);
    }
    
    /* Modern Buttons */
    .stButton > button {
        background: linear-gradient(135deg, #667eea, #764ba2);
        color: white;
        border: none;
        border-radius: 40px;
        padding: 0.7rem 1.8rem;
        font-weight: 600;
        transition: all 0.3s ease;
        width: 100%;
    }
    .stButton > button:hover {
        background: linear-gradient(135deg, #5a67d8, #6b46c1);
        transform: translateY(-2px);
        box-shadow: 0 10px 20px -5px rgba(102,126,234,0.4);
    }
    
    /* Menu Buttons */
    .menu-btn {
        background: rgba(255,255,255,0.2) !important;
        backdrop-filter: blur(4px);
        border: 1px solid rgba(255,255,255,0.3) !important;
        color: white !important;
        padding: 0.5rem 1.2rem !important;
        border-radius: 40px !important;
        font-weight: 600 !important;
        font-size: 0.9rem !important;
        transition: all 0.3s ease !important;
    }
    .menu-btn:hover {
        background: rgba(102, 126, 234, 0.3) !important;
        color: #667eea !important;
        border-color: #667eea !important;
    }
    
    /* Question Cards */
    .question-card {
        background: rgba(247, 250, 252, 0.9);
        border-radius: 20px;
        padding: 1rem;
        margin: 0.8rem 0;
        border-left: 5px solid #667eea;
        backdrop-filter: blur(4px);
    }
    
    /* Stream Cards - Gradient Cards */
    .stream-card-high {
        background: linear-gradient(135deg, #11998e, #38ef7d);
        border-radius: 20px;
        padding: 1.5rem;
        text-align: center;
        transition: all 0.3s ease;
        margin: 0.5rem;
        cursor: pointer;
        color: white;
    }
    .stream-card-good {
        background: linear-gradient(135deg, #f2994a, #f2c94c);
        border-radius: 20px;
        padding: 1.5rem;
        text-align: center;
        transition: all 0.3s ease;
        margin: 0.5rem;
        cursor: pointer;
        color: white;
    }
    .stream-card-fair {
        background: linear-gradient(135deg, #ff6b6b, #feca57);
        border-radius: 20px;
        padding: 1.5rem;
        text-align: center;
        transition: all 0.3s ease;
        margin: 0.5rem;
        cursor: pointer;
        color: white;
    }
    .stream-card-potential {
        background: linear-gradient(135deg, #4facfe, #00f2fe);
        border-radius: 20px;
        padding: 1.5rem;
        text-align: center;
        transition: all 0.3s ease;
        margin: 0.5rem;
        cursor: pointer;
        color: white;
    }
    .stream-card-low {
        background: linear-gradient(135deg, #8e9eab, #eef2f3);
        border-radius: 20px;
        padding: 1.5rem;
        text-align: center;
        transition: all 0.3s ease;
        margin: 0.5rem;
        cursor: pointer;
        color: #4a5568;
    }
    
    .stream-card-high:hover, .stream-card-good:hover, 
    .stream-card-fair:hover, .stream-card-potential:hover, 
    .stream-card-low:hover {
        transform: translateY(-8px);
        box-shadow: 0 20px 40px -12px rgba(0,0,0,0.3);
    }
    
    /* Score Bar */
    .score-bar {
        background: rgba(0,0,0,0.2);
        border-radius: 20px;
        height: 10px;
        margin: 0.5rem 0;
        overflow: hidden;
    }
    .score-fill {
        background: linear-gradient(90deg, #11998e, #38ef7d);
        border-radius: 20px;
        height: 100%;
        transition: width 1s ease;
    }
    
    /* Match Card */
    .match-high {
        background: linear-gradient(135deg, rgba(232,245,233,0.9), rgba(200,230,201,0.9));
        backdrop-filter: blur(4px);
        border-left: 8px solid #11998e;
        border-radius: 20px;
        padding: 1.5rem;
        margin: 1rem 0;
    }
    
    /* Radio Buttons */
    .stRadio > div {
        background: rgba(255,255,255,0.9);
        padding: 0.8rem;
        border-radius: 20px;
    }
    
    /* Progress Bar */
    .progress-text {
        color: #667eea;
        font-size: 0.85rem;
        margin-top: 0.5rem;
        font-weight: 600;
    }
    
    /* Page Counter */
    .page-counter {
        background: linear-gradient(135deg, #667eea, #764ba2);
        border-radius: 20px;
        padding: 0.5rem 1rem;
        text-align: center;
        margin: 1rem 0;
        color: white;
        font-weight: 600;
    }
    
    /* User Type Indicator */
    .user-type-indicator {
        background: linear-gradient(135deg, #667eea, #764ba2);
        color: white;
        padding: 0.3rem 1rem;
        border-radius: 20px;
        display: inline-block;
        margin-bottom: 1rem;
        font-weight: 600;
    }
    
    /* Scrollbar */
    ::-webkit-scrollbar {
        width: 8px;
        height: 8px;
    }
    ::-webkit-scrollbar-track {
        background: rgba(255,255,255,0.1);
        border-radius: 10px;
    }
    ::-webkit-scrollbar-thumb {
        background: linear-gradient(135deg, #667eea, #764ba2);
        border-radius: 10px;
    }
    
    /* Print styles */
    @media print {
        .stButton, .stDownloadButton, .menu-container {
            display: none !important;
        }
        .main-card {
            background: white !important;
            box-shadow: none !important;
        }
        .stApp::before {
            display: none !important;
        }
    }

    /* ==================== FIXED DROPDOWN VISIBILITY - CRITICAL FIX ==================== */
    
    /* SelectBox Container - Base styling */
    .stSelectbox > div {
        background: white !important;
        border-radius: 12px !important;
    }
    
    /* The main select box input field */
    .stSelectbox div[data-baseweb="select"] {
        background: white !important;
        border: 2px solid #1E88E5 !important;
        border-radius: 12px !important;
        min-height: 45px !important;
    }
    
    .stSelectbox div[data-baseweb="select"]:hover {
        border-color: #1565C0 !important;
        background: #E3F2FD !important;
    }
    
    /* THE MOST IMPORTANT FIX - Selected value text */
    .stSelectbox div[data-baseweb="select"] div {
        color: #1a1a2e !important;
        font-size: 1rem !important;
        font-weight: 500 !important;
    }
    
    /* The value display span */
    .stSelectbox div[data-baseweb="select"] span {
        color: #1a1a2e !important;
        font-weight: 500 !important;
    }
    
    /* Dropdown arrow icon */
    .stSelectbox svg {
        fill: #1E88E5 !important;
    }
    
    /* Dropdown menu container (when opened) */
    div[data-baseweb="popover"] {
        background: white !important;
        border: 1px solid #1E88E5 !important;
        border-radius: 12px !important;
        box-shadow: 0 4px 12px rgba(0,0,0,0.15) !important;
    }
    
    /* Dropdown options list */
    ul[role="listbox"] {
        background: white !important;
        border-radius: 12px !important;
    }
    
    /* Individual option items */
    li[role="option"] {
        color: #1a1a2e !important;
        background: white !important;
        padding: 10px 15px !important;
        font-size: 0.9rem !important;
    }
    
    /* Hover effect on options */
    li[role="option"]:hover {
        background: #E3F2FD !important;
        color: #1E88E5 !important;
    }
    
    /* Selected option in dropdown */
    li[role="option"][aria-selected="true"] {
        background: #1E88E5 !important;
        color: white !important;
    }
    
    /* ==================== INPUT FIELDS STYLING ==================== */
    
    /* Text Input Fields */
    .stTextInput > div > div > input {
        background: white !important;
        border: 2px solid #1E88E5 !important;
        border-radius: 12px !important;
        padding: 12px 15px !important;
        font-size: 1rem !important;
        color: #1a1a2e !important;
        transition: all 0.3s ease !important;
    }
    
    .stTextInput > div > div > input:focus {
        border-color: #1565C0 !important;
        box-shadow: 0 0 0 3px rgba(30, 136, 229, 0.2) !important;
        outline: none !important;
    }
    
    .stTextInput > div > div > input:hover {
        border-color: #1565C0 !important;
        background: #E3F2FD !important;
    }
    
    /* Number Input Fields */
    .stNumberInput > div > div > input {
        background: white !important;
        border: 2px solid #1E88E5 !important;
        border-radius: 12px !important;
        padding: 12px 15px !important;
        font-size: 1rem !important;
        color: #1a1a2e !important;
        transition: all 0.3s ease !important;
    }
    
    .stNumberInput > div > div > input:focus {
        border-color: #1565C0 !important;
        box-shadow: 0 0 0 3px rgba(30, 136, 229, 0.2) !important;
        outline: none !important;
    }
    
    /* Labels */
    .stTextInput label, 
    .stNumberInput label, 
    .stSelectbox label {
        color: #1565C0 !important;
        font-weight: 600 !important;
        font-size: 0.9rem !important;
        margin-bottom: 5px !important;
    }
    
    /* Placeholder text */
    .stTextInput input::placeholder,
    .stNumberInput input::placeholder {
        color: #90A4AE !important;
        font-size: 0.9rem !important;
    }
       
</style>
""", unsafe_allow_html=True)

# Initialize session state
if 'page' not in st.session_state:
    st.session_state.page = 'welcome'
if 'user_type' not in st.session_state:
    st.session_state.user_type = None
if 'student_city' not in st.session_state:
    st.session_state.student_city = ""
if 'student_state' not in st.session_state:
    st.session_state.student_state = ""
if 'responses' not in st.session_state:
    st.session_state.responses = {}
if 'current_page' not in st.session_state:
    st.session_state.current_page = 0
if 'questions_list' not in st.session_state:
    st.session_state.questions_list = []
if 'categories_data' not in st.session_state:
    st.session_state.categories_data = {}
if 'recommended_categories' not in st.session_state:
    st.session_state.recommended_categories = []
if 'selected_stream' not in st.session_state:
    st.session_state.selected_stream = None
if 'student_name' not in st.session_state:
    st.session_state.student_name = ""
if 'student_age' not in st.session_state:
    st.session_state.student_age = ""
if 'student_institution' not in st.session_state:
    st.session_state.student_institution = ""
if 'student_grade' not in st.session_state:
    st.session_state.student_grade = ""
if 'show_about' not in st.session_state:
    st.session_state.show_about = False
if 'show_contact' not in st.session_state:
    st.session_state.show_contact = False
if 'selected_career' not in st.session_state:
    st.session_state.selected_career = None
if 'show_career_detail' not in st.session_state:
    st.session_state.show_career_detail = False
if 'personality_responses' not in st.session_state:
    st.session_state.personality_responses = {}
if 'personality_current_index' not in st.session_state:
    st.session_state.personality_current_index = 0
if 'personality_questions' not in st.session_state:
    st.session_state.personality_questions = []
if 'personality_completed' not in st.session_state:
    st.session_state.personality_completed = False
if 'personality_pathway' not in st.session_state:
    st.session_state.personality_pathway = None

# Load JSON files
@st.cache_data
def load_json_file(file_path):
    """Load JSON file with error handling"""
    try:
        full_path = Path(file_path)
        if not full_path.exists():
            st.error(f"File not found: {file_path}")
            return None
        with open(full_path, 'r', encoding='utf-8') as f:
            data = json.load(f)
        
        # Debug info
        total_questions = 0
        for cat in data.get('categories', []):
            # Check for both formats
            if 'questions' in cat:
                total_questions += len(cat['questions'])
            else:
                total_questions += len(cat.get('parent_questions', []))
                total_questions += len(cat.get('subfield_questions', []))
        
        print(f"Loaded {file_path}: {len(data.get('categories', []))} categories, {total_questions} questions")
        return data
    except Exception as e:
        st.error(f"Error loading {file_path}: {str(e)}")
        return None
        
def extract_questions_from_json(data):
    """Extract questions and categories from JSON format"""
    questions = []
    categories = {}
    
    if not data or 'categories' not in data:
        print("No categories found in data")
        return questions, categories
    
    for category in data.get('categories', []):
        cat_id = category.get('category_id')
        cat_name = category.get('category_name')
        cat_icon = category.get('icon', '📁')
        cat_color = category.get('color', '#6B7280')
        
        categories[cat_id] = {
            'id': cat_id,
            'name': cat_name,
            'icon': cat_icon,
            'color': cat_color,
            'score': 0,
            'question_count': 0,
            'subfield_scores': {}
        }
        
        # IMPORTANT: Use 'questions' key (not 'parent_questions' or 'subfield_questions')
        # This works for both school.json and college.json
        category_questions = category.get('questions', [])
        
        # Also handle legacy format (parent_questions + subfield_questions)
        if not category_questions:
            # Legacy format: combine parent and subfield questions
            parent_qs = category.get('parent_questions', [])
            subfield_qs = category.get('subfield_questions', [])
            category_questions = parent_qs + subfield_qs
        
        print(f"Loading {len(category_questions)} questions for {cat_name}")
        
        for q in category_questions:
            q_id = q.get('id')
            q_text = q.get('text')
            q_weight = q.get('weight', 1.0)
            q_type = q.get('type', 'parent')
            q_subfield = q.get('subfield')
            
            # Skip if missing required fields
            if not q_id or not q_text:
                print(f"Warning: Question missing id or text in {cat_name}")
                continue
            
            # Add to questions list
            questions.append({
                'id': q_id,
                'text': q_text,
                'category_id': cat_id,
                'category_name': cat_name,
                'weight': q_weight,
                'type': q_type,
                'subfield': q_subfield
            })
            
            # Initialize subfield tracking if needed
            if q_subfield and q_subfield != 'null' and q_subfield is not None:
                if q_subfield not in categories[cat_id]['subfield_scores']:
                    categories[cat_id]['subfield_scores'][q_subfield] = {
                        'score': 0,
                        'max_score': 0,
                        'count': 0
                    }
            
            # Increment question count
            categories[cat_id]['question_count'] += 1
    
    print(f"Total questions extracted: {len(questions)}")
    print(f"Total categories: {len(categories)}")
    
    return questions, categories

def get_personality_questions(user_type):
    """Get 25 personality questions based on user type"""
    school_questions = [
        {"id": 1, "text": "Do you enjoy solving puzzles or math problems in your free time?", "options": ["Yes, a lot", "Sometimes", "Not really"]},
        {"id": 2, "text": "Do you like drawing, painting, or crafting things?", "options": ["Yes, a lot", "Sometimes", "Not really"]},
        {"id": 3, "text": "Are you interested in how computers and games work?", "options": ["Yes, a lot", "Sometimes", "Not really"]},
        {"id": 4, "text": "Do you enjoy reading storybooks or writing small stories?", "options": ["Yes, a lot", "Sometimes", "Not really"]},
        {"id": 5, "text": "Do you like helping classmates with their work?", "options": ["Yes, a lot", "Sometimes", "Not really"]},
        {"id": 6, "text": "Are you curious about stars, planets, or science experiments?", "options": ["Yes, a lot", "Sometimes", "Not really"]},
        {"id": 7, "text": "Do you enjoy organizing events or leading a group?", "options": ["Yes, a lot", "Sometimes", "Not really"]},
        {"id": 8, "text": "Do you like playing sports or outdoor games?", "options": ["Yes, a lot", "Sometimes", "Not really"]},
        {"id": 9, "text": "Do you enjoy listening to music or playing an instrument?", "options": ["Yes, a lot", "Sometimes", "Not really"]},
        {"id": 10, "text": "Do you like fixing broken toys or gadgets?", "options": ["Yes, a lot", "Sometimes", "Not really"]},
        {"id": 11, "text": "Do you enjoy debating or discussing topics with friends?", "options": ["Yes, a lot", "Sometimes", "Not really"]},
        {"id": 12, "text": "Do you like memorizing facts or learning new words?", "options": ["Yes, a lot", "Sometimes", "Not really"]},
        {"id": 13, "text": "Do you enjoy gardening or taking care of pets?", "options": ["Yes, a lot", "Sometimes", "Not really"]},
        {"id": 14, "text": "Do you prefer working alone rather than in a group?", "options": ["Yes, a lot", "Sometimes", "Not really"]},
        {"id": 15, "text": "Are you good at explaining things to others?", "options": ["Yes, a lot", "Sometimes", "Not really"]},
        {"id": 16, "text": "Do you enjoy acting or performing on stage?", "options": ["Yes, a lot", "Sometimes", "Not really"]},
        {"id": 17, "text": "Do you like collecting things like stamps, coins, or rocks?", "options": ["Yes, a lot", "Sometimes", "Not really"]},
        {"id": 18, "text": "Do you enjoy cooking or baking with family?", "options": ["Yes, a lot", "Sometimes", "Not really"]},
        {"id": 19, "text": "Do you like learning new languages?", "options": ["Yes, a lot", "Sometimes", "Not really"]},
        {"id": 20, "text": "Do you enjoy solving riddles or brain teasers?", "options": ["Yes, a lot", "Sometimes", "Not really"]},
        {"id": 21, "text": "Do you like building things with LEGO or blocks?", "options": ["Yes, a lot", "Sometimes", "Not really"]},
        {"id": 22, "text": "Do you enjoy planning trips or schedules?", "options": ["Yes, a lot", "Sometimes", "Not really"]},
        {"id": 23, "text": "Are you interested in how plants grow or animals behave?", "options": ["Yes, a lot", "Sometimes", "Not really"]},
        {"id": 24, "text": "Do you like video editing or making digital art?", "options": ["Yes, a lot", "Sometimes", "Not really"]},
        {"id": 25, "text": "Do you enjoy learning about history or ancient civilizations?", "options": ["Yes, a lot", "Sometimes", "Not really"]}
    ]
    
    college_questions = [
        {"id": 1, "text": "Do you prefer theoretical research or hands-on projects?", "options": ["Theoretical Research", "Both equally", "Hands-on Projects"]},
        {"id": 2, "text": "Do you enjoy data analysis and statistics?", "options": ["Yes, a lot", "Sometimes", "Not really"]},
        {"id": 3, "text": "Are you interested in entrepreneurship and startups?", "options": ["Very interested", "Somewhat", "Not at all"]},
        {"id": 4, "text": "Do you like teaching or mentoring juniors?", "options": ["Yes, a lot", "Sometimes", "Not really"]},
        {"id": 5, "text": "Do you enjoy coding or developing software?", "options": ["Yes, a lot", "Sometimes", "Not really"]},
        {"id": 6, "text": "Are you interested in financial markets or investing?", "options": ["Very interested", "Somewhat", "Not at all"]},
        {"id": 7, "text": "Do you like writing essays, blogs, or research papers?", "options": ["Yes, a lot", "Sometimes", "Not really"]},
        {"id": 8, "text": "Do you enjoy public speaking or presentations?", "options": ["Yes, a lot", "Sometimes", "Not really"]},
        {"id": 9, "text": "Are you interested in psychology or human behavior?", "options": ["Very interested", "Somewhat", "Not at all"]},
        {"id": 10, "text": "Do you like working with robots or electronics?", "options": ["Yes, a lot", "Sometimes", "Not really"]},
        {"id": 11, "text": "Do you enjoy social media management or digital marketing?", "options": ["Yes, a lot", "Sometimes", "Not really"]},
        {"id": 12, "text": "Are you interested in environmental sustainability?", "options": ["Very interested", "Somewhat", "Not at all"]},
        {"id": 13, "text": "Do you like designing graphics or user interfaces?", "options": ["Yes, a lot", "Sometimes", "Not really"]},
        {"id": 14, "text": "Do you enjoy scientific lab work or experiments?", "options": ["Yes, a lot", "Sometimes", "Not really"]},
        {"id": 15, "text": "Are you interested in law, politics, or governance?", "options": ["Very interested", "Somewhat", "Not at all"]},
        {"id": 16, "text": "Do you like event management or coordinating teams?", "options": ["Yes, a lot", "Sometimes", "Not really"]},
        {"id": 17, "text": "Do you enjoy traveling and learning new cultures?", "options": ["Yes, a lot", "Sometimes", "Not really"]},
        {"id": 18, "text": "Are you good at negotiating or persuading people?", "options": ["Yes, a lot", "Sometimes", "Not really"]},
        {"id": 19, "text": "Do you like photography or filmmaking?", "options": ["Yes, a lot", "Sometimes", "Not really"]},
        {"id": 20, "text": "Are you interested in AI and machine learning?", "options": ["Very interested", "Somewhat", "Not at all"]},
        {"id": 21, "text": "Do you enjoy volunteering or social work?", "options": ["Yes, a lot", "Sometimes", "Not really"]},
        {"id": 22, "text": "Do you like solving complex real-world problems?", "options": ["Yes, a lot", "Sometimes", "Not really"]},
        {"id": 23, "text": "Are you interested in animation or game design?", "options": ["Very interested", "Somewhat", "Not at all"]},
        {"id": 24, "text": "Do you enjoy writing business plans or case studies?", "options": ["Yes, a lot", "Sometimes", "Not really"]},
        {"id": 25, "text": "Do you like creating YouTube videos or podcasts?", "options": ["Yes, a lot", "Sometimes", "Not really"]}
    ]
    
    if user_type == 'school':
        return school_questions
    else:
        return college_questions

# ==================== PERSONALITY PATHWAY ANALYSIS ====================
def analyze_personality_pathway(responses, user_type):
    """Analyze personality responses and return pathway recommendation"""
    # Calculate scores based on responses
    visual_score = 0
    auditory_score = 0
    kinesthetic_score = 0
    reading_score = 0
    
    # Sample mapping - you can customize this based on your questions
    for q_id, answer in responses.items():
        if answer in ["Yes, a lot", "Very interested", "Always"]:
            visual_score += 3
            kinesthetic_score += 2
        elif answer in ["Sometimes", "Somewhat"]:
            visual_score += 2
            auditory_score += 2
            reading_score += 2
        else:
            reading_score += 3
            auditory_score += 2
    
    scores = {
        "Visual Learner": visual_score,
        "Auditory Learner": auditory_score,
        "Kinesthetic Learner": kinesthetic_score,
        "Reading/Writing Learner": reading_score
    }
    
    dominant = max(scores, key=scores.get)
    percentage = int((scores[dominant] / sum(scores.values())) * 100)
    
    pathways = {
        "Visual Learner": {
            "icon": "👁️🎨",
            "title": "Visual Learner",
            "description": "You learn best through visual aids like diagrams, charts, videos, and written instructions. You remember information better when it's presented visually.",
            "strengths": ["Strong visual memory", "Good at spatial relationships", "Excellent at reading maps and diagrams", "Detail-oriented"],
            "careers": ["Graphic Designer", "Architect", "Photographer", "Video Editor", "UI/UX Designer", "Data Analyst"],
            "study_tips": ["Use color-coded notes", "Watch video tutorials", "Create mind maps and diagrams", "Use flashcards with images"],
            "work_environment": ["Creative studios", "Design agencies", "Tech companies", "Media production houses"]
        },
        "Auditory Learner": {
            "icon": "🎧🗣️",
            "title": "Auditory Learner",
            "description": "You learn best through listening - lectures, discussions, audio books, and verbal explanations. You remember information through sound and rhythm.",
            "strengths": ["Excellent listening skills", "Good at verbal instructions", "Strong memory for spoken information", "Great at public speaking"],
            "careers": ["Teacher/Trainer", "Journalist", "Musician", "Customer Service", "Sales Representative", "Podcaster"],
            "study_tips": ["Record lectures and listen again", "Read text aloud", "Join study groups for discussion", "Use mnemonic devices and rhymes"],
            "work_environment": ["Schools/Universities", "Media houses", "Call centers", "Training organizations"]
        },
        "Kinesthetic Learner": {
            "icon": "✋🏃",
            "title": "Kinesthetic Learner",
            "description": "You learn best through hands-on activities, movement, and physical experiences. You remember information by doing and practicing.",
            "strengths": ["Excellent hand-eye coordination", "Good at physical activities", "Strong problem-solving through action", "Practical and hands-on"],
            "careers": ["Surgeon", "Athlete", "Dancer", "Mechanical Engineer", "Physical Therapist", "Lab Technician"],
            "study_tips": ["Take frequent breaks while studying", "Use hands-on experiments", "Act out concepts", "Study while walking or moving"],
            "work_environment": ["Laboratories", "Hospitals", "Sports facilities", "Manufacturing plants", "Construction sites"]
        },
        "Reading/Writing Learner": {
            "icon": "📚✍️",
            "title": "Reading/Writing Learner",
            "description": "You learn best through reading and writing - books, articles, notes, and essays. You excel at expressing ideas through text.",
            "strengths": ["Strong reading comprehension", "Excellent writing skills", "Good at research", "Detail-oriented in documentation"],
            "careers": ["Author/Writer", "Editor", "Journalist", "Lawyer", "Researcher", "Librarian", "Content Creator"],
            "study_tips": ["Take detailed notes", "Rewrite information in your own words", "Read extensively", "Write summaries and essays"],
            "work_environment": ["Publishing houses", "Law firms", "Research institutions", "Libraries", "Corporate communications"]
        }
    }
    
    pathway = pathways.get(dominant, pathways["Visual Learner"])
    pathway["match_percentage"] = percentage
    pathway["personality_type"] = dominant
    
    return pathway

def calculate_results(responses, questions_list, categories):
    """Calculate weighted scores for each category"""
    # Reset scores
    for cat_id in categories:
        categories[cat_id]['score'] = 0
        categories[cat_id]['question_count'] = 0
    
    # Calculate weighted scores
    for q_id, score in responses.items():
        for q in questions_list:
            if q['id'] == q_id:
                cat_id = q['category_id']
                weight = q.get('weight', 1.0)
                weighted_score = int(score) * weight
                categories[cat_id]['score'] += weighted_score
                categories[cat_id]['question_count'] += 1
                break
    
    # Calculate percentages
    for cat_id in categories:
        cat = categories[cat_id]
        if cat['question_count'] > 0:
            # Each question max is 5, multiplied by weights
            # Calculate actual max possible based on weights
            total_weight = 0
            for q in questions_list:
                if q['category_id'] == cat_id:
                    total_weight += q.get('weight', 1.0)
            max_score = total_weight * 5
            
            if max_score > 0:
                cat['score'] = (cat['score'] / max_score) * 100
            else:
                cat['score'] = 0
        else:
            cat['score'] = 0
    
    # Sort categories by score and return top 3
    sorted_cats = sorted(categories.items(), key=lambda x: x[1]['score'], reverse=True)
    recommended = [cat[0] for cat in sorted_cats[:3]]
    
    return categories, recommended

def generate_pdf_report():
    """Generate PDF report for download with proper Unicode support"""
    
    from fpdf import FPDF
    import tempfile
    import os
    import re
    
    cat = st.session_state.categories_data.get(st.session_state.selected_stream, {})
    stream_details = get_stream_details(st.session_state.selected_stream, st.session_state.user_type)
    
    if not stream_details:
        stream_details = {
            'name': cat.get('name', 'Selected Stream'),
            'icon': '📚',
            'description': 'Excellent career opportunities',
            'careers': ['Career opportunities'],
            'subjects': ['Core subjects'],
            'skills': ['Key skills'],
            'future_scope': 'Good growth',
            'top_companies': ['Leading companies'],
            'education_path': 'Degree programs',
            'certifications': ['Certifications']
        }
    
    # Custom PDF class with Unicode support
    class PDF(FPDF):
        def header(self):
            # Add logo or header if needed
            pass
        
        def footer(self):
            self.set_y(-15)
            self.set_font('helvetica', 'I', 8)
            self.set_text_color(128, 128, 128)
            self.cell(0, 10, f'Page {self.page_no()}', 0, 0, 'C')
    
    # Create PDF
    pdf = PDF()
    pdf.add_page()
    
    # Try to add Unicode font, fallback to helvetica
    try:
        pdf.add_font('helvetica', '', 'helvetica.ttf', uni=True)
        pdf.set_font('helvetica', '', 12)
    except:
        pdf.set_font('helvetica', '', 12)
    
    # Helper function to clean text (remove emojis and special chars)
    def clean_text(text):
        # Remove emojis and special characters that cause issues
        emoji_pattern = re.compile("["
            u"\U0001F600-\U0001F64F"  # emoticons
            u"\U0001F300-\U0001F5FF"  # symbols & pictographs
            u"\U0001F680-\U0001F6FF"  # transport & map symbols
            u"\U0001F1E0-\U0001F1FF"  # flags (iOS)
            u"\U00002702-\U000027B0"
            u"\U000024C2-\U0001F251"
            u"\U0001F900-\U0001F9FF"  # supplemental symbols
            u"\U0001FA70-\U0001FAFF"  # more emojis
            "]+", flags=re.UNICODE)
        text = emoji_pattern.sub(r'', text)
        # Replace bullet points with asterisks
        text = text.replace('•', '-').replace('●', '-').replace('○', '-')
        # Remove other special characters
        text = text.encode('ascii', 'ignore').decode('ascii')
        return text.strip()
    
    # Helper function to add multi-cell text safely
    def safe_multi_cell(pdf, width, height, text, border=0, align='L'):
        clean = clean_text(text)
        pdf.multi_cell(width, height, clean, border, align)
    
    # Helper function to add cell text safely
    def safe_cell(pdf, width, height, text, border=0, ln=0, align='L'):
        clean = clean_text(text)
        pdf.cell(width, height, clean, border, ln, align)
    
    # Title
    pdf.set_font('helvetica', 'B', 20)
    pdf.set_text_color(211, 84, 0)  # Orange
    safe_cell(pdf, 0, 10, "CoActions Career Counselling Report", ln=True, align='C')
    pdf.ln(10)
    
    # Student Information
    pdf.set_font('helvetica', 'B', 14)
    pdf.set_text_color(46, 125, 50)  # Green
    pdf.cell(0, 8, "Student Information", ln=True)
    pdf.set_font('helvetica', '', 11)
    pdf.set_text_color(0, 0, 0)
    
    safe_cell(pdf, 0, 6, f"Name: {st.session_state.student_name}", ln=True)
    safe_cell(pdf, 0, 6, f"Age: {st.session_state.student_age}", ln=True)
    safe_cell(pdf, 0, 6, f"Institution: {st.session_state.student_institution}", ln=True)
    safe_cell(pdf, 0, 6, f"City: {st.session_state.student_city}", ln=True)
    safe_cell(pdf, 0, 6, f"State: {st.session_state.student_state}", ln=True)
    safe_cell(pdf, 0, 6, f"Grade/Year: {st.session_state.student_grade}", ln=True)
    safe_cell(pdf, 0, 6, f"Assessment Type: {'School Student' if st.session_state.user_type == 'school' else 'College Student'} Pathway", ln=True)
    safe_cell(pdf, 0, 6, f"Date: {datetime.now().strftime('%Y-%m-%d')}", ln=True)
    pdf.ln(5)
    
    # Selected Stream
    pdf.set_font('helvetica', 'B', 14)
    pdf.set_text_color(211, 84, 0)
    pdf.cell(0, 8, "Selected Stream", ln=True)
    pdf.set_font('helvetica', '', 11)
    pdf.set_text_color(0, 0, 0)
    safe_cell(pdf, 0, 6, f"Stream: {stream_details['name']}", ln=True)
    score_value = cat.get('score', 0)
    safe_cell(pdf, 0, 6, f"Match Score: {score_value:.1f}%", ln=True)
    pdf.ln(5)
    
    # About Stream
    pdf.set_font('helvetica', 'B', 14)
    pdf.set_text_color(46, 125, 50)
    pdf.cell(0, 8, "About this Stream", ln=True)
    pdf.set_font('helvetica', '', 11)
    pdf.set_text_color(0, 0, 0)
    description = stream_details['description']
    safe_multi_cell(pdf, 0, 6, description)
    pdf.ln(5)
    
    # Top Careers
    pdf.set_font('helvetica', 'B', 14)
    pdf.set_text_color(211, 84, 0)
    pdf.cell(0, 8, "Top Career Paths", ln=True)
    pdf.set_font('helvetica', '', 11)
    pdf.set_text_color(0, 0, 0)
    
    for career in stream_details.get('careers', [])[:10]:
        safe_cell(pdf, 0, 6, f"- {career}", ln=True)
    pdf.ln(5)
    
    # Key Subjects
    pdf.set_font('helvetica', 'B', 14)
    pdf.set_text_color(46, 125, 50)
    pdf.cell(0, 8, "Key Subjects to Focus", ln=True)
    pdf.set_font('helvetica', '', 11)
    pdf.set_text_color(0, 0, 0)
    
    for subject in stream_details.get('subjects', [])[:10]:
        safe_cell(pdf, 0, 6, f"- {subject}", ln=True)
    pdf.ln(5)
    
    # Skills
    pdf.set_font('helvetica', 'B', 14)
    pdf.set_text_color(211, 84, 0)
    pdf.cell(0, 8, "Skills to Develop", ln=True)
    pdf.set_font('helvetica', '', 11)
    pdf.set_text_color(0, 0, 0)
    
    for skill in stream_details.get('skills', [])[:10]:
        safe_cell(pdf, 0, 6, f"- {skill}", ln=True)
    pdf.ln(5)
    
    # Future Scope
    pdf.set_font('helvetica', 'B', 14)
    pdf.set_text_color(46, 125, 50)
    pdf.cell(0, 8, "Future Scope", ln=True)
    pdf.set_font('helvetica', '', 11)
    pdf.set_text_color(0, 0, 0)
    future_scope = stream_details.get('future_scope', 'Excellent growth opportunities')
    safe_multi_cell(pdf, 0, 6, future_scope)
    pdf.ln(5)
    
    # Top Companies (First 10)
    pdf.set_font('helvetica', 'B', 14)
    pdf.set_text_color(211, 84, 0)
    pdf.cell(0, 8, "Top Companies Hiring", ln=True)
    pdf.set_font('helvetica', '', 11)
    pdf.set_text_color(0, 0, 0)
    
    top_companies = stream_details.get('top_companies', [])
    for company in top_companies[:10]:
        safe_cell(pdf, 0, 6, f"- {company}", ln=True)
    pdf.ln(5)
    
    # Education Path
    pdf.set_font('helvetica', 'B', 14)
    pdf.set_text_color(46, 125, 50)
    pdf.cell(0, 8, "Recommended Education Path", ln=True)
    pdf.set_font('helvetica', '', 11)
    pdf.set_text_color(0, 0, 0)
    education_path = stream_details.get('education_path', 'Various educational pathways available')
    safe_multi_cell(pdf, 0, 6, education_path)
    pdf.ln(5)
    
    # Certifications
    pdf.set_font('helvetica', 'B', 14)
    pdf.set_text_color(211, 84, 0)
    pdf.cell(0, 8, "Valuable Certifications", ln=True)
    pdf.set_font('helvetica', '', 11)
    pdf.set_text_color(0, 0, 0)
    
    for cert in stream_details.get('certifications', [])[:10]:
        safe_cell(pdf, 0, 6, f"- {cert}", ln=True)
    
    # Save to temporary file
    temp_file = tempfile.NamedTemporaryFile(delete=False, suffix='.pdf')
    pdf.output(temp_file.name)
    temp_file.close()
    
    return temp_file.name

# ==================== COMPLETE STREAM DETAILS DATABASE ====================
# This covers ALL possible streams from both school and college JSON files

# ==================== COMPLETE STREAM DETAILS DATABASE ====================
# ALL categories with Indian companies and cities

STREAM_DETAILS_DB = {
    # ==================== 1. TECHNOLOGY & ENGINEERING ====================
    'tech_engineering': {
        'name': 'Technology & Engineering',
        'icon': '💻',
        'description': 'This dynamic stream focuses on technology, programming, and engineering principles. Students learn to design, develop, and maintain technological solutions that shape our digital world.',
        'careers': ['Software Engineer - Design and develop software applications', 'Data Scientist - Analyze complex data to drive business decisions', 'AI/ML Engineer - Create intelligent systems and algorithms', 'Cybersecurity Analyst - Protect systems from cyber threats', 'Cloud Architect - Design cloud infrastructure solutions', 'DevOps Engineer - Streamline development operations', 'Full Stack Developer - Build complete web applications', 'Database Administrator - Manage and optimize databases'],
        'subjects': ['Computer Science', 'Mathematics', 'Physics', 'Programming Fundamentals', 'Data Structures', 'Algorithms', 'Database Management'],
        'skills': ['Problem Solving', 'Logical Thinking', 'Programming Languages', 'Analytical Skills', 'Team Collaboration', 'Critical Thinking'],
        'software_skills': [
            '🖥️ Languages: Python, Java, JavaScript, C++, SQL',
            '🛠️ Frameworks: React, Angular, Spring Boot, Django, TensorFlow',
            '🔧 Tools: Git, Docker, Kubernetes, Jenkins, JIRA',
            '🗄️ Databases: MySQL, PostgreSQL, MongoDB, Oracle',
            '☁️ Cloud Platforms: AWS, Azure, Google Cloud',
            '📝 IDEs: VS Code, IntelliJ, PyCharm, Eclipse'
        ],
        'career_skills': [
            '🎯 Problem Solving & Critical Thinking',
            '🤝 Team Collaboration & Communication',
            '📊 Logical Reasoning & Analytical Skills',
            '⏰ Time Management & Attention to Detail',
            '📈 Project Management & Agile Methodologies',
            '🔄 Continuous Learning & Adaptability'
        ],
        'technical_skills': [
          'Programming Languages (Python, Java, C++, JavaScript)',
          'Data Structures & Algorithms',
          'Database Management (SQL, MongoDB)',
          'Cloud Computing (AWS, Azure, GCP)',
          'DevOps Tools (Docker, Kubernetes, Jenkins)',
          'Machine Learning & AI',
          'System Design & Architecture',
          'API Development & Integration',
          'Version Control (Git, GitHub)',
          'Testing & Debugging',
          'Cybersecurity Fundamentals',
          'Web Development (React, Angular, Node.js)'
        ],

        'future_scope': 'High demand in IT industry, AI, Machine Learning, Data Science, Software Development, Cloud Computing',
        'top_companies': [
            'Infosys - Bengaluru, Mysore, Pune, Bhubaneswar, Hyderabad, Chennai, Thiruvananthapuram',
            'Tata Consultancy Services (TCS) - Mumbai, Chennai, Bengaluru, Hyderabad, Kolkata, Pune, Delhi NCR, Lucknow, Indore',
            'Wipro - Bengaluru, Chennai, Hyderabad, Pune, Kolkata, Delhi NCR, Kochi, Bhubaneswar',
            'HCL Technologies - Noida, Chennai, Bengaluru, Hyderabad, Pune, Lucknow, Vijayawada',
            'Tech Mahindra - Pune, Bengaluru, Hyderabad, Noida, Chennai, Nagpur, Kolkata',
            'LTIMindtree - Bengaluru, Mumbai, Pune, Chennai, Hyderabad, Kolkata, Delhi NCR',
            'Mphasis - Bengaluru, Pune, Chennai, Indore, Hyderabad, Delhi NCR',
            'Hexaware Technologies - Mumbai, Chennai, Pune, Noida, Bengaluru, Dehradun',
            'Persistent Systems - Pune, Nagpur, Bengaluru, Hyderabad, Goa, Kolkata',
            'Mindtree - Bengaluru, Pune, Hyderabad, Chennai, Kolkata, Bhubaneswar, Mangalore'
        ],
        'education_path': 'B.Tech/BE in Computer Science, BCA, MCA, B.Sc in IT, Diploma in Engineering',
        'certifications': ['AWS Certified', 'Microsoft Certified', 'Python Certification', 'Java Certification', 'Cisco CCNA'],
        'hiring_cities': ['Bengaluru', 'Hyderabad', 'Pune', 'Chennai', 'Mumbai', 'Noida', 'Gurugram', 'Kolkata', 'Ahmedabad', 'Indore', 'Nagpur', 'Bhubaneswar', 'Kochi', 'Mysore', 'Thiruvananthapuram']
    },
    'tech_engineering_college': {
        'name': 'Technology & Engineering (Advanced)',
        'icon': '💻',
        'description': 'Advanced study in technology, programming, and engineering principles. Prepare for specialized roles in software development, AI, and system architecture.',
        'careers': ['Senior Software Engineer - Lead software development projects', 'Data Scientist - Advanced analytics and predictive modeling', 'AI/ML Engineer - Develop cutting-edge AI solutions', 'Cloud Solutions Architect - Enterprise cloud solutions', 'Technical Lead - Guide technical teams', 'Research Scientist - Innovate new technologies', 'IT Consultant - Advise on technology strategies'],
        'subjects': ['Advanced Programming', 'Data Structures & Algorithms', 'Cloud Computing', 'Artificial Intelligence', 'Machine Learning', 'Cybersecurity', 'Software Architecture'],
        'skills': ['Advanced Problem Solving', 'System Design', 'Project Management', 'Technical Leadership', 'Research Skills', 'Innovation'],
        'software_skills': [
            '🖥️ Advanced Languages: Python, Java, Scala, Go, Rust',
            '🛠️ Advanced Frameworks: TensorFlow, PyTorch, Kafka, Spark',
            '🔧 DevOps Tools: Kubernetes, Terraform, Ansible, Prometheus',
            '☁️ Cloud: AWS Solutions Architect, Azure, GCP',
            '🔬 ML/AI: LLMs, Computer Vision, NLP, Reinforcement Learning',
            '📊 Big Data: Hadoop, Spark, Kafka, Airflow'
        ],
        'career_skills': [
            '🎯 Strategic Problem Solving & System Design',
            '👥 Technical Leadership & Mentoring',
            '📈 Project Portfolio Management',
            '🔬 Research & Development Skills',
            '💡 Innovation & Creative Thinking',
            '🌐 Cross-functional Collaboration'
        ],
        'technical_skills': [
          'Programming Languages (Python, Java, C++, JavaScript)',
          'Data Structures & Algorithms',
          'Database Management (SQL, MongoDB)',
          'Cloud Computing (AWS, Azure, GCP)',
          'DevOps Tools (Docker, Kubernetes, Jenkins)',
          'Machine Learning & AI',
          'System Design & Architecture',
          'API Development & Integration',
          'Version Control (Git, GitHub)',
          'Testing & Debugging',
          'Cybersecurity Fundamentals',
          'Web Development (React, Angular, Node.js)'
        ],
        'future_scope': 'Leadership roles in tech industry, Research & Development, Specialized technical domains',
        'top_companies': [
            'Infosys Research Labs - Bengaluru, Mysore, Pune',
            'TCS Innovation Labs - Mumbai, Chennai, Bengaluru, Hyderabad, Kolkata',
            'Wipro Research - Bengaluru, Chennai, Hyderabad, Pune',
            'HCL Technologies - Noida, Chennai, Bengaluru, Lucknow',
            'Tech Mahindra - Pune, Bengaluru, Hyderabad, Noida',
            'LTIMindtree - Bengaluru, Mumbai, Pune, Chennai',
            'Microsoft India R&D - Hyderabad, Bengaluru, Noida',
            'Amazon India Development Center - Bengaluru, Hyderabad, Chennai, Delhi NCR, Pune',
            'Google India R&D - Bengaluru, Hyderabad, Gurugram',
            'Oracle India - Bengaluru, Hyderabad, Mumbai, Noida, Pune',
            'IBM India - Bengaluru, Pune, Hyderabad, Delhi NCR, Kolkata, Chennai',
            'SAP Labs India - Bengaluru, Pune, Mumbai, Gurugram'
        ],
        'education_path': 'M.Tech/MS in Computer Science, PhD programs, Executive MBA',
        'certifications': ['AWS Solutions Architect', 'Google Cloud Professional', 'CISSP', 'PMP'],
        'hiring_cities': ['Bengaluru', 'Hyderabad', 'Pune', 'Chennai', 'Mumbai', 'Noida', 'Gurugram', 'Kolkata', 'Thiruvananthapuram', 'Mysore']
    },

    # ==================== 2. BUSINESS & FINANCE ====================
    'business_finance': {
        'name': 'Business & Finance',
        'icon': '📊',
        'description': 'This strategic stream focuses on business management, finance, economics, and entrepreneurship. Students learn about markets, investments, and organizational management.',
        'careers': ['Business Analyst - Analyze and improve business processes', 'Investment Banker - Facilitate financial transactions', 'Marketing Manager - Develop marketing strategies', 'Entrepreneur - Start your own business', 'Financial Advisor - Guide investment decisions', 'Management Consultant - Solve business problems', 'Accountant - Manage financial records', 'Human Resources Manager - Handle employee relations'],
        'subjects': ['Economics', 'Accounting', 'Business Studies', 'Mathematics', 'Marketing', 'Finance', 'Organizational Behavior', 'Business Law'],
        'skills': ['Leadership', 'Analytical Thinking', 'Communication', 'Decision Making', 'Strategic Planning', 'Negotiation', 'Financial Literacy'],
        'software_skills': [
            '📊 Advanced Excel: Pivot Tables, VLOOKUP, Macros, Power Query',
            '💰 Financial Tools: Bloomberg Terminal, Reuters, Tally, QuickBooks',
            '📈 Data Visualization: Tableau, Power BI, Looker',
            '🏦 ERP Systems: SAP FICO, Oracle Financials, Microsoft Dynamics',
            '📉 CRM Software: Salesforce, Zoho, HubSpot',
            '📋 Accounting: Tally ERP 9, Zoho Books, QuickBooks'
        ],
        'career_skills': [
            '🎯 Strategic Leadership & Vision',
            '🤝 Negotiation & Persuasion',
            '📊 Financial Analysis & Risk Assessment',
            '💡 Decision Making & Problem Solving',
            '🗣️ Client Management & Relationship Building',
            '📈 Business Acumen & Market Awareness'
        ],
        'technical_skills': [
          'Financial Analysis & Modeling',
          'Investment Analysis (DCF, NPV, IRR)',
          'Financial Statement Analysis',
          'Risk Assessment & Management',
          'Business Strategy Development',
          'Market Research & Analysis',
          'Data Analysis (Excel, SQL, Tableau)',
          'Accounting Principles (GAAP, IFRS)',
          'Corporate Finance',
          'Portfolio Management',
          'Mergers & Acquisitions (M&A)',
          'Business Valuation Techniques'
        ],
        'future_scope': 'Corporate sector, Banking, Consulting, Entrepreneurship, Financial markets',
        'top_companies': [
            'HDFC Bank - Mumbai, Delhi, Bengaluru, Chennai, Kolkata, Pune, Hyderabad, Ahmedabad, Jaipur, Lucknow',
            'ICICI Bank - Mumbai, Delhi, Bengaluru, Hyderabad, Chennai, Kolkata, Pune, Ahmedabad, Jaipur',
            'Axis Bank - Mumbai, Delhi, Bengaluru, Pune, Kolkata, Chennai, Hyderabad, Chandigarh',
            'Kotak Mahindra Bank - Mumbai, Delhi, Bengaluru, Chennai, Hyderabad, Pune, Kolkata, Ahmedabad',
            'State Bank of India (SBI) - All major cities across India',
            'Goldman Sachs India - Bengaluru, Mumbai, Hyderabad',
            'JP Morgan India - Mumbai, Bengaluru, Hyderabad, Delhi NCR',
            'Morgan Stanley India - Mumbai, Bengaluru, Delhi NCR',
            'Deloitte India - Mumbai, Delhi, Bengaluru, Hyderabad, Chennai, Pune, Kolkata, Gurugram, Ahmedabad',
            'PwC India - Kolkata, Mumbai, Delhi, Bengaluru, Hyderabad, Chennai, Pune, Ahmedabad',
            'KPMG India - Mumbai, Delhi, Bengaluru, Hyderabad, Chennai, Pune, Gurugram, Noida',
            'EY India - Mumbai, Delhi, Bengaluru, Hyderabad, Chennai, Kolkata, Pune, Ahmedabad, Kochi',
            'McKinsey India - Mumbai, Delhi, Bengaluru, Chennai, Gurugram',
            'Boston Consulting Group (BCG) India - Mumbai, Delhi, Bengaluru, Kolkata, Chennai',
            'Bain & Company India - Mumbai, Delhi, Bengaluru, Gurugram'
        ],
        'education_path': 'BBA, B.Com, BMS, MBA, CA, CS, CMA, CFA',
        'certifications': ['CPA', 'CFA', 'CMA', 'FRM', 'Six Sigma', 'PMP'],
        'hiring_cities': ['Mumbai', 'Delhi NCR', 'Bengaluru', 'Hyderabad', 'Chennai', 'Pune', 'Kolkata', 'Ahmedabad', 'Jaipur', 'Lucknow', 'Chandigarh', 'Kochi', 'Indore', 'Nagpur']
    },
    'business_finance_college': {
        'name': 'Business & Finance (Advanced)',
        'icon': '📊',
        'description': 'Advanced study in business management, finance, and entrepreneurship. Prepare for leadership roles in corporate sector and investment banking.',
        'careers': ['Senior Business Analyst - Lead strategic initiatives', 'Investment Banker - Manage high-value transactions', 'Marketing Director - Oversee marketing operations', 'Entrepreneur - Scale business ventures', 'Financial Consultant - Advise corporate clients', 'Business Strategist - Develop growth strategies', 'Chief Financial Officer - Manage financial operations'],
        'subjects': ['Advanced Economics', 'Corporate Finance', 'Strategic Management', 'Marketing Analytics', 'Business Law', 'International Business'],
        'skills': ['Strategic Leadership', 'Financial Analysis', 'Risk Management', 'Negotiation', 'Executive Communication', 'Global Business Acumen'],
        'software_skills': [
            '📊 Advanced Financial Modeling: Excel VBA, Python for Finance',
            '💰 Investment Tools: Bloomberg Professional, FactSet, Capital IQ',
            '📈 Advanced BI: Tableau Server, Power BI Premium, QlikView',
            '🏦 Enterprise ERP: SAP S/4HANA, Oracle EBS, NetSuite',
            '📉 Risk Management Tools: RiskMetrics, MATLAB',
            '📋 Corporate Strategy Tools: IBM Cognos, Anaplan'
        ],
        'career_skills': [
            '🎯 Executive Leadership & Board Management',
            '🌍 Global Business Strategy & Expansion',
            '📊 Advanced Financial Engineering',
            '🤝 High-Stakes Negotiation & Deal Making',
            '📈 Corporate Governance & Compliance',
            '💡 Strategic Innovation & Change Management'
        ],
        'technical_skills': [
          'Financial Analysis & Modeling',
          'Investment Analysis (DCF, NPV, IRR)',
          'Financial Statement Analysis',
          'Risk Assessment & Management',
          'Business Strategy Development',
          'Market Research & Analysis',
          'Data Analysis (Excel, SQL, Tableau)',
          'Accounting Principles (GAAP, IFRS)',
          'Corporate Finance',
          'Portfolio Management',
          'Mergers & Acquisitions (M&A)',
          'Business Valuation Techniques'
        ],
        'future_scope': 'Executive leadership, Investment banking, Corporate strategy, Entrepreneurship',
        'top_companies': [
            'Goldman Sachs India - Bengaluru, Mumbai, Hyderabad',
            'JP Morgan India - Mumbai, Bengaluru, Hyderabad, Delhi NCR',
            'Morgan Stanley India - Mumbai, Bengaluru, Delhi NCR',
            'BlackRock India - Mumbai, Delhi, Bengaluru',
            'Avendus Capital - Mumbai, Bengaluru, Delhi',
            'Kotak Investment Banking - Mumbai, Delhi, Bengaluru, Chennai',
            'Axis Capital - Mumbai, Delhi, Bengaluru',
            'ICICI Securities - Mumbai, Delhi, Bengaluru, Chennai, Kolkata',
            'HDFC Securities - Mumbai, Delhi, Bengaluru, Chennai, Kolkata, Pune',
            'Motilal Oswal - Mumbai, Delhi, Bengaluru, Chennai, Pune, Kolkata',
            'IIFL Securities - Mumbai, Delhi, Bengaluru, Chennai, Hyderabad, Pune'
        ],
        'education_path': 'MBA from top B-schools (IIMs, ISB, XLRI, FMS, SPJIMR), Executive MBA, PhD in Management',
        'certifications': ['CFA Level 3', 'CPA', 'MBA', 'Six Sigma Black Belt', 'FRM'],
        'hiring_cities': ['Mumbai', 'Delhi NCR', 'Bengaluru', 'Hyderabad', 'Chennai', 'Pune', 'Kolkata', 'Ahmedabad', 'Gurugram']
    },

    # ==================== 3. HEALTH SCIENCES ====================
    'health_sciences': {
        'name': 'Health Sciences',
        'icon': '🏥',
        'description': 'This rewarding stream focuses on healthcare, medicine, and wellness. Students learn about the human body, diseases, treatments, and patient care.',
        'careers': ['Doctor (MBBS) - Diagnose and treat medical conditions', 'Nurse - Provide patient care and support', 'Pharmacist - Dispense medications', 'Physiotherapist - Help patients recover mobility', 'Public Health Specialist - Improve community health', 'Medical Researcher - Conduct clinical studies', 'Healthcare Administrator - Manage healthcare facilities', 'Clinical Psychologist - Treat mental health conditions'],
        'subjects': ['Biology', 'Chemistry', 'Anatomy', 'Physiology', 'Biochemistry', 'Pathology', 'Pharmacology', 'Microbiology'],
        'skills': ['Empathy', 'Attention to Detail', 'Communication', 'Problem Solving', 'Teamwork', 'Critical Thinking', 'Medical Ethics'],
        'software_skills': [
            '🏥 Electronic Health Records: Epic, Cerner, Meditech',
            '📊 Medical Imaging: DICOM, PACS, 3D Slicer',
            '📋 Hospital Management Systems: HMS, Medinous',
            '📈 Research Tools: SPSS, SAS, R for Medical Research',
            '💊 Pharmacy Management: McKesson, PioneerRx',
            '🩺 Telemedicine Platforms: Practo, Doxy.me'
        ],
        'career_skills': [
            '💝 Empathy & Compassion in Patient Care',
            '🔍 Attention to Detail & Diagnostic Accuracy',
            '🗣️ Communication & Patient Interaction',
            '🤝 Teamwork & Interdisciplinary Collaboration',
            '⚡ Stress Management & Emotional Resilience',
            '⚖️ Medical Ethics & Professionalism'
        ],
        'technical_skills': [
           'Medical Diagnosis & Treatment Planning',
           'Patient Assessment & Examination',
           'Clinical Procedures & Techniques',
           'Medical Terminology & Documentation',
           'Pharmacology & Drug Interactions',
           'Anatomy & Physiology Knowledge',
           'Emergency Response & Life Support (BLS, ACLS)',
           'Medical Equipment Operation',
           'Infection Control Practices',
           'Electronic Health Records (EHR)',
           'Laboratory Test Interpretation',
           'Rehabilitation Techniques'
        ],
        'future_scope': 'Healthcare sector, Research opportunities, Clinical practice, Public health',
        'top_companies': [
            'Apollo Hospitals - Chennai, Delhi, Hyderabad, Bengaluru, Mumbai, Kolkata, Ahmedabad, Pune, Lucknow, Bhubaneswar',
            'Fortis Healthcare - Delhi NCR, Bengaluru, Mumbai, Chennai, Kolkata, Jaipur, Mohali, Lucknow',
            'Max Healthcare - Delhi NCR, Punjab, Uttarakhand, Mumbai',
            'Narayana Health - Bengaluru, Kolkata, Mumbai, Delhi NCR, Ahmedabad, Raipur, Jaipur',
            'Manipal Hospitals - Bengaluru, Mangalore, Delhi, Pune, Jaipur, Vijayawada, Salem, Goa',
            'Medanta - Gurugram, Lucknow, Ranchi, Indore, Patna',
            'AIIMS - New Delhi, Bhopal, Bhubaneswar, Jodhpur, Patna, Raipur, Rishikesh, Nagpur, Bathinda',
            'Sun Pharmaceutical - Mumbai, Vadodara, Gurugram, Halol, Ahmedabad',
            'Dr. Reddy\'s Laboratories - Hyderabad, Bengaluru, Vishakhapatnam, Srikakulam',
            'Cipla - Mumbai, Bengaluru, Goa, Kurkumbh, Indore, Sikkim',
            'Lupin - Mumbai, Pune, Indore, Mandideep, Goa, Nagpur',
            'Aurobindo Pharma - Hyderabad, Vizag, Nellore, Srikakulam, Himachal Pradesh',
            'Biocon - Bengaluru, Mysore, Hyderabad',
            'Serum Institute of India - Pune'
        ],
        'education_path': 'MBBS, BDS, BAMS, BHMS, B.Sc Nursing, BPT, B.Pharma, MD/MS specialization',
        'certifications': ['ACLS', 'BLS', 'PALS', 'Specialty Board Certifications'],
        'hiring_cities': ['Delhi NCR', 'Mumbai', 'Bengaluru', 'Chennai', 'Hyderabad', 'Kolkata', 'Pune', 'Ahmedabad', 'Lucknow', 'Jaipur', 'Bhubaneswar', 'Chandigarh', 'Kochi', 'Nagpur', 'Indore']
    },
    'health_sciences_college': {
        'name': 'Health Sciences (Advanced)',
        'icon': '🏥',
        'description': 'Advanced studies in healthcare and medical sciences. Prepare for specialized medical careers and research positions.',
        'careers': ['Specialized Doctor - Expert in specific medical fields', 'Medical Researcher - Lead clinical trials', 'Healthcare Administrator - Manage hospital systems', 'Clinical Specialist - Advanced patient care', 'Public Health Director - Lead health initiatives', 'Pharmaceutical Researcher - Develop new medications', 'Medical Professor - Teach future healthcare professionals'],
        'subjects': ['Advanced Anatomy', 'Clinical Pathology', 'Advanced Pharmacology', 'Medical Ethics', 'Healthcare Management', 'Epidemiology'],
        'skills': ['Advanced Clinical Skills', 'Research Methodology', 'Leadership', 'Critical Thinking', 'Evidence-based Practice'],
        'software_skills': [
            '🏥 Advanced EHR: Epic Hyperspace, Cerner Millennium',
            '📊 Clinical Research: REDCap, Medidata Rave, Veeva Vault',
            '🔬 Lab Information Systems: STARLIMS, LabWare',
            '📈 Biostatistics: SAS, R, STATA for Clinical Trials',
            '🧬 Genomics Tools: BLAST, Galaxy, IGV',
            '🏥 Hospital Administration: SAP Healthcare, Meditech'
        ],
        'career_skills': [
            '🎯 Advanced Clinical Decision Making',
            '🔬 Research Leadership & Grant Writing',
            '👥 Healthcare Team Management',
            '📊 Evidence-Based Practice Implementation',
            '⚖️ Bioethics & Medical Law',
            '🌍 Global Health & Epidemiology'
        ],
        'technical_skills': [
           'Medical Diagnosis & Treatment Planning',
           'Patient Assessment & Examination',
           'Clinical Procedures & Techniques',
           'Medical Terminology & Documentation',
           'Pharmacology & Drug Interactions',
           'Anatomy & Physiology Knowledge',
           'Emergency Response & Life Support (BLS, ACLS)',
           'Medical Equipment Operation',
           'Infection Control Practices',
           'Electronic Health Records (EHR)',
           'Laboratory Test Interpretation',
           'Rehabilitation Techniques'
        ],
        'future_scope': 'Specialized medical practice, Research institutions, Healthcare policy',
        'top_companies': [
            'Apollo Hospitals Enterprises - Chennai, Hyderabad, Delhi, Bengaluru',
            'Fortis Healthcare - Gurugram, Bengaluru, Mumbai, Mohali',
            'Narayana Health - Bengaluru, Kolkata, Ahmedabad',
            'Manipal Health Enterprises - Bengaluru, Mangalore, Delhi',
            'Max Healthcare - Delhi NCR, Mohali',
            'AIIMS - New Delhi, Jodhpur, Bhopal, Bhubaneswar',
            'Biocon - Bengaluru, Mysore',
            'Serum Institute of India - Pune',
            'Indian Council of Medical Research (ICMR) - New Delhi, Hyderabad, Bengaluru, Chennai, Kolkata, Guwahati',
            'National Institute of Mental Health and Neurosciences (NIMHANS) - Bengaluru',
            'Post Graduate Institute of Medical Education and Research (PGIMER) - Chandigarh',
            'Christian Medical College (CMC) - Vellore, Ludhiana'
        ],
        'education_path': 'MD/MS specialization, DM/MCh super-specialization, PhD in Medical Sciences',
        'certifications': ['Specialty Board Certifications', 'Fellowship programs', 'Research Ethics Certification'],
        'hiring_cities': ['Delhi NCR', 'Mumbai', 'Bengaluru', 'Chennai', 'Hyderabad', 'Pune', 'Kolkata', 'Ahmedabad', 'Chandigarh', 'Vellore', 'Guwahati']
    },

    # ==================== 4. CREATIVE ARTS ====================
    'creative_arts': {
        'name': 'Creative Arts',
        'icon': '🎨',
        'description': 'This innovative stream focuses on design, visual arts, and creative expression. Students learn about design principles, user experience, and digital media.',
        'careers': ['Graphic Designer - Create visual concepts', 'UX/UI Designer - Design user experiences', 'Animator - Bring characters to life', 'Game Designer - Create interactive games', 'Art Director - Lead creative projects', 'Creative Strategist - Develop creative campaigns', 'Web Designer - Design engaging websites', 'Illustrator - Create original artwork'],
        'subjects': ['Design Fundamentals', 'Color Theory', 'Typography', 'Digital Media', 'Animation', 'UX Design', 'Photography', '3D Modeling'],
        'skills': ['Creativity', 'Visual Thinking', 'Communication', 'Design Software', 'Storytelling', 'Attention to Detail', 'Time Management'],
        'software_skills': [
            '🎨 Adobe Creative Suite: Photoshop, Illustrator, InDesign, After Effects, Premiere Pro',
            '🎭 UI/UX Tools: Figma, Sketch, Adobe XD, InVision',
            '🎬 3D Software: Blender, Maya, 3ds Max, Cinema 4D',
            '🎮 Animation Tools: Toon Boom, After Effects, Spine, Moho',
            '🎯 Game Engines: Unity, Unreal Engine, Godot',
            '📱 Prototyping: Balsamiq, Axure RP, Framer'
        ],
        'career_skills': [
            '🎨 Creativity & Visual Storytelling',
            '👁️ Attention to Detail & Aesthetic Sense',
            '🗣️ Client Communication & Feedback Integration',
            '⏰ Time Management & Deadline Adherence',
            '🤝 Team Collaboration & Creative Direction',
            '📈 Trend Awareness & Adaptability'
        ],
        'technical_skills': [
          'Adobe Creative Suite (Photoshop, Illustrator, InDesign)',
          'UI/UX Design (Figma, Sketch, Adobe XD)',
          'Animation (Maya, Blender, After Effects)',
          '3D Modeling & Rendering',
          'Typography & Color Theory',
          'Video Editing (Premiere Pro, Final Cut)',
          'Motion Graphics',
          'Digital Illustration',
          'Brand Identity Design',
          'Print Production Knowledge',
          'Web Design (HTML, CSS basics)',
          'Photography & Lighting'
        ],
        'future_scope': 'Design agencies, Gaming industry, Media, Entertainment, UX/UI design',
        'top_companies': [
            'DreamWorks India - Bengaluru',
            'Technicolor India - Bengaluru, Mumbai, Pune',
            'Dhruva Interactive - Bengaluru',
            'Junglee Games - Gurugram, Bengaluru',
            'Nazara Technologies - Mumbai',
            'Moonfrog Labs - Bengaluru',
            '99Games - Udupi, Bengaluru',
            'Lakshya Digital - Gurugram, Pune',
            'Zynga India - Bengaluru',
            'Ubisoft India - Pune, Mumbai',
            'Electronic Arts (EA) India - Hyderabad, Bengaluru',
            'Rockstar Games India - Bengaluru',
            'Games2win - Mumbai, Goa',
            'Octro Inc - Noida, Delhi NCR',
            'Creatiosoft - Pune, Mumbai',
            'Frameboxx Animation - Across India (Mumbai, Pune, Delhi, Bengaluru, Chennai, Kolkata)',
            'Arena Animation - Across all major Indian cities',
            'MAAC - Across all major Indian cities',
            'Toonz Animation - Thiruvananthapuram, Kochi'
        ],
        'education_path': 'B.Des, BFA, B.Sc in Animation, Diploma in Graphic Design, B.Sc in Game Design',
        'certifications': ['Adobe Certified Expert', 'UX Certification', 'Maya Certification', 'Blender Certification', 'Unity Certification', 'Unreal Engine Certification'],
        'hiring_cities': ['Bengaluru', 'Mumbai', 'Pune', 'Gurugram', 'Hyderabad', 'Chennai', 'Kolkata', 'Noida', 'Thiruvananthapuram', 'Kochi', 'Goa', 'Ahmedabad', 'Jaipur']
    },
    'creative_arts_college': {
        'name': 'Creative Arts (Advanced)',
        'icon': '🎨',
        'description': 'Advanced studies in design, creative arts, and digital media. Prepare for creative leadership roles.',
        'careers': ['Senior UX Designer - Lead user experience design', 'Creative Director - Oversee creative vision', 'Lead Animator - Manage animation teams', 'Game Designer - Design complex game systems', 'Art Director - Direct artistic productions', 'Creative Consultant - Advise on creative strategies', 'Design Manager - Lead design departments'],
        'subjects': ['Advanced Design Theory', 'User Experience Research', '3D Animation', 'Interactive Media', 'Portfolio Development', 'Creative Direction'],
        'skills': ['Creative Leadership', 'Design Strategy', 'User Research', 'Advanced Software Skills', 'Project Management', 'Team Leadership'],
        'software_skills': [
            '🎨 Advanced Adobe: Photoshop, Illustrator, InDesign, After Effects, Premiere Pro',
            '🎭 Advanced UI/UX: Figma Enterprise, Adobe XD, Sketch, Framer',
            '🎬 Advanced 3D: Maya, Houdini, ZBrush, Substance Painter',
            '🎮 Advanced Game Engines: Unreal Engine 5, Unity Pro',
            '🎯 Motion Graphics: Cinema 4D, Blender, After Effects',
            '📱 Design Systems: Storybook, Zeroheight, Supernova'
        ],
        'career_skills': [
            '🎯 Creative Direction & Vision Setting',
            '👥 Team Management & Mentorship',
            '📊 Design Strategy & Business Alignment',
            '🔬 User Research & Behavioral Analysis',
            '💡 Innovation & Trend Forecasting',
            '🗣️ Client Relationship & Stakeholder Management'
        ],
        'technical_skills': [
          'Adobe Creative Suite (Photoshop, Illustrator, InDesign)',
          'UI/UX Design (Figma, Sketch, Adobe XD)',
          'Animation (Maya, Blender, After Effects)',
          '3D Modeling & Rendering',
          'Typography & Color Theory',
          'Video Editing (Premiere Pro, Final Cut)',
          'Motion Graphics',
          'Digital Illustration',
          'Brand Identity Design',
          'Print Production Knowledge',
          'Web Design (HTML, CSS basics)',
          'Photography & Lighting'
        ],
        'future_scope': 'Creative leadership, Design agencies, Entertainment industry',
        'top_companies': [
            'Technicolor India - Bengaluru, Mumbai, Pune',
            'Dhruva Interactive - Bengaluru',
            'Lakshya Digital - Gurugram, Pune',
            'Nazara Technologies - Mumbai',
            'Moonfrog Labs - Bengaluru',
            'Ubisoft India - Pune, Mumbai',
            'Electronic Arts India - Hyderabad, Bengaluru',
            'Rockstar Games India - Bengaluru',
            'National Institute of Design (NID) - Ahmedabad, Bengaluru, Gandhinagar',
            'Industrial Design Centre (IDC) IIT Bombay - Mumbai',
            'National Institute of Fashion Technology (NIFT) - Across India (Delhi, Mumbai, Bengaluru, Kolkata, Chennai, Hyderabad, Gandhinagar, Patna)'
        ],
        'education_path': 'M.Des, MFA, MA in Design, Advanced diploma programs',
        'certifications': ['Certified UX Designer', 'Advanced Motion Graphics', 'Design Thinking Professional', 'Creative Direction Certification'],
        'hiring_cities': ['Bengaluru', 'Mumbai', 'Pune', 'Gurugram', 'Hyderabad', 'Chennai', 'Ahmedabad', 'Gandhinagar', 'Kolkata', 'Noida', 'Goa']
    },

    # ==================== 5. MANUFACTURING ====================
    'manufacturing': {
        'name': 'Manufacturing & Production',
        'icon': '🏭',
        'description': 'This stream focuses on manufacturing processes, production planning, quality control, and industrial engineering.',
        'careers': ['Production Manager - Oversee manufacturing operations', 'Quality Control Engineer - Ensure product quality', 'Manufacturing Engineer - Design and improve processes', 'Supply Chain Manager - Manage logistics', 'Industrial Engineer - Optimize production', 'Process Improvement Specialist - Implement lean manufacturing', 'Plant Manager - Lead factory operations', 'Operations Manager - Manage daily operations'],
        'subjects': ['Manufacturing Processes', 'Quality Management', 'Supply Chain Management', 'Industrial Engineering', 'Production Planning', 'Lean Manufacturing'],
        'skills': ['Process Optimization', 'Quality Control', 'Project Management', 'Problem Solving', 'Team Leadership', 'Data Analysis'],
        'software_skills': [
            '🏭 CAD Software: AutoCAD, SolidWorks, CATIA, Fusion 360',
            '⚙️ CAM Software: Mastercam, Edgecam, GibbsCAM',
            '📊 ERP Systems: SAP S/4HANA, Oracle Manufacturing, Infor',
            '📈 PLM Software: Teamcenter, Windchill, Arena PLM',
            '🔬 Simulation Tools: ANSYS, Simulink, FlexSim',
            '📋 Quality Tools: Minitab, QMS Software, Six Sigma Tools'
        ],
        'career_skills': [
            '🏭 Process Optimization & Lean Manufacturing',
            '📊 Quality Control & Six Sigma Methodologies',
            '👥 Team Leadership & Shift Management',
            '⚙️ Root Cause Analysis & Problem Solving',
            '🛡️ Safety Management & OSHA Compliance',
            '📈 Data-Driven Decision Making'
        ],
        'technical_skills': [
          'Lean Manufacturing & Six Sigma',
          'Production Planning & Scheduling',
          'Quality Control (SPC, FMEA, 8D)',
          'CAD/CAM Software (AutoCAD, SolidWorks)',
          'Industrial Automation (PLC, SCADA)',
          'Supply Chain Management',
          'Inventory Control Systems',
          'Process Optimization',
          'Root Cause Analysis',
          'ISO Standards Knowledge',
          'Safety Management (OSHA)',
          'Equipment Maintenance Planning'
        ],
        'future_scope': 'Manufacturing sector, Automotive industry, Pharmaceuticals, Consumer goods',
        'top_companies': [
            'Tata Motors - Mumbai, Pune, Jamshedpur, Lucknow, Sanand (Gujarat), Pantnagar, Dharwad',
            'Mahindra & Mahindra - Mumbai, Pune, Chennai, Nagpur, Zaheerabad, Haridwar, Kandivali, Chakan',
            'Maruti Suzuki - Gurugram, Manesar, Gujarat (Hansalpur), Rohtak',
            'Bajaj Auto - Pune, Aurangabad, Chakan, Akurdi, Pantnagar',
            'Hero MotoCorp - Delhi NCR, Gurugram, Manesar, Haridwar, Neemrana, Halol',
            'TVS Motor Company - Chennai, Hosur, Mysore, Nalagarh',
            'Ashok Leyland - Chennai, Hosur, Alwar, Bhandara',
            'Reliance Industries - Jamnagar, Vadodara, Mumbai, Hazira, Dahej, Nagothane, Patalganga, Silvassa',
            'Adani Group - Ahmedabad, Mundra, Mumbai, Raipur, Vizag',
            'Bosch India - Bengaluru, Nashik, Jaipur, Goa, Coimbatore, Bidadi',
            'Siemens India - Mumbai, Bengaluru, Goa, Aurangabad, Kalwa',
            'Cummins India - Pune, Phaltan, Mumbai, Jamshedpur, Kothrud',
            'Larsen & Toubro (L&T) - Mumbai, Chennai, Bengaluru, Hazira, Surat, Kanchipuram',
            'Godrej & Boyce - Mumbai, Pune, Chennai, Hyderabad, Mohali',
            'Escorts - Faridabad, Ballabgarh, Greater Noida, Madhya Pradesh'
        ],
        'education_path': 'B.Tech in Mechanical/Industrial Engineering, Diploma in Manufacturing, MBA in Operations',
        'certifications': ['Six Sigma', 'Lean Manufacturing', 'PMP', 'Quality Management', 'ISO Certification'],
        'hiring_cities': ['Pune', 'Chennai', 'Mumbai', 'Gurugram', 'Bengaluru', 'Ahmedabad', 'Jamshedpur', 'Lucknow', 'Nagpur', 'Hosur', 'Jamnagar', 'Vadodara', 'Faridabad', 'Coimbatore', 'Nashik', 'Chakan', 'Haridwar', 'Sanand', 'Goa']
    },
    'manufacturing_college': {
        'name': 'Manufacturing & Production (Advanced)',
        'icon': '🏭',
        'description': 'Advanced study in manufacturing systems, Industry 4.0, and smart manufacturing.',
        'careers': ['Senior Production Manager - Lead manufacturing teams', 'Operations Director - Oversee production strategy', 'Manufacturing Consultant - Advise on improvements', 'Plant Manager - Lead factory operations', 'Supply Chain Director - Manage global logistics', 'Industry 4.0 Specialist - Implement smart manufacturing'],
        'subjects': ['Advanced Manufacturing', 'Industry 4.0', 'Robotics', 'Automation', 'Operations Research', 'Smart Factory'],
        'skills': ['Strategic Planning', 'Operations Management', 'Data Analytics', 'Leadership', 'Process Excellence', 'Digital Transformation'],
        'software_skills': [
            '🏭 Advanced CAD/CAM: CATIA V6, NX, Creo',
            '🤖 Robotics Software: ROS, RobotStudio, KUKA Sim',
            '📊 Advanced ERP: SAP Manufacturing, Oracle Cloud SCM',
            '🔬 Digital Twin: Siemens NX, ANSYS Twin Builder',
            '📈 MES Software: Apriso, Siemens MES, Rockwell Automation',
            '🔧 Industry 4.0 Tools: IoT Platforms, SCADA, PLC Programming'
        ],
        'career_skills': [
            '🎯 Strategic Manufacturing Planning',
            '🤖 Automation & Robotics Integration',
            '📊 Digital Transformation Leadership',
            '🌍 Global Supply Chain Management',
            '💡 Industry 4.0 Implementation',
            '👥 Cross-functional Team Leadership'
        ],
        'technical_skills': [
          'Lean Manufacturing & Six Sigma',
          'Production Planning & Scheduling',
          'Quality Control (SPC, FMEA, 8D)',
          'CAD/CAM Software (AutoCAD, SolidWorks)',
          'Industrial Automation (PLC, SCADA)',
          'Supply Chain Management',
          'Inventory Control Systems',
          'Process Optimization',
          'Root Cause Analysis',
          'ISO Standards Knowledge',
          'Safety Management (OSHA)',
          'Equipment Maintenance Planning'
        ],
        'future_scope': 'Smart manufacturing, Industry 4.0, Automation, Production optimization',
        'top_companies': [
            'Tata Motors - Pune, Jamshedpur, Sanand, Lucknow',
            'Mahindra & Mahindra - Mumbai, Chennai, Nagpur, Pune',
            'Maruti Suzuki - Gurugram, Manesar, Gujarat',
            'Reliance Industries - Jamnagar, Vadodara, Dahej, Hazira',
            'Adani Group - Ahmedabad, Mundra, Raipur',
            'Siemens India - Mumbai, Bengaluru, Goa, Aurangabad',
            'Bosch India - Bengaluru, Nashik, Jaipur, Goa',
            'Cummins India - Pune, Phaltan, Mumbai',
            'Larsen & Toubro - Mumbai, Chennai, Bengaluru, Hazira',
            'Indian Institute of Technology (IIT) Manufacturing Labs - Across IITs (Mumbai, Delhi, Chennai, Kanpur, Kharagpur, Roorkee)',
            'National Institute of Industrial Engineering (NITIE) - Mumbai'
        ],
        'education_path': 'M.Tech in Manufacturing, MBA in Operations Management, PhD in Industrial Engineering',
        'certifications': ['Six Sigma Black Belt', 'Lean Master', 'Supply Chain Certification', 'PMP', 'Industry 4.0 Certification'],
        'hiring_cities': ['Pune', 'Chennai', 'Mumbai', 'Ahmedabad', 'Gurugram', 'Bengaluru', 'Jamshedpur', 'Vadodara', 'Jamnagar', 'Nagpur', 'Sanand', 'Faridabad', 'Goa', 'Aurangabad']
    },

    # ==================== 6. CONSTRUCTION ====================
    'construction': {
        'name': 'Construction & Civil Engineering',
        'icon': '🏗️',
        'description': 'This stream focuses on construction management, civil engineering, project planning, and infrastructure development.',
        'careers': ['Civil Engineer - Design construction projects', 'Construction Manager - Manage construction sites', 'Project Manager - Lead project planning', 'Site Engineer - Supervise daily operations', 'Structural Engineer - Design building structures', 'Quantity Surveyor - Manage costs', 'Architect - Design buildings', 'Urban Planner - Plan city development'],
        'subjects': ['Construction Management', 'Structural Engineering', 'Project Planning', 'Building Materials', 'Surveying', 'Geotechnical Engineering'],
        'skills': ['Project Management', 'Blueprint Reading', 'Cost Estimation', 'Team Coordination', 'Safety Management', 'Problem Solving'],
        'software_skills': [
            '🏗️ CAD Software: AutoCAD, Revit, SketchUp, ArchiCAD',
            '📐 Structural Analysis: STAAD Pro, ETABS, SAP2000',
            '📊 Project Management: Primavera P6, MS Project, Jira',
            '🏢 BIM Software: Navisworks, BIM 360, Tekla',
            '💰 Estimation Tools: Quantity Takeoff, CostX, Bluebeam',
            '🗺️ GIS Software: ArcGIS, QGIS for site planning'
        ],
        'career_skills': [
            '🏗️ Project Management & Scheduling',
            '📐 Blueprint Reading & Technical Drawing',
            '💰 Cost Estimation & Budgeting',
            '👥 Team Coordination & Leadership',
            '🛡️ Safety Management & Risk Assessment',
            '🗣️ Client Communication & Stakeholder Management'
        ],
        'technical_skills': [
          'Building Information Modeling (BIM)',
          'AutoCAD & Revit',
          'STAAD Pro & Structural Analysis',
          'Project Planning (Primavera P6, MS Project)',
          'Quantity Surveying & Cost Estimation',
          'Construction Materials Knowledge',
          'Site Surveying & Leveling',
          'Safety Compliance (OSHA, IS Codes)',
          'Contract Management',
          'Quality Control in Construction',
          'Geotechnical Engineering',
          'Sustainable Construction Practices'
        ],
        'future_scope': 'Construction industry, Infrastructure projects, Real estate development',
        'top_companies': [
            'Larsen & Toubro (L&T) - Mumbai, Chennai, Bengaluru, Delhi, Hyderabad, Kolkata, Pune, Vadodara, Ahmedabad, Lucknow',
            'Shapoorji Pallonji Group - Mumbai, Pune, Chennai, Bengaluru, Hyderabad, Kolkata, Delhi NCR, Ahmedabad',
            'Tata Projects - Mumbai, Hyderabad, Delhi NCR, Chennai, Bengaluru, Kolkata',
            'Gammon India - Mumbai, Delhi NCR, Bengaluru, Chennai, Kolkata, Hyderabad',
            'NCC Limited - Hyderabad, Chennai, Bengaluru, Mumbai, Delhi NCR, Kolkata, Vizag',
            'Prestige Group - Bengaluru, Chennai, Hyderabad, Kochi, Mumbai, Delhi NCR',
            'Godrej Properties - Mumbai, Bengaluru, Pune, Delhi NCR, Chennai, Ahmedabad, Kolkata',
            'DLF Limited - Gurugram, Delhi NCR, Chennai, Bengaluru, Kolkata, Chandigarh',
            'Sobha Limited - Bengaluru, Chennai, Coimbatore, Gurugram, Pune, Mysore, Kozhikode',
            'Brigade Group - Bengaluru, Chennai, Hyderabad, Kochi, Mysore, Ahmedabad',
            'Oberoi Realty - Mumbai, Pune, Thane',
            'Puravankara Limited - Bengaluru, Chennai, Hyderabad, Coimbatore, Mumbai, Pune, Kochi',
            'Mahindra Lifespaces - Mumbai, Pune, Delhi NCR, Chennai, Bengaluru, Hyderabad',
            'National Buildings Construction Corporation (NBCC) - Delhi NCR, Across India',
            'Rail Vikas Nigam Limited (RVNL) - Across India, Major Railway Hubs'
        ],
        'education_path': 'B.Tech in Civil Engineering, Diploma in Construction Management, B.Arch',
        'certifications': ['PMP', 'LEED Certification', 'Construction Safety', 'AutoCAD', 'Primavera', 'Revit', 'STAAD Pro'],
        'hiring_cities': ['Mumbai', 'Delhi NCR', 'Bengaluru', 'Chennai', 'Hyderabad', 'Pune', 'Kolkata', 'Ahmedabad', 'Lucknow', 'Jaipur', 'Kochi', 'Coimbatore', 'Chandigarh', 'Vizag', 'Indore', 'Nagpur']
    },
    'construction_college': {
        'name': 'Construction & Civil Engineering (Advanced)',
        'icon': '🏗️',
        'description': 'Advanced study in construction management and sustainable infrastructure.',
        'careers': ['Senior Project Manager - Lead major projects', 'Construction Director - Oversee construction strategy', 'Structural Consultant - Advise on structures', 'Infrastructure Planner - Plan large-scale projects', 'Real Estate Developer - Develop properties', 'Sustainability Consultant - Green building expert'],
        'subjects': ['Advanced Construction Methods', 'Sustainable Design', 'Project Finance', 'Risk Management', 'Urban Planning', 'Green Building'],
        'skills': ['Strategic Planning', 'Budget Management', 'Team Leadership', 'Risk Assessment', 'Contract Negotiation', 'Sustainable Design'],
        'software_skills': [
            '🏗️ Advanced BIM: Revit Architecture, Navisworks Manage',
            '📐 Advanced Structural: Tekla Structures, RAM Structural',
            '📊 Advanced Project Management: Primavera P6 EPPM, Oracle Aconex',
            '🏢 Digital Twin: Autodesk Tandem, Bentley iTwin',
            '💰 Advanced Cost Management: CostX, Vico Office',
            '🌍 GIS Advanced: ArcGIS Pro, CityEngine'
        ],
        'career_skills': [
            '🎯 Strategic Infrastructure Planning',
            '📊 Megaproject Management & Risk Mitigation',
            '🌱 Sustainable Design & LEED Certification',
            '🤝 Contract Negotiation & Legal Compliance',
            '👥 Executive Leadership & Board Reporting',
            '💡 Innovation in Construction Technology'
        ],
        'technical_skills': [
          'Building Information Modeling (BIM)',
          'AutoCAD & Revit',
          'STAAD Pro & Structural Analysis',
          'Project Planning (Primavera P6, MS Project)',
          'Quantity Surveying & Cost Estimation',
          'Construction Materials Knowledge',
          'Site Surveying & Leveling',
          'Safety Compliance (OSHA, IS Codes)',
          'Contract Management',
          'Quality Control in Construction',
          'Geotechnical Engineering',
          'Sustainable Construction Practices'
        ],
        'future_scope': 'Large-scale infrastructure, Smart cities, Sustainable construction',
        'top_companies': [
            'Larsen & Toubro (L&T) - Mumbai, Chennai, Bengaluru, Delhi, Hyderabad',
            'Shapoorji Pallonji - Mumbai, Pune, Chennai',
            'Tata Projects - Mumbai, Hyderabad, Delhi NCR',
            'NCC Limited - Hyderabad, Chennai, Bengaluru',
            'DLF Limited - Gurugram, Delhi NCR',
            'Godrej Properties - Mumbai, Bengaluru, Pune',
            'National Highways Authority of India (NHAI) - Delhi NCR, All State Capitals',
            'Delhi Metro Rail Corporation (DMRC) - Delhi NCR',
            'Mumbai Metro Rail Corporation - Mumbai',
            'Bengaluru Metro Rail Corporation (BMRCL) - Bengaluru',
            'Chennai Metro Rail Limited - Chennai',
            'Hyderabad Metro Rail - Hyderabad',
            'Kolkata Metro Rail Corporation - Kolkata'
        ],
        'education_path': 'M.Tech in Civil Engineering, MBA in Construction Management, PhD in Structural Engineering',
        'certifications': ['PMP', 'LEED AP', 'Construction Management Certification', 'Primavera P6', 'Advanced Revit'],
        'hiring_cities': ['Mumbai', 'Delhi NCR', 'Bengaluru', 'Chennai', 'Hyderabad', 'Pune', 'Ahmedabad', 'Kolkata', 'Lucknow', 'Jaipur']
    },

    # ==================== 7. AGRICULTURE ====================
    'agriculture': {
        'name': 'Agriculture & Food Technology',
        'icon': '🌾',
        'description': 'This stream focuses on modern agriculture, food processing, agribusiness, and sustainable farming practices.',
        'careers': ['Agricultural Engineer - Design farming equipment', 'Food Technologist - Develop food products', 'Agribusiness Manager - Manage agricultural businesses', 'Farm Manager - Oversee farm operations', 'Research Scientist - Conduct agricultural research', 'Quality Control Manager - Ensure food safety', 'Soil Scientist - Study soil management', 'Plant Breeder - Develop new crop varieties'],
        'subjects': ['Agronomy', 'Soil Science', 'Food Processing', 'Agricultural Economics', 'Plant Pathology', 'Entomology', 'Horticulture'],
        'skills': ['Research Skills', 'Data Analysis', 'Problem Solving', 'Project Management', 'Sustainability Knowledge', 'Communication'],
        'software_skills': [
            '🌾 GIS Software: ArcGIS, QGIS for precision farming',
            '🚜 Farm Management: AgriWebb, FarmLogs, Climate FieldView',
            '📊 Data Analysis: R, Python, SPSS for agricultural research',
            '🔬 Lab Software: LIMS, GenStat, SAS for crop science',
            '📈 ERP: SAP Agriculture, Oracle Agribusiness',
            '💧 Irrigation Management: RainBird, Netafim, CropX'
        ],
        'career_skills': [
            '🌾 Research & Data Analysis Skills',
            '🔬 Laboratory Techniques & Field Sampling',
            '📊 Project Management & Planning',
            '🌱 Sustainability Knowledge & Implementation',
            '🗣️ Communication & Stakeholder Management',
            '💡 Problem Solving & Critical Thinking'
        ],
        'technical_skills': [
          'Crop Management & Agronomy',
          'Soil Science & Testing',
          'Irrigation Systems Design',
          'Pest & Disease Management',
          'Precision Agriculture Technologies',
          'Farm Machinery Operation',
          'Post-Harvest Technology',
          'Food Processing Techniques',
          'Agricultural Economics',
          'Sustainable Farming Practices',
          'Greenhouse Management',
          'Organic Farming Methods'
        ],
        'future_scope': 'Agritech industry, Food processing, Agricultural research, Government departments',
        'top_companies': [
            'ITC Limited - Kolkata, Bengaluru, Gurugram, Chennai, Hyderabad, Pune, Lucknow, Vijayawada, Guntur',
            'Nestlé India - Gurugram, Moga (Punjab), Nanjangud (Karnataka), Samalkha (Haryana), Ponda (Goa), Bicholim (Goa), Tahliwal (HP)',
            'Britannia Industries - Bengaluru, Kolkata, Delhi NCR, Mumbai, Chennai, Pune, Guwahati, Rudrapur',
            'PepsiCo India - Gurugram, Mumbai, Bengaluru, Pune, Kolkata, Chennai, Hyderabad, Channo (Punjab)',
            'Cargill India - Gurugram, Bengaluru, Mumbai, Delhi, Kolkata, Hyderabad, Pune',
            'Godrej Agrovet - Mumbai, Hyderabad, Bengaluru, Kolkata, Chennai, Guwahati, Patna, Lucknow',
            'UPL Limited - Mumbai, Hyderabad, Ankleshwar, Bharuch, Gujarat',
            'Rallis India - Mumbai, Bengaluru, Hyderabad, Pune, Davangere, Akola',
            'National Dairy Development Board (NDDB) - Anand (Gujarat)',
            'Indian Council of Agricultural Research (ICAR) - New Delhi, Across Agricultural Research Stations',
            'Mother Dairy - Delhi NCR, Mumbai, Bengaluru, Hyderabad, Kolkata',
            'Amul (GCMMF) - Anand (Gujarat), Across India',
            'Parle Agro - Mumbai, Bengaluru, Hyderabad, Kolkata, Lucknow, Bahadurgarh',
            'Dabur India - New Delhi, Ghaziabad, Bengaluru, Siliguri, Baddi, Jammu'
        ],
        'education_path': 'B.Sc Agriculture, B.Tech Food Technology, B.Sc Horticulture, MBA Agribusiness',
        'certifications': ['Certified Crop Advisor', 'Food Safety Certification', 'Organic Farming', 'Agricultural Management', 'ISO 22000'],
        'hiring_cities': ['Mumbai', 'Bengaluru', 'Gurugram', 'Pune', 'Chennai', 'Hyderabad', 'Kolkata', 'Ahmedabad', 'Lucknow', 'Anand', 'Punjab Region', 'Nagpur', 'Patna', 'Guwahati', 'Jaipur', 'Coimbatore', 'Ludhiana']
    },
    'agriculture_college': {
        'name': 'Agriculture & Food Technology (Advanced)',
        'icon': '🌾',
        'description': 'Advanced study in agricultural science and food technology.',
        'careers': ['Agricultural Research Scientist - Lead research projects', 'Food Processing Director - Manage food production', 'Agritech Consultant - Advise on technology', 'Sustainability Manager - Lead sustainability initiatives', 'Agricultural Policy Advisor - Shape agricultural policy', 'Biotechnology Specialist - Develop GM crops'],
        'subjects': ['Advanced Agronomy', 'Biotechnology', 'Food Engineering', 'Agribusiness Management', 'Precision Agriculture', 'Climate Smart Agriculture'],
        'skills': ['Research Methodology', 'Data Analytics', 'Strategic Planning', 'Policy Analysis', 'Innovation Management', 'Sustainable Practices'],
        'software_skills': [
            '🌾 Precision Agriculture: Climate FieldView, John Deere Operations Center',
            '🧬 Advanced Biotech: Geneious, Benchling, SnapGene',
            '📊 Advanced Analytics: R Studio, Python, SAS, Tableau',
            '🔬 Lab Management: STARLIMS, LabWare, Benchling',
            '🚜 Drone Software: DroneDeploy, Pix4Dfields',
            '📈 ERP Advanced: SAP Agriculture Cloud, Oracle Agribusiness Suite'
        ],
        'career_skills': [
            '🎯 Agricultural Research Leadership',
            '🔬 Biotechnology & Genetic Engineering',
            '📊 Agribusiness Strategy & Policy',
            '🌍 Sustainability & Climate Resilience',
            '💡 Innovation & Technology Adoption',
            '🗣️ Stakeholder Engagement & Policy Advocacy'
        ],
        'technical_skills': [
          'Crop Management & Agronomy',
          'Soil Science & Testing',
          'Irrigation Systems Design',
          'Pest & Disease Management',
          'Precision Agriculture Technologies',
          'Farm Machinery Operation',
          'Post-Harvest Technology',
          'Food Processing Techniques',
          'Agricultural Economics',
          'Sustainable Farming Practices',
          'Greenhouse Management',
          'Organic Farming Methods'
        ],
        'future_scope': 'Agritech startups, Research institutions, Food corporations, Government policy',
        'top_companies': [
            'ITC Limited - Kolkata, Bengaluru, Gurugram',
            'Nestlé India - Gurugram, Moga',
            'Godrej Agrovet - Mumbai, Hyderabad',
            'UPL Limited - Mumbai, Hyderabad',
            'ICAR Research Institutes - New Delhi, Across India (50+ institutes)',
            'Indian Agricultural Research Institute (IARI) - New Delhi',
            'Punjab Agricultural University (PAU) - Ludhiana',
            'Tamil Nadu Agricultural University (TNAU) - Coimbatore',
            'National Dairy Research Institute (NDRI) - Karnal, Bengaluru',
            'Central Food Technological Research Institute (CFTRI) - Mysore'
        ],
        'education_path': 'M.Sc Agriculture, M.Tech Food Technology, PhD in Agricultural Sciences, MBA Agribusiness',
        'certifications': ['Certified Professional Agronomist', 'Food Safety Lead Auditor', 'Precision Agriculture Certification', 'Organic Certification'],
        'hiring_cities': ['Mumbai', 'Bengaluru', 'Gurugram', 'Pune', 'Hyderabad', 'Kolkata', 'Anand', 'Ludhiana', 'Coimbatore', 'Karnal', 'Mysore', 'New Delhi', 'Nagpur', 'Ranchi']
    },

    # ==================== 8. MATHEMATICS ====================
    'mathematics': {
        'name': 'Mathematics & Statistics',
        'icon': '📐',
        'description': 'This analytical stream focuses on mathematical theories, statistical analysis, and data interpretation. Students develop strong problem-solving skills.',
        'careers': ['Data Scientist - Extract insights from data', 'Actuary - Analyze financial risks', 'Statistician - Design and analyze surveys', 'Quantitative Analyst - Develop financial models', 'Mathematics Professor - Teach and research', 'Operations Research Analyst - Optimize processes', 'Financial Analyst - Analyze investments', 'Cryptographer - Develop security algorithms'],
        'subjects': ['Calculus', 'Linear Algebra', 'Statistics', 'Probability', 'Discrete Mathematics', 'Numerical Analysis', 'Differential Equations'],
        'skills': ['Analytical Thinking', 'Problem Solving', 'Logical Reasoning', 'Data Analysis', 'Mathematical Modeling', 'Critical Thinking'],
        'software_skills': [
            '📊 Statistical Software: R, SPSS, Stata, SAS, JMP',
            '🐍 Programming: Python (NumPy, Pandas, SciPy), MATLAB, Julia',
            '📈 Data Visualization: Tableau, Power BI, ggplot2, Plotly',
            '📐 Mathematical Tools: Mathematica, Maple, Wolfram Alpha',
            '🗄️ Database: SQL, PostgreSQL, MongoDB',
            '🤖 Machine Learning: scikit-learn, TensorFlow, PyTorch'
        ],
        'career_skills': [
            '📐 Analytical Thinking & Pattern Recognition',
            '🧮 Mathematical Modeling & Optimization',
            '📊 Data Interpretation & Statistical Inference',
            '🎯 Problem Solving & Logical Reasoning',
            '🔍 Attention to Detail & Accuracy',
            '🗣️ Communication of Complex Concepts'
        ],
        'technical_skills': [
          'Advanced Calculus & Linear Algebra',
          'Statistical Analysis (SPSS, R, SAS)',
          'Probability Theory',
          'Mathematical Modeling',
          'Data Analysis & Visualization',
          'Actuarial Mathematics',
          'Numerical Methods',
          'Operations Research',
          'Cryptography & Number Theory',
          'Machine Learning Algorithms',
          'Financial Mathematics',
          'Optimization Techniques'
        ],
        'future_scope': 'Finance, Insurance, Tech industry, Research, Education',
        'top_companies': [
            'Mu Sigma - Bengaluru, Delhi NCR, Pune',
            'Fractal Analytics - Mumbai, Bengaluru, Delhi NCR, Chennai',
            'Tiger Analytics - Chennai, Bengaluru, Hyderabad, Pune',
            'Bridgenext - Pune, Bengaluru, Hyderabad',
            'Absolutdata - Gurugram, Bengaluru, Kolkata',
            'ICICI Prudential - Mumbai, Delhi, Bengaluru, Chennai, Kolkata, Pune',
            'HDFC Life - Mumbai, Delhi, Bengaluru, Chennai, Kolkata, Hyderabad',
            'Max Life Insurance - Delhi NCR, Mumbai, Bengaluru, Chennai, Kolkata, Pune',
            'SBI Life - Mumbai, Across India',
            'Indian Statistical Institute (ISI) - Kolkata, Delhi, Bengaluru, Chennai, Hyderabad, Tezpur',
            'Indian Institute of Science (IISc) - Bengaluru',
            'Tata Institute of Fundamental Research (TIFR) - Mumbai, Bengaluru, Hyderabad',
            'ISRO - Bengaluru, Ahmedabad, Thiruvananthapuram, Sriharikota',
            'DRDO - Delhi, Hyderabad, Bengaluru, Pune, Chandigarh, Tezpur',
            'Indian Institute of Technology (IIT) Mathematics Departments - Across IITs'
        ],
        'education_path': 'B.Sc Mathematics, B.Sc Statistics, M.Sc Mathematics, M.Sc Statistics, PhD',
        'certifications': ['Actuarial Science Certification', 'Data Science Certification', 'SAS Certification', 'R Programming Certification'],
        'hiring_cities': ['Bengaluru', 'Mumbai', 'Delhi NCR', 'Hyderabad', 'Chennai', 'Pune', 'Kolkata', 'Gurugram', 'Kochi', 'Ahmedabad', 'Chandigarh']
    },
    'mathematics_college': {
        'name': 'Mathematics & Statistics (Advanced)',
        'icon': '📐',
        'description': 'Advanced study in mathematical sciences and statistical modeling.',
        'careers': ['Senior Data Scientist - Lead data projects', 'Quantitative Researcher - Develop trading models', 'Actuarial Manager - Lead actuarial teams', 'Professor - Teach advanced mathematics', 'Research Mathematician - Conduct research', 'Financial Engineer - Create financial products'],
        'subjects': ['Advanced Calculus', 'Real Analysis', 'Complex Analysis', 'Advanced Statistics', 'Machine Learning', 'Optimization Theory'],
        'skills': ['Advanced Mathematical Modeling', 'Statistical Computing', 'Research Methodology', 'Algorithm Design', 'Machine Learning'],
        'software_skills': [
            '📊 Advanced Stats: JAGS, Stan, INLA',
            '🐍 Advanced Python: Dask, Numba, Cython',
            '🧮 Machine Learning: XGBoost, LightGBM, CatBoost',
            '📈 Big Data: Spark, Hadoop, Dask',
            '🔬 Research Tools: LaTeX, Overleaf, MathJax',
            '🤖 Deep Learning: Keras, PyTorch Lightning, JAX'
        ],
        'career_skills': [
            '🎯 Advanced Mathematical Research',
            '🔬 Statistical Consulting & Methodology',
            '📊 Big Data Analytics & Machine Learning',
            '💡 Algorithm Design & Optimization',
            '📚 Academic Writing & Publishing',
            '👥 Team Leadership in Research'
        ],
        'technical_skills': [
          'Advanced Calculus & Linear Algebra',
          'Statistical Analysis (SPSS, R, SAS)',
          'Probability Theory',
          'Mathematical Modeling',
          'Data Analysis & Visualization',
          'Actuarial Mathematics',
          'Numerical Methods',
          'Operations Research',
          'Cryptography & Number Theory',
          'Machine Learning Algorithms',
          'Financial Mathematics',
          'Optimization Techniques'
        ],
        'future_scope': 'Research institutions, Investment banks, Tech companies, Academia',
        'top_companies': [
            'Mu Sigma - Bengaluru',
            'Fractal Analytics - Mumbai, Bengaluru',
            'Tiger Analytics - Chennai, Bengaluru',
            'Indian Statistical Institute (ISI) - Kolkata, Delhi, Bengaluru, Chennai',
            'IITs - Across India (Mumbai, Delhi, Chennai, Kanpur, Kharagpur, Roorkee, Guwahati)',
            'ISRO - Bengaluru, Ahmedabad, Thiruvananthapuram',
            'DRDO - Delhi, Hyderabad, Bengaluru, Pune',
            'TIFR - Mumbai, Bengaluru, Hyderabad',
            'Chennai Mathematical Institute (CMI) - Chennai',
            'International Institute of Information Technology (IIIT) - Hyderabad, Bengaluru, Delhi'
        ],
        'education_path': 'M.Sc Mathematics, M.Sc Statistics, PhD in Mathematics/Statistics, Integrated PhD programs',
        'certifications': ['Actuarial Fellow', 'Certified Statistician', 'Data Science Professional', 'Machine Learning Certification'],
        'hiring_cities': ['Bengaluru', 'Mumbai', 'Chennai', 'Hyderabad', 'Pune', 'Kolkata', 'Delhi NCR', 'Ahmedabad']
    },

    # ==================== 9. PHYSICS ====================
    'physics': {
        'name': 'Physics & Astronomy',
        'icon': '⚛️',
        'description': 'This fundamental science stream explores the laws of nature, matter, energy, and the universe.',
        'careers': ['Research Scientist - Conduct physics research', 'Astrophysicist - Study celestial bodies', 'Data Scientist - Apply physics to data', 'Medical Physicist - Apply to healthcare', 'Physics Professor - Teach and research', 'Quantum Computing Specialist - Develop quantum algorithms', 'Nuclear Engineer - Work with nuclear tech', 'Materials Scientist - Study material properties'],
        'subjects': ['Mechanics', 'Electromagnetism', 'Thermodynamics', 'Quantum Mechanics', 'Astrophysics', 'Nuclear Physics', 'Optics'],
        'skills': ['Scientific Reasoning', 'Experimental Design', 'Data Analysis', 'Problem Solving', 'Research Skills', 'Mathematical Modeling'],
        'software_skills': [
            '⚛️ Programming: Python (NumPy, SciPy), MATLAB, C++, Fortran',
            '📊 Data Analysis: ROOT, AstroPy, IRAF, DS9',
            '🔬 Simulation: COMSOL Multiphysics, ANSYS, Geant4',
            '🌌 Astronomy: SAOImage DS9, Aladin, TOPCAT',
            '🧪 LabVIEW for instrumentation & data acquisition',
            '📈 Computational Physics: Quantum ESPRESSO, VASP'
        ],
        'career_skills': [
            '⚛️ Scientific Reasoning & Critical Thinking',
            '🔬 Experimental Design & Methodology',
            '📊 Data Analysis & Interpretation',
            '🎯 Problem Solving & Mathematical Modeling',
            '📚 Research & Publication Skills',
            '🤝 Collaboration & Teamwork in Research'
        ],
        'technical_skills': [
          'Quantum Mechanics & Theory',
          'Thermodynamics & Statistical Physics',
          'Electromagnetism & Optics',
          'Computational Physics (Python, MATLAB)',
          'Experimental Design & Lab Skills',
          'Data Analysis & Modeling',
          'Nuclear Physics',
          'Astrophysics & Cosmology',
          'Material Science',
          'Semiconductor Physics',
          'Instrumentation & Measurement',
          'Scientific Computing'
        ],
        'future_scope': 'Research institutions, Space agencies, Tech industry, Healthcare',
        'top_companies': [
            'Indian Space Research Organisation (ISRO) - Bengaluru, Thiruvananthapuram, Ahmedabad, Sriharikota, Hyderabad, Delhi',
            'Defence Research and Development Organisation (DRDO) - Delhi, Hyderabad, Bengaluru, Pune, Chandigarh, Tezpur, Jodhpur',
            'Bhabha Atomic Research Centre (BARC) - Mumbai, Indore, Kalpakkam, Tarapur, Trombay',
            'Tata Institute of Fundamental Research (TIFR) - Mumbai, Bengaluru, Hyderabad, Pune',
            'Indian Institute of Science (IISc) - Bengaluru',
            'Physical Research Laboratory (PRL) - Ahmedabad',
            'Saha Institute of Nuclear Physics - Kolkata',
            'Inter-University Centre for Astronomy and Astrophysics (IUCAA) - Pune',
            'Institute of Physics (IOP) - Bhubaneswar',
            'Indian Institute of Astrophysics (IIA) - Bengaluru, Kodaikanal',
            'Raman Research Institute (RRI) - Bengaluru',
            'National Physical Laboratory (NPL) - New Delhi',
            'Variable Energy Cyclotron Centre (VECC) - Kolkata'
        ],
        'education_path': 'B.Sc Physics, M.Sc Physics, PhD in Physics, B.Tech Engineering Physics',
        'certifications': ['Research Certification', 'Lab Safety Certification', 'Data Science Certification', 'Computational Physics', 'Nuclear Safety Certification'],
        'hiring_cities': ['Bengaluru', 'Mumbai', 'Hyderabad', 'Pune', 'Ahmedabad', 'Kolkata', 'Thiruvananthapuram', 'Delhi NCR', 'Sriharikota', 'Indore', 'Kalpakkam', 'Bhubaneswar', 'Kodaikanal', 'Chandigarh']
    },
    'physics_college': {
        'name': 'Physics & Astronomy (Advanced)',
        'icon': '⚛️',
        'description': 'Advanced study in physics, quantum mechanics, and astrophysics.',
        'careers': ['Senior Research Scientist - Lead research teams', 'Quantum Physicist - Develop quantum technologies', 'Astronomer - Study celestial phenomena', 'Nuclear Physicist - Work on nuclear energy', 'Physics Professor - Teach at universities', 'Patent Examiner - Review physics patents'],
        'subjects': ['Quantum Field Theory', 'General Relativity', 'Statistical Mechanics', 'Particle Physics', 'Cosmology', 'String Theory'],
        'skills': ['Advanced Research', 'Computational Physics', 'Scientific Writing', 'Project Management', 'Teaching', 'Grant Writing'],
        'software_skills': [
            '⚛️ Advanced Simulation: GROMACS, LAMMPS, Quantum ESPRESSO',
            '📊 Data Science: Python, R, Julia for Physics',
            '🌌 Radio Astronomy: CASA, AIPS, MIRIAD',
            '🔬 Particle Physics: ROOT, Geant4, MadGraph',
            '💻 HPC: MPI, OpenMP, CUDA programming',
            '📈 Scientific Computing: MATLAB, Mathematica, Maple'
        ],
        'career_skills': [
            '🎯 Advanced Research Leadership',
            '🔬 Experimental Physics & Instrumentation',
            '📊 Big Data in Physics & Astronomy',
            '💡 Quantum Computing & Emerging Technologies',
            '📚 Grant Writing & Research Funding',
            '👥 Mentoring & Teaching Physics'
        ],
        'technical_skills': [
          'Quantum Mechanics & Theory',
          'Thermodynamics & Statistical Physics',
          'Electromagnetism & Optics',
          'Computational Physics (Python, MATLAB)',
          'Experimental Design & Lab Skills',
          'Data Analysis & Modeling',
          'Nuclear Physics',
          'Astrophysics & Cosmology',
          'Material Science',
          'Semiconductor Physics',
          'Instrumentation & Measurement',
          'Scientific Computing'
        ],
        'future_scope': 'National labs, Space agencies, Quantum computing companies, Academia',
        'top_companies': [
            'ISRO - Bengaluru, Thiruvananthapuram, Ahmedabad',
            'DRDO - Delhi, Hyderabad, Bengaluru',
            'BARC - Mumbai, Indore, Kalpakkam',
            'TIFR - Mumbai, Bengaluru, Hyderabad',
            'IISc - Bengaluru',
            'PRL - Ahmedabad',
            'IUCAA - Pune',
            'IIA - Bengaluru',
            'RRI - Bengaluru',
            'CERN India (through DAE) - Mumbai (Collaboration)',
            'LIGO India - Pune, Bengaluru (Collaboration)'
        ],
        'education_path': 'M.Sc Physics, PhD in Physics, Integrated PhD programs, M.Tech Engineering Physics',
        'certifications': ['Research Fellowship', 'Teaching Certification', 'Computational Physics', 'Quantum Computing Certification', 'Nuclear Physics Certification'],
        'hiring_cities': ['Bengaluru', 'Mumbai', 'Hyderabad', 'Pune', 'Ahmedabad', 'Kolkata', 'Delhi NCR', 'Thiruvananthapuram', 'Indore', 'Kalpakkam', 'Bhubaneswar']
    },

    # ==================== 10. CHEMISTRY ====================
    'chemistry': {
        'name': 'Chemistry & Chemical Sciences',
        'icon': '🧪',
        'description': 'This stream explores the composition, structure, and properties of matter and chemical reactions.',
        'careers': ['Chemist - Analyze chemical substances', 'Pharmaceutical Scientist - Develop new drugs', 'Materials Scientist - Create new materials', 'Forensic Scientist - Analyze crime evidence', 'Quality Control Analyst - Ensure product quality', 'Chemical Engineer - Design chemical processes', 'Environmental Chemist - Study environmental impacts', 'Analytical Chemist - Perform chemical analysis'],
        'subjects': ['Organic Chemistry', 'Inorganic Chemistry', 'Physical Chemistry', 'Analytical Chemistry', 'Biochemistry', 'Polymer Chemistry'],
        'skills': ['Laboratory Skills', 'Analytical Thinking', 'Attention to Detail', 'Research Methods', 'Safety Protocols', 'Problem Solving'],
        'software_skills': [
            '🧪 Analytical Software: ChemDraw, MarvinSketch, ChemOffice',
            '📊 Lab Information Systems: LIMS, LabWare, STARLIMS',
            '📈 Statistical Analysis: R, Python, Minitab, JMP',
            '🔬 Spectroscopy: OriginLab, GRAMS/AI, OMNIC',
            '💻 Computational Chemistry: Gaussian, Schrödinger, GROMACS',
            '🔧 Chromatography: Empower, Chromeleon, OpenLab'
        ],
        'career_skills': [
            '🧪 Laboratory Techniques & Safety Protocols',
            '🔍 Analytical Thinking & Attention to Detail',
            '📊 Method Development & Validation',
            '📚 Research & Documentation Skills',
            '⚖️ Quality Control & Regulatory Compliance',
            '🤝 Team Collaboration & Communication'
        ],
        'technical_skills': [
          'Organic & Inorganic Synthesis',
          'Analytical Techniques (HPLC, GC, NMR, Mass Spec)',
          'Spectroscopy (FTIR, UV-Vis)',
          'Chromatography Methods',
          'Polymer Chemistry',
          'Medicinal Chemistry',
          'Green Chemistry Principles',
          'Chemical Process Engineering',
          'Laboratory Safety Protocols',
          'Quality Control Testing',
          'Computational Chemistry',
          'Materials Characterization'
        ],
        'future_scope': 'Pharmaceutical industry, Materials science, Environmental science, Food industry',
        'top_companies': [
            'Reliance Industries - Mumbai, Jamnagar, Vadodara, Hazira, Dahej, Nagothane, Patalganga, Silvassa',
            'Sun Pharmaceutical - Mumbai, Vadodara, Gurugram, Halol, Ahmedabad, Mohali, Indore',
            'Dr. Reddy\'s Laboratories - Hyderabad, Bengaluru, Vishakhapatnam, Srikakulam, Duvvada',
            'Cipla - Mumbai, Bengaluru, Goa, Kurkumbh, Indore, Sikkim, Patalganga',
            'Torrent Pharmaceuticals - Ahmedabad, Indore, Baddi, Dahej',
            'Lupin - Mumbai, Pune, Indore, Mandideep, Goa, Nagpur, Tarapur',
            'Aurobindo Pharma - Hyderabad, Vizag, Nellore, Srikakulam, Himachal Pradesh, Jadcherla',
            'Zydus Cadila - Ahmedabad, Vadodara, Sikkim, Baddi, Indore, Daman',
            'Hindustan Unilever - Mumbai, Bengaluru, Kolkata, Delhi NCR, Chennai, Pune, Haridwar, Sumerpur',
            'Indian Oil Corporation - Delhi NCR, Mumbai, Chennai, Kolkata, Bengaluru, Guwahati, Panipat, Mathura, Barauni',
            'Bharat Petroleum - Mumbai, Delhi NCR, Chennai, Kochi, Bengaluru, Nagpur',
            'Hindustan Petroleum - Mumbai, Delhi NCR, Chennai, Bengaluru, Vizag, Kochi'
        ],
        'education_path': 'B.Sc Chemistry, M.Sc Chemistry, PhD in Chemistry, B.Tech Chemical Engineering',
        'certifications': ['Lab Safety Certification', 'Analytical Chemistry Certification', 'GMP Certification', 'Green Chemistry', 'ISO 17025'],
        'hiring_cities': ['Mumbai', 'Hyderabad', 'Ahmedabad', 'Vadodara', 'Bengaluru', 'Pune', 'Delhi NCR', 'Chennai', 'Kolkata', 'Jamnagar', 'Indore', 'Goa', 'Nagpur', 'Vishakhapatnam', 'Baddi', 'Sikkim']
    },
    'chemistry_college': {
        'name': 'Chemistry & Chemical Sciences (Advanced)',
        'icon': '🧪',
        'description': 'Advanced study in chemical sciences and molecular modeling.',
        'careers': ['Research Chemist - Lead research projects', 'Pharmaceutical R&D Director - Manage drug development', 'Materials Scientist - Develop new materials', 'Environmental Consultant - Advise on environment', 'Chemistry Professor - Teach at universities', 'Patent Attorney - Handle chemical patents'],
        'subjects': ['Advanced Organic Synthesis', 'Computational Chemistry', 'Supramolecular Chemistry', 'Medicinal Chemistry', 'Nanochemistry'],
        'skills': ['Advanced Lab Techniques', 'Research Leadership', 'Scientific Communication', 'Project Management', 'Grant Writing', 'Mentoring'],
        'software_skills': [
            '🧪 Advanced Computational: Gaussian 16, GAMESS, ORCA',
            '🔬 Molecular Modeling: PyMOL, Chimera, VMD',
            '📊 Chemoinformatics: KNIME, Pipeline Pilot, DataWarrior',
            '🧬 Bioinformatics: BLAST, ClustalW, Geneious',
            '📈 Advanced Analytics: Python (RDKit), R (ChemmineR)',
            '🔧 ELN: LabArchives, PerkinElmer Elements'
        ],
        'career_skills': [
            '🎯 Research Leadership & Strategy',
            '🔬 Advanced Analytical Method Development',
            '📊 Grant Writing & Research Funding',
            '⚖️ Regulatory Affairs & Patent Law',
            '🧪 Green Chemistry & Sustainability',
            '👥 Mentoring & Team Management'
        ],
        'technical_skills': [
          'Organic & Inorganic Synthesis',
          'Analytical Techniques (HPLC, GC, NMR, Mass Spec)',
          'Spectroscopy (FTIR, UV-Vis)',
          'Chromatography Methods',
          'Polymer Chemistry',
          'Medicinal Chemistry',
          'Green Chemistry Principles',
          'Chemical Process Engineering',
          'Laboratory Safety Protocols',
          'Quality Control Testing',
          'Computational Chemistry',
          'Materials Characterization'
       ],
        'future_scope': 'Pharmaceutical R&D, Materials research, Environmental consulting, Academia',
        'top_companies': [
            'Reliance Industries - Mumbai, Jamnagar, Vadodara',
            'Sun Pharmaceutical - Mumbai, Vadodara, Gurugram',
            'Dr. Reddy\'s Laboratories - Hyderabad',
            'Cipla - Mumbai, Goa',
            'Indian Institute of Chemical Technology (IICT) - Hyderabad',
            'National Chemical Laboratory (NCL) - Pune',
            'Central Drug Research Institute (CDRI) - Lucknow',
            'Indian Association for the Cultivation of Science (IACS) - Kolkata',
            'CSIR Laboratories (Across India) - Delhi, Chennai, Chandigarh, Jammu, Bhopal, Dehradun',
            'Indian Institute of Science (IISc) - Bengaluru'
        ],
        'education_path': 'M.Sc Chemistry, PhD in Chemistry, Integrated PhD programs',
        'certifications': ['Research Fellowship', 'Analytical Chemistry Advanced', 'Patent Law Certification', 'GMP Advanced', 'CSIR-UGC NET'],
        'hiring_cities': ['Mumbai', 'Hyderabad', 'Ahmedabad', 'Pune', 'Bengaluru', 'Vadodara', 'Delhi NCR', 'Chennai', 'Kolkata', 'Lucknow', 'Chandigarh']
    },

    # ==================== 11. BIOLOGY ====================
    'biology': {
        'name': 'Biology & Life Sciences',
        'icon': '🧬',
        'description': 'This stream explores living organisms, their structure, function, growth, and evolution.',
        'careers': ['Biologist - Study living organisms', 'Geneticist - Research genes and heredity', 'Microbiologist - Study microorganisms', 'Biotechnologist - Apply biology to technology', 'Environmental Scientist - Solve environmental issues', 'Wildlife Biologist - Study and conserve wildlife', 'Marine Biologist - Study ocean life', 'Bioinformatician - Analyze biological data'],
        'subjects': ['Cell Biology', 'Genetics', 'Ecology', 'Microbiology', 'Biochemistry', 'Molecular Biology', 'Evolutionary Biology'],
        'skills': ['Laboratory Techniques', 'Observation Skills', 'Research Methods', 'Data Analysis', 'Critical Thinking', 'Scientific Writing'],
        'software_skills': [
            '🧬 Bioinformatics: BLAST, ClustalW, Geneious, MEGA',
            '📊 Statistical Analysis: R, SPSS, GraphPad Prism, JMP',
            '🔬 Lab Software: LabWare, Benchling, SnapGene',
            '🧪 Molecular Biology: Primer3, SnapGene, Vector NTI',
            '📈 Data Visualization: Tableau, ggplot2, BioVinci',
            '🧬 Genomics: Galaxy, IGV, UCSC Genome Browser'
        ],
        'career_skills': [
            '🧬 Laboratory Techniques & Aseptic Methods',
            '🔬 Observation & Data Collection Skills',
            '📊 Research Methods & Experimental Design',
            '🎯 Critical Thinking & Problem Solving',
            '📚 Scientific Writing & Documentation',
            '🤝 Team Collaboration & Communication'
        ],
        'technical_skills': [
          'Molecular Biology (PCR, Gel Electrophoresis)',
          'Cell Culture Techniques',
          'Microscopy & Imaging',
          'Genetics & Genomics',
          'Biochemistry Assays',
          'Bioinformatics (BLAST, Sequence Analysis)',
          'Ecology & Field Sampling',
          'Microbiology Techniques',
          'Histology & Tissue Processing',
          'Flow Cytometry',
          'CRISPR & Gene Editing',
          'Phylogenetic Analysis'
       ],
        'future_scope': 'Biotechnology companies, Environmental agencies, Pharmaceutical industry',
        'top_companies': [
            'Biocon - Bengaluru, Mysore, Hyderabad',
            'Serum Institute of India - Pune, Hadapsar',
            'Panacea Biotec - Delhi NCR, Baddi, Lalru, Jammu',
            'Bharat Biotech - Hyderabad, Guntur',
            'Indian Immunologicals - Hyderabad, Ooty, Gwalior',
            'Syngene International - Bengaluru, Mangalore, Hyderabad',
            'Novozymes India - Bengaluru, Delhi NCR, Pune, Hyderabad, Mysore',
            'National Institute of Oceanography (NIO) - Goa, Kochi, Visakhapatnam, Mumbai',
            'Wildlife Institute of India (WII) - Dehradun',
            'Zoological Survey of India (ZSI) - Kolkata, Hyderabad, Chennai, Pune, Dehradun, Andaman & Nicobar',
            'National Centre for Biological Sciences (NCBS) - Bengaluru',
            'Centre for Cellular and Molecular Biology (CCMB) - Hyderabad',
            'Institute of Genomics and Integrative Biology (IGIB) - Delhi',
            'National Institute of Plant Genome Research (NIPGR) - New Delhi'
        ],
        'education_path': 'B.Sc Biology, B.Sc Biotechnology, M.Sc Life Sciences, PhD, B.Tech Biotechnology',
        'certifications': ['Lab Safety', 'Biotechnology Certification', 'Environmental Impact Assessment', 'Bioinformatics', 'GMP Certification'],
        'hiring_cities': ['Bengaluru', 'Hyderabad', 'Pune', 'Delhi NCR', 'Mumbai', 'Chennai', 'Kolkata', 'Goa', 'Dehradun', 'Mysore', 'Kochi', 'Visakhapatnam', 'Chandigarh', 'Bhubaneswar']
    },
    'biology_college': {
        'name': 'Biology & Life Sciences (Advanced)',
        'icon': '🧬',
        'description': 'Advanced study in biological sciences, genetics, and biotechnology.',
        'careers': ['Research Biologist - Lead research projects', 'Genetic Counselor - Advise on genetic conditions', 'Biotech R&D Manager - Manage development', 'Conservation Scientist - Lead conservation efforts', 'Biology Professor - Teach at universities', 'Pharmaceutical Researcher - Develop new drugs'],
        'subjects': ['Advanced Genetics', 'Proteomics', 'Bioinformatics', 'Stem Cell Biology', 'Systems Biology', 'Synthetic Biology'],
        'skills': ['Advanced Research', 'Bioinformatics', 'Grant Writing', 'Team Leadership', 'Scientific Writing', 'Project Management'],
        'software_skills': [
            '🧬 Advanced Genomics: BWA, GATK, Samtools, Cell Ranger',
            '🔬 Proteomics: MaxQuant, Proteome Discoverer, Skyline',
            '🧪 Structural Biology: PyMOL, Chimera, Coot',
            '📊 Systems Biology: Cytoscape, CellDesigner, COPASI',
            '🤖 Machine Learning: Python (scikit-learn), R (caret) for bioinformatics',
            '🔧 Lab Management: Quartzy, Labguru, eLabJournal'
        ],
        'career_skills': [
            '🎯 Research Leadership & Project Direction',
            '🔬 Advanced Genomic & Proteomic Analysis',
            '📊 Bioinformatics & Computational Biology',
            '💡 Innovation in Biotech & Synthetic Biology',
            '📚 Grant Writing & Funding Acquisition',
            '👥 Team Mentoring & Scientific Collaboration'
        ],
        'technical_skills': [
          'Molecular Biology (PCR, Gel Electrophoresis)',
          'Cell Culture Techniques',
          'Microscopy & Imaging',
          'Genetics & Genomics',
          'Biochemistry Assays',
          'Bioinformatics (BLAST, Sequence Analysis)',
          'Ecology & Field Sampling',
          'Microbiology Techniques',
          'Histology & Tissue Processing',
          'Flow Cytometry',
          'CRISPR & Gene Editing',
          'Phylogenetic Analysis'
        ],
        'future_scope': 'Biotech R&D, Pharmaceutical research, Environmental conservation, Academia',
        'top_companies': [
            'Biocon - Bengaluru, Mysore',
            'Serum Institute of India - Pune',
            'Bharat Biotech - Hyderabad',
            'Syngene International - Bengaluru',
            'National Centre for Biological Sciences (NCBS) - Bengaluru',
            'Centre for Cellular and Molecular Biology (CCMB) - Hyderabad',
            'Institute of Genomics and Integrative Biology (IGIB) - Delhi',
            'National Institute of Immunology (NII) - New Delhi',
            'Indian Institute of Science (IISc) - Bengaluru',
            'Jawaharlal Nehru University (JNU) - New Delhi',
            'University of Hyderabad - Hyderabad'
        ],
        'education_path': 'M.Sc Life Sciences, PhD in Biology, Integrated PhD, M.Tech Biotechnology',
        'certifications': ['Research Fellowship', 'Bioinformatics Certification', 'Clinical Research', 'GCP Certification', 'CSIR-UGC NET'],
        'hiring_cities': ['Bengaluru', 'Hyderabad', 'Pune', 'Delhi NCR', 'Mumbai', 'Chennai', 'Kolkata', 'Goa', 'Dehradun', 'Mysore']
    },

    # ==================== 12. ARTS & HUMANITIES ====================
    'arts_humanities': {
        'name': 'Arts & Humanities',
        'icon': '🎭',
        'description': 'This stream focuses on literature, history, philosophy, languages, and social sciences. Students develop critical thinking and communication skills.',
        'careers': ['Teacher/Professor - Educate students', 'Writer/Author - Create written content', 'Journalist - Report news and stories', 'Historian - Research and preserve history', 'Philosopher - Study fundamental questions', 'Translator - Convert languages', 'Librarian - Manage information resources', 'Museum Curator - Manage collections'],
        'subjects': ['Literature', 'History', 'Philosophy', 'Languages', 'Psychology', 'Sociology', 'Political Science', 'Economics'],
        'skills': ['Critical Thinking', 'Communication', 'Research Skills', 'Writing', 'Analysis', 'Empathy', 'Cultural Awareness'],
        'software_skills': [
            '📝 Word Processing: MS Word, Google Docs, LaTeX, Scrivener',
            '📚 Reference Management: Zotero, Mendeley, EndNote, Paperpile',
            '🔍 Research Tools: JSTOR, Google Scholar, ProQuest, Scopus',
            '📊 Digital Humanities: Omeka, Voyant Tools, Gephi',
            '📰 CMS: WordPress, Drupal, Joomla, Medium',
            '🎨 Multimedia: Adobe InDesign, Audacity, Canva'
        ],
        'career_skills': [
            '🎯 Critical Thinking & Analytical Skills',
            '✍️ Writing & Communication Excellence',
            '📚 Research & Information Literacy',
            '🤝 Empathy & Cultural Awareness',
            '🎨 Creativity & Storytelling',
            '🗣️ Public Speaking & Presentation Skills'
        ],
      'technical_skills': [
           'Research Methodology',
           'Academic Writing & Citation',
           'Historical Analysis',
           'Language Proficiency',
           'Literary Criticism',
           'Archival Research',
           'Digital Humanities Tools',
           'Translation Skills',
           'Philosophical Analysis',
           'Media & Communication',
           'Cultural Studies',
           'Public Speaking'
       ],
        'future_scope': 'Education, Publishing, Media, Research, Government, NGOs',
        'top_companies': [
            'NCERT - New Delhi, Across Regional Centers',
            'Central Universities - Across India (Delhi, Hyderabad, Allahabad, Jammu, Kashmir, Kerala, Gujarat, Punjab, Tamil Nadu, etc.)',
            'State Universities - All State Capitals and Major Cities',
            'Penguin Random House India - Gurugram, New Delhi, Mumbai, Bengaluru, Kolkata',
            'HarperCollins India - Noida, New Delhi, Mumbai',
            'The Times Group - Mumbai, Delhi NCR, Bengaluru, Chennai, Kolkata, Hyderabad, Ahmedabad, Pune, Lucknow',
            'Hindustan Times - Delhi NCR, Mumbai, Lucknow, Patna, Ranchi, Chandigarh',
            'The Hindu - Chennai, Bengaluru, Delhi, Mumbai, Hyderabad, Kolkata, Thiruvananthapuram, Kochi',
            'The Indian Express - Delhi NCR, Mumbai, Chennai, Bengaluru, Kolkata, Ahmedabad, Lucknow, Chandigarh',
            'NDTV - Delhi NCR, Mumbai, Bengaluru, Chennai, Hyderabad, Kolkata',
            'BBC News India - Delhi NCR, Mumbai',
            'CNN-News18 - Delhi NCR, Mumbai, Bengaluru, Chennai',
            'UNESCO India - New Delhi',
            'PRS Legislative Research - New Delhi',
            'Indian Council for Cultural Relations (ICCR) - New Delhi',
            'National Museum - New Delhi',
            'Indian Museum - Kolkata',
            'Salar Jung Museum - Hyderabad',
            'Chhatrapati Shivaji Maharaj Vastu Sangrahalaya (CSMVS) - Mumbai'
        ],
        'education_path': 'BA in Arts/Humanities, MA, PhD, B.Ed, M.Ed',
        'certifications': ['Teaching Certification (B.Ed, M.Ed)', 'Research Certification', 'Digital Humanities', 'Archive Management', 'Journalism Certification'],
        'hiring_cities': ['Delhi NCR', 'Mumbai', 'Bengaluru', 'Chennai', 'Kolkata', 'Pune', 'Hyderabad', 'Ahmedabad', 'Lucknow', 'Jaipur', 'Chandigarh', 'Bhopal', 'Patna', 'Ranchi', 'Thiruvananthapuram', 'Kochi', 'Guwahati']
    },
    'arts_humanities_college': {
        'name': 'Arts & Humanities (Advanced)',
        'icon': '🎭',
        'description': 'Advanced study in arts, literature, philosophy, and social sciences.',
        'careers': ['University Professor - Teach advanced courses', 'Research Scholar - Conduct academic research', 'Editor - Edit publications', 'Cultural Heritage Manager - Preserve culture', 'Policy Analyst - Analyze social policies', 'Creative Writer - Publish creative works'],
        'subjects': ['Advanced Literary Theory', 'Historical Methodology', 'Contemporary Philosophy', 'Cultural Studies', 'Media Studies', 'Digital Humanities'],
        'skills': ['Advanced Research', 'Academic Writing', 'Critical Analysis', 'Teaching', 'Public Speaking', 'Project Management'],
        'software_skills': [
            '📚 Advanced Research: NVivo, ATLAS.ti for qualitative analysis',
            '📝 Academic Writing: Scrivener, Ulysses, Authorea',
            '📊 Digital Humanities: Palladio, NodeXL, Tableau Public',
            '🎓 Online Teaching: Moodle, Canvas, Blackboard',
            '📰 Media Analysis: Meltwater, Brand24, Talkwalker',
            '🗂️ Archive Management: ArchivesSpace, CollectiveAccess'
        ],
        'career_skills': [
            '🎯 Advanced Academic Research',
            '✍️ Scholarly Writing & Publication',
            '📚 Curriculum Development & Pedagogy',
            '🗣️ Public Speaking & Conference Presentation',
            '💡 Critical Theory & Contemporary Thought',
            '👥 Academic Leadership & Mentoring'
        ],
        'technical_skills': [
          'Research Methodology',
          'Academic Writing & Citation',
          'Historical Analysis',
          'Language Proficiency',
          'Literary Criticism',
          'Archival Research',
          'Digital Humanities Tools',
          'Translation Skills',
          'Philosophical Analysis',
          'Media & Communication',
          'Cultural Studies',
          'Public Speaking'
       ],
        'future_scope': 'Academia, Research institutions, Publishing, Cultural institutions',
        'top_companies': [
            'Jawaharlal Nehru University (JNU) - New Delhi',
            'University of Delhi - Delhi',
            'Banaras Hindu University (BHU) - Varanasi',
            'University of Calcutta - Kolkata',
            'University of Mumbai - Mumbai',
            'University of Madras - Chennai',
            'University of Hyderabad - Hyderabad',
            'University of Pune (SPPU) - Pune',
            'University of Bengaluru - Bengaluru',
            'Penguin Random House - Gurugram, New Delhi',
            'HarperCollins - Noida, New Delhi',
            'Indian Council of Historical Research (ICHR) - New Delhi',
            'Indian Council of Philosophical Research (ICPR) - New Delhi',
            'Sahitya Akademi - New Delhi, Across Regional Offices',
            'National Archives of India - New Delhi',
            'Indira Gandhi National Centre for the Arts (IGNCA) - New Delhi'
        ],
        'education_path': 'MA in Arts/Humanities, M.Phil, PhD, Post-doctoral research',
        'certifications': ['Teaching Certification', 'Research Fellowship (UGC-NET)', 'Digital Humanities Certification', 'Archive Management', 'Museum Studies'],
        'hiring_cities': ['Delhi NCR', 'Mumbai', 'Bengaluru', 'Chennai', 'Kolkata', 'Pune', 'Hyderabad', 'Varanasi', 'Ahmedabad', 'Lucknow', 'Jaipur', 'Chandigarh', 'Bhopal']
    },

    # ==================== 13. LAW ====================
    'law': {
        'name': 'Law & Legal Studies',
        'icon': '⚖️',
        'description': 'This stream focuses on legal systems, justice, rights, and regulations. Students learn about laws, court procedures, and legal reasoning.',
        'careers': ['Lawyer - Represent clients in court', 'Judge - Preside over legal cases', 'Legal Advisor - Provide legal counsel', 'Corporate Lawyer - Handle business law', 'Criminal Lawyer - Handle criminal cases', 'Legal Researcher - Research legal issues', 'Public Prosecutor - Represent the state', 'Legal Consultant - Advise on legal matters'],
        'subjects': ['Constitutional Law', 'Criminal Law', 'Civil Law', 'Corporate Law', 'International Law', 'Legal Writing', 'Moot Court'],
        'skills': ['Critical Thinking', 'Argumentation', 'Research Skills', 'Communication', 'Negotiation', 'Analytical Skills', 'Attention to Detail'],
        'software_skills': [
            '⚖️ Legal Research: Manupatra, SCC Online, Westlaw India, LexisNexis',
            '📄 Document Management: ContractExpress, HotDocs, DocuSign',
            '⚙️ Case Management: Clio, MyCase, PracticePanther, LegalEdge',
            '📊 E-discovery: Relativity, Logikcull, Everlaw',
            '💰 Legal Billing: Tabs3, Bill4Time, TimeSolv, Legistify',
            '📝 Legal Drafting: Draftable, CompareDocs, Kira Systems'
        ],
        'career_skills': [
            '⚖️ Critical Thinking & Logical Reasoning',
            '🗣️ Argumentation & Persuasion Skills',
            '📚 Legal Research & Writing Excellence',
            '🤝 Negotiation & Conflict Resolution',
            '🔍 Attention to Detail & Accuracy',
            '⚖️ Ethical Judgment & Professional Integrity'
        ],
        'technical_skills': [
          'Legal Research (Manupatra, SCC Online)',
          'Drafting (Pleadings, Contracts, Deeds)',
          'Constitutional Law Knowledge',
          'Criminal & Civil Procedure',
          'Corporate & Commercial Law',
          'Intellectual Property Law',
          'Alternative Dispute Resolution (Arbitration, Mediation)',
          'Legal Writing & Briefing',
          'Moot Court Advocacy',
          'Statutory Interpretation',
          'Compliance & Regulatory Knowledge',
          'Due Diligence'
       ],
        'future_scope': 'Legal practice, Corporate legal departments, Government, NGOs, Judiciary',
        'top_companies': [
            'Supreme Court of India - New Delhi',
            'High Courts - Across India (Delhi, Mumbai, Chennai, Kolkata, Bengaluru, Hyderabad, Ahmedabad, Patna, Allahabad, Chandigarh, Guwahati, etc.)',
            'District Courts - All District Headquarters across India',
            'AZB & Partners - Mumbai, Delhi, Bengaluru, Pune, Chennai',
            'Khaitan & Co - Mumbai, Delhi, Bengaluru, Kolkata, Gurugram, Pune',
            'Shardul Amarchand Mangaldas - Delhi, Mumbai, Bengaluru, Kolkata, Gurugram, Chennai',
            'Cyril Amarchand Mangaldas - Mumbai, Delhi, Bengaluru, Chennai, Hyderabad, Kolkata, Ahmedabad',
            'Trilegal - Mumbai, Delhi, Bengaluru, Hyderabad',
            'J. Sagar Associates - Mumbai, Delhi, Bengaluru, Chennai, Hyderabad, Gurugram',
            'Tata Sons Legal Dept - Mumbai',
            'Reliance Industries Legal Dept - Mumbai, Delhi NCR',
            'Infosys Legal Dept - Bengaluru',
            'Wipro Legal Dept - Bengaluru',
            'ICICI Bank Legal Dept - Mumbai, Delhi NCR',
            'HDFC Bank Legal Dept - Mumbai',
            'Ministry of Law and Justice - New Delhi',
            'Attorney General of India Office - New Delhi',
            'Solicitor General of India Office - New Delhi'
        ],
        'education_path': 'LLB (Bachelor of Laws), LLM (Master of Laws), PhD in Law, Integrated BA-LLB, BBA-LLB',
        'certifications': ['Bar Council Certification (All India Bar Exam - AIBE)', 'Mediation Certification', 'Arbitration Certification', 'Cyber Law Certification', 'Intellectual Property Rights Certification'],
        'hiring_cities': ['Delhi NCR', 'Mumbai', 'Bengaluru', 'Chennai', 'Kolkata', 'Hyderabad', 'Pune', 'Ahmedabad', 'Lucknow', 'Patna', 'Chandigarh', 'Bhopal', 'Jaipur', 'Guwahati', 'All State Capitals']
    },
    'law_college': {
        'name': 'Law & Legal Studies (Advanced)',
        'icon': '⚖️',
        'description': 'Advanced study in legal systems, jurisprudence, and specialized law areas.',
        'careers': ['Senior Lawyer - Lead legal teams', 'High Court Judge - Preside over high courts', 'Legal Department Head - Manage legal operations', 'Legal Scholar - Conduct legal research', 'International Lawyer - Handle cross-border cases', 'Legal Tech Consultant - Apply tech to law'],
        'subjects': ['Constitutional Law Advanced', 'Jurisprudence', 'International Trade Law', 'Intellectual Property Law', 'Environmental Law', 'Human Rights Law'],
        'skills': ['Advanced Legal Reasoning', 'Case Strategy', 'Legal Writing', 'Negotiation', 'Leadership', 'Client Management', 'Courtroom Skills'],
        'software_skills': [
            '⚖️ Advanced Legal Research: Westlaw Edge, Lexis+, Practical Law',
            '🤖 Legal Tech: AI-powered contract review (Kira, LawGeex)',
            '📊 Litigation Analytics: Lex Machina, Premonition',
            '⚙️ Practice Management: Clio Grow, Lawmatics, Filevine',
            '📄 E-discovery Advanced: RelativityOne, Logikcull',
            '🔒 Cybersecurity for Law Firms: NetDocuments, iManage'
        ],
        'career_skills': [
            '🎯 Advanced Legal Strategy & Case Management',
            '⚖️ Supreme Court & High Court Litigation',
            '🌍 International Law & Cross-border Transactions',
            '💡 Legal Tech & Innovation Consulting',
            '👥 Team Leadership & Law Firm Management',
            '📚 Legal Scholarship & Academic Writing'
        ],
        'technical_skills': [
          'Legal Research (Manupatra, SCC Online)',
          'Drafting (Pleadings, Contracts, Deeds)',
          'Constitutional Law Knowledge',
          'Criminal & Civil Procedure',
          'Corporate & Commercial Law',
          'Intellectual Property Law',
          'Alternative Dispute Resolution (Arbitration, Mediation)',
          'Legal Writing & Briefing',
          'Moot Court Advocacy',
          'Statutory Interpretation',
          'Compliance & Regulatory Knowledge',
          'Due Diligence'
       ],
        'future_scope': 'Senior legal positions, Judiciary, Legal academia, International law',
        'top_companies': [
            'Supreme Court of India - New Delhi',
            'High Courts - Delhi, Mumbai, Bengaluru, Chennai, Kolkata, Hyderabad',
            'AZB & Partners - Mumbai, Delhi, Bengaluru',
            'Khaitan & Co - Mumbai, Delhi, Kolkata',
            'Shardul Amarchand Mangaldas - Delhi, Mumbai, Bengaluru',
            'Cyril Amarchand Mangaldas - Mumbai, Delhi, Bengaluru',
            'National Law Universities (NLUs) - Across India (Bengaluru, Delhi, Jodhpur, Bhopal, Kolkata, Hyderabad, Patna, Gandhinagar, etc.)',
            'Indian Law Institute (ILI) - New Delhi',
            'Supreme Court Bar Association - New Delhi',
            'Law Commission of India - New Delhi'
        ],
        'education_path': 'LLM (Master of Laws), PhD in Law, Executive LLM, Diploma in Specialized Law',
        'certifications': ['Supreme Court Advocate', 'International Law Certification', 'Arbitration Fellowship', 'Mediation Master', 'Corporate Law Certification'],
        'hiring_cities': ['Delhi NCR', 'Mumbai', 'Bengaluru', 'Chennai', 'Kolkata', 'Hyderabad', 'Ahmedabad', 'Pune', 'Lucknow', 'Chandigarh']
    },

    # ==================== 14. COMMERCE ====================
    'commerce': {
        'name': 'Commerce',
        'icon': '💰',
        'description': 'This stream focuses on trade, business, accounting, and economics. Students learn about financial management, taxation, and business operations.',
        'careers': ['Chartered Accountant - Manage financial accounts', 'Company Secretary - Handle corporate compliance', 'Cost Accountant - Manage cost analysis', 'Financial Analyst - Analyze financial data', 'Tax Consultant - Advise on taxation', 'Banking Professional - Work in banks', 'Insurance Advisor - Provide insurance solutions', 'Stock Broker - Trade in stock markets'],
        'subjects': ['Accountancy', 'Business Studies', 'Economics', 'Mathematics', 'Statistics', 'Taxation', 'Cost Accounting', 'Financial Management'],
        'skills': ['Numerical Ability', 'Analytical Thinking', 'Attention to Detail', 'Financial Literacy', 'Problem Solving', 'Ethical Judgment'],
        'software_skills': [
            '💰 Accounting: Tally ERP 9, Tally Prime, QuickBooks, Zoho Books',
            '📊 ERP: SAP FICO, Oracle Financials, Microsoft Dynamics 365',
            '📈 Taxation: ClearTax, Taxmann, CompuTax, GenTally',
            '📉 Advanced Excel: Pivot Tables, Power Query, VBA Macros',
            '📋 Financial Modeling: MS Excel, Python, R, Tableau',
            '🏦 Banking Software: Finacle, BaNCS, Flexcube'
        ],
        'career_skills': [
            '💰 Numerical Ability & Financial Literacy',
            '📊 Analytical Thinking & Data Interpretation',
            '🔍 Attention to Detail & Accuracy',
            '💡 Problem Solving & Decision Making',
            '⚖️ Ethical Judgment & Professional Integrity',
            '🗣️ Communication & Client Management'
        ],
        'technical_skills': [
          'Accounting Principles (Tally, SAP FICO)',
          'Taxation (Direct & Indirect)',
          'Auditing & Assurance',
          'Financial Reporting',
          'Cost Accounting',
          'Corporate Law Knowledge',
          'GST Compliance',
          'Budgeting & Forecasting',
          'Financial Statement Analysis',
          'Management Accounting',
          'Investment Analysis',
          'Banking Operations'
       ],
        'future_scope': 'Banking, Financial services, Corporate accounting, Taxation, Auditing',
        'top_companies': [
            'Deloitte India - Mumbai, Delhi, Bengaluru, Hyderabad, Chennai, Pune, Kolkata, Gurugram, Ahmedabad, Kochi',
            'PwC India - Kolkata, Mumbai, Delhi, Bengaluru, Hyderabad, Chennai, Pune, Ahmedabad, Guwahati',
            'KPMG India - Mumbai, Delhi, Bengaluru, Hyderabad, Chennai, Pune, Gurugram, Noida, Kochi, Chandigarh',
            'EY India - Mumbai, Delhi, Bengaluru, Hyderabad, Chennai, Kolkata, Pune, Ahmedabad, Kochi, Chandigarh',
            'HDFC Bank - Mumbai, Delhi, Bengaluru, Chennai, Kolkata, Pune, Hyderabad, Ahmedabad, Jaipur, Lucknow, Chandigarh, Kochi',
            'ICICI Bank - Mumbai, Delhi, Bengaluru, Hyderabad, Chennai, Kolkata, Pune, Ahmedabad, Jaipur, Lucknow',
            'State Bank of India - Across India (All Major Cities and Towns)',
            'Axis Bank - Mumbai, Delhi, Bengaluru, Kolkata, Chennai, Pune, Hyderabad, Ahmedabad, Chandigarh',
            'Kotak Mahindra Bank - Mumbai, Delhi, Bengaluru, Chennai, Hyderabad, Pune, Kolkata, Ahmedabad, Jaipur',
            'Bajaj Finserv - Pune, Mumbai, Delhi NCR, Bengaluru, Chennai, Hyderabad, Kolkata, Lucknow',
            'Tata Capital - Mumbai, Delhi, Bengaluru, Chennai, Kolkata, Hyderabad, Pune, Lucknow',
            'ICICI Prudential - Mumbai, Delhi NCR, Bengaluru, Chennai, Kolkata, Hyderabad, Pune, Ahmedabad',
            'HDFC Life - Mumbai, Delhi NCR, Bengaluru, Chennai, Kolkata, Hyderabad, Pune, Lucknow',
            'SBI Life - Mumbai, Across India',
            'National Stock Exchange (NSE) - Mumbai, Delhi, Kolkata, Chennai, Bengaluru, Ahmedabad, Hyderabad',
            'Bombay Stock Exchange (BSE) - Mumbai'
        ],
        'education_path': 'B.Com, BBA, M.Com, MBA, CA, CS, CMA, CFA',
        'certifications': ['CA (Chartered Accountant)', 'CS (Company Secretary)', 'CMA (Cost Management Accountant)', 'CFA', 'CPA', 'Financial Modeling Certification', 'NCFM Certification'],
        'hiring_cities': ['Mumbai', 'Delhi NCR', 'Bengaluru', 'Chennai', 'Hyderabad', 'Pune', 'Kolkata', 'Ahmedabad', 'Gurugram', 'Noida', 'Jaipur', 'Lucknow', 'Chandigarh', 'Kochi', 'Indore', 'Nagpur']
    },
    'commerce_college': {
        'name': 'Commerce (Advanced)',
        'icon': '💰',
        'description': 'Advanced study in commerce, financial management, and corporate accounting.',
        'careers': ['Senior Accountant - Lead accounting teams', 'Finance Manager - Manage corporate finance', 'Investment Banker - Handle financial transactions', 'Tax Director - Oversee tax strategy', 'Audit Partner - Lead audit firms', 'Chief Financial Officer - Manage company finances'],
        'subjects': ['Advanced Accounting', 'Corporate Finance', 'International Taxation', 'Financial Reporting', 'Auditing', 'Risk Management'],
        'skills': ['Strategic Financial Planning', 'Leadership', 'Risk Assessment', 'Corporate Governance', 'Regulatory Compliance', 'Team Management'],
        'software_skills': [
            '💰 Advanced Accounting: SAP S/4HANA Finance, Oracle Cloud ERP',
            '📊 Advanced Financial Modeling: Python, R, MATLAB',
            '📈 Business Intelligence: Tableau, Power BI, QlikView, Looker',
            '🏦 Treasury Management: Kyriba, Coupa, GTreasury',
            '📋 Audit Software: CaseWare, TeamMate, ACL Analytics',
            '💹 Risk Management: RiskWatch, Active Risk Manager, Resolver'
        ],
        'career_skills': [
            '🎯 Strategic Financial Leadership',
            '📊 Advanced Financial Analysis & Modeling',
            '⚖️ Corporate Governance & Compliance',
            '🤝 Investment Banking & M&A Strategy',
            '👥 Team Leadership & Talent Development',
            '🌍 Global Finance & International Taxation'
        ],
        'technical_skills': [
          'Accounting Principles (Tally, SAP FICO)',
          'Taxation (Direct & Indirect)',
          'Auditing & Assurance',
          'Financial Reporting',
          'Cost Accounting',
          'Corporate Law Knowledge',
          'GST Compliance',
          'Budgeting & Forecasting',
          'Financial Statement Analysis',
          'Management Accounting',
          'Investment Analysis',
          'Banking Operations'
       ],
        'future_scope': 'Corporate finance leadership, Investment banking, Financial consulting',
        'top_companies': [
            'Deloitte India - Mumbai, Delhi, Bengaluru',
            'PwC India - Kolkata, Mumbai, Delhi',
            'KPMG India - Mumbai, Delhi, Bengaluru',
            'EY India - Mumbai, Delhi, Bengaluru',
            'Goldman Sachs India - Bengaluru, Mumbai, Hyderabad',
            'JP Morgan India - Mumbai, Bengaluru, Hyderabad',
            'Morgan Stanley India - Mumbai, Bengaluru',
            'ICICI Bank - Mumbai, Delhi, Bengaluru',
            'HDFC Bank - Mumbai, Delhi',
            'Indian Institutes of Management (IIMs) - Across India (Ahmedabad, Bengaluru, Kolkata, Indore, Lucknow, Kozhikode, Shillong, Rohtak, Ranchi, Raipur, Tiruchirappalli, Udaipur, Nagpur, Visakhapatnam, Bodh Gaya, Amritsar, Jammu, Sirmaur, Sambalpur)',
            'Institute of Chartered Accountants of India (ICAI) - New Delhi, Mumbai, Chennai, Kolkata, Bengaluru, Hyderabad, Pune, Ahmedabad, Jaipur, Lucknow, Chandigarh',
            'Institute of Company Secretaries of India (ICSI) - New Delhi, Mumbai, Chennai, Kolkata, Bengaluru, Hyderabad, Pune, Ahmedabad'
        ],
        'education_path': 'M.Com, MBA Finance, CA Final, CS Executive, CMA Final, CFA Level 3, CPA',
        'certifications': ['CA', 'CS', 'CMA', 'CFA', 'CPA', 'FRM', 'CIMA', 'ICWA'],
        'hiring_cities': ['Mumbai', 'Delhi NCR', 'Bengaluru', 'Chennai', 'Hyderabad', 'Pune', 'Kolkata', 'Ahmedabad', 'Gurugram', 'Noida', 'Jaipur', 'Lucknow', 'Chandigarh', 'Kochi', 'Indore']
    },

    # ==================== 15. COMPUTER SCIENCE ====================
    'computer_science': {
        'name': 'Computer Science',
        'icon': '💻',
        'description': 'This stream focuses on programming, software development, algorithms, and computational theory. Students learn to build software solutions and understand computing principles.',
        'careers': ['Software Developer - Build applications', 'Web Developer - Create websites', 'Mobile App Developer - Build mobile apps', 'System Analyst - Analyze IT systems', 'Database Administrator - Manage databases', 'Network Administrator - Manage networks', 'IT Support Specialist - Provide technical support', 'Game Developer - Create video games'],
        'subjects': ['Programming', 'Data Structures', 'Algorithms', 'Database Management', 'Web Development', 'Operating Systems', 'Computer Networks'],
        'skills': ['Programming Languages', 'Problem Solving', 'Logical Thinking', 'Debugging', 'Version Control', 'Team Collaboration'],
        'software_skills': [
            '💻 Languages: Python, Java, JavaScript, C++, C#, Go, Rust, TypeScript',
            '🛠️ Frameworks: React, Angular, Vue.js, Node.js, Spring Boot, Django, Flask',
            '🗄️ Databases: MySQL, PostgreSQL, MongoDB, Firebase, Redis, Cassandra',
            '🔧 Tools: Git, Docker, Kubernetes, Jenkins, VS Code, IntelliJ',
            '☁️ Cloud: AWS, Azure, Google Cloud Platform, Heroku',
            '📱 Mobile: Android Studio, Swift, Flutter, React Native, Kotlin'
        ],
        'career_skills': [
            '💻 Problem Solving & Algorithm Design',
            '🧠 Logical Thinking & Debugging',
            '🤝 Team Collaboration & Git Workflow',
            '📈 Agile & Scrum Methodologies',
            '🔍 Attention to Detail & Code Review',
            '🔄 Continuous Learning & Adaptability'
        ],
        'technical_skills': [
          'Programming Languages (Python, Java, C++, JavaScript)',
          'Data Structures & Algorithms',
          'Database Management (SQL, MongoDB, PostgreSQL)',
          'Web Development (React, Angular, Node.js)',
          'Operating Systems & Networking',
          'Cloud Computing (AWS, Azure, GCP)',
          'DevOps (Docker, Kubernetes, Jenkins)',
          'Machine Learning & AI',
          'Cybersecurity Fundamentals',
          'Mobile App Development (Android, iOS)',
          'System Design & Architecture',
          'Version Control (Git)'
       ],
        'future_scope': 'IT industry, Software companies, Tech startups, Freelancing, Remote work',
        'top_companies': [
            'Infosys - Bengaluru, Mysore, Pune, Bhubaneswar, Hyderabad, Chennai, Thiruvananthapuram, Mangalore, Nagpur, Indore',
            'TCS - Mumbai, Chennai, Bengaluru, Hyderabad, Kolkata, Pune, Delhi NCR, Lucknow, Indore, Nagpur, Kochi, Bhubaneswar, Ahmedabad, Jaipur',
            'Wipro - Bengaluru, Chennai, Hyderabad, Pune, Kolkata, Delhi NCR, Kochi, Bhubaneswar, Nagpur, Indore',
            'HCL Technologies - Noida, Chennai, Bengaluru, Hyderabad, Pune, Lucknow, Vijayawada, Nagpur',
            'Tech Mahindra - Pune, Bengaluru, Hyderabad, Noida, Chennai, Nagpur, Kolkata, Bhubaneswar',
            'LTIMindtree - Bengaluru, Mumbai, Pune, Chennai, Hyderabad, Kolkata, Delhi NCR, Nagpur',
            'Mphasis - Bengaluru, Pune, Chennai, Indore, Hyderabad, Delhi NCR, Nagpur',
            'Persistent Systems - Pune, Nagpur, Bengaluru, Hyderabad, Goa, Kolkata, Delhi NCR',
            'Mindtree - Bengaluru, Pune, Hyderabad, Chennai, Kolkata, Bhubaneswar, Mangalore, Nagpur',
            'Hexaware Technologies - Mumbai, Chennai, Pune, Noida, Bengaluru, Dehradun, Indore',
            'Accenture India - Bengaluru, Mumbai, Pune, Hyderabad, Chennai, Kolkata, Delhi NCR, Indore, Jaipur',
            'Capgemini India - Mumbai, Pune, Bengaluru, Hyderabad, Chennai, Kolkata, Delhi NCR, Nagpur'
        ],
        'education_path': 'B.Tech CS, BCA, B.Sc CS, M.Tech CS, MCA, Diploma in CS',
        'certifications': ['Java Certification (Oracle)', 'Python Certification', 'Web Development Certification', 'Cloud Certification (AWS, Azure, GCP)', 'DevOps Certification', 'Full Stack Certification'],
        'hiring_cities': ['Bengaluru', 'Hyderabad', 'Pune', 'Chennai', 'Mumbai', 'Delhi NCR', 'Kolkata', 'Ahmedabad', 'Indore', 'Nagpur', 'Bhubaneswar', 'Kochi', 'Mysore', 'Mangalore', 'Jaipur', 'Lucknow', 'Chandigarh', 'Goa']
    },
    'computer_science_college': {
        'name': 'Computer Science (Advanced)',
        'icon': '💻',
        'description': 'Advanced study in computer science, software architecture, and emerging technologies.',
        'careers': ['Senior Software Engineer - Lead development', 'Software Architect - Design system architecture', 'Technical Lead - Guide technical teams', 'Research Scientist - Conduct CS research', 'Product Manager - Manage software products', 'DevOps Engineer - Manage deployment', 'Security Specialist - Ensure system security'],
        'subjects': ['Advanced Algorithms', 'Distributed Systems', 'Machine Learning', 'Big Data Analytics', 'Cloud Computing', 'Blockchain', 'IoT', 'Cybersecurity'],
        'skills': ['System Design', 'Architecture Planning', 'Technical Leadership', 'Research', 'Innovation', 'Project Management', 'Cloud Architecture'],
        'software_skills': [
            '💻 Advanced Languages: Go, Rust, Scala, Kotlin, TypeScript',
            '🏗️ Architecture: Microservices, Serverless, Event-driven, DDD',
            '☁️ Cloud Native: Kubernetes, Istio, Terraform, AWS CDK',
            '🤖 AI/ML: TensorFlow, PyTorch, Hugging Face, LangChain',
            '📊 Big Data: Apache Spark, Kafka, Flink, Snowflake',
            '🔒 Security: OWASP, Penetration Testing, DevSecOps'
        ],
        'career_skills': [
            '🎯 System Design & Software Architecture',
            '👥 Technical Leadership & Mentoring',
            '📊 Product Strategy & Roadmap Planning',
            '🔬 Research & Development Innovation',
            '📈 Agile Transformation & DevOps Culture',
            '🌐 Cross-functional Collaboration'
        ],
        'technical_skills': [
          'Programming Languages (Python, Java, C++, JavaScript)',
          'Data Structures & Algorithms',
          'Database Management (SQL, MongoDB, PostgreSQL)',
          'Web Development (React, Angular, Node.js)',
          'Operating Systems & Networking',
          'Cloud Computing (AWS, Azure, GCP)',
          'DevOps (Docker, Kubernetes, Jenkins)',
          'Machine Learning & AI',
          'Cybersecurity Fundamentals',
          'Mobile App Development (Android, iOS)',
          'System Design & Architecture',
          'Version Control (Git)'
       ],
        'future_scope': 'Tech leadership, Research, Specialized domains like AI/ML, Cloud architecture, Blockchain',
        'top_companies': [
            'Infosys - Bengaluru, Mysore, Pune, Hyderabad',
            'TCS - Mumbai, Chennai, Bengaluru, Hyderabad, Kolkata',
            'Wipro - Bengaluru, Hyderabad, Pune, Chennai',
            'HCL Technologies - Noida, Chennai, Bengaluru',
            'Tech Mahindra - Pune, Bengaluru, Hyderabad',
            'Microsoft India - Hyderabad, Bengaluru, Noida, Mumbai, Chennai',
            'Amazon India - Bengaluru, Hyderabad, Chennai, Delhi NCR, Pune, Mumbai',
            'Google India - Bengaluru, Hyderabad, Gurugram, Mumbai',
            'Oracle India - Bengaluru, Hyderabad, Mumbai, Noida, Pune, Chennai',
            'IBM India - Bengaluru, Pune, Hyderabad, Delhi NCR, Kolkata, Chennai, Mumbai',
            'SAP Labs India - Bengaluru, Pune, Mumbai, Gurugram, Hyderabad',
            'Intel India - Bengaluru, Hyderabad, Delhi NCR',
            'NVIDIA India - Bengaluru, Pune, Hyderabad, Mumbai',
            'Cisco India - Bengaluru, Bengaluru (ECity), Pune, Mumbai, Delhi NCR',
            'Adobe India - Bengaluru, Noida, Delhi NCR'
        ],
        'education_path': 'M.Tech CS, MS in CS, PhD in CS, Executive MBA in IT, MCA',
        'certifications': ['AWS Solutions Architect Professional', 'Google Cloud Professional Architect', 'Azure Solutions Architect Expert', 'Security+', 'CISSP', 'Certified Kubernetes Administrator (CKA)'],
        'hiring_cities': ['Bengaluru', 'Hyderabad', 'Pune', 'Chennai', 'Mumbai', 'Delhi NCR', 'Noida', 'Gurugram', 'Kolkata', 'Ahmedabad', 'Chandigarh', 'Indore', 'Nagpur']
    },

    # ==================== 16. ECONOMICS ====================
    'economics': {
        'name': 'Economics',
        'icon': '📈',
        'description': 'This stream focuses on production, distribution, and consumption of goods and services. Students learn about markets, economic policies, and financial systems.',
        'careers': ['Economist - Analyze economic trends', 'Policy Analyst - Develop economic policies', 'Financial Analyst - Analyze financial markets', 'Investment Banker - Handle investments', 'Economic Researcher - Conduct research', 'Government Advisor - Advise on economics', 'Data Analyst - Analyze economic data', 'Banking Professional - Work in banks'],
        'subjects': ['Microeconomics', 'Macroeconomics', 'Econometrics', 'International Economics', 'Development Economics', 'Public Finance', 'Monetary Economics'],
        'skills': ['Analytical Thinking', 'Statistical Analysis', 'Research Skills', 'Data Interpretation', 'Policy Analysis', 'Economic Modeling'],
        'software_skills': [
            '📊 Statistical: Stata, EViews, R, SPSS, SAS, JMP',
            '🐍 Programming: Python (Pandas, NumPy), MATLAB, Julia',
            '📈 Data Visualization: Tableau, Power BI, ggplot2, Plotly',
            '💰 Financial: Bloomberg Terminal, Reuters Eikon, FactSet',
            '📉 Econometrics: Gretl, EViews, R (plm, lmtest)',
            '🗄️ Database: SQL, Excel (Advanced), Access'
        ],
        'career_skills': [
            '📊 Analytical Thinking & Data Interpretation',
            '📈 Statistical Analysis & Econometrics',
            '📚 Research & Policy Analysis',
            '🎯 Critical Thinking & Problem Solving',
            '🗣️ Communication & Report Writing',
            '🔮 Forecasting & Economic Modeling'
        ],
        'technical_skills': [
          'Econometrics (Stata, EViews, R)',
          'Data Analysis & Visualization',
          'Macro & Microeconomic Theory',
          'Financial Modeling',
          'Policy Analysis',
          'Time Series Analysis',
          'Cost-Benefit Analysis',
          'International Trade Theory',
          'Development Economics',
          'Economic Forecasting',
          'Public Finance',
          'Statistical Software (SPSS, SAS)'
       ],
        'future_scope': 'Government agencies, Central banks, Financial institutions, Research organizations, Consulting',
        'top_companies': [
            'Reserve Bank of India (RBI) - Mumbai, Delhi, Chennai, Kolkata, Bengaluru, Hyderabad, Ahmedabad, Lucknow, Chandigarh, Kanpur, Nagpur, Patna, Jaipur, Kochi, Bhopal, Guwahati',
            'SEBI - Mumbai, Delhi, Chennai, Kolkata, Bengaluru, Hyderabad, Ahmedabad, Jaipur',
            'NITI Aayog - New Delhi',
            'Ministry of Finance - New Delhi, North Block',
            'Ministry of Commerce - New Delhi',
            'International Monetary Fund (IMF) India Office - New Delhi',
            'World Bank India Office - New Delhi, Chennai',
            'Asian Development Bank (ADB) India - New Delhi',
            'McKinsey India - Mumbai, Delhi, Bengaluru, Chennai, Gurugram',
            'Deloitte India - Mumbai, Delhi, Bengaluru, Hyderabad, Chennai, Pune, Kolkata',
            'PwC India - Kolkata, Mumbai, Delhi, Bengaluru, Hyderabad, Chennai, Pune',
            'KPMG India - Mumbai, Delhi, Bengaluru, Hyderabad, Chennai, Pune',
            'EY India - Mumbai, Delhi, Bengaluru, Hyderabad, Chennai, Kolkata, Pune',
            'CRISIL - Mumbai, Delhi, Bengaluru, Kolkata, Hyderabad, Pune, Ahmedabad',
            'ICRA Limited - Gurugram, Mumbai, Delhi, Bengaluru, Chennai, Hyderabad, Kolkata',
            'India Ratings & Research - Mumbai, Delhi, Bengaluru, Chennai, Hyderabad, Kolkata',
            'Care Ratings - Mumbai, Delhi, Chennai, Kolkata, Hyderabad, Ahmedabad'
        ],
        'education_path': 'BA Economics, B.Sc Economics, MA Economics, M.Sc Economics, PhD Economics, MBA, MPA in Economic Policy',
        'certifications': ['Economic Policy Certificate', 'Financial Analysis Certification', 'Econometrics Certification', 'Data Analysis Certification', 'RBI Grade B', 'UPSC Economics Optional'],
        'hiring_cities': ['Mumbai', 'Delhi NCR', 'Bengaluru', 'Chennai', 'Kolkata', 'Hyderabad', 'Pune', 'Ahmedabad', 'Gurugram', 'Chandigarh', 'Jaipur', 'Lucknow', 'Bhopal', 'Patna', 'Guwahati']
    },
    'economics_college': {
        'name': 'Economics (Advanced)',
        'icon': '📈',
        'description': 'Advanced study in economic theory, econometrics, and policy analysis.',
        'careers': ['Senior Economist - Lead economic analysis', 'Policy Director - Shape economic policy', 'Economic Consultant - Advise organizations', 'Central Banker - Work at central banks', 'Professor - Teach economics', 'Research Director - Lead research teams'],
        'subjects': ['Advanced Microeconomics', 'Advanced Macroeconomics', 'Advanced Econometrics', 'Game Theory', 'Behavioral Economics', 'International Trade Theory', 'Development Economics Advanced'],
        'skills': ['Advanced Statistical Analysis', 'Economic Modeling', 'Policy Evaluation', 'Research Leadership', 'Teaching', 'Consulting', 'Time Series Analysis'],
        'software_skills': [
            '📊 Advanced Stats: Stata MP, SAS/ETS, EViews Professional',
            '🐍 Advanced Programming: Python (statsmodels, linearmodels), R',
            '📈 Time Series: R (forecast, vars), EViews, Stata',
            '💻 Causal Inference: R (causalTree), Stata (teffects)',
            '📉 Machine Learning for Econ: Python (scikit-learn), R (tidymodels)',
            '📋 Policy Analysis: Vensim, AnyLogic, Stella'
        ],
        'career_skills': [
            '🎯 Advanced Economic Research',
            '📊 Causal Inference & Impact Evaluation',
            '💡 Policy Design & Implementation',
            '📈 Macroeconomic Forecasting',
            '🗣️ Stakeholder Engagement & Policy Communication',
            '👥 Research Leadership & Mentoring'
        ],
        'technical_skills': [
          'Econometrics (Stata, EViews, R)',
          'Data Analysis & Visualization',
          'Macro & Microeconomic Theory',
          'Financial Modeling',
          'Policy Analysis',
          'Time Series Analysis',
          'Cost-Benefit Analysis',
          'International Trade Theory',
          'Development Economics',
          'Economic Forecasting',
          'Public Finance',
          'Statistical Software (SPSS, SAS)'
        ],
        'future_scope': 'Central banks, International organizations, Think tanks, Academia, Economic consulting',
        'top_companies': [
            'Reserve Bank of India (RBI) - Mumbai, Delhi, Chennai, Kolkata',
            'SEBI - Mumbai, Delhi',
            'NITI Aayog - New Delhi',
            'IMF India - New Delhi',
            'World Bank India - New Delhi, Chennai',
            'Asian Development Bank - New Delhi',
            'Delhi School of Economics (DSE) - Delhi',
            'Indian Statistical Institute (ISI) - Kolkata, Delhi, Bengaluru, Chennai, Hyderabad',
            'Indian Institute of Management (IIMs) Economics Departments - Across IIMs',
            'Indian Institute of Technology (IITs) Economics Departments - Across IITs',
            'Madras School of Economics (MSE) - Chennai',
            'Gokhale Institute of Politics and Economics (GIPE) - Pune',
            'Centre for Development Studies (CDS) - Thiruvananthapuram',
            'National Institute of Public Finance and Policy (NIPFP) - New Delhi'
        ],
        'education_path': 'MA Economics, M.Sc Economics, PhD Economics, MPA in Economic Policy, M.Phil Economics',
        'certifications': ['Economic Research Fellowship (UGC-NET)', 'Policy Analysis Certification', 'Advanced Econometrics Certification', 'RBI Grade B (Economist)', 'UPSC Economics Optional'],
        'hiring_cities': ['Mumbai', 'Delhi NCR', 'Bengaluru', 'Chennai', 'Kolkata', 'Hyderabad', 'Pune', 'Ahmedabad', 'Thiruvananthapuram', 'Chandigarh']
    },

    # ==================== 17. PSYCHOLOGY ====================
    'psychology': {
        'name': 'Psychology',
        'icon': '🧠',
        'description': 'This stream focuses on human mind, behavior, emotions, and mental processes. Students learn about psychological theories, research methods, and therapeutic techniques.',
        'careers': ['Clinical Psychologist - Treat mental health issues', 'Counseling Psychologist - Provide therapy', 'School Psychologist - Help students', 'Industrial Psychologist - Improve workplace', 'Research Psychologist - Conduct research', 'Neuropsychologist - Study brain-behavior', 'Forensic Psychologist - Work in legal system', 'Sports Psychologist - Help athletes'],
        'subjects': ['General Psychology', 'Abnormal Psychology', 'Developmental Psychology', 'Social Psychology', 'Cognitive Psychology', 'Research Methods', 'Statistics', 'Clinical Psychology'],
        'skills': ['Empathy', 'Active Listening', 'Communication', 'Critical Thinking', 'Observation', 'Ethical Judgment', 'Patience', 'Therapeutic Skills'],
        'software_skills': [
            '📊 Statistical: SPSS, R, JASP, Jamovi, Stata',
            '📋 Assessment Tools: Q-interactive, PARiConnect, MHS Assessments',
            '🏥 Therapy Platforms: SimplePractice, TheraNest, TherapyNotes',
            '📈 Data Analysis: Excel, Python, Qualtrics, PsychoPy',
            '📚 Literature Review: PsycINFO, PubMed, Google Scholar',
            '📝 Report Writing: Microsoft Word, LaTeX, Overleaf'
        ],
        'career_skills': [
            '🧠 Empathy & Active Listening',
            '🗣️ Communication & Counseling Skills',
            '🔍 Critical Thinking & Psychological Assessment',
            '📊 Observation & Diagnostic Skills',
            '⚖️ Ethical Judgment & Confidentiality',
            '💪 Patience & Emotional Resilience'
        ],
        'technical_skills': [
          'Psychological Assessment (WAIS, Rorschach)',
          'Therapeutic Techniques (CBT, REBT, DBT)',
          'Research Methodology',
          'Statistical Analysis (SPSS)',
          'Clinical Interviewing',
          'Developmental Psychology Knowledge',
          'Neuropsychological Assessment',
          'Counseling Techniques',
          'Behavioral Observation',
          'Psychometric Testing',
          'Case Formulation',
          'Ethical Guidelines (RCI)'
       ],
        'future_scope': 'Hospitals, Schools, Corporate sector, Research institutions, Private practice, Rehabilitation centers',
        'top_companies': [
            'NIMHANS - Bengaluru',
            'AIIMS - New Delhi, Jodhpur, Bhopal, Bhubaneswar, Patna, Raipur, Rishikesh, Nagpur, Bathinda',
            'Fortis Healthcare - Delhi NCR, Bengaluru, Mumbai, Chennai, Kolkata, Jaipur, Mohali, Lucknow',
            'Apollo Hospitals - Chennai, Delhi, Hyderabad, Bengaluru, Mumbai, Kolkata, Ahmedabad, Pune, Lucknow, Bhubaneswar',
            'Max Healthcare - Delhi NCR, Punjab, Uttarakhand, Mumbai',
            'Manipal Hospitals - Bengaluru, Delhi, Pune, Jaipur, Vijayawada, Goa',
            'Narayana Health - Bengaluru, Kolkata, Mumbai, Delhi NCR, Ahmedabad, Raipur, Jaipur',
            'Tata Motors (Industrial Psychologist) - Pune, Mumbai, Jamshedpur, Lucknow, Sanand',
            'Infosys (Organizational Psychology) - Bengaluru, Pune, Hyderabad, Chennai, Mysore, Mangalore',
            'TCS (HR Psychology) - Mumbai, Chennai, Bengaluru, Hyderabad, Kolkata, Pune',
            'Wipro (Organizational Psychology) - Bengaluru, Hyderabad, Pune, Chennai, Kolkata',
            'ITC Limited (HR Psychology) - Kolkata, Bengaluru, Gurugram, Chennai, Hyderabad',
            'Hindustan Unilever (Industrial Psychology) - Mumbai, Bengaluru, Kolkata, Delhi NCR, Chennai, Pune',
            'Rehabilitation Council of India (RCI) - New Delhi',
            'Indian Psychiatric Society (IPS) - Mumbai (Registered Office)'
        ],
        'education_path': 'BA Psychology, B.Sc Psychology, MA Psychology, M.Sc Psychology, PhD Psychology, M.Phil Clinical Psychology',
        'certifications': ['Licensed Psychologist (RCI Registration)', 'Therapy Certification (CBT, REBT, DBT)', 'Counseling Certification', 'Rehabilitation Certification', 'Psychometric Testing Certification'],
        'hiring_cities': ['Bengaluru', 'Delhi NCR', 'Mumbai', 'Chennai', 'Hyderabad', 'Pune', 'Kolkata', 'Ahmedabad', 'Jaipur', 'Lucknow', 'Chandigarh', 'Bhubaneswar', 'Goa', 'Mysore', 'Mangalore']
    },
    'psychology_college': {
        'name': 'Psychology (Advanced)',
        'icon': '🧠',
        'description': 'Advanced study in psychological theories, clinical practice, and research methodology.',
        'careers': ['Clinical Psychologist Specialist - Treat complex cases', 'Psychiatry Consultant - Work with psychiatrists', 'Psychology Professor - Teach psychology', 'Research Director - Lead research', 'Organizational Psychologist - Improve organizations', 'Neuropsychologist - Study brain disorders'],
        'subjects': ['Advanced Clinical Psychology', 'Cognitive Neuroscience', 'Psychopathology Advanced', 'Psychological Assessment', 'Therapeutic Techniques Advanced', 'Research Design Advanced', 'Neuropsychology'],
        'skills': ['Advanced Clinical Skills', 'Diagnostic Assessment (DSM, ICD)', 'Therapeutic Techniques (CBT, REBT, DBT, ACT)', 'Research Leadership', 'Teaching', 'Supervision', 'Psychometric Assessment'],
        'software_skills': [
            '📊 Advanced Stats: R (lme4, brms), Mplus, AMOS, Lisrel',
            '🧠 Neuroimaging: FSL, SPM, AFNI, BrainVoyager',
            '📋 Advanced Assessment: Q-global, PARiConnect Pro',
            '💻 Research: PsychoPy, OpenSesame, E-Prime, Gorilla',
            '📈 Advanced Data: Python (pandas, seaborn), R Shiny',
            '📚 Systematic Review: Covidence, Rayyan, RevMan'
        ],
        'career_skills': [
            '🎯 Advanced Clinical Diagnosis & Treatment',
            '🧠 Neuropsychology & Cognitive Assessment',
            '📊 Research Leadership & Grant Writing',
            '💡 Therapeutic Innovation & Evidence-based Practice',
            '👥 Supervision & Clinical Training',
            '📚 Academic Teaching & Curriculum Development'
        ],
        'technical_skills': [
          'Psychological Assessment (WAIS, Rorschach)',
          'Therapeutic Techniques (CBT, REBT, DBT)',
          'Research Methodology',
          'Statistical Analysis (SPSS)',
          'Clinical Interviewing',
          'Developmental Psychology Knowledge',
          'Neuropsychological Assessment',
          'Counseling Techniques',
          'Behavioral Observation',
          'Psychometric Testing',
          'Case Formulation',
          'Ethical Guidelines (RCI)'
       ],
        'future_scope': 'Clinical practice, Research institutions, Academia, Corporate consulting, Rehabilitation',
        'top_companies': [
            'NIMHANS - Bengaluru',
            'AIIMS - New Delhi, Jodhpur, Bhopal, Bhubaneswar, Patna, Raipur, Rishikesh, Nagpur, Bathinda',
            'Fortis Healthcare - Delhi NCR, Bengaluru, Mumbai',
            'Apollo Hospitals - Chennai, Hyderabad, Delhi, Bengaluru',
            'Manipal Hospitals - Bengaluru, Delhi, Pune',
            'National Institute of Mental Health and Neuro Sciences (NIMHANS) - Bengaluru',
            'Central Institute of Psychiatry (CIP) - Ranchi',
            'Institute of Human Behaviour and Allied Sciences (IHBAS) - Delhi',
            'PGIMER - Chandigarh',
            'JIPMER - Puducherry',
            'Indian Institute of Psychology - Hyderabad',
            'Tata Institute of Social Sciences (TISS) - Mumbai, Chennai, Hyderabad, Guwahati'
        ],
        'education_path': 'M.Phil Clinical Psychology, PhD Psychology, PsyD, Post-doctoral fellowship, RCI Registration',
        'certifications': ['Licensed Clinical Psychologist (RCI)', 'CBT Practitioner Certification', 'REBT Certification', 'Neuropsychology Certification', 'Psychometric Assessment Specialist', 'M.Phil Clinical Psychology Degree'],
        'hiring_cities': ['Bengaluru', 'Delhi NCR', 'Mumbai', 'Chennai', 'Hyderabad', 'Pune', 'Kolkata', 'Ranchi', 'Chandigarh', 'Puducherry', 'Ahmedabad', 'Jaipur']
    },

    # ==================== 18. SOCIAL WORK ====================
    'social_work': {
        'name': 'Social Work',
        'icon': '🤝',
        'description': 'This stream focuses on helping individuals, families, and communities. Students learn about social welfare, community development, and counseling techniques.',
        'careers': ['Social Worker - Help individuals and families', 'Community Organizer - Develop community programs', 'Child Welfare Specialist - Protect children', 'Medical Social Worker - Work in hospitals', 'School Social Worker - Help students', 'Mental Health Counselor - Provide therapy', 'NGO Manager - Manage non-profits', 'Policy Advocate - Influence social policies'],
        'subjects': ['Social Welfare', 'Community Development', 'Counseling Skills', 'Human Behavior', 'Social Policy', 'Research Methods', 'Crisis Intervention', 'Social Justice'],
        'skills': ['Empathy', 'Communication', 'Problem Solving', 'Crisis Management', 'Advocacy', 'Cultural Competence', 'Case Management', 'Community Organizing'],
        'software_skills': [
            '🤝 Case Management: Apricot, ETO Software, CaseWorthy',
            '📊 Client Management: Salesforce Nonprofit Cloud, DonorPerfect',
            '📈 Data Analysis: Excel, SPSS, R, Tableau for Nonprofits',
            '📝 Grant Writing: GrantHub, Fluxx, Instrumentl, Foundant',
            '🗣️ Communication: Zoom, Slack, Microsoft Teams, WhatsApp Business',
            '📋 Documentation: Microsoft Office, Google Workspace, DocuSign'
        ],
        'career_skills': [
            '💝 Empathy & Compassion',
            '🗣️ Communication & Active Listening',
            '🎯 Problem Solving & Crisis Management',
            '🤝 Advocacy & Community Organizing',
            '🌍 Cultural Competence & Sensitivity',
            '📋 Case Management & Documentation'
        ],
        'technical_skills': [
          'Case Management & Documentation',
          'Community Needs Assessment',
          'Crisis Intervention Techniques',
          'Counseling & Guidance',
          'Social Welfare Policy Knowledge',
          'Referral & Resource Navigation',
          'Advocacy Skills',
          'Program Planning & Evaluation',
          'Rehabilitation Techniques',
          'Child Protection Procedures',
          'Disaster Response & Management',
          'NGO Management'
       ],
        'future_scope': 'NGOs, Government welfare departments, Hospitals, Schools, Community centers, International organizations',
        'top_companies': [
            'UNICEF India - New Delhi, Mumbai, Chennai, Kolkata, Hyderabad, Lucknow, Bhopal, Guwahati, Patna, Bhubaneswar, Ranchi, Jaipur',
            'Save the Children India - Delhi, Mumbai, Bengaluru, Hyderabad, Kolkata, Chennai, Lucknow, Jaipur, Bhopal, Patna',
            'CRY (Child Rights and You) - Bengaluru, Mumbai, Delhi, Kolkata, Chennai, Hyderabad, Pune, Ahmedabad, Lucknow, Bhubaneswar',
            'Goonj - Delhi NCR, Bengaluru, Mumbai, Kolkata, Chennai, Hyderabad, Pune, Nagpur, Jaipur, Lucknow',
            'Pratham Education Foundation - Mumbai, Delhi, Bengaluru, Kolkata, Chennai, Hyderabad, Pune, Ahmedabad, Jaipur, Lucknow, Patna, Ranchi',
            'Akshaya Patra Foundation - Bengaluru, Delhi, Jaipur, Vrindavan, Pune, Ahmedabad, Hyderabad, Lucknow, Bhubaneswar, Vizag, Guwahati, Kolkata, Chennai, Mumbai',
            'HelpAge India - Delhi, Mumbai, Bengaluru, Chennai, Kolkata, Hyderabad, Pune, Ahmedabad, Jaipur, Lucknow, Bhubaneswar, Patna',
            'Smile Foundation - Delhi NCR, Mumbai, Bengaluru, Chennai, Kolkata, Hyderabad, Pune, Ahmedabad, Lucknow, Bhopal, Ranchi',
            'Tata Institute of Social Sciences (TISS) Field Work - Mumbai, Chennai, Hyderabad, Guwahati, Tuljapur, Guwahati (Field placements across India)',
            'Delhi School of Social Work - Delhi NCR',
            'Karuna Trust - Bengaluru, Delhi, Mumbai',
            'M.S. Swaminathan Research Foundation - Chennai, Delhi, Hyderabad, Bhubaneswar, Jaipur',
            'Sewa Bharat - Delhi NCR, Mumbai, Bengaluru, Chennai, Kolkata, Hyderabad, Ahmedabad, Jaipur, Lucknow',
            'Sulabh International - Delhi NCR, Across India',
            'Childline India Foundation - Mumbai, Across All Major Cities (1098 service)'
        ],
        'education_path': 'BSW (Bachelor of Social Work), MSW (Master of Social Work), PhD Social Work, Diploma in Social Work',
        'certifications': ['Licensed Social Worker', 'Counseling Certification', 'Crisis Intervention Certification', 'Child Protection Certification', 'NGO Management Certification', 'Community Development Certification'],
        'hiring_cities': ['Delhi NCR', 'Mumbai', 'Bengaluru', 'Chennai', 'Kolkata', 'Hyderabad', 'Pune', 'Ahmedabad', 'Jaipur', 'Lucknow', 'Bhubaneswar', 'Patna', 'Ranchi', 'Bhopal', 'Guwahati', 'Chandigarh', 'Nagpur', 'Kochi', 'Vizag']
    },
    'social_work_college': {
        'name': 'Social Work (Advanced)',
        'icon': '🤝',
        'description': 'Advanced study in social welfare, community development, and social policy analysis.',
        'careers': ['Senior Social Worker - Lead case management', 'Program Director - Manage social programs', 'Social Policy Analyst - Analyze policies', 'NGO Director - Lead non-profits', 'Social Work Professor - Teach social work', 'Clinical Social Worker - Provide advanced therapy'],
        'subjects': ['Advanced Social Policy', 'Program Evaluation', 'Community Organization Advanced', 'Clinical Social Work', 'Social Justice Advanced', 'International Social Work', 'Disaster Management'],
        'skills': ['Advanced Case Management', 'Program Development', 'Policy Analysis', 'Leadership', 'Grant Writing', 'Supervision', 'Advocacy Skills', 'Research Methodology'],
        'software_skills': [
            '🤝 Advanced Case Management: Social Solutions Apricot, ETO',
            '📊 M&E Software: ActivityInfo, DHIS2, TolaData',
            '📈 Program Evaluation: SPSS, R, Stata, NVivo',
            '💰 Grant Management: Fluxx, Submittable, Foundant GLM',
            '🗣️ Stakeholder Engagement: Miro, MURAL, Asana, Trello',
            '📋 Policy Analysis: Vensim, STELLA, Qualitative Data Analysis'
        ],
        'career_skills': [
            '🎯 Strategic Program Development',
            '📊 Policy Analysis & Advocacy',
            '💡 Leadership & Organizational Management',
            '💰 Grant Writing & Fundraising',
            '👥 Supervision & Team Development',
            '🌍 International Development & Human Rights'
        ],
        'technical_skills': [
          'Case Management & Documentation',
          'Community Needs Assessment',
          'Crisis Intervention Techniques',
          'Counseling & Guidance',
          'Social Welfare Policy Knowledge',
          'Referral & Resource Navigation',
          'Advocacy Skills',
          'Program Planning & Evaluation',
          'Rehabilitation Techniques',
          'Child Protection Procedures',
          'Disaster Response & Management',
          'NGO Management'
       ],
        'future_scope': 'NGO leadership, Policy making, Clinical practice, Academia, International development, Social entrepreneurship',
        'top_companies': [
            'Tata Institute of Social Sciences (TISS) - Mumbai, Chennai, Hyderabad, Guwahati, Tuljapur',
            'UNICEF India - New Delhi, All State Capitals',
            'CRY - Bengaluru, Mumbai, Delhi, Kolkata, Chennai',
            'Goonj - Delhi NCR, Bengaluru, Mumbai',
            'Pratham - Mumbai, Delhi, Bengaluru, Kolkata, Chennai',
            'Jamia Millia Islamia (Dept of Social Work) - Delhi',
            'University of Delhi (Dept of Social Work) - Delhi',
            'Loyola College of Social Sciences - Thiruvananthapuram',
            'Madras School of Social Work - Chennai',
            'Nirmala Niketan College of Social Work - Mumbai',
            'Roshni Nilaya School of Social Work - Mangalore',
            'National Institute of Social Work and Social Sciences (NISWASS) - Bhubaneswar'
        ],
        'education_path': 'MSW, PhD Social Work, M.Phil, Post-graduate diploma in specialized areas (PG Diploma in Social Work, PG Diploma in Counseling, PG Diploma in NGO Management)',
        'certifications': ['Licensed Clinical Social Worker', 'Program Evaluation Certification', 'Grant Writing Certification', 'Policy Analysis Certification', 'UGC-NET for Social Work', 'Clinical Social Work Supervision'],
        'hiring_cities': ['Mumbai', 'Delhi NCR', 'Bengaluru', 'Chennai', 'Kolkata', 'Hyderabad', 'Pune', 'Ahmedabad', 'Jaipur', 'Lucknow', 'Bhubaneswar', 'Patna', 'Ranchi', 'Bhopal', 'Guwahati', 'Chandigarh', 'Nagpur', 'Kochi', 'Thiruvananthapuram', 'Mangalore']
    },
         # ==================== 19. TRANSPORTATION & MOBILITY ====================
    'transportation': {
        'name': 'Transportation & Mobility',
        'icon': '🚗',
        'description': 'This dynamic stream focuses on transportation systems, logistics, supply chain management, urban mobility, and emerging technologies like electric vehicles and autonomous transport.',
        'careers': ['Logistics Manager - Oversee supply chain and transportation operations', 'Supply Chain Analyst - Optimize supply chain efficiency', 'Transportation Planner - Design urban transport systems', 'Fleet Manager - Manage vehicle fleets and operations', 'Warehouse Manager - Oversee storage and distribution', 'EV (Electric Vehicle) Engineer - Develop electric mobility solutions', 'Rail Transport Manager - Manage railway operations', 'Airport Operations Manager - Oversee airport ground operations', 'Port/Harbor Manager - Manage maritime logistics', 'Last-Mile Delivery Specialist - Optimize final delivery operations', 'Urban Mobility Planner - Design sustainable city transport', 'Autonomous Vehicle Engineer - Develop self-driving technology'],
        'subjects': ['Logistics & Supply Chain Management', 'Transportation Engineering', 'Urban Planning', 'Operations Research', 'Inventory Management', 'Warehouse Management', 'Fleet Management', 'Electric Vehicle Technology', 'Sustainable Transportation', 'Transport Economics', 'GPS & GIS Systems', 'Route Optimization'],
        'skills': ['Supply Chain Optimization', 'Data Analytics', 'Route Planning', 'Inventory Control', 'Transportation Management Systems (TMS)', 'Warehouse Management Systems (WMS)', 'Problem Solving', 'Analytical Thinking', 'Project Management', 'Communication Skills', 'Cost Optimization', 'Vendor Management', 'Regulatory Compliance'],
        'software_skills': [
            '🚚 TMS: SAP TM, Oracle Transportation Management, Manhattan TMS',
            '📦 WMS: SAP EWM, Oracle WMS, Manhattan WMS, HighJump',
            '🗺️ Route Planning: Locus, FarEye, Routematic, OptimoRoute',
            '📊 Supply Chain Analytics: Kinaxis, Blue Yonder, LLamasoft',
            '🚗 Fleet Management: Fleetroot, TrackoBit, LocoNav, GPS Insight',
            '📈 Data Analytics: Tableau, Power BI, Python, SQL'
        ],
        'career_skills': [
            '🚚 Supply Chain Optimization & Strategy',
            '📊 Data Analytics & Demand Forecasting',
            '🗺️ Route Planning & Logistics Coordination',
            '👥 Team Leadership & Vendor Management',
            '💰 Cost Optimization & Budget Management',
            '📋 Regulatory Compliance & Safety Standards'
        ],
        'technical_skills': [
          'Supply Chain Management (SCM) Systems',
          'Transportation Management Software (TMS)',
          'Warehouse Management Systems (WMS)',
          'Route Optimization Algorithms',
          'GPS Tracking & Telematics',
          'Electric Vehicle Technology',
          'Battery Management Systems',
          'Fleet Management Software',
          'Data Analytics (Python, SQL, Tableau)',
          'GIS & Spatial Analysis',
          'Inventory Optimization Tools',
          'Autonomous Vehicle Technology'
       ],
        'future_scope': 'Growing e-commerce, EV revolution, government initiatives (National Logistics Policy, Bharatmala, Sagarmala, Dedicated Freight Corridors, Electric Vehicle Policy), last-mile delivery boom, urban metro expansion',
        'top_companies': [
            'Logistics & Supply Chain: Delhivery - Gurugram, Bengaluru, Mumbai, Delhi, Hyderabad, Chennai, Kolkata, Pune, Ahmedabad',
            'Blue Dart - Mumbai, Delhi, Bengaluru, Chennai, Hyderabad, Kolkata, Pune, Ahmedabad',
            'DTDC - Bengaluru, Mumbai, Delhi, Chennai, Kolkata, Hyderabad, Pune, Ahmedabad',
            'Amazon Logistics - Bengaluru, Hyderabad, Delhi, Mumbai, Chennai, Kolkata, Pune, Ahmedabad',
            'Flipkart Ekart - Bengaluru, Delhi, Mumbai, Chennai, Hyderabad, Kolkata, Pune, Ahmedabad',
            'Rivigo - Gurugram, Delhi, Bengaluru, Mumbai, Pune, Hyderabad, Chennai, Kolkata',
            'Mahindra Logistics - Mumbai, Pune, Chennai, Delhi, Bengaluru, Hyderabad, Kolkata',
            'Container Corporation of India (CONCOR) - Delhi, Mumbai, Chennai, Kolkata, Hyderabad, Ahmedabad, Bengaluru',
            'Adani Logistics - Ahmedabad, Mundra, Mumbai, Delhi, Chennai, Hyderabad, Vizag',
            'EV & Automotive: Tata Motors EV Division - Pune, Mumbai, Sanand, Jamshedpur',
            'Mahindra Electric - Bengaluru, Mumbai, Pune, Chennai, Delhi',
            'Ola Electric - Bengaluru, Chennai, Pune, Delhi, Mumbai, Hyderabad',
            'Ather Energy - Bengaluru, Chennai, Delhi, Mumbai, Pune, Hyderabad, Ahmedabad',
            'Rail & Metro: Indian Railways - All State Capitals, Divisional Headquarters across India',
            'Delhi Metro Rail Corporation (DMRC) - Delhi NCR, Meerut',
            'Mumbai Metro - Mumbai, Thane',
            'Bengaluru Metro (BMRCL) - Bengaluru',
            'Chennai Metro - Chennai',
            'Hyderabad Metro - Hyderabad',
            'Airport & Aviation: GMR Airports - Delhi, Hyderabad, Goa',
            'Adani Airports - Mumbai, Ahmedabad, Lucknow, Mangaluru, Jaipur, Guwahati, Thiruvananthapuram',
            'Bangalore International Airport Limited (BIAL) - Bengaluru',
            'Airports Authority of India (AAI) - Across India',
            'Ports & Shipping: Adani Ports & SEZ - Mundra, Hazira, Dahej, Vizag, Chennai',
            'Jawaharlal Nehru Port Trust (JNPT) - Navi Mumbai',
            'Chennai Port Trust - Chennai',
            'Kolkata Port Trust - Kolkata, Haldia'
        ],
        'education_path': 'B.Tech in Transportation Engineering, B.Tech in Mechanical/Automobile Engineering, BBA in Logistics & Supply Chain Management, MBA in Supply Chain Management, Diploma in Logistics, B.Sc in Transportation Management',
        'certifications': ['Certified Supply Chain Professional (CSCP)', 'Certified in Logistics, Transportation and Distribution (CLTD)', 'Six Sigma Green/Black Belt', 'Lean Supply Chain Certification', 'SAP Transportation Management (TM)', 'Fleet Management Certification', 'EV Technology Certification', 'Project Management Professional (PMP)'],
        'hiring_cities': ['Mumbai', 'Delhi NCR', 'Bengaluru', 'Chennai', 'Hyderabad', 'Pune', 'Ahmedabad', 'Kolkata', 'Gurugram', 'Jaipur', 'Lucknow', 'Chandigarh', 'Visakhapatnam', 'Kochi', 'Coimbatore']
    },
    'transportation_college': {
        'name': 'Transportation & Mobility (Advanced)',
        'icon': '🚗',
        'description': 'Advanced study in transportation systems, logistics optimization, electric mobility, autonomous vehicles, and intelligent transport systems. Prepare for leadership roles in supply chain, urban planning, and sustainable mobility solutions.',
        'careers': ['Supply Chain Director - Lead global supply chain operations', 'Logistics Vice President - Oversee logistics strategy', 'Transportation Consultant - Advise on mobility solutions', 'EV Fleet Manager - Manage electric fleet operations', 'Urban Mobility Director - Design city transport systems', 'Autonomous Vehicle Engineer - Develop self-driving tech', 'Railway Operations Director - Manage rail networks', 'Aviation Logistics Head - Lead air cargo operations', 'Port Authority Director - Manage port operations', 'Sustainable Mobility Specialist - Drive green transport initiatives', 'Transportation Data Scientist - Analyze mobility patterns', 'Smart City Transport Planner - Design intelligent transport systems'],
        'subjects': ['Advanced Supply Chain Management', 'Transportation Economics', 'Urban & Regional Planning', 'Intelligent Transport Systems (ITS)', 'Electric Vehicle Engineering', 'Autonomous Vehicle Technology', 'Transportation Data Analytics', 'Multi-modal Logistics', 'Port & Terminal Management', 'Air Cargo Management', 'Railway Operations Management', 'Sustainable Mobility', 'Geographic Information Systems (GIS)', 'Transportation Safety & Security'],
        'skills': ['Strategic Supply Chain Planning', 'Advanced Data Analytics (Python, R, SQL)', 'Transportation Modeling & Simulation', 'GIS & Spatial Analysis', 'Fleet Optimization', 'Cost-Benefit Analysis', 'Sustainability Assessment', 'Project Portfolio Management', 'Change Management', 'Stakeholder Management', 'International Logistics', 'Customs & Compliance (EXIM)', 'Risk Management'],
        'software_skills': [
            '🚚 Advanced TMS: SAP TM Advanced, Oracle OTM Cloud, Blue Yonder TMS',
            '📊 Supply Chain Analytics: Kinaxis RapidResponse, Llamasoft Supply Chain Guru',
            '🤖 Autonomous Vehicle Tech: ROS (Robot Operating System), CARLA Simulator, Apollo Auto',
            '🚗 EV Simulation: AVL Cruise, GT-Suite, Simcenter Amesim',
            '🗺️ GIS Advanced: ArcGIS Pro, QGIS, MapInfo Professional',
            '📈 Transportation Modeling: PTV Vissim, Aimsun, TransCAD, Cube Voyager'
        ],
        'career_skills': [
            '🎯 Strategic Supply Chain Transformation',
            '📊 Advanced Data Analytics & AI in Logistics',
            '🤖 Autonomous & Electric Vehicle Innovation',
            '🌍 Global Trade & Cross-border Logistics',
            '💡 Smart City & Sustainable Mobility Planning',
            '👥 C-level Stakeholder Management'
        ],
        'technical_skills': [
          'Supply Chain Management (SCM) Systems',
          'Transportation Management Software (TMS)',
          'Warehouse Management Systems (WMS)',
          'Route Optimization Algorithms',
          'GPS Tracking & Telematics',
          'Electric Vehicle Technology',
          'Battery Management Systems',
          'Fleet Management Software',
          'Data Analytics (Python, SQL, Tableau)',
          'GIS & Spatial Analysis',
          'Inventory Optimization Tools',
          'Autonomous Vehicle Technology'
       ],
        'future_scope': 'Global supply chain restructuring, EV revolution (30% by 2030 target), Hyperloop projects, Urban Air Mobility (flying taxis), Autonomous vehicles, Drone deliveries, High-speed rail corridors, Smart city mobility',
        'top_companies': [
            'Supply Chain Leadership: Delhivery - Gurugram/Bengaluru', 'Blue Dart - Mumbai', 'Amazon Logistics - Bengaluru/Hyderabad', 'Flipkart Logistics - Bengaluru', 'Rivigo - Gurugram',
            'EV Leadership: Ola Electric - Bengaluru', 'Tata Motors EV - Pune', 'Mahindra Electric - Bengaluru', 'Ather Energy - Bengaluru', 'Bajaj Auto EV - Pune',
            'Infrastructure: Indian Railways (Rail Bhawan) - Delhi', 'NHAI - Delhi', 'DMRC - Delhi', 'Mumbai Metro - Mumbai', 'Adani Ports - Ahmedabad',
            'Consulting: McKinsey Mobility - Mumbai/Delhi', 'BCG Transport - Mumbai/Delhi', 'Deloitte Supply Chain - Mumbai/Delhi/Bengaluru', 'PwC Logistics - Kolkata/Mumbai/Delhi', 'KPMG Transport - Mumbai/Delhi/Bengaluru', 'EY Mobility - Mumbai/Delhi/Bengaluru',
            'Public Sector: NITI Aayog (Transport vertical) - Delhi', 'Ministry of Road Transport & Highways - Delhi', 'Ministry of Railways - Delhi', 'Ministry of Ports, Shipping & Waterways - Delhi'
        ],
        'education_path': 'M.Tech in Transportation Engineering, MBA in Supply Chain Management, M.Sc in Logistics & Supply Chain, PhD in Transportation Planning, Executive MBA in Logistics, PG Diploma in Port Management, PG Diploma in Aviation Management',
        'certifications': ['Certified Supply Chain Professional (CSCP) - APICS', 'Certified in Logistics, Transportation and Distribution (CLTD) - APICS', 'Six Sigma Black Belt', 'Lean Master Certification', 'Project Management Professional (PMP)', 'SAP TM Certified Professional', 'Certified EV Engineer'],
        'hiring_cities': ['Mumbai', 'Delhi NCR', 'Bengaluru', 'Pune', 'Chennai', 'Hyderabad', 'Ahmedabad', 'Gurugram', 'Kolkata', 'Visakhapatnam', 'Kochi', 'Chandigarh']
    },

    # ==================== 20. SERVICE, HOSPITALITY & PUBLIC SAFETY ====================
    'service_hospitality': {
        'name': 'Service, Hospitality & Public Safety',
        'icon': '🏨',
        'description': 'This dynamic stream focuses on customer service, hotel management, tourism, event planning, and public safety services including police, fire, emergency response, and disaster management.',
        'careers': ['Hotel Manager - Oversee hotel operations and guest services', 'Restaurant Manager - Manage food and beverage operations', 'Event Manager - Plan and execute events', 'Tourism Officer - Promote travel and tourism', 'Customer Service Manager - Lead customer support teams', 'Police Officer - Maintain law and order', 'Firefighter - Respond to fire emergencies', 'Emergency Medical Technician (EMT) - Provide emergency medical care', 'Disaster Management Specialist - Coordinate disaster response', 'Security Manager - Manage security operations', 'Airport Customer Service - Handle passenger services', 'Resort Manager - Manage resort operations'],
        'subjects': ['Hotel Management', 'Food & Beverage Management', 'Tourism Management', 'Event Planning', 'Customer Relationship Management', 'Public Safety Administration', 'Emergency Response', 'Disaster Management', 'Fire Safety', 'Security Management', 'Front Office Operations', 'Housekeeping Management', 'Culinary Arts', 'Crisis Communication'],
        'skills': ['Customer Service Excellence', 'Communication (Multiple Languages)', 'Leadership & Team Management', 'Problem Solving', 'Crisis Management', 'Attention to Detail', 'Time Management', 'Stress Management', 'Conflict Resolution', 'Emergency Response', 'First Aid & CPR', 'Fire Safety Protocols', 'Budget Management', 'Sales & Marketing', 'Event Planning', 'Risk Assessment'],
        'software_skills': [
            '🏨 PMS: Opera PMS, IDS WinHms, Hotelogix, Oracle Hospitality',
            '🍽️ POS: Micros Simphony, Toast, Square, Zoho POS',
            '📊 CRS: SiteMinder, TravelClick, RateGain',
            '🎫 Event Management: Cvent, Eventbrite, Planning Pod, Zoho Backstage',
            '🗣️ Customer Service: Zendesk, Freshdesk, ServiceNow, Salesforce Service Cloud',
            '🚨 Emergency Management: WebEOC, E-Team, Veoci, D4H'
        ],
        'career_skills': [
            '🏨 Guest Relations & Service Excellence',
            '🗣️ Multilingual Communication',
            '👥 Team Leadership & Staff Management',
            '🚨 Crisis Management & Emergency Response',
            '📊 Revenue Management & Cost Control',
            '🎯 Attention to Detail & Quality Assurance'
        ],
        'technical_skills': [
          'Property Management Systems (PMS - Opera, IDS, WinHms)',
          'Point of Sale (POS) Systems',
          'Security Systems (CCTV, Access Control)',
          'Emergency Response Equipment',
          'Fire Safety Equipment',
          'Communication Systems',
          'Reservation Systems (CRS, GDS)',
          'Event Management Software',
          'Customer Relationship Management (CRM)',
          'Hotel Accounting Software',
          'Inventory Management Systems',
          'Tourism Management Systems'
       ],
        'future_scope': 'Growing tourism industry (Incredible India campaign), hotel chain expansion (Taj, Oberoi, Marriott, Hyatt, ITC), IRCTC tourism, event management boom, medical tourism, spiritual tourism, food delivery and cloud kitchens, public safety modernization',
        'top_companies': [
            'Hotel Chains: Taj Hotels (IHCL) - Mumbai, Delhi, Bengaluru, Chennai, Kolkata, Hyderabad, Goa, Jaipur',
            'Oberoi Hotels - Delhi, Mumbai, Bengaluru, Udaipur, Jaipur, Agra',
            'ITC Hotels - Delhi, Mumbai, Bengaluru, Chennai, Kolkata, Hyderabad, Ahmedabad, Jaipur',
            'Marriott International India - Delhi, Mumbai, Bengaluru, Chennai, Hyderabad, Pune, Kolkata, Goa',
            'Hyatt India - Delhi, Mumbai, Bengaluru, Chennai, Hyderabad, Pune, Goa, Jaipur',
            'Restaurants: Dominos India - Across 1,350+ cities', 'McDonalds India - Across major cities',
            'Starbucks India - Across 350+ stores in 50+ cities', 'Cafe Coffee Day - Across 400+ cities',
            'Tourism: IRCTC - Delhi, All State Capitals', 'MakeMyTrip - Gurugram, Bengaluru, Mumbai, Delhi',
            'Yatra.com - Gurugram, Mumbai, Bengaluru, Delhi', 'Thomas Cook India - Mumbai, Delhi, Bengaluru, Chennai',
            'Event Management: Wizcraft International - Mumbai, Delhi, Bengaluru',
            'Percept - Mumbai, Delhi, Bengaluru, Pune, Chennai', 'Cineyug - Mumbai, Delhi, Bengaluru',
            'Customer Service: Teleperformance India - Across 30+ cities', 'Concentrix India - Across 20+ cities',
            'Tech Mahindra BPO - Pune, Bengaluru, Hyderabad, Noida', 'Wipro BPO - Bengaluru, Hyderabad, Pune, Chennai',
            'Public Safety: Indian Police Service (IPS) - All State Capitals', 'Mumbai Police - Mumbai',
            'Delhi Police - Delhi NCR', 'National Disaster Response Force (NDRF) - Delhi',
            'Securitas India - Across 30+ cities', 'G4S India - Across 40+ cities'
        ],
        'education_path': 'BBA in Hotel Management, B.Sc in Hospitality & Hotel Management, BHMCT, MBA in Hospitality, Diploma in Hotel Management, BBA in Event Management, BA in Tourism Management, B.Sc in Public Safety, Diploma in Fire Safety, Certificate in Emergency Medical Services',
        'certifications': ['Certified Hotel Administrator (CHA)', 'Certified Hospitality Supervisor (CHS)', 'ServSafe Food Safety Certification', 'HACCP Certification', 'Certified Event Planner (CEP)', 'Certified Tourism Professional (CTP)', 'Six Sigma Green/Black Belt (Customer Service)', 'Customer Experience Professional Certification', 'Fire Safety Certification (NIFS)', 'First Aid & CPR Certification', 'Disaster Management Certification (NDMA)'],
        'hiring_cities': ['Mumbai', 'Delhi NCR', 'Bengaluru', 'Goa', 'Chennai', 'Hyderabad', 'Kolkata', 'Pune', 'Ahmedabad', 'Jaipur', 'Udaipur', 'Agra', 'Kochi', 'Thiruvananthapuram', 'Chandigarh', 'Lucknow', 'Shimla', 'Manali', 'Darjeeling', 'Ooty']
    },
    'service_hospitality_college': {
        'name': 'Service, Hospitality & Public Safety (Advanced)',
        'icon': '🏨',
        'description': 'Advanced study in hospitality management, tourism administration, event leadership, and public safety administration. Prepare for leadership roles in luxury hotels, tourism boards, mega events, disaster response agencies, and security organizations.',
        'careers': ['General Manager (Hotel) - Lead hotel operations', 'Regional Director (Hospitality) - Oversee multiple properties', 'Food & Beverage Director - Manage F&B operations', 'Event Director - Lead major events (weddings, corporate, MICE)', 'Tourism Board Director - Promote regional tourism', 'Customer Experience Head - Lead CX strategy', 'Police Commissioner - Lead city police force', 'Fire Chief - Lead fire department', 'Disaster Management Director - Coordinate state/national response', 'Security Consultant - Advise on security strategy', 'Luxury Hotel Manager - Manage premium properties', 'Resort General Manager - Lead resort operations'],
        'subjects': ['Advanced Hospitality Management', 'Luxury Brand Management', 'Revenue Management & Pricing Strategy', 'Food & Beverage Management Advanced', 'Event Leadership & Mega Event Planning', 'Tourism Policy & Planning', 'Crisis Communication & Reputation Management', 'Public Safety Administration', 'Strategic Emergency Management', 'Disaster Risk Reduction (DRR)', 'Security Risk Assessment', 'Advanced Fire Safety Engineering', 'Urban Safety & Smart Policing', 'Customer Experience Design', 'Service Operations Management'],
        'skills': ['Strategic Leadership', 'Revenue Management (RevPAR, GOPPAR)', 'Luxury Service Standards', 'Crisis Leadership', 'Public Policy Analysis', 'Emergency Operations Center (EOC) Management', 'Inter-agency Coordination', 'Budgeting & Financial Control', 'Change Management', 'Stakeholder Management (Government, Private, NGOs)', 'Data-Driven Decision Making', 'Team Development & Training', 'Brand Reputation Management', 'International Hospitality Standards'],
        'software_skills': [
            '🏨 Advanced PMS: Oracle Opera Cloud, Amadeus PMS, Infor HMS',
            '📊 Revenue Management: IDeaS, Duetto, Rainmaker',
            '🎯 CRM Advanced: Salesforce Hospitality Cloud, Oracle Hospitality CX',
            '📈 Business Intelligence: HotStats, STR Analytics, Kalibri Labs',
            '🎫 Mega Event Management: Momentus Technologies, Ungerboeck, Aventri',
            '🚨 Advanced Emergency Management: Juvare, Everbridge, Crisis Commander'
        ],
        'career_skills': [
            '🏨 Strategic Hospitality Leadership',
            '📊 Revenue & Yield Management Expertise',
            '🎯 Luxury Service & Brand Management',
            '🚨 Crisis Leadership & Emergency Coordination',
            '🌍 International Tourism Policy',
            '👥 Executive Leadership & Board Management'
        ],
        'technical_skills': [
          'Property Management Systems (PMS - Opera, IDS, WinHms)',
          'Point of Sale (POS) Systems',
          'Security Systems (CCTV, Access Control)',
          'Emergency Response Equipment',
          'Fire Safety Equipment',
          'Communication Systems',
          'Reservation Systems (CRS, GDS)',
          'Event Management Software',
          'Customer Relationship Management (CRM)',
          'Hotel Accounting Software',
          'Inventory Management Systems',
          'Tourism Management Systems'
       ],
        'future_scope': 'Luxury hotel expansion (Taj, Oberoi, Leela), International hotel brands growth in India (Marriott, Hyatt, Hilton), MICE tourism growth, Medical tourism, Spiritual tourism, Cruise tourism, Smart policing initiatives, Disaster management modernization',
        'top_companies': [
            'Luxury Hotels: Taj Hotels (IHCL) Corporate - Mumbai - Leadership roles',
            'Oberoi Hotels Corporate - Delhi - Regional management',
            'ITC Hotels Corporate - Gurugram - Director positions',
            'Marriott International India Corporate - Mumbai/Gurugram - Regional Directors',
            'Hyatt India Corporate - Gurugram - Leadership team',
            'Accor India Corporate - Gurugram - Country leadership',
            'Tourism Boards: Ministry of Tourism (Government of India) - Delhi',
            'Incredible India Campaign - Delhi', 'Kerala Tourism - Thiruvananthapuram', 'Rajasthan Tourism - Jaipur',
            'Goa Tourism - Panaji', 'Himachal Tourism - Shimla', 'Uttarakhand Tourism - Dehradun',
            'Public Safety Leadership: National Disaster Management Authority (NDMA) - Delhi',
            'National Disaster Response Force (NDRF) HQ - Delhi', 'Ministry of Home Affairs - Delhi',
            'Indian Police Service (IPS) Cadre - State Capitals (Senior leadership roles)',
            'Consulting: Deloitte Hospitality Consulting - Mumbai/Delhi',
            'PwC Hospitality & Tourism - Mumbai/Delhi', 'KPMG Hospitality Advisory - Mumbai/Delhi/Bengaluru',
            'EY Hospitality & Leisure - Mumbai/Delhi/Bengaluru', 'HVS India - Gurugram',
            'Customer Experience Leadership: Amazon Customer Service HQ - Hyderabad, Bengaluru, Delhi NCR',
            'Flipkart Customer Experience - Bengaluru, Gurugram', 'Swiggy Customer Support - Bengaluru, Gurugram',
            'Zomato Customer Experience - Gurugram', 'Razorpay Customer Success - Bengaluru'
        ],
        'education_path': 'MBA in Hospitality Management, MSc in International Hospitality Management, Master in Tourism Management (MTM), MBA in Tourism, PG Diploma in Event Management, Master in Public Administration (MPA - Safety), PG Diploma in Disaster Management, M.Tech in Fire Safety Engineering, MBA in Customer Experience Management, Executive MBA in Hospitality Leadership',
        'certifications': ['Certified Hotel Administrator (CHA) - Advanced', 'Certified Hospitality Educator (CHE)', 'Certified Revenue Management Executive (CRME)', 'LEED Green Associate (Sustainable Hospitality)', 'Certified Meeting Professional (CMP)', 'Certified Special Events Professional (CSEP)', 'Certified Emergency Manager (CEM)', 'Certified Business Continuity Professional (CBCP)', 'Certified Security Professional (CSP)', 'Incident Command System (ICS) Certification', 'Six Sigma Black Belt (Service Operations)', 'Customer Experience Professional (CCXP)'],
        'hiring_cities': ['Mumbai', 'Delhi NCR', 'Bengaluru', 'Goa', 'Jaipur', 'Chennai', 'Kolkata', 'Hyderabad', 'Pune', 'Ahmedabad', 'Thiruvananthapuram', 'Guwahati', 'Lucknow', 'Chandigarh', 'Bhopal', 'Shimla', 'Dehradun']
    },

    # ==================== 21. ENERGY & UTILITIES ====================
    'energy_utilities': {
        'name': 'Energy & Utilities',
        'icon': '⚡',
        'description': 'This vital stream focuses on power generation (thermal, hydro, nuclear, solar, wind), transmission, distribution, renewable energy, oil & gas, and utility management.',
        'careers': ['Power Plant Engineer - Manage power plants', 'Renewable Energy Engineer - Design solar/wind systems', 'Solar Project Manager - Lead solar projects', 'Wind Energy Engineer - Design wind farms', 'Electrical Engineer (Power) - Manage transmission', 'Grid Operations Manager - Oversee power grid', 'Energy Analyst - Analyze energy patterns', 'Oil & Gas Engineer - Manage exploration', 'Utility Manager - Manage utilities', 'Energy Consultant - Advise on efficiency'],
        'subjects': ['Power Generation', 'Renewable Energy', 'Electrical Power Systems', 'Transmission & Distribution', 'Smart Grid Technology', 'Energy Storage', 'Oil & Gas Engineering', 'Energy Economics', 'Energy Auditing', 'Utility Management'],
        'skills': ['Power System Analysis', 'Renewable Energy Design', 'Project Management', 'Energy Auditing', 'Data Analysis', 'SCADA Systems', 'Grid Integration', 'Safety Compliance', 'Regulatory Knowledge', 'Team Leadership'],
        'software_skills': [
            '⚡ Power System: ETAP, PSS/E, DIgSILENT PowerFactory, PSCAD',
            '☀️ Solar Design: PVSyst, Helioscope, PVSOL, SAM (NREL)',
            '💨 Wind Design: WAsP, WindPRO, OpenWind, GH WindFarmer',
            '🔋 Battery Storage: HOMER Energy, DER-CAM, Storage VET',
            '📊 SCADA: Wonderware, Ignition, Siemens WinCC, Schneider ClearSCADA',
            '📈 Energy Management: EnergyCAP, eSight, BuildingOS, ENERGY STAR Portfolio Manager'
        ],
        'career_skills': [
            '⚡ Power System Analysis & Grid Management',
            '☀️ Renewable Energy Project Development',
            '📊 Energy Auditing & Efficiency Optimization',
            '🎯 Project Management & Regulatory Compliance',
            '🔋 Battery Energy Storage Systems (BESS)',
            '👥 Team Leadership & Safety Management'
        ],
        'technical_skills': [
          'Power Generation Technologies (Thermal, Hydro, Nuclear, Solar, Wind)',
          'Renewable Energy Systems Design (PVSyst, Helioscope)',
          'Grid Management & SCADA Systems',
          'Energy Storage Technologies (Battery, Pumped Hydro)',
          'Smart Grid & IoT Integration',
          'Power System Analysis Software (ETAP, PSS/E)',
          'Electrical Distribution Management',
          'Oil & Gas Exploration Techniques',
          'Refinery Operations & Process Engineering',
          'Energy Management Systems (EMS)',
          'Building Management Systems (BMS)',
          'Energy Auditing Tools & Techniques',
          'HVDC Transmission Systems',
          'Substation Automation'
       ],
        'future_scope': "India's 500 GW renewable target by 2030, Green Hydrogen Mission, Nuclear expansion, Smart Grid Nation, EV charging infrastructure, Oil & gas exploration, City Gas Distribution expansion",
        'top_companies': [
            'NTPC - Delhi (India\'s largest power generator)',
            'Power Grid Corporation - Gurugram (National grid operator)',
            'Adani Power - Ahmedabad (15 GW+ capacity)',
            'Tata Power - Mumbai (14 GW capacity)',
            'Adani Green Energy - Ahmedabad (India\'s largest renewable - 20 GW+)',
            'ReNew Power - Gurugram (15+ GW renewable)',
            'Greenko Group - Hyderabad (7+ GW with storage)',
            'Azure Power - Delhi (7+ GW solar)',
            'Suzlon Group - Pune (Wind turbines - 20 GW+ installed)',
            'Vestas India - Chennai (Wind turbines - 8+ GW)',
            'Siemens Gamesa India - Chennai (Wind turbines - 6+ GW)',
            'Sterling and Wilson Solar - Mumbai (World\'s largest solar EPC - 12+ GW)',
            'L&T Solar - Mumbai (Solar EPC - 5+ GW)',
            'Tata Power Solar - Bengaluru (Solar manufacturing & EPC - 10+ GW)',
            'ONGC - Dehradun (India\'s largest E&P - 60% of oil & gas)',
            'IOCL - Delhi (India\'s largest refiner - 70+ MMTPA)',
            'BPCL - Mumbai (35+ MMTPA refining)', 'HPCL - Mumbai (30+ MMTPA refining)',
            'GAIL India - Delhi (India\'s largest gas utility - 17,000+ km pipelines)',
            'Reliance Industries - Mumbai (World\'s largest refining complex - Jamnagar 68 MMTPA)',
            'BSES Rajdhani - Delhi (Distribution - 2.5M+ customers)',
            'Adani Electricity - Mumbai (Distribution - 4M+ customers)',
            'CESC - Kolkata (Distribution - 3M+ customers)'
        ],
        'education_path': 'B.Tech Electrical/Mechanical/Power/Renewable Energy, M.Tech Power Systems, MBA Energy Management, B.Tech Petroleum Engineering, Diploma in Electrical/Power, Certification in Solar/Wind Energy',
        'certifications': ['Certified Energy Manager (CEM)', 'Certified Energy Auditor (CEA)', 'Solar PV Design Certification', 'Wind Energy Professional', 'PMP for Energy Projects', 'Grid Code Certification', 'ISO 50001 Lead Auditor', 'Energy Storage Professional'],
        'hiring_cities': ['Delhi NCR', 'Mumbai', 'Ahmedabad', 'Bengaluru', 'Chennai', 'Hyderabad', 'Kolkata', 'Pune', 'Vadodara', 'Jaipur', 'Lucknow', 'Chandigarh', 'Bhubaneswar', 'Guwahati', 'Dehradun', 'Visakhapatnam']
    },
    'energy_utilities_college': {
        'name': 'Energy & Utilities (Advanced)',
        'icon': '⚡',
        'description': 'Advanced study in power systems, renewable energy integration, smart grids, energy storage, oil & gas, and utility management. Prepare for leadership roles in India\'s energy sector.',
        'careers': ['Chief Power Engineer - Lead plant operations', 'Renewable Energy Director - Oversee RE projects', 'Grid Controller - Manage national grid', 'Energy Strategy Consultant - Advise on transition', 'Head of Energy Storage - Lead BESS projects', 'VP of Renewables - Drive RE development', 'Energy Policy Advisor - Shape policies', 'Oil & Gas Director - Lead E&P projects', 'Utility CEO - Lead utilities'],
        'subjects': ['Advanced Power Systems', 'Grid Integration', 'Smart Grid Technologies', 'Energy Storage', 'HVDC Transmission', 'Energy Economics', 'Oil & Gas Engineering', 'Carbon Capture', 'Green Hydrogen', 'Energy Policy'],
        'skills': ['Strategic Planning', 'Grid Modernization', 'Power System Modeling', 'Energy Forecasting', 'Project Finance', 'Policy Analysis', 'M&A Advisory', 'Risk Management', 'Stakeholder Management', 'Carbon Markets'],
        'software_skills': [
            '⚡ Advanced Grid: PSS/E, PowerWorld, PSCAD/EMTDC, RSCAD',
            '☀️ Solar Advanced: PVsyst Pro, SolarFarmer, PlantPredict',
            '💨 Wind Advanced: WindFarmer, GH WindFarmer, OpenFAST',
            '🔋 Storage Advanced: Homer Pro, DER-CAM, PLEXOS',
            '📊 Energy Trading: Allegro, ETRM, Triple Point, Amphora',
            '💚 Green Hydrogen: H2A, HOMER Pro, Greenius'
        ],
        'career_skills': [
            '⚡ Grid Modernization & Smart Grid Strategy',
            '☀️ Renewable Energy Investment & Finance',
            '💚 Green Hydrogen & Carbon Capture',
            '📊 Energy Policy & Regulatory Affairs',
            '🎯 M&A & Project Finance Leadership',
            '🌍 International Energy Markets & Trading'
        ],
        'technical_skills': [
          'Power Generation Technologies (Thermal, Hydro, Nuclear, Solar, Wind)',
          'Renewable Energy Systems Design (PVSyst, Helioscope)',
          'Grid Management & SCADA Systems',
          'Energy Storage Technologies (Battery, Pumped Hydro)',
          'Smart Grid & IoT Integration',
          'Power System Analysis Software (ETAP, PSS/E)',
          'Electrical Distribution Management',
          'Oil & Gas Exploration Techniques',
          'Refinery Operations & Process Engineering',
          'Energy Management Systems (EMS)',
          'Building Management Systems (BMS)',
          'Energy Auditing Tools & Techniques',
          'HVDC Transmission Systems',
          'Substation Automation'
       ],
        'future_scope': "India's energy transition, Green Hydrogen Mission (₹8,000 crore), Smart Grid Nation, National Carbon Market, Energy Storage Obligation, Offshore Wind (30 GW), Hydrogen blending, Carbon capture projects",
        'top_companies': [
            'NTPC Corporate - Delhi (CMD, Director roles)',
            'Power Grid Corporation - Gurugram (Leadership roles)',
            'ONGC - Dehradun/Mumbai (CMD, Director)',
            'IOCL - Delhi (CMD, Director)',
            'Adani Green Energy - Ahmedabad (CEO, COO, Directors)',
            'ReNew Power - Gurugram (CEO, VP roles)',
            'Greenko Group - Hyderabad (Leadership roles)',
            'Tata Power - Mumbai (CEO - Renewables, T&D)',
            'Reliance New Energy - Mumbai (CEO - Green Energy)',
            'McKinsey Energy - Mumbai/Delhi (Engagement Managers)',
            'BCG Energy - Mumbai/Delhi (Consultants)',
            'Deloitte Energy - Mumbai/Delhi (Directors)',
            'Ministry of Power - Delhi (Joint Secretary, Directors)',
            'MNRE - Delhi (Joint Secretary, Directors)',
            'World Bank India - Delhi (Energy Specialists)',
            'PFC - Delhi (Director, CFO)', 'REC - Gurugram (Director)',
            'IREDA - Delhi (Director)', 'IEX - Delhi (CEO, Head of Trading)'
        ],
        'education_path': 'M.Tech Power Systems/Renewable Energy (IITs, NITs), MBA Energy Management (UPES, TERI), M.Sc Energy Economics, PhD Energy Sciences, PG Diploma Renewable Energy, Executive MBA Energy (IIM A, ISB)',
        'certifications': ['CEM (Advanced)', 'CEA (BEE)', 'REP (Renewable Energy Professional)', 'Energy Storage Professional', 'Smart Grid Professional', 'Green Hydrogen Professional', 'Carbon Trading Certified', 'PMP', 'Advanced Power System Analysis'],
        'hiring_cities': ['Delhi NCR', 'Mumbai', 'Ahmedabad', 'Bengaluru', 'Hyderabad', 'Chennai', 'Pune', 'Kolkata', 'Gurugram', 'Dehradun']
    },
         # ==================== RETAIL & E-COMMERCE ====================
    'retail_ecommerce': {
        'name': 'Retail & E-commerce',
        'icon': '🛒',
        'description': 'This dynamic stream focuses on retail management, e-commerce operations, digital marketing, supply chain logistics, and customer experience. Students learn about online marketplaces, inventory management, omnichannel retail, and consumer behavior in the digital age.',
        'careers': ['E-commerce Manager - Oversee online sales operations', 'Retail Store Manager - Manage physical retail locations', 'Digital Marketing Specialist - Drive online customer acquisition', 'Supply Chain Analyst - Optimize logistics and inventory', 'Merchandise Planner - Plan product assortment and pricing', 'Customer Experience Manager - Enhance shopping experience', 'Product Manager - Manage online product catalogs', 'Logistics Coordinator - Coordinate shipping and delivery', 'Category Manager - Manage product categories', 'E-commerce Developer - Build and maintain online stores', 'Retail Buyer - Select products for stores', 'Social Media Manager - Manage brand presence online', 'Data Analyst - Analyze sales and customer data', 'Warehouse Operations Manager - Manage fulfillment centers', 'Visual Merchandiser - Design store displays', 'Online Marketplace Specialist - Manage Amazon, Flipkart, etc.', 'Payment Solutions Manager - Handle payment gateways', 'Returns and Refunds Manager - Process customer returns'],
        'subjects': ['Retail Management', 'E-commerce Operations', 'Digital Marketing', 'Supply Chain Management', 'Inventory Management', 'Customer Relationship Management', 'Web Analytics', 'Online Payment Systems', 'Logistics and Fulfillment', 'Consumer Behavior', 'Merchandising', 'Omnichannel Retail', 'Marketplace Management', 'E-commerce Platforms (Shopify, Magento)'],
        'skills': ['Digital Marketing (SEO, SEM, Social Media)', 'Data Analysis and Analytics', 'Inventory Management', 'Customer Service Excellence', 'Supply Chain Optimization', 'Project Management', 'E-commerce Platform Management', 'Negotiation Skills', 'Financial Planning', 'Team Leadership', 'Problem Solving', 'Communication Skills', 'Strategic Planning', 'Vendor Management'],
        'software_skills': [
            '🛒 E-commerce Platforms: Shopify, Magento, WooCommerce, BigCommerce',
            '📊 Analytics: Google Analytics, Adobe Analytics, Mixpanel, Amplitude',
            '📈 Digital Marketing: Google Ads, Facebook Ads Manager, SEMrush, HubSpot',
            '📦 Inventory Management: TradeGecko, Skubana, Cin7, Zoho Inventory',
            '🗣️ CRM: Salesforce Commerce Cloud, Zendesk, Freshdesk, Klaviyo',
            '💳 Payment Gateways: Razorpay, PayU, Stripe, PayPal, CCAvenue',
            '📱 Social Media: Hootsuite, Buffer, Sprout Social, Later',
            '📧 Email Marketing: Mailchimp, SendGrid, MoEngage, Webengage'
        ],
        'career_skills': [
            '🎯 Strategic E-commerce Planning',
            '📊 Data-Driven Decision Making',
            '🤝 Customer Relationship Management',
            '📈 Digital Marketing & SEO Expertise',
            '📦 Inventory & Supply Chain Optimization',
            '🗣️ Communication & Negotiation Skills'
        ],
        'technical_skills': [
          'E-commerce Platforms (Shopify, Magento, WooCommerce)',
          'Digital Marketing (SEO, SEM, Google Ads)',
          'Social Media Marketing (Meta, Instagram, LinkedIn)',
          'Email Marketing & Automation',
          'Analytics (Google Analytics, Tableau)',
          'Inventory Management Systems',
          'Customer Relationship Management (CRM)',
          'Payment Gateway Integration',
          'Supply Chain Management',
          'Order Fulfillment Systems',
          'Data Analysis (Excel, SQL)',
          'Marketplace Management (Amazon, Flipkart)'
       ],
        'future_scope': 'Explosive growth in online retail, digital commerce, and omnichannel experiences. High demand for e-commerce professionals, digital marketers, and supply chain experts.',
        'top_companies': [
            'Amazon India - Bengaluru, Hyderabad, Delhi, Mumbai, Chennai, Pune, Kolkata',
            'Flipkart - Bengaluru, Delhi, Mumbai, Chennai, Hyderabad, Kolkata, Pune',
            'Meesho - Bengaluru, Delhi, Mumbai, Chennai, Hyderabad, Pune, Kolkata',
            'Nykaa - Mumbai, Delhi, Bengaluru, Chennai, Hyderabad, Pune, Kolkata',
            'Myntra - Bengaluru, Delhi, Mumbai, Chennai, Hyderabad, Pune, Kolkata',
            'BigBasket - Bengaluru, Delhi, Mumbai, Chennai, Hyderabad, Pune, Kolkata, Ahmedabad',
            'Zepto - Mumbai, Bengaluru, Delhi, Chennai, Hyderabad, Pune, Kolkata',
            'Blinkit - Gurugram, Delhi, Mumbai, Bengaluru, Chennai, Hyderabad, Pune',
            'Swiggy Instamart - Bengaluru, Delhi, Mumbai, Chennai, Hyderabad, Pune, Kolkata',
            'Tata Cliq - Mumbai, Bengaluru, Delhi, Chennai, Kolkata, Pune, Hyderabad',
            'Reliance Retail - Mumbai, Across India', 'Ajio - Mumbai, Bengaluru, Delhi, Chennai',
            'Unicommerce - Delhi NCR, Mumbai, Bengaluru', 'Shiprocket - Delhi NCR, Bengaluru, Mumbai'
        ],
        'education_path': 'BBA in Retail Management, B.Com, BBA in E-commerce, MBA in Marketing/Operations, Diploma in Digital Marketing, Certification in E-commerce Management',
        'certifications': ['Google Digital Marketing Certification', 'Shopify Partner Certification', 'Facebook Blueprint Certification', 'Amazon Seller Central Certification', 'Google Analytics Certification', 'HubSpot E-commerce Certification', 'Certified E-commerce Consultant', 'Supply Chain Management Certification', 'Digital Marketing Master Certification', 'E-commerce Strategy Certification'],
        'hiring_cities': ['Bengaluru', 'Mumbai', 'Delhi NCR', 'Hyderabad', 'Chennai', 'Pune', 'Kolkata', 'Ahmedabad', 'Jaipur', 'Lucknow', 'Chandigarh', 'Goa']
    },
    'retail_ecommerce_college': {
        'name': 'Retail & E-commerce (Advanced)',
        'icon': '🛒',
        'description': 'Advanced study in retail strategy, e-commerce technology, omnichannel integration, and digital transformation. Prepare for leadership roles in online retail, marketplace management, and retail technology innovation.',
        'careers': ['Chief E-commerce Officer - Lead e-commerce strategy', 'Head of Digital Retail - Oversee digital channels', 'E-commerce Director - Manage online business growth', 'Retail Technology Consultant - Advise on retail tech', 'Digital Transformation Manager - Lead retail innovation', 'Head of Marketplace Operations - Manage online marketplaces', 'Customer Analytics Manager - Analyze customer behavior', 'Supply Chain Director - Lead logistics strategy', 'E-commerce Platform Architect - Design e-commerce systems', 'Head of Omnichannel Retail - Integrate online and offline', 'Retail Data Scientist - Drive data-based decisions', 'Digital Payments Head - Manage payment solutions', 'Last-Mile Delivery Director - Optimize final delivery', 'Retail Innovation Manager - Drive new retail concepts'],
        'subjects': ['Advanced E-commerce Strategy', 'Retail Analytics and BI', 'Omnichannel Retail Management', 'Digital Supply Chain', 'Customer Data Platforms', 'E-commerce Technology Stack', 'Marketplace Dynamics', 'Last-Mile Logistics', 'Retail Fintech', 'Digital Customer Experience', 'Retail AI and Automation', 'International E-commerce', 'Subscription Commerce Models', 'Social Commerce Strategies'],
        'skills': ['Strategic Leadership', 'Advanced Data Analytics', 'Digital Transformation', 'E-commerce Platform Architecture', 'Omnichannel Integration', 'Customer Journey Optimization', 'Revenue Management', 'Team Leadership', 'Vendor Negotiation', 'International Trade Knowledge', 'Risk Management', 'Innovation Management', 'Change Management', 'Financial Modeling'],
        'software_skills': [
            '🛒 Advanced E-commerce: Salesforce Commerce Cloud, SAP Hybris, Oracle Commerce',
            '📊 Advanced Analytics: Google Analytics 4, Adobe Analytics, Heap, Mixpanel',
            '🤖 AI/ML in Retail: Dynamic Yield, Monetate, Clerk.io, Nosto',
            '📈 CDP: Segment, mParticle, Lytics, BlueConic',
            '📦 OMS: Manhattan OMS, IBM Sterling, Fluent Order Management',
            '💳 Fintech: Stripe Connect, RazorpayX, Paytm Payments Bank APIs',
            '🔧 DevOps for E-commerce: AWS Retail, Shopify Plus, BigCommerce Enterprise'
        ],
        'career_skills': [
            '🎯 Strategic E-commerce Leadership',
            '📊 Advanced Customer Analytics & Personalization',
            '🤝 Omnichannel Strategy & Integration',
            '📈 International E-commerce Expansion',
            '💡 Retail Technology Innovation',
            '👥 Executive Leadership & Board Management'
        ],
        'technical_skills': [
          'E-commerce Platforms (Shopify, Magento, WooCommerce)',
          'Digital Marketing (SEO, SEM, Google Ads)',
          'Social Media Marketing (Meta, Instagram, LinkedIn)',
          'Email Marketing & Automation',
          'Analytics (Google Analytics, Tableau)',
          'Inventory Management Systems',
          'Customer Relationship Management (CRM)',
          'Payment Gateway Integration',
          'Supply Chain Management',
          'Order Fulfillment Systems',
          'Data Analysis (Excel, SQL)',
          'Marketplace Management (Amazon, Flipkart)'
       ],
        'future_scope': 'Leadership positions in e-commerce companies, retail chains, digital agencies, and technology firms. Growing demand for omnichannel experts and retail technology leaders.',
        'top_companies': [
            'Amazon India - Bengaluru, Hyderabad, Delhi NCR',
            'Flipkart Group - Bengaluru, Gurugram',
            'Walmart Global Tech India - Bengaluru, Chennai',
            'Tata Digital - Mumbai, Bengaluru',
            'Reliance Retail Ventures - Mumbai',
            'Meesho - Bengaluru',
            'Nykaa - Mumbai',
            'Unilever Digital Hub - Bengaluru',
            'Nestle E-commerce - Gurugram',
            'P&G Digital - Mumbai',
            'Shopify Plus - Remote (India operations)',
            'Salesforce Commerce Cloud - Hyderabad, Bengaluru',
            'Adobe Commerce (Magento) - Bengaluru, Noida',
            'BigCommerce - Remote',
            'Razorpay - Bengaluru (E-commerce Payments)'
        ],
        'education_path': 'MBA in E-commerce/Digital Business, M.Com in E-commerce, PG Diploma in Digital Retail Management, Executive MBA in Retail Management',
        'certifications': ['Certified E-commerce Professional (CEP)', 'Advanced Google Analytics Certification', 'Shopify Plus Certification', 'Salesforce Commerce Cloud Certification', 'Adobe Commerce Certification', 'Certified Digital Supply Chain Professional', 'Retail Management Advanced Certification', 'E-commerce Strategy Certification (Harvard)'],
        'hiring_cities': ['Bengaluru', 'Mumbai', 'Delhi NCR (Gurugram, Noida)', 'Hyderabad', 'Chennai', 'Pune', 'Kolkata', 'Ahmedabad']
    },
         # ==================== ACCOUNTING & FINANCE ====================
    'accounting': {
        'name': 'Accounting & Finance',
        'icon': '💰',
        'description': 'This stream focuses on financial management, accounting principles, taxation, auditing, and corporate finance. Students learn to manage financial records, analyze financial data, and make strategic financial decisions for organizations.',
        'careers': ['Chartered Accountant (CA) - Manage financial accounts and audits', 'Certified Public Accountant (CPA) - Handle accounting and tax services', 'Financial Analyst - Analyze financial data for investment decisions', 'Investment Banker - Facilitate mergers, acquisitions, and fundraising', 'Tax Consultant - Advise on tax planning and compliance', 'Audit Manager - Lead audit teams and ensure financial compliance', 'Cost Accountant - Manage cost analysis and optimization', 'Finance Manager - Oversee corporate financial operations', 'Chief Financial Officer (CFO) - Lead financial strategy', 'Risk Manager - Identify and mitigate financial risks', 'Wealth Manager - Manage investment portfolios for clients', 'Credit Analyst - Assess creditworthiness of borrowers', 'Forensic Accountant - Investigate financial fraud', 'Treasury Analyst - Manage cash flow and liquidity', 'Financial Controller - Oversee financial reporting', 'Internal Auditor - Evaluate internal financial controls', 'Payroll Manager - Manage employee payroll systems', 'Budget Analyst - Prepare and analyze budgets'],
        'subjects': ['Financial Accounting', 'Managerial Accounting', 'Corporate Finance', 'Taxation (Direct & Indirect)', 'Auditing and Assurance', 'Cost Accounting', 'Financial Management', 'Investment Analysis', 'Risk Management', 'International Finance', 'Financial Reporting', 'Business Law', 'Economics', 'Statistics', 'Financial Modeling'],
        'skills': ['Financial Analysis', 'Attention to Detail', 'Analytical Thinking', 'Excel and Financial Software', 'Problem Solving', 'Communication Skills', 'Ethical Judgment', 'Time Management', 'Team Collaboration', 'Regulatory Knowledge', 'Risk Assessment', 'Data Interpretation', 'Strategic Planning', 'Negotiation Skills'],
        'software_skills': [
            '💰 Accounting Software: Tally ERP 9, Tally Prime, QuickBooks, Zoho Books, SAP FICO',
            '📊 Financial Modeling: MS Excel (Advanced), Python, R, MATLAB',
            '📈 ERP Systems: SAP S/4HANA, Oracle Financials, Microsoft Dynamics 365, NetSuite',
            '📋 Taxation Software: ClearTax, Taxmann, CompuTax, GenTally, IRIS',
            '🏦 Banking Software: Finacle, BaNCS, Flexcube, Finastra',
            '📉 BI & Analytics: Tableau, Power BI, QlikView, Looker, IBM Cognos',
            '📑 Audit Software: CaseWare, TeamMate, ACL Analytics, IDEA',
            '💹 Risk Management: RiskWatch, Active Risk Manager, SAS Risk Management'
        ],
        'career_skills': [
            '💰 Financial Analysis & Interpretation',
            '🔍 Attention to Detail & Accuracy',
            '📊 Analytical Thinking & Problem Solving',
            '⚖️ Ethical Judgment & Professional Integrity',
            '🗣️ Communication & Client Management',
            '📈 Strategic Financial Planning',
            '🤝 Team Collaboration & Leadership',
            '⏰ Time Management & Deadline Adherence',
            '📋 Regulatory Compliance Knowledge'
        ],
        'technical_skills': [
          'Financial Accounting & Reporting',
          'Taxation (Direct & Indirect)',
          'Auditing & Assurance',
          'Financial Modeling (Excel, VBA)',
          'Corporate Finance & Valuation',
          'Investment Analysis (CFA Principles)',
          'Cost Accounting & Management',
          'ERP Systems (SAP, Oracle, Tally)',
          'Regulatory Compliance (SEBI, RBI)',
          'Risk Management',
          'Budgeting & Forecasting',
          'Mergers & Acquisitions'
       ],
        'future_scope': 'High demand in banking, corporate finance, auditing firms, tax consulting, and financial services. Growing opportunities in fintech and digital finance.',
        'top_companies': [
            'Deloitte India - Mumbai, Delhi, Bengaluru, Hyderabad, Chennai, Pune, Kolkata',
            'PwC India - Kolkata, Mumbai, Delhi, Bengaluru, Hyderabad, Chennai, Pune',
            'KPMG India - Mumbai, Delhi, Bengaluru, Hyderabad, Chennai, Pune, Gurugram, Noida',
            'EY India - Mumbai, Delhi, Bengaluru, Hyderabad, Chennai, Kolkata, Pune, Ahmedabad',
            'Goldman Sachs India - Bengaluru, Mumbai, Hyderabad',
            'JP Morgan India - Mumbai, Bengaluru, Hyderabad, Delhi NCR',
            'Morgan Stanley India - Mumbai, Bengaluru, Delhi NCR',
            'HDFC Bank - Mumbai, Delhi, Bengaluru, Chennai, Kolkata, Pune, Hyderabad',
            'ICICI Bank - Mumbai, Delhi, Bengaluru, Hyderabad, Chennai, Kolkata, Pune',
            'State Bank of India - Across India (All Major Cities)',
            'Axis Bank - Mumbai, Delhi, Bengaluru, Kolkata, Chennai, Pune, Hyderabad',
            'Kotak Mahindra Bank - Mumbai, Delhi, Bengaluru, Chennai, Hyderabad, Pune',
            'Grant Thornton India - Mumbai, Delhi, Bengaluru', 'BDO India - Mumbai, Delhi, Bengaluru',
            'RSM India - Mumbai, Delhi, Bengaluru', 'Nexdigm - Mumbai, Delhi, Bengaluru'
        ],
        'education_path': 'B.Com, BBA in Finance, CA (Chartered Accountant), CPA (Certified Public Accountant), CMA (Certified Management Accountant), CFA (Chartered Financial Analyst), MBA in Finance, M.Com, CS (Company Secretary)',
        'certifications': ['Chartered Accountant (CA)', 'Certified Public Accountant (CPA)', 'Chartered Financial Analyst (CFA)', 'Certified Management Accountant (CMA)', 'Association of Chartered Certified Accountants (ACCA)', 'Certified Internal Auditor (CIA)', 'Financial Risk Manager (FRM)', 'Certified Information Systems Auditor (CISA)', 'Certified Fraud Examiner (CFE)', 'Diploma in IFRS', 'Certified Treasury Professional (CTP)', 'Certified Financial Planner (CFP)'],
        'hiring_cities': ['Mumbai', 'Delhi NCR', 'Bengaluru', 'Chennai', 'Hyderabad', 'Pune', 'Kolkata', 'Ahmedabad', 'Gurugram', 'Noida', 'Jaipur', 'Lucknow', 'Chandigarh', 'Kochi', 'Indore', 'Nagpur']
    },
    'accounting_college': {
        'name': 'Accounting & Finance (Advanced)',
        'icon': '💰',
        'description': 'Advanced study in financial management, corporate accounting, international taxation, and strategic finance. Prepare for leadership roles in financial institutions, corporate finance, and investment banking.',
        'careers': ['Senior Accountant - Lead accounting teams', 'Finance Manager - Manage corporate finance', 'Investment Banker - Handle financial transactions', 'Tax Director - Oversee tax strategy', 'Audit Partner - Lead audit firms', 'Chief Financial Officer (CFO) - Manage company finances', 'Financial Controller - Oversee financial reporting', 'Treasury Manager - Manage corporate treasury', 'M&A Specialist - Handle mergers and acquisitions', 'Private Equity Analyst - Analyze investment opportunities', 'Hedge Fund Manager - Manage investment funds', 'Chief Risk Officer - Lead risk management'],
        'subjects': ['Advanced Accounting', 'Corporate Finance', 'International Taxation', 'Financial Reporting', 'Auditing Advanced', 'Risk Management Advanced', 'Mergers & Acquisitions', 'Private Equity & Venture Capital', 'Derivatives & Risk Management', 'Financial Statement Analysis', 'Strategic Financial Management', 'Corporate Governance'],
        'skills': ['Strategic Financial Planning', 'Leadership', 'Risk Assessment', 'Corporate Governance', 'Regulatory Compliance', 'Team Management', 'Advanced Financial Modeling', 'Investment Analysis', 'M&A Strategy', 'International Finance', 'Executive Communication', 'Decision Making'],
        'software_skills': [
            '💰 Advanced Accounting: SAP S/4HANA Finance, Oracle Cloud ERP, NetSuite',
            '📊 Advanced Financial Modeling: Python, R, MATLAB, VBA, C++ for Finance',
            '📈 BI Advanced: Tableau Server, Power BI Premium, Qlik Sense Enterprise',
            '💹 Risk Management Advanced: Bloomberg Terminal, Reuters Eikon, FactSet',
            '📑 Audit Advanced: CaseWare Working Papers, Teammate+, ACL Robotics',
            '🏦 Treasury Management: Kyriba, Coupa, GTreasury, SAP Treasury',
            '📋 Compliance: Thomson Reuters, Wolters Kluwer, CCH Tagetik'
        ],
        'career_skills': [
            '🎯 Strategic Financial Leadership',
            '📊 Advanced Financial Analysis & Modeling',
            '⚖️ Corporate Governance & Compliance',
            '🤝 Investment Banking & M&A Strategy',
            '👥 Team Leadership & Talent Development',
            '🌍 Global Finance & International Taxation',
            '💡 Strategic Decision Making',
            '📈 Risk Management & Mitigation'
        ],
        'technical_skills': [
          'Financial Accounting & Reporting',
          'Taxation (Direct & Indirect)',
          'Auditing & Assurance',
          'Financial Modeling (Excel, VBA)',
          'Corporate Finance & Valuation',
          'Investment Analysis (CFA Principles)',
          'Cost Accounting & Management',
          'ERP Systems (SAP, Oracle, Tally)',
          'Regulatory Compliance (SEBI, RBI)',
          'Risk Management',
          'Budgeting & Forecasting',
          'Mergers & Acquisitions'
       ],
        'future_scope': 'Corporate finance leadership, Investment banking, Financial consulting, Private equity, Hedge funds, CFO positions',
        'top_companies': [
            'Deloitte India - Mumbai, Delhi, Bengaluru', 'PwC India - Kolkata, Mumbai, Delhi',
            'KPMG India - Mumbai, Delhi, Bengaluru', 'EY India - Mumbai, Delhi, Bengaluru',
            'Goldman Sachs India - Bengaluru, Mumbai, Hyderabad', 'JP Morgan India - Mumbai, Bengaluru, Hyderabad',
            'Morgan Stanley India - Mumbai, Bengaluru', 'BlackRock India - Mumbai, Delhi, Bengaluru',
            'Avendus Capital - Mumbai, Bengaluru, Delhi', 'Kotak Investment Banking - Mumbai, Delhi, Bengaluru',
            'ICICI Securities - Mumbai, Delhi, Bengaluru, Chennai', 'HDFC Securities - Mumbai, Delhi, Bengaluru',
            'Institute of Chartered Accountants of India (ICAI) - New Delhi, Mumbai, Chennai, Kolkata, Bengaluru',
            'Indian Institutes of Management (IIMs) - Across India'
        ],
        'education_path': 'M.Com, MBA Finance, CA Final, CS Executive, CMA Final, CFA Level 3, CPA, PhD in Finance',
        'certifications': ['CA', 'CS', 'CMA', 'CFA', 'CPA', 'FRM', 'CIMA', 'ICWA', 'Certified Treasury Professional (CTP)'],
        'hiring_cities': ['Mumbai', 'Delhi NCR', 'Bengaluru', 'Chennai', 'Hyderabad', 'Pune', 'Kolkata', 'Ahmedabad', 'Gurugram', 'Noida', 'Jaipur', 'Lucknow', 'Chandigarh', 'Kochi', 'Indore']
    },

    # ==================== SPORTS & FITNESS INDUSTRY ====================
    'sports': {
        'name': 'Sports & Fitness Industry',
        'icon': '⚽',
        'description': 'This dynamic stream focuses on sports management, exercise science, fitness training, sports psychology, and athletic administration. Students learn about sports business, athlete development, fitness programming, and health promotion.',
        'careers': ['Sports Manager - Oversee sports organizations and teams', 'Fitness Trainer - Design and lead fitness programs', 'Sports Coach - Train athletes for competition', 'Sports Psychologist - Support athlete mental health', 'Exercise Physiologist - Study body response to exercise', 'Sports Nutritionist - Advise on athlete nutrition', 'Athletic Director - Manage school/college sports programs', 'Sports Marketing Manager - Promote sports brands and events', 'Physical Education Teacher - Teach sports in schools', 'Sports Agent - Represent professional athletes', 'Sports Event Coordinator - Organize sporting events', 'Sports Journalist - Cover sports news and events', 'Sports Data Analyst - Analyze athlete and team performance', 'Sports Facility Manager - Manage sports venues', 'Sports Rehabilitator - Help athletes recover from injuries', 'Personal Trainer - Provide one-on-one fitness training', 'Group Exercise Instructor - Lead fitness classes', 'Sports Scout - Identify talented athletes', 'Sports Biomechanist - Analyze athletic movement', 'Corporate Wellness Coordinator - Manage workplace fitness'],
        'subjects': ['Sports Management', 'Exercise Physiology', 'Sports Psychology', 'Biomechanics', 'Sports Nutrition', 'Fitness Programming', 'Sports Marketing', 'Event Management', 'Athletic Training', 'Sports Law', 'Sports Analytics', 'Strength and Conditioning', 'Sports Medicine', 'Physical Education', 'Health and Wellness'],
        'skills': ['Leadership and Team Management', 'Communication and Interpersonal Skills', 'Fitness Assessment and Programming', 'Data Analysis and Statistics', 'Event Planning and Organization', 'Sports Knowledge and Rules', 'Motivation and Coaching', 'Injury Prevention and First Aid', 'Marketing and Promotion', 'Business Management', 'Nutrition and Wellness Planning', 'Athlete Development', 'Sports Psychology Techniques', 'Strength and Conditioning Methods'],
        'software_skills': [
            '⚽ Sports Analytics: Hudl, Sportscode, Catapult, Kinduct, Kitman Labs',
            '📊 Data Analysis: Excel, Tableau, Python, R, SPSS for sports data',
            '🏋️ Fitness Tracking: MyFitnessPal, Trainerize, TrueCoach, PT Distinction',
            '📈 Performance Analysis: Dartfish, Kinovea, Silverback, Coachs Eye',
            '🎯 Sports Management: TeamSnap, LeagueApps, SportsEngine, Upper Hand',
            '📋 Nutrition Software: Nutrium, Nutritics, Cronometer, FoodWorks',
            '💪 Strength Training: BridgeAthletic, Volt Athletics, TeamBuildr'
        ],
        'career_skills': [
            '⚽ Leadership & Team Management',
            '🗣️ Communication & Interpersonal Skills',
            '📊 Fitness Assessment & Program Design',
            '🎯 Motivation & Coaching Excellence',
            '📈 Sports Psychology & Mental Training',
            '💪 Strength & Conditioning Expertise',
            '🤝 Event Planning & Organization',
            '🩺 Injury Prevention & First Aid'
        ],
        'technical_skills': [
          'Sports Training & Coaching Methods',
          'Exercise Physiology',
          'Sports Nutrition & Diet Planning',
          'Injury Prevention & Rehabilitation',
          'Strength & Conditioning Programming',
          'Sports Psychology Techniques',
          'Biomechanics Analysis',
          'Fitness Assessment & Testing',
          'First Aid & CPR',
          'Sports Management & Administration',
          'Performance Tracking & Analytics',
          'Yoga & Flexibility Training'
       ],
        'future_scope': 'Rapidly growing industry with opportunities in professional sports, fitness centers, schools, corporate wellness, and sports technology.',
        'top_companies': [
            'Sports Brands: Nike India - Bengaluru, Delhi, Mumbai', 'Adidas India - Gurugram, Mumbai, Bengaluru',
            'Puma India - Bengaluru, Mumbai, Delhi', 'Decathlon India - Across 90+ cities',
            'Sports Leagues: BCCI - Mumbai (IPL Teams across India)', 'ISL Teams - Across major cities',
            'Pro Kabaddi League Teams - Across India', 'Indian Olympic Association - New Delhi',
            'Sports Authority of India (SAI) - Delhi, Bengaluru, Patiala, Kolkata, Mumbai',
            'Gyms: Gold\'s Gym - Across India', 'Cult.fit - Bengaluru, Delhi, Mumbai, Chennai, Hyderabad, Pune',
            'Anytime Fitness - Across 30+ cities', 'Equinox - Mumbai, Delhi, Bengaluru',
            'Media: Star Sports - Mumbai', 'Sony Sports Network - Mumbai', 'ESPN India - Gurugram',
            'Fantasy Sports: Dream11 - Mumbai', 'My11Circle - Bengaluru', 'MPL - Bengaluru',
            'Fitness Tech: Fitbit India - Bengaluru', 'Cult.fit - Bengaluru'
        ],
        'education_path': 'B.Sc Sports Science, B.P.Ed (Physical Education), BBA in Sports Management, B.Sc Fitness and Nutrition, M.Sc Sports Psychology, MBA in Sports Management, Diploma in Fitness Training, Certification in Personal Training',
        'certifications': ['Certified Personal Trainer (CPT) - ACE, NASM, ACSM', 'Certified Strength and Conditioning Specialist (CSCS)', 'Certified Sports Nutritionist (ISSN)', 'First Aid and CPR Certification', 'Sports Management Certification (NASSM)', 'Certified Exercise Physiologist (ACSM-EP)', 'Certified Athletic Trainer (ATC)', 'Sports Coaching Certification (NSCA, IAAF)', 'Yoga and Wellness Certification', 'Group Exercise Instructor Certification (AFAA)', 'Corrective Exercise Specialist (CES)', 'Performance Enhancement Specialist (PES)'],
        'hiring_cities': ['Mumbai', 'Delhi NCR', 'Bengaluru', 'Chennai', 'Hyderabad', 'Pune', 'Kolkata', 'Ahmedabad', 'Jaipur', 'Chandigarh', 'Kochi', 'Goa', 'Lucknow', 'Indore', 'Bhubaneswar', 'Guwahati']
    },
    'sports_college': {
        'name': 'Sports & Fitness Industry (Advanced)',
        'icon': '⚽',
        'description': 'Advanced study in sports management, sports science, athletic administration, and high-performance training. Prepare for leadership roles in professional sports organizations, sports federations, elite athlete development, and sports technology.',
        'careers': ['Sports Director - Lead sports organizations', 'High Performance Manager - Manage elite athlete programs', 'Head Coach - Lead professional teams', 'Sports Psychologist - Work with elite athletes', 'Director of Sports Science - Lead research', 'Sports Technology Consultant - Advise on sports tech', 'Athletic Director - Lead university sports', 'Sports Marketing Director - Lead brand strategy', 'Sports Agent - Represent elite athletes', 'Head of Scouting - Lead talent identification', 'Sports Analytics Director - Lead data strategy', 'Fitness Technology Entrepreneur - Start fitness tech ventures'],
        'subjects': ['Advanced Sports Management', 'High Performance Training', 'Elite Athlete Development', 'Sports Technology & Innovation', 'Sports Analytics Advanced', 'Sports Medicine Advanced', 'Athletic Administration', 'Sports Law & Ethics', 'International Sports Governance', 'Sports Facility Management', 'Sports Marketing Strategy', 'Exercise Science Research'],
        'skills': ['Strategic Sports Leadership', 'High-Performance Management', 'Elite Athlete Development', 'Sports Analytics & Data Science', 'Sports Technology Innovation', 'Executive Communication', 'Crisis Management in Sports', 'International Sports Governance', 'Sports Business Strategy', 'Talent Identification & Development'],
        'software_skills': [
            '⚽ Advanced Analytics: Catapult Vector, Kinduct, Kitman Labs Pro',
            '📊 Performance Analysis: Hudl Pro, Sportscode Elite, Nacsport',
            '🤖 AI in Sports: Zone7, Kitman AI, Playermaker, ShotTracker',
            '📈 Biomechanics: Qualisys, Vicon, Noraxon, The Motion Monitor',
            '💪 Athlete Management: Smartabase, Fusion Sport, TeamBuildr Elite',
            '📋 Sports Medicine: SportsMED, PhysioBase, Rehab Guru',
            '🎯 Recruitment: Scout7, Wyscout, Instat Scouting, Hudl Recruitment'
        ],
        'career_skills': [
            '🎯 Strategic Sports Leadership',
            '📊 High-Performance Analytics',
            '💡 Sports Technology Innovation',
            '🌍 International Sports Governance',
            '👥 Elite Athlete Management',
            '🤝 Sports Business Strategy',
            '📈 Talent Identification & Development',
            '🩺 Sports Medicine & Rehabilitation'
        ],
        'technical_skills': [
          'Sports Training & Coaching Methods',
          'Exercise Physiology',
          'Sports Nutrition & Diet Planning',
          'Injury Prevention & Rehabilitation',
          'Strength & Conditioning Programming',
          'Sports Psychology Techniques',
          'Biomechanics Analysis',
          'Fitness Assessment & Testing',
          'First Aid & CPR',
          'Sports Management & Administration',
          'Performance Tracking & Analytics',
          'Yoga & Flexibility Training'
       ],
        'future_scope': 'Leadership roles in professional sports, sports technology, elite athlete development, sports science research, and international sports federations.',
        'top_companies': [
            'Sports Federations: BCCI - Mumbai', 'IOA - New Delhi', 'ISL - Mumbai',
            'NBA India - Mumbai, Delhi, Bengaluru', 'FIFA India Office - Delhi',
            'Sports Technology: Hudl India - Bengaluru', 'Catapult Sports - Bengaluru',
            'Kinduct - Remote India', 'Playermaker - Remote',
            'Professional Teams: IPL Teams (MI, CSK, RCB, KKR, etc.)',
            'ISL Teams (ATK Mohun Bagan, Bengaluru FC, Mumbai City FC, etc.)',
            'Pro Kabaddi Teams (Patna Pirates, Bengaluru Bulls, etc.)',
            'Sports NGOs: Olympic Gold Quest - Mumbai, Bengaluru',
            'Go Sports Foundation - Bengaluru', 'Rise Worldwide - Mumbai',
            'Consulting: Deloitte Sports Business - Mumbai/Delhi',
            'PwC Sports Advisory - Mumbai/Delhi', 'KPMG Sports - Mumbai/Delhi/Bengaluru'
        ],
        'education_path': 'M.Sc Sports Science, MBA in Sports Management, M.P.Ed (Master of Physical Education), PhD in Sports Science, Post Graduate Diploma in Sports Management, Executive MBA in Sports Business',
        'certifications': ['Advanced Personal Trainer Certification', 'Certified Strength and Conditioning Specialist (CSCS) - Advanced', 'Sports Nutrition Specialist (SNS)', 'Certified Sports Psychologist', 'Advanced Sports Management Certification', 'Sports Analytics Professional Certification', 'FIFA/IOA Coaching Certifications', 'Sports Medicine Certification', 'Doping Control Officer Certification'],
        'hiring_cities': ['Mumbai', 'Delhi NCR', 'Bengaluru', 'Chennai', 'Hyderabad', 'Pune', 'Kolkata', 'Ahmedabad', 'Goa', 'Chandigarh', 'Jaipur', 'Lucknow', 'Kochi', 'Bhubaneswar', 'Guwahati', 'Patna']
    },
    # ==================== RETAIL & E-COMMERCE STREAM ====================
  'retail_ecommerce': {
    'name': 'Retail & E-commerce',
    'icon': '🛒',
    'description': 'This dynamic stream focuses on retail management, e-commerce operations, digital marketing, supply chain logistics, and customer experience. Students learn about online marketplaces, inventory management, omnichannel retail, and consumer behavior in the digital age.',
    'careers': [
        'E-commerce Manager - Oversee online sales operations',
        'Retail Store Manager - Manage physical retail locations',
        'Digital Marketing Specialist - Drive online customer acquisition',
        'Supply Chain Analyst - Optimize logistics and inventory',
        'Merchandise Planner - Plan product assortment and pricing',
        'Customer Experience Manager - Enhance shopping experience',
        'Product Manager - Manage online product catalogs',
        'Logistics Coordinator - Coordinate shipping and delivery',
        'Category Manager - Manage product categories',
        'Social Media Manager - Manage brand presence online',
        'Data Analyst - Analyze sales and customer data',
        'Warehouse Operations Manager - Manage fulfillment centers'
    ],
    'subjects': [
        'Retail Management',
        'E-commerce Operations',
        'Digital Marketing',
        'Supply Chain Management',
        'Inventory Management',
        'Customer Relationship Management',
        'Web Analytics',
        'Online Payment Systems',
        'Logistics and Fulfillment',
        'Consumer Behavior',
        'Merchandising',
        'Omnichannel Retail'
    ],
    'skills': [
        'Digital Marketing (SEO, SEM, Social Media)',
        'Data Analysis and Analytics',
        'Inventory Management',
        'Customer Service Excellence',
        'Supply Chain Optimization',
        'Project Management',
        'E-commerce Platform Management',
        'Negotiation Skills',
        'Financial Planning',
        'Team Leadership',
        'Problem Solving'
    ],
    'technical_skills': [
        'E-commerce Platforms (Shopify, Magento, WooCommerce)',
        'Digital Marketing Tools (Google Analytics, Facebook Ads)',
        'CRM Software (Salesforce, Zendesk)',
        'Inventory Management Systems',
        'Payment Gateway Integration',
        'Data Analytics (Excel, Tableau, SQL)'
    ],
    'software_skills': [
        'Shopify / Magento',
        'Google Analytics',
        'Meta Business Suite',
        'Email Marketing Tools (Mailchimp)',
        'CRM Software',
        'MS Excel / Google Sheets',
        'ERP Systems (SAP, Oracle)'
    ],
    'career_skills': [
        'Customer Focus',
        'Analytical Thinking',
        'Communication Skills',
        'Problem Solving',
        'Adaptability',
        'Leadership',
        'Time Management',
        'Negotiation Skills'
    ],
    'future_scope': 'Explosive growth in online retail, digital commerce, and omnichannel experiences. High demand for e-commerce professionals, digital marketers, and supply chain experts. Indian e-commerce market expected to reach $350 billion by 2030.',
    'top_companies': [
        'Amazon India - Bengaluru, Hyderabad, Delhi NCR, Mumbai, Chennai, Pune, Kolkata, Ahmedabad',
        'Flipkart Group - Bengaluru, Delhi NCR, Mumbai, Chennai, Hyderabad, Kolkata, Pune',
        'Meesho - Bengaluru, Delhi NCR, Mumbai, Chennai, Hyderabad, Pune, Kolkata',
        'Nykaa - Mumbai, Delhi NCR, Bengaluru, Chennai, Hyderabad, Pune, Kolkata',
        'Myntra - Bengaluru, Delhi NCR, Mumbai, Chennai, Hyderabad, Pune, Kolkata',
        'Tata Cliq - Mumbai, Bengaluru, Delhi NCR, Kolkata, Chennai',
        'Ajio - Mumbai, Bengaluru, Delhi NCR, Kolkata, Chennai, Hyderabad',
        'Reliance Retail - Mumbai, Delhi NCR, Bengaluru, Chennai, Hyderabad, Kolkata, Pune, Ahmedabad',
        'BigBasket - Bengaluru, Delhi NCR, Mumbai, Chennai, Hyderabad, Pune, Kolkata, Ahmedabad',
        'Zepto - Mumbai, Bengaluru, Delhi NCR, Chennai, Hyderabad, Pune, Kolkata',
        'Blinkit - Gurugram, Delhi NCR, Mumbai, Bengaluru, Chennai, Hyderabad, Pune',
        'Swiggy Instamart - Bengaluru, Delhi NCR, Mumbai, Chennai, Hyderabad, Pune, Kolkata',
        'Zomato - Gurugram, Delhi NCR, Mumbai, Bengaluru, Chennai, Hyderabad, Pune',
        'Unicommerce - Delhi NCR, Mumbai, Bengaluru',
        'Shiprocket - Delhi NCR, Bengaluru, Mumbai',
        'Shopify India - Mumbai, Delhi NCR, Bengaluru',
        'Walmart Global Tech - Bengaluru, Chennai'
    ],
    'hiring_cities': ['Bengaluru', 'Delhi NCR', 'Mumbai', 'Hyderabad', 'Chennai', 'Pune', 'Kolkata', 'Ahmedabad', 'Jaipur', 'Lucknow', 'Chandigarh', 'Indore', 'Kochi', 'Goa'],
    'education_path': 'BBA in Retail Management, BBA in E-commerce, B.Com, MBA in Marketing/Operations, Diploma in Digital Marketing, Certification in E-commerce Management, B.Tech CS (for technical roles)',
    'certifications': [
        'Google Digital Marketing Certification',
        'Shopify Partner Certification',
        'Facebook Blueprint Certification',
        'Amazon Seller Central Certification',
        'Google Analytics Certification',
        'HubSpot E-commerce Certification',
        'Certified E-commerce Consultant',
        'Supply Chain Management Certification',
        'Digital Marketing Master Certification'
    ]
  },
  'retail_ecommerce_college': {
    'name': 'Retail & E-commerce (Advanced)',
    'icon': '🛒',
    'description': 'Advanced study in retail strategy, e-commerce technology, omnichannel integration, and digital transformation. Prepare for leadership roles in online retail, marketplace management, and retail technology innovation.',
    'careers': [
        'Chief E-commerce Officer - Lead e-commerce strategy',
        'Head of Digital Retail - Oversee digital channels',
        'E-commerce Director - Manage online business growth',
        'Retail Technology Consultant - Advise on retail tech',
        'Digital Transformation Manager - Lead retail innovation',
        'Head of Marketplace Operations - Manage online marketplaces',
        'Customer Analytics Manager - Analyze customer behavior',
        'Supply Chain Director - Lead logistics strategy',
        'E-commerce Platform Architect - Design e-commerce systems',
        'Head of Omnichannel Retail - Integrate online and offline',
        'Retail Data Scientist - Drive data-based decisions',
        'Digital Payments Head - Manage payment solutions'
    ],
    'subjects': [
        'Advanced E-commerce Strategy',
        'Retail Analytics and BI',
        'Omnichannel Retail Management',
        'Digital Supply Chain',
        'Customer Data Platforms',
        'E-commerce Technology Stack',
        'Marketplace Dynamics',
        'Last-Mile Logistics',
        'Retail Fintech',
        'Digital Customer Experience',
        'Retail AI and Automation',
        'International E-commerce'
    ],
    'skills': [
        'Strategic Leadership',
        'Advanced Data Analytics',
        'Digital Transformation',
        'E-commerce Platform Architecture',
        'Omnichannel Integration',
        'Customer Journey Optimization',
        'Revenue Management',
        'Team Leadership',
        'Vendor Negotiation',
        'International Trade Knowledge',
        'Risk Management'
    ],
    'technical_skills': [
        'E-commerce Platform Architecture',
        'Data Analytics & Business Intelligence',
        'Customer Data Platforms (CDP)',
        'Marketing Automation',
        'AI/ML in Retail',
        'Payment Gateway Integration',
        'Supply Chain Optimization'
    ],
    'software_skills': [
        'Salesforce Commerce Cloud',
        'Adobe Commerce (Magento)',
        'Shopify Plus',
        'Tableau / PowerBI',
        'Google Analytics 4',
        'AWS/Azure Cloud Platforms',
        'SAP Hybris'
    ],
    'career_skills': [
        'Strategic Thinking',
        'Executive Leadership',
        'Change Management',
        'Stakeholder Management',
        'Crisis Management',
        'Innovation Management',
        'Financial Acumen'
    ],
    'future_scope': 'Leadership positions in e-commerce companies, retail chains, digital agencies, and technology firms. Growing demand for omnichannel experts and retail technology leaders. Indian e-commerce market projected to reach $350 billion by 2030.',
    'top_companies': [
        'Amazon India - Bengaluru, Hyderabad, Delhi NCR',
        'Flipkart Group - Bengaluru, Delhi NCR',
        'Walmart Global Tech - Bengaluru, Chennai',
        'Tata Digital - Mumbai, Bengaluru',
        'Reliance Retail - Mumbai, Bengaluru, Delhi NCR',
        'Meesho - Bengaluru',
        'Nykaa - Mumbai, Bengaluru',
        'Shopify Plus - Mumbai, Delhi NCR, Bengaluru',
        'Salesforce Commerce Cloud - Hyderabad, Bengaluru',
        'Adobe Commerce - Bengaluru, Noida',
        'Razorpay (E-commerce Payments) - Bengaluru',
        'Unilever Digital - Mumbai, Bengaluru',
        'Nestle E-commerce - Gurugram, Bengaluru',
        'P&G Digital - Mumbai, Bengaluru'
    ],
    'hiring_cities': ['Bengaluru', 'Mumbai', 'Delhi NCR', 'Hyderabad', 'Chennai', 'Pune', 'Kolkata', 'Gurugram', 'Noida'],
    'education_path': 'MBA in E-commerce/Digital Business, M.Com in E-commerce, PG Diploma in Digital Retail Management, Executive MBA in Retail Management',
    'certifications': [
        'Certified E-commerce Professional (CEP)',
        'Advanced Google Analytics Certification',
        'Shopify Plus Certification',
        'Salesforce Commerce Cloud Certification',
        'Adobe Commerce Certification',
        'Certified Digital Supply Chain Professional',
        'Retail Management Advanced Certification'
    ]
  },
  'environment_agriculture': {
    'name': 'Environment, Agriculture & Earth Sciences',
    'icon': '🌍',
    'description': 'This vital stream focuses on environmental science, agriculture, earth sciences, and sustainable development. Students learn about climate change, conservation, food security, natural resources, and how to protect our planet for future generations. Career opportunities include environmental scientist, agricultural engineer, geologist, climate change analyst, conservation scientist, soil scientist, hydrologist, environmental consultant, and sustainable agriculture specialist.',
    'careers': [
        'Environmental Scientist - Study and protect the environment',
        'Agricultural Engineer - Design sustainable farming solutions',
        'Geologist - Study Earth\'s structure and materials',
        'Climate Change Analyst - Research climate patterns and solutions',
        'Conservation Scientist - Protect natural resources and wildlife',
        'Soil Scientist - Study soil composition and management',
        'Hydrologist - Study water resources and distribution',
        'Environmental Consultant - Advise on environmental compliance',
        'Sustainable Agriculture Specialist - Promote eco-friendly farming',
        'Renewable Energy Specialist - Develop clean energy solutions'
    ],
    'subjects': [
        'Environmental Science', 'Agricultural Science', 'Geology', 'Meteorology',
        'Soil Science', 'Hydrology', 'Ecology', 'Climate Science',
        'Renewable Energy', 'Sustainable Development', 'Natural Resource Management',
        'Conservation Biology', 'Environmental Chemistry', 'Agronomy'
    ],
    'skills': [
        'Research and Data Analysis', 'Field Work and Sampling Techniques',
        'GIS and Remote Sensing', 'Laboratory Analysis', 'Environmental Impact Assessment',
        'Problem Solving', 'Critical Thinking', 'Communication and Report Writing',
        'Project Management', 'Sustainability Planning', 'Climate Modeling'
    ],
    'technical_skills': [
        'Environmental Impact Assessment (EIA)',
        'Geographic Information Systems (GIS)',
        'Remote Sensing & Mapping',
        'Water & Air Quality Testing',
        'Soil Analysis & Remediation',
        'Climate Modeling & Forecasting',
        'Ecology & Biodiversity Assessment',
        'Waste Management Techniques',
        'Renewable Energy Systems',
        'Environmental Chemistry',
        'Conservation Biology',
        'Sustainable Development Planning'
    ],
    'software_skills': [
        'ArcGIS / QGIS',
        'Python / R Programming',
        'SPSS / SAS',
        'AutoCAD',
        'ERDAS Imagine',
        'ENVI'
    ],
    'career_skills': [
        'Critical Thinking',
        'Problem Solving',
        'Communication',
        'Teamwork',
        'Project Management',
        'Attention to Detail',
        'Environmental Ethics'
    ],
    'future_scope': 'High demand in environmental consulting, renewable energy, sustainable agriculture, climate research, government agencies, NGOs, and international organizations. India is focusing on sustainable development, climate action, and green jobs.',
    'top_companies': [
        'Indian Council of Agricultural Research (ICAR) - New Delhi',
        'Indian Institute of Soil Science - Bhopal',
        'Central Ground Water Board - Faridabad',
        'Geological Survey of India - Kolkata',
        'Indian Meteorological Department - Pune',
        'Wildlife Institute of India - Dehradun',
        'The Energy and Resources Institute (TERI) - New Delhi',
        'World Wildlife Fund (WWF) India - New Delhi',
        'Greenpeace India - Bengaluru',
        'Centre for Science and Environment - New Delhi'
    ],
    'hiring_cities': ['Delhi NCR', 'Bengaluru', 'Pune', 'Chennai', 'Kolkata', 'Hyderabad', 'Dehradun', 'Bhopal', 'Ahmedabad', 'Lucknow'],
    'education_path': 'B.Sc Environmental Science, B.Sc Agriculture, B.Sc Geology, B.Tech Environmental Engineering, M.Sc in related fields, PhD for research positions',
    'certifications': [
        'LEED Green Associate',
        'Certified Environmental Professional (CEP)',
        'GIS Professional Certification',
        'Certified Crop Advisor (CCA)',
        'Environmental Impact Assessment Certification',
        'Climate Change Professional Certification',
        'Sustainable Agriculture Certification'
    ]
  },
  'service_hospitality': {
    'name': 'Services, Hospitality & Public Safety',
    'icon': '🏨',
    'description': 'This dynamic stream focuses on customer service, hotel management, tourism, event planning, and public safety services including police, fire, emergency response, and disaster management. Students learn about hospitality operations, guest relations, safety protocols, and serving the community. This field offers diverse career opportunities in hotels, restaurants, travel agencies, event management companies, government agencies, and emergency services.',
    'careers': [
        'Hotel Manager - Oversee hotel operations and guest services',
        'Restaurant Manager - Manage food and beverage operations',
        'Event Manager - Plan and execute events',
        'Tourism Officer - Promote travel and tourism',
        'Customer Service Manager - Lead customer support teams',
        'Police Officer - Maintain law and order',
        'Firefighter - Respond to fire emergencies',
        'Emergency Medical Technician - Provide emergency medical care',
        'Disaster Management Specialist - Coordinate disaster response',
        'Security Manager - Manage security operations'
    ],
    'subjects': [
        'Hotel Management', 'Food & Beverage Management', 'Tourism Management',
        'Event Planning', 'Customer Relationship Management', 'Public Safety Administration',
        'Emergency Response', 'Disaster Management', 'Fire Safety', 'Security Management'
    ],
    'skills': [
        'Customer Service Excellence', 'Communication (Multiple Languages)',
        'Leadership & Team Management', 'Problem Solving', 'Crisis Management',
        'Attention to Detail', 'Time Management', 'Stress Management',
        'Conflict Resolution', 'Emergency Response', 'First Aid & CPR'
    ],
    'technical_skills': [
        'Property Management Systems (PMS - Opera, IDS, WinHms)',
        'Point of Sale (POS) Systems',
        'Security Systems (CCTV, Access Control)',
        'Emergency Response Equipment',
        'Fire Safety Equipment',
        'Communication Systems',
        'Reservation Systems (CRS, GDS)',
        'Event Management Software',
        'Customer Relationship Management (CRM)',
        'Hotel Accounting Software',
        'Inventory Management Systems',
        'Tourism Management Systems'
    ],
    'software_skills': [
        'Hotel PMS (Opera, IDS, WinHms)',
        'Restaurant POS Systems',
        'Event Management Software',
        'CRM Software',
        'Microsoft Office Suite'
    ],
    'career_skills': [
        'Customer Focus', 'Communication', 'Leadership', 'Problem Solving',
        'Teamwork', 'Adaptability', 'Stress Management', 'Attention to Detail'
    ],
    'future_scope': 'Growing tourism industry (Incredible India campaign), hotel chain expansion, event management boom, government focus on tourism infrastructure, Smart City safety initiatives, disaster management authorities strengthening.',
    'top_companies': [
        'Taj Hotels - Across India', 'Oberoi Hotels - Delhi/Mumbai/Bengaluru',
        'ITC Hotels - Across India', 'Marriott India - Across India',
        'Hyatt India - Across India', 'Leela Palaces - Across India',
        'Indian Police Service - All State Capitals',
        'National Disaster Response Force (NDRF) - Delhi',
        'Indian Fire Service - All Major Cities',
        'MakeMyTrip - Gurugram', 'Yatra.com - Gurugram'
    ],
    'hiring_cities': ['Mumbai', 'Delhi NCR', 'Bengaluru', 'Goa', 'Jaipur', 'Chennai', 'Hyderabad', 'Kolkata', 'Pune', 'Ahmedabad'],
    'education_path': 'BBA in Hotel Management, B.Sc in Hospitality, BHMCT, MBA in Hospitality, Diploma in Hotel Management, BBA in Event Management, BA in Tourism Management, B.Sc in Public Safety',
    'certifications': [
        'Certified Hotel Administrator (CHA)', 'Certified Hospitality Supervisor (CHS)',
        'ServSafe Food Safety Certification', 'HACCP Certification',
        'Certified Event Planner (CEP)', 'Certified Tourism Professional (CTP)',
        'Fire Safety Certification', 'First Aid & CPR Certification'
    ]
  }

}
def get_stream_details(stream_id, user_type='school'):
    """Get stream details from the database - handles all possible stream IDs"""
    
    # First, try exact match
    if stream_id in STREAM_DETAILS_DB:
        return STREAM_DETAILS_DB[stream_id]
    
    # Try without _college suffix
    lookup_id = stream_id.replace('_college', '')
    if lookup_id in STREAM_DETAILS_DB:
        return STREAM_DETAILS_DB[lookup_id]
    
    # Try partial matches for common patterns
    stream_mappings = {
        'tech': 'tech_engineering', 'engineering': 'tech_engineering', 'technology': 'tech_engineering', 'computer': 'computer_science',
        'business': 'business_finance', 'finance': 'business_finance', 'commerce': 'commerce',
        'health': 'health_sciences', 'medical': 'health_sciences', 'medicine': 'health_sciences',
        'creative': 'creative_arts', 'arts': 'arts_humanities', 'design': 'creative_arts',
        'manufacturing': 'manufacturing', 'production': 'manufacturing',
        'construction': 'construction', 'civil': 'construction',
        'agriculture': 'agriculture', 'farming': 'agriculture',
        'math': 'mathematics', 'mathematics': 'mathematics', 'statistics': 'mathematics',
        'physics': 'physics', 'chemistry': 'chemistry', 'biology': 'biology',
        'life_sciences': 'biology', 'law': 'law', 'legal': 'law',
        'humanities': 'arts_humanities', 'economics': 'economics', 'psychology': 'psychology',
        'social': 'social_work', 'service': 'service_hospitality', 'hospitality': 'service_hospitality', 'hotel': 'service_hospitality','tourism': 'service_hospitality',
        'event': 'service_hospitality',
        'safety': 'service_hospitality',
        'police': 'service_hospitality',
        'fire': 'service_hospitality',
        'emergency': 'service_hospitality',
        'security': 'service_hospitality',
        'energy': 'energy_utilities', 'utilities': 'energy_utilities', 'power': 'energy_utilities', 'solar': 'energy_utilities',
        'wind': 'energy_utilities',
        'renewable': 'energy_utilities',
        'oil': 'energy_utilities',
        'gas': 'energy_utilities',
        'petroleum': 'energy_utilities',
        'environment': 'environment_agriculture',
        'agriculture': 'environment_agriculture',
        'earth': 'environment_agriculture',
        'ecology': 'environment_agriculture',
        'climate': 'environment_agriculture',
        'sustainability': 'environment_agriculture',
        'farming': 'environment_agriculture',
        'horticulture': 'environment_agriculture',
        'forestry': 'environment_agriculture',
        'conservation': 'environment_agriculture',
        'renewable': 'environment_agriculture',
        'geology': 'environment_agriculture',
        'enviro': 'environment_agriculture',
        'agri': 'environment_agriculture',
        'soil': 'environment_agriculture',
        'water': 'environment_agriculture',
        'natural_resources': 'environment_agriculture',
        'wildlife': 'environment_agriculture',
        'retail': 'retail',
        'e-commerce': 'retail_college',
        'online_retail': 'retail_college',
        'emarketplace': 'retail_college',
        'marketplace': 'retail_college',
        'digital_retail': 'retail_college',
        'omnichannel': 'retail_college',
        'flipkart': 'retail_college',
        'amazon': 'retail_college',
        'shopify': 'retail_college',
        'myntra': 'retail_college',
        'nykaa': 'retail_college',
        'meesho': 'retail_college',
        'warehouse': 'retail_college',
        'logistics': 'retail_college',
        'supply_chain': 'retail_college',
        'last_mile': 'retail_college',
        'fulfillment': 'retail_college',
        'dropshipping': 'retail_college',
        'quick_commerce': 'retail_college',
        'accounting': 'accounting',
        'accounting_college': 'accounting_college',
        'finance': 'accounting_college',
        'account': 'accounting_college',
        'accounts': 'accounting_college',
        'ca': 'accounting_college',
        'cpa': 'accounting_college',
        'cfa': 'accounting_college',
        'cma': 'accounting_college',
        'audit': 'accounting_college',
        'tax': 'accounting_college',
        'financial_analysis': 'accounting_college',
        'investment_banking': 'accounting_college',
        'wealth_management': 'accounting_college',
        'risk_management': 'accounting_college',
        'forensic_accounting': 'accounting_college',
        'corporate_finance': 'accounting_college',
        'treasury': 'accounting_college',
        'bookkeeping': 'accounting_college',
        'sports': 'sports',
    'sports_college': 'sports_college',
    'fitness': 'fitness',
    'sport': 'sports_college',
    'gym': 'sports_college',
    'workout': 'sports_college',
    'athletics': 'sports_college',
    'exercise': 'sports_college',
    'wellness': 'sports_college',
    'health_fitness': 'sports_college',
    'physical_education': 'sports_college',
    'pe': 'sports_college',
    'coaching': 'sports_college',
    'training': 'sports_college',
    'athlete': 'sports_college',
    'sports_management': 'sports_college',
    'sports_psychology': 'sports_college',
    'exercise_physiology': 'sports_college',
    'kinesiology': 'sports_college',
    'sports_science': 'sports_college',
    'personal_training': 'sports_college',
    'group_fitness': 'sports_college',
    'yoga': 'sports_college',
    'pilates': 'sports_college',
    'zumba': 'sports_college',
    'crossfit': 'sports_college',
    'bodybuilding': 'sports_college',
    'sports_nutrition': 'sports_college',
    'sports_medicine': 'sports_college',
    'athletic_training': 'sports_college',
    'cricket': 'sports_college',
    'football': 'sports_college',
    'soccer': 'sports_college',
    'basketball': 'sports_college',
    'tennis': 'sports_college',
    'swimming': 'sports_college',
    'badminton': 'sports_college',
    'hockey': 'sports_college',
    'volleyball': 'sports_college',
    'retail': 'retail_ecommerce',
    'ecommerce': 'retail_ecommerce',
    'e-commerce': 'retail_ecommerce',
    'online_retail': 'retail_ecommerce',
    'shopify': 'retail_ecommerce',
    'amazon': 'retail_ecommerce',
    'flipkart': 'retail_ecommerce',
    'nykaa': 'retail_ecommerce',
    'meesho': 'retail_ecommerce',
    'warehouse': 'retail_ecommerce',
    'logistics': 'retail_ecommerce',
    'supply_chain': 'retail_ecommerce'
    }
    
    # Check if any key in stream_id matches the mappings
    stream_id_lower = stream_id.lower()
    for key, mapped_id in stream_mappings.items():
        if key in stream_id_lower:
            return STREAM_DETAILS_DB.get(mapped_id)
    
    # Return None if not found (will show fallback)
    return None

# ==================== CITY-STATE DATABASE AND LOCATION FUNCTIONS ====================

# Map cities to their states and regions
CITY_STATE_MAP = {
    'mumbai': 'Maharashtra', 'pune': 'Maharashtra', 'nagpur': 'Maharashtra', 'nasik': 'Maharashtra',
    'delhi': 'Delhi NCR', 'gurugram': 'Haryana', 'noida': 'Uttar Pradesh', 'faridabad': 'Haryana',
    'bengaluru': 'Karnataka', 'bangalore': 'Karnataka', 'mysore': 'Karnataka', 'mangalore': 'Karnataka',
    'chennai': 'Tamil Nadu', 'coimbatore': 'Tamil Nadu', 'madurai': 'Tamil Nadu', 'salem': 'Tamil Nadu', 'hosur': 'Tamil Nadu',
    'hyderabad': 'Telangana', 'secunderabad': 'Telangana', 'warangal': 'Telangana',
    'kolkata': 'West Bengal', 'howrah': 'West Bengal', 'durgapur': 'West Bengal',
    'ahmedabad': 'Gujarat', 'vadodara': 'Gujarat', 'surat': 'Gujarat', 'rajkot': 'Gujarat', 'gandhinagar': 'Gujarat',
    'jaipur': 'Rajasthan', 'jodhpur': 'Rajasthan', 'udaipur': 'Rajasthan', 'kota': 'Rajasthan',
    'lucknow': 'Uttar Pradesh', 'kanpur': 'Uttar Pradesh', 'agra': 'Uttar Pradesh', 'varanasi': 'Uttar Pradesh',
    'kochi': 'Kerala', 'thiruvananthapuram': 'Kerala', 'kozhikode': 'Kerala', 'kollam': 'Kerala',
    'vizag': 'Andhra Pradesh', 'visakhapatnam': 'Andhra Pradesh', 'vijayawada': 'Andhra Pradesh', 'guntur': 'Andhra Pradesh',
    'bhubaneswar': 'Odisha', 'cuttack': 'Odisha', 'rourkela': 'Odisha',
    'indore': 'Madhya Pradesh', 'bhopal': 'Madhya Pradesh', 'gwalior': 'Madhya Pradesh', 'jabalpur': 'Madhya Pradesh',
    'chandigarh': 'Chandigarh', 'mohali': 'Punjab', 'ludhiana': 'Punjab', 'amritsar': 'Punjab',
    'goa': 'Goa', 'panaji': 'Goa', 'margao': 'Goa',
    'ranchi': 'Jharkhand', 'jamshedpur': 'Jharkhand', 'dhanbad': 'Jharkhand',
    'patna': 'Bihar', 'gaya': 'Bihar', 'bhagalpur': 'Bihar',
    'guwahati': 'Assam', 'dibrugarh': 'Assam', 'silchar': 'Assam',
}

# Major hiring hubs by region
HIRING_HUBS = {
    'Maharashtra': ['Mumbai', 'Pune', 'Nagpur', 'Nashik', 'Thane'],
    'Delhi NCR': ['Delhi', 'Gurugram', 'Noida', 'Faridabad', 'Ghaziabad'],
    'Karnataka': ['Bengaluru', 'Mysore', 'Mangalore', 'Hubli'],
    'Tamil Nadu': ['Chennai', 'Coimbatore', 'Madurai', 'Salem', 'Hosur'],
    'Telangana': ['Hyderabad', 'Secunderabad', 'Warangal'],
    'West Bengal': ['Kolkata', 'Howrah', 'Salt Lake City', 'Durgapur'],
    'Gujarat': ['Ahmedabad', 'Vadodara', 'Surat', 'Rajkot', 'Gandhinagar'],
    'Rajasthan': ['Jaipur', 'Jodhpur', 'Udaipur', 'Kota'],
    'Uttar Pradesh': ['Lucknow', 'Noida', 'Kanpur', 'Agra', 'Varanasi'],
    'Kerala': ['Kochi', 'Thiruvananthapuram', 'Kozhikode', 'Kollam'],
    'Andhra Pradesh': ['Visakhapatnam', 'Vijayawada', 'Guntur', 'Tirupati'],
    'Odisha': ['Bhubaneswar', 'Cuttack', 'Rourkela'],
    'Madhya Pradesh': ['Indore', 'Bhopal', 'Gwalior', 'Jabalpur'],
    'Punjab': ['Chandigarh', 'Ludhiana', 'Amritsar', 'Mohali'],
    'Goa': ['Panaji', 'Margao', 'Vasco da Gama'],
    'Jharkhand': ['Ranchi', 'Jamshedpur', 'Dhanbad'],
    'Bihar': ['Patna', 'Gaya', 'Bhagalpur'],
    'Assam': ['Guwahati', 'Dibrugarh', 'Silchar'],
    'Other': ['Jaipur', 'Lucknow', 'Indore', 'Bhopal', 'Chandigarh', 'Kochi', 'Vizag', 'Bhubaneswar']
}

def get_user_state(city):
    """Get state name from city name"""
    city_lower = city.lower().strip()
    if city_lower in CITY_STATE_MAP:
        return CITY_STATE_MAP[city_lower]
    # Try partial match
    for key, state in CITY_STATE_MAP.items():
        if key in city_lower or city_lower in key:
            return state
    return None

def filter_companies_by_location(companies_list, user_city, user_state):
    """Filter companies based on user's location"""
    user_city_lower = user_city.lower().strip()
    user_state_lower = user_state.lower().strip()
    
    local_companies = []
    same_state_companies = []
    other_companies = []
    
    for company in companies_list:
        company_lower = company.lower()
        
        # Check if company is in user's city
        if user_city_lower in company_lower:
            local_companies.append(company)
        # Check if company is in user's state (but different city)
        elif user_state_lower in company_lower:
            same_state_companies.append(company)
        else:
            other_companies.append(company)
    
    return local_companies, same_state_companies, other_companies

def get_hiring_cities_near_user(user_city, user_state):
    """Get hiring cities near user's location"""
    user_state_hubs = HIRING_HUBS.get(user_state, HIRING_HUBS['Other'])
    
    # Separate user's city from other cities in the same state
    user_city_lower = user_city.lower().strip()
    user_city_hub = None
    other_cities = []
    
    for hub in user_state_hubs:
        if hub.lower() == user_city_lower or user_city_lower in hub.lower():
            user_city_hub = hub
        else:
            other_cities.append(hub)
    
    # Also include major hubs from neighboring states
    all_major_hubs = ['Mumbai', 'Bengaluru', 'Hyderabad', 'Chennai', 'Delhi NCR', 'Pune', 'Kolkata', 'Ahmedabad']
    nearby_hubs = []
    
    for hub in all_major_hubs:
        if hub.lower() not in user_city_lower and hub not in other_cities:
            nearby_hubs.append(hub)
    
    return user_city_hub, other_cities, nearby_hubs
# ============ COMPLETE CAREER DETAILS DATABASE - INDIAN COMPANIES & SALARIES ============
# All 18 streams covered with detailed career information

CAREER_DETAILS_DB = {
    # ==================== 1. TECHNOLOGY & ENGINEERING CAREERS ====================
    'Software Engineer': {
        'description': 'Software engineers design, develop, and maintain software applications. They work on everything from mobile apps to large enterprise systems for Indian IT companies and MNCs in India.',
        'skills': ['Programming (Java, Python, C++, JavaScript)', 'Problem Solving', 'Debugging', 'Version Control (Git)', 'Database Management (SQL, MongoDB)', 'System Design', 'API Development', 'Testing & Deployment'],
        'salary_range': '₹4,00,000 - ₹30,00,000 per year (Entry: ₹3-6 LPA, Mid: ₹10-18 LPA, Senior: ₹20-35 LPA, Principal: ₹40+ LPA)',
        'education': 'B.Tech/BE in Computer Science, BCA, MCA, B.Sc Computer Science, M.Tech',
        'growth': 'Excellent growth in Indian IT sector - 15-20% annual salary growth with experience',
        'top_companies': ['Infosys - Bengaluru/Mysore/Pune', 'TCS - Mumbai/Chennai/Bengaluru', 'Wipro - Bengaluru/Hyderabad', 'HCL - Noida/Chennai', 'Tech Mahindra - Pune/Bengaluru', 'LTIMindtree - Bengaluru/Pune', 'Mphasis - Bengaluru/Pune', 'Persistent Systems - Pune/Nagpur'],
        'indian_hubs': ['Bengaluru (Silicon Valley of India)', 'Hyderabad (Cyberabad)', 'Pune', 'Chennai', 'Mumbai', 'Delhi NCR', 'Kolkata', 'Ahmedabad']
    },
    'Data Scientist': {
        'description': 'Data scientists analyze complex data to help Indian organizations make better decisions. They use statistical methods, machine learning, and data visualization to extract insights from big data.',
        'skills': ['Python/R Programming', 'Statistics & Probability', 'Machine Learning', 'Data Visualization (Tableau, PowerBI)', 'SQL', 'Big Data Tools (Hadoop, Spark)', 'Deep Learning (TensorFlow, PyTorch)', 'Business Intelligence'],
        'salary_range': '₹8,00,000 - ₹45,00,000 per year (Entry: ₹6-10 LPA, Mid: ₹15-25 LPA, Senior: ₹28-40 LPA, Lead: ₹45+ LPA)',
        'education': "Master's or PhD in Data Science, Statistics, Computer Science, or related field; B.Tech with certification acceptable",
        'growth': 'Very high demand - India has 30% annual growth in data science jobs, 40-50% salary jump with 2-3 years experience',
        'top_companies': ['Mu Sigma - Bengaluru', 'Fractal Analytics - Mumbai/Bengaluru', 'Tiger Analytics - Chennai/Bengaluru/Hyderabad', 'LatentView Analytics - Chennai/Bengaluru/Princeton', 'Absolutdata - Gurugram/Bengaluru', 'Incedo - Gurugram/Chennai/Bengaluru', 'Gramener - Bengaluru', 'Bridgei2i - Bengaluru', 'Quantiphi - Mumbai/Bengaluru', 'ZS Associates - Pune/Bengaluru/Delhi'],
        'indian_hubs': ['Bengaluru', 'Mumbai', 'Hyderabad', 'Pune', 'Chennai', 'Gurugram', 'Delhi NCR', 'Kolkata']
    },
    'AI/ML Engineer': {
        'description': 'AI/ML engineers build and deploy artificial intelligence and machine learning models that can learn from data and make predictions for Indian businesses, healthcare, finance, and more.',
        'skills': ['Python', 'TensorFlow/PyTorch/Keras', 'Machine Learning Algorithms', 'Deep Learning', 'Mathematics & Statistics', 'Data Preprocessing', 'Model Deployment (Docker, Kubernetes)', 'NLP', 'Computer Vision'],
        'salary_range': '₹10,00,000 - ₹60,00,000 per year (Entry: ₹8-12 LPA, Mid: ₹18-30 LPA, Senior: ₹32-50 LPA, Expert: ₹55-70 LPA)',
        'education': "Master's or PhD in AI, Machine Learning, Computer Science; B.Tech from top institutes with strong portfolio",
        'growth': 'Fastest growing field in India - 40% annual growth, huge demand in fintech, healthcare, e-commerce, and manufacturing',
        'top_companies': ['Infosys AI Labs - Bengaluru', 'TCS AI & ML Team - Mumbai/Chennai', 'Wipro AI - Bengaluru', 'HCL AI & Cloud - Noida/Chennai', 'Tech Mahindra AI - Pune/Hyderabad', 'LTIMindtree AI - Bengaluru', 'Fractal AI - Mumbai/Bengaluru', 'DeepTek AI - Pune', 'Flutura AI - Bengaluru', 'Mad Street Den - Chennai/Bengaluru', 'Uniphore - Chennai/Bengaluru/Delhi', 'Niki.ai - Mumbai/Bengaluru'],
        'indian_hubs': ['Bengaluru (AI Capital)', 'Hyderabad', 'Pune', 'Mumbai', 'Chennai', 'Gurugram', 'Delhi NCR']
    },
    'Cybersecurity Analyst': {
        'description': 'Cybersecurity analysts protect Indian computer systems, networks, and data from cyber threats, attacks, and unauthorized access for corporations, banks, and government.',
        'skills': ['Network Security', 'Risk Assessment & Management', 'Incident Response', 'Security Tools (Firewalls, IDS/IPS)', 'Cryptography', 'Compliance (ISO, GDPR, IT Act)', 'Penetration Testing', 'Vulnerability Assessment'],
        'salary_range': '₹5,00,000 - ₹35,00,000 per year (Entry: ₹4-7 LPA, Mid: ₹10-18 LPA, Senior: ₹20-30 LPA, Expert: ₹35-45 LPA, CISSP: ₹40+ LPA)',
        'education': "Bachelor's in Cybersecurity, Computer Science, IT; Certifications like CEH, CISSP, CISM highly valued",
        'growth': 'Critical demand - 35% growth in India, RBI mandates for banks, government initiatives like Cyber Surakshit Bharat',
        'top_companies': ['TCS Cybersecurity - Mumbai/Chennai', 'Infosys Security - Bengaluru', 'Wipro Security - Bengaluru/Chennai', 'HCL Security - Noida/Chennai', 'Tech Mahindra Security - Pune/Hyderabad', 'LTIMindtree Security - Bengaluru', 'Paladion Networks - Mumbai/Bengaluru/Delhi', 'Quick Heal - Pune', 'Seqrite - Pune', 'Lucideus - Delhi NCR', 'K7 Computing - Chennai', 'Tresorit India - Mumbai', 'NortonLifeLock India - Pune/Bengaluru'],
        'indian_hubs': ['Bengaluru', 'Mumbai', 'Pune', 'Chennai', 'Hyderabad', 'Delhi NCR', 'Gurugram']
    },
    'Cloud Architect': {
        'description': 'Cloud architects design and manage cloud infrastructure for Indian enterprises migrating to AWS, Azure, and Google Cloud platforms.',
        'skills': ['AWS/Azure/GCP Services', 'Infrastructure as Code (Terraform)', 'Cloud Security', 'Networking', 'Containerization (Docker, Kubernetes)', 'DevOps Practices', 'Cost Optimization', 'Disaster Recovery'],
        'salary_range': '₹15,00,000 - ₹50,00,000 per year (Entry Cloud Eng: ₹6-10 LPA, Cloud Arch: ₹18-30 LPA, Senior: ₹35-50 LPA, Principal: ₹55-70 LPA)',
        'education': "B.Tech in CS/IT, Cloud Certifications (AWS Certified Solutions Architect, Azure Solutions Architect, Google Cloud Architect)",
        'growth': 'High demand as Indian companies move to cloud - 30% annual growth, multi-cloud expertise highly valued',
        'top_companies': ['Infosys Cloud - Bengaluru', 'TCS Cloud - Mumbai/Chennai', 'Wipro Cloud - Bengaluru/Hyderabad', 'HCL Cloud - Noida', 'Tech Mahindra Cloud - Pune', 'LTIMindtree Cloud - Bengaluru', 'Persistent Systems Cloud - Pune', 'Mphasis Cloud - Bengaluru', 'CloudThat - Bengaluru/Mysore', 'Rackspace India - Mumbai/Delhi', 'CtrlS - Hyderabad/Mumbai'],
        'indian_hubs': ['Bengaluru', 'Hyderabad', 'Pune', 'Mumbai', 'Chennai', 'Noida', 'Gurugram']
    },
    'DevOps Engineer': {
        'description': 'DevOps engineers bridge development and operations, automating deployment pipelines and infrastructure for faster software delivery in Indian tech companies.',
        'skills': ['CI/CD (Jenkins, GitLab CI, GitHub Actions)', 'Containerization (Docker)', 'Orchestration (Kubernetes)', 'Infrastructure as Code (Terraform, Ansible)', 'Monitoring (Prometheus, Grafana)', 'Cloud Platforms', 'Scripting (Python, Bash)', 'Version Control (Git)'],
        'salary_range': '₹6,00,000 - ₹40,00,000 per year (Entry: ₹5-9 LPA, Mid: ₹12-22 LPA, Senior: ₹25-35 LPA, Lead: ₹38-50 LPA)',
        'education': "B.Tech in CS/IT, DevOps certifications (AWS DevOps, Azure DevOps, Kubernetes Certification)",
        'growth': 'Essential role in modern IT - 35% growth, every Indian tech company needs DevOps, huge demand in startups',
        'top_companies': ['Infosys DevOps - Bengaluru/Pune', 'TCS DevOps - Mumbai/Chennai', 'Wipro DevOps - Bengaluru/Hyderabad', 'HCL DevOps - Noida/Chennai', 'Tech Mahindra DevOps - Pune', 'LTIMindtree DevOps - Bengaluru', 'Persistent Systems DevOps - Pune', 'Razorpay - Bengaluru', 'Flipkart - Bengaluru', 'Paytm - Noida/Delhi', 'Zomato - Gurugram/Bengaluru'],
        'indian_hubs': ['Bengaluru', 'Pune', 'Hyderabad', 'Mumbai', 'Chennai', 'Gurugram', 'Noida']
    },
    'Full Stack Developer': {
        'description': 'Full stack developers build complete web applications including frontend, backend, and database layers for Indian companies and startups.',
        'skills': ['Frontend (React, Angular, Vue.js)', 'Backend (Node.js, Python Django/Flask, Java Spring)', 'Databases (SQL, MongoDB)', 'REST APIs', 'HTML/CSS/JavaScript', 'Version Control (Git)', 'Deployment (Heroku, AWS)', 'Testing'],
        'salary_range': '₹4,50,000 - ₹35,00,000 per year (Entry: ₹4-8 LPA, Mid: ₹10-18 LPA, Senior: ₹20-30 LPA, Lead: ₹32-40 LPA)',
        'education': "B.Tech/BE in CS/IT, BCA, MCA; Bootcamp graduates also hired with strong portfolios",
        'growth': 'High demand in startups and product companies - 25% growth, most versatile role in tech industry',
        'top_companies': ['TCS Digital - Mumbai/Chennai', 'Infosys - Bengaluru/Pune', 'Wipro - Bengaluru', 'HCL - Noida', 'Tech Mahindra - Pune', 'LTIMindtree - Bengaluru', 'Mindtree - Bengaluru', 'Persistent Systems - Pune', 'Flipkart - Bengaluru', 'Amazon India - Bengaluru/Hyderabad', 'Paytm - Noida', 'Swiggy - Bengaluru', 'Zomato - Gurugram', 'Unacademy - Bengaluru', 'BYJU\'s - Bengaluru', 'Razorpay - Bengaluru', 'Ola - Bengaluru'],
        'indian_hubs': ['Bengaluru (Startup capital)', 'Hyderabad', 'Pune', 'Mumbai', 'Chennai', 'Noida', 'Gurugram', 'Kolkata']
    },
    'Database Administrator': {
        'description': 'Database administrators manage and maintain databases ensuring data security, performance, and availability for Indian organizations.',
        'skills': ['SQL (MySQL, PostgreSQL, Oracle, SQL Server)', 'Database Design', 'Performance Tuning', 'Backup & Recovery', 'Security Management', 'Data Migration', 'High Availability (Replication, Clustering)', 'NoSQL (MongoDB, Cassandra)'],
        'salary_range': '₹4,00,000 - ₹28,00,000 per year (Entry: ₹3-6 LPA, Mid: ₹8-15 LPA, Senior: ₹18-25 LPA, Lead: ₹28-35 LPA)',
        'education': "B.Tech in CS/IT, BCA, MCA; Certifications like Oracle Certified Professional (OCP), Microsoft SQL Server Certification",
        'growth': 'Steady demand - 12% growth, essential for every company with data, banks and financial institutions are major employers',
        'top_companies': ['TCS - Mumbai/Chennai', 'Infosys - Bengaluru', 'Wipro - Bengaluru', 'HCL - Noida/Chennai', 'Tech Mahindra - Pune', 'LTIMindtree - Bengaluru', 'Oracle India - Bengaluru/Hyderabad', 'Microsoft India - Hyderabad/Bengaluru', 'IBM India - Bengaluru/Pune', 'HDFC Bank - Mumbai', 'ICICI Bank - Mumbai', 'SBI - All India'],
        'indian_hubs': ['Bengaluru', 'Mumbai', 'Hyderabad', 'Chennai', 'Pune', 'Noida', 'Gurugram', 'Kolkata']
    },

    # ==================== 2. BUSINESS & FINANCE CAREERS ====================
    'Business Analyst': {
        'description': 'Business analysts help Indian organizations improve processes, products, and services through data analysis and business insights bridging IT and business teams.',
        'skills': ['Data Analysis (Excel, SQL)', 'Requirements Gathering', 'Communication & Stakeholder Management', 'Problem Solving', 'Business Process Modeling', 'Documentation', 'Agile Methodologies', 'Tools: JIRA, Confluence, Tableau'],
        'salary_range': '₹5,00,000 - ₹25,00,000 per year (Entry: ₹4-7 LPA, Mid: ₹9-15 LPA, Senior: ₹16-22 LPA, Lead: ₹24-30 LPA)',
        'education': "Bachelor's in Business, Finance, IT, Economics; MBA preferred; CBAP certification valued",
        'growth': 'Steady growth - 15% CAGR in India, high demand in consulting, IT services, and banking sectors',
        'top_companies': ['Deloitte India - Mumbai/Delhi/Bengaluru', 'PwC India - Kolkata/Mumbai/Delhi', 'KPMG India - Mumbai/Delhi/Bengaluru', 'EY India - Mumbai/Delhi/Bengaluru', 'McKinsey India - Mumbai/Delhi/Bengaluru', 'BCG India - Mumbai/Delhi/Bengaluru', 'Accenture India - Bengaluru/Mumbai/Pune', 'Capgemini India - Mumbai/Pune/Bengaluru', 'Infosys Consulting - Bengaluru', 'TCS BFSI - Mumbai/Chennai', 'Wipro Consulting - Bengaluru', 'HCL - Noida/Chennai'],
        'indian_hubs': ['Mumbai', 'Delhi NCR', 'Bengaluru', 'Pune', 'Hyderabad', 'Chennai', 'Kolkata', 'Gurugram']
    },
    'Investment Banker': {
        'description': 'Investment bankers help Indian companies, government, and financial institutions raise capital, provide M&A advisory, and execute financial transactions.',
        'skills': ['Financial Modeling', 'Valuation (DCF, LBO, Comparable Analysis)', 'Negotiation', 'Deal Making', 'Client Management', 'Excel (Advanced)', 'Bloomberg Terminal', 'Due Diligence', 'Capital Markets Knowledge'],
        'salary_range': '₹12,00,000 - ₹80,00,000+ per year (Entry Analyst: ₹10-18 LPA, Associate: ₹20-35 LPA, VP: ₹40-60 LPA, Director: ₹65-80+ LPA, MD: ₹1-2 Cr+)',
        'education': "Bachelor's in Finance, Economics, Commerce; MBA from IIM/ISB/SP Jain preferred; CFA Charterholder valued",
        'growth': 'Growing with Indian economy - 10-12% growth, strong demand in Mumbai (financial capital), bonus-heavy industry (50-200% of base)',
        'top_companies': ['Goldman Sachs India - Bengaluru/Mumbai/Hyderabad', 'JP Morgan India - Mumbai/Bengaluru/Hyderabad', 'Morgan Stanley India - Mumbai/Bengaluru', 'Bank of America India - Mumbai/Bengaluru', 'Citigroup India - Mumbai/Chennai', 'Deutsche Bank India - Mumbai/Bengaluru', 'Avendus Capital - Mumbai/Bengaluru/Delhi', 'Kotak Investment Banking - Mumbai/Delhi/Bengaluru/Chennai', 'Axis Capital - Mumbai/Delhi/Bengaluru', 'ICICI Securities - Mumbai/Delhi/Bengaluru/Chennai', 'Motilal Oswal Investment Banking - Mumbai/Delhi', 'IIFL Capital - Mumbai/Bengaluru/Delhi'],
        'indian_hubs': ['Mumbai (BKC, Nariman Point)', 'Bengaluru', 'Delhi NCR', 'Hyderabad', 'Chennai', 'Gurugram']
    },
    'Marketing Manager': {
        'description': 'Marketing managers develop and execute marketing strategies to promote Indian products, services, and brands across traditional and digital channels.',
        'skills': ['Strategic Planning', 'Digital Marketing (SEO, SEM, Social Media)', 'Brand Management', 'Market Research', 'Analytics (Google Analytics)', 'Leadership', 'Budget Management', 'Content Strategy', 'Campaign Management'],
        'salary_range': '₹6,00,000 - ₹35,00,000 per year (Entry: ₹4-7 LPA, Mid: ₹10-18 LPA, Senior: ₹20-30 LPA, Director: ₹35-50 LPA)',
        'education': "Bachelor's in Marketing, Business, Communications; MBA in Marketing from top B-school preferred; Digital Marketing certifications valued",
        'growth': 'Strong growth - 18% CAGR in digital marketing, FMCG and e-commerce sectors are top employers',
        'top_companies': ['Hindustan Unilever - Mumbai', 'ITC Limited - Kolkata/Bengaluru/Gurugram', 'Tata Consumer Products - Mumbai/Bengaluru', 'Nestlé India - Gurugram', 'Britannia Industries - Bengaluru', 'Parle Agro - Mumbai', 'PepsiCo India - Gurugram/Mumbai', 'Coca-Cola India - Gurugram/Mumbai', 'Amazon India - Bengaluru/Mumbai/Delhi', 'Flipkart - Bengaluru', 'Reliance Retail - Mumbai', 'Tata Motors - Mumbai/Pune', 'Mahindra & Mahindra - Mumbai', 'Maruti Suzuki - Delhi NCR', 'Zomato - Gurugram', 'Swiggy - Bengaluru', 'Unacademy - Bengaluru', 'BYJU\'s - Bengaluru'],
        'indian_hubs': ['Mumbai', 'Delhi NCR', 'Bengaluru', 'Kolkata', 'Chennai', 'Hyderabad', 'Pune', 'Gurugram']
    },
    'Entrepreneur': {
        'description': 'Entrepreneurs start and run their own businesses in India, taking financial risks in hopes of profit and growth. India has a thriving startup ecosystem.',
        'skills': ['Leadership', 'Risk Taking', 'Strategic Planning', 'Financial Management', 'Sales & Marketing', 'Networking', 'Problem Solving', 'Team Building', 'Resilience', 'Product Development'],
        'salary_range': 'Variable - ₹5,00,000 to ₹1,00,00,000+ per year (Startup founder draw: ₹10-25 LPA early stage, Successful exits: ₹1-100 Cr+)',
        'education': "No specific degree required; IIT/IIM/BITS alumni with MBA often successful; Business education helpful; Learning from failure key",
        'growth': 'India has 3rd largest startup ecosystem - 100+ unicorns, 50,000+ startups; Growing at 15% annually; Government support via Startup India',
        'top_companies': 'Self-employed / Business Owner / Startup Founder (Indian Unicorns: Flipkart, Ola, Paytm, BYJU\'s, Zomato, Swiggy, Razorpay, OYO, CRED, Unacademy, UpGrad, Dream11, BharatPe, PhonePe, Meesho, Nykaa, PolicyBazaar, Delhivery, Freshworks)',
        'indian_hubs': ['Bengaluru (Startup Capital)', 'Delhi NCR (Gurugram, Noida)', 'Mumbai (Fintech Hub)', 'Hyderabad (Pharma-Tech)', 'Pune', 'Chennai', 'Kolkata', 'Ahmedabad', 'Jaipur'],
        'success_factors': ['Market opportunity in India (1.4B population)', 'Innovation & product-market fit', 'Strong team & execution', 'Access to Indian VC funding', 'Government schemes (Startup India, Make in India)', 'Persistence & adaptability']
    },
    'Financial Analyst': {
        'description': 'Financial analysts evaluate investment opportunities, analyze financial data, and provide recommendations for Indian companies, banks, and investment firms.',
        'skills': ['Financial Modeling', 'Financial Statement Analysis', 'Valuation Techniques', 'Excel (Advanced)', 'Investment Research', 'Ratio Analysis', 'Risk Assessment', 'Bloomberg/Reuters', 'Report Writing'],
        'salary_range': '₹5,00,000 - ₹28,00,000 per year (Entry: ₹4-7 LPA, Mid: ₹9-15 LPA, Senior: ₹16-22 LPA, Lead: ₹24-30 LPA)',
        'education': "Bachelor's in Finance, Accounting, Economics; CFA/CPA/CA preferred; MBA Finance valued",
        'growth': 'Steady demand - 14% growth, high demand in banking, investment firms, and corporate finance departments',
        'top_companies': ['Goldman Sachs - Bengaluru/Mumbai', 'JP Morgan - Mumbai/Bengaluru', 'Morgan Stanley - Mumbai/Bengaluru', 'HDFC Bank - Mumbai', 'ICICI Bank - Mumbai', 'Kotak Securities - Mumbai', 'Motilal Oswal - Mumbai', 'Angel Broking - Mumbai', 'Zerodha - Bengaluru', 'Groww - Bengaluru', 'INDmoney - Gurugram', 'Deloitte - Mumbai/Delhi/Bengaluru', 'PwC - Kolkata/Mumbai/Delhi', 'KPMG - Mumbai/Delhi/Bengaluru', 'EY - Mumbai/Delhi/Bengaluru'],
        'indian_hubs': ['Mumbai', 'Bengaluru', 'Delhi NCR', 'Chennai', 'Hyderabad', 'Pune', 'Kolkata']
    },
    'Management Consultant': {
        'description': 'Management consultants help Indian organizations solve complex business problems, improve performance, and drive transformation across industries.',
        'skills': ['Problem Solving', 'Data Analysis', 'Strategic Thinking', 'Client Management', 'Project Management', 'Presentation Skills', 'Stakeholder Management', 'Industry Knowledge', 'Change Management'],
        'salary_range': '₹12,00,000 - ₹60,00,000 per year (Entry Associate: ₹12-18 LPA, Consultant: ₹20-30 LPA, Manager: ₹35-45 LPA, Partner: ₹60 LPA - 1 Cr+)',
        'education': "MBA from IIMs/ISB/XLRI/FMS/SPJIMR; Bachelor's from top institutes (IIT, SRCC, St. Stephens); Engineering background common",
        'growth': 'High growth - 20% CAGR in India, top consulting firms expanding rapidly, expertise in digital transformation highly valued',
        'top_companies': ['McKinsey & Company - Mumbai/Delhi/Bengaluru/Chennai', 'Boston Consulting Group (BCG) - Mumbai/Delhi/Bengaluru/Kolkata', 'Bain & Company - Mumbai/Delhi/Bengaluru/Gurugram', 'Deloitte Consulting - Mumbai/Delhi/Bengaluru/Hyderabad', 'PwC Consulting - Kolkata/Mumbai/Delhi/Bengaluru', 'KPMG Advisory - Mumbai/Delhi/Bengaluru/Hyderabad', 'EY Advisory - Mumbai/Delhi/Bengaluru/Chennai', 'Accenture Strategy - Bengaluru/Mumbai/Delhi', 'Capgemini Invent - Mumbai/Bengaluru/Pune', 'ZS Associates - Pune/Bengaluru/Delhi', 'A.T. Kearney - Mumbai/Delhi/Bengaluru', 'Oliver Wyman - Mumbai/Delhi/Gurugram', 'Arthur D. Little - Mumbai'],
        'indian_hubs': ['Mumbai', 'Delhi NCR (Gurugram)', 'Bengaluru', 'Chennai', 'Pune', 'Hyderabad', 'Kolkata']
    },
    'Chartered Accountant (CA)': {
        'description': 'Chartered Accountants manage financial accounts, conduct audits, ensure tax compliance, and provide financial advice for Indian businesses and individuals.',
        'skills': ['Accounting Standards (Ind AS)', 'Taxation (Direct & Indirect)', 'Auditing & Assurance', 'Financial Reporting', 'Corporate Law', 'Risk Management', 'Analytical Skills', 'Ethical Judgment'],
        'salary_range': '₹6,00,000 - ₹50,00,000 per year (Entry: ₹6-9 LPA, Mid: ₹12-20 LPA, Senior: ₹22-35 LPA, Partner: ₹40 LPA - 1 Cr+)',
        'education': 'CA (Chartered Accountant) from ICAI - Requires clearing 3 levels (Foundation, Intermediate, Final) + 3 years articleship',
        'growth': 'Steady demand - 10% growth, statutory requirement for Indian companies, global recognition',
        'top_companies': ['Deloitte India - Mumbai/Delhi/Bengaluru/Hyderabad', 'PwC India - Kolkata/Mumbai/Delhi/Bengaluru', 'KPMG India - Mumbai/Delhi/Bengaluru/Chennai', 'EY India - Mumbai/Delhi/Bengaluru/Chennai', 'BDO India - Mumbai/Delhi/Bengaluru', 'Grant Thornton India - Mumbai/Delhi/Bengaluru', 'RSM India - Mumbai/Delhi/Bengaluru', 'Nexdigm - Mumbai/Delhi/Bengaluru', 'Walker Chandiok & Co - Delhi/Gurugram', 'SRBC & Co - Mumbai/Delhi', 'Tata Sons - Mumbai', 'Reliance Industries - Mumbai', 'HDFC Bank - Mumbai', 'ICICI Bank - Mumbai', 'SBI - Mumbai'],
        'indian_hubs': ['Mumbai', 'Delhi NCR', 'Bengaluru', 'Kolkata', 'Chennai', 'Hyderabad', 'Pune', 'Ahmedabad']
    },
    'Company Secretary (CS)': {
        'description': 'Company Secretaries handle corporate compliance, legal governance, board meetings, and regulatory filings for Indian companies listed on stock exchanges.',
        'skills': ['Company Law (Companies Act)', 'Corporate Governance', 'SEBI Regulations', 'Board Meeting Management', 'Legal Compliance', 'Drafting & Documentation', 'NSE/BSE Filings', 'Due Diligence', 'Risk Management'],
        'salary_range': '₹5,00,000 - ₹40,00,000 per year (Entry: ₹5-8 LPA, Mid: ₹10-16 LPA, Senior: ₹18-28 LPA, CS Head: ₹30-40 LPA)',
        'education': 'CS (Company Secretary) from ICSI - Requires clearing 3 levels (Foundation, Executive, Professional) + training',
        'growth': 'Steady demand - 8% growth, mandatory for listed companies, compliance role critical in Indian regulatory environment',
        'top_companies': ['Tata Consultancy Services (TCS) - Mumbai', 'Reliance Industries - Mumbai', 'HDFC Bank - Mumbai', 'ICICI Bank - Mumbai', 'Infosys - Bengaluru', 'Wipro - Bengaluru', 'ITC Limited - Kolkata', 'Hindustan Unilever - Mumbai', 'Larsen & Toubro - Mumbai', 'Maruti Suzuki - Delhi NCR', 'State Bank of India - Mumbai', 'Adani Group - Ahmedabad/Mumbai', 'DLF Limited - Gurugram', 'Godrej Properties - Mumbai', 'Indian Oil Corporation - Delhi'],
        'indian_hubs': ['Mumbai', 'Delhi NCR', 'Bengaluru', 'Chennai', 'Kolkata', 'Ahmedabad', 'Hyderabad', 'Pune']
    },

    # ==================== 3. HEALTH SCIENCES CAREERS ====================
    'Specialized Doctor': {
        'description': 'Doctors diagnose and treat medical conditions, prescribe medications, and provide healthcare to patients in Indian hospitals and clinics.',
        'skills': ['Medical Knowledge (MBBS)', 'Diagnostic Skills', 'Patient Care & Communication', 'Empathy', 'Decision Making Under Pressure', 'Teamwork with Nurses/Technicians', 'Emergency Response', 'Clinical Procedures'],
        'salary_range': '₹6,00,000 - ₹1,00,00,000+ per year (Entry JR: ₹6-9 LPA, SR: ₹10-15 LPA, Specialist MD/MS: ₹20-40 LPA, Surgeon: ₹30-60 LPA, Senior Consultant: ₹50 LPA - 1 Cr+, Private Practice: ₹1-5 Cr+)',
        'education': 'MBBS (5.5 years including internship) + MD/MS specialization (3 years) + DM/MCh super-specialization (3 years) for advanced roles',
        'growth': '7-9% growth, high demand in tier 2/3 cities, government initiatives (Ayushman Bharat) increasing healthcare access',
        'top_companies': ['AIIMS - New Delhi/Bhopal/Bhubaneswar/Jodhpur/Patna/Raipur/Rishikesh', 'Apollo Hospitals - Chennai/Delhi/Hyderabad/Bengaluru/Mumbai/Kolkata', 'Fortis Healthcare - Delhi NCR/Bengaluru/Mumbai/Chennai/Kolkata', 'Max Healthcare - Delhi NCR/Punjab', 'Narayana Health - Bengaluru/Kolkata/Mumbai/Delhi NCR', 'Manipal Hospitals - Bengaluru/Mangalore/Delhi/Pune/Jaipur', 'Medanta - Gurugram/Lucknow/Ranchi/Indore', 'Care Hospitals - Hyderabad/Bhubaneswar/Nagpur', 'Kokilaben Hospital - Mumbai', 'Lilavati Hospital - Mumbai', 'Christian Medical College (CMC) - Vellore/Ludhiana', 'PGIMER - Chandigarh', 'Tata Memorial Hospital - Mumbai', 'Government Medical Colleges - All State Capitals'],
        'indian_hubs': ['Delhi NCR', 'Mumbai', 'Bengaluru', 'Chennai', 'Hyderabad', 'Kolkata', 'Pune', 'Ahmedabad', 'Chandigarh', 'Lucknow', 'Jaipur', 'Bhubaneswar']
    },
    'Clinical Specialist': {
        'description': 'Nurses provide patient care, administer medications, monitor vital signs, and support doctors in medical procedures across Indian healthcare settings.',
        'skills': ['Patient Care', 'Medical Knowledge', 'Communication', 'Compassion', 'Critical Thinking', 'Attention to Detail', 'Emergency Response', 'Medication Administration', 'Vital Signs Monitoring'],
        'salary_range': '₹2,00,000 - ₹8,00,000 per year (Entry: ₹2-3 LPA, Staff Nurse: ₹3.5-5 LPA, Senior Nurse: ₹5-7 LPA, Nurse Manager: ₹7-9 LPA, Overseas: ₹15-25 LPA)',
        'education': 'B.Sc Nursing (4 years), GNM (General Nursing and Midwifery - 3.5 years), M.Sc Nursing (2 years) for advanced roles',
        'growth': '12-15% growth, high demand in India and abroad (Gulf, UK, USA, Australia), government health initiatives increasing hiring',
        'top_companies': ['Apollo Hospitals - All Major Cities', 'Fortis Healthcare - Delhi NCR/Bengaluru/Mumbai', 'Max Healthcare - Delhi NCR', 'Narayana Health - Bengaluru/Kolkata', 'Manipal Hospitals - Bengaluru/Delhi/Pune', 'Medanta - Gurugram/Lucknow', 'AIIMS - New Delhi/Others', 'Government Hospitals - All State Capitals and Districts', 'Shankar Nethralaya - Chennai', 'LV Prasad Eye Hospital - Hyderabad/Bhubaneswar'],
        'indian_hubs': ['Delhi NCR', 'Mumbai', 'Bengaluru', 'Chennai', 'Hyderabad', 'Kolkata', 'Pune', 'Ahmedabad', 'Kochi', 'Chandigarh']
    },
    'Pharmaceutical Researcher': {
        'description': 'Pharmacists dispense medications, advise patients on drug interactions, ensure safe medication use, and manage pharmacy inventory in India.',
        'skills': ['Pharmaceutical Knowledge (Drugs, Dosages)', 'Attention to Detail', 'Patient Counseling', 'Math & Calculation Skills', 'Regulatory Compliance (Drugs & Cosmetics Act)', 'Inventory Management', 'Communication', 'Computer Skills for Billing'],
        'salary_range': '₹2,50,000 - ₹10,00,000 per year (Entry Retail: ₹2-3 LPA, Hospital: ₹3-5 LPA, Senior: ₹5-8 LPA, Pharmacist Manager: ₹8-10 LPA)',
        'education': 'B.Pharma (4 years), D.Pharma (2 years), M.Pharma (2 years) for advanced/clinical roles',
        'growth': '10% growth, expansion of pharmacy chains, online pharmacies (Netmeds, PharmEasy, 1mg, Apollo Pharmacy), growing healthcare awareness',
        'top_companies': ['Apollo Pharmacy - Across India', 'MedPlus Health - Hyderabad/All Major Cities', 'Netmeds (API Holdings) - Chennai/Bengaluru/Mumbai', 'PharmEasy - Mumbai/Bengaluru/Delhi', '1mg (Tata 1mg) - Gurugram/Bengaluru/Mumbai', 'Wellness Forever - Mumbai/Pune/Bengaluru', 'Medlife - Bengaluru', 'Health & Glow - Chennai/Bengaluru/Hyderabad', 'Fortis Hospital Pharmacies - Delhi NCR/Bengaluru', 'Apollo Hospitals Pharmacies - Across India', 'Manipal Hospitals Pharmacies - Bengaluru/Delhi', 'Narayana Health Pharmacies - Bengaluru/Kolkata', 'Government Hospitals - State-wise'],
        'indian_hubs': ['Mumbai', 'Bengaluru', 'Hyderabad', 'Delhi NCR', 'Chennai', 'Pune', 'Kolkata', 'Ahmedabad']
    },
    'Healthcare Administrator': {
        'description': 'Physiotherapists help Indian patients recover from injuries, manage pain, improve mobility, and prevent disability through physical therapy techniques.',
        'skills': ['Anatomy & Physiology Knowledge', 'Therapeutic Exercise', 'Patient Assessment', 'Communication', 'Manual Therapy (Joint mobilization, massage)', 'Rehabilitation Planning', 'Electrotherapy (Ultrasound, TENS)', 'Sports Injury Management'],
        'salary_range': '₹2,50,000 - ₹12,00,000 per year (Entry: ₹2.5-4 LPA, Mid: ₹4.5-7 LPA, Senior: ₹8-10 LPA, Sports Physio: ₹10-15 LPA)',
        'education': 'BPT (Bachelor of Physiotherapy - 4.5 years including internship), MPT (Master of Physiotherapy - 2 years) for specialization',
        'growth': '18-20% growth (much faster than average), rising sports culture, aging population, increasing health awareness, demand in hospitals and sports academies',
        'top_companies': ['Apollo Hospitals - Chennai/Delhi/Hyderabad', 'Fortis Healthcare - Delhi NCR/Bengaluru', 'Max Healthcare - Delhi NCR', 'Manipal Hospitals - Bengaluru/Delhi', 'Narayana Health - Bengaluru/Kolkata', 'Mumbai Sports Club physio clinics', 'Indian Cricket team physio (BCCI) - Mumbai', 'Sports Authority of India (SAI) - Delhi/Bengaluru/Patiala', 'Indian Olympic Association - Delhi', 'National Institute of Sports (NIS) - Patiala', 'Khelo India Centers - Across India'],
        'indian_hubs': ['Mumbai', 'Delhi NCR', 'Bengaluru', 'Chennai', 'Hyderabad', 'Pune', 'Kolkata', 'Ahmedabad', 'Chandigarh']
    },
    'Medical Researcher': {
        'description': 'Medical researchers conduct clinical studies, clinical trials, and lab research to develop new treatments, drugs, and medical knowledge in India.',
        'skills': ['Research Methodology', 'Clinical Trial Design', 'Data Analysis (SPSS, R, SAS)', 'Laboratory Techniques', 'Scientific Writing', 'Grant Writing', 'Regulatory Compliance (ICMR, DCGI, CDSCO)', 'Ethics Committee Standards'],
        'salary_range': '₹3,50,000 - ₹20,00,000 per year (Entry Research Assistant: ₹3-5 LPA, Junior Scientist: ₹5-8 LPA, Senior Scientist: ₹9-15 LPA, Principal Investigator: ₹16-25 LPA)',
        'education': 'PhD in Medical Sciences/Life Sciences, MD (Doctor of Medicine) for clinical research, M.Sc/M.Tech in Biomedical Research, MBBS+MD+PhD for senior roles',
        'growth': '15% growth, India becoming clinical trial hub, government funding (ICMR, DBT, CSIR), pharmaceutical R&D expansion',
        'top_companies': ['Indian Council of Medical Research (ICMR) - Delhi', 'All India Institute of Medical Sciences (AIIMS) - New Delhi', 'Tata Memorial Centre - Mumbai', 'National Institute of Mental Health and Neurosciences (NIMHANS) - Bengaluru', 'Centre for Cellular and Molecular Biology (CCMB) - Hyderabad', 'National Centre for Biological Sciences (NCBS) - Bengaluru', 'Serum Institute of India R&D - Pune', 'Biocon Research - Bengaluru', 'Dr. Reddy\'s R&D - Hyderabad', 'Lupin Research - Pune', 'Sun Pharma Research - Mumbai/Vadodara', 'Cipla R&D - Mumbai/Bengaluru', 'Syngene (Biocon) - Bengaluru/Hyderabad'],
        'indian_hubs': ['Delhi NCR', 'Bengaluru', 'Hyderabad', 'Pune', 'Mumbai', 'Chennai', 'Kolkata', 'Chandigarh']
    },
    'Medical Professor': {
        'description': 'Medical Professorss conduct clinical studies, clinical trials, and lab research to develop new treatments, drugs, and medical knowledge in India.',
        'skills': ['Research Methodology', 'Clinical Trial Design', 'Data Analysis (SPSS, R, SAS)', 'Laboratory Techniques', 'Scientific Writing', 'Grant Writing', 'Regulatory Compliance (ICMR, DCGI, CDSCO)', 'Ethics Committee Standards'],
        'salary_range': '₹3,50,000 - ₹20,00,000 per year (Entry Research Assistant: ₹3-5 LPA, Junior Scientist: ₹5-8 LPA, Senior Scientist: ₹9-15 LPA, Principal Investigator: ₹16-25 LPA)',
        'education': 'PhD in Medical Sciences/Life Sciences, MD (Doctor of Medicine) for clinical research, M.Sc/M.Tech in Biomedical Research, MBBS+MD+PhD for senior roles',
        'growth': '15% growth, India becoming clinical trial hub, government funding (ICMR, DBT, CSIR), pharmaceutical R&D expansion',
        'top_companies': ['Indian Council of Medical Research (ICMR) - Delhi', 'All India Institute of Medical Sciences (AIIMS) - New Delhi', 'Tata Memorial Centre - Mumbai', 'National Institute of Mental Health and Neurosciences (NIMHANS) - Bengaluru', 'Centre for Cellular and Molecular Biology (CCMB) - Hyderabad', 'National Centre for Biological Sciences (NCBS) - Bengaluru', 'Serum Institute of India R&D - Pune', 'Biocon Research - Bengaluru', 'Dr. Reddy\'s R&D - Hyderabad', 'Lupin Research - Pune', 'Sun Pharma Research - Mumbai/Vadodara', 'Cipla R&D - Mumbai/Bengaluru', 'Syngene (Biocon) - Bengaluru/Hyderabad'],
        'indian_hubs': ['Delhi NCR', 'Bengaluru', 'Hyderabad', 'Pune', 'Mumbai', 'Chennai', 'Kolkata', 'Chandigarh']
    },

    # ==================== 4. CREATIVE ARTS CAREERS ====================
    'Graphic Designer': {
        'description': 'Graphic designers create visual concepts using software to communicate ideas that inspire, inform, or captivate consumers for Indian brands and agencies.',
        'skills': ['Adobe Creative Suite (Photoshop, Illustrator, InDesign)', 'Typography', 'Color Theory', 'Layout & Composition', 'Creativity', 'Visual Communication', 'Brand Identity', 'Time Management', 'Client Presentation'],
        'salary_range': '₹2,50,000 - ₹12,00,000 per year (Entry Junior: ₹2.5-4 LPA, Mid: ₹4.5-8 LPA, Senior: ₹8-12 LPA, Art Director: ₹12-18 LPA)',
        'education': "Bachelor's in Graphic Design, Fine Arts, Visual Communication, B.Des; Diploma in Graphic Design sufficient with strong portfolio",
        'growth': '10-12% growth, rising demand for digital content, e-commerce, social media marketing, UI/UX skills add premium',
        'top_companies': ['Design Agencies: Landor (Mumbai/Bengaluru), Interbrand (Mumbai), VGC (Mumbai), Elephant Design (Pune/Delhi), Ray+Keshavan (Bengaluru)', 'Publishing: Penguin Random House (Gurugram), HarperCollins (Noida)', 'Tech: Flipkart (Bengaluru), Amazon India (Bengaluru/Hyderabad), Swiggy (Bengaluru)', 'Media: Disney+ Hotstar (Mumbai), Netflix India (Mumbai), Zee5 (Mumbai), SonyLIV (Mumbai)', 'E-commerce: Myntra (Bengaluru), Nykaa (Mumbai), Meesho (Bengaluru)', 'Studios: Technicolor India (Bengaluru/Mumbai)'],
        'indian_hubs': ['Mumbai', 'Bengaluru', 'Delhi NCR (Gurugram, Noida)', 'Pune', 'Hyderabad', 'Chennai', 'Kolkata', 'Ahmedabad']
    },
    'Senior UX Designer': {
        'description': 'UX/UI designers create user-friendly interfaces for Indian websites and apps, focusing on user experience research and visual design for digital products.',
        'skills': ['User Research & Personas', 'Wireframing & Prototyping (Figma, Sketch, Adobe XD)', 'Usability Testing', 'Interaction Design', 'Visual Design', 'Information Architecture', 'Figma/Framer', 'HTML/CSS basics', 'Design Systems'],
        'salary_range': '₹4,00,000 - ₹25,00,000 per year (Entry Junior: ₹4-7 LPA, Mid: ₹8-15 LPA, Senior: ₹16-22 LPA, Lead: ₹24-30 LPA, UX Director: ₹35-50 LPA)',
        'education': "Bachelor's in Design (B.Des), HCI, Interaction Design; UX Bootcamp certifications valued; Portfolio is most important",
        'growth': '18-20% growth, explosive demand in Indian tech startups, product companies, fintech, e-commerce',
        'top_companies': ['Flipkart - Bengaluru', 'Amazon India - Bengaluru/Hyderabad/Delhi', 'Paytm - Noida/Delhi', 'Razorpay - Bengaluru', 'PhonePe - Bengaluru', 'Groww - Bengaluru', 'CRED - Bengaluru', 'Unacademy - Bengaluru', 'BYJU\'s - Bengaluru', 'Swiggy - Bengaluru', 'Zomato - Gurugram', 'Ola - Bengaluru', 'Meesho - Bengaluru', 'Nykaa - Mumbai', 'Myntra - Bengaluru', 'Dream11 - Mumbai', 'PolicyBazaar - Gurugram', 'UpGrad - Mumbai', 'Tech Product Companies: Freshworks (Chennai), Zoho (Chennai), Postman (Bengaluru), InMobi (Bengaluru)'],
        'indian_hubs': ['Bengaluru (UX Capital)', 'Mumbai', 'Delhi NCR (Gurugram, Noida)', 'Pune', 'Hyderabad', 'Chennai', 'Ahmedabad']
    },
    'Lead Animator': {
        'description': 'Animators create moving images and visual effects for Indian films, TV, video games, advertising, and digital content.',
        'skills': ['Animation Software (Maya, Blender, After Effects, Cinema 4D)', 'Storyboarding', 'Character Design', 'Timing & Spacing', 'Motion Graphics', 'Creativity', 'Attention to Detail', '3D Modeling & Rigging', '2D Animation'],
        'salary_range': '₹3,00,000 - ₹15,00,000 per year (Entry Junior: ₹3-5 LPA, Mid: ₹6-10 LPA, Senior: ₹11-15 LPA, Lead Animator: ₹16-22 LPA)',
        'education': "Bachelor's in Animation, Fine Arts, Multimedia; Diploma from institutes like Arena, MAAC, Frameboxx, Whistling Woods, FTII",
        'growth': '12-15% growth, Indian animation industry growing rapidly (Karan Johar\'s Brahmastra VFX, Baahubali success), OTT platforms increasing demand',
        'top_companies': ['Technicolor India - Bengaluru/Mumbai', 'Dhruva Interactive (Rockstar) - Bengaluru', 'Lakshya Digital - Gurugram/Pune', 'Pixion - Mumbai', 'DQ Entertainment - Hyderabad', 'Green Gold Animation (Chhota Bheem) - Hyderabad', 'Cosmos-Maya (Motu Patlu) - Mumbai', 'Toonz Animation - Thiruvananthapuram', 'Tata Elxsi VFX - Bengaluru', 'Prime Focus (Double Negative) - Mumbai/Chennai', 'Red Chillies VFX - Mumbai', 'PhantomFX - Hyderabad', 'Assemblage Entertainment - Mumbai', 'Xentrix Studios - Mumbai/Bengaluru', 'Rockstar Games India - Bengaluru', 'Ubisoft India - Pune'],
        'indian_hubs': ['Mumbai (Bollywood VFX)', 'Bengaluru', 'Hyderabad', 'Chennai', 'Pune', 'Thiruvananthapuram', 'Gurugram', 'Kolkata']
    },
    'Game Designer': {
        'description': 'Game designers create concepts, mechanics, levels, and gameplay experiences for Indian video games (mobile, PC, console).',
        'skills': ['Game Design Principles', 'Level Design', 'Game Mechanics', 'Scripting (Lua, Python)', 'Storytelling & Narrative Design', 'Player Psychology', 'Balance & Tuning', 'Game Engines (Unity, Unreal)', 'Game Documentation'],
        'salary_range': '₹4,00,000 - ₹25,00,000 per year (Entry Junior: ₹4-7 LPA, Game Designer: ₹8-12 LPA, Senior: ₹13-18 LPA, Lead Designer: ₹20-25 LPA, Game Director: ₹30+ LPA)',
        'education': "Bachelor's in Game Design, Computer Science, B.Des; Certifications in Unity/Unreal; Strong portfolio of game projects crucial",
        'growth': '15% growth, Indian gaming industry booming (India has 500M+ gamers), mobile gaming and real-money gaming driving growth',
        'top_companies': ['Dream11 - Mumbai', 'Games24x7 - Mumbai', 'Moonfrog Labs - Bengaluru', 'Junglee Games - Gurugram/Bengaluru', 'Nazara Technologies - Mumbai', 'Octro Inc - Noida/Delhi NCR', 'Nextwave Multimedia (World Cricket Championship) - Chennai', 'PlaySimple Games - Bengaluru', 'Pocket Gems - Bengaluru', 'Zynga India - Bengaluru', 'Ubisoft India - Pune/Mumbai', 'Electronic Arts (EA) India - Hyderabad/Bengaluru', 'Rockstar Games India - Bengaluru', 'Lakshya Digital - Gurugram/Pune', 'Dhruva Interactive - Bengaluru', 'Nukebox Studios - Bengaluru', 'SuperGaming - Pune', 'Gametion Technologies - Mumbai (Ludo King)'],
        'indian_hubs': ['Bengaluru', 'Mumbai', 'Pune', 'Hyderabad', 'Chennai', 'Gurugram', 'Noida', 'Kolkata']
    },
    'Art Director': {
        'description': 'Art Directors lead creative projects, manage design teams, and establish visual direction for Indian advertising, publishing, film, and digital media.',
        'skills': ['Creative Leadership', 'Visual Design', 'Team Management', 'Client Communication', 'Project Management', 'Adobe Creative Suite', 'Typography & Color Theory', 'Brand Strategy', 'Art Direction'],
        'salary_range': '₹8,00,000 - ₹30,00,000 per year (Mid: ₹8-15 LPA, Senior AD: ₹16-22 LPA, Creative Director: ₹25-35 LPA, Group CD: ₹40-50 LPA)',
        'education': "Bachelor's/Master's in Fine Arts, Design, Visual Communication; BFA/MFA, B.Des/M.Des; Portfolio and experience most critical",
        'growth': '8-10% growth, ad agencies expanding, digital content boom, brand storytelling importance, OTT platforms hiring creative directors',
        'top_companies': ['Ogilvy - Mumbai/Delhi/Bengaluru/Chennai/Kolkata', 'McCann Worldgroup - Mumbai/Delhi/Bengaluru', 'FCB India - Mumbai/Delhi/Bengaluru', 'Leo Burnett - Mumbai/Delhi/Bengaluru', 'DDB Mudra - Mumbai/Delhi/Bengaluru', 'BBDO India - Mumbai/Delhi', 'Havas Worldwide - Mumbai/Delhi/Bengaluru', 'Wunderman Thompson - Mumbai/Delhi/Bengaluru', 'Publicis India - Mumbai/Delhi/Bengaluru', 'Grey Group - Mumbai/Delhi/Bengaluru', 'Lowe Lintas - Mumbai/Bengaluru/Delhi', 'Contract Advertising - Mumbai/Delhi/Bengaluru', 'Taproot Dentsu - Mumbai/Delhi/Bengaluru', 'Scarecrow M&C Saatchi - Mumbai', 'Famous Innovations - Mumbai/Bengaluru'],
        'indian_hubs': ['Mumbai (Ad Capital)', 'Delhi NCR', 'Bengaluru', 'Chennai', 'Kolkata', 'Pune', 'Hyderabad']
    },
    'Creative Consultant': {
        'description': 'Creative strategists develop creative campaigns and brand strategies, bridging creative teams and business objectives for Indian brands.',
        'skills': ['Creative Strategy', 'Brand Planning', 'Consumer Insights', 'Market Research', 'Campaign Development', 'Client Presentation', 'Storytelling', 'Competitor Analysis', 'Digital Trends'],
        'salary_range': '₹6,00,000 - ₹25,00,000 per year (Entry Strategist: ₹6-10 LPA, Mid: ₹11-16 LPA, Senior: ₹17-22 LPA, Planning Director: ₹24-30 LPA)',
        'education': "Bachelor's/Master's in Advertising, Marketing, Communications; MBA preferred; Psychology/Anthropology background valued",
        'growth': '12-15% growth, ad agencies strengthening strategy teams, brands need insights-led campaigns, data-driven creative important',
        'top_companies': ['Ogilvy Strategy - Mumbai/Delhi/Bengaluru', 'BBDO Strategy - Mumbai/Delhi', 'FCB Ulka Strategy - Mumbai/Delhi/Bengaluru', 'McCann Strategy - Mumbai/Delhi/Bengaluru', 'DDB Mudra Strategy - Mumbai/Delhi/Bengaluru', 'Leo Burnett Strategy - Mumbai/Delhi/Bengaluru', 'Havas Strategy - Mumbai/Delhi/Bengaluru', 'Publicis Strategy - Mumbai/Delhi/Bengaluru', 'Wunderman Thompson Strategy - Mumbai/Delhi/Bengaluru', 'Contract Strategy - Mumbai/Delhi/Bengaluru', 'Taproot Dentsu Strategy - Mumbai/Delhi/Bengaluru'],
        'indian_hubs': ['Mumbai', 'Delhi NCR', 'Bengaluru', 'Chennai', 'Kolkata', 'Pune']
    },
    'Creative Director': {
        'description': 'Creative strategists develop creative campaigns and brand strategies, bridging creative teams and business objectives for Indian brands.',
        'skills': ['Creative Strategy', 'Brand Planning', 'Consumer Insights', 'Market Research', 'Campaign Development', 'Client Presentation', 'Storytelling', 'Competitor Analysis', 'Digital Trends'],
        'salary_range': '₹6,00,000 - ₹25,00,000 per year (Entry Strategist: ₹6-10 LPA, Mid: ₹11-16 LPA, Senior: ₹17-22 LPA, Planning Director: ₹24-30 LPA)',
        'education': "Bachelor's/Master's in Advertising, Marketing, Communications; MBA preferred; Psychology/Anthropology background valued",
        'growth': '12-15% growth, ad agencies strengthening strategy teams, brands need insights-led campaigns, data-driven creative important',
        'top_companies': ['Ogilvy Strategy - Mumbai/Delhi/Bengaluru', 'BBDO Strategy - Mumbai/Delhi', 'FCB Ulka Strategy - Mumbai/Delhi/Bengaluru', 'McCann Strategy - Mumbai/Delhi/Bengaluru', 'DDB Mudra Strategy - Mumbai/Delhi/Bengaluru', 'Leo Burnett Strategy - Mumbai/Delhi/Bengaluru', 'Havas Strategy - Mumbai/Delhi/Bengaluru', 'Publicis Strategy - Mumbai/Delhi/Bengaluru', 'Wunderman Thompson Strategy - Mumbai/Delhi/Bengaluru', 'Contract Strategy - Mumbai/Delhi/Bengaluru', 'Taproot Dentsu Strategy - Mumbai/Delhi/Bengaluru'],
        'indian_hubs': ['Mumbai', 'Delhi NCR', 'Bengaluru', 'Chennai', 'Kolkata', 'Pune']
    },

    # ==================== 5. MANUFACTURING CAREERS ====================
    'Production Manager': {
        'description': 'Production managers oversee manufacturing operations, ensuring efficient production schedules, quality standards, and safety compliance in Indian factories.',
        'skills': ['Production Planning', 'Lean Manufacturing', 'Process Optimization', 'Quality Control', 'Team Leadership', 'Resource Allocation', 'Inventory Management', 'Safety Management', 'Cost Reduction'],
        'salary_range': '₹6,00,000 - ₹25,00,000 per year (Entry Production Engineer: ₹4-6 LPA, Production Manager: ₹8-15 LPA, Senior: ₹16-22 LPA, Plant Manager: ₹25-35 LPA)',
        'education': "B.Tech in Mechanical/Industrial/Production Engineering, Diploma in Manufacturing, MBA in Operations preferred",
        'growth': '8-10% growth, Make in India initiative, manufacturing sector expansion, Industry 4.0 skills valued',
        'top_companies': ['Tata Motors - Pune/Mumbai/Jamshedpur', 'Maruti Suzuki - Gurugram/Manesar', 'Mahindra & Mahindra - Mumbai/Pune/Chennai', 'Bajaj Auto - Pune/Aurangabad', 'Hero MotoCorp - Gurugram/Haridwar', 'Reliance Industries - Jamnagar/Vadodara/Mumbai', 'Adani Group - Ahmedabad/Mundra', 'Bosch India - Bengaluru/Nashik/Jaipur', 'Cummins India - Pune/Phaltan', 'Siemens India - Mumbai/Goa/Bengaluru', 'Larsen & Toubro - Mumbai/Chennai/Bengaluru'],
        'indian_hubs': ['Pune', 'Mumbai', 'Chennai', 'Ahmedabad', 'Gurugram', 'Bengaluru', 'Jamshedpur', 'Jaipur', 'Indore']
    },
    'Quality Control Engineer': {
        'description': 'Quality control engineers ensure product quality meets specifications, conduct inspections, implement quality systems, and drive continuous improvement in Indian manufacturing.',
        'skills': ['Quality Management (ISO 9001, Six Sigma)', 'Statistical Process Control (SPC)', 'Root Cause Analysis', 'Inspection Techniques', 'Calibration', 'Auditing', 'Quality Tools (8D, FMEA, Kaizen)', 'GD&T', 'Testing & Measurement'],
        'salary_range': '₹3,50,000 - ₹15,00,000 per year (Entry: ₹3.5-5 LPA, Quality Engineer: ₹5-9 LPA, Sr QC Engineer: ₹10-14 LPA, Quality Manager: ₹15-20 LPA)',
        'education': "B.Tech in Mechanical/Industrial/Production Engineering, Diploma, Six Sigma Green/Black Belt certification valued",
        'growth': '8-10% growth, critical role in manufacturing, automotive & auto-component sector demand, quality standards compliance essential',
        'top_companies': ['Tata Motors - Pune/Mumbai/Jamshedpur/Sanand', 'Mahindra & Mahindra - Pune/Mumbai/Chennai', 'Maruti Suzuki - Gurugram/Manesar', 'Bajaj Auto - Pune/Aurangabad', 'Bosch India - Bengaluru/Nashik/Jaipur', 'Cummins India - Pune/Phaltan', 'Siemens India - Mumbai/Goa/Bengaluru', 'L&T - Mumbai/Chennai/Bengaluru', 'Ashok Leyland - Chennai/Hosur', 'TVS Motors - Chennai/Hosur', 'Hero MotoCorp - Haridwar/Neemrana'],
        'indian_hubs': ['Pune', 'Chennai', 'Mumbai', 'Gurugram', 'Bengaluru', 'Ahmedabad', 'Jaipur', 'Hosur', 'Haridwar']
    },
    'Manufacturing Engineer': {
        'description': 'Manufacturing engineers design, implement, and improve production processes, equipment, and systems to optimize efficiency and quality in Indian factories.',
        'skills': ['Process Design & Optimization', 'Lean Manufacturing & Six Sigma', 'CAD/CAM (AutoCAD, SolidWorks)', 'Automation & Robotics', 'Tooling & Fixture Design', 'Workflow Analysis', 'Industry 4.0', 'Cost Reduction', 'Assembly Line Design'],
        'salary_range': '₹4,00,000 - ₹18,00,000 per year (Entry: ₹4-6 LPA, Manufacturing Eng: ₹7-12 LPA, Senior: ₹13-16 LPA, Lead: ₹17-22 LPA)',
        'education': "B.Tech in Mechanical/Industrial/Manufacturing Engineering; M.Tech in Manufacturing preferred; Lean/Kaizen certifications valued",
        'growth': '9-11% growth, Make in India driving manufacturing engineering demand, automation skills highly valued, Industry 4.0 expertise premium',
        'top_companies': ['Tata Motors - Pune/Mumbai/Jamshedpur', 'Mahindra & Mahindra - Mumbai/Pune/Chennai', 'Maruti Suzuki - Gurugram/Manesar', 'Bajaj Auto - Pune/Aurangabad', 'Hero MotoCorp - Gurugram/Haridwar', 'TVS Motors - Chennai/Hosur', 'Reliance Industries - Jamnagar/Vadodara', 'Bosch India - Bengaluru/Nashik/Jaipur', 'Cummins India - Pune/Phaltan', 'Siemens India - Mumbai/Goa/Bengaluru', 'Schaeffler India - Pune/Hosur', 'ZF India - Pune/Hyderabad', 'Bharat Forge - Pune'],
        'indian_hubs': ['Pune', 'Chennai', 'Mumbai', 'Ahmedabad', 'Gurugram', 'Bengaluru', 'Jamshedpur', 'Jaipur', 'Hosur', 'Coimbatore']
    },

    # ==================== 6. CONSTRUCTION CAREERS ====================
    'Civil Engineer': {
        'description': 'Civil engineers design, plan, and oversee construction projects including buildings, bridges, roads, dams, and infrastructure in India.',
        'skills': ['Structural Analysis & Design', 'AutoCAD & Revit', 'STAAD Pro', 'Project Planning', 'Site Supervision', 'Material Testing', 'Quality Control', 'Safety Management', 'Quantity Surveying'],
        'salary_range': '₹3,00,000 - ₹20,00,000 per year (Entry Junior Eng: ₹3-5 LPA, Civil Engineer: ₹5-9 LPA, Senior: ₹10-15 LPA, Project Manager: ₹16-22 LPA)',
        'education': 'B.Tech/BE in Civil Engineering, Diploma in Civil Engineering, M.Tech in Structural/Construction Management for senior roles',
        'growth': '8-10% growth, infrastructure boom (roads, railways, metros, smart cities), real estate recovery, government spending on infrastructure',
        'top_companies': ['Larsen & Toubro (L&T) - Mumbai/Chennai/Bengaluru', 'Shapoorji Pallonji - Mumbai/Pune', 'Tata Projects - Mumbai/Hyderabad/Delhi', 'NCC Limited - Hyderabad/Chennai', 'Gammon India - Mumbai/Delhi', 'Prestige Group - Bengaluru/Chennai', 'Godrej Properties - Mumbai/Bengaluru/Pune', 'DLF Limited - Gurugram/Delhi', 'Sobha Limited - Bengaluru/Chennai', 'Brigade Group - Bengaluru/Chennai'],
        'indian_hubs': ['Mumbai', 'Delhi NCR', 'Bengaluru', 'Chennai', 'Hyderabad', 'Pune', 'Ahmedabad', 'Kolkata', 'Lucknow']
    },
    'Construction Manager': {
        'description': 'Construction managers plan, coordinate, budget, and supervise construction projects from start to finish for Indian real estate and infrastructure.',
        'skills': ['Project Management (PMP, Primavera P6, MS Project)', 'Budgeting & Cost Control', 'Contract Management', 'Resource Allocation', 'Site Safety Management', 'Team Leadership', 'Scheduling', 'Quality Assurance', 'Risk Management'],
        'salary_range': '₹6,00,000 - ₹30,00,000 per year (Construction Manager: ₹8-15 LPA, Sr CM: ₹16-22 LPA, Project Director: ₹25-35 LPA, VP Construction: ₹40-50 LPA)',
        'education': "B.Tech Civil + MBA in Construction Management/PMP; Diploma in Construction Management; M.Tech in Construction Management",
        'growth': '10-12% growth, large-scale infrastructure projects require experienced managers, government smart cities mission, real estate developers expanding',
        'top_companies': ['Larsen & Toubro (L&T) - Mumbai/Chennai/Delhi', 'Shapoorji Pallonji - Mumbai/Pune/Chennai', 'Tata Realty - Mumbai/Hyderabad', 'DLF Limited - Gurugram', 'Godrej Properties - Mumbai/Bengaluru/Pune', 'Prestige Group - Bengaluru/Chennai/Hyderabad', 'Sobha Limited - Bengaluru/Chennai', 'Brigade Enterprises - Bengaluru', 'National Highways Authority of India (NHAI) - Delhi', 'Delhi Metro Rail Corp (DMRC) - Delhi', 'Mumbai Metro - Mumbai', 'Bengaluru Metro (BMRCL) - Bengaluru'],
        'indian_hubs': ['Mumbai', 'Delhi NCR', 'Bengaluru', 'Chennai', 'Hyderabad', 'Pune', 'Ahmedabad', 'Kolkata']
    },
    'Project Manager': {
        'description': 'Project managers lead construction projects, managing timelines, budgets, resources, teams, and stakeholders for successful project delivery in India.',
        'skills': ['PMP/Prince2 Certification', 'Primavera P6/MS Project', 'Budget Management', 'Risk Management', 'Contract Management', 'Team Leadership', 'Stakeholder Communication', 'Quality Control', 'Safety Compliance'],
        'salary_range': '₹8,00,000 - ₹40,00,000 per year (Project Manager: ₹10-18 LPA, Sr PM: ₹19-25 LPA, Program Manager: ₹26-35 LPA, Project Director: ₹36-50 LPA)',
        'education': "B.Tech Civil/Mechanical/Electrical + MBA/PMP; Project Management certification (PMP, PRINCE2) highly valued",
        'growth': '10-12% growth, infrastructure projects need certified PMs, real estate, industrial projects, government infrastructure',
        'top_companies': ['L&T Construction - Mumbai/Chennai', 'Tata Projects - Mumbai/Hyderabad', 'Shapoorji Pallonji - Mumbai', 'DLF Limited - Gurugram', 'Godrej Properties - Mumbai', 'Prestige Group - Bengaluru', 'Sobha Limited - Bengaluru', 'NCC Limited - Hyderabad', 'NHAI - Delhi', 'Indian Railways (RVNL) - Delhi', 'Metro Rail Corporations (Delhi, Mumbai, Bengaluru, Chennai, Kolkata, Hyderabad, Lucknow, Ahmedabad)'],
        'indian_hubs': ['Mumbai', 'Delhi NCR', 'Bengaluru', 'Chennai', 'Hyderabad', 'Pune', 'Ahmedabad', 'Kolkata', 'Lucknow', 'Jaipur']
    },

    # ==================== 7. AGRICULTURE CAREERS ====================
    'Agricultural Engineer': {
        'description': 'Agricultural engineers design and develop farm equipment, irrigation systems, and agricultural machinery to improve farming efficiency in India.',
        'skills': ['Farm Machinery Design', 'Irrigation Systems', 'Soil & Water Conservation', 'CAD Software', 'Post-harvest Technology', 'Renewable Energy (Solar pumps)', 'Precision Agriculture', 'Agri-mechatronics'],
        'salary_range': '₹3,00,000 - ₹12,00,000 per year (Entry: ₹3-5 LPA, Engineer: ₹5-8 LPA, Senior: ₹9-12 LPA)',
        'education': 'B.Tech Agricultural Engineering, M.Tech in Farm Machinery/Water Resources Engineering',
        'growth': '8-10% growth, government focus on farm mechanization, PM-KUSUM scheme for solar pumps, subsidy-driven demand for farm equipment',
        'top_companies': ['Mahindra & Mahindra Agri - Mumbai/Nagpur', 'John Deere India - Pune/Delhi NCR', 'Escorts Agri Machinery - Faridabad/Delhi NCR', 'Kubota India - Delhi NCR', 'New Holland (CNH) - Delhi NCR', 'Tafe Tractors - Chennai', 'Swaraj Tractors (Mahindra) - Ludhiana', 'Sonalika Tractors - Ludhiana', 'Jain Irrigation Systems - Jalgaon/Mumbai', 'Netafim India - Bengaluru/Delhi', 'Rivulis Irrigation - Mumbai/Bengaluru', 'Precision Farming Development Centres (PFDC) - All India', 'ICAR Institutes - Across India'],
        'indian_hubs': ['Punjab (Ludhiana)', 'Delhi NCR', 'Pune', 'Chennai', 'Bengaluru', 'Nagpur', 'Ahmedabad', 'Jalgaon']
    },
    'Food Technologist': {
        'description': 'Food technologists develop and improve food products, ensure quality & safety, and create innovative food processing methods for Indian food industry.',
        'skills': ['Food Science & Technology', 'Quality Control (ISO 22000, HACCP)', 'Food Safety (FSSAI regulations)', 'Product Development', 'Food Microbiology', 'Sensory Evaluation', 'Food Packaging', 'Processing Technology'],
        'salary_range': '₹3,00,000 - ₹12,00,000 per year (Entry: ₹3-5 LPA, Food Technologist: ₹5-8 LPA, Senior: ₹9-12 LPA, R&D Manager: ₹12-18 LPA)',
        'education': 'B.Tech Food Technology, B.Sc Food Science & Technology, M.Tech Food Technology',
        'growth': '12-14% growth, Indian food processing industry growing rapidly (Make in India, Mega Food Parks scheme), health-conscious consumers driving innovation',
        'top_companies': ['Nestlé India - Gurugram/Moga/Nanjangud', 'Britannia Industries - Bengaluru', 'ITC Limited (Foods Division) - Kolkata/Bengaluru', 'PepsiCo India - Gurugram/Mumbai', 'Coca-Cola India - Gurugram', 'Parle Agro - Mumbai', 'Hindustan Unilever (Foods) - Mumbai', 'Amul (GCMMF) - Anand/Gujarat', 'Mother Dairy - Delhi NCR', 'Dabur India - Delhi NCR', 'Adani Wilmar - Ahmedabad', 'McCain Foods - Delhi NCR', 'Mondelez India (Cadbury) - Mumbai/Delhi', 'Perfetti Van Melle - Delhi NCR'],
        'indian_hubs': ['Delhi NCR', 'Mumbai', 'Bengaluru', 'Kolkata', 'Chennai', 'Pune', 'Ahmedabad', 'Anand (Gujarat)']
    },
    'Agribusiness Manager': {
        'description': 'Agribusiness managers oversee agricultural companies, manage farm operations, handle supply chains, and drive business growth in Indian agriculture sector.',
        'skills': ['Agribusiness Management', 'Supply Chain Management', 'Market Analysis', 'Farm Management', 'Commodity Trading', 'Agri-marketing', 'Financial Management', 'Contract Farming', 'Export-Import Knowledge'],
        'salary_range': '₹4,00,000 - ₹18,00,000 per year (Entry: ₹4-6 LPA, Manager: ₹7-12 LPA, Senior: ₹13-16 LPA, Director: ₹17-20 LPA)',
        'education': 'MBA in Agribusiness, B.Sc Agriculture + MBA, PGDM in Agribusiness (MANAGE, IRMA, IIM Ahmedabad FABM)',
        'growth': '10-12% growth, agribusiness sector booming, startups in agritech, e-NAM (electronic National Agriculture Market), corporate farming growth',
        'top_companies': ['ITC Agri Business Division - Kolkata/Hyderabad', 'Godrej Agrovet - Mumbai/Hyderabad', 'Rallis India (Tata Group) - Mumbai/Bengaluru', 'UPL Limited - Mumbai', 'Dhanuka Agritech - Delhi NCR', 'PI Industries - Jaipur/Mumbai', 'Sumitomo Chemical India - Mumbai', 'Coromandel International - Chennai/Hyderabad', 'Nagarjuna Agrichem - Hyderabad', 'Advanta Seeds - Hyderabad/Delhi NCR', 'Nuziveedu Seeds - Hyderabad', 'Mahyco - Mumbai/Delhi NCR', 'PepsiCo Agribusiness - Gurugram', 'Cargill India - Gurugram/Bengaluru', 'Olam India - Delhi NCR'],
        'indian_hubs': ['Mumbai', 'Delhi NCR', 'Hyderabad', 'Bengaluru', 'Chennai', 'Ahmedabad', 'Kolkata', 'Jaipur']
    },

    # ==================== 8. MATHEMATICS CAREERS ====================
    'Actuary': {
        'description': 'Actuaries analyze financial risks for Indian insurance companies, pension funds, and financial institutions using mathematics, statistics, and financial theory.',
        'skills': ['Probability & Statistics', 'Financial Mathematics', 'Risk Modeling', 'Data Analysis', 'Insurance Regulations (IRDAI)', 'Reserving & Pricing', 'Valuation', 'Stochastic Modeling', 'Actuarial Software'],
        'salary_range': '₹6,00,000 - ₹40,00,000 per year (Entry (passed few exams): ₹6-9 LPA, Near-qualified: ₹12-18 LPA, Qualified Actuary (Fellow): ₹20-35 LPA, Chief Actuary: ₹40-70 LPA)',
        'education': 'Actuarial Science degree + passing IFoA (Institute and Faculty of Actuaries, UK) or IAI (Institute of Actuaries of India) exams. Typically 15+ exams, 6-8 years to qualify.',
        'growth': '15-18% growth, IRDAI requires all insurance companies to have appointed actuaries, growing demand in banking, pensions, and enterprise risk management',
        'top_companies': ['Insurance Companies: LIC (Mumbai/Delhi/Chennai/Kolkata), HDFC Life (Mumbai), ICICI Prudential (Mumbai), SBI Life (Mumbai), Max Life (Delhi NCR), Kotak Life (Mumbai), Bajaj Allianz (Pune), Tata AIA (Mumbai), Reliance Nippon (Mumbai), Birla Sun Life (Mumbai), Aditya Birla Sun Life (Mumbai), PNB MetLife (Delhi NCR)', 'Consulting Firms: Milliman (Mumbai/Delhi), Mercer (Mumbai/Delhi), Aon India (Mumbai/Delhi), Willis Towers Watson (Mumbai/Delhi/Delhi NCR), Ernst & Young (Mumbai/Delhi), PwC (Mumbai/Delhi), KPMG (Mumbai/Delhi), Deloitte (Mumbai/Delhi)'],
        'indian_hubs': ['Mumbai', 'Delhi NCR', 'Chennai', 'Bengaluru', 'Hyderabad', 'Kolkata', 'Pune']
    },
    'Statistician': {
        'description': 'Statisticians design surveys, collect and analyze data, and interpret results to help Indian organizations make data-driven decisions.',
        'skills': ['Statistical Analysis (R, SPSS, Stata, SAS)', 'Survey Design', 'Data Collection & Sampling', 'Hypothesis Testing', 'Regression Analysis', 'Data Visualization', 'Statistical Modeling', 'Machine Learning Basics'],
        'salary_range': '₹4,00,000 - ₹20,00,000 per year (Entry: ₹4-7 LPA, Statistician: ₹8-12 LPA, Senior: ₹13-17 LPA, Lead: ₹18-22 LPA)',
        'education': 'B.Sc/M.Sc Statistics, M.Stat from Indian Statistical Institute (ISI) highly valued, PhD for research roles',
        'growth': '12-14% growth, data-driven decision making across industries, RBI/Government demand for statisticians, research organizations',
        'top_companies': ['Indian Statistical Institute (ISI) - Kolkata/Delhi/Bengaluru/Chennai', 'RBI - Mumbai', 'NITI Aayog - Delhi', 'Ministry of Statistics - Delhi', 'National Sample Survey Office (NSSO) - Delhi/Kolkata', 'ICAR - Delhi', 'ICMR - Delhi', 'WHO India - Delhi', 'UNICEF India - Delhi', 'World Bank India - Delhi', 'Mu Sigma - Bengaluru', 'Fractal Analytics - Mumbai/Bengaluru', 'Tiger Analytics - Chennai/Bengaluru', 'Absolutdata - Gurugram', 'CRISIL - Mumbai', 'ICRA - Gurugram', 'Care Ratings - Mumbai'],
        'indian_hubs': ['Kolkata (ISI)', 'Delhi NCR', 'Mumbai', 'Bengaluru', 'Hyderabad', 'Chennai', 'Pune']
    },

    # ==================== 9. PHYSICS CAREERS ====================
    'Research Scientist (Physics)': {
        'description': 'Research scientists conduct experimental and theoretical physics research in Indian national labs, universities, and research institutions.',
        'skills': ['Experimental Design', 'Data Analysis (Python, MATLAB, ROOT)', 'Scientific Computing', 'Instrumentation', 'Theoretical Modeling', 'Research Publication', 'Grant Writing', 'Collaboration', 'Presentation Skills'],
        'salary_range': '₹5,00,000 - ₹25,00,000 per year (Research Fellow: ₹3.5-5 LPA, Scientist B/C: ₹8-12 LPA, Senior Scientist: ₹15-20 LPA, Principal Scientist: ₹22-30 LPA)',
        'education': 'M.Sc Physics + PhD (must), Post-doc experience for permanent positions, JEST/JAM/GATE/NET qualification essential',
        'growth': '8-10% growth in R&D, government funding for research (DST, DAE, DRDO, ISRO), private R&D expansion',
        'top_companies': ['ISRO - Bengaluru/Thiruvananthapuram/Ahmedabad/Sriharikota', 'DRDO - Delhi/Hyderabad/Bengaluru/Pune', 'BARC - Mumbai', 'TIFR - Mumbai/Bengaluru/Hyderabad', 'IISc - Bengaluru', 'IIT Physics Departments - Across IITs (Mumbai, Delhi, Chennai, Kanpur, Kharagpur, Roorkee, Guwahati)', 'PRL - Ahmedabad', 'Saha Institute of Nuclear Physics - Kolkata', 'RRI - Bengaluru', 'IIA - Bengaluru', 'NISER - Bhubaneswar', 'IUCAA - Pune', 'IOP - Bhubaneswar', 'IMSc - Chennai', 'HRI - Allahabad', 'Bose Institute - Kolkata', 'Variable Energy Cyclotron Centre - Kolkata'],
        'indian_hubs': ['Bengaluru', 'Mumbai', 'Delhi NCR', 'Pune', 'Kolkata', 'Ahmedabad', 'Chennai', 'Hyderabad']
    },
    'Astrophysicist': {
        'description': 'Astrophysicists study celestial objects, cosmic phenomena, and the universe using telescopes, satellites, and theoretical models in India.',
        'skills': ['Astronomy & Astrophysics', 'Data Analysis (Python, IRAF, DS9)', 'Observational Techniques', 'Computational Modeling', 'Telescope Operation', 'Spectroscopy', 'Image Processing', 'Statistics', 'Scientific Programming'],
        'salary_range': '₹5,00,000 - ₹22,00,000 per year (Research Associate: ₹4-7 LPA, Scientist: ₹9-14 LPA, Senior: ₹15-20 LPA)',
        'education': 'M.Sc Physics/Astronomy + PhD, JEST/JAM/NET/INAT eligibility, Post-doc for senior positions',
        'growth': '8-10% growth, Indian astronomy expanding (AstroSat, MACE, LIGO-India, Square Kilometre Array participation), government R&D funding',
        'top_companies': ['ISRO (AstroSat mission) - Bengaluru', 'Indian Institute of Astrophysics (IIA) - Bengaluru/Kodaikanal', 'Inter-University Centre for Astronomy & Astrophysics (IUCAA) - Pune', 'TIFR (Astronomy & Astrophysics) - Mumbai', 'Raman Research Institute (RRI) - Bengaluru', 'Physical Research Laboratory (PRL) - Ahmedabad', 'IIT Kanpur (Astrophysics) - Kanpur', 'IIT Bombay (Astrophysics) - Mumbai', 'NCRA-TIFR (Radio Astronomy) - Pune', 'Udaipur Solar Observatory - Udaipur', 'Aryabhatta Research Institute of Observational Sciences (ARIES) - Nainital', 'National Centre for Radio Astrophysics (NCRA) - Pune'],
        'indian_hubs': ['Bengaluru', 'Pune', 'Mumbai', 'Ahmedabad', 'Delhi NCR', 'Kolkata', 'Hyderabad', 'Nainital']
    },

    # ==================== 10. CHEMISTRY CAREERS ====================
    'Chemist (Analytical)': {
        'description': 'Analytical chemists analyze chemical substances, perform quality control, and develop test methods for Indian pharmaceutical, chemical, and food industries.',
        'skills': ['Analytical Techniques (HPLC, GC, LC-MS, GC-MS, FTIR, UV-Vis)', 'Wet Chemistry', 'Method Development & Validation', 'Quality Control (QC)', 'GMP/GLP Compliance', 'Data Analysis', 'Lab Safety', 'Documentation (SOPs, Lab Notebooks)'],
        'salary_range': '₹2,50,000 - ₹10,00,000 per year (Entry: ₹2.5-4 LPA, Chemist: ₹4-7 LPA, Senior: ₹7-10 LPA, Lab Manager: ₹10-15 LPA)',
        'education': 'B.Sc/M.Sc Chemistry (Analytical specialization preferred), B.Pharma also eligible, PhD for R&D roles',
        'growth': '9-11% growth, pharmaceutical and chemical industry expansion, quality control essential in pharma, food, and environmental testing',
        'top_companies': ['Sun Pharmaceutical - Mumbai/Vadodara', 'Dr. Reddy\'s Laboratories - Hyderabad', 'Cipla - Mumbai/Bengaluru', 'Lupin - Mumbai/Pune/Indore', 'Aurobindo Pharma - Hyderabad', 'Torrent Pharma - Ahmedabad', 'Reliance Industries - Jamnagar/Vadodara', 'Gujarat Fluorochemicals - Vadodara', 'SRF Limited - Gurugram/Bhopal', 'Pidilite Industries - Mumbai', 'Asian Paints - Mumbai', 'Godrej Industries - Mumbai'],
        'indian_hubs': ['Mumbai', 'Hyderabad', 'Vadodara', 'Ahmedabad', 'Pune', 'Bengaluru', 'Delhi NCR', 'Chennai']
    },
    'Pharmaceutical Scientist': {
        'description': 'Pharmaceutical scientists discover and develop new drugs, optimize formulations, and conduct clinical research for Indian pharma companies.',
        'skills': ['Drug Discovery & Development', 'Medicinal Chemistry', 'Formulation Development', 'Pharmacology', 'ADME/Tox Studies', 'Clinical Research', 'Regulatory Affairs (DCGI, USFDA, EMA)', 'Quality by Design (QbD)', 'Process Chemistry'],
        'salary_range': '₹4,00,000 - ₹25,00,000 per year (Research Associate: ₹4-7 LPA, Scientist: ₹8-14 LPA, Sr Scientist: ₹15-20 LPA, R&D Manager: ₹22-30 LPA)',
        'education': 'B.Pharma/M.Pharma (Pharmaceutics, Pharmacology, Medicinal Chemistry), PhD for leadership roles',
        'growth': '12-14% growth, Indian pharma R&D expanding, focus on novel drug discovery, biosimilars, and complex generics',
        'top_companies': ['Sun Pharma R&D - Mumbai/Vadodara/Gurugram', 'Dr. Reddy\'s R&D - Hyderabad', 'Lupin R&D - Pune/Mumbai/Indore', 'Cipla R&D - Mumbai/Bengaluru', 'Aurobindo Pharma R&D - Hyderabad', 'Biocon R&D - Bengaluru', 'Syngene (Biocon) - Bengaluru/Hyderabad', 'Serum Institute R&D - Pune', 'Zydus Cadila R&D - Ahmedabad', 'Wockhardt R&D - Mumbai/Aurangabad', 'Jubilant Life Sciences R&D - Noida'],
        'indian_hubs': ['Hyderabad (Genome Valley)', 'Mumbai', 'Bengaluru', 'Pune', 'Ahmedabad', 'Delhi NCR']
    },

    # ==================== 11. BIOLOGY CAREERS ====================
    'Biotechnologist': {
        'description': 'Biotechnologists apply biology and technology to develop products and processes in healthcare, agriculture, and environment sectors in India.',
        'skills': ['Molecular Biology (PCR, Gel electrophoresis)', 'Cell Culture', 'Fermentation Technology', 'Protein Purification', 'Genetic Engineering (CRISPR)', 'Bioreactor Operation', 'Bioinformatics', 'Downstream Processing', 'GMP Compliance'],
        'salary_range': '₹3,00,000 - ₹15,00,000 per year (Entry: ₹3-5 LPA, Biotech: ₹5-8 LPA, Senior: ₹9-12 LPA, R&D Manager: ₹13-18 LPA)',
        'education': 'B.Tech/M.Tech Biotechnology, B.Sc/M.Sc Biotechnology, PhD for senior R&D roles',
        'growth': '14-16% growth, India\'s biotech sector growing at 15%+, DBT-BIRAC funding for startups, vaccines, biosimilars, and agri-biotech demand',
        'top_companies': ['Biocon - Bengaluru/Mysore', 'Serum Institute of India - Pune', 'Bharat Biotech - Hyderabad', 'Syngene International - Bengaluru/Hyderabad', 'Indian Immunologicals - Hyderabad', 'Panacea Biotec - Delhi NCR', 'Novozymes India - Bengaluru/Delhi NCR', 'Advanced Enzyme Technologies - Mumbai/Nasik', 'Novo Nordisk India - Bengaluru/Delhi NCR', 'Eli Lilly India - Bengaluru', 'Pfizer India R&D - Chennai'],
        'indian_hubs': ['Bengaluru (Biotech Capital)', 'Hyderabad (Genome Valley)', 'Pune', 'Delhi NCR', 'Mumbai', 'Chennai', 'Ahmedabad']
    },
    'Geneticist': {
        'description': 'Geneticists study genes, heredity, and genetic disorders, conducting research and offering genetic counseling in Indian healthcare and research settings.',
        'skills': ['Molecular Genetics', 'Cytogenetics', 'Genomic Analysis', 'Next-Generation Sequencing (NGS)', 'PCR & DNA Sequencing', 'Genetic Counseling', 'Bioinformatics (BLAST, Genome Browsers)', 'CRISPR/Cas9', 'Population Genetics'],
        'salary_range': '₹4,00,000 - ₹18,00,000 per year (Research Associate: ₹4-7 LPA, Geneticist: ₹7-12 LPA, Senior: ₹13-16 LPA, Genetic Counselor: ₹15-20 LPA)',
        'education': 'M.Sc Genetics/Molecular Biology/Human Genetics, PhD for research, Diploma in Genetic Counseling for counseling roles',
        'growth': '12-14% growth, genomics research expanding, precision medicine initiatives, rare disease research, genetic testing demand rising',
        'top_companies': ['Centre for Cellular and Molecular Biology (CCMB) - Hyderabad', 'Institute of Genomics and Integrative Biology (IGIB) - Delhi', 'National Institute of Biomedical Genomics (NIBMG) - Kalyani (WB)', 'Strand Life Sciences - Bengaluru', 'MedGenome - Bengaluru/Delhi NCR', 'Mapmygenome - Hyderabad', 'Xcode Life Sciences - Chennai', 'Genotypic Technology - Bengaluru', 'Premas Life Sciences - Delhi NCR/Bengaluru', 'AIIMS Genetics Dept - Delhi', 'NIMHANS Genetics - Bengaluru'],
        'indian_hubs': ['Hyderabad', 'Bengaluru', 'Delhi NCR', 'Kolkata', 'Mumbai', 'Chennai', 'Pune']
    },

    # ==================== 12. ARTS & HUMANITIES CAREERS ====================
    'Professor (Arts)': {
        'description': 'Professors teach undergraduate and graduate courses in arts, humanities, and social sciences at Indian universities and colleges.',
        'skills': ['Subject Expertise (Literature, History, Philosophy, etc.)', 'Teaching & Pedagogy', 'Curriculum Development', 'Research Methodology', 'Academic Writing & Publishing', 'Student Mentoring', 'Public Speaking', 'Grant Writing', 'Administration'],
        'salary_range': '₹5,00,000 - ₹25,00,000 per year (Assistant Professor: ₹5-9 LPA (UGC scale - Level 10: ₹57,700 + allowances), Associate: ₹10-15 LPA, Professor: ₹16-22 LPA, Senior Professor/Director: ₹25-35 LPA)',
        'education': 'MA/M.Sc + PhD + UGC-NET/JRF mandatory for assistant professor, M.Phil preferred, Post-doc for senior positions',
        'growth': '8-10% growth (government regulations: 103 Central Universities, State Universities expanding), NEP 2020 driving higher education expansion',
        'top_companies': ['Central Universities: Delhi University (Delhi), JNU (Delhi), BHU (Varanasi), University of Hyderabad, University of Calcutta, University of Mumbai, University of Madras, University of Pune (SPPU), University of Bengaluru, Aligarh Muslim University, Jamia Millia Islamia (Delhi)', 'State Universities: Across all state capitals and major cities (Lucknow University, Panjab University, Rajasthan University, Gujarat University, etc.)', 'Deemed Universities & Private: Ashoka University (Delhi NCR), Shiv Nadar University (Delhi NCR), Azim Premji University (Bengaluru), Symbiosis International (Pune), Christ University (Bengaluru)'],
        'indian_hubs': ['Delhi NCR (DU, JNU, Jamia)', 'Mumbai', 'Bengaluru', 'Chennai', 'Kolkata', 'Pune', 'Hyderabad', 'Varanasi', 'Lucknow', 'Chandigarh']
    },
    'Journalist': {
        'description': 'Journalists research, write, and report news stories for Indian newspapers, TV channels, digital media, and news agencies.',
        'skills': ['Reporting & Writing', 'Interviewing', 'Research', 'Digital Journalism', 'Media Ethics', 'Fact-Checking', 'Video/Audio Editing (basic)', 'Social Media Management', 'News Judgment', 'Time Management'],
        'salary_range': '₹2,50,000 - ₹18,00,000 per year (Entry Trainee: ₹2.5-4 LPA, Reporter: ₹4-7 LPA, Senior Reporter: ₹7-10 LPA, Editor: ₹10-15 LPA, News Director/Managing Editor: ₹15-20 LPA)',
        'education': "Bachelor's/Master's in Journalism & Mass Communication (BJMC, MJMC), English/Hindi literature + Journalism diploma",
        'growth': '8-10% growth, digital media boom (News18, The Quint, The Wire, Scroll), regional language media expanding, OTT news platforms',
        'top_companies': ['Print: The Times of India - Mumbai/Delhi/Bengaluru/Chennai/Kolkata, Hindustan Times - Delhi NCR/Mumbai/Lucknow, The Hindu - Chennai/Bengaluru/Delhi/Mumbai/Hyderabad, The Indian Express - Delhi NCR/Mumbai/Chennai/Bengaluru, The Telegraph - Kolkata, The Economic Times - Mumbai/Delhi, Mint - Delhi/Mumbai, Business Standard - Delhi/Mumbai', 'TV News: NDTV - Delhi NCR/Mumbai, CNN-News18 - Delhi NCR/Mumbai, Republic TV - Mumbai, India Today TV - Delhi NCR, Times Now - Mumbai, News18 India - Delhi NCR', 'Digital: The Quint - Delhi NCR, The Wire - Delhi NCR, Scroll.in - Delhi NCR/Mumbai, The Print - Delhi NCR, Newslaundry - Delhi NCR'],
        'indian_hubs': ['Delhi NCR', 'Mumbai', 'Bengaluru', 'Chennai', 'Kolkata', 'Hyderabad', 'Pune', 'Lucknow', 'Ahmedabad']
    },
    'Writer/Author': {
        'description': 'Writers create content for books, magazines, websites, blogs, and other media, including fiction, non-fiction, technical writing, and copywriting in India.',
        'skills': ['Creative Writing', 'Research', 'Editing & Proofreading', 'Storytelling', 'Grammar & Style', 'SEO Writing (for digital)', 'Time Management', 'Self-discipline', 'Publishing Knowledge'],
        'salary_range': 'Highly variable - ₹2,00,000 - ₹50,00,000+ per year (Freelance: ₹2-6 LPA, Staff Writer: ₹4-8 LPA, Content Manager: ₹8-12 LPA, Author (book advances): ₹2-20 LPA, Bestselling Author: ₹50 LPA - 1 Cr+)',
        'education': "No formal degree required; Bachelor's/Master's in English Literature, Journalism, Creative Writing; MFA Creative Writing (rare in India) valued but optional",
        'growth': '10-12% growth, self-publishing boom (Amazon KDP, Pothi, Notion Press), digital content demand, freelance opportunities',
        'top_companies': ['Publishers: Penguin Random House India - Gurugram/Delhi, HarperCollins India - Noida/Delhi, Juggernaut Books - Delhi NCR, Westland Books (Amazon) - Chennai, Hachette India - Gurugram, Speaking Tiger - Delhi NCR, Rupa Publications - Delhi NCR, Bloomsbury India - Delhi NCR, Oxford University Press India - Delhi NCR', 'Digital Content: WittyFeed - Indore, ScoopWhoop - Delhi NCR/Delhi, Storypick - Delhi NCR, BuzzFeed India (operational) - Mumbai, The Better India - Bengaluru', 'Journalism (as above)'],
        'indian_hubs': ['Delhi NCR (Publishing hub)', 'Mumbai', 'Bengaluru', 'Chennai', 'Kolkata', 'Pune']
    },

    # ==================== 13. LAW CAREERS ====================
    'Lawyer': {
        'description': 'Lawyers represent clients in court, provide legal advice, draft legal documents, and handle litigation or corporate legal matters in India.',
        'skills': ['Legal Research (Manupatra, SCC Online)', 'Drafting (Pleadings, Contracts)', 'Client Counseling', 'Courtroom Advocacy', 'Negotiation', 'Analytical Skills', 'Legal Writing', 'Bar Council Rules Knowledge'],
        'salary_range': '₹3,00,000 - ₹50,00,000+ per year (Entry (Litigation): ₹2-5 LPA, Corporate (Entry): ₹6-12 LPA, Mid: ₹15-25 LPA, Senior Associate: ₹25-40 LPA, Partner: ₹50 LPA - 2 Cr+)',
        'education': 'LLB (3 years after graduation) or Integrated BA-LLB/BBA-LLB (5 years) + Bar Council enrollment (AIBE)',
        'growth': '10-12% growth, corporate legal services expanding, litigation backlog creating demand, arbitration (commercial courts), cyber law, IP law emerging fields',
        'top_companies': ['Corporate Law Firms: AZB & Partners - Mumbai/Delhi/Bengaluru/Pune, Khaitan & Co - Mumbai/Delhi/Bengaluru/Kolkata, Shardul Amarchand Mangaldas - Delhi/Mumbai/Bengaluru/Kolkata, Cyril Amarchand Mangaldas - Mumbai/Delhi/Bengaluru/Chennai, Trilegal - Mumbai/Delhi/Bengaluru/Hyderabad, J. Sagar Associates - Mumbai/Delhi/Bengaluru/Chennai/Hyderabad', 'Corporate Legal Departments: Tata Sons - Mumbai, Reliance Industries - Mumbai, Infosys - Bengaluru, Wipro - Bengaluru, HDFC Bank - Mumbai, ICICI Bank - Mumbai', 'Government: Public Prosecutor, Legal Advisor to Government'],
        'indian_hubs': ['Delhi NCR (Supreme Court, High Court)', 'Mumbai (Bombay High Court)', 'Bengaluru (Karnataka High Court)', 'Chennai (Madras High Court)', 'Kolkata (Calcutta High Court)', 'Hyderabad (Telangana High Court)']
    },
    'Corporate Lawyer': {
        'description': 'Corporate lawyers handle mergers & acquisitions, contracts, corporate governance, compliance, and securities law for Indian companies.',
        'skills': ['M&A and Private Equity', 'Corporate Governance', 'SEBI Regulations', 'Contract Drafting & Negotiation', 'Due Diligence', 'Company Law (Companies Act)', 'Regulatory Compliance', 'Securities Law (IPO, FPO)', 'Merger Control (Competition Law)'],
        'salary_range': '₹8,00,000 - ₹60,00,000+ per year (Entry: ₹8-15 LPA, Mid Associate: ₹16-25 LPA, Senior Associate: ₹26-40 LPA, Partner: ₹50 LPA - 2 Cr+)',
        'education': 'LLB + Company Secretary (CS) preferred; LLM in Corporate Law/Business Law valued',
        'growth': '12-14% growth, Indian M&A activity high, startups raising funds, IPO boom, corporate compliance essential (SEBI LODR)',
        'top_companies': ['Top Law Firms (Corporate Depts): AZB & Partners - Mumbai/Delhi/Bengaluru, Khaitan & Co - Mumbai/Delhi/Bengaluru, Shardul Amarchand Mangaldas - Delhi/Mumbai/Bengaluru, Cyril Amarchand Mangaldas - Mumbai/Delhi/Bengaluru, Trilegal - Mumbai/Delhi/Bengaluru, JSA - Mumbai/Delhi/Bengaluru', 'In-house Legal: Tata Group - Mumbai, Reliance - Mumbai, Adani Group - Ahmedabad/Mumbai, Amazon India Legal - Bengaluru, Google India Legal - Gurugram, Microsoft India Legal - Hyderabad, Flipkart Legal - Bengaluru'],
        'indian_hubs': ['Mumbai (Corporate legal capital)', 'Delhi NCR', 'Bengaluru (Startup legal hub)', 'Hyderabad', 'Chennai', 'Ahmedabad']
    },

    # ==================== 14. COMMERCE CAREERS ====================
    'Chartered Accountant (CA) - Already added above, keeping reference':
    'Company Secretary (CS) - Already added above, keeping reference',
    'Cost Accountant (CMA)': {
        'description': 'Cost Accountants (CMAs) manage cost analysis, cost control, budgeting, and performance evaluation for Indian manufacturing and service companies.',
        'skills': ['Cost Accounting Standards', 'Cost Management', 'Budgeting & Forecasting', 'Variance Analysis', 'Inventory Valuation', 'Activity-Based Costing (ABC)', 'Transfer Pricing', 'Cost Auditing', 'ERP Systems (SAP, Oracle)'],
        'salary_range': '₹5,00,000 - ₹25,00,000 per year (Entry: ₹5-8 LPA, CMA: ₹8-12 LPA, Senior: ₹13-18 LPA, Finance Controller: ₹20-30 LPA)',
        'education': 'CMA (ICMAI) - Certified Management Accountant (Institute of Cost Accountants of India), requires clearing 3 levels + practical training',
        'growth': '9-11% growth, cost audit mandatory for specified Indian companies (as per Companies Act), manufacturing sector demand, costing expertise valuable in CFO offices',
        'top_companies': ['Manufacturing: Tata Motors - Pune/Mumbai, Mahindra & Mahindra - Mumbai/Pune, Maruti Suzuki - Delhi NCR, Reliance Industries - Mumbai, Adani Group - Ahmedabad/Mumbai', 'Audit Firms: Deloitte India - Mumbai/Delhi/Bengaluru, PwC India - Kolkata/Mumbai/Delhi, KPMG India - Mumbai/Delhi/Bengaluru, EY India - Mumbai/Delhi/Bengaluru, BDO India - Mumbai/Delhi/Bengaluru', 'Corporate: HDFC Bank - Mumbai, ICICI Bank - Mumbai, ITC Limited - Kolkata, Hindustan Unilever - Mumbai'],
        'indian_hubs': ['Mumbai', 'Delhi NCR', 'Kolkata', 'Chennai', 'Bengaluru', 'Hyderabad', 'Pune', 'Ahmedabad']
    },

    # ==================== 15. COMPUTER SCIENCE CAREERS ====================
    'Software Developer': {
        'description': 'Software developers design, code, test, and maintain software applications for Indian IT companies, product firms, and startups.',
        'skills': ['Programming (Java, Python, C++, JavaScript)', 'Data Structures & Algorithms', 'Problem Solving', 'Databases (SQL, MongoDB)', 'Version Control (Git)', 'Agile Methodologies', 'Testing & Debugging', 'API Integration'],
        'salary_range': '₹4,00,000 - ₹35,00,000 per year (Entry: ₹4-8 LPA, Software Dev: ₹8-15 LPA, Senior: ₹16-25 LPA, Lead: ₹26-35 LPA, Architect: ₹35-50 LPA)',
        'education': "B.Tech/BE in CS/IT, BCA, MCA; B.Sc CS; Bootcamp graduates hired with strong portfolios",
        'growth': '18-20% growth, IT services and product companies hiring, Indian startups unicorns demand developers, remote work opportunities',
        'top_companies': ['IT Services: Infosys - Bengaluru/Mysore/Pune, TCS - Mumbai/Chennai/Bengaluru, Wipro - Bengaluru/Hyderabad, HCL - Noida/Chennai, Tech Mahindra - Pune/Bengaluru, LTIMindtree - Bengaluru/Pune, Mphasis - Bengaluru/Pune, Persistent Systems - Pune/Nagpur', 'Product: Flipkart - Bengaluru, Amazon India - Bengaluru/Hyderabad, Microsoft India - Hyderabad/Bengaluru, Google India - Bengaluru/Hyderabad, Oracle India - Bengaluru/Hyderabad, Salesforce India - Hyderabad/Bengaluru, Adobe India - Bengaluru/Noida, Freshworks - Chennai/Bengaluru', 'Startups: Razorpay - Bengaluru, CRED - Bengaluru, Groww - Bengaluru, Unacademy - Bengaluru, BYJU\'s - Bengaluru, Swiggy - Bengaluru, Zomato - Gurugram, Ola - Bengaluru, Meesho - Bengaluru, Nykaa - Mumbai'],
        'indian_hubs': ['Bengaluru', 'Hyderabad', 'Pune', 'Chennai', 'Mumbai', 'Delhi NCR (Gurugram, Noida)', 'Kolkata', 'Ahmedabad', 'Kochi', 'Indore']
    },
    'Web Developer': {
        'description': 'Web developers build and maintain websites and web applications for Indian companies, agencies, and startups using frontend and backend technologies.',
        'skills': ['HTML5/CSS3', 'JavaScript (React, Angular, Vue.js)', 'Backend (Node.js, Python Django, PHP Laravel, Java Spring)', 'Database (MySQL, PostgreSQL, MongoDB)', 'REST APIs', 'Git/GitHub', 'Responsive Design', 'Web Security Basics', 'Deployment (Netlify, Vercel, AWS)'],
        'salary_range': '₹3,50,000 - ₹25,00,000 per year (Entry: ₹3.5-6 LPA, Web Dev: ₹6-12 LPA, Senior: ₹13-18 LPA, Lead: ₹20-25 LPA)',
        'education': "B.Tech/BE/BCA, Bootcamp graduates, self-taught with portfolio; Certifications in MERN/MEAN stack valued",
        'growth': '18-20% growth, digital transformation of Indian businesses, e-commerce growth, every company needs web presence, freelance opportunities abundant',
        'top_companies': ['Tech: Flipkart - Bengaluru, Amazon India - Bengaluru/Hyderabad, Paytm - Noida, Razorpay - Bengaluru, CRED - Bengaluru, Groww - Bengaluru, Unacademy - Bengaluru, BYJU\'s - Bengaluru, Swiggy - Bengaluru, Zomato - Gurugram, Ola - Bengaluru, Nykaa - Mumbai, Meesho - Bengaluru', 'IT Services: Infosys, TCS, Wipro, HCL, Tech Mahindra - All major IT hubs', 'Agencies: Digital agencies in Mumbai/Bengaluru/Delhi (Webenza, FoxyMoron, Schbang, WATConsult, BC Web Wise)'],
        'indian_hubs': ['Bengaluru', 'Hyderabad', 'Pune', 'Mumbai', 'Delhi NCR (Gurugram, Noida)', 'Chennai', 'Kolkata', 'Jaipur', 'Indore']
    },
    'Mobile App Developer': {
        'description': 'Mobile app developers create native or cross-platform applications for Android and iOS devices for Indian startups, product companies, and enterprises.',
        'skills': ['Android (Kotlin/Java)', 'iOS (Swift/SwiftUI)', 'Cross-platform (React Native, Flutter)', 'REST APIs Integration', 'Firebase', 'Git', 'Mobile UI/UX Principles', 'App Store Publishing (Play Store/App Store)', 'Mobile Security'],
        'salary_range': '₹4,00,000 - ₹30,00,000 per year (Entry: ₹4-8 LPA, App Dev: ₹8-15 LPA, Senior: ₹16-22 LPA, Lead: ₹24-30 LPA)',
        'education': "B.Tech/BE/BCA; Bootcamp graduates; Portfolios with published apps essential",
        'growth': '20-22% growth, India has 700M+ smartphone users, mobile-first economy, fintech, edtech, e-commerce apps dominate',
        'top_companies': ['Product Companies: Flipkart - Bengaluru, Amazon India - Bengaluru/Hyderabad, Paytm - Noida, PhonePe - Bengaluru, Google India - Bengaluru/Hyderabad, CRED - Bengaluru, Groww - Bengaluru, Razorpay - Bengaluru, Ola - Bengaluru, Uber India - Bengaluru/Hyderabad, Zomato - Gurugram, Swiggy - Bengaluru, Unacademy - Bengaluru, BYJU\'s - Bengaluru, Dream11 - Mumbai, Myntra - Bengaluru, Nykaa - Mumbai', 'Startups: BharatPe - Delhi NCR, Jupiter - Bengaluru, Fampay - Bengaluru, Khatabook - Bengaluru, MPL - Bengaluru', 'IT Services: Infosys, TCS, Wipro, HCL, Tech Mahindra mobile dev teams'],
        'indian_hubs': ['Bengaluru', 'Hyderabad', 'Mumbai', 'Pune', 'Delhi NCR (Gurugram, Noida)', 'Chennai', 'Jaipur (Rajasthan startup hub)']
    },

    # ==================== 16. ECONOMICS CAREERS ====================
    'Economist': {
        'description': 'Economists analyze economic data, forecast trends, and advise businesses, banks, and government on economic policies in India.',
        'skills': ['Econometrics (Stata, EViews, R)', 'Macro/Micro Economics', 'Forecasting', 'Data Analysis', 'Policy Analysis', 'Report Writing', 'Economic Modeling', 'Indian Economy Knowledge (Union Budget, RBI policies, GDP analysis)'],
        'salary_range': '₹6,00,000 - ₹35,00,000 per year (Entry: ₹6-10 LPA, Economist: ₹10-18 LPA, Senior: ₹20-28 LPA, Chief Economist: ₹35-50 LPA)',
        'education': 'BA/MA Economics, M.Sc Economics (ISI, DSE), PhD Economics for senior roles; UGC-NET essential for academia',
        'growth': '10-12% growth, RBI and government economists in demand, corporate economists (banks, rating agencies), consulting firms',
        'top_companies': ['Government: Reserve Bank of India (RBI) - Mumbai, NITI Aayog - Delhi, Ministry of Finance - Delhi, Ministry of Commerce - Delhi, Indian Statistical Institute (ISI) - Kolkata/Delhi/Bengaluru/Chennai, RBI Monetary Policy Committee - Mumbai', 'Banks: SBI - Mumbai, HDFC Bank - Mumbai, ICICI Bank - Mumbai, Axis Bank - Mumbai, Kotak Mahindra Bank - Mumbai', 'Rating Agencies: CRISIL - Mumbai, ICRA - Gurugram, India Ratings - Mumbai, CARE Ratings - Mumbai', 'Consulting: McKinsey Global Institute - Mumbai/Delhi, Deloitte Economics - Mumbai/Delhi, PwC Economics - Kolkata/Mumbai/Delhi, KPMG Economics - Mumbai/Delhi/Bengaluru, EY Economics - Mumbai/Delhi/Bengaluru', 'Research: IDFC Institute - Mumbai, Centre for Monitoring Indian Economy (CMIE) - Mumbai, National Council of Applied Economic Research (NCAER) - Delhi'],
        'indian_hubs': ['Mumbai (RBI)', 'Delhi NCR (Government, NITI Aayog)', 'Bengaluru', 'Kolkata (ISI)', 'Chennai', 'Hyderabad', 'Pune']
    },
    'Policy Analyst (Economics)': {
        'description': 'Policy analysts research and evaluate public policies, providing recommendations to government, think tanks, and international organizations in India.',
        'skills': ['Policy Analysis', 'Economic Research', 'Data Analysis (Stata, R)', 'Stakeholder Engagement', 'Report Writing', 'Program Evaluation', 'Cost-Benefit Analysis', 'Indian Governance Knowledge'],
        'salary_range': '₹5,00,000 - ₹20,00,000 per year (Entry: ₹5-8 LPA, Analyst: ₹8-12 LPA, Senior: ₹13-18 LPA, Policy Advisor: ₹18-25 LPA)',
        'education': 'MA/M.Sc Economics + M.Phil/PhD preferred, MPA (Master of Public Administration), UGC-NET for research roles',
        'growth': '10-12% growth, think tanks expanding, NITI Aayog hiring, state governments needing policy analysts, CSR funds for research',
        'top_companies': ['Think Tanks: Centre for Policy Research (CPR) - Delhi, Indian Council for Research on International Economic Relations (ICRIER) - Delhi, National Institute of Public Finance and Policy (NIPFP) - Delhi, Centre for Social and Economic Progress (CSEP) - Delhi, Brookings India (now CSEP) - Delhi, ORF (Observer Research Foundation) - Mumbai/Delhi/Kolkata, IDFC Institute - Mumbai', 'Government: NITI Aayog - Delhi, Ministry of Finance - Delhi, RBI - Mumbai, State Planning Boards - All State Capitals', 'International Organizations: World Bank India - Delhi, IMF India - Delhi, ADB India - Delhi, UNDP India - Delhi, UNICEF India - Delhi, UNESCO India - Delhi'],
        'indian_hubs': ['Delhi NCR (Policy hub)', 'Mumbai', 'Bengaluru', 'Chennai', 'Kolkata']
    },

    # ==================== 17. PSYCHOLOGY CAREERS ====================
    'Clinical Psychologist': {
        'description': 'Clinical psychologists assess, diagnose, and treat mental health disorders using therapy techniques in Indian hospitals, clinics, and private practice.',
        'skills': ['Psychodiagnostic Assessment (WAIS, Rorschach, NIMHANS tests)', 'Psychotherapy (CBT, REBT, DBT, ACT)', 'Clinical Interviewing', 'Case Formulation', 'Treatment Planning', 'Report Writing', 'Crisis Intervention', 'Ethical Practice (RCI guidelines)'],
        'salary_range': '₹3,50,000 - ₹18,00,000 per year (Entry (RCI intern): ₹2-4 LPA, Clinical Psychologist: ₹4-8 LPA, Senior: ₹9-12 LPA, Consultant: ₹12-18 LPA, Private Practice: ₹15-30 LPA)',
        'education': 'M.Phil Clinical Psychology (RCI approved - 2 years + internship) mandatory for license; PhD for senior/academic roles',
        'growth': '18-20% growth, mental health awareness increasing (post-COVID), government initiatives (NMHP), RCI mandating professionals, private clinics and online therapy platforms (YourDOST, HeartItOut, Mpower, 1to1Help, BetterLYF)',
        'top_companies': ['NIMHANS - Bengaluru', 'AIIMS - New Delhi/Bhopal/Bhubaneswar/Jodhpur', 'IHBAS - Delhi', 'PGIMER - Chandigarh', 'CIP - Ranchi', 'Institute of Psychiatry (Kolkata) - Kolkata', 'Fortis Mental Health - Delhi NCR/Bengaluru/Mumbai', 'Apollo Hospitals Psychology Dept - Chennai/Delhi/Hyderabad', 'Mpower - Mumbai/Bengaluru/Delhi', 'YourDOST - Bengaluru/Mumbai', 'HeartItOut - Delhi NCR', '1to1Help - Mumbai', 'BetterLYF - Delhi NCR', 'The Mind Clinic (Dr. Samir Parikh) - Delhi', 'Manastha - Mumbai'],
        'indian_hubs': ['Bengaluru (NIMHANS)', 'Delhi NCR', 'Mumbai', 'Chennai', 'Kolkata', 'Hyderabad', 'Pune', 'Chandigarh']
    },
    'Counseling Psychologist': {
        'description': 'Counseling psychologists help individuals cope with life challenges, stress, relationships, and career issues through therapy in Indian schools, colleges, corporate organizations, and private practice.',
        'skills': ['Counseling Techniques (Person-centered, Gestalt)', 'Active Listening', 'Empathy', 'Crisis Counseling', 'Career Counseling', 'Stress Management', 'Group Therapy', 'Ethical Practice'],
        'salary_range': '₹3,00,000 - ₹12,00,000 per year (Entry: ₹3-5 LPA, Counselor: ₹5-8 LPA, Senior: ₹8-10 LPA, Head Counselor: ₹10-14 LPA, Private Practice: ₹10-20 LPA)',
        'education': 'MA/M.Sc Counseling Psychology/Master of Counseling Psychology; Diploma in Counseling; UGC-NET for academia; RCI registration not mandatory (unlike Clinical Psychology) but recommended',
        'growth': '18-20% growth (similar to clinical), school counselors mandatory as per RTE Act (2009) being enforced, corporate employee wellness programs (EAPs), college counseling centers',
        'top_companies': ['Schools (mandatory requirement): Delhi Public Schools (DPS) across India, The Shri Ram Schools (Delhi NCR), Vasant Valley (Delhi), Cathedral School (Mumbai), Bishop Cotton (Bengaluru), St. Xavier\'s Collegiate (Kolkata), Billabong High - All India', 'Universities & Colleges: University of Delhi colleges (Miranda House, St. Stephens, Hindu, etc.), JNU (Delhi), TISS (Mumbai), Christ University (Bengaluru), St. Xavier\'s College (Mumbai) - all have counseling centers', 'Corporate EAPs: ICICI Bank EAP, HDFC Bank EAP, Infosys Employee Wellness, Wipro Wellness, Tata Group EAPs, Unilever EAP', 'Online Platforms: YourDOST - Bengaluru, HeartItOut - Delhi NCR, BetterLYF - Delhi NCR, 1to1Help - Mumbai, Manastha - Mumbai, Therapize - Bengaluru', 'NGOs: Vandrevala Foundation - Mumbai, iCall (TISS) - Mumbai, Sneha - Chennai, Samaritans - Mumbai, AASRA - Mumbai'],
        'indian_hubs': ['Delhi NCR (schools & colleges)', 'Mumbai', 'Bengaluru', 'Chennai', 'Kolkata', 'Hyderabad', 'Pune', 'Chandigarh']
    },

    # ==================== 18. SOCIAL WORK CAREERS ====================
    'Social Worker': {
        'description': 'Social workers help individuals, families, and communities cope with challenges, access resources, and improve wellbeing in Indian NGOs, hospitals, and government agencies.',
        'skills': ['Case Management', 'Counseling (basic)', 'Crisis Intervention', 'Community Mobilization', 'Advocacy', 'Referral Networking', 'Documentation & Reporting', 'Empathy & Active Listening', 'Fieldwork Skills', 'Government Scheme Knowledge (PMJJBY, PMSBY, PMMVY, etc.)'],
        'salary_range': '₹2,50,000 - ₹8,00,000 per year (Entry: ₹2.5-4 LPA, Social Worker: ₹4-6 LPA, Senior: ₹6-8 LPA, Program Manager: ₹8-12 LPA)',
        'education': 'BSW (Bachelor of Social Work) for entry, MSW (Master of Social Work) for senior roles and RCI licensing (for medical social work)',
        'growth': '12-14% growth, CSR funding for NGOs (Companies Act 2013 mandates 2% profit for CSR), government social welfare schemes expansion, child protection (ICPS), mental health, elderly care',
        'top_companies': ['NGOs (India-wide): CRY (Child Rights and You) - Bengaluru/Mumbai/Delhi/Kolkata/Chennai, Save the Children India - Delhi/Mumbai/Bengaluru/Hyderabad/Kolkata, Goonj - Delhi NCR/Bengaluru/Mumbai, Pratham - Mumbai/Delhi/Bengaluru, HelpAge India - Delhi/Mumbai/Bengaluru/Chennai/Kolkata, Smile Foundation - Delhi NCR/Mumbai/Bengaluru/Chennai, Akshaya Patra Foundation - Bengaluru/Delhi/Jaipur, Magic Bus - Mumbai/Delhi, Room to Read India - Delhi/Mumbai/Bengaluru', 'Government: Integrated Child Protection Scheme (ICPS) - District Child Protection Units across India, District Legal Services Authorities (DLSA) - All Districts, Women & Child Development Departments - State Capitals, Childline (1098) - Across major cities', 'Hospitals: Medical Social Workers in Apollo, Fortis, AIIMS, Government Hospitals - All major cities'],
        'indian_hubs': ['Delhi NCR (NGO capital)', 'Mumbai', 'Bengaluru', 'Chennai', 'Kolkata', 'Hyderabad', 'Pune', 'Ahmedabad', 'Jaipur', 'Lucknow', 'Bhubaneswar', 'Patna']
    },
    'Community Organizer': {
        'description': 'Community organizers mobilize communities, facilitate participatory development, and lead social change initiatives in Indian urban slums and rural areas.',
        'skills': ['Community Mobilization', 'Participatory Rural Appraisal (PRA)', 'Capacity Building', 'Advocacy & Campaigning', 'Stakeholder Mapping', 'Facilitation Skills', 'Documentation', 'Vernacular Language Proficiency (local languages)', 'Conflict Resolution'],
        'salary_range': '₹3,00,000 - ₹9,00,000 per year (Entry: ₹3-5 LPA, Community Organizer: ₹5-7 LPA, Senior: ₹7-9 LPA, Community Manager: ₹10-12 LPA)',
        'education': 'MSW (Master of Social Work) with community development specialization, BSW + experience, MA in Development Studies, Rural Management (IRMA, XIMB)',
        'growth': '11-13% growth, large number of grassroots NGOs, government community-based programs (NRLM, DAY-NULM, MGNREGA), CSR community engagement',
        'top_companies': ['Grassroots NGOs: SEWA (Self Employed Women\'s Association) - Ahmedabad/Delhi/Mumbai, MHT (Mahila Housing Trust) - Ahmedabad/Delhi/Bengaluru/Mumbai, PRADAN - Across rural India (Delhi/Guwahati/Ranchi/Bhopal), BAIF - Pune (Maharashtra/Gujarat/Karnataka/UP/MP), DHAN Foundation - Madurai (Tamil Nadu), MYRADA - Bengaluru (Karnataka), Seva Mandir - Udaipur (Rajasthan), Vikas Samvad - Ranchi (Jharkhand), Chetna Vikas - Visakhapatnam (Andhra Pradesh)', 'Government Schemes: National Rural Livelihood Mission (NRLM) - Community Resource Persons across all states, DAY-NULM (urban) - City Mission Management Units', 'International NGOs: Oxfam India - Delhi, ActionAid India - Bengaluru/Delhi/Bhopal/Patna, CARE India - Delhi/Hyderabad/Patna'],
        'indian_hubs': ['Ahmedabad (SEWA)', 'Delhi NCR', 'Bengaluru', 'Mumbai', 'Chennai', 'Pune', 'Kolkata', 'Jaipur', 'Bhopal', 'Ranchi', 'Guwahati', 'Bhubaneswar', 'Patna', 'Lucknow']
    },
        # ==================== TRANSPORTATION & MOBILITY CAREERS ====================
    'Logistics Manager': {
        'description': 'Logistics managers oversee supply chain and transportation operations, coordinating the movement of goods from suppliers to customers efficiently and cost-effectively in Indian companies.',
        'skills': ['Supply Chain Management', 'Transportation Planning', 'Inventory Management', 'Warehouse Operations', 'Vendor Negotiation', 'Cost Optimization', 'Data Analysis (Excel, Tableau)', 'Team Leadership', 'Regulatory Compliance (GST, Customs)', 'TMS Software (SAP TM, Oracle Transportation)'],
        'salary_range': '₹5,00,000 - ₹25,00,000 per year (Entry: ₹4-6 LPA, Logistics Coordinator: ₹5-8 LPA, Logistics Manager: ₹8-15 LPA, Senior Manager: ₹16-22 LPA, Supply Chain Director: ₹25-40 LPA)',
        'education': 'BBA/MBA in Logistics & Supply Chain Management, B.Tech Industrial Engineering, Diploma in Logistics; Certification: CLTD, CSCP valued',
        'growth': '15% growth (Much faster than average), E-commerce boom, National Logistics Policy 2022, government infrastructure spending',
        'top_companies': ['Delhivery - Gurugram/Bengaluru', 'Blue Dart - Mumbai', 'DTDC - Bengaluru', 'Ecom Express - Gurugram', 'Xpressbees - Pune', 'Shadowfax - Bengaluru', 'Amazon Logistics - Bengaluru/Hyderabad', 'Flipkart Ekart - Bengaluru', 'Rivigo - Gurugram', 'Mahindra Logistics - Mumbai', 'TCI - Gurugram', 'Gati - Hyderabad', 'Allcargo Logistics - Mumbai'],
        'indian_hubs': ['Mumbai', 'Delhi NCR', 'Bengaluru', 'Chennai', 'Hyderabad', 'Pune', 'Ahmedabad', 'Kolkata', 'Gurugram']
    },
    'Supply Chain Analyst': {
        'description': 'Supply chain analysts optimize supply chain efficiency by analyzing data, forecasting demand, managing inventory levels, and improving logistics processes for Indian companies.',
        'skills': ['Data Analysis (SQL, Python, R)', 'Demand Forecasting', 'Inventory Optimization', 'Statistical Modeling', 'Excel (Advanced, Power Query, Macros)', 'Tableau/PowerBI Visualization', 'Supply Chain KPIs (OTIF, Inventory Turns)', 'ERP Systems (SAP, Oracle, NetSuite)', 'Problem Solving'],
        'salary_range': '₹4,00,000 - ₹20,00,000 per year (Entry: ₹4-7 LPA, Analyst: ₹7-12 LPA, Senior Analyst: ₹12-17 LPA, Supply Chain Manager: ₹18-25 LPA)',
        'education': 'B.Tech Industrial/Production, BBA, MBA Supply Chain; Certification: CSCP, CPIM, Six Sigma Green Belt',
        'growth': '18% growth, Data-driven supply chains, AI/ML in logistics, real-time tracking, predictive analytics demand',
        'top_companies': ['Amazon India - Bengaluru/Hyderabad', 'Flipkart - Bengaluru', 'Delhivery - Gurugram', 'Rivigo - Gurugram', 'Mahindra Logistics - Mumbai', 'TCS Supply Chain Consulting - Mumbai/Chennai', 'Infosys Supply Chain - Bengaluru', 'Wipro Supply Chain - Bengaluru', 'Accenture Supply Chain - Bengaluru/Mumbai', 'Deloitte Supply Chain - Mumbai/Delhi/Bengaluru'],
        'indian_hubs': ['Bengaluru', 'Mumbai', 'Delhi NCR', 'Hyderabad', 'Pune', 'Chennai', 'Gurugram']
    },
    'Transportation Planner': {
        'description': 'Transportation planners design urban transport systems, conduct traffic studies, plan public transit routes, and develop sustainable mobility solutions for Indian cities.',
        'skills': ['Urban Planning', 'Traffic Engineering', 'GIS Software (ArcGIS, QGIS)', 'Transport Modeling (VISUM, VISSIM, Cube)', 'Statistical Analysis', 'Public Transit Planning', 'Sustainable Transport (BRT, Metro, NMT)', 'Project Management', 'Stakeholder Engagement', 'Report Writing'],
        'salary_range': '₹4,00,000 - ₹18,00,000 per year (Entry: ₹4-7 LPA, Planner: ₹7-12 LPA, Senior Planner: ₹12-16 LPA, Transport Planning Manager: ₹16-22 LPA)',
        'education': 'B.Plan/B.Tech Transportation Engineering, M.Plan (Transport Planning), M.Tech Transportation Engineering; UGC-NET/JRF for government roles',
        'growth': '12% growth, Smart Cities Mission (100 cities), Metro expansion (20+ cities), BRTS corridors, NMT (Non-Motorized Transport) focus',
        'top_companies': ['DMRC - Delhi', 'Mumbai Metro - Mumbai', 'BMRCL - Bengaluru', 'Chennai Metro - Chennai', 'Kolkata Metro - Kolkata', 'Hyderabad Metro - Hyderabad', 'Lucknow Metro - Lucknow', 'Ahmedabad Metro - Ahmedabad', 'Pune Metro - Pune', 'Kochi Metro - Kochi', 'NHAI - Delhi', 'State Transport Departments - All State Capitals', 'Consulting Firms: AECOM India - Gurugram/Bengaluru/Mumbai, Atkins India - Bengaluru/Mumbai/Delhi, SYSTRA India - Delhi/Mumbai/Bengaluru, Lea Associates - Delhi/Mumbai, RITES - Gurugram'],
        'indian_hubs': ['Delhi NCR', 'Mumbai', 'Bengaluru', 'Chennai', 'Hyderabad', 'Ahmedabad', 'Pune', 'Kolkata', 'Lucknow', 'Kochi']
    },
    'Fleet Manager': {
        'description': 'Fleet managers oversee vehicle fleets, manage maintenance schedules, optimize routes, control costs, and ensure compliance with regulations for Indian logistics and mobility companies.',
        'skills': ['Fleet Maintenance Management', 'Route Optimization', 'Telematics & GPS Tracking', 'Cost Control (Fuel, Maintenance, Tires)', 'Vendor Management (Workshops, Vendors)', 'Driver Management & Safety', 'Compliance (Motor Vehicles Act, Pollution norms)', 'Data Analysis (Fleet KPIs)', 'Fleet Management Software (Fleetroot, TrackoBit, LocoNav)'],
        'salary_range': '₹4,00,000 - ₹18,00,000 per year (Entry: ₹4-7 LPA, Fleet Supervisor: ₹6-9 LPA, Fleet Manager: ₹9-14 LPA, Senior Fleet Manager: ₹14-18 LPA)',
        'education': 'Diploma/B.Tech Mechanical/Automobile Engineering, BBA Logistics, MBA; Certification: Fleet Management Certification (NAFT, SAE)',
        'growth': '14% growth, EV fleet adoption, telematics penetration, GPS mandatory for commercial vehicles, last-mile delivery explosion',
        'top_companies': ['Amazon Logistics - Bengaluru/Hyderabad', 'Flipkart Ekart - Bengaluru', 'Delhivery - Gurugram', 'BigBasket - Bengaluru', 'Zepto - Mumbai', 'Blinkit - Gurugram', 'Swiggy Instamart - Bengaluru', 'Ola Fleet - Bengaluru', 'Uber Fleet - Bengaluru/Hyderabad', 'Rapido - Bengaluru', 'BlackBuck - Bengaluru', 'Rivigo - Gurugram', 'LetsTransport - Bengaluru', 'TCI - Gurugram', 'Blue Dart - Mumbai'],
        'indian_hubs': ['Bengaluru', 'Delhi NCR', 'Mumbai', 'Hyderabad', 'Pune', 'Chennai', 'Ahmedabad', 'Kolkata', 'Gurugram']
    },
    'Warehouse Manager': {
        'description': 'Warehouse managers oversee storage facilities, manage inventory, coordinate inbound/outbound operations, and optimize warehouse efficiency for Indian logistics and e-commerce companies.',
        'skills': ['Warehouse Management Systems (WMS)', 'Inventory Control (FIFO, FEFO, Cycle Counts)', 'Slotting & Layout Optimization', 'Labor Management & Training', 'Safety & Compliance (OSHA, Factory Act)', 'Automation (Conveyors, Sorters, AGVs, ASRS)', 'Space Utilization', 'KPI Management (Order Accuracy, Pick Rates, On-time Dispatch)', 'Process Improvement (Lean, Six Sigma)'],
        'salary_range': '₹4,00,000 - ₹20,00,000 per year (Entry Warehouse Supervisor: ₹3-5 LPA, Warehouse Manager: ₹6-12 LPA, Senior Manager: ₹12-18 LPA, Distribution Center Head: ₹18-25 LPA)',
        'education': 'BBA/Diploma in Logistics, B.Tech Industrial Engineering, MBA Supply Chain; Certification: Lean Warehouse, Six Sigma, WMS Certification',
        'growth': '15% growth, E-commerce and 3PL warehousing expansion, automation adoption, dark stores for quick commerce, warehouse robotics',
        'top_companies': ['Amazon Fulfillment Centers - Across 15+ cities (Bengaluru, Hyderabad, Delhi, Mumbai, Chennai, Pune, Kolkata, Ahmedabad, Lucknow, Nagpur, Jaipur, Kochi, Coimbatore, Guwahati, Patna)', 'Flipkart Warehouses - Across India (Bengaluru, Delhi, Mumbai, Chennai, Hyderabad, Kolkata, Pune, Ahmedabad, Lucknow, Guwahati)', 'Delhivery Warehouses - Across 35+ cities', 'BigBasket Warehouses - Bengaluru, Delhi, Mumbai, Chennai, Hyderabad, Pune, Kolkata, Ahmedabad', 'Zepto Dark Stores - Mumbai, Bengaluru, Delhi, Chennai, Hyderabad, Pune, Kolkata', 'Blinkit Warehouses - Delhi NCR, Mumbai, Bengaluru, Chennai, Hyderabad, Pune', 'Swiggy Instamart Warehouses - Bengaluru, Delhi, Mumbai, Chennai, Hyderabad, Pune', 'Reliance Warehouses - Across India', 'DHL Warehouses - Across India', 'Blue Dart Warehouses - Across India'],
        'indian_hubs': ['Bengaluru', 'Delhi NCR', 'Mumbai', 'Hyderabad', 'Chennai', 'Pune', 'Ahmedabad', 'Kolkata', 'Lucknow', 'Nagpur', 'Jaipur', 'Indore', 'Guwahati', 'Patna']
    },
    'Electric Vehicle (EV) Engineer': {
        'description': 'EV engineers design, develop, and test electric vehicles, battery systems, motors, controllers, and charging infrastructure for India\'s rapidly growing EV industry.',
        'skills': ['EV Powertrain Design', 'Battery Technology (Li-ion, LFP, NMC)', 'BMS (Battery Management Systems)', 'Motor Control (BLDC, PMSM, Induction Motors)', 'Power Electronics (Inverters, Converters, Chargers)', 'Vehicle Dynamics', 'Thermal Management', 'CAN Bus Communication', 'ISO 26262 Functional Safety', 'EV Charging Standards (CCS, CHAdeMO, GB/T, Bharat EV)'],
        'salary_range': '₹5,00,000 - ₹25,00,000 per year (Entry: ₹5-8 LPA, EV Engineer: ₹8-15 LPA, Senior EV Engineer: ₹15-20 LPA, EV Lead/Manager: ₹20-30 LPA)',
        'education': 'B.Tech/M.Tech Electrical/Electronics/Mechanical Engineering with EV specialization; Certification: EV Technology from IITs/NITs, NPTEL EV courses',
        'growth': '40% growth (Explosive growth!), India\'s EV30@30 target (30% EV penetration by 2030), FAME II subsidies, state EV policies, charging infrastructure expansion',
        'top_companies': ['Tata Motors EV Division - Pune, Mumbai', 'Mahindra Electric - Bengaluru, Chennai', 'Ola Electric - Bengaluru, Chennai, Pune', 'Ather Energy - Bengaluru, Chennai', 'Bajaj Auto (Chetak EV) - Pune', 'TVS Motor (iQube Electric) - Chennai', 'Hero Electric - Delhi, Ludhiana', 'Simple Energy - Bengaluru', 'Ultraviolette Automotive - Bengaluru', 'Olectra Greentech - Hyderabad', 'PMI Electro Mobility - Delhi NCR', 'Switch Mobility (Ashok Leyland EV) - Chennai', 'Euler Motors - Delhi NCR', 'Altigreen - Bengaluru', 'Kinetic Green - Pune', 'Wardwizard Innovations (Joy e-bike) - Vadodara', 'Lithion Power - Bengaluru', 'Exicom - Delhi NCR/Hyderabad', 'ABB India EV Charging - Bengaluru', 'Delta Electronics India - Bengaluru'],
        'indian_hubs': ['Bengaluru (EV Capital)', 'Chennai (Auto Hub)', 'Pune (Auto Cluster)', 'Delhi NCR', 'Mumbai', 'Hyderabad', 'Ahmedabad', 'Coimbatore']
    },
    'Last-Mile Delivery Specialist': {
        'description': 'Last-Mile delivery specialists optimize final-stage delivery operations, managing hyperlocal logistics, route planning, and delivery partner networks for e-commerce, food delivery, and quick commerce in India.',
        'skills': ['Route Optimization Algorithms', 'Last-Mile Technology Platforms (Locus, FarEye, Routematic)', 'Delivery Partner Management', 'Time Slot Management', 'Reverse Logistics (Returns)', 'Customer Experience', 'Data Analytics (OTIF, DSR, NPS)', 'Real-time Tracking Systems', 'Cost Optimization (Per-delivery cost)', 'Hyperlocal Logistics'],
        'salary_range': '₹3,50,000 - ₹15,00,000 per year (Entry: ₹3.5-6 LPA, Specialist: ₹6-10 LPA, Senior/Manager: ₹10-15 LPA)',
        'education': 'Graduation (any stream), BBA Logistics, MBA preferred; Certification in Supply Chain/Logistics valued',
        'growth': '20% growth, Quick commerce (10-minute delivery) explosion, 500M+ e-commerce shipments annually, gig economy expansion, hyperlocal delivery demand',
        'top_companies': ['Zomato - Gurugram', 'Swiggy - Bengaluru', 'Zepto - Mumbai/Bengaluru/Delhi', 'Blinkit - Gurugram', 'BigBasket - Bengaluru', 'Amazon Flex - Across India', 'Flipkart Quick - Bengaluru', 'Dunzo - Bengaluru', 'Shadowfax - Bengaluru', 'Loadshare - Bengaluru', 'Pickrr - Delhi NCR', 'Shiprocket - Delhi NCR', 'XpressBees - Pune', 'Ecom Express - Gurugram', 'Delhivery Hyperlocal - Gurugram'],
        'indian_hubs': ['Bengaluru', 'Delhi NCR', 'Mumbai', 'Hyderabad', 'Pune', 'Chennai', 'Kolkata', 'Ahmedabad', 'Jaipur', 'Lucknow']
    },
    'Rail Transport Manager': {
        'description': 'Rail transport managers oversee railway operations, freight logistics, passenger services, and rail infrastructure projects for Indian Railways and metro systems.',
        'skills': ['Railway Operations Management', 'Freight & Passenger Planning', 'Train Scheduling', 'Safety Management (Rail Safety Standards)', 'Terminal Management (Goods Sheds, Yards, Stations)', 'Coaching Operations', 'Wagon/Coach Maintenance Planning', 'Signal & Telecommunication Basics', 'Project Management', 'Regulatory Compliance (Railways Act, Commissioner of Railway Safety)'],
        'salary_range': '₹6,00,000 - ₹35,00,000 per year (Entry (IRMS Officer): ₹8-12 LPA, Divisional Manager: ₹15-20 LPA, Railway Board positions: ₹20-35 LPA)',
        'education': 'B.Tech (Civil, Mechanical, Electrical, Electronics) + UPSC-IES/RRB exams for Indian Railways; MBA Transportation for metro/private',
        'growth': '8-10% growth, Indian Railways (world\'s 4th largest), High-speed rail (Mumbai-Ahmedabad bullet train), Dedicated Freight Corridors (Western & Eastern DFC), Metro expansion (25+ cities by 2030), Station redevelopment (Amrit Bharat Station Scheme)',
        'top_companies': ['Indian Railways - Across India (70+ Divisions, All State Capitals)', 'DFCCIL (Dedicated Freight Corridor) - Delhi, Allahabad, Mumbai, Ahmedabad', 'Rail Vikas Nigam Limited (RVNL) - Delhi, Across India', 'RITES Limited - Gurugram, Across India', 'IRCON International - Delhi, Across India', 'Delhi Metro Rail Corporation (DMRC) - Delhi', 'Mumbai Metro - Mumbai', 'Bengaluru Metro (BMRCL) - Bengaluru', 'Chennai Metro - Chennai', 'Kolkata Metro - Kolkata', 'Hyderabad Metro - Hyderabad', 'Lucknow Metro - Lucknow', 'Ahmedabad Metro - Ahmedabad', 'Pune Metro - Pune', 'Kochi Metro - Kochi', 'Nagpur Metro - Nagpur', 'Jaipur Metro - Jaipur', 'NCRTC (RRTS) - Delhi NCR'],
        'indian_hubs': ['Delhi NCR (Rail Bhawan, RCF Kapurthala, DLW Varanasi)', 'Mumbai (Western Railway HQ, Central Railway HQ)', 'Kolkata (Eastern Railway HQ)', 'Chennai (Southern Railway HQ)', 'Ahmedabad (Western Railway, DFCCIL)', 'Bengaluru (South Western Railway)', 'Hyderabad (South Central Railway)', 'Lucknow (North Eastern Railway, RDSO)', 'Chandigarh (Northern Railway)', 'Jaipur (North Western Railway)']
    },
    'Airport Operations Manager': {
        'description': 'Airport operations managers oversee airport ground operations, passenger services, security compliance, and airline coordination at Indian airports.',
        'skills': ['Airport Operations (Terminal Management, Apron Management)', 'Airside Safety & Security (BCAS Regulations)', 'Passenger Processing (Check-in, Boarding, Baggage)', 'Flight Scheduling & Slot Coordination', 'Emergency Response Planning', 'Stakeholder Management (Airlines, CISF, Customs, Immigration)', 'Resource Allocation (Gates, Buses, Aerobridges)', 'Customer Service Excellence', 'Liaison with DGCA & BCAS', 'Airport Collaborative Decision Making (ACDM)'],
        'salary_range': '₹4,00,000 - ₹25,00,000 per year (Entry: ₹4-7 LPA, Duty Manager: ₹7-12 LPA, Operations Manager: ₹12-18 LPA, Senior/General Manager: ₹18-25 LPA, COO: ₹30-50 LPA)',
        'education': 'BBA Aviation Management, MBA Aviation Management, Diploma in Airport Operations; Certification: IATA Airport Operations, DGCA Safety Courses',
        'growth': '12% growth, UDAN (Regional Connectivity Scheme), Tier-2/3 airport expansion, Privatization of airports (Adani, GMR, BIAL), Passenger traffic growth (500M+ passengers by 2030)',
        'top_companies': ['GMR Airports - Delhi (IGI), Hyderabad (RGIA), Goa (Mopa)', 'Adani Airports - Mumbai (CSIA), Ahmedabad, Lucknow, Mangaluru, Jaipur, Guwahati, Thiruvananthapuram', 'Bangalore International Airport Limited (BIAL) - Bengaluru (Kempegowda International Airport)', 'Chennai International Airport - Chennai', 'Kolkata Airport - Kolkata', 'Cochin International Airport Limited (CIAL) - Kochi', 'Airports Authority of India (AAI) - All operational airports across India (100+ airports)', 'Mumbai International Airport Limited (MIAL) - Mumbai (operated by Adani now)', 'Noida International Airport (Jewar) - Greater Noida (under construction)', 'Navi Mumbai International Airport - Navi Mumbai (under construction)', 'Airlines: IndiGo (Aviation Ops) - Gurugram, Mumbai, Delhi, Bengaluru, Hyderabad, Chennai', 'Air India (Airside Ops) - Delhi, Mumbai, Bengaluru', 'SpiceJet (Ground Ops) - Gurugram, Across India', 'Vistara (Airport Ops) - Gurugram, Delhi, Mumbai, Bengaluru'],
        'indian_hubs': ['Delhi NCR (IGI Airport)', 'Mumbai (CSIA Airport)', 'Bengaluru (KIA Airport)', 'Chennai (Meenambakkam Airport)', 'Hyderabad (RGIA Airport)', 'Kolkata (Dum Dum Airport)', 'Kochi (CIAL Airport)', 'Ahmedabad (SVPIA Airport)', 'Goa (Mopa & Dabolim)', 'Thiruvananthapuram', 'Guwahati', 'Jaipur', 'Lucknow', 'Chandigarh']
    },
    'Port/Harbor Manager': {
        'description': 'Port managers oversee port operations, cargo handling, vessel berthing, and marine logistics at Indian sea ports and harbors.',
        'skills': ['Port Operations (Berthing, Unberthing, Cargo Handling)', 'Marine Logistics & Shipping', 'Vessel Traffic Management', 'Customs Clearance & EXIM Documentation', 'Safety & Security (ISPS Code)', 'Equipment Management (Cranes, Reach Stackers, Forklifts)', 'Container Terminal Management', 'Stevedoring & Cargo Planning', 'Port Community Systems (PCS)', 'Maritime Regulations (Indian Ports Act, Major Port Trusts Act)'],
        'salary_range': '₹6,00,000 - ₹30,00,000 per year (Entry: ₹6-10 LPA, Port Operations Manager: ₹10-18 LPA, Senior Manager: ₹18-25 LPA, Port Director: ₹25-35 LPA)',
        'education': 'B.Sc Nautical Science, B.E Marine Engineering, MBA Shipping Logistics, PG Diploma in Port Management; Certification: Port Management from IITs/NITs, Maritime certifications',
        'growth': '10% growth, Sagarmala Programme (₹8 lakh crore), Major port modernization, Private participation in ports (Adani, JM Baxi), Container traffic growth, EXIM trade expansion',
        'top_companies': ['Adani Ports & SEZ - Mundra (Gujarat), Hazira, Dahej, Vizag, Kattupalli (Chennai), Gangavaram (Vizag), Krishnapatnam', 'Jawaharlal Nehru Port Trust (JNPT) - Navi Mumbai (largest container port)', 'Chennai Port Trust - Chennai', 'Kolkata Port Trust - Kolkata, Haldia', 'Deendayal Port Trust (Kandla) - Gandhidham, Gujarat', 'Paradip Port Trust - Paradip, Odisha', 'V.O. Chidambaranar Port Trust (Tuticorin) - Thoothukudi, Tamil Nadu', 'Mumbai Port Trust - Mumbai', 'Visakhapatnam Port Trust - Visakhapatnam', 'Mormugao Port Trust - Goa', 'New Mangalore Port Trust - Mangaluru', 'Kamarajar Port (Ennore) - Chennai', 'DP World India - Mumbai, Chennai, Mundra, Kochi, Vizag', 'APM Terminals - Mumbai, Chennai, Pipavav', 'CMA CGM Terminals - Mumbai, Mundra', 'Hindustan Ports (RIL) - Gujarat', 'Kerala Maritime Board - Kochi'],
        'indian_hubs': ['Mumbai (JNPT, Mumbai Port)', 'Chennai (Chennai Port, Ennore)', 'Gujarat (Mundra, Kandla, Hazira, Dahej, Pipavav)', 'Kolkata (Kolkata Port, Haldia)', 'Visakhapatnam (Vizag Port, Gangavaram)', 'Kochi (Cochin Port, Vallarpadam Container Terminal)', 'Paradip (Odisha)', 'Mangaluru (New Mangalore Port)', 'Goa (Mormugao Port)', 'Thoothukudi (Tuticorin Port)']
    },
    'Urban Mobility Planner': {
        'description': 'Urban mobility planners design sustainable transportation systems for cities, including public transit (metro, bus), non-motorized transport (walking, cycling), and emerging mobility solutions (EVs, shared mobility) for Indian smart cities.',
        'skills': ['Sustainable Transport Planning', 'Public Transit (Metro, BRT, Bus) Design', 'Non-Motorized Transport (NMT) Planning', 'Integrated Mobility Solutions', 'Mobility as a Service (MaaS)', 'Traffic Demand Modeling (VISUM, VISSIM, Cube, EMME)', 'GIS Analysis (ArcGIS, QGIS)', 'Smart City Mobility Concepts (ITS, TMS)', 'Multi-modal Integration', 'Parking Policy & Management', 'Transport Policy Analysis', 'Stakeholder Consultation'],
        'salary_range': '₹5,00,000 - ₹22,00,000 per year (Entry: ₹5-8 LPA, Mobility Planner: ₹8-13 LPA, Senior Planner: ₹14-18 LPA, Urban Mobility Lead: ₹18-25 LPA)',
        'education': 'B.Plan/M.Plan (Transport Planning), M.Tech Transportation Engineering, M.Sc Urban Planning; PhD for research/leadership; Certification: GISP, AICP (USA - internationally recognized)',
        'growth': '14% growth, Smart Cities Mission (100 cities), National Transit-Oriented Development (TOD) Policy, Metro expansion (25+ cities), Bicycle Master Plans (multiple cities), First/Last-mile connectivity focus, PM e-Bus Sewa (10,000 e-buses)',
        'top_companies': ['Smart City Missions - Across 100 Smart Cities (Delhi, Bengaluru, Mumbai, Chennai, Pune, Ahmedabad, Surat, Lucknow, Jaipur, Kochi, Bhubaneswar, Indore, etc.)', 'Urban Local Bodies - All State Capitals, Municipal Corporations', 'Metro Rail Corporations (all metros): DMRC, BMRCL, MMRC, CMRL, HMRL, KMRC, LMRC, GMRC, PMRC, KMRL', 'Consulting Firms: AECOM India - Gurugram, Bengaluru, Mumbai, Chennai, SYSTRA India - Delhi, Mumbai, Bengaluru, Atkins India - Bengaluru, Mumbai, Delhi, Lea Associates - Delhi, Mumbai, RITES - Gurugram, Feedback Infra - Delhi, WSP India - Gurugram, Bengaluru, ITD Consulting - Delhi, Mumbai, Urban Mass Transit Company (UMTC) - Delhi', 'International Agencies: World Bank India - Delhi (Urban Transport), ADB India - Delhi (Sustainable Transport), GIZ India - Delhi (NMT, EV)'],
        'indian_hubs': ['Delhi NCR (Smart Cities Mission HQ, DMRC)', 'Bengaluru (BMRCL, DULT)', 'Mumbai (MMRC, MMRDA)', 'Chennai (CMRL, Chennai Smart City)', 'Ahmedabad (GMRC, AUDA, AMC)', 'Pune (PMRDA, Pune Smart City)', 'Hyderabad (HMRL, GHMC)', 'Kolkata (KMRC, KMDA)', 'Kochi (KMRL)', 'Lucknow (LMRC, LDA)', 'Jaipur (JMRC, JDA)', 'Bhubaneswar (Bhubaneswar Smart City)']
    },

    # ==================== SERVICE, HOSPITALITY & PUBLIC SAFETY CAREERS ====================
    'Hotel Manager': {
        'description': 'Hotel managers oversee hotel operations, manage staff, ensure guest satisfaction, control budgets, and drive revenue growth for Indian hotels, resorts, and hospitality chains.',
        'skills': ['Hotel Operations (Front Office, Housekeeping, F&B)', 'Staff Management & Training', 'Guest Relations & Complaint Handling', 'Revenue Management (RevPAR, ADR, Occupancy)', 'Budgeting & Cost Control', 'Sales & Marketing', 'Quality Standards (ISO 9001)', 'Property Management Systems (PMS - Opera, IDS, WinHms)', 'Inventory Management', 'Team Leadership'],
        'salary_range': '₹3,00,000 - ₹25,00,000 per year (Entry (Asst Manager): ₹3-5 LPA, Duty Manager: ₹4-7 LPA, Hotel Manager: ₹6-12 LPA, General Manager: ₹15-25 LPA, Regional Director: ₹25-50 LPA)',
        'education': 'BBA in Hotel Management, BHMCT (Bachelor of Hotel Management & Catering Technology), Diploma in Hotel Management, MBA in Hospitality',
        'growth': '12-15% growth, India\'s hotel industry growing at 13% CAGR, domestic tourism boom (1.5 billion domestic trips annually), medical tourism ($9 billion by 2026)',
        'top_companies': ['Taj Hotels - Across India', 'Oberoi Hotels - Delhi/Mumbai/Bengaluru', 'ITC Hotels - Across India', 'Marriott India - Across India', 'Hyatt India - Across India', 'Leela Palaces - Mumbai/Delhi/Bengaluru/Goa/Jaipur/Chennai', 'Lemon Tree Hotels - Across 50+ cities', 'Radisson India - Across India', 'Hilton India - Across India', 'Accor India - Across India', 'Club Mahindra - Across 50+ resort locations'],
        'indian_hubs': ['Mumbai', 'Delhi NCR', 'Bengaluru', 'Goa', 'Jaipur', 'Chennai', 'Hyderabad', 'Kolkata', 'Pune', 'Ahmedabad', 'Kochi', 'Udaipur', 'Agra', 'Chandigarh', 'Shimla', 'Manali', 'Darjeeling', 'Ooty', 'Munnar']
    },
    'Restaurant Manager': {
        'description': 'Restaurant managers oversee food and beverage operations, manage service staff, ensure food quality, control inventory, and maximize customer satisfaction in Indian restaurants, cafes, and QSRs.',
        'skills': ['Restaurant Operations', 'Food & Beverage Service', 'Staff Training & Scheduling', 'Inventory Management', 'Cost Control (Food cost, labor cost)', 'Menu Planning & Engineering', 'Customer Service Excellence', 'Food Safety (HACCP, FSSAI compliance)', 'Point of Sale (POS) Systems', 'Vendor Management'],
        'salary_range': '₹2,50,000 - ₹15,00,000 per year (Entry Asst Manager: ₹2.5-4 LPA, Restaurant Manager: ₹4-8 LPA, Senior Manager: ₹8-12 LPA, Multi-unit Manager: ₹12-18 LPA)',
        'education': 'Diploma in Hotel Management, BHMCT, Diploma in Food & Beverage Service, BBA in Hospitality',
        'growth': '14% growth, QSR expansion (Dominos, KFC, McDonalds, Pizza Hut), Cloud kitchens boom (Rebel Foods), Café culture growth (Starbucks, CCD, Chaayos), Dining-out culture post-pandemic',
        'top_companies': ['Dominos India (Jubilant FoodWorks) - Across 1,350+ cities', 'McDonalds India - Across major cities', 'KFC India - Across 300+ cities', 'Pizza Hut India - Across 350+ cities', 'Starbucks India (Tata Starbucks) - Across 350+ stores', 'Cafe Coffee Day - Across 400+ cities', 'Chaayos - Across major cities', 'Barista Coffee - Across 40+ cities', 'Speciality Restaurants (Mainland China) - Across India', 'Impresario (Social, Smoke House Deli) - Across major cities', 'Massive Restaurants (Farzi Café) - Across India', 'Rebel Foods (Faasos) - Across 25+ cities', 'Wow! Momo - Across India'],
        'indian_hubs': ['Mumbai', 'Delhi NCR', 'Bengaluru', 'Pune', 'Hyderabad', 'Chennai', 'Kolkata', 'Ahmedabad', 'Jaipur', 'Chandigarh']
    },
    'Event Manager': {
        'description': 'Event managers plan, coordinate, and execute events including weddings, corporate events, conferences, exhibitions, and festivals for Indian clients and organizations.',
        'skills': ['Event Planning & Coordination', 'Budget Management', 'Vendor Management (Catering, Decor, AV, Lighting, Entertainment)', 'Client Relations', 'Venue Selection', 'Logistics Management', 'Timeline Management', 'Risk Management & Safety', 'Crisis Management', 'Marketing & Promotion', 'On-site Execution', 'Post-event Analysis'],
        'salary_range': '₹3,00,000 - ₹20,00,000 per year (Entry Coordinator: ₹3-5 LPA, Event Manager: ₹5-10 LPA, Senior Manager: ₹10-15 LPA, Event Director: ₹15-22 LPA)',
        'education': 'BBA in Event Management, BA in Event Management, Diploma in Event Management, MBA in Marketing/Operations (with Event specialization)',
        'growth': '18% growth (Very fast), MICE tourism growth (Meetings, Incentives, Conferences, Exhibitions), Wedding industry ($50 billion), Corporate events recovery, Festival & cultural events boom',
        'top_companies': ['Wizcraft International - Mumbai/Delhi/Bengaluru', 'Percept - Mumbai/Delhi/Bengaluru/Pune/Chennai', 'Cineyug - Mumbai/Delhi/Bengaluru', 'Encompass Events - Mumbai/Delhi/Bengaluru', 'Showtime Events - Mumbai/Delhi', 'DNA Entertainment Networks - Mumbai/Delhi', '360 Degrees - Mumbai/Delhi/Bengaluru', 'Sagitar Entertainment - Mumbai', 'SourceWiz - Mumbai/Delhi', 'Buzz Events - Delhi/Bengaluru', 'Concept MICE - Mumbai/Delhi', 'First Choice Events - Mumbai/Delhi', 'Big Bang Experiences - Mumbai/Delhi/Bengaluru'],
        'indian_hubs': ['Mumbai (Event Capital)', 'Delhi NCR', 'Bengaluru', 'Goa (Destination Weddings)', 'Pune', 'Hyderabad', 'Chennai', 'Jaipur (Wedding Destination)', 'Udaipur (Heritage Weddings)', 'Kolkata']
    },
    'Tourism Officer': {
        'description': 'Tourism officers promote tourism destinations, develop tour packages, coordinate with travel trade, and implement tourism policies for Indian government tourism departments and private tour operators.',
        'skills': ['Tourism Marketing & Promotion', 'Destination Management', 'Tour Package Development', 'Travel Trade Relations', 'Event Coordination', 'Social Media & Digital Marketing', 'Cultural & Heritage Knowledge', 'Language Skills (English + Regional Languages)', 'Tourism Policy Implementation', 'Statistics & Reporting', 'Customer Service'],
        'salary_range': '₹3,50,000 - ₹15,00,000 per year (Entry Tourism Officer: ₹3.5-6 LPA, Senior Officer: ₹6-10 LPA, Assistant Director: ₹10-14 LPA, Director Tourism: ₹14-20 LPA)',
        'education': 'BA in Tourism Management, B.Sc in Travel & Tourism, MBA in Tourism, MA in Tourism Management, BBA in Travel & Tourism',
        'growth': '12% growth, Government focus on tourism (Incredible India 2.0, Swadesh Darshan, PRASHAD, Dekho Apna Desh), Medical tourism, Spiritual tourism, Eco-tourism, Rural tourism',
        'top_companies': ['Ministry of Tourism (Govt of India) - Delhi', 'India Tourism Development Corporation (ITDC) - Delhi', 'State Tourism Development Corporations (MTDC, KTDC, RTDC, UP Tourism, Gujarat Tourism, etc.) - State Capitals', 'IRCTC Tourism - Delhi, All Regions', 'Incredible India Campaign - Delhi', 'Kerala Tourism - Thiruvananthapuram', 'Rajasthan Tourism - Jaipur', 'Goa Tourism - Panaji', 'Himachal Tourism - Shimla', 'Uttarakhand Tourism - Dehradun', 'Tamil Nadu Tourism - Chennai', 'Karnataka Tourism - Bengaluru', 'Maharashtra Tourism - Mumbai', 'Gujarat Tourism - Gandhinagar', 'MakeMyTrip - Gurugram', 'Yatra.com - Gurugram', 'Thomas Cook India - Mumbai', 'SOTC - Mumbai', 'Kesari Tours - Mumbai/Pune/Delhi/Bengaluru/Chennai'],
        'indian_hubs': ['Delhi NCR (Tourism HQ)', 'Mumbai', 'Thiruvananthapuram (Kerala Tourism)', 'Jaipur (Rajasthan Tourism)', 'Panaji (Goa Tourism)', 'Bengaluru (Karnataka Tourism)', 'Chennai (Tamil Nadu Tourism)', 'Shimla (HP Tourism)', 'Dehradun (UK Tourism)', 'Gandhinagar (Gujarat Tourism)', 'Bhubaneswar (Odisha Tourism)', 'Guwahati (Assam Tourism)']
    },
    'Customer Service Manager': {
        'description': 'Customer service managers lead customer support teams, manage escalations, improve customer satisfaction metrics, and drive service excellence for Indian BPOs, e-commerce, and service companies.',
        'skills': ['Team Leadership & Coaching', 'Escalation Management', 'Customer Satisfaction (CSAT) Improvement', 'Key Performance Indicators (KPIs) - CSAT, NPS, AHT, FCR', 'Quality Assurance & Monitoring', 'Training & Development', 'Data Analysis (Excel, Tableau)', 'CRM Software (Salesforce, Zendesk, Freshdesk)', 'Conflict Resolution', 'Problem Solving', 'Communication Skills', 'Process Improvement (Six Sigma)'],
        'salary_range': '₹4,00,000 - ₹18,00,000 per year (Entry Team Lead: ₹4-6 LPA, Customer Service Manager: ₹6-12 LPA, Senior Manager: ₹12-16 LPA, Customer Experience Head: ₹16-22 LPA)',
        'education': 'BBA, MBA (Marketing/Operations), BA/B.Com, Diploma in Customer Service, Certification: Six Sigma Green Belt, Customer Experience Professional (CCXP)',
        'growth': '15% growth, E-commerce & D2C brands growth, Customer retention focus, Omni-channel service importance, Chatbots & AI support complementing human agents, BPO industry expansion ($50 billion by 2025)',
        'top_companies': ['Teleperformance India - Across 30+ cities', 'Concentrix India - Across 20+ cities', 'Tech Mahindra BPO - Pune/Bengaluru/Hyderabad/Noida/Chennai/Kolkata', 'Wipro BPO - Bengaluru/Hyderabad/Pune/Chennai/Kolkata/Delhi NCR', 'Infosys BPM - Bengaluru/Hyderabad/Pune/Jaipur/Mysore/Bhubaneswar', 'TCS BPS - Across 30+ cities', 'HCL BPO - Noida/Chennai/Bengaluru/Hyderabad/Pune/Nagpur', 'FirstSource Solutions - Mumbai/Bengaluru/Chennai/Indore/Bhopal/Salem/Raipur', 'Startek - Mumbai/Bengaluru/Delhi NCR/Chennai/Hyderabad/Pune', 'Amazon Customer Service - Hyderabad/Bengaluru/Delhi NCR', 'Flipkart Customer Support - Bengaluru/Gurugram', 'Swiggy Customer Service - Bengaluru/Gurugram', 'Zomato Customer Support - Gurugram', 'Razorpay CX - Bengaluru', 'Paytm Customer Service - Noida', 'PhonePe Customer Experience - Bengaluru', 'CRED Customer Experience - Bengaluru', 'Ola Customer Support - Bengaluru', 'Uber India Support - Hyderabad'],
        'indian_hubs': ['Bengaluru (CX Hub)', 'Delhi NCR (Gurugram, Noida)', 'Mumbai', 'Hyderabad', 'Pune', 'Chennai', 'Kolkata', 'Ahmedabad', 'Indore', 'Jaipur', 'Nagpur', 'Bhopal', 'Chandigarh']
    },
    'Police Officer': {
        'description': 'Police officers maintain law and order, prevent crime, conduct investigations, and protect citizens and property in Indian states and union territories.',
        'skills': ['Law Enforcement (IPC, CrPC, Evidence Act)', 'Investigation Techniques', 'Crime Scene Management', 'Report Writing (FIR, Chargesheet)', 'Patrol & Surveillance', 'Crowd Control', 'Crisis Intervention', 'Communication & Negotiation', 'Physical Fitness', 'Firearms Training', 'Cyber Crime Awareness', 'Traffic Management', 'Human Rights Knowledge'],
        'salary_range': '₹4,00,000 - ₹20,00,000 per year (Entry (SI/Inspector): ₹4-8 LPA, DSP/ACP: ₹9-12 LPA, SP/DCP: ₹12-16 LPA, SSP/Commissioner: ₹16-20 LPA, IG/DIG: ₹20-30 LPA)',
        'education': "Bachelor's degree (any discipline) + UPSC/State PSC exams (Civil Services) for IPS, State Police recruitment for Sub-Inspector/Constable (10+2/12th pass)",
        'growth': '5-7% growth, Police modernization (CCTNS, Crime & Criminal Tracking Network, CCTVs, Body cameras), Cyber crime cells expansion, Women safety initiatives, Community policing focus',
        'top_companies': ['Indian Police Service (IPS) - Central & State Cadres', 'Delhi Police - Delhi NCR', 'Mumbai Police - Mumbai Metropolitan Region', 'Bengaluru City Police - Bengaluru', 'Chennai Police - Chennai', 'Kolkata Police - Kolkata', 'Hyderabad Police - Hyderabad', 'Pune Police - Pune', 'Ahmedabad Police - Ahmedabad', 'Jaipur Police - Jaipur', 'Lucknow Police - Lucknow', 'Patna Police - Patna', 'Bhopal Police - Bhopal', 'Chandigarh Police - Chandigarh', 'State Police Departments (Maharashtra, Karnataka, Tamil Nadu, Gujarat, UP, West Bengal, Rajasthan, Kerala, Andhra, Telangana, Punjab, Haryana, Bihar, MP, Odisha, Assam, etc.)', 'Central Armed Police Forces (CRPF, BSF, CISF, ITBP, SSB, NSG - Across India)'],
        'indian_hubs': ['Delhi NCR (Police HQ)', 'Mumbai', 'Bengaluru', 'Chennai', 'Kolkata', 'Hyderabad', 'Pune', 'Ahmedabad', 'Jaipur', 'Lucknow', 'Patna', 'Bhopal', 'Chandigarh', 'All State Capitals']
    },
    'Firefighter': {
        'description': 'Firefighters respond to fire emergencies, rescue people from hazardous situations, conduct fire prevention inspections, and educate the public on fire safety in Indian cities and industrial zones.',
        'skills': ['Fire Suppression Techniques', 'Fire Equipment Operation (Ladders, Hoses, Extinguishers, Pumps)', 'Search & Rescue', 'Emergency Medical Response (First Aid, CPR, AED)', 'Hazardous Materials (HAZMAT) Response', 'Rope Rescue & Confined Space Entry', 'Fire Prevention Inspections', 'Building Codes Knowledge', 'Physical Fitness & Stamina', 'Team Coordination', 'Emergency Communication', 'Fire Investigation Basics'],
        'salary_range': '₹2,50,000 - ₹10,00,000 per year (Entry Firefighter: ₹2.5-4 LPA, Leading Fireman: ₹4-6 LPA, Station Officer: ₹6-8 LPA, Divisional Fire Officer: ₹8-12 LPA, Chief Fire Officer: ₹12-18 LPA)',
        'education': '10+2 pass, Diploma in Fire Safety Engineering, B.Sc in Fire & Safety, Certificate in Fire Fighting from NFSC Nagpur, NIFS certification',
        'growth': '8-10% growth, High-rise building fire safety regulations (mandatory fire NOC), Industrial fire safety (SEZ, factories), Airport fire services expansion, Fire safety audits mandatory for commercial buildings',
        'top_companies': ['Delhi Fire Service - Delhi NCR', 'Mumbai Fire Brigade - Mumbai', 'Kolkata Fire Service - Kolkata', 'Chennai Fire Service - Chennai', 'Bengaluru Fire Service - Bengaluru', 'Hyderabad Fire Service - Hyderabad', 'Ahmedabad Fire Service - Ahmedabad', 'Pune Fire Service - Pune', 'Jaipur Fire Service - Jaipur', 'Lucknow Fire Service - Lucknow', 'National Fire Service College (NFSC) - Nagpur', 'Airport Fire Services - Across all international and domestic airports (AAI & Private)', 'Industrial Fire Services (Tata, Reliance, Adani, L&T) - Across industrial zones', 'Oil & Gas Fire Services (IOCL, BPCL, HPCL, ONGC) - Refineries and installations', 'Defense Fire Services - Army, Navy, Air Force stations across India', 'State Fire Training Centers - All States'],
        'indian_hubs': ['Mumbai', 'Delhi NCR', 'Kolkata', 'Chennai', 'Bengaluru', 'Hyderabad', 'Ahmedabad', 'Nagpur (NFSC)', 'Pune', 'Jaipur', 'Lucknow', 'Chandigarh', 'Industrial corridors (Gujarat, Maharashtra, Tamil Nadu, Karnataka, Andhra)']
    },
    'Emergency Medical Technician (EMT)': {
        'description': 'Emergency Medical Technicians respond to medical emergencies, provide pre-hospital care, stabilize patients, and transport them to hospitals in Indian ambulances and emergency response systems.',
        'skills': ['Patient Assessment (Primary & Secondary Survey)', 'Basic Life Support (BLS - CPR, AED)', 'First Aid (Bleeding control, Fracture immobilization)', 'Airway Management (OPA, NPA, Suction)', 'Oxygen Therapy', 'Spinal Immobilization (Backboard, Cervical collar)', 'Splinting & Bandaging', 'Emergency Childbirth Assistance', 'Ambulance Operations (Driving, Equipment)', 'Medical Terminology', 'Triage (Prioritizing patients)', 'Radio Communication', 'HIPAA/GDPR (Patient Privacy)'],
        'salary_range': '₹1,80,000 - ₹5,00,000 per year (Entry EMT: ₹1.8-3 LPA, Advanced EMT: ₹3-4 LPA, Paramedic: ₹4-6 LPA, EMT Supervisor: ₹5-7 LPA)',
        'education': '10+2 pass, Diploma in Emergency Medical Technology (1-2 years), Certificate in Basic Life Support (BLS), Advanced Cardiac Life Support (ACLS) for paramedics',
        'growth': '15% growth, 108 Emergency Services expansion to all districts, Corporate ambulance services, Event medical services, Industrial on-site EMTs (factories), Private hospital ambulances',
        'top_companies': ['GVK EMRI (108 Services) - Across India (15+ states including Andhra, Telangana, Karnataka, Gujarat, Goa, Assam, etc.)', 'Ziqitza Health Care Limited - Across 8+ states (Maharashtra, Delhi, Odisha, Kerala, Punjab, Rajasthan, MP, Bihar)', 'Medulance - Delhi NCR, Gurugram, Mumbai, Bengaluru, Jaipur, Lucknow, Chennai', 'Portea Medical - Across 12+ cities', 'StanPlus - Hyderabad, Bengaluru, Mumbai, Delhi, Chennai, Kolkata, Pune', 'Swasth Ambulance - Delhi NCR, Mumbai, Bengaluru, Chennai, Hyderabad, Pune', 'CallHealth - Hyderabad, Bengaluru, Chennai, Mumbai, Delhi', 'Pallium India - Thiruvananthapuram, Kochi, Kozhikode (Palliative care ambulances)', 'Hospital-based Ambulance Services - Apollo, Fortis, Max, Manipal, Narayana Health across all locations', 'Industrial EMS - Tata, Reliance, Adani factories/sez zones', 'Event Medical Services - Large event organizers (Cineyug, Wizcraft, Percept for concerts, Kumbh Mela, IPL, etc.)'],
        'indian_hubs': ['Hyderabad (108 HQs)', 'Delhi NCR', 'Mumbai', 'Bengaluru', 'Chennai', 'Ahmedabad', 'Kolkata', 'Pune', 'Jaipur', 'Lucknow', 'Bhopal']
    },
    'Disaster Management Specialist': {
        'description': 'Disaster management specialists coordinate disaster preparedness, response, recovery, and mitigation efforts for Indian government agencies, NGOs, and international organizations.',
        'skills': ['Disaster Risk Reduction (DRR)', 'Emergency Response Planning', 'Incident Command System (ICS)', 'Search & Rescue Coordination', 'Logistics Management for Disasters', 'Humanitarian Operations', 'Needs Assessment', 'Resource Mobilization', 'Stakeholder Coordination (Govt, NGOs, Armed Forces)', 'Public Awareness & Training', 'Reporting & Documentation', 'GIS Mapping for Disaster Management', 'Early Warning Systems'],
        'salary_range': '₹4,00,000 - ₹18,00,000 per year (Entry Associate: ₹4-7 LPA, Disaster Specialist: ₹7-11 LPA, Manager: ₹11-15 LPA, Director (NDMA/SDMA): ₹15-20 LPA)',
        'education': 'Master\'s/M.Sc in Disaster Management, PG Diploma in Disaster Management, B.Tech/M.Tech in Disaster Mitigation, NIDM certification, PhD for research/policy roles',
        'growth': '14% growth, Climate change increasing disasters (floods, cyclones, heat waves, earthquakes), NDMA/SDMA expansion, NDRF battalions increasing, Corporate disaster preparedness (BS 25999, ISO 22301), Community-based disaster management (CBDM)',
        'top_companies': ['National Disaster Management Authority (NDMA) - Delhi', 'National Disaster Response Force (NDRF) HQ - Delhi (12 Battalions across India)', 'State Disaster Management Authorities (SDMA) - All State Capitals', 'National Institute of Disaster Management (NIDM) - Delhi', 'Indian Meteorological Department (IMD) - Delhi, Pune, Kolkata, Chennai, Mumbai, Bengaluru, Hyderabad, Guwahati, Nagpur, Thiruvananthapuram, Ahmedabad', 'Central Water Commission (CWC) - Delhi (Flood Forecasting)', 'Geological Survey of India (GSI) - Kolkata, Across India (Landslide/Earthquake studies)', 'UNICEF India (Disaster Risk Reduction) - Delhi', 'UNDP India (Disaster Management) - Delhi', 'World Bank India (Disaster Risk Financing) - Delhi', 'Asian Disaster Preparedness Centre (ADPC) - Delhi (Regional office)', 'SEEDS India - Delhi NCR (NGO - Community resilience)', 'Goonj (Post-disaster response) - Delhi NCR', 'ActionAid India (Disaster Response) - Bengaluru', 'Save the Children India (Disaster Response) - Delhi', 'Red Cross India (Disaster Response) - Across all states', 'Corporate Disaster Management - Tata, Reliance, Adani, Infosys (BCP teams) - Respective HQs'],
        'indian_hubs': ['Delhi NCR (NDMA, NDRF HQ, NIDM)', 'Mumbai (IMD Regional Office)', 'Kolkata (GSI HQ)', 'Chennai (IMD Regional Office)', 'Pune (IMD HQ - Earth System Science)', 'Hyderabad (Disaster Management Telangana)', 'Ahmedabad (Disaster Management Gujarat)', 'Bengaluru (Disaster Management Karnataka)', 'Guwahati (Northeast Disaster Hub)', 'Thiruvananthapuram (Kerala Disaster Hub)']
    },
    'Security Manager': {
        'description': 'Security managers oversee security operations, manage security personnel, conduct risk assessments, implement security protocols, and ensure compliance with safety regulations for Indian corporations, malls, hotels, and events.',
        'skills': ['Security Operations Management', 'Risk Assessment & Security Audits', 'Physical Security (CCTV, Access Control, Alarm Systems)', 'Security Guard Management', 'Emergency Response Planning', 'Incident Investigation & Reporting', 'Liaison with Police/Fire Services', 'Security Protocol Development (SOPs)', 'Budget Management (Security contracts)', 'Safety Compliance (OSHA, Factory Act)', 'Training & Drill Management', 'Crisis Communication'],
        'salary_range': '₹3,00,000 - ₹15,00,000 per year (Entry Security Supervisor: ₹3-5 LPA, Security Manager: ₹5-10 LPA, Senior Manager: ₹10-13 LPA, Head of Security: ₹13-18 LPA)',
        'education': 'Bachelor\'s degree, Diploma in Security Management, Certification in Physical Security (ASIS International - CPP), MBA in Security Management (rare)',
        'growth': '10% growth, Corporate security expansion (CCTV mandatory for public buildings, IT parks, malls), PSARA Act (2005) regulating private security agencies, Airport security (BCAS standards), Event security demand, Gated communities growth',
        'top_companies': ['Securitas India - Across 30+ cities', 'G4S India - Across 40+ cities', 'Topsgrup - Mumbai/Delhi/Bengaluru/Chennai/Hyderabad/Pune/Kolkata/Ahmedabad', 'Peregrine Guarding - Mumbai/Delhi/Bengaluru/Chennai/Hyderabad/Pune', 'SIS India - Across 200+ locations', 'Guardian Security - Across India', 'ORCA Security - Bengaluru', 'Tata Security - Across Tata Group companies', 'Reliance Security - Across Reliance Group companies', 'Adani Security - Across Adani Group locations', 'Corporate Security - HDFC Bank, ICICI Bank, Infosys, Wipro, TCS, Flipkart, Amazon India (Corporate & Facility security) - Across major cities', 'Airport Security (CISF) - All airports - Direct contract, also private security at non-core areas', 'Mall Security - Phoenix, DLF, Select Citywalk, Inorbit, etc. - Across major cities'],
        'indian_hubs': ['Mumbai', 'Delhi NCR', 'Bengaluru', 'Chennai', 'Hyderabad', 'Pune', 'Ahmedabad', 'Kolkata', 'Gurugram', 'Noida']
    },
    'Airport Customer Service Agent': {
        'description': 'Airport customer service agents assist passengers with check-in, baggage handling, boarding, flight inquiries, and special assistance at Indian airports for airlines and ground handling companies.',
        'skills': ['Check-in Procedures (CUTE, CUSS, DCS - Departure Control Systems)', 'Baggage Handling & Tagging', 'Boarding Gate Operations', 'Flight Information Management', 'Customer Service Excellence', 'Passenger Handling (Unaccompanied minors, wheelchair, pets)', 'Overbooking & Rerouting', 'Special Assistance (PRM - Persons with Reduced Mobility)', 'Emergency Response', 'Conflict Resolution', 'Airport Security Protocols (BCAS)', 'Communication (English + Regional Language)'],
        'salary_range': '₹2,00,000 - ₹6,00,000 per year (Entry CSA: ₹2-3.5 LPA, Senior CSA: ₹3.5-5 LPA, Duty Manager: ₹5-7 LPA)',
        'education': 'Graduation (any stream), Diploma in Aviation Management, Certificate in Airport Ground Handling, IATA certification in Ground Operations',
        'growth': '12% growth, Passenger traffic growth (500M+ by 2030), New airports (Noida, Navi Mumbai, Mopa), Airline expansion (IndiGo, Akasa, Air India expansion), Ground handling privatization (Ramp, Passenger services)',
        'top_companies': ['Air India - Delhi, Mumbai, Bengaluru, Chennai, Kolkata, Hyderabad, Ahmedabad, Pune, Kochi, Goa, Chandigarh, Lucknow, Guwahati', 'IndiGo - Across 100+ airports', 'SpiceJet - Across 60+ airports', 'Vistara - Across 50+ airports', 'Akasa Air - Across 25+ airports', 'Go First - Across 30+ airports (operational challenges currently)', 'Airport Authority of India (AAI) - All operational airports', 'GMR Airports (Ground Handling - Delhi, Hyderabad, Goa) - Delhi, Hyderabad, Goa', 'Adani Airports (Ground Handling - Mumbai, Ahmedabad, Lucknow, Mangaluru, Jaipur, Guwahati, Thiruvananthapuram) - Respective cities', 'Celebi Ground Handling - Delhi, Mumbai, Bengaluru, Chennai, Hyderabad, Kolkata, Kochi, Ahmedabad, Pune, Goa', 'Bhadra Ground Handling - Bengaluru, Mumbai, Delhi, Chennai, Hyderabad, Pune, Kolkata, Ahmedabad', 'Bird Group (Ground Services) - Delhi, Mumbai, Bengaluru, Chennai, Hyderabad, Kolkata, Pune', 'InterGlobe Air Transport (IGAT) - Across India (IndiGo\'s ground handling)'],
        'indian_hubs': ['Delhi NCR (IGI Airport)', 'Mumbai (CSIA Airport)', 'Bengaluru (KIA Airport)', 'Hyderabad (RGIA Airport)', 'Chennai International Airport', 'Kolkata Airport', 'Goa (Mopa & Dabolim Airport)', 'Ahmedabad Airport', 'Pune Airport', 'Kochi Airport', 'Jaipur Airport', 'Lucknow Airport', 'Guwahati Airport', 'Thiruvananthapuram Airport']
    },
    # ==================== ENERGY & UTILITIES CAREERS ====================
    'Power Plant Engineer': {
        'description': 'Operate and maintain thermal, hydro, nuclear, or renewable power plants ensuring efficient electricity generation.',
        'skills': ['Plant Operations', 'Maintenance Planning', 'SCADA/DCS Systems', 'Safety Protocols', 'Performance Optimization', 'Team Supervision'],
        'salary_range': '₹4,00,000 - ₹20,00,000 per year',
        'education': 'B.Tech Mechanical/Electrical/Power Engineering, Diploma in Engineering',
        'growth': '8-10% growth, India adding 50 GW new capacity by 2030',
        'top_companies': ['NTPC', 'Tata Power', 'Adani Power', 'JSW Energy', 'Torrent Power', 'CESC', 'NHPC', 'NPCIL'],
        'indian_hubs': ['Delhi NCR', 'Mumbai', 'Ahmedabad', 'Kolkata', 'Chennai', 'Hyderabad', 'Nagpur', 'Raipur']
    },
    'Solar Project Manager': {
        'description': 'Oversee planning, execution, and commissioning of solar power projects from land acquisition to grid connection.',
        'skills': ['Project Management (PMP)', 'Solar PV Design (PVSyst)', 'Contract Management', 'Vendor Management', 'Quality Control', 'Grid Connectivity'],
        'salary_range': '₹5,00,000 - ₹25,00,000 per year',
        'education': 'B.Tech Electrical/Mechanical, MBA, PMP certification, PG Diploma in Solar Energy',
        'growth': '18-20% growth, India\'s 275 GW solar target by 2030',
        'top_companies': ['Adani Green', 'ReNew Power', 'Azure Power', 'Tata Power Solar', 'Sterling & Wilson', 'L&T Solar', 'Gensol Engineering', 'Mahindra Susten'],
        'indian_hubs': ['Ahmedabad', 'Mumbai', 'Delhi NCR', 'Bengaluru', 'Kolkata', 'Hyderabad', 'Pune', 'Chennai']
    },
    'Wind Energy Engineer': {
        'description': 'Design, develop, install, and maintain wind farms including site assessment and turbine selection.',
        'skills': ['Wind Resource Assessment (WAsP)', 'Micro-siting', 'Turbine Technology', 'SCADA Systems', 'O&M Planning', 'GIS Mapping'],
        'salary_range': '₹4,00,000 - ₹20,00,000 per year',
        'education': 'B.Tech Mechanical/Electrical/Aerospace, B.Tech Wind Energy, Diploma in Wind Energy (NIWE)',
        'growth': '15% growth, India\'s 100 GW wind target by 2030',
        'top_companies': ['Suzlon', 'Vestas India', 'Siemens Gamesa', 'Inox Wind', 'GE Renewable', 'Nordex', 'Envision', 'ReNew Power', 'Adani Green'],
        'indian_hubs': ['Chennai', 'Pune', 'Bengaluru', 'Ahmedabad', 'Gurugram', 'Hyderabad', 'Mumbai']
    },
    'Energy Analyst': {
        'description': 'Analyze energy consumption patterns, perform energy audits, forecast energy prices, and provide data-driven recommendations.',
        'skills': ['Data Analysis (Python, R, SQL)', 'Energy Forecasting', 'Energy Auditing', 'Energy Modelling (RETScreen)', 'Market Analysis', 'Report Writing (Tableau, PowerBI)'],
        'salary_range': '₹4,00,000 - ₹18,00,000 per year',
        'education': 'B.Tech Electrical/Mechanical, M.Tech Energy Systems, MBA Energy Management, BEE Energy Auditor certified',
        'growth': '14% growth, mandatory energy audits for large industries, carbon markets starting 2025',
        'top_companies': ['Deloitte', 'PwC', 'KPMG', 'EY', 'ABPS Infrastructure', 'CES Pune', 'PTC India', 'IEX', 'TERI', 'CSTEP', 'BEE', 'EESL'],
        'indian_hubs': ['Delhi NCR', 'Mumbai', 'Bengaluru', 'Pune', 'Kolkata', 'Hyderabad', 'Chennai', 'Ahmedabad']
    },
    'Oil & Gas Engineer': {
        'description': 'Manage exploration, drilling, production, refining, and transportation of crude oil and natural gas.',
        'skills': ['Petroleum Engineering', 'Drilling Engineering', 'Reservoir Simulation', 'Refinery Operations', 'Pipeline Engineering', 'Safety (HAZOP)', 'Process Simulation (Aspen HYSYS)'],
        'salary_range': '₹6,00,000 - ₹35,00,000 per year',
        'education': 'B.Tech Petroleum/Chemical Engineering (UPES, IIT ISM, PDPU), M.Tech, MBA Oil & Gas',
        'growth': '9-11% growth, OALP exploration rounds, CGD expansion to 300+ districts',
        'top_companies': ['ONGC', 'OIL', 'Reliance Industries', 'Cairn Oil & Gas', 'IOCL', 'BPCL', 'HPCL', 'GAIL', 'Gujarat Gas', 'IGL', 'MGL', 'Adani Total Gas'],
        'indian_hubs': ['Dehradun', 'Mumbai', 'Delhi NCR', 'Ahmedabad', 'Chennai', 'Kolkata', 'Gurugram', 'Gandhinagar', 'Jamnagar']
    },
    'Utility Manager': {
        'description': 'Oversee electricity, water, or gas utility operations including distribution networks, customer service, billing, and infrastructure planning.',
        'skills': ['Utility Operations', 'Network Planning', 'Customer Management', 'Billing & Revenue', 'Regulatory Compliance', 'Smart Grid Implementation', 'Team Leadership'],
        'salary_range': '₹6,00,000 - ₹25,00,000 per year',
        'education': 'B.Tech Electrical/Mechanical/Civil, MBA Power Management, PG Diploma Utility Management (NPTI)',
        'growth': '10-12% growth, RDSS scheme ₹3 lakh crore, smart metering (10 crore meters)',
        'top_companies': ['BSES Delhi', 'TPDDL Delhi', 'Adani Electricity Mumbai', 'CESC Kolkata', 'UPPCL Lucknow', 'MSEDCL Mumbai', 'TANGEDCO Chennai', 'KPTCL Bengaluru', 'GUVNL Vadodara'],
        'indian_hubs': ['Delhi NCR', 'Mumbai', 'Kolkata', 'Chennai', 'Bengaluru', 'Hyderabad', 'Ahmedabad', 'Lucknow', 'Jaipur']
    },
    'Energy Consultant': {
        'description': 'Advise industries, commercial buildings, and government on energy efficiency, renewable energy adoption, carbon reduction, and regulatory compliance.',
        'skills': ['Energy Auditing (BEE)', 'Energy Efficiency Technologies', 'Renewable Integration', 'Carbon Footprint', 'Financial Analysis (IRR, NPV)', 'Policy & Regulatory', 'M&V (IPMVP)'],
        'salary_range': '₹5,00,000 - ₹22,00,000 per year',
        'education': 'B.Tech (Mechanical/Electrical), BEE Certified Energy Manager (CEM), MBA Energy Management, LEED certification',
        'growth': '15-18% growth, PAT scheme, ESCerts trading, ECBC mandatory, ESCO market growth',
        'top_companies': ['Deloitte', 'PwC', 'KPMG', 'EY', 'EESL', 'BEE', 'TERI', 'ICLEI', 'CSTEP', 'ABPS', 'CES Pune', 'SgurrEnergy'],
        'indian_hubs': ['Delhi NCR', 'Mumbai', 'Bengaluru', 'Pune', 'Kolkata', 'Chennai', 'Ahmedabad', 'Hyderabad']
    },
    # Add these to your CAREER_DETAILS_DB dictionary

  'Environmental Scientist': {
     'description': 'Environmental scientists study environmental problems and develop solutions to protect the environment and human health. They analyze data, conduct research, and advise on environmental policies.',
     'skills': ['Data Analysis', 'Field Sampling', 'Environmental Monitoring', 'Report Writing', 'GIS', 'Statistical Analysis', 'Regulatory Knowledge'],
     'salary_range': '$55,000 - $95,000 per year',
     'education': "Bachelor's degree in Environmental Science, Biology, Chemistry, or related field; Master's preferred for advancement",
     'growth': '8% growth (Faster than average)',
     'top_companies': ['EPA', 'Environmental Consulting Firms', 'Government Agencies', 'Research Institutes', 'NGOs']
 }, 
 'Agricultural Engineer': {
     'description': 'Agricultural engineers design and develop solutions for farming, food processing, and natural resource conservation. They work on irrigation systems, farm machinery, and sustainable agriculture practices.',
     'skills': ['Engineering Design', 'Problem Solving', 'Project Management', 'CAD Software', 'Irrigation Systems', 'Precision Agriculture', 'Data Analysis'],
     'salary_range': '$60,000 - $110,000 per year',
     'education': "Bachelor's degree in Agricultural Engineering, Biological Engineering, or related field",
     'growth': '6% growth (Average)',
     'top_companies': ['John Deere', 'Caterpillar', 'Bayer', 'Cargill', 'USDA', 'Farm Equipment Manufacturers']
  },
  'Geologist': {
     'description': 'Geologists study the Earth\'s physical structure, composition, and history. They search for natural resources, assess environmental hazards, and advise on land use and construction projects.',
     'skills': ['Field Mapping', 'Rock and Mineral Identification', 'Geophysical Surveys', 'GIS', 'Data Interpretation', 'Report Writing', 'Risk Assessment'],
     'salary_range': '$60,000 - $120,000 per year',
     'education': "Bachelor's degree in Geology or Earth Sciences; Master's for research or specialized roles",
     'growth': '5% growth (Average)',
     'top_companies': ['Mining Companies', 'Oil and Gas Companies', 'Environmental Consulting Firms', 'USGS', 'Government Agencies']
  },
  'Climate Change Analyst': {
     'description': 'Climate change analysts study climate patterns, model future scenarios, and develop strategies to mitigate and adapt to climate change impacts.',
     'skills': ['Climate Modeling', 'Data Analysis', 'Statistical Software', 'GIS', 'Research Methods', 'Policy Analysis', 'Communication Skills'],
     'salary_range': '$65,000 - $115,000 per year',
     'education': "Master's degree in Climate Science, Atmospheric Science, Environmental Science, or related field",
     'growth': '15% growth (Much faster than average)',
     'top_companies': ['NASA', 'NOAA', 'Environmental Defense Fund', 'World Resources Institute', 'Climate Policy Institutes']
  },
  'Conservation Scientist': {
     'description': 'Conservation scientists manage and protect natural resources, including forests, rangelands, and wildlife habitats. They develop conservation plans and work with landowners to implement sustainable practices.',
     'skills': ['Ecological Assessment', 'Land Management', 'Data Collection', 'GIS', 'Environmental Law Knowledge', 'Communication', 'Project Planning'],
     'salary_range': '$55,000 - $90,000 per year',
     'education': "Bachelor's degree in Forestry, Conservation Biology, Environmental Science, or related field",
     'growth': '7% growth (Faster than average)',
     'top_companies': ['US Forest Service', 'National Park Service', 'The Nature Conservancy', 'State Conservation Agencies', 'NGOs']
  },
  'Renewable Energy Specialist': {
     'description': 'Renewable energy specialists develop and implement clean energy solutions including solar, wind, hydro, and geothermal power systems. They assess feasibility, design systems, and promote sustainable energy adoption.',
     'skills': ['Energy Systems Design', 'Project Management', 'Technical Analysis', 'Feasibility Studies', 'Regulatory Knowledge', 'Data Analysis', 'Communication'],
     'salary_range': '$65,000 - $120,000 per year',
     'education': "Bachelor's degree in Renewable Energy, Mechanical Engineering, Environmental Science, or related field",
     'growth': '20% growth (Much faster than average)',
     'top_companies': ['Tesla', 'NextEra Energy', 'Siemens Gamesa', 'Vestas', 'SolarCity', 'GE Renewable Energy']
 },
 'Sustainable Agriculture Specialist': {
     'description': 'Sustainable agriculture specialists promote farming practices that are environmentally friendly, economically viable, and socially responsible. They work with farmers to implement regenerative and organic farming methods.',
     'skills': ['Agronomy Knowledge', 'Soil Science', 'Crop Management', 'Farm Planning', 'Research Skills', 'Extension Education', 'Communication'],
     'salary_range': '$50,000 - $85,000 per year',
     'education': "Bachelor's degree in Agriculture, Agronomy, Environmental Science, or related field",
     'growth': '9% growth (Faster than average)',
     'top_companies': ['USDA NRCS', 'Organic Farming Research Foundation', 'Rodale Institute', 'Sustainable Agriculture Organizations', 'Agricultural Consulting Firms']
  },
 'Hydrologist': {
     'description': 'Hydrologists study water distribution, movement, and quality on Earth. They assess water resources, predict floods and droughts, and develop water management strategies.',
     'skills': ['Hydrological Modeling', 'Data Analysis', 'GIS', 'Water Sampling', 'Statistical Analysis', 'Report Writing', 'Regulatory Knowledge'],
     'salary_range': '$65,000 - $110,000 per year',
     'education': "Bachelor's degree in Hydrology, Geology, Environmental Science, or related field; Master's preferred",
     'growth': '7% growth (Faster than average)',
     'top_companies': ['USGS', 'EPA', 'Water Districts', 'Environmental Consulting Firms', 'Dam Authorities']
   },
 'Environmental Engineer': {
     'description': 'Environmental engineers design solutions to environmental problems, including pollution control, waste management, water treatment, and remediation of contaminated sites.',
     'skills': ['Engineering Design', 'Problem Solving', 'Water Treatment', 'Air Quality Control', 'Waste Management', 'CAD Software', 'Regulatory Compliance'],
     'salary_range': '$65,000 - $120,000 per year',
     'education': "Bachelor's degree in Environmental Engineering, Civil Engineering, or Chemical Engineering",
     'growth': '8% growth (Faster than average)',
     'top_companies': ['AECOM', 'Jacobs Engineering', 'CH2M Hill', 'Environmental Consulting Firms', 'Government Agencies']
   },
   # Add these to your CAREER_DETAILS_DB dictionary

'E-commerce Manager': {
    'description': 'E-commerce managers oversee online sales operations, including website management, product listings, pricing strategies, and customer experience. They drive online revenue growth and optimize digital store performance.',
    'skills': ['E-commerce Platforms', 'Digital Marketing', 'Data Analysis', 'Inventory Management', 'Customer Service', 'Project Management', 'SEO/SEM'],
    'salary_range': '$55,000 - $120,000 per year',
    'education': "Bachelor's degree in Business, Marketing, or IT; MBA preferred",
    'growth': '15% growth (Much faster than average)',
    'top_companies': ['Amazon', 'Flipkart', 'Walmart', 'Shopify', 'Myntra', 'Nykaa']
},
'Digital Marketing Specialist': {
    'description': 'Digital marketing specialists develop and execute online marketing campaigns across search engines, social media, email, and other digital channels to drive traffic and sales.',
    'skills': ['SEO/SEM', 'Social Media Marketing', 'Email Marketing', 'Content Creation', 'Google Analytics', 'PPC Advertising', 'Conversion Optimization'],
    'salary_range': '$45,000 - $85,000 per year',
    'education': "Bachelor's degree in Marketing, Communications, or Business; Digital marketing certifications",
    'growth': '10% growth (Faster than average)',
    'top_companies': ['Digital Marketing Agencies', 'E-commerce Companies', 'Retail Brands', 'Startups', 'Amazon']
},
'Supply Chain Analyst': {
    'description': 'Supply chain analysts optimize logistics, inventory, and distribution processes. They analyze data to improve efficiency, reduce costs, and ensure timely product delivery.',
    'skills': ['Data Analysis', 'Inventory Management', 'Logistics Planning', 'Forecasting', 'ERP Systems', 'Problem Solving', 'Excel/SQL'],
    'salary_range': '$55,000 - $95,000 per year',
    'education': "Bachelor's degree in Supply Chain, Business, or Logistics; Master's preferred",
    'growth': '8% growth (Faster than average)',
    'top_companies': ['Amazon Logistics', 'Flipkart', 'DHL', 'FedEx', 'Blue Dart', 'Delhivery', 'Shadowfax']
},
'Retail Store Manager': {
    'description': 'Retail store managers oversee daily store operations, including sales, staff management, customer service, inventory, and visual merchandising to achieve business goals.',
    'skills': ['Leadership', 'Sales Management', 'Customer Service', 'Inventory Control', 'Staff Training', 'Financial Management', 'Problem Solving'],
    'salary_range': '$40,000 - $80,000 per year',
    'education': "Bachelor's degree in Business, Retail Management, or related field",
    'growth': '5% growth (Average)',
    'top_companies': ['Reliance Retail', 'Tata Croma', 'Shoppers Stop', 'Westside', 'Lifestyle', 'Pantaloons']
},
'Merchandise Planner': {
    'description': 'Merchandise planners develop product assortment strategies, plan inventory levels, and analyze sales data to optimize product mix and maximize profitability.',
    'skills': ['Data Analysis', 'Forecasting', 'Inventory Planning', 'Excel', 'Retail Math', 'Product Knowledge', 'Strategic Thinking'],
    'salary_range': '$50,000 - $90,000 per year',
    'education': "Bachelor's degree in Merchandising, Business, or Fashion Retail",
    'growth': '6% growth (Average)',
    'top_companies': ['Myntra', 'Nykaa', 'Ajio', 'Tata Cliq', 'Shoppers Stop', 'Westside']
},
'Customer Experience Manager': {
    'description': 'Customer experience managers design and implement strategies to improve customer satisfaction, loyalty, and retention across all touchpoints in the retail journey.',
    'skills': ['Customer Service', 'Data Analysis', 'Process Improvement', 'Communication', 'Problem Solving', 'CRM Systems', 'Empathy'],
    'salary_range': '$55,000 - $100,000 per year',
    'education': "Bachelor's degree in Business, Marketing, or Psychology; MBA preferred",
    'growth': '12% growth (Faster than average)',
    'top_companies': ['Amazon', 'Zappos', 'Flipkart', 'Apple Retail', 'Starbucks', 'Nordstrom']
},
'Product Manager (E-commerce)': {
    'description': 'Product managers define product vision, strategy, and roadmap for e-commerce platforms. They work with engineering, design, and marketing teams to launch and improve online shopping features.',
    'skills': ['Product Strategy', 'User Research', 'Agile Methodology', 'Data Analysis', 'Roadmap Planning', 'Cross-functional Leadership', 'A/B Testing'],
    'salary_range': '$70,000 - $150,000 per year',
    'education': "Bachelor's degree in Business, CS, or Engineering; MBA preferred",
    'growth': '14% growth (Much faster than average)',
    'top_companies': ['Amazon', 'Flipkart', 'Google Shopping', 'Meta Commerce', 'Shopify', 'Walmart']
},
'Logistics Coordinator': {
    'description': 'Logistics coordinators manage shipping, warehousing, and transportation operations to ensure efficient product movement from suppliers to customers.',
    'skills': ['Logistics Planning', 'Communication', 'Problem Solving', 'Inventory Tracking', 'Vendor Management', 'Documentation', 'Time Management'],
    'salary_range': '$40,000 - $70,000 per year',
    'education': "Bachelor's degree in Logistics, Supply Chain, or Business",
    'growth': '6% growth (Average)',
    'top_companies': ['Amazon Logistics', 'Flipkart', 'Delhivery', 'Ecom Express', 'Xpressbees', 'DTDC']
},
'Category Manager': {
    'description': 'Category managers oversee specific product categories, including assortment planning, pricing, promotions, and vendor relationships to maximize sales and profitability.',
    'skills': ['Category Strategy', 'Vendor Negotiation', 'Data Analysis', 'Pricing Strategy', 'Inventory Management', 'Market Research', 'Financial Planning'],
    'salary_range': '$60,000 - $120,000 per year',
    'education': "Bachelor's degree in Business, Marketing, or Merchandising; MBA preferred",
    'growth': '7% growth (Faster than average)',
    'top_companies': ['Amazon', 'Flipkart', 'Myntra', 'Nykaa', 'Walmart', 'Target', 'Reliance Retail']
},
'Social Media Manager': {
    'description': 'Social media managers develop and execute social media strategies to build brand awareness, engage customers, and drive e-commerce sales through social platforms.',
    'skills': ['Social Media Platforms', 'Content Creation', 'Community Management', 'Analytics', 'Copywriting', 'Campaign Management', 'Trend Awareness'],
    'salary_range': '$45,000 - $85,000 per year',
    'education': "Bachelor's degree in Marketing, Communications, or related field",
    'growth': '9% growth (Faster than average)',
    'top_companies': ['E-commerce Brands', 'Digital Agencies', 'Retail Companies', 'Fashion Brands', 'Beauty Brands']
},
'Online Marketplace Specialist': {
    'description': 'Online marketplace specialists manage seller accounts on platforms like Amazon, Flipkart, and eBay. They optimize listings, manage advertising, and analyze marketplace performance.',
    'skills': ['Marketplace Platforms', 'Listing Optimization', 'PPC Advertising', 'Inventory Management', 'Data Analysis', 'Customer Service', 'Competitor Analysis'],
    'salary_range': '$40,000 - $75,000 per year',
    'education': "Bachelor's degree in Business, Marketing, or E-commerce",
    'growth': '12% growth (Faster than average)',
    'top_companies': ['Amazon Seller Support', 'Flipkart', 'eBay', 'Etsy', 'Walmart Marketplace', 'Meesho']
},
'Warehouse Operations Manager': {
    'description': 'Warehouse operations managers oversee fulfillment center operations, including receiving, storage, picking, packing, and shipping to ensure efficient order fulfillment.',
    'skills': ['Warehouse Management', 'Team Leadership', 'Process Optimization', 'Inventory Control', 'Safety Compliance', 'ERP Systems', 'Problem Solving'],
    'salary_range': '$55,000 - $100,000 per year',
    'education': "Bachelor's degree in Logistics, Supply Chain, or Business; Operations certifications",
    'growth': '7% growth (Faster than average)',
    'top_companies': ['Amazon Fulfillment', 'Flipkart', 'Myntra', 'BigBasket', 'Blinkit', 'Zepto']
  },
  # Add these to your CAREER_DETAILS_DB dictionary

'Chartered Accountant (CA)': {
    'description': 'Chartered Accountants manage financial accounts, conduct audits, provide tax advice, and ensure financial compliance for organizations. They are essential for business financial health and regulatory compliance.',
    'skills': ['Accounting Principles', 'Auditing', 'Taxation', 'Financial Reporting', 'Analytical Skills', 'Attention to Detail', 'Ethical Judgment'],
    'salary_range': '$60,000 - $150,000 per year',
    'education': 'CA qualification (3-5 years after graduation), B.Com or equivalent degree',
    'growth': '6% growth (Average)',
    'top_companies': ['Deloitte', 'PwC', 'KPMG', 'EY', 'Grant Thornton', 'BDO', 'Corporate Finance Departments']
},
'Certified Public Accountant (CPA)': {
    'description': 'CPAs provide accounting services, tax preparation, auditing, and financial consulting to individuals and businesses. They are licensed professionals trusted for financial expertise.',
    'skills': ['US GAAP', 'Tax Preparation', 'Auditing', 'Financial Analysis', 'Ethics', 'Client Management', 'Software Proficiency'],
    'salary_range': '$65,000 - $140,000 per year',
    'education': 'Bachelor\'s degree, CPA certification, 150 credit hours',
    'growth': '7% growth (Faster than average)',
    'top_companies': ['Deloitte', 'PwC', 'KPMG', 'EY', 'Mid-size CPA Firms', 'Corporate Finance']
},
'Financial Analyst': {
    'description': 'Financial analysts evaluate investment opportunities, analyze financial data, and provide recommendations to businesses and individuals for investment decisions.',
    'skills': ['Financial Modeling', 'Data Analysis', 'Excel', 'Valuation Techniques', 'Industry Research', 'Communication', 'Critical Thinking'],
    'salary_range': '$55,000 - $120,000 per year',
    'education': "Bachelor's degree in Finance, Economics, or Accounting; MBA or CFA preferred",
    'growth': '9% growth (Faster than average)',
    'top_companies': ['Goldman Sachs', 'Morgan Stanley', 'JP Morgan', 'BlackRock', 'Fidelity', 'Investment Banks']
},
'Investment Banker': {
    'description': 'Investment bankers help companies raise capital, facilitate mergers and acquisitions, and provide strategic financial advice for major transactions.',
    'skills': ['Financial Modeling', 'Valuation', 'Negotiation', 'Deal Making', 'Client Management', 'Excel', 'Presentation Skills'],
    'salary_range': '$100,000 - $250,000+ per year',
    'education': "Bachelor's degree in Finance, Economics, or Business; MBA from top school preferred",
    'growth': '10% growth (Average)',
    'top_companies': ['Goldman Sachs', 'Morgan Stanley', 'JP Morgan', 'Bank of America', 'Citigroup', 'Deutsche Bank']
},
'Tax Consultant': {
    'description': 'Tax consultants advise clients on tax planning strategies, prepare tax returns, ensure compliance with tax laws, and help minimize tax liabilities.',
    'skills': ['Tax Law Knowledge', 'Research Skills', 'Attention to Detail', 'Analytical Thinking', 'Client Communication', 'Ethics'],
    'salary_range': '$55,000 - $110,000 per year',
    'education': "Bachelor's degree in Accounting or Finance; CPA or CA preferred",
    'growth': '8% growth (Faster than average)',
    'top_companies': ['Deloitte Tax', 'PwC Tax', 'KPMG Tax', 'EY Tax', 'Tax Consulting Firms', 'Corporate Tax Departments']
},
'Audit Manager': {
    'description': 'Audit managers lead audit teams, evaluate financial records, assess internal controls, and ensure compliance with accounting standards and regulations.',
    'skills': ['Auditing Standards', 'Risk Assessment', 'Team Leadership', 'Communication', 'Analytical Skills', 'Attention to Detail', 'Ethics'],
    'salary_range': '$75,000 - $140,000 per year',
    'education': "Bachelor's degree in Accounting; CPA or CA required; 5+ years experience",
    'growth': '6% growth (Average)',
    'top_companies': ['Deloitte', 'PwC', 'KPMG', 'EY', 'Internal Audit Departments', 'Government Audit Agencies']
},
'Cost Accountant': {
    'description': 'Cost accountants analyze production costs, optimize pricing strategies, and help businesses understand their cost structures to improve profitability.',
    'skills': ['Cost Accounting', 'Manufacturing Processes', 'Budgeting', 'Variance Analysis', 'Excel', 'ERP Systems', 'Analytical Skills'],
    'salary_range': '$55,000 - $95,000 per year',
    'education': "Bachelor's degree in Accounting; CMA certification preferred",
    'growth': '5% growth (Average)',
    'top_companies': ['Manufacturing Companies', 'CMA Firms', 'Corporate Finance Departments', 'Cost Consulting Firms']
},
'Finance Manager': {
    'description': 'Finance managers oversee financial operations, prepare financial reports, develop budgets, and provide strategic financial guidance to organizations.',
    'skills': ['Financial Planning', 'Budget Management', 'Cash Flow Analysis', 'Team Leadership', 'Strategic Thinking', 'Risk Management'],
    'salary_range': '$80,000 - $150,000 per year',
    'education': "Bachelor's degree in Finance or Accounting; MBA or CFA preferred",
    'growth': '9% growth (Faster than average)',
    'top_companies': ['Corporate Finance Departments', 'Banks', 'Financial Institutions', 'Fortune 500 Companies']
},
'Chief Financial Officer (CFO)': {
    'description': 'CFOs are executive-level leaders responsible for financial strategy, risk management, financial planning, and reporting for organizations.',
    'skills': ['Strategic Leadership', 'Financial Strategy', 'Risk Management', 'Investor Relations', 'Corporate Governance', 'Decision Making'],
    'salary_range': '$150,000 - $500,000+ per year',
    'education': "Bachelor's degree in Finance or Accounting; MBA or CPA preferred; 10+ years experience",
    'growth': '6% growth (Average)',
    'top_companies': ['Public Companies', 'Large Corporations', 'Financial Institutions', 'Startups']
},
'Risk Manager': {
    'description': 'Risk managers identify, assess, and mitigate financial and operational risks to protect organizations from potential losses.',
    'skills': ['Risk Assessment', 'Data Analysis', 'Financial Modeling', 'Regulatory Knowledge', 'Problem Solving', 'Communication'],
    'salary_range': '$70,000 - $140,000 per year',
    'education': "Bachelor's degree in Finance, Economics, or Risk Management; FRM certification preferred",
    'growth': '8% growth (Faster than average)',
    'top_companies': ['Banks', 'Insurance Companies', 'Investment Firms', 'Corporate Risk Departments']
},
'Wealth Manager': {
    'description': 'Wealth managers provide financial planning and investment management services to high-net-worth individuals and families.',
    'skills': ['Investment Management', 'Financial Planning', 'Client Relationship Management', 'Tax Planning', 'Estate Planning', 'Communication'],
    'salary_range': '$70,000 - $200,000+ per year',
    'education': "Bachelor's degree in Finance; CFP or CFA preferred",
    'growth': '10% growth (Faster than average)',
    'top_companies': ['Wealth Management Firms', 'Private Banks', 'Investment Advisory Firms', 'Morgan Stanley Wealth Management']
},
'Credit Analyst': {
    'description': 'Credit analysts evaluate the creditworthiness of individuals or businesses, analyze financial data, and make recommendations on lending decisions.',
    'skills': ['Financial Analysis', 'Risk Assessment', 'Credit Scoring', 'Industry Research', 'Communication', 'Attention to Detail'],
    'salary_range': '$50,000 - $90,000 per year',
    'education': "Bachelor's degree in Finance, Economics, or Accounting",
    'growth': '7% growth (Faster than average)',
    'top_companies': ['Banks', 'Credit Unions', 'Credit Rating Agencies (Moody\'s, S&P, Fitch)', 'Corporate Credit Departments']
},
'Forensic Accountant': {
    'description': 'Forensic accountants investigate financial fraud, analyze financial evidence, and provide expert testimony in legal proceedings.',
    'skills': ['Fraud Detection', 'Data Analysis', 'Legal Knowledge', 'Interview Skills', 'Report Writing', 'Attention to Detail'],
    'salary_range': '$65,000 - $120,000 per year',
    'education': "Bachelor's degree in Accounting; Certified Fraud Examiner (CFE) preferred",
    'growth': '8% growth (Faster than average)',
    'top_companies': ['Forensic Accounting Firms', 'FBI', 'IRS', 'Law Enforcement', 'Corporate Investigation Departments']
},
'Treasury Analyst': {
    'description': 'Treasury analysts manage corporate cash flow, liquidity, investments, and financial risk to ensure optimal use of financial resources.',
    'skills': ['Cash Management', 'Liquidity Analysis', 'Financial Forecasting', 'Banking Relationships', 'Risk Management', 'Excel'],
    'salary_range': '$55,000 - $100,000 per year',
    'education': "Bachelor's degree in Finance, Accounting, or Economics; CTP preferred",
    'growth': '7% growth (Faster than average)',
    'top_companies': ['Corporate Treasury Departments', 'Banks', 'Financial Institutions']
},
'Financial Controller': {
    'description': 'Financial controllers oversee accounting operations, financial reporting, internal controls, and compliance for organizations.',
    'skills': ['Financial Reporting', 'Internal Controls', 'Team Management', 'Regulatory Compliance', 'ERP Systems', 'Analytical Skills'],
    'salary_range': '$90,000 - $160,000 per year',
    'education': "Bachelor's degree in Accounting; CPA or CA required; 7+ years experience",
    'growth': '6% growth (Average)',
    'top_companies': ['Corporate Finance Departments', 'Mid-size to Large Companies', 'Non-profit Organizations']
},
'Internal Auditor': {
    'description': 'Internal auditors evaluate internal controls, assess operational efficiency, and ensure compliance with policies and regulations within organizations.',
    'skills': ['Internal Controls', 'Risk Assessment', 'Process Evaluation', 'Communication', 'Analytical Skills', 'Ethics'],
    'salary_range': '$60,000 - $110,000 per year',
    'education': "Bachelor's degree in Accounting; CIA certification preferred",
    'growth': '7% growth (Faster than average)',
    'top_companies': ['Corporate Internal Audit Departments', 'Audit Firms', 'Government Agencies']
 },
 # Add these to your CAREER_DETAILS_DB dictionary

'Sports Director': {
    'description': 'Sports managers oversee the business operations of sports organizations, teams, or facilities. They handle contracts, budgets, marketing, and strategic planning for sports entities.',
    'skills': ['Business Management', 'Contract Negotiation', 'Budget Planning', 'Marketing Strategy', 'Leadership', 'Communication'],
    'salary_range': '$50,000 - $120,000 per year',
    'education': "Bachelor's degree in Sports Management, Business Administration, or related field; MBA preferred",
    'growth': '10% growth (Faster than average)',
    'top_companies': ['Sports Teams', 'Sports Leagues', 'Sports Facilities', 'Colleges and Universities', 'Sports Management Firms']
},
'Fitness Trainer': {
    'description': 'Fitness trainers design and lead exercise programs for individuals or groups to help clients achieve health and fitness goals. They demonstrate proper techniques and ensure safe workouts.',
    'skills': ['Fitness Assessment', 'Exercise Programming', 'Motivation', 'Communication', 'First Aid', 'Nutrition Knowledge', 'Safety Protocols'],
    'salary_range': '$35,000 - $75,000 per year',
    'education': 'High school diploma plus certification; Bachelor\'s degree in Exercise Science preferred',
    'growth': '15% growth (Much faster than average)',
    'top_companies': ['Gyms', 'Fitness Centers', 'Corporate Wellness Programs', 'Personal Training Studios', 'Hotels and Resorts']
},
'Sports Coach': {
    'description': 'Sports coaches train athletes and teams to improve their skills, performance, and competitive success. They develop practice plans, teach techniques, and strategize for competitions.',
    'skills': ['Sport-Specific Knowledge', 'Leadership', 'Communication', 'Strategy Development', 'Motivation', 'Athlete Assessment', 'Safety Protocols'],
    'salary_range': '$35,000 - $100,000+ per year',
    'education': "Bachelor's degree in Physical Education, Sports Science, or related field; Coaching certifications",
    'growth': '8% growth (Faster than average)',
    'top_companies': ['Schools', 'Colleges', 'Sports Academies', 'Professional Sports Teams', 'Club Sports', 'Sports Camps']
},
'Sports Psychologist': {
    'description': 'Sports psychologists help athletes improve mental performance, cope with pressure, overcome performance anxiety, and maintain mental health for optimal athletic achievement.',
    'skills': ['Psychology Expertise', 'Cognitive Behavioral Techniques', 'Mental Training', 'Communication', 'Stress Management', 'Performance Assessment', 'Team Dynamics'],
    'salary_range': '$60,000 - $120,000 per year',
    'education': "Doctoral degree (PhD or PsyD) in Clinical or Counseling Psychology with sports specialization; State license required",
    'growth': '12% growth (Much faster than average)',
    'top_companies': ['Professional Sports Teams', 'Sports Psychology Clinics', 'Universities', 'Olympic Training Centers', 'Private Practice']
},
'Exercise Physiologist': {
    'description': 'Exercise physiologists study how exercise affects the human body. They develop fitness programs for people with chronic conditions or injuries and conduct research on physical activity.',
    'skills': ['Physiology Knowledge', 'Fitness Assessment', 'Rehabilitation Techniques', 'Research Methods', 'Data Analysis', 'Patient Assessment'],
    'salary_range': '$45,000 - $85,000 per year',
    'education': "Bachelor's degree in Exercise Physiology or Kinesiology; Master's degree for clinical positions",
    'growth': '11% growth (Much faster than average)',
    'top_companies': ['Hospitals', 'Rehabilitation Centers', 'University Research Labs', 'Corporate Wellness Programs', 'Sports Performance Centers']
},
'Sports Nutritionist': {
    'description': 'Sports nutritionists advise athletes and active individuals on optimal nutrition for performance, recovery, and overall health. They create meal plans and educate on supplementation.',
    'skills': ['Nutrition Science', 'Diet Planning', 'Supplement Knowledge', 'Body Composition Analysis', 'Client Education', 'Research Skills'],
    'salary_range': '$45,000 - $85,000 per year',
    'education': "Bachelor's degree in Nutrition or Dietetics; Registered Dietitian (RD) certification; Sports Nutrition specialty",
    'growth': '10% growth (Faster than average)',
    'top_companies': ['Sports Teams', 'Fitness Centers', 'Hospitals', 'Sports Nutrition Companies', 'Private Practice']
},
'Athletic Director': {
    'description': 'Athletic directors oversee sports programs at schools, colleges, or universities. They manage budgets, hire coaches, schedule competitions, and ensure compliance with regulations.',
    'skills': ['Administrative Management', 'Budget Planning', 'Leadership', 'Compliance Knowledge', 'Communication', 'Strategic Planning'],
    'salary_range': '$60,000 - $150,000 per year',
    'education': "Master's degree in Sports Management, Athletic Administration, or related field",
    'growth': '6% growth (Average)',
    'top_companies': ['High Schools', 'Colleges and Universities', 'Sports Academies', 'Recreation Departments']
},
'Sports Marketing Manager': {
    'description': 'Sports marketing managers develop and execute marketing strategies to promote sports teams, events, brands, or products. They manage sponsorships, advertising, and fan engagement.',
    'skills': ['Marketing Strategy', 'Brand Management', 'Social Media Marketing', 'Sponsorship Sales', 'Event Promotion', 'Data Analytics', 'Communication'],
    'salary_range': '$55,000 - $120,000 per year',
    'education': "Bachelor's degree in Marketing, Sports Management, or Business; MBA preferred",
    'growth': '10% growth (Faster than average)',
    'top_companies': ['Sports Brands (Nike, Adidas)', 'Sports Teams', 'Broadcast Networks', 'Marketing Agencies', 'Sports Leagues']
},
'Physical Education Teacher': {
    'description': 'Physical education teachers develop and deliver fitness and sports curriculum to students at schools. They promote physical activity, teach sports skills, and encourage healthy lifestyles.',
    'skills': ['Teaching Skills', 'Curriculum Development', 'Sports Instruction', 'Classroom Management', 'Child Development', 'Communication', 'Fitness Knowledge'],
    'salary_range': '$40,000 - $75,000 per year',
    'education': "Bachelor's degree in Physical Education; Teaching license/certification",
    'growth': '5% growth (Average)',
    'top_companies': ['Public Schools', 'Private Schools', 'International Schools', 'Special Education Centers', 'Community Centers']
},
'Sports Agent': {
    'description': 'Sports agents represent professional athletes in contract negotiations, endorsements, and career management. They seek opportunities to maximize athlete earnings and brand value.',
    'skills': ['Negotiation', 'Contract Law', 'Sales', 'Networking', 'Athlete Representation', 'Business Development', 'Marketing'],
    'salary_range': '$50,000 - $500,000+ per year (commission-based)',
    'education': "Bachelor's degree in Sports Management, Business, or Law; Certification required",
    'growth': '8% growth (Faster than average)',
    'top_companies': ['Sports Agencies (CAA, WME, Wasserman)', 'Independent Representation', 'Sports Management Firms']
},
'Sports Event Coordinator': {
    'description': 'Sports event coordinators plan and execute sporting events, from local tournaments to major competitions. They manage logistics, venues, schedules, and participant coordination.',
    'skills': ['Event Planning', 'Logistics Management', 'Budgeting', 'Vendor Coordination', 'Problem Solving', 'Time Management', 'Communication'],
    'salary_range': '$40,000 - $75,000 per year',
    'education': "Bachelor's degree in Event Management, Sports Management, or Hospitality",
    'growth': '9% growth (Faster than average)',
    'top_companies': ['Event Management Companies', 'Sports Organizations', 'Convention Centers', 'Tournament Organizers']
},
'Sports Journalist': {
    'description': 'Sports journalists report on sports news, events, and stories for media outlets including TV, radio, newspapers, and digital platforms. They interview athletes and provide analysis.',
    'skills': ['Writing', 'Research', 'Interviewing', 'Broadcasting', 'Social Media', 'Sports Knowledge', 'Video Editing'],
    'salary_range': '$35,000 - $80,000 per year',
    'education': "Bachelor's degree in Journalism, Communications, or Sports Media",
    'growth': '4% growth (Average)',
    'top_companies': ['ESPN', 'Sky Sports', 'Star Sports', 'Sports Illustrated', 'The Athletic', 'Newspapers', 'Digital Media']
},
'Sports Data Analyst': {
    'description': 'Sports data analysts collect and analyze performance data to help teams, coaches, and players improve strategy and decision-making. They work with advanced statistics and analytics tools.',
    'skills': ['Data Analysis', 'Statistics', 'Programming (Python, R)', 'Database Management', 'Data Visualization', 'Sports Knowledge', 'Machine Learning'],
    'salary_range': '$55,000 - $110,000 per year',
    'education': "Bachelor's degree in Data Science, Statistics, Mathematics, or related field",
    'growth': '15% growth (Much faster than average)',
    'top_companies': ['Sports Teams', 'Analytics Companies', 'Sports Betting Firms', 'Media Companies', 'Tech Startups']
},
'Sports Facility Manager': {
    'description': 'Sports facility managers oversee the operation and maintenance of sports venues, including stadiums, arenas, fitness centers, and recreational facilities.',
    'skills': ['Facility Management', 'Budget Planning', 'Safety Compliance', 'Staff Management', 'Vendor Coordination', 'Customer Service', 'Maintenance Knowledge'],
    'salary_range': '$45,000 - $95,000 per year',
    'education': "Bachelor's degree in Facility Management, Sports Management, or Business",
    'growth': '7% growth (Faster than average)',
    'top_companies': ['Sports Stadiums', 'Fitness Centers', 'Universities', 'Recreation Departments', 'Event Venues']
},
'Personal Trainer': {
    'description': 'Personal trainers work one-on-one with clients to achieve fitness goals, providing personalized exercise programs, motivation, and accountability.',
    'skills': ['Exercise Programming', 'Motivation', 'Communication', 'Anatomy Knowledge', 'Goal Setting', 'Safety Protocols', 'Nutrition Basics'],
    'salary_range': '$40,000 - $80,000 per year',
    'education': 'High school diploma plus certification; Associate or Bachelor\'s degree in Exercise Science preferred',
    'growth': '15% growth (Much faster than average)',
    'top_companies': ['Gyms', 'Fitness Centers', 'Private Studios', 'Corporate Wellness', 'Self-employed']
},
'Group Exercise Instructor': {
    'description': 'Group exercise instructors lead fitness classes such as aerobics, spinning, yoga, Zumba, or HIIT. They create engaging workouts and motivate participants.',
    'skills': ['Fitness Knowledge', 'Music Timing', 'Class Leadership', 'Motivation', 'Safety Awareness', 'Communication', 'Choreography'],
    'salary_range': '$30,000 - $60,000 per year',
    'education': 'Certification in specific fitness format; CPR/AED certified',
    'growth': '11% growth (Faster than average)',
    'top_companies': ['Fitness Chains', 'Yoga Studios', 'Community Centers', 'Resorts', 'Corporate Fitness Centers']
},
'Sports Rehabilitator': {
    'description': 'Sports rehabilitators help athletes recover from injuries through specialized exercise programs and rehabilitation techniques to restore function and prevent re-injury.',
    'skills': ['Injury Assessment', 'Rehabilitation Techniques', 'Therapeutic Exercise', 'Manual Therapy', 'Athlete Education', 'Progress Monitoring'],
    'salary_range': '$45,000 - $85,000 per year',
    'education': "Bachelor's or Master's degree in Athletic Training, Physical Therapy, or Sports Rehabilitation; Certification required",
    'growth': '10% growth (Faster than average)',
    'top_companies': ['Sports Medicine Clinics', 'Hospitals', 'Sports Teams', 'Rehabilitation Centers', 'College Sports Programs']
 },
'Corporate Wellness Coordinator': {
    'description': 'Corporate wellness coordinators develop and manage workplace health programs to improve employee well-being, reduce healthcare costs, and increase productivity.',
    'skills': ['Wellness Programming', 'Health Education', 'Data Analysis', 'Communication', 'Event Planning', 'Budget Management', 'Health Screening'],
    'salary_range': '$45,000 - $85,000 per year',
    'education': "Bachelor's degree in Health Promotion, Exercise Science, or Public Health; Wellness certification preferred",
    'growth': '13% growth (Much faster than average)',
    'top_companies': ['Large Corporations', 'Insurance Companies', 'Tech Companies', 'Healthcare Organizations', 'Consulting Firms']
 }
}

# ==================== DEFAULT CAREER DETAILS DATABASE ====================
# This database covers ALL streams with Indian context (companies, salaries, cities)

DEFAULT_CAREER_DB = {
    # ==================== TECHNOLOGY & ENGINEERING CAREERS ====================
    "Software Engineer": {
        "description": "Software engineers design, develop, and maintain software applications for Indian IT companies, startups, and MNCs. They work on everything from mobile apps to large enterprise systems.",
        "skills": ["Programming (Python, Java, C++, JavaScript)", "Problem Solving", "Debugging", "Version Control (Git)", "Database Management (SQL, MongoDB)", "System Design", "API Development"],
        "salary_range": "₹4,00,000 - ₹30,00,000 per year (Entry: ₹3-6 LPA, Mid: ₹10-18 LPA, Senior: ₹20-35 LPA)",
        "education": "B.Tech/BE in Computer Science, BCA, MCA, B.Sc Computer Science",
        "growth": "Excellent growth in Indian IT sector - 15-20% annual salary growth with experience",
        "top_companies": ["Infosys - Bengaluru/Mysore/Pune", "TCS - Mumbai/Chennai/Bengaluru", "Wipro - Bengaluru/Hyderabad", "HCL - Noida/Chennai", "Tech Mahindra - Pune/Bengaluru", "LTIMindtree - Bengaluru/Pune", "Mphasis - Bengaluru/Pune", "Persistent Systems - Pune/Nagpur"],
        "indian_hubs": ["Bengaluru", "Hyderabad", "Pune", "Chennai", "Mumbai", "Delhi NCR", "Kolkata", "Ahmedabad"]
    },
    
    "Data Scientist": {
        "description": "Data scientists analyze complex data to help Indian organizations make better decisions using statistical methods, machine learning, and data visualization.",
        "skills": ["Python/R Programming", "Statistics & Probability", "Machine Learning", "Data Visualization (Tableau, PowerBI)", "SQL", "Big Data Tools (Hadoop, Spark)", "Deep Learning (TensorFlow, PyTorch)"],
        "salary_range": "₹8,00,000 - ₹45,00,000 per year (Entry: ₹6-10 LPA, Mid: ₹15-25 LPA, Senior: ₹28-40 LPA)",
        "education": "Master's or PhD in Data Science, Statistics, Computer Science; B.Tech with certification",
        "growth": "Very high demand - India has 30% annual growth in data science jobs",
        "top_companies": ["Mu Sigma - Bengaluru", "Fractal Analytics - Mumbai/Bengaluru", "Tiger Analytics - Chennai/Bengaluru/Hyderabad", "LatentView Analytics - Chennai/Bengaluru", "Absolutdata - Gurugram/Bengaluru", "Quantiphi - Mumbai/Bengaluru", "ZS Associates - Pune/Bengaluru/Delhi"],
        "indian_hubs": ["Bengaluru", "Mumbai", "Hyderabad", "Pune", "Chennai", "Gurugram", "Delhi NCR"]
    },
    
    "AI/ML Engineer": {
        "description": "AI/ML engineers build and deploy artificial intelligence and machine learning models for Indian businesses, healthcare, finance, and e-commerce.",
        "skills": ["Python", "TensorFlow/PyTorch/Keras", "Machine Learning Algorithms", "Deep Learning", "Mathematics & Statistics", "Data Preprocessing", "Model Deployment (Docker, Kubernetes)", "NLP", "Computer Vision"],
        "salary_range": "₹10,00,000 - ₹60,00,000 per year (Entry: ₹8-12 LPA, Mid: ₹18-30 LPA, Senior: ₹32-50 LPA)",
        "education": "Master's or PhD in AI/ML; B.Tech from top institutes with strong portfolio",
        "growth": "Fastest growing field in India - 40% annual growth",
        "top_companies": ["Infosys AI Labs - Bengaluru", "TCS AI & ML - Mumbai/Chennai", "Wipro AI - Bengaluru", "HCL AI - Noida/Chennai", "Tech Mahindra AI - Pune/Hyderabad", "Fractal AI - Mumbai/Bengaluru", "DeepTek AI - Pune", "Mad Street Den - Chennai/Bengaluru", "Uniphore - Chennai/Bengaluru/Delhi"],
        "indian_hubs": ["Bengaluru", "Hyderabad", "Pune", "Mumbai", "Chennai", "Gurugram", "Delhi NCR"]
    },
    
    "Cybersecurity Analyst": {
        "description": "Cybersecurity analysts protect Indian computer systems, networks, and data from cyber threats for corporations, banks, and government.",
        "skills": ["Network Security", "Risk Assessment", "Incident Response", "Security Tools (Firewalls, IDS/IPS)", "Cryptography", "Compliance (ISO, GDPR, IT Act)", "Penetration Testing"],
        "salary_range": "₹5,00,000 - ₹35,00,000 per year (Entry: ₹4-7 LPA, Mid: ₹10-18 LPA, Senior: ₹20-30 LPA)",
        "education": "Bachelor's in Cybersecurity, Computer Science, IT; Certifications: CEH, CISSP, CISM",
        "growth": "Critical demand - 35% growth, RBI mandates for banks",
        "top_companies": ["TCS Cybersecurity - Mumbai/Chennai", "Infosys Security - Bengaluru", "Wipro Security - Bengaluru/Chennai", "HCL Security - Noida/Chennai", "Paladion Networks - Mumbai/Bengaluru/Delhi", "Quick Heal - Pune", "Seqrite - Pune", "Lucideus - Delhi NCR", "K7 Computing - Chennai"],
        "indian_hubs": ["Bengaluru", "Mumbai", "Pune", "Chennai", "Hyderabad", "Delhi NCR", "Gurugram"]
    },
    
    "Cloud Architect": {
        "description": "Cloud architects design and manage cloud infrastructure for Indian enterprises migrating to AWS, Azure, and GCP platforms.",
        "skills": ["AWS/Azure/GCP Services", "Infrastructure as Code (Terraform)", "Cloud Security", "Networking", "Containerization (Docker, Kubernetes)", "DevOps Practices", "Cost Optimization"],
        "salary_range": "₹15,00,000 - ₹50,00,000 per year (Entry Cloud Eng: ₹6-10 LPA, Cloud Arch: ₹18-30 LPA, Senior: ₹35-50 LPA)",
        "education": "B.Tech in CS/IT, Cloud Certifications (AWS Certified Solutions Architect, Azure Solutions Architect)",
        "growth": "High demand as Indian companies move to cloud - 30% annual growth",
        "top_companies": ["Infosys Cloud - Bengaluru", "TCS Cloud - Mumbai/Chennai", "Wipro Cloud - Bengaluru/Hyderabad", "HCL Cloud - Noida", "Tech Mahindra Cloud - Pune", "LTIMindtree Cloud - Bengaluru", "CloudThat - Bengaluru/Mysore", "CtrlS - Hyderabad/Mumbai"],
        "indian_hubs": ["Bengaluru", "Hyderabad", "Pune", "Mumbai", "Chennai", "Noida", "Gurugram"]
    },
    
    "DevOps Engineer": {
        "description": "DevOps engineers bridge development and operations, automating deployment pipelines for faster software delivery in Indian tech companies.",
        "skills": ["CI/CD (Jenkins, GitLab CI, GitHub Actions)", "Docker", "Kubernetes", "Terraform/Ansible", "Monitoring (Prometheus, Grafana)", "Cloud Platforms", "Scripting (Python, Bash)"],
        "salary_range": "₹6,00,000 - ₹40,00,000 per year (Entry: ₹5-9 LPA, Mid: ₹12-22 LPA, Senior: ₹25-35 LPA)",
        "education": "B.Tech in CS/IT, DevOps certifications (AWS DevOps, Azure DevOps, CKA)",
        "growth": "Essential role in modern IT - 35% growth",
        "top_companies": ["Infosys DevOps - Bengaluru/Pune", "TCS DevOps - Mumbai/Chennai", "Wipro DevOps - Bengaluru/Hyderabad", "HCL DevOps - Noida/Chennai", "Razorpay - Bengaluru", "Flipkart - Bengaluru", "Paytm - Noida/Delhi", "Zomato - Gurugram/Bengaluru"],
        "indian_hubs": ["Bengaluru", "Pune", "Hyderabad", "Mumbai", "Chennai", "Gurugram", "Noida"]
    },
    
    # ==================== BUSINESS & FINANCE CAREERS ====================
    "Business Analyst": {
        "description": "Business analysts help Indian organizations improve processes and products through data analysis, bridging IT and business teams.",
        "skills": ["Data Analysis (Excel, SQL)", "Requirements Gathering", "Stakeholder Management", "Problem Solving", "Business Process Modeling", "Agile Methodologies", "JIRA, Confluence, Tableau"],
        "salary_range": "₹5,00,000 - ₹25,00,000 per year (Entry: ₹4-7 LPA, Mid: ₹9-15 LPA, Senior: ₹16-22 LPA)",
        "education": "Bachelor's in Business, Finance, IT, Economics; MBA preferred",
        "growth": "Steady growth - 15% CAGR in India",
        "top_companies": ["Deloitte India - Mumbai/Delhi/Bengaluru", "PwC India - Kolkata/Mumbai/Delhi", "KPMG India - Mumbai/Delhi/Bengaluru", "EY India - Mumbai/Delhi/Bengaluru", "McKinsey India - Mumbai/Delhi/Bengaluru", "Accenture India - Bengaluru/Mumbai/Pune", "Infosys Consulting - Bengaluru", "TCS BFSI - Mumbai/Chennai"],
        "indian_hubs": ["Mumbai", "Delhi NCR", "Bengaluru", "Pune", "Hyderabad", "Chennai", "Kolkata"]
    },
    
    "Investment Banker": {
        "description": "Investment bankers help Indian companies raise capital, facilitate M&A, and execute financial transactions.",
        "skills": ["Financial Modeling", "Valuation (DCF, LBO)", "Negotiation", "Deal Making", "Client Management", "Excel Advanced", "Bloomberg Terminal"],
        "salary_range": "₹12,00,000 - ₹80,00,000+ per year (Analyst: ₹10-18 LPA, Associate: ₹20-35 LPA, VP: ₹40-60 LPA, Director: ₹65-80+ LPA)",
        "education": "Bachelor's in Finance/Economics/Commerce; MBA from IIM/ISB; CFA valued",
        "growth": "Growing with Indian economy - 10-12% growth",
        "top_companies": ["Goldman Sachs India - Bengaluru/Mumbai/Hyderabad", "JP Morgan India - Mumbai/Bengaluru/Hyderabad", "Morgan Stanley India - Mumbai/Bengaluru", "Avendus Capital - Mumbai/Bengaluru/Delhi", "Kotak Investment Banking - Mumbai/Delhi/Bengaluru/Chennai", "Axis Capital - Mumbai/Delhi/Bengaluru", "ICICI Securities - Mumbai/Delhi/Bengaluru/Chennai"],
        "indian_hubs": ["Mumbai (BKC, Nariman Point)", "Bengaluru", "Delhi NCR", "Hyderabad", "Chennai"]
    },
    
    "Marketing Manager": {
        "description": "Marketing managers develop and execute marketing strategies to promote Indian products, brands, and services.",
        "skills": ["Strategic Planning", "Digital Marketing (SEO, SEM, Social Media)", "Brand Management", "Market Research", "Google Analytics", "Leadership", "Budget Management"],
        "salary_range": "₹6,00,000 - ₹35,00,000 per year (Entry: ₹4-7 LPA, Mid: ₹10-18 LPA, Senior: ₹20-30 LPA, Director: ₹35-50 LPA)",
        "education": "Bachelor's in Marketing/Business/Communications; MBA in Marketing from top B-school",
        "growth": "Strong growth - 18% CAGR in digital marketing",
        "top_companies": ["Hindustan Unilever - Mumbai", "ITC Limited - Kolkata/Bengaluru/Gurugram", "Nestlé India - Gurugram", "Britannia Industries - Bengaluru", "PepsiCo India - Gurugram/Mumbai", "Amazon India - Bengaluru/Mumbai/Delhi", "Flipkart - Bengaluru", "Reliance Retail - Mumbai", "Zomato - Gurugram", "Swiggy - Bengaluru"],
        "indian_hubs": ["Mumbai", "Delhi NCR", "Bengaluru", "Kolkata", "Chennai", "Hyderabad", "Pune"]
    },
    
    "Entrepreneur": {
        "description": "Entrepreneurs start and run their own businesses in India's thriving startup ecosystem, taking financial risks for growth.",
        "skills": ["Leadership", "Risk Taking", "Strategic Planning", "Financial Management", "Sales & Marketing", "Networking", "Problem Solving", "Team Building"],
        "salary_range": "₹5,00,000 - ₹1,00,00,000+ per year (Startup founder draw: ₹10-25 LPA early stage, Successful exits: ₹1-100 Cr+)",
        "education": "No specific degree required; IIT/IIM/BITS alumni often successful",
        "growth": "India has 3rd largest startup ecosystem - 100+ unicorns, 50,000+ startups; 15% annual growth",
        "top_companies": "Self-employed (Indian Unicorns: Flipkart, Ola, Paytm, BYJU's, Zomato, Swiggy, Razorpay, CRED, Unacademy, Meesho, Nykaa, PolicyBazaar, Delhivery)",
        "indian_hubs": ["Bengaluru", "Delhi NCR", "Mumbai", "Hyderabad", "Pune", "Chennai", "Kolkata", "Ahmedabad"]
    },
    
    # ==================== HEALTH SCIENCES CAREERS ====================
    "Doctor (MBBS)": {
        "description": "Doctors diagnose and treat medical conditions, prescribe medications, and provide healthcare to patients in Indian hospitals and clinics.",
        "skills": ["Medical Knowledge", "Diagnostic Skills", "Patient Care", "Communication", "Empathy", "Emergency Response", "Clinical Procedures"],
        "salary_range": "₹6,00,000 - ₹1,00,00,000+ per year (Junior: ₹6-9 LPA, Specialist: ₹20-40 LPA, Surgeon: ₹30-60 LPA, Consultant: ₹50 LPA - 1 Cr+)",
        "education": "MBBS (5.5 years) + MD/MS specialization (3 years) + DM/MCh super-specialization",
        "growth": "7-9% growth, high demand in tier 2/3 cities",
        "top_companies": ["AIIMS - New Delhi/Bhopal/Bhubaneswar/Jodhpur/Patna/Raipur/Rishikesh", "Apollo Hospitals - Chennai/Delhi/Hyderabad/Bengaluru/Mumbai/Kolkata", "Fortis Healthcare - Delhi NCR/Bengaluru/Mumbai/Chennai", "Max Healthcare - Delhi NCR/Punjab", "Narayana Health - Bengaluru/Kolkata/Mumbai/Delhi NCR", "Manipal Hospitals - Bengaluru/Delhi/Pune/Jaipur", "Medanta - Gurugram/Lucknow/Ranchi/Indore"],
        "indian_hubs": ["Delhi NCR", "Mumbai", "Bengaluru", "Chennai", "Hyderabad", "Kolkata", "Pune", "Ahmedabad", "Chandigarh", "Lucknow"]
    },
    
    "Nurse": {
        "description": "Nurses provide patient care, administer medications, monitor vital signs, and support doctors in Indian healthcare settings.",
        "skills": ["Patient Care", "Medical Knowledge", "Communication", "Compassion", "Critical Thinking", "Attention to Detail", "Emergency Response"],
        "salary_range": "₹2,00,000 - ₹8,00,000 per year (Staff Nurse: ₹3.5-5 LPA, Senior: ₹5-7 LPA, Overseas: ₹15-25 LPA)",
        "education": "B.Sc Nursing (4 years), GNM (3.5 years), M.Sc Nursing for advanced roles",
        "growth": "12-15% growth, high demand in India and abroad",
        "top_companies": ["Apollo Hospitals - All Major Cities", "Fortis Healthcare - Delhi NCR/Bengaluru/Mumbai", "Max Healthcare - Delhi NCR", "Narayana Health - Bengaluru/Kolkata", "Manipal Hospitals - Bengaluru/Delhi/Pune", "AIIMS - New Delhi/Others", "Government Hospitals - All State Capitals"],
        "indian_hubs": ["Delhi NCR", "Mumbai", "Bengaluru", "Chennai", "Hyderabad", "Kolkata", "Pune", "Ahmedabad", "Kochi"]
    },
    
    "Pharmacist": {
        "description": "Pharmacists dispense medications, advise patients on drug interactions, ensure safe medication use, and manage pharmacy inventory.",
        "skills": ["Pharmaceutical Knowledge", "Attention to Detail", "Patient Counseling", "Math Skills", "Regulatory Compliance", "Inventory Management"],
        "salary_range": "₹2,50,000 - ₹10,00,000 per year (Retail: ₹2-3 LPA, Hospital: ₹3-5 LPA, Manager: ₹8-10 LPA)",
        "education": "B.Pharma (4 years), D.Pharma (2 years), M.Pharma for clinical roles",
        "growth": "10% growth, pharmacy chains expansion, online pharmacies growth",
        "top_companies": ["Apollo Pharmacy - Across India", "MedPlus Health - Hyderabad/Major Cities", "Netmeds - Chennai/Bengaluru/Mumbai", "PharmEasy - Mumbai/Bengaluru/Delhi", "1mg (Tata 1mg) - Gurugram/Bengaluru/Mumbai", "Wellness Forever - Mumbai/Pune/Bengaluru"],
        "indian_hubs": ["Mumbai", "Bengaluru", "Hyderabad", "Delhi NCR", "Chennai", "Pune", "Kolkata", "Ahmedabad"]
    },
    
    "Physiotherapist": {
        "description": "Physiotherapists help patients recover from injuries, manage pain, improve mobility, and prevent disability through physical therapy.",
        "skills": ["Anatomy & Physiology", "Therapeutic Exercise", "Patient Assessment", "Manual Therapy", "Rehabilitation Planning", "Sports Injury Management"],
        "salary_range": "₹2,50,000 - ₹12,00,000 per year (Entry: ₹2.5-4 LPA, Mid: ₹4.5-7 LPA, Senior: ₹8-10 LPA, Sports Physio: ₹10-15 LPA)",
        "education": "BPT (4.5 years), MPT for specialization",
        "growth": "18-20% growth, rising sports culture, aging population",
        "top_companies": ["Apollo Hospitals - Chennai/Delhi/Hyderabad", "Fortis Healthcare - Delhi NCR/Bengaluru", "Max Healthcare - Delhi NCR", "Manipal Hospitals - Bengaluru/Delhi", "Sports Authority of India (SAI) - Delhi/Bengaluru/Patiala", "Indian Cricket Team (BCCI) - Mumbai"],
        "indian_hubs": ["Mumbai", "Delhi NCR", "Bengaluru", "Chennai", "Hyderabad", "Pune", "Kolkata", "Chandigarh"]
    },
    
    # ==================== CREATIVE ARTS CAREERS ====================
    "Graphic Designer": {
        "description": "Graphic designers create visual concepts using software to communicate ideas for Indian brands and agencies.",
        "skills": ["Adobe Creative Suite", "Typography", "Color Theory", "Layout & Composition", "Creativity", "Brand Identity", "Visual Communication"],
        "salary_range": "₹2,50,000 - ₹12,00,000 per year (Junior: ₹2.5-4 LPA, Mid: ₹4.5-8 LPA, Senior: ₹8-12 LPA)",
        "education": "Bachelor's in Graphic Design, Fine Arts, B.Des; Diploma with strong portfolio",
        "growth": "10-12% growth, digital content demand, e-commerce marketing",
        "top_companies": ["Design Agencies: Landor (Mumbai/Bengaluru)", "Interbrand (Mumbai)", "Elephant Design (Pune/Delhi)", "Tech: Flipkart (Bengaluru)", "Amazon India (Bengaluru/Hyderabad)", "Swiggy (Bengaluru)", "Media: Disney+ Hotstar (Mumbai)", "Netflix India (Mumbai)", "E-commerce: Myntra (Bengaluru)", "Nykaa (Mumbai)", "Meesho (Bengaluru)"],
        "indian_hubs": ["Mumbai", "Bengaluru", "Delhi NCR", "Pune", "Hyderabad", "Chennai", "Kolkata"]
    },
    
    "UX/UI Designer": {
        "description": "UX/UI designers create user-friendly interfaces for Indian websites and apps, focusing on user experience research and visual design.",
        "skills": ["User Research", "Wireframing (Figma, Sketch, Adobe XD)", "Usability Testing", "Interaction Design", "Information Architecture", "Design Systems"],
        "salary_range": "₹4,00,000 - ₹25,00,000 per year (Junior: ₹4-7 LPA, Mid: ₹8-15 LPA, Senior: ₹16-22 LPA, Lead: ₹24-30 LPA)",
        "education": "Bachelor's in Design (B.Des), HCI; UX Bootcamp certifications; Portfolio is key",
        "growth": "18-20% growth, explosive demand in Indian tech startups",
        "top_companies": ["Flipkart - Bengaluru", "Amazon India - Bengaluru/Hyderabad/Delhi", "Paytm - Noida/Delhi", "Razorpay - Bengaluru", "PhonePe - Bengaluru", "CRED - Bengaluru", "Swiggy - Bengaluru", "Zomato - Gurugram", "Freshworks - Chennai", "Zoho - Chennai", "Postman - Bengaluru"],
        "indian_hubs": ["Bengaluru", "Mumbai", "Delhi NCR", "Pune", "Hyderabad", "Chennai", "Ahmedabad"]
    },
    
    "Animator": {
        "description": "Animators create moving images and visual effects for Indian films, TV, games, and digital content.",
        "skills": ["Maya, Blender, After Effects", "Storyboarding", "Character Design", "Motion Graphics", "3D Modeling", "2D Animation", "Timing & Spacing"],
        "salary_range": "₹3,00,000 - ₹15,00,000 per year (Junior: ₹3-5 LPA, Mid: ₹6-10 LPA, Senior: ₹11-15 LPA)",
        "education": "Bachelor's in Animation, Fine Arts; Diploma from Arena, MAAC, Whistling Woods",
        "growth": "12-15% growth, Indian animation industry growing rapidly",
        "top_companies": ["Technicolor India - Bengaluru/Mumbai", "Dhruva Interactive - Bengaluru", "Lakshya Digital - Gurugram/Pune", "Green Gold Animation (Chhota Bheem) - Hyderabad", "Cosmos-Maya (Motu Patlu) - Mumbai", "Toonz Animation - Thiruvananthapuram", "Prime Focus (Double Negative) - Mumbai/Chennai", "Red Chillies VFX - Mumbai", "Rockstar Games India - Bengaluru", "Ubisoft India - Pune"],
        "indian_hubs": ["Mumbai", "Bengaluru", "Hyderabad", "Chennai", "Pune", "Thiruvananthapuram", "Gurugram"]
    },
    
    # ==================== EDUCATION & TRAINING CAREERS ====================
    "Teacher": {
        "description": "Teachers educate students in schools, creating lesson plans, assessing progress, and fostering learning environments.",
        "skills": ["Teaching Skills", "Lesson Planning", "Classroom Management", "Communication", "Patience", "Subject Expertise", "Assessment Design"],
        "salary_range": "₹2,50,000 - ₹8,00,000 per year (Entry: ₹2.5-4 LPA, Experienced: ₹4-6 LPA, Senior: ₹6-8 LPA, PGT: ₹7-10 LPA)",
        "education": "B.Ed (mandatory), BA/B.Sc + B.Ed, CTET/TET qualification for government schools",
        "growth": "5-7% growth, government schools expansion, private schools increasing",
        "top_companies": ["Kendriya Vidyalaya Sangathan - Across India", "Navodaya Vidyalaya Samiti - Across India", "Delhi Public Schools (DPS) - Across India", "Ryan International Schools - Across India", "Podar International Schools - Across India", "Orchids International - Across India", "State Government Schools - All States"],
        "indian_hubs": ["Delhi NCR", "Mumbai", "Bengaluru", "Chennai", "Kolkata", "Hyderabad", "Pune", "Ahmedabad", "All State Capitals"]
    },
    
    "Professor": {
        "description": "Professors teach undergraduate and graduate courses at Indian universities and colleges, conduct research, and publish academic work.",
        "skills": ["Subject Expertise", "Teaching Pedagogy", "Research Methodology", "Academic Writing", "Student Mentoring", "Public Speaking", "Curriculum Development"],
        "salary_range": "₹5,00,000 - ₹25,00,000 per year (Asst Professor: ₹5-9 LPA, Associate: ₹10-15 LPA, Professor: ₹16-22 LPA, Senior: ₹25-35 LPA)",
        "education": "MA/M.Sc + PhD + UGC-NET/JRF mandatory",
        "growth": "8-10% growth, 103 Central Universities expanding, NEP 2020 driving higher education",
        "top_companies": ["Central Universities: Delhi University, JNU, BHU, University of Hyderabad, University of Calcutta, University of Mumbai, University of Madras", "IITs and NITs (for engineering subjects)", "IIMs (for management subjects)", "Private Universities: Ashoka University, Shiv Nadar University, Azim Premji University, Symbiosis, Christ University"],
        "indian_hubs": ["Delhi NCR", "Mumbai", "Bengaluru", "Chennai", "Kolkata", "Pune", "Hyderabad", "Varanasi", "Lucknow", "Chandigarh"]
    },
    
    # ==================== MANUFACTURING & CONSTRUCTION CAREERS ====================
    "Production Manager": {
        "description": "Production managers oversee manufacturing operations, ensuring efficient production schedules and quality standards in Indian factories.",
        "skills": ["Production Planning", "Lean Manufacturing", "Process Optimization", "Quality Control", "Team Leadership", "Safety Management"],
        "salary_range": "₹6,00,000 - ₹25,00,000 per year (Production Engineer: ₹4-6 LPA, Manager: ₹8-15 LPA, Plant Manager: ₹25-35 LPA)",
        "education": "B.Tech in Mechanical/Industrial/Production Engineering, MBA in Operations preferred",
        "growth": "8-10% growth, Make in India initiative",
        "top_companies": ["Tata Motors - Pune/Mumbai/Jamshedpur", "Maruti Suzuki - Gurugram/Manesar", "Mahindra & Mahindra - Mumbai/Pune/Chennai", "Bajaj Auto - Pune/Aurangabad", "Hero MotoCorp - Gurugram/Haridwar", "Reliance Industries - Jamnagar/Vadodara/Mumbai", "Bosch India - Bengaluru/Nashik/Jaipur"],
        "indian_hubs": ["Pune", "Mumbai", "Chennai", "Ahmedabad", "Gurugram", "Bengaluru", "Jamshedpur", "Jaipur", "Indore"]
    },
    
    "Civil Engineer": {
        "description": "Civil engineers design, plan, and oversee construction projects including buildings, bridges, roads, and dams in India.",
        "skills": ["Structural Analysis", "AutoCAD & Revit", "STAAD Pro", "Project Planning", "Site Supervision", "Material Testing", "Quality Control"],
        "salary_range": "₹3,00,000 - ₹20,00,000 per year (Junior: ₹3-5 LPA, Civil Engineer: ₹5-9 LPA, Senior: ₹10-15 LPA, PM: ₹16-22 LPA)",
        "education": "B.Tech/BE in Civil Engineering, M.Tech in Structural/Construction Management",
        "growth": "8-10% growth, infrastructure boom (roads, railways, metros, smart cities)",
        "top_companies": ["Larsen & Toubro (L&T) - Mumbai/Chennai/Bengaluru", "Shapoorji Pallonji - Mumbai/Pune", "Tata Projects - Mumbai/Hyderabad/Delhi", "NCC Limited - Hyderabad/Chennai", "DLF Limited - Gurugram/Delhi", "Godrej Properties - Mumbai/Bengaluru/Pune", "Sobha Limited - Bengaluru/Chennai"],
        "indian_hubs": ["Mumbai", "Delhi NCR", "Bengaluru", "Chennai", "Hyderabad", "Pune", "Ahmedabad", "Kolkata", "Lucknow"]
    },
    
    # ==================== LAW CAREERS ====================
    "Lawyer": {
        "description": "Lawyers represent clients in court, provide legal advice, draft documents, and handle litigation or corporate legal matters in India.",
        "skills": ["Legal Research (Manupatra, SCC Online)", "Drafting", "Client Counseling", "Courtroom Advocacy", "Negotiation", "Analytical Skills", "Legal Writing"],
        "salary_range": "₹3,00,000 - ₹50,00,000+ per year (Litigation Entry: ₹2-5 LPA, Corporate Entry: ₹6-12 LPA, Senior Associate: ₹25-40 LPA, Partner: ₹50 LPA - 2 Cr+)",
        "education": "LLB (3 years) or Integrated BA-LLB/BBA-LLB (5 years) + Bar Council enrollment (AIBE)",
        "growth": "10-12% growth, corporate legal services expanding, arbitration, cyber law emerging",
        "top_companies": ["AZB & Partners - Mumbai/Delhi/Bengaluru/Pune", "Khaitan & Co - Mumbai/Delhi/Bengaluru/Kolkata", "Shardul Amarchand Mangaldas - Delhi/Mumbai/Bengaluru/Kolkata", "Cyril Amarchand Mangaldas - Mumbai/Delhi/Bengaluru/Chennai", "Trilegal - Mumbai/Delhi/Bengaluru/Hyderabad", "Tata Sons Legal - Mumbai", "Reliance Industries Legal - Mumbai"],
        "indian_hubs": ["Delhi NCR (Supreme Court)", "Mumbai (Bombay High Court)", "Bengaluru", "Chennai", "Kolkata", "Hyderabad"]
    },
    
    "Corporate Lawyer": {
        "description": "Corporate lawyers handle M&A, contracts, corporate governance, compliance, and securities law for Indian companies.",
        "skills": ["M&A and Private Equity", "Corporate Governance", "SEBI Regulations", "Contract Drafting", "Due Diligence", "Company Law", "Securities Law"],
        "salary_range": "₹8,00,000 - ₹60,00,000+ per year (Entry: ₹8-15 LPA, Mid Associate: ₹16-25 LPA, Senior: ₹26-40 LPA, Partner: ₹50 LPA - 2 Cr+)",
        "education": "LLB + Company Secretary (CS) preferred; LLM in Corporate Law valued",
        "growth": "12-14% growth, Indian M&A activity high, startup fundraising, IPO boom",
        "top_companies": ["AZB & Partners - Mumbai/Delhi/Bengaluru", "Khaitan & Co - Mumbai/Delhi/Bengaluru", "Shardul Amarchand Mangaldas - Delhi/Mumbai/Bengaluru", "Cyril Amarchand Mangaldas - Mumbai/Delhi/Bengaluru", "Tata Group Legal - Mumbai", "Reliance Legal - Mumbai", "Amazon India Legal - Bengaluru", "Flipkart Legal - Bengaluru"],
        "indian_hubs": ["Mumbai", "Delhi NCR", "Bengaluru", "Hyderabad", "Chennai", "Ahmedabad"]
    },
    
    # ==================== ENVIRONMENT & AGRICULTURE CAREERS ====================
    "Environmental Scientist": {
        "description": "Environmental scientists study and protect the environment, analyze data, and advise on environmental policies in India.",
        "skills": ["Data Analysis", "Field Sampling", "Environmental Monitoring", "GIS", "Report Writing", "Regulatory Knowledge", "Impact Assessment"],
        "salary_range": "₹3,50,000 - ₹15,00,000 per year (Entry: ₹3.5-6 LPA, Mid: ₹6-10 LPA, Senior: ₹10-15 LPA)",
        "education": "Bachelor's in Environmental Science, M.Sc Environmental Science preferred",
        "growth": "8-10% growth, climate action focus, green jobs expansion",
        "top_companies": ["TERI - New Delhi", "CSE - New Delhi", "WWF India - New Delhi", "Greenpeace India - Bengaluru", "ICAR - New Delhi", "CPCB - Delhi", "State Pollution Control Boards - All State Capitals"],
        "indian_hubs": ["Delhi NCR", "Bengaluru", "Pune", "Chennai", "Kolkata", "Hyderabad", "Dehradun"]
    },
    
    "Agricultural Engineer": {
        "description": "Agricultural engineers design farm equipment, irrigation systems, and sustainable farming solutions for Indian agriculture.",
        "skills": ["Farm Machinery Design", "Irrigation Systems", "Soil & Water Conservation", "CAD Software", "Precision Agriculture", "Post-harvest Technology"],
        "salary_range": "₹3,00,000 - ₹12,00,000 per year (Entry: ₹3-5 LPA, Engineer: ₹5-8 LPA, Senior: ₹9-12 LPA)",
        "education": "B.Tech Agricultural Engineering, M.Tech in Farm Machinery",
        "growth": "8-10% growth, PM-KUSUM scheme, farm mechanization focus",
        "top_companies": ["Mahindra & Mahindra Agri - Mumbai/Nagpur", "John Deere India - Pune/Delhi NCR", "Escorts Agri - Faridabad", "Kubota India - Delhi NCR", "Jain Irrigation - Jalgaon/Mumbai", "Netafim India - Bengaluru/Delhi"],
        "indian_hubs": ["Punjab (Ludhiana)", "Delhi NCR", "Pune", "Chennai", "Bengaluru", "Nagpur", "Ahmedabad"]
    },
    
    # ==================== MATHEMATICS & STATISTICS CAREERS ====================
    "Data Analyst": {
        "description": "Data analysts collect, process, and perform statistical analyses on data to help Indian businesses make better decisions.",
        "skills": ["SQL", "Excel Advanced", "Python/R", "Data Visualization (Tableau, PowerBI)", "Statistical Analysis", "Problem Solving"],
        "salary_range": "₹4,00,000 - ₹15,00,000 per year (Entry: ₹4-7 LPA, Analyst: ₹7-11 LPA, Senior: ₹12-15 LPA)",
        "education": "Bachelor's in Statistics, Mathematics, Economics, Computer Science",
        "growth": "15-18% growth, data-driven decision making across industries",
        "top_companies": ["Mu Sigma - Bengaluru", "Fractal Analytics - Mumbai/Bengaluru", "Tiger Analytics - Chennai/Bengaluru", "Absolutdata - Gurugram", "ZS Associates - Pune/Bengaluru"],
        "indian_hubs": ["Bengaluru", "Mumbai", "Hyderabad", "Pune", "Chennai", "Gurugram", "Delhi NCR"]
    },
    
    "Actuary": {
        "description": "Actuaries analyze financial risks for Indian insurance companies, pension funds, and financial institutions.",
        "skills": ["Probability & Statistics", "Financial Mathematics", "Risk Modeling", "Data Analysis", "Insurance Regulations", "Valuation"],
        "salary_range": "₹6,00,000 - ₹40,00,000 per year (Entry (few exams): ₹6-9 LPA, Qualified Actuary: ₹20-35 LPA, Chief Actuary: ₹40-70 LPA)",
        "education": "Actuarial Science degree + passing IFoA (UK) or IAI (India) exams (15+ exams, 6-8 years)",
        "growth": "15-18% growth, IRDAI requirement for actuaries in insurance companies",
        "top_companies": ["LIC - Mumbai/Delhi/Chennai/Kolkata", "HDFC Life - Mumbai", "ICICI Prudential - Mumbai", "SBI Life - Mumbai", "Max Life - Delhi NCR", "Bajaj Allianz - Pune", "Milliman - Mumbai/Delhi", "Mercer - Mumbai/Delhi", "Aon India - Mumbai/Delhi", "Deloitte - Mumbai/Delhi"],
        "indian_hubs": ["Mumbai", "Delhi NCR", "Chennai", "Bengaluru", "Hyderabad", "Kolkata", "Pune"]
    },
    
    # ==================== RETAIL & E-COMMERCE CAREERS ====================
    "E-commerce Manager": {
        "description": "E-commerce managers oversee online sales operations, website management, product listings, and customer experience for Indian e-commerce companies.",
        "skills": ["E-commerce Platforms (Shopify, Magento)", "Digital Marketing", "Data Analysis", "Inventory Management", "Customer Service", "SEO/SEM"],
        "salary_range": "₹5,00,000 - ₹20,00,000 per year (Entry: ₹5-8 LPA, Manager: ₹8-15 LPA, Senior: ₹15-20 LPA)",
        "education": "Bachelor's in Business, Marketing, or IT; MBA preferred",
        "growth": "15-18% growth, Indian e-commerce booming",
        "top_companies": ["Amazon India - Bengaluru/Hyderabad/Delhi NCR", "Flipkart - Bengaluru/Delhi NCR", "Myntra - Bengaluru", "Nykaa - Mumbai", "Meesho - Bengaluru", "Tata Cliq - Mumbai/Bengaluru", "Ajio - Mumbai/Bengaluru", "Reliance Retail - Mumbai"],
        "indian_hubs": ["Bengaluru", "Mumbai", "Delhi NCR", "Hyderabad", "Chennai", "Pune", "Kolkata"]
    },
    
    # ==================== TRANSPORTATION & LOGISTICS CAREERS ====================
    "Logistics Manager": {
        "description": "Logistics managers oversee supply chain and transportation operations, coordinating movement of goods efficiently.",
        "skills": ["Supply Chain Management", "Transportation Planning", "Inventory Management", "Warehouse Operations", "Vendor Negotiation", "Cost Optimization"],
        "salary_range": "₹4,00,000 - ₹20,00,000 per year (Coordinator: ₹4-7 LPA, Manager: ₹8-15 LPA, Sr Manager: ₹16-20 LPA)",
        "education": "BBA/MBA in Logistics & Supply Chain Management, B.Tech Industrial Engineering",
        "growth": "15% growth, e-commerce boom, National Logistics Policy 2022",
        "top_companies": ["Delhivery - Gurugram/Bengaluru", "Blue Dart - Mumbai", "DTDC - Bengaluru", "Amazon Logistics - Bengaluru/Hyderabad", "Flipkart Ekart - Bengaluru", "Rivigo - Gurugram", "Xpressbees - Pune", "TCI - Gurugram", "Gati - Hyderabad"],
        "indian_hubs": ["Mumbai", "Delhi NCR", "Bengaluru", "Chennai", "Hyderabad", "Pune", "Ahmedabad", "Kolkata"]
    },
    
    # ==================== HOSPITALITY & TOURISM CAREERS ====================
    "Hotel Manager": {
        "description": "Hotel managers oversee hotel operations, manage staff, ensure guest satisfaction, and drive revenue growth for Indian hotel chains.",
        "skills": ["Hotel Operations", "Staff Management", "Guest Relations", "Revenue Management", "Budgeting", "Sales & Marketing", "PMS Software"],
        "salary_range": "₹3,00,000 - ₹25,00,000 per year (Asst Manager: ₹3-5 LPA, Manager: ₹6-12 LPA, GM: ₹15-25 LPA)",
        "education": "BBA in Hotel Management, BHMCT, Diploma in Hotel Management, MBA in Hospitality",
        "growth": "12-15% growth, domestic tourism boom, medical tourism growth",
        "top_companies": ["Taj Hotels - Across India", "Oberoi Hotels - Delhi/Mumbai/Bengaluru", "ITC Hotels - Across India", "Marriott India - Across India", "Hyatt India - Across India", "Leela Palaces - Mumbai/Delhi/Bengaluru/Goa/Jaipur/Chennai", "Lemon Tree Hotels - Across 50+ cities"],
        "indian_hubs": ["Mumbai", "Delhi NCR", "Bengaluru", "Goa", "Jaipur", "Chennai", "Hyderabad", "Kolkata", "Pune", "Ahmedabad", "Udaipur", "Agra"]
    },
    
    # ==================== SPORTS & FITNESS CAREERS ====================
    "Sports Manager": {
        "description": "Sports managers oversee sports organizations, teams, facilities, and events, handling operations, budgets, and marketing.",
        "skills": ["Sports Management", "Event Planning", "Marketing", "Budget Management", "Team Leadership", "Sponsorship Sales", "Athlete Relations"],
        "salary_range": "₹4,00,000 - ₹20,00,000 per year (Entry: ₹4-7 LPA, Manager: ₹8-14 LPA, Director: ₹15-20 LPA)",
        "education": "BBA in Sports Management, MBA in Sports Management, Diploma in Sports Administration",
        "growth": "12-15% growth, Indian sports leagues expansion (IPL, ISL, PKL)",
        "top_companies": ["BCCI - Mumbai", "IPL Teams - Across India", "ISL Teams - Across India", "Pro Kabaddi Teams - Across India", "Sports Authority of India - Delhi/Bengaluru/Patiala", "IOA - New Delhi"],
        "indian_hubs": ["Mumbai", "Delhi NCR", "Bengaluru", "Chennai", "Kolkata", "Hyderabad", "Ahmedabad", "Pune"]
    },
    
    "Fitness Trainer": {
        "description": "Fitness trainers design and lead exercise programs for individuals or groups to help clients achieve health and fitness goals.",
        "skills": ["Fitness Assessment", "Exercise Programming", "Motivation", "Communication", "First Aid", "Nutrition Knowledge", "Safety Protocols"],
        "salary_range": "₹2,50,000 - ₹10,00,000 per year (Entry: ₹2.5-4 LPA, Experienced: ₹4-7 LPA, Master Trainer: ₹8-10 LPA)",
        "education": "High school + Certification (ACE, NASM, ACSM); Bachelor's in Exercise Science preferred",
        "growth": "15-18% growth, fitness awareness increasing, gym culture boom",
        "top_companies": ["Cult.fit - Bengaluru/Delhi/Mumbai/Chennai/Hyderabad/Pune", "Gold's Gym - Across India", "Anytime Fitness - Across 30+ cities", "Talwalkars - Across India", "Equinox - Mumbai/Delhi/Bengaluru"],
        "indian_hubs": ["Bengaluru", "Mumbai", "Delhi NCR", "Pune", "Hyderabad", "Chennai", "Kolkata", "Ahmedabad"]
    },
    
    # ==================== SPACE & EMERGING TECH CAREERS ====================
    "Space Scientist": {
        "description": "Space scientists conduct research on space, celestial bodies, and space missions at Indian space organizations.",
        "skills": ["Space Science", "Orbital Mechanics", "Data Analysis", "Remote Sensing", "Satellite Technology", "Research Methods"],
        "salary_range": "₹8,00,000 - ₹30,00,000 per year (Scientist: ₹8-15 LPA, Senior: ₹16-25 LPA, Distinguished: ₹26-35 LPA)",
        "education": "M.Sc in Physics/Astrophysics/Space Science + PhD, B.Tech Aerospace Engineering",
        "growth": "8-10% growth, India's space program expansion (Gaganyaan, Chandrayaan, Aditya-L1)",
        "top_companies": ["ISRO - Bengaluru/Thiruvananthapuram/Ahmedabad/Sriharikota/Hyderabad", "PRL - Ahmedabad", "IIA - Bengaluru", "IUCAA - Pune", "TIFR - Mumbai", "Physical Research Laboratory - Ahmedabad"],
        "indian_hubs": ["Bengaluru", "Ahmedabad", "Thiruvananthapuram", "Pune", "Mumbai", "Sriharikota", "Hyderabad"]
    },
    
    # ==================== ACCOUNTING & FINANCE CAREERS ====================
    "Chartered Accountant (CA)": {
        "description": "Chartered Accountants manage financial accounts, conduct audits, provide tax advice, and ensure financial compliance for Indian organizations.",
        "skills": ["Accounting Standards (Ind AS)", "Taxation (Direct & Indirect)", "Auditing & Assurance", "Financial Reporting", "Corporate Law", "Risk Management"],
        "salary_range": "₹6,00,000 - ₹50,00,000 per year (Entry: ₹6-9 LPA, Mid: ₹12-20 LPA, Senior: ₹22-35 LPA, Partner: ₹40 LPA - 1 Cr+)",
        "education": "CA from ICAI - Requires clearing 3 levels (Foundation, Intermediate, Final) + 3 years articleship",
        "growth": "10-12% growth, statutory requirement for Indian companies",
        "top_companies": ["Deloitte India - Mumbai/Delhi/Bengaluru/Hyderabad", "PwC India - Kolkata/Mumbai/Delhi/Bengaluru", "KPMG India - Mumbai/Delhi/Bengaluru/Chennai", "EY India - Mumbai/Delhi/Bengaluru/Chennai", "BDO India - Mumbai/Delhi/Bengaluru", "Grant Thornton India - Mumbai/Delhi/Bengaluru", "Tata Sons - Mumbai", "Reliance Industries - Mumbai"],
        "indian_hubs": ["Mumbai", "Delhi NCR", "Bengaluru", "Kolkata", "Chennai", "Hyderabad", "Pune", "Ahmedabad"]
    },
    
    "Financial Analyst": {
        "description": "Financial analysts evaluate investment opportunities, analyze financial data, and provide recommendations for Indian businesses and investors.",
        "skills": ["Financial Modeling", "Financial Statement Analysis", "Valuation Techniques", "Excel Advanced", "Investment Research", "Ratio Analysis", "Report Writing"],
        "salary_range": "₹5,00,000 - ₹28,00,000 per year (Entry: ₹4-7 LPA, Analyst: ₹8-14 LPA, Senior: ₹15-22 LPA)",
        "education": "Bachelor's in Finance/Economics/Accounting; CFA/CPA/CA preferred",
        "growth": "12-14% growth, high demand in banking and investment firms",
        "top_companies": ["Goldman Sachs - Bengaluru/Mumbai", "JP Morgan - Mumbai/Bengaluru", "Morgan Stanley - Mumbai/Bengaluru", "HDFC Bank - Mumbai", "ICICI Bank - Mumbai", "Kotak Securities - Mumbai", "Motilal Oswal - Mumbai", "Zerodha - Bengaluru", "Groww - Bengaluru", "Deloitte - Mumbai/Delhi/Bengaluru"],
        "indian_hubs": ["Mumbai", "Bengaluru", "Delhi NCR", "Chennai", "Hyderabad", "Pune", "Kolkata"]
    }
}

def get_career_details(career_name):
    """Get detailed information about a specific career from the database"""
    # Try exact match
    if career_name in DEFAULT_CAREER_DB:
        return DEFAULT_CAREER_DB[career_name]
    
    # Try partial match
    for key in DEFAULT_CAREER_DB:
        if key.lower() in career_name.lower() or career_name.lower() in key.lower():
            return DEFAULT_CAREER_DB[key]
    
    # Return default career info if not found
    return {
        "description": f"{career_name} offers excellent career opportunities in the Indian job market with good growth potential.",
        "skills": ["Communication", "Problem Solving", "Team Collaboration", "Time Management", "Customer Focus", "Adaptability"],
        "technical_skills": ["Domain Knowledge", "Practical Application", "Quality Standards", "Safety Awareness", "Documentation", "Industry Tools"],
        "software_skills": ["MS Office Suite", "Email Communication", "Industry Software", "Data Entry Tools", "Project Management Basics", "CRM Systems"],
        "career_skills": ["Professionalism", "Work Ethic", "Teamwork", "Problem Solving", "Time Management", "Continuous Learning"],
        "salary_range": "₹3,00,000 - ₹12,00,000 per year (varies by experience and location)",
        "education": "Bachelor's degree in relevant field; Professional certifications valued",
        "growth": "Positive growth outlook - 8-10% CAGR in most industries",
        "top_companies": ["Leading companies in this sector across Mumbai, Delhi NCR, Bengaluru, Chennai, Hyderabad, Pune, Kolkata, Ahmedabad"],
        "hiring_cities": ["Mumbai", "Delhi NCR", "Bengaluru", "Chennai", "Hyderabad", "Pune", "Kolkata", "Ahmedabad"]
    }
# ==========================================

def get_user_type_from_grade(grade):
    """Determine user type based on grade/year"""
    school_grades = ["9th", "10th", "11th", "12th"]
    college_grades = ["1st Year College", "2nd Year College", "3rd Year College", "4th Year College"]
    
    if grade in school_grades:
        return "school"
    elif grade in college_grades:
        return "college"
    else:
        return "school"

def generate_html_report():
    """Generate HTML report for printing"""
    cat = st.session_state.categories_data.get(st.session_state.selected_stream, {})
    stream_details = get_stream_details(st.session_state.selected_stream, st.session_state.user_type)
    
    if not stream_details:
        stream_details = {
            'name': cat.get('name', 'Selected Stream'),
            'icon': cat.get('icon', '📚'),
            'description': f'{cat.get("name", "This stream")} offers excellent career opportunities in various fields.',
            'careers': ['Career opportunities in this field', 'Professional roles in industry', 'Research and development positions', 'Leadership and management roles'],
            'subjects': ['Core Subjects', 'Specialized Courses', 'Practical Training', 'Industry Knowledge'],
            'skills': ['Critical Thinking', 'Problem Solving', 'Communication', 'Teamwork', 'Leadership'],
            'future_scope': 'Excellent growth opportunities in this field with competitive compensation packages',
            'top_companies': ['Leading Companies', 'Industry Leaders', 'Multinational Corporations', 'Government Organizations'],
            'education_path': 'Bachelor\'s degree, Master\'s degree, Professional certifications, Doctoral programs',
            'certifications': ['Professional Certification', 'Industry Recognition', 'Specialized Training', 'Advanced Diploma']
        }
    
    # Format careers for HTML
    careers_html = ''.join([f'<div class="career-item">💼 {career}</div>' for career in stream_details.get('careers', [])])
    
    html_content = f"""
    <!DOCTYPE html>
    <html>
    <head>
        <title>Career Report - {st.session_state.student_name}</title>
        <meta charset="UTF-8">
        <style>
            body {{
                font-family: Arial, sans-serif;
                margin: 40px;
                line-height: 1.6;
                color: #333;
            }}
            .header {{
                text-align: center;
                margin-bottom: 30px;
                border-bottom: 2px solid #E67E22;
                padding-bottom: 20px;
            }}
            h1 {{ color: #D35400; }}
            h2 {{ color: #2E7D32; margin-top: 20px; }}
            .section {{
                margin-bottom: 30px;
                page-break-inside: avoid;
            }}
            .info-box {{
                background: #FFF8F0;
                padding: 15px;
                border-radius: 10px;
                margin: 10px 0;
            }}
            .career-item {{
                background: #E8F5E9;
                padding: 10px;
                margin: 10px 0;
                border-radius: 8px;
            }}
            .footer {{
                text-align: center;
                margin-top: 40px;
                padding-top: 20px;
                border-top: 1px solid #ddd;
                font-size: 12px;
                color: #666;
            }}
        </style>
    </head>
    <body>
        <div class="header">
            <h1>CoActions Career Counselling Report</h1>
            <p>Prepared for: {st.session_state.student_name}</p>
            <p>Date: {datetime.now().strftime('%Y-%m-%d')}</p>
        </div>
        
        <div class="section">
            <h2>Student Information</h2>
            <div class="info-box">
                <strong>Name:</strong> {st.session_state.student_name}<br>
                <strong>Age:</strong> {st.session_state.student_age}<br>
                <strong>Institution:</strong> {st.session_state.student_institution}<br>
                <strong>Grade/Year:</strong> {st.session_state.student_grade}<br>
                <strong>Assessment Type:</strong> {'School Student' if st.session_state.user_type == 'school' else 'College Student'} Pathway
            </div>
        </div>
        
        <div class="section">
            <h2>Selected Stream</h2>
            <div class="info-box">
                <div style="font-size:2rem;">{stream_details['icon']}</div>
                <strong>{stream_details['name']}</strong><br>
                <strong>Match Score:</strong> {cat.get('score', 0):.1f}%
            </div>
        </div>
        
        <div class="section">
            <h2>About this Stream</h2>
            <p>{stream_details['description']}</p>
        </div>
        
        <div class="section">
            <h2>Top Career Paths</h2>
            {careers_html}
        </div>
        
        <div class="section">
            <h2>Key Subjects to Focus</h2>
            <ul>
                {''.join([f'<li>{subject}</li>' for subject in stream_details.get('subjects', [])])}
            </ul>
        </div>
        
        <div class="section">
            <h2>Skills to Develop</h2>
            <ul>
                {''.join([f'<li>{skill}</li>' for skill in stream_details.get('skills', [])])}
            </ul>
        </div>
        
        <div class="section">
            <h2>Future Scope</h2>
            <p>{stream_details.get('future_scope', 'Excellent growth opportunities')}</p>
        </div>
        
        <div class="section">
            <h2>Top Companies Hiring</h2>
            <ul>
                {''.join([f'<li>{company}</li>' for company in stream_details.get('top_companies', [])])}
            </ul>
        </div>
        
        <div class="section">
            <h2>Recommended Education Path</h2>
            <p>{stream_details.get('education_path', 'Various educational pathways available')}</p>
        </div>
        
        <div class="section">
            <h2>Valuable Certifications</h2>
            <ul>
                {''.join([f'<li>{cert}</li>' for cert in stream_details.get('certifications', [])])}
            </ul>
        </div>
        
        <div class="footer">
            <p>Thank you for using CoActions Career Counselling Tool!</p>
            <p>We wish you the best in your career journey!</p>
        </div>
    </body>
    </html>
    """
    return html_content

# Header with menu
def show_header():
    col1, col2 = st.columns([2, 1])
    with col1:
        st.markdown('<div class="app-title">CoActions</div>', unsafe_allow_html=True)
    with col2:
        menu_col1, menu_col2, menu_col3 = st.columns(3)
        with menu_col1:
            if st.button("🏠 Home", key="menu_home", use_container_width=True):
                # Reset all session state for home
                for key in list(st.session_state.keys()):
                    if key not in ['page', 'show_about', 'show_contact']:
                        del st.session_state[key]
                st.session_state.page = 'welcome'
                st.session_state.show_about = False
                st.session_state.show_contact = False
                st.rerun()
        with menu_col2:
            if st.button("📖 About", key="menu_about", use_container_width=True):
                st.session_state.show_about = True
                st.session_state.show_contact = False
        with menu_col3:
            if st.button("📞 Contact", key="menu_contact", use_container_width=True):
                st.session_state.show_contact = True
                st.session_state.show_about = False

def show_welcome():
    show_header()
    
    if st.session_state.show_about:
        st.markdown('<div class="main-card">', unsafe_allow_html=True)
        st.markdown('<h1 class="welcome-heading">📖 About CoActions</h1>', unsafe_allow_html=True)
        st.markdown("""
        <div style="background:#FFF8F0; border-radius:20px; padding:1.5rem;">
            <p>🌟 <strong>CoActions</strong> is a professional career guidance platform.</p>
            <p>🎯 We help students discover their ideal career path through personalized assessments.</p>
            <p>📊 Analyzing responses across 18+ career categories to provide accurate recommendations.</p>
            <p>💡 Our AI-powered tool helps identify your strengths, interests, and potential career paths.</p>
            <p>🏆 Trusted by thousands of students to make informed career decisions.</p>
        </div>
        """, unsafe_allow_html=True)
        if st.button("← Back to Home", key="back_to_home_about"):
            st.session_state.show_about = False
            st.rerun()
        st.markdown('</div>', unsafe_allow_html=True)
        return
    
    if st.session_state.show_contact:
        st.markdown('<div class="main-card">', unsafe_allow_html=True)
        st.markdown('<h1 class="welcome-heading">📞 Contact Us</h1>', unsafe_allow_html=True)
        st.markdown("""
        <div style="background:#FFF8F0; border-radius:20px; padding:1.5rem;">
            <p>📧 <strong>Email:</strong> elevatea0200@gmail.com</p>
            <p>🌐 <strong>Website:</strong> www.coactions.com</p>
            <p>💬 <strong>Support:</strong> Mon-Fri, 9AM-6PM</p>
            <p>📱 <strong>Phone:</strong> +91 12345 67890</p>
            <p>📍 <strong>Address:</strong> Career Guidance Center, Main Street, City</p>
        </div>
        """, unsafe_allow_html=True)
        if st.button("← Back to Home", key="back_to_home_contact"):
            st.session_state.show_contact = False
            st.rerun()
        st.markdown('</div>', unsafe_allow_html=True)
        return
    
    st.markdown('<div class="main-card">', unsafe_allow_html=True)
    st.markdown('<div class="deco-icon">🎓✨🚀</div>', unsafe_allow_html=True)
    st.markdown('<h1 class="welcome-heading">Welcome to the Career Counselling Tool</h1>', unsafe_allow_html=True)
    st.markdown('<p class="welcome-subheading">Discover Your Perfect Career Path with Personalized Guidance</p>', unsafe_allow_html=True)
    st.markdown('<hr>', unsafe_allow_html=True)
    
    st.markdown('<h3 class="section-title">📝 Student Information</h3>', unsafe_allow_html=True)

    st.markdown("""
        <style>    
          /* For all select/dropdown elements */
          select, .stSelectbox select, [data-baseweb="select"] {
             color: black !important;
             background-color: white !important;
            }

          /* For all option items */
          option, [role="option"] {
             color: black !important;
             background-color: white !important;
            }

          /* For Streamlit selectbox specifically */
          .stSelectbox > div > div {
              color: black !important;
              background-color: white !important;
            }

          .stSelectbox [data-baseweb="select"] span {
             color: black !important;
            }
        </style>
        """, unsafe_allow_html=True)

    col1, col2 = st.columns(2)
    with col1:
        student_name = st.text_input("Full Name *", placeholder="Enter your full name", key="welcome_name")
        student_age = st.number_input("Age", min_value=10, max_value=100, step=1, key="welcome_age")
        student_city = st.text_input("City *", placeholder="Enter your city", key="welcome_city")
    with col2:
        student_institution = st.text_input("School/College/Institute", placeholder="Enter your institution", key="welcome_institution")
        student_grade = st.selectbox("Current Grade/Year *", 
                                      ["Select Grade", "9th", "10th", "11th", "12th", "1st Year College", "2nd Year College", "3rd Year College", "4th Year College"],
                                      key="welcome_grade")
        states_list = [
                  "Select State",
                  "Andhra Pradesh", "Arunachal Pradesh", "Assam", "Bihar", "Chhattisgarh", "Goa", "Gujarat", "Haryana", "Himachal Pradesh", "Jharkhand",
                  "Karnataka", "Kerala", "Madhya Pradesh", "Maharashtra", "Manipur", "Meghalaya", "Mizoram", "Nagaland", "Odisha", "Punjab",
                  "Rajasthan", "Sikkim", "Tamil Nadu", "Telangana", "Tripura","Uttar Pradesh", "Uttarakhand", "West Bengal", "Delhi"
            ]

        student_state = st.selectbox(
               "State *",
               states_list,
               key="welcome_state"
           )
    
    st.markdown('<hr>', unsafe_allow_html=True)
    
    # Define grade lists
    school_grades_list = ["9th", "10th", "11th", "12th"]
    college_grades_list = ["1st Year College", "2nd Year College", "3rd Year College", "4th Year College"]
    
    if st.button("🚀 Start Your Career Journey", type="primary", use_container_width=True, key="start_journey"):
        if student_name and student_grade != "Select Grade" and student_city and student_state:
            st.session_state.student_name = student_name
            st.session_state.student_age = student_age
            st.session_state.student_city = student_city
            st.session_state.student_state = student_state
            st.session_state.student_institution = student_institution
            st.session_state.student_grade = student_grade
            
            if student_grade in school_grades_list:
                st.session_state.user_type = "school"
            elif student_grade in college_grades_list:
                st.session_state.user_type = "college"
            else:
                st.session_state.user_type = "school"
            
            st.session_state.page = 'load_assessment'
            st.rerun()
        elif not student_name:
            st.warning("Please enter your name")
        elif not student_city:
            st.warning("Please enter your city")
        elif student_state == "Select State":
            st.warning("Please select your state")
        elif student_grade == "Select Grade":
            st.warning("Please select your grade/year")
    
    st.markdown('</div>', unsafe_allow_html=True)

# Load Assessment Page
def show_load_assessment():
    with st.spinner("Loading your personalized assessment..."):
        # Load appropriate JSON file based on user type
        if st.session_state.user_type == 'school':
            json_file = 'school_questions.json'
        else:
            json_file = 'college_questions.json'
        
        data = load_json_file(json_file)
        
        if data:
            questions, categories = extract_questions_from_json(data)
            st.session_state.questions_list = questions
            st.session_state.categories_data = categories
            st.session_state.responses = {}
            st.session_state.current_page = 0
            st.session_state.selected_stream = None
            st.session_state.recommended_categories = []
            st.session_state.page = 'assessment'
            st.rerun()
        else:
            st.error(f"{json_file} not found. Please make sure the file exists.")
            if st.button("Go Back"):
                st.session_state.page = 'welcome'
                st.rerun()

# Assessment Page - 10 questions per page
def show_assessment():
    show_header()
    st.markdown('<div class="main-card">', unsafe_allow_html=True)
    
    # Show user type indicator
    user_type_display = "School Student" if st.session_state.user_type == 'school' else "College Student"
    st.markdown(f'<div class="user-type-indicator">🎓 {user_type_display} Pathway</div>', unsafe_allow_html=True)
    
    if not st.session_state.questions_list:
        st.error("No questions loaded. Please go back and try again.")
        if st.button("Go Back"):
            st.session_state.page = 'welcome'
            st.rerun()
        st.markdown('</div>', unsafe_allow_html=True)
        return
    
    total_questions = len(st.session_state.questions_list)
    questions_per_page = 10
    total_pages = (total_questions + questions_per_page - 1) // questions_per_page
    current_page = st.session_state.current_page
    start_idx = current_page * questions_per_page
    end_idx = min(start_idx + questions_per_page, total_questions)
    page_questions = st.session_state.questions_list[start_idx:end_idx]
    
    st.markdown(f'<h1 class="welcome-heading" style="font-size:1.8rem;">Career Assessment</h1>', unsafe_allow_html=True)
    st.markdown(f'<p class="sub-message" style="font-size:1.1rem;">Rate each statement honestly to get accurate career recommendations</p>', unsafe_allow_html=True)
    
    # Page counter
    st.markdown(f'<div class="page-counter">📄 Page {current_page + 1} of {total_pages}</div>', unsafe_allow_html=True)
    
    # Display questions for current page
    for i, q in enumerate(page_questions):
        question_number = start_idx + i + 1
        st.markdown(f"""
        <div style="background: #FEF9F0; border-radius: 20px; padding: 1.2rem; margin: 1rem 0; border-left: 5px solid #E67E22; box-shadow: 0 2px 8px rgba(0,0,0,0.05);">
            <div style="font-weight: 700; color: #2E7D32; margin-bottom: 1rem; font-size: 1.2rem;">{question_number}. {q['text']}</div>
            <p style="color: #1565C0; font-size: 0.85rem; margin-bottom: 0.5rem;">Category: {q['category_name']}</p>
        </div>
        """, unsafe_allow_html=True)
        
        # Radio button with NO default selection (index=None)
        rating = st.radio(
            "Select your answer:",
            options=[1, 2, 3, 4, 5],
            format_func=lambda x: {1: "1 - Strongly Disagree", 2: "2 - Disagree", 3: "3 - Neutral", 4: "4 - Agree", 5: "5 - Strongly Agree"}[x],
            horizontal=True,
            key=f"q_{q['id']}_{question_number}",
            index=None  # This prevents any default selection
        )
        
        # Only store if user made a selection
        if rating is not None:
            st.session_state.responses[q['id']] = rating
        
        st.markdown("<br>", unsafe_allow_html=True)
    
    # Calculate answered questions count
    answered_count = sum(1 for q in st.session_state.questions_list[:end_idx] 
                         if st.session_state.responses.get(q['id']) is not None)
    progress = answered_count / total_questions if total_questions > 0 else 0
    st.progress(progress)
    st.markdown(f'<p class="progress-text" style="font-size:0.9rem;">📊 Progress: {answered_count}/{total_questions} questions answered ({int(progress*100)}%)</p>', unsafe_allow_html=True)
    
    # Navigation buttons
    col1, col2, col3 = st.columns([1, 2, 1])
    with col1:
        if current_page > 0:
            if st.button("← Previous Page", key="career_prev_page"):
                st.session_state.current_page -= 1
                st.rerun()
    
    with col3:
        # Check if all questions on current page are answered
        current_page_answered = all(
            st.session_state.responses.get(q['id']) is not None 
            for q in page_questions
        )
        
        if end_idx < total_questions:
            if current_page_answered:
                if st.button("Next Page →", key="career_next_page", type="primary"):
                    st.session_state.current_page += 1
                    st.rerun()
            else:
                # Show disabled button with warning
                st.button("Next Page →", key="career_next_page_disabled", disabled=True)
                st.warning(f"⚠️ Please answer all {len(page_questions)} questions on this page")
        else:
            # Last page - check if all questions are answered
            all_answered = all(
                st.session_state.responses.get(q['id']) is not None 
                for q in st.session_state.questions_list
            )
            if all_answered:
                if st.button("Submit & Get Results", type="primary", key="submit_career_results"):
                    # Calculate career assessment results
                    st.session_state.categories_data, st.session_state.recommended_categories = calculate_results(
                        st.session_state.responses, st.session_state.questions_list, st.session_state.categories_data
                    )
                    # Go to personality choice (OPTIONAL assessment)
                    st.session_state.page = 'personality_choice'
                    st.rerun()
            else:
                unanswered = total_questions - answered_count
                st.button("Submit & Get Results", key="submit_career_results_disabled", disabled=True)
                st.warning(f"⚠️ Please answer {unanswered} more question(s) before submitting")
    
    st.markdown('</div>', unsafe_allow_html=True)

def show_personality_choice():
    show_header()
    st.markdown('<div class="main-card">', unsafe_allow_html=True)
    
    st.markdown(f'''
    <div class="student-info-card">
        👋 Welcome, <strong>{st.session_state.student_name}</strong><br>
        📍 {st.session_state.student_city} | 🎂 Age: {st.session_state.student_age} | 📚 {st.session_state.student_grade}
    </div>
    ''', unsafe_allow_html=True)
    
    st.markdown('<h1 class="welcome-heading" style="font-size:1.8rem;">🎭 Optional: Personality Assessment</h1>', unsafe_allow_html=True)
    st.markdown('<p class="welcome-subheading">⚠️ <strong>Note: Your career assessment is already complete. This is optional.</strong></p>', unsafe_allow_html=True)
    
    # Add Back button to go to career assessment
    col_back1, col_back2, col_back3 = st.columns([1, 2, 1])
    with col_back1:
        if st.button("←Back   ", key="back_to_career_assessment", use_container_width=True):
            st.session_state.page = 'assessment'
            st.rerun()
    
    st.markdown("<br>", unsafe_allow_html=True)
    
    # ============ DETAILS SHOWN DIRECTLY (NO EXPANDER) ============
    st.markdown("""
    <div style="background: #E8F5E9; border-radius: 16px; padding: 1rem; margin: 1rem 0; border-left: 5px solid #1565C0;">
        <strong style="color: #1565C0; font-size: 1.1rem;">🔍 What does the personality assessment include?</strong><br><br>
        The personality assessment helps identify your learning style by evaluating:
        <ul>
            <li><strong>Learning Preferences</strong>: How you learn best (visual, auditory, reading/writing, kinesthetic)</li>
            <li><strong>Work Style</strong>: Whether you prefer independent work, teamwork, or a mix</li>
            <li><strong>Problem-Solving Approach</strong>: How you tackle challenges and new problems</li>
            <li><strong>Communication Style</strong>: Your preferred way of expressing ideas</li>
            <li><strong>Study Habits</strong>: Effective learning strategies for your personality type</li>
        </ul>
        Based on your responses, we'll provide personalized study tips and career suggestions!
    </div>
    """, unsafe_allow_html=True)
    
    st.markdown("<br>", unsafe_allow_html=True)
    
    # Display assessment options
    st.markdown('<p style="text-align: center; font-size: 1.1rem; font-weight: 500;">Choose an option below:</p>', unsafe_allow_html=True)
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown('''
        <div class="user-card" style="height: 100%; min-height: 350px; display: flex; flex-direction: column; justify-content: space-between;">
            <div>
                <div class="user-icon">📝</div>
                <h3>Take Personality Assessment</h3>
                <p>Complete the personality assessment to discover your learning style and get personalized study tips.</p>
                <p style="margin-top:10px; font-size:0.8rem; color:#1E88E5;">⏱️ Takes about 10-15 minutes</p>
                <p style="font-size:0.8rem; color:#1E88E5;">📊 25 questions</p>
                <p style="margin-top:10px; font-size:0.8rem; color:#1565C0;">✨ Get personalized insights</p>
            </div>
            <div style="margin-top: 15px;">
                <div class="stButton" style="width: 100%;"></div>
            </div>
        </div>
        ''', unsafe_allow_html=True)
        
        if st.button("✅ Yes, Take Personality Assessment", key="take_personality_btn", use_container_width=True):
            st.session_state.personality_questions = get_personality_questions(st.session_state.user_type)
            st.session_state.personality_responses = {}
            st.session_state.personality_current_page = 0
            st.session_state.personality_completed = False
            st.session_state.page = 'personality_assessment'
            st.rerun()
    
    with col2:
        st.markdown('''
        <div class="user-card" style="height: 100%; min-height: 350px; display: flex; flex-direction: column; justify-content: space-between;">
            <div>
                <div class="user-icon">⏭️</div>
                <h3>Skip Personality Assessment</h3>
                <p>Skip the personality test and go directly to your career stream comparison.</p>
                <p style="margin-top:10px; font-size:0.8rem; color:#1E88E5;">⚡ Continue directly</p>
                <p style="font-size:0.8rem; color:#1E88E5;">📊 View your career recommendations</p>
                <p style="margin-top:10px; font-size:0.8rem; color:#1565C0;">🎯 Your career assessment results are ready!</p>
            </div>
            <div style="margin-top: 15px;">
                <div class="stButton" style="width: 100%;"></div>
            </div>
        </div>
        ''', unsafe_allow_html=True)
        
        if st.button("⏭️ Skip Personality Assessment", key="skip_personality_btn", use_container_width=True):
            st.session_state.page = 'stream_comparison'
            st.rerun()
    
    st.markdown('</div>', unsafe_allow_html=True)

def show_personality_assessment():
    # Add Home button only at the top
    col_home, col_spacer = st.columns([1, 11])
    with col_home:
        if st.button("🏠 Home", key="personality_home", use_container_width=True):
            # Reset to welcome page
            for key in list(st.session_state.keys()):
                if key not in ['page']:
                    del st.session_state[key]
            st.session_state.page = 'welcome'
            st.rerun()
    
    st.markdown('<div class="main-card">', unsafe_allow_html=True)
    
    if not st.session_state.personality_questions:
        st.session_state.personality_questions = get_personality_questions(st.session_state.user_type)
    
    questions_per_page = 10
    total_questions = len(st.session_state.personality_questions)
    total_pages = (total_questions + questions_per_page - 1) // questions_per_page
    current_page = st.session_state.personality_current_page
    start_idx = current_page * questions_per_page
    end_idx = min(start_idx + questions_per_page, total_questions)
    page_questions = st.session_state.personality_questions[start_idx:end_idx]
    
    st.markdown(f'<h1 class="welcome-heading" style="font-size:1.5rem;">🧠 Personality Assessment</h1>', unsafe_allow_html=True)
    st.markdown(f'<p class="sub-message">Page {current_page + 1} of {total_pages} • Discover your learning style</p>', unsafe_allow_html=True)
    
    for i, q in enumerate(page_questions):
        q_index = start_idx + i
        st.markdown(f"""
        <div class="question-card">
            <div class="question-text">{q_index + 1}. {q['text']}</div>
        </div>
        """, unsafe_allow_html=True)
        
        # Get current value from session state if exists
        current_value = st.session_state.personality_responses.get(q['id'], None)
        
        # Radio button with NO default selection (index=None)
        answer = st.radio(
            "Select your answer:",
            options=q['options'],
            horizontal=True,
            key=f"personality_q_{q['id']}_{q_index}",
            index=None  # This removes the default pointer - no option pre-selected
        )
        
        # Only store if user made a selection
        if answer is not None:
            st.session_state.personality_responses[q['id']] = answer
        
        st.markdown("<br>", unsafe_allow_html=True)
    
    # Calculate progress based on answered questions
    answered_count = sum(1 for q in st.session_state.personality_questions[:end_idx] 
                         if st.session_state.personality_responses.get(q['id']) is not None)
    progress = answered_count / total_questions if total_questions > 0 else 0
    st.progress(progress)
    st.markdown(f'<p class="progress-text">📊 Progress: {answered_count}/{total_questions} questions answered ({int(progress*100)}%)</p>', unsafe_allow_html=True)
    
    # Navigation buttons
    col1, col2, col3 = st.columns([1, 2, 1])
    with col1:
        if current_page > 0:
            if st.button("← Previous Page", use_container_width=True):
                st.session_state.personality_current_page -= 1
                st.rerun()
    
    with col3:
        # Check if all questions on current page are answered
        current_page_answered = all(
            st.session_state.personality_responses.get(q['id']) is not None 
            for q in page_questions
        )
        
        if end_idx < total_questions:
            if current_page_answered:
                if st.button("Next Page →", type="primary", use_container_width=True):
                    st.session_state.personality_current_page += 1
                    st.rerun()
            else:
                st.button("Next Page →", type="primary", use_container_width=True, disabled=True)
                st.warning(f"⚠️ Please answer all {len(page_questions)} questions on this page")
        else:
            # Last page - check if all questions are answered
            all_answered = all(
                st.session_state.personality_responses.get(q['id']) is not None 
                for q in st.session_state.personality_questions
            )
            if all_answered:
                if st.button("Submit & See Results", type="primary", use_container_width=True):
                    # Filter out None values before analyzing
                    valid_responses = {k: v for k, v in st.session_state.personality_responses.items() if v is not None}
                    st.session_state.personality_pathway = analyze_personality_pathway(
                        valid_responses, st.session_state.user_type
                    )
                    st.session_state.personality_completed = True
                    st.session_state.page = 'personality_result'
                    st.rerun()
            else:
                unanswered = total_questions - answered_count
                st.button("Submit & See Results", type="primary", use_container_width=True, disabled=True)
                st.warning(f"⚠️ Please answer {unanswered} more question(s) before submitting")
    
    # Skip button with full width
    st.markdown("---")
    col_skip1, col_skip2, col_skip3 = st.columns([1, 2, 1])
    with col_skip2:
        if st.button("⏭️ Skip for Now", use_container_width=True):
            st.session_state.personality_skipped = True
            st.session_state.page = 'stream_comparison'
            st.rerun()
    
    st.markdown('</div>', unsafe_allow_html=True)

def show_personality_result():
    show_header()
    st.markdown('<div class="main-card">', unsafe_allow_html=True)
    
    if st.session_state.personality_pathway:
        pathway = st.session_state.personality_pathway
        
        st.markdown(f"""
        <div class="stream-detail-card">
            <div style="text-align:center;">
                <div style="font-size:3rem;">{pathway['icon']}</div>
                <h1 style="color:#D35400; margin:0.5rem 0;">{pathway['title']}</h1>
                <div style="background:#FFF3E0; display:inline-block; padding:0.3rem 1rem; border-radius:20px; margin:0.5rem 0;">
                    {pathway['match_percentage']}% Match
                </div>
            </div>
        </div>
        """, unsafe_allow_html=True)
        
        st.markdown(f"<p>{pathway['description']}</p>", unsafe_allow_html=True)
        
        col1, col2 = st.columns(2)
        with col1:
            st.markdown("**✨ Your Key Strengths:**")
            for strength in pathway.get('strengths', []):
                st.markdown(f"- {strength}")
            
            st.markdown("**💼 Recommended Careers:**")
            for career in pathway.get('careers', [])[:5]:
                st.markdown(f"- {career}")
        
        with col2:
            st.markdown("**📚 Study Tips for You:**")
            for tip in pathway.get('study_tips', []):
                st.markdown(f"- {tip}")
            
            st.markdown("**🏢 Ideal Work Environment:**")
            for env in pathway.get('work_environment', []):
                st.markdown(f"- {env}")
        
        st.markdown("<hr>", unsafe_allow_html=True)
        
        col1, col2 = st.columns(2)
        with col1:
            if st.button("← Back to Personality Test", use_container_width=True):
                st.session_state.page = 'personality_assessment'
                st.rerun()
        with col2:
            if st.button("Continue to Stream Comparison →", type="primary", use_container_width=True):
                st.session_state.page = 'stream_comparison'
                st.rerun()
    
    st.markdown('</div>', unsafe_allow_html=True)

# ==================== STREAM COMPARISON TABLE ====================
def show_stream_comparison():
    st.markdown('<div class="main-card">', unsafe_allow_html=True)
    
    st.markdown('<h1 class="welcome-heading" style="font-size:1.8rem;">📊 Your Career Stream Recommendations</h1>', unsafe_allow_html=True)
    st.markdown('<p class="sub-message">Based on your assessment answers, your top recommended streams are shown first. Click on any career name to learn more!</p>', unsafe_allow_html=True)
    
    # Get user's recommended streams with their scores
    user_recommended_streams = []
    if st.session_state.recommended_categories:
        for cat_id in st.session_state.recommended_categories[:3]:  # Top 3 only
            cat = st.session_state.categories_data.get(cat_id, {})
            score = cat.get('score', 0)
            
            # Get stream details for better display
            stream_details = get_stream_details(cat_id, st.session_state.user_type)
            if stream_details:
                stream_name = stream_details['name']
                stream_icon = stream_details['icon']
            else:
                stream_name = cat.get('name', 'Unknown Stream')
                stream_icon = cat.get('icon', '📚')
            
            user_recommended_streams.append({
                'id': cat_id,
                'score': score,
                'name': stream_name,
                'icon': stream_icon,
                'stream_details': stream_details
            })
    
    # Define all streams data (your complete list)
    all_streams_data = [
        {"icon": "💻", "id": "tech_engineering", "name": "Technology & Engineering", "category_name": "Technology & Engineering",
         "careers": [
             ("Software Engineer", "https://www.tcs.com/careers/software-engineer"),
             ("Data Scientist", "https://www.datascience.org.in"),
             ("AI/ML Engineer", "https://indiaai.gov.in")
         ],
         "skills": ["Problem Solving", "Logical Thinking", "Programming Languages"],
         "future": "High demand in IT industry, AI, Machine Learning, Data Science",
         "resources": [
             ("TCS Careers", "https://www.tcs.com/careers"),
             ("NASSCOM", "https://www.nasscom.in"),
             ("AICTE", "https://www.aicte-india.org")
         ]},
        
        {"icon": "📊", "id": "business_finance", "name": "Business & Finance", "category_name": "Business, Finance & Management",
         "careers": [
             ("Business Analyst", "https://www.iiba.org"),
             ("Investment Banker", "https://www.nseindia.com"),
             ("Marketing Manager", "https://www.indiabschool.net")
         ],
         "skills": ["Leadership", "Analytical Thinking", "Communication"],
         "future": "Corporate sector, Banking, Consulting, Entrepreneurship",
         "resources": [
             ("ICAI", "https://www.icai.org"),
             ("NSE India", "https://www.nseindia.com"),
             ("IIMB", "https://www.iimb.ac.in")
         ]},
        
        {"icon": "🏥", "id": "health_sciences", "name": "Health & Life Sciences", "category_name": "Health & Life Sciences",
         "careers": [
             ("Specialized Doctor", "https://www.nmc.org.in"),
             ("Healthcare Administrator", "https://www.indiannursingcouncil.org"),
             ("Pharmacist", "https://www.pci.nic.in")
         ],
         "skills": ["Empathy", "Attention to Detail", "Communication"],
         "future": "Healthcare sector, Research opportunities, Clinical practice",
         "resources": [
             ("NMC", "https://www.nmc.org.in"),
             ("ICMR", "https://www.icmr.gov.in"),
             ("AIIMS", "https://www.aiims.edu")
         ]},
        
        {"icon": "🎨", "id": "creative_arts", "name": "Creative Arts, Design & Media", "category_name": "Creative Arts, Design & Media",
         "careers": [
             ("Graphic Designer", "https://www.adobe.com/in/creativecloud/careers.html"),
             ("UX/UI Designer", "https://www.interaction-design.org"),
             ("Animator", "https://www.toonz.co.in")
         ],
         "skills": ["Creativity", "Visual Thinking", "Communication"],
         "future": "Design agencies, Gaming industry, Media, Entertainment",
         "resources": [
             ("Adobe Careers", "https://www.adobe.com/in/careers.html"),
             ("NIFT", "https://www.nift.ac.in"),
             ("NID", "https://www.nid.edu")
         ]},
        
        {"icon": "🏭", "id": "manufacturing", "name": "Manufacturing & Industrial Production", "category_name": "Manufacturing & Industrial Production",
         "careers": [
             ("Production Manager", "https://www.cii.in"),
             ("Quality Control Engineer", "https://www.iso.org"),
             ("Manufacturing Engineer", "https://www.sme.org")
         ],
         "skills": ["Process Optimization", "Quality Control", "Project Management"],
         "future": "Manufacturing sector, Automotive industry, Pharmaceuticals",
         "resources": [
             ("CII", "https://www.cii.in"),
             ("Make in India", "https://www.makeinindia.com"),
             ("DPIIT", "https://www.dipp.gov.in")
         ]},
        
        {"icon": "🏗️", "id": "construction", "name": "Construction", "category_name": "Construction & Civil Engineering",
         "careers": [
             ("Civil Engineer", "https://www.ice.org.uk"),
             ("Construction Manager", "https://www.cic.org.in"),
             ("Project Manager", "https://www.pmi.org")
         ],
         "skills": ["Project Management", "Blueprint Reading", "Cost Estimation"],
         "future": "Construction industry, Infrastructure projects, Real estate",
         "resources": [
             ("CIC", "https://www.cic.org.in"),
             ("NHAI", "https://www.nhai.gov.in"),
             ("CPWD", "https://www.cpwd.gov.in")
         ]},
        
        {"icon": "🌾", "id": "agriculture", "name": "Environment, Agriculture & Earth Sciences", "category_name": "Environment, Agriculture & Earth Sciences",
         "careers": [
             ("Agricultural Engineer", "https://www.icar.org.in"),
             ("Food Technologist", "https://www.cftri.res.in"),
             ("Agribusiness Manager", "https://www.manage.gov.in")
         ],
         "skills": ["Research Skills", "Data Analysis", "Problem Solving"],
         "future": "Agritech industry, Food processing, Agricultural research",
         "resources": [
             ("ICAR", "https://www.icar.org.in"),
             ("IARI", "https://www.iari.res.in"),
             ("MANAGE", "https://www.manage.gov.in")
         ]},
        
        {"icon": "📐", "id": "mathematics", "name": "Mathematics & Statistics", "category_name": "Mathematics & Statistics",
         "careers": [
             ("Data Scientist", "https://www.isical.ac.in"),
             ("Actuary", "https://www.actuariesindia.org"),
             ("Statistician", "https://www.mospi.gov.in")
         ],
         "skills": ["Analytical Thinking", "Problem Solving", "Logical Reasoning"],
         "future": "Finance, Insurance, Tech industry, Research, Education",
         "resources": [
             ("ISI Kolkata", "https://www.isical.ac.in"),
             ("IMSc Chennai", "https://www.imsc.res.in"),
             ("CMI", "https://www.cmi.ac.in")
         ]},
        
        {"icon": "⚛️", "id": "physics", "name": "Physics", "category_name": "Physics & Astronomy",
         "careers": [
             ("Research Scientist", "https://www.isro.gov.in"),
             ("Astrophysicist", "https://www.iiap.res.in"),
             ("Nuclear Engineer", "https://www.barc.gov.in")
         ],
         "skills": ["Scientific Reasoning", "Experimental Design", "Data Analysis"],
         "future": "Research institutions, Space agencies, Tech industry",
         "resources": [
             ("ISRO", "https://www.isro.gov.in"),
             ("IISc", "https://www.iisc.ac.in"),
             ("TIFR", "https://www.tifr.res.in")
         ]},
        
        {"icon": "🧪", "id": "chemistry", "name": "Chemistry", "category_name": "Chemistry & Chemical Sciences",
         "careers": [
             ("Chemist", "https://www.iscbangalore.com"),
             ("Pharmaceutical Scientist", "https://www.cdsco.gov.in"),
             ("Materials Scientist", "https://www.iisc.ac.in")
         ],
         "skills": ["Laboratory Skills", "Analytical Thinking", "Attention to Detail"],
         "future": "Pharmaceutical industry, Materials science, Environmental",
         "resources": [
             ("CSIR", "https://www.csir.res.in"),
             ("CDSCO", "https://www.cdsco.gov.in"),
             ("IISc", "https://www.iisc.ac.in")
         ]},
        
        {"icon": "🧬", "id": "biology", "name": "Biology", "category_name": "Biology & Life Sciences",
         "careers": [
             ("Biologist", "https://www.ncbs.res.in"),
             ("Geneticist", "https://www.ccmb.res.in"),
             ("Microbiologist", "https://www.amiindia.org")
         ],
         "skills": ["Laboratory Techniques", "Observation Skills", "Research Methods"],
         "future": "Biotechnology companies, Environmental agencies",
         "resources": [
             ("NCBS", "https://www.ncbs.res.in"),
             ("CCMB", "https://www.ccmb.res.in"),
             ("DBT India", "https://dbtindia.gov.in")
         ]},
        
        {"icon": "🎭", "id": "arts_humanities", "name": "Arts & Humanities", "category_name": "Arts & Humanities",
         "careers": [
             ("Professor", "https://www.ugc.ac.in"),
             ("Journalist", "https://www.presscouncil.nic.in"),
             ("Writer/Author", "https://www.sahitya-akademi.gov.in")
         ],
         "skills": ["Critical Thinking", "Communication", "Research Skills"],
         "future": "Education, Publishing, Media, Research, Government",
         "resources": [
             ("UGC", "https://www.ugc.ac.in"),
             ("NCERT", "https://www.ncert.nic.in"),
             ("JNU", "https://www.jnu.ac.in")
         ]},
        
        {"icon": "⚖️", "id": "law", "name": "Law", "category_name": "Law & Legal Studies",
         "careers": [
             ("Lawyer", "https://www.barcouncilofindia.org"),
             ("Judge", "https://www.sci.gov.in"),
             ("Corporate Lawyer", "https://www.mca.gov.in")
         ],
         "skills": ["Critical Thinking", "Argumentation", "Research Skills"],
         "future": "Legal practice, Corporate legal departments, Government",
         "resources": [
             ("BCI", "https://www.barcouncilofindia.org"),
             ("Supreme Court", "https://www.sci.gov.in"),
             ("NLU Delhi", "https://www.nludelhi.ac.in")
         ]},
        
        {"icon": "💰", "id": "commerce", "name": "Commerce", "category_name": "Commerce & Accounting",
         "careers": [
             ("Chartered Accountant", "https://www.icai.org"),
             ("Company Secretary", "https://www.icsi.edu"),
             ("Cost Accountant", "https://www.icmai.in")
         ],
         "skills": ["Numerical Ability", "Analytical Thinking", "Attention to Detail"],
         "future": "Banking, Financial services, Corporate accounting",
         "resources": [
             ("ICAI", "https://www.icai.org"),
             ("ICSI", "https://www.icsi.edu"),
             ("ICMAI", "https://www.icmai.in")
         ]},
        
        {"icon": "📈", "id": "economics", "name": "Economics", "category_name": "Economics",
         "careers": [
             ("Economist", "https://www.rbi.org.in"),
             ("Policy Analyst", "https://www.niti.gov.in"),
             ("Financial Analyst", "https://www.sebi.gov.in")
         ],
         "skills": ["Analytical Thinking", "Statistical Analysis", "Research Skills"],
         "future": "Government agencies, Central banks, Financial institutions",
         "resources": [
             ("RBI", "https://www.rbi.org.in"),
             ("NITI Aayog", "https://www.niti.gov.in"),
             ("SEBI", "https://www.sebi.gov.in")
         ]},
        
        {"icon": "🧠", "id": "psychology", "name": "Psychology", "category_name": "Psychology",
         "careers": [
             ("Clinical Psychologist", "https://www.rciindia.in"),
             ("Counseling Psychologist", "https://www.iccp.org.in"),
             ("School Psychologist", "https://www.apsi.org.in")
         ],
         "skills": ["Empathy", "Active Listening", "Communication"],
         "future": "Hospitals, Schools, Corporate sector, Research",
         "resources": [
             ("RCI", "https://www.rciindia.in"),
             ("NIMHANS", "https://www.nimhans.ac.in"),
             ("APSI", "https://www.apsi.org.in")
         ]},
        
        {"icon": "🤝", "id": "social_work", "name": "Social Work", "category_name": "Social Work",
         "careers": [
             ("Social Worker", "https://www.tiss.edu"),
             ("Community Organizer", "https://www.nirmalaniketan.com"),
             ("Child Welfare Specialist", "https://www.ncpcr.gov.in")
         ],
         "skills": ["Empathy", "Communication", "Problem Solving"],
         "future": "NGOs, Government welfare departments, Hospitals, Schools",
         "resources": [
             ("TISS", "https://www.tiss.edu"),
             ("NCPCR", "https://www.ncpcr.gov.in"),
             ("UNICEF India", "https://www.unicef.org/india")
         ]},
        
        {"icon": "🛒", "id": "retail_ecommerce", "name": "Retail & E-commerce", "category_name": "Retail & E-commerce",
         "careers": [
             ("E-commerce Manager", "https://www.amazon.jobs"),
             ("Digital Marketing Specialist", "https://skillshop.withgoogle.com"),
             ("Supply Chain Analyst", "https://www.cscmp.org")
         ],
         "skills": ["Digital Marketing", "Data Analysis", "Customer Service"],
         "future": "E-commerce boom, Online retail growth, Digital transformation",
         "resources": [
             ("Amazon Careers", "https://www.amazon.jobs"),
             ("Flipkart Careers", "https://www.flipkartcareers.com"),
             ("Shopify", "https://www.shopify.com")
         ]},
        
        {"icon": "🏨", "id": "service_hospitality", "name": "Services, Hospitality & Public Safety", "category_name": "Services, Hospitality & Public Safety",
         "careers": [
             ("Hotel Manager", "https://www.ihm.net.in"),
             ("Event Manager", "https://www.eventfaqs.com"),
             ("Police Officer", "https://www.upsc.gov.in")
         ],
         "skills": ["Customer Service", "Communication", "Crisis Management"],
         "future": "Hospitality, Tourism, Public Safety, Events",
         "resources": [
             ("IHM", "https://www.ihm.net.in"),
             ("Tourism India", "https://www.tourism.gov.in"),
             ("UPSC", "https://www.upsc.gov.in")
         ]},
        
        {"icon": "⚡", "id": "energy_utilities", "name": "Energy & Utilities", "category_name": "Energy & Utilities",
         "careers": [
             ("Power Plant Engineer", "https://www.ntpc.co.in"),
             ("Solar Project Manager", "https://www.mnre.gov.in"),
             ("Energy Analyst", "https://www.beeindia.gov.in")
         ],
         "skills": ["Technical Skills", "Project Management", "Safety Compliance"],
         "future": "Renewable energy, Smart grids, Green hydrogen",
         "resources": [
             ("NTPC", "https://www.ntpc.co.in"),
             ("MNRE", "https://www.mnre.gov.in"),
             ("BEE", "https://www.beeindia.gov.in")
         ]},
        
        {"icon": "🚗", "id": "transportation", "name": "Transportation & Mobility", "category_name": "Transportation & Mobility",
         "careers": [
             ("Logistics Manager", "https://www.delhivery.com/careers"),
             ("Supply Chain Analyst", "https://www.cscmp.org"),
             ("EV Engineer", "https://www.fame-india.gov.in")
         ],
         "skills": ["Logistics", "Supply Chain", "Route Planning"],
         "future": "EV revolution, Last-mile delivery, Hyperloop",
         "resources": [
             ("Delhivery", "https://www.delhivery.com"),
             ("NHAI", "https://www.nhai.gov.in"),
             ("FAME India", "https://www.fame-india.gov.in")
         ]},

        {"icon": "⚽", "id": "sports_fitness", "name": "Sports & Fitness", "category_name": "Sports & Fitness Industry",
         "careers": [
             ("Sports Manager", "https://www.iisports.com"),
             ("Fitness Trainer", "https://www.acefitness.org"),
             ("Sports Psychologist", "https://www.apsi.org.in")
         ],
         "skills": ["Leadership", "Communication", "Physical Training"],
         "future": "Sports industry growth, Fitness awareness, Sports management",
         "resources": [
             ("SAI", "https://sportsauthorityofindia.nic.in"),
             ("BCCI", "https://www.bcci.tv"),
             ("NIS Patiala", "https://www.nispatiala.com")
          ]},

        {"icon": "🚀", "id": "space_technology", "name": "Space & Technology", "category_name": "Space & Emerging Technologies",
         "careers": [
             ("Aerospace Engineer", "https://www.isro.gov.in"),
             ("Satellite Engineer", "https://www.isro.gov.in"),
             ("Space Scientist", "https://www.isro.gov.in")
         ],
         "skills": ["Aerospace Engineering", "Satellite Technology", "Space Research"],
         "future": "Space exploration, Satellite launches, Space research",
         "resources": [
             ("ISRO", "https://www.isro.gov.in"),
             ("NASA", "https://www.nasa.gov"),
             ("SpaceX", "https://www.spacex.com")
         ]},

        {"icon": "🌍", "id": "environmental_science", "name": "Environmental Science", "category_name": "Environment, Agriculture & Earth Sciences",
         "careers": [
             ("Environmental Scientist", "https://www.teriin.org"),
             ("Climate Change Analyst", "https://www.cseindia.org"),
             ("Conservation Scientist", "https://www.wii.gov.in")
         ],
         "skills": ["Research Skills", "Data Analysis", "Field Work"],
         "future": "Climate action, Sustainable development, Green jobs",
         "resources": [
             ("TERI", "https://www.teriin.org"),
             ("CSE", "https://www.cseindia.org"),
             ("WWF India", "https://www.wwfindia.org")
         ]},
        
        {"icon": "📊", "id": "accounting_finance", "name": "Accounting & Finance", "category_name": "Accounting & Finance",
         "careers": [
             ("Chartered Accountant", "https://www.icai.org"),
             ("Financial Analyst", "https://www.nseindia.com"),
             ("Audit Manager", "https://www.icai.org")
         ],
         "skills": ["Numerical Ability", "Analytical Thinking", "Attention to Detail"],
         "future": "Banking, Financial services, Corporate accounting",
         "resources": [
             ("ICAI", "https://www.icai.org"),
             ("ICSI", "https://www.icsi.edu"),
             ("NSE", "https://www.nseindia.com")
         ]}
    ]
    
    # ============ DISPLAY TOP 3 RECOMMENDED STREAMS ============
    if user_recommended_streams:
        st.markdown("## 🏆 Your Top Recommended Streams")
        st.markdown("*Based on your assessment answers, these streams match your interests the best!*")
        st.markdown("---")
        
        # Sort top streams by score (highest first)
        user_recommended_streams.sort(key=lambda x: x['score'], reverse=True)
        
        for i, stream_data in enumerate(user_recommended_streams):
            stream = stream_data['stream_details']
            match_score = stream_data['score']
            stream_id = stream_data['id']
            
            # Get careers from stream details or use default
            careers = []
            if stream:
                careers = stream.get('careers', [
                    f"Career opportunity in {stream_data['name']}",
                    f"Professional role in {stream_data['name']}",
                    f"Research position in {stream_data['name']}"
                ])
            else:
                careers = [f"Career opportunity in {stream_data['name']}", "Professional roles in industry"]
            
            # Format careers as clickable links (only first 3)
            career_links_html = ""
            for career in careers[:3]:
                if isinstance(career, tuple):
                    career_name, career_url = career
                    career_links_html += f'<a href="{career_url}" target="_blank" style="color: #1E88E5; text-decoration: none; display: block; margin: 5px 0; font-weight: 500;">• {career_name} →</a>'
                else:
                    career_links_html += f'<div style="margin: 5px 0;">• {career}</div>'
            
            # Get resources
            resources = []
            if stream:
                resources = stream.get('resources', [
                    ("Career Resources", "#"),
                    ("Professional Organizations", "#"),
                    ("Further Learning", "#")
                ])
            else:
                resources = [("Career Resources", "#"), ("Professional Organizations", "#")]
            
            resource_buttons_html = ""
            for res_name, res_url in resources[:3]:
                resource_buttons_html += f'<a href="{res_url}" target="_blank" style="display: inline-block; background: #E8F5E9; color: #2E7D32; padding: 5px 12px; border-radius: 20px; text-decoration: none; margin: 5px 8px 5px 0; font-size: 0.8rem; font-weight: 600;">📚 {res_name}</a>'
            
            # Get skills
            skills = stream.get('skills', ["Problem Solving", "Communication", "Teamwork"]) if stream else ["Problem Solving", "Communication", "Teamwork"]
            
            # Get future scope
            future_scope = stream.get('future_scope', "Good growth opportunities in this field") if stream else "Good growth opportunities"
            
            # Display stream card with match badge (special highlighted style for top 3)
            st.markdown(f"""
            <div style="background: linear-gradient(135deg, #E8F5E9, #FFF8F0); border-radius: 20px; padding: 1.5rem; margin-bottom: 1.5rem; box-shadow: 0 4px 15px rgba(0,0,0,0.1); border-left: 8px solid #2E7D32;">
                <div style="display: flex; justify-content: space-between; align-items: center; flex-wrap: wrap;">
                    <div style="font-size: 1.8rem; display: flex; align-items: center; gap: 15px;">
                        <span>{stream_data['icon']}</span>
                        <strong style="color: #1E88E5; font-size: 1.5rem;">{stream_data['name']}</strong>
                    </div>
                    <div style="background: #2E7D32; color: white; padding: 6px 18px; border-radius: 30px; font-size: 1.1rem; font-weight: 700;">
                        🎯 {match_score:.1f}% Match
                    </div>
                </div>
            </div>
            """, unsafe_allow_html=True)
            
            # Display stream details
            st.markdown(f"""
            <div style="background: white; border-radius: 16px; padding: 1.2rem; margin-bottom: 1rem; box-shadow: 0 2px 8px rgba(0,0,0,0.05);">
                <table style="width: 100%; border-collapse: collapse;">
                    <tr>
                        <td style="width: 25%; vertical-align: top;">
                            <strong>💼 Top Careers (Click to learn more):</strong><br>
                            {career_links_html}
                        </td>
                        <td style="width: 25%; vertical-align: top;">
                            <strong>✨ Key Skills:</strong><br>
                            {''.join([f'• {s}<br>' for s in skills[:5]])}
                        </td>
                        <td style="width: 25%; vertical-align: top;">
                            <strong>🚀 Future Scope:</strong><br>
                            {future_scope}
                        </td>
                        <td style="width: 25%; vertical-align: top;">
                            <strong>📚 Learning Resources:</strong><br>
                            {resource_buttons_html}
                        </td>
                    </tr>
                </table>
            </div>
            """, unsafe_allow_html=True)
    
    # ============ DISPLAY OTHER STREAMS ============
    # Get IDs of top recommended streams
    recommended_ids = [rec['id'] for rec in user_recommended_streams] if user_recommended_streams else []
    
    # Filter out top streams from all streams
    other_streams = [s for s in all_streams_data if s['id'] not in recommended_ids]
    
    if other_streams:
        st.markdown("## 📚 Explore Other Career Streams")
        st.markdown("*You may also explore these streams for alternative career paths*")
        st.markdown("---")
        
        for stream in other_streams:
            career_links_html = ""
            for career_name, career_url in stream['careers']:
                career_links_html += f'<a href="{career_url}" target="_blank" style="color: #1E88E5; text-decoration: none; display: block; margin: 5px 0; font-weight: 500;">• {career_name} →</a>'
            
            resource_buttons_html = ""
            for res_name, res_url in stream['resources']:
                resource_buttons_html += f'<a href="{res_url}" target="_blank" style="display: inline-block; background: #E8F5E9; color: #2E7D32; padding: 5px 12px; border-radius: 20px; text-decoration: none; margin: 5px 8px 5px 0; font-size: 0.8rem; font-weight: 600;">📚 {res_name}</a>'
            
            st.markdown(f"""
            <div style="background: white; border-radius: 16px; padding: 1.2rem; margin-bottom: 1rem; box-shadow: 0 2px 8px rgba(0,0,0,0.05); border-left: 3px solid #ccc;">
                <div style="font-size: 1.3rem; font-weight: 700; color: #1E88E5; margin-bottom: 12px;">
                    {stream['icon']} {stream['name']}
                </div>
                <table style="width: 100%; border-collapse: collapse;">
                    <tr>
                        <td style="width: 25%; vertical-align: top;">
                            <strong>💼 Top Careers:</strong><br>
                            {career_links_html}
                        </td>
                        <td style="width: 25%; vertical-align: top;">
                            <strong>✨ Key Skills:</strong><br>
                            {''.join([f'• {s}<br>' for s in stream['skills'][:4]])}
                        </td>
                        <td style="width: 25%; vertical-align: top;">
                            <strong>🚀 Future Scope:</strong><br>
                            {stream['future'][:120]}...
                        </td>
                        <td style="width: 25%; vertical-align: top;">
                            <strong>📚 Resources:</strong><br>
                            {resource_buttons_html}
                        </td>
                    </tr>
                </table>
            </div>
            """, unsafe_allow_html=True)
    
    st.markdown("---")
    st.markdown("💡 **Tip:** Click on any blue career name above to open official career information websites. Green buttons provide additional learning resources.")
    
    # Navigation buttons
    col1, col2 = st.columns(2)
    with col1:
        if st.session_state.personality_completed:
            if st.button("← Back to Personality Results", use_container_width=True):
                st.session_state.page = 'personality_result'
                st.rerun()
        else:
            if st.button("← Back to Assessment", use_container_width=True):
                st.session_state.page = 'assessment'
                st.rerun()
    with col2:
        if st.button("Continue to Stream Selection →", type="primary", use_container_width=True):
            st.session_state.page = 'stream_selection'
            st.rerun()
    
    st.markdown('</div>', unsafe_allow_html=True)

def show_stream_selection():
    show_header()
    st.markdown('<div class="main-card">', unsafe_allow_html=True)
    
    st.markdown(f'<h1 class="welcome-heading" style="font-size:1.5rem;">Hello {st.session_state.student_name}!</h1>', unsafe_allow_html=True)
    st.markdown('<p class="sub-message">Based on your assessment, here are your top recommended streams. Select one to learn more!</p>', unsafe_allow_html=True)
    
    if st.session_state.recommended_categories and len(st.session_state.recommended_categories) >= 1:
        # Show top 3 streams in columns
        cols = st.columns(3)
        
        for i, cat_id in enumerate(st.session_state.recommended_categories[:3]):
            cat = st.session_state.categories_data.get(cat_id, {})
            match_score = cat.get('score', 0)
            
            # Get stream details for better display
            stream_details = get_stream_details(cat_id, st.session_state.user_type)
            if stream_details:
                stream_icon = stream_details['icon']
                stream_name = stream_details['name']
            else:
                stream_icon = cat.get('icon', '📚')
                stream_name = cat.get('name', 'Unknown Stream')
            
            with cols[i]:
                st.markdown(f"""
                <div class="stream-card">
                    <div class="stream-icon">{stream_icon}</div>
                    <div class="stream-name">{stream_name}</div>
                    <div class="stream-match">{match_score:.1f}% Match</div>
                    <div class="score-bar"><div class="score-fill" style="width:{match_score}%;"></div></div>
                </div>
                """, unsafe_allow_html=True)
                
                if st.button(f"🔍Click to Know {stream_name}", key=f"select_stream_{i}", use_container_width=True):
                    st.session_state.selected_stream = cat_id
                    st.session_state.page = 'stream_detail'
                    st.rerun()
    
    st.markdown('<hr>', unsafe_allow_html=True)
    
    col1, col2 = st.columns(2)
    with col1:
        if st.button("← Back to Comparison Table", use_container_width=True):
            st.session_state.page = 'stream_comparison'
            st.rerun()
    with col2:
        if st.button("Skip to Report →", use_container_width=True):
            if not st.session_state.selected_stream and st.session_state.recommended_categories:
                st.session_state.selected_stream = st.session_state.recommended_categories[0]
            st.session_state.page = 'report'
            st.rerun()
    
    st.markdown('</div>', unsafe_allow_html=True)

# Stream Detail Page - Show detailed information about selected stream with clickable careers
def show_stream_detail():
    show_header()
    st.markdown('<div class="main-card">', unsafe_allow_html=True)
    
    # Check if showing career detail popup
    if st.session_state.show_career_detail and st.session_state.selected_career:
        career_details = get_career_details(st.session_state.selected_career)
        
        st.markdown(f"""
        <div class="stream-detail-card">
            <div style="text-align:center;">
                <div style="font-size:3rem;">💼</div>
                <h1 style="color:#1565C0; margin:0.5rem 0;">{st.session_state.selected_career}</h1>
            </div>
        </div>
        """, unsafe_allow_html=True)
        
        st.markdown(f"""
        <div class="match-high">
            <strong>📖 About this Career</strong>
            <p style="margin-top:10px;">{career_details.get('description', 'No description available')}</p>
        </div>
        """, unsafe_allow_html=True)
        
        # Three columns for skills - with safe fallbacks
        col1, col2, col3 = st.columns(3)
        
        with col1:
            # Technical Skills (Hard Skills)
            st.markdown("### 🔧 Technical Skills")
            technical_skills = career_details.get('technical_skills', [])
            if not technical_skills:
                technical_skills = career_details.get('skills', [])
            if not technical_skills:
                technical_skills = ['Adobe Creative Suite (Photoshop, Illustrator, InDesign)',
        'UI/UX Design (Figma, Sketch, Adobe XD)',
        'Animation (Maya, Blender, After Effects)',
        '3D Modeling & Rendering',
        'Typography & Color Theory',
        'Video Editing (Premiere Pro, Final Cut)',
        'Motion Graphics',
        'Digital Illustration',
        'Brand Identity Design',
        'Print Production Knowledge',
        'Web Design (HTML, CSS basics)',
        'Photography & Lighting']
            
            for skill in technical_skills[:6]:
                st.markdown(f"- {skill}")
        
        with col2:
            # Software Skills
            st.markdown("### 💻 Software Skills")
            software_skills = career_details.get('software_skills', [])
            if not software_skills:
                software_skills = career_details.get('tools', [])
            if not software_skills:
                software_skills = ['Analytical Thinking & Problem Solving',
        'Attention to Detail',
        'Logical Reasoning',
        'Continuous Learning Mindset',
        'Communication (Technical Writing)',
        'Time Management',
        'Adaptability to New Technologies',
        'Team Collaboration in Agile Environment',
        'Critical Thinking',
        'Research & Innovation Mindset']
            
            for skill in software_skills[:6]:
                st.markdown(f"- {skill}")
        
        with col3:
            # Career/Soft Skills
            st.markdown("### 🌟 Soft Skills")
            career_skills = career_details.get('career_skills', [])
            if not career_skills:
                career_skills = career_details.get('soft_skills', [])
            if not career_skills:
                career_skills = ['Attention to Aesthetics',
        'Client Communication',
        'Time Management',
        'Open to Feedback & Critique',
        'Adaptability to Trends',
        'Conceptual Thinking',
        'Problem Solving Through Design',
        'Portfolio Presentation']
            
            for skill in career_skills[:6]:
                st.markdown(f"- {skill}")
        
        st.markdown("---")
        
        # Salary and Education in two columns
        col1, col2 = st.columns(2)
        with col1:
            st.markdown("### 💰 Salary Range")
            st.markdown(career_details.get('salary_range', 'Competitive industry standards'))
        
        with col2:
            st.markdown("### 📚 Education Required")
            st.markdown(career_details.get('education', "Bachelor's or Master's degree in relevant field"))
        
        # Job Growth Outlook
        st.markdown("### 📈 Job Growth Outlook")
        st.markdown(career_details.get('growth', 'Positive growth outlook'))
        
        # Show location-based companies
        top_companies = career_details.get('top_companies', [])
        if top_companies and isinstance(top_companies, list):
            st.markdown("### 🏢 Top Companies Hiring")
            
            user_city = st.session_state.student_city
            user_state = st.session_state.student_state
            
            local_companies, same_state_companies, other_companies = filter_companies_by_location(
                top_companies, user_city, user_state
            )
            
            if local_companies:
                st.markdown(f"**📍 In Your City ({user_city.title()}):**")
                for company in local_companies[:5]:
                    st.markdown(f"- {company}")
            
            if same_state_companies:
                st.markdown(f"**📍 In Your State ({user_state.title()} - Other Cities):**")
                for company in same_state_companies[:5]:
                    st.markdown(f"- {company}")
            
            if other_companies:
                st.markdown("**📍 Other Major Hubs (Across India):**")
                for company in other_companies[:8]:
                    st.markdown(f"- {company}")
        
        # Navigation buttons
        col1, col2 = st.columns(2)
        with col1:
            if st.button("← Back to Stream Details", use_container_width=True):
                st.session_state.show_career_detail = False
                st.session_state.selected_career = None
                st.rerun()
        with col2:
            if st.button("📥 Save Career Info", use_container_width=True):
                career_text = f"""CAREER DETAILS: {st.session_state.selected_career}

DESCRIPTION: {career_details.get('description', 'No description available')}

TECHNICAL SKILLS:
{chr(10).join(['• ' + skill for skill in career_details.get('technical_skills', career_details.get('skills', ['Analytical Thinking']))])}

SOFTWARE SKILLS:
{chr(10).join(['• ' + skill for skill in career_details.get('software_skills', career_details.get('tools', ['MS Office']))])}

SOFT SKILLS:
{chr(10).join(['• ' + skill for skill in career_details.get('career_skills', career_details.get('soft_skills', ['Communication', 'Teamwork']))])}

SALARY RANGE: {career_details.get('salary_range', 'Competitive')}
EDUCATION: {career_details.get('education', "Bachelor's degree")}
JOB GROWTH: {career_details.get('growth', 'Positive')}
"""
                st.download_button("Download Career Info", career_text, file_name=f"{st.session_state.selected_career}_details.txt")
        
        st.markdown('</div>', unsafe_allow_html=True)
        return
    
    # Original stream detail view
    if st.session_state.selected_stream:
        stream = st.session_state.categories_data.get(st.session_state.selected_stream, {})
        stream_details = get_stream_details(st.session_state.selected_stream, st.session_state.user_type)
        
        if stream_details:
            st.markdown(f"""
            <div class="stream-detail-card">
                <div style="text-align:center;">
                    <div style="font-size:3rem;">{stream_details['icon']}</div>
                    <h1 style="color:#1565C0; margin:0.5rem 0;">{stream_details['name']}</h1>
                    <div style="background:#FFF3E0; display:inline-block; padding:0.3rem 1rem; border-radius:20px; margin:0.5rem 0;">
                        Your Match Score: <strong style="color:#1565C0; font-size:1.3rem;">{stream.get('score', 0):.1f}%</strong>
                    </div>
                </div>
            </div>
            """, unsafe_allow_html=True)
            
            # Description
            st.markdown(f"""
            <div class="match-high">
                <strong>📖 About this Stream</strong>
                <p style="margin-top:10px;">{stream_details['description']}</p>
            </div>
            """, unsafe_allow_html=True)
            
            col1, col2 = st.columns(2)
            
            with col1:
                st.markdown(f"""
                <div style="background:#FFF8F0; border-radius:16px; padding:1.2rem; margin:0.5rem 0;">
                    <strong>💼 Top Career Paths</strong>
                    <ul>{''.join([f'<li>{career}</li>' for career in stream_details.get('careers', [])])}</ul>
                </div>
                <div style="background:#FFF8F0; border-radius:16px; padding:1.2rem; margin:0.5rem 0;">
                    <strong>🎯 Key Subjects to Focus</strong>
                    <ul>{''.join([f'<li>{subject}</li>' for subject in stream_details.get('subjects', [])])}</ul>
                </div>
                """, unsafe_allow_html=True)
            
            with col2:
                st.markdown(f"""
                <div style="background:#FFF8F0; border-radius:16px; padding:1.2rem; margin:0.5rem 0;">
                    <strong>✨ Skills to Develop</strong>
                    <ul>{''.join([f'<li>{skill}</li>' for skill in stream_details.get('skills', [])])}</ul>
                </div>
                <div style="background:#FFF8F0; border-radius:16px; padding:1.2rem; margin:0.5rem 0;">
                    <strong>🚀 Future Scope</strong>
                    <p>{stream_details.get('future_scope', 'Excellent growth opportunities in this field')}</p>
                </div>
                """, unsafe_allow_html=True)
            
            st.markdown('<hr>', unsafe_allow_html=True)
            
            # ============ THREE SKILLS SECTIONS ============
            # Row 1 - Technical Skills & Software Skills
            col_tech, col_soft = st.columns(2)
            
            with col_tech:
                # Technical Skills (Domain-specific knowledge)
                st.markdown("### 🔧 Technical Skills")
                if 'technical_skills' in stream_details and stream_details['technical_skills']:
                    tech_html = '<div style="background:#E8EAF6; border-radius:16px; padding:1rem; margin:0.5rem 0;"><ul>'
                    for skill in stream_details['technical_skills']:
                        tech_html += f'<li style="margin:5px 0;">{skill}</li>'
                    tech_html += '</ul></div>'
                    st.markdown(tech_html, unsafe_allow_html=True)
                else:
                    # Fallback to general skills
                    general_skills = stream_details.get('skills', ['Problem Solving', 'Critical Thinking', 'Domain Knowledge'])
                    tech_html = '<div style="background:#E8EAF6; border-radius:16px; padding:1rem; margin:0.5rem 0;"><ul>'
                    for skill in general_skills[:5]:
                        tech_html += f'<li style="margin:5px 0;">{skill}</li>'
                    tech_html += '</ul></div>'
                    st.markdown(tech_html, unsafe_allow_html=True)
            
            with col_soft:
                # Software Skills
                st.markdown("### 💻 Software Skills")
                if 'software_skills' in stream_details and stream_details['software_skills']:
                    soft_html = '<div style="background:#E3F2FD; border-radius:16px; padding:1rem; margin:0.5rem 0;"><ul>'
                    for skill in stream_details['software_skills']:
                        soft_html += f'<li style="margin:5px 0;">{skill}</li>'
                    soft_html += '</ul></div>'
                    st.markdown(soft_html, unsafe_allow_html=True)
                else:
                    soft_html = '<div style="background:#E3F2FD; border-radius:16px; padding:1rem; margin:0.5rem 0;"><ul>'
                    soft_html += '<li style="margin:5px 0;">MS Office Suite</li>'
                    soft_html += '<li style="margin:5px 0;">Email & Communication Tools</li>'
                    soft_html += '<li style="margin:5px 0;">Project Management Tools</li>'
                    soft_html += '<li style="margin:5px 0;">Industry Specific Software</li>'
                    soft_html += '</ul></div>'
                    st.markdown(soft_html, unsafe_allow_html=True)
            
            st.markdown("<br>", unsafe_allow_html=True)
            
            # Row 2 - Career/Soft Skills
            st.markdown("### 🌟 Soft Skills")
            if 'career_skills' in stream_details and stream_details['career_skills']:
                career_html = '<div style="background:#FFF3E0; border-radius:16px; padding:1rem; margin:0.5rem 0;"><ul>'
                for skill in stream_details['career_skills']:
                    career_html += f'<li style="margin:5px 0;">{skill}</li>'
                career_html += '</ul></div>'
                st.markdown(career_html, unsafe_allow_html=True)
            else:
                # Fallback to regular skills if career_skills doesn't exist
                if 'skills' in stream_details and stream_details['skills']:
                    career_html = '<div style="background:#FFF3E0; border-radius:16px; padding:1rem; margin:0.5rem 0;"><ul>'
                    for skill in stream_details['skills']:
                        career_html += f'<li style="margin:5px 0;">{skill}</li>'
                    career_html += '</ul></div>'
                    st.markdown(career_html, unsafe_allow_html=True)
                else:
                    default_skills = ['Communication', 'Teamwork', 'Problem Solving', 'Time Management', 'Leadership', 'Adaptability']
                    career_html = '<div style="background:#FFF3E0; border-radius:16px; padding:1rem; margin:0.5rem 0;"><ul>'
                    for skill in default_skills:
                        career_html += f'<li style="margin:5px 0;">{skill}</li>'
                    career_html += '</ul></div>'
                    st.markdown(career_html, unsafe_allow_html=True)
            
            st.markdown('<hr>', unsafe_allow_html=True)

            st.markdown("""
            <style>
                .dark-hiring-section {
                    background: linear-gradient(135deg, #0d1117, #161b22);
                    border-radius: 20px;
                    padding: 1.5rem;
                    margin: 1rem 0;
                    border: 1px solid #30363d;
                }
                .dark-hiring-title {
                    color: #f0883e;
                    font-size: 1.4rem;
                    font-weight: 800;
                    margin-bottom: 1.2rem;
                    border-left: 4px solid #f0883e;
                    padding-left: 1rem;
                }
                .dark-city-tag {
                    display: inline-block;
                    background: #21262d;
                    color: #f0883e;
                    padding: 8px 18px;
                    border-radius: 40px;
                    margin: 6px;
                    font-size: 1rem;
                    font-weight: 600;
                    border: 1px solid #30363d;
                    transition: all 0.3s ease;
                }
                .dark-city-tag:hover {
                    background: #f0883e;
                    color: #0d1117;
                    transform: translateY(-2px);
                }
                .dark-city-tag-special {
                    display: inline-block;
                    background: linear-gradient(135deg, #f0883e, #e06c2e);
                    color: white;
                    padding: 8px 20px;
                    border-radius: 40px;
                    margin: 6px;
                    font-size: 1rem;
                    font-weight: 700;
                    border: 1px solid #f0883e;
                    transition: all 0.3s ease;
                    box-shadow: 0 2px 8px rgba(240,136,62,0.3);
                }
                .dark-city-tag-special:hover {
                    transform: translateY(-2px);
                    box-shadow: 0 5px 15px rgba(240,136,62,0.5);
                }
            </style>
            """, unsafe_allow_html=True)
            
            # Display Top Hiring Cities
            hiring_cities = stream_details.get('hiring_cities', [])
            if hiring_cities:
                st.markdown("""
                <div class="dark-hiring-section">
                    <div class="dark-hiring-title">
                        🏙️ Top Hiring Cities
                    </div>
                    <div style="display: flex; flex-wrap: wrap; gap: 8px;">
                """, unsafe_allow_html=True)
                
                user_city_lower = st.session_state.student_city.lower() if st.session_state.student_city else ""
                for city in hiring_cities[:15]:
                    if city.lower() == user_city_lower:
                        st.markdown(f'<span class="dark-city-tag-special">📍 {city} <span style="font-size:0.75rem;">(Your City)</span></span>', unsafe_allow_html=True)
                    else:
                        st.markdown(f'<span class="dark-city-tag">📍 {city}</span>', unsafe_allow_html=True)
                
                st.markdown("</div></div>", unsafe_allow_html=True)
            
            # ============ LOCATION-BASED COMPANIES SECTION ============
            st.markdown("### 🏢 Hiring Companies Based on Your Location")
            
            all_companies = stream_details.get('top_companies', [])
            user_city = st.session_state.student_city
            user_state = st.session_state.student_state
            
            if all_companies and user_city and user_state:
                local_companies, same_state_companies, other_companies = filter_companies_by_location(
                    all_companies, user_city, user_state
                )
                
                # Show companies in user's city
                if local_companies:
                    st.markdown(f"#### 📍 In Your City: **{user_city.title()}**")
                    companies_html = '<div style="background:#E8F5E9; border-radius:16px; padding:1rem; margin:0.5rem 0;"><ul>'
                    for company in local_companies[:5]:
                        companies_html += f'<li style="margin:5px 0;">🏢 {company}</li>'
                    companies_html += '</ul></div>'
                    st.markdown(companies_html, unsafe_allow_html=True)
                else:
                    st.info(f"📍 No specific companies listed in {user_city.title()} yet. Check nearby cities below.")
                
                # Show companies in same state (other cities)
                if same_state_companies:
                    st.markdown(f"#### 📍 In Your State: **{user_state.title()}** (Other Cities)")
                    companies_html = '<div style="background:#FFF3E0; border-radius:16px; padding:1rem; margin:0.5rem 0;"><ul>'
                    for company in same_state_companies[:5]:
                        companies_html += f'<li style="margin:5px 0;">🏢 {company}</li>'
                    companies_html += '</ul></div>'
                    st.markdown(companies_html, unsafe_allow_html=True)
                
                # Show other major hubs across India
                if other_companies:
                    st.markdown("#### 📍 Other Major Hubs (Across India)")
                    companies_html = '<div style="background:#FFF8F0; border-radius:16px; padding:1rem; margin:0.5rem 0;"><ul>'
                    for company in other_companies[:10]:
                        companies_html += f'<li style="margin:5px 0;">🏢 {company}</li>'
                    companies_html += '</ul></div>'
                    st.markdown(companies_html, unsafe_allow_html=True)
                
            
            # Education Path and Certifications
            st.markdown(f"""
            <div style="background:#FFF8F0; border-radius:16px; padding:1.2rem; margin:0.5rem 0;">
                <strong>📚 Education Path</strong>
                <p>{stream_details.get('education_path', 'Various educational pathways available')}</p>
            </div>
            <div style="background:#FFF8F0; border-radius:16px; padding:1.2rem; margin:0.5rem 0;">
                <strong>🎓 Recommended Certifications</strong>
                <ul>{''.join([f'<li>{cert}</li>' for cert in stream_details.get('certifications', [])])}</ul>
            </div>
            """, unsafe_allow_html=True)
            
            # Career options - Clickable tags
            st.markdown('<strong>🔍 Explore Specific Careers (Click on any career to see details):</strong>', unsafe_allow_html=True)
            st.markdown("<br>", unsafe_allow_html=True)
            
            careers_list = stream_details.get('careers', [])
            num_careers = len(careers_list)
            
            # Display careers in rows of 3 buttons
            for idx in range(0, num_careers, 3):
                cols = st.columns(3)
                for j in range(3):
                    if idx + j < num_careers:
                        career = careers_list[idx + j]
                        career_title = career.split(' - ')[0] if ' - ' in career else career
                        with cols[j]:
                            if st.button(f"💼 {career_title}", key=f"career_{idx+j}", use_container_width=True):
                                st.session_state.selected_career = career_title
                                st.session_state.show_career_detail = True
                                st.rerun()
            
            # Navigation buttons
            col1, col2, col3 = st.columns(3)
            with col1:
                if st.button("← Back to Streams", use_container_width=True):
                    st.session_state.page = 'stream_selection'
                    st.rerun()
            with col2:
                if st.button("View Full Report →", type="primary", use_container_width=True):
                    st.session_state.page = 'report'
                    st.rerun()
            with col3:
                if st.button("Start Over 🔄", use_container_width=True):
                    # Reset everything
                    for key in list(st.session_state.keys()):
                        if key not in ['page']:
                            del st.session_state[key]
                    st.session_state.page = 'welcome'
                    st.rerun()
        else:
            # Fallback content when stream_details not found
            st.markdown(f"""
            <div class="stream-detail-card">
                <div style="text-align:center;">
                    <div style="font-size:3rem;">{stream.get('icon', '📚')}</div>
                    <h1 style="color:#D35400; margin:0.5rem 0;">{stream.get('name', 'Selected Stream')}</h1>
                    <div style="background:#FFF3E0; display:inline-block; padding:0.3rem 1rem; border-radius:20px; margin:0.5rem 0;">
                        Your Match Score: <strong style="color:#2E7D32; font-size:1.3rem;">{stream.get('score', 0):.1f}%</strong>
                    </div>
                </div>
            </div>
            
            <div class="match-high">
                <strong>📖 About this Stream</strong>
                <p style="margin-top:10px;">{stream.get('description', 'This stream offers excellent career opportunities in various fields.')}</p>
            </div>
            """, unsafe_allow_html=True)
            
            col1, col2, col3 = st.columns(3)
            with col1:
                if st.button("← Back to Streams", use_container_width=True):
                    st.session_state.page = 'stream_selection'
                    st.rerun()
            with col2:
                if st.button("View Full Report →", type="primary", use_container_width=True):
                    st.session_state.page = 'report'
                    st.rerun()
            with col3:
                if st.button("Start Over 🔄", use_container_width=True):
                    for key in list(st.session_state.keys()):
                        if key not in ['page']:
                            del st.session_state[key]
                    st.session_state.page = 'welcome'
                    st.rerun()
    
    st.markdown('</div>', unsafe_allow_html=True)

# Report Page
def show_report():
    show_header()
    st.markdown('<div class="main-card">', unsafe_allow_html=True)
    
    st.markdown(f'<h1 class="welcome-heading" style="font-size:1.5rem;">Your Personalized Career Report</h1>', unsafe_allow_html=True)
    st.markdown(f'<p class="sub-message">Prepared for {st.session_state.student_name}</p>', unsafe_allow_html=True)
    
    if st.session_state.selected_stream and st.session_state.selected_stream in st.session_state.categories_data:
        cat = st.session_state.categories_data[st.session_state.selected_stream]
        stream_details = get_stream_details(st.session_state.selected_stream, st.session_state.user_type)
        
        if stream_details:
            # Student Profile and Selected Stream
            col1, col2 = st.columns(2)
            with col1:
                st.markdown(f"""
                <div style="background:#FFF8F0; border-radius:16px; padding:1.2rem;">
                    <strong>📊 Student Profile</strong><br><br>
                    <strong>Name:</strong> {st.session_state.student_name}<br>
                    <strong>Age:</strong> {st.session_state.student_age}<br>
                    <strong>City:</strong> {st.session_state.student_city}<br>
                    <strong>State:</strong> {st.session_state.student_state}<br>
                    <strong>Institution:</strong> {st.session_state.student_institution}<br>
                    <strong>Grade/Year:</strong> {st.session_state.student_grade}<br>
                    <strong>Assessment Type:</strong> {'School Student' if st.session_state.user_type == 'school' else 'College Student'} Pathway<br>
                    <strong>Date:</strong> {datetime.now().strftime('%Y-%m-%d')}
                </div>
                """, unsafe_allow_html=True)
            with col2:
                score_value = cat.get('score', 0)
                st.markdown(f"""
                <div style="background:#FFF8F0; border-radius:16px; padding:1.2rem;">
                    <strong>🎯 Selected Stream</strong><br><br>
                    <div style="font-size:2rem;">{stream_details['icon']}</div>
                    <strong>{stream_details['name']}</strong><br>
                    Match Score: <span style="color:#2E7D32; font-size:1.8rem; font-weight:700;">{score_value:.1f}%</span>
                </div>
                """, unsafe_allow_html=True)
            
            st.markdown("<hr>", unsafe_allow_html=True)
            
            # About the Stream
            st.markdown("### 📖 About this Stream")
            st.markdown(f"""
            <div style="background:#E8F5E9; border-radius:16px; padding:1rem; margin:0.5rem 0;">
                <p>{stream_details['description']}</p>
            </div>
            """, unsafe_allow_html=True)
            
            # Career Recommendations
            st.markdown("### 📋 Top Career Paths")
            for career in stream_details.get('careers', []):
                st.markdown(f"""
                <div style="background:#E8F5E9; border-radius:16px; padding:1rem; margin:0.5rem 0;">
                    <strong>💼 {career}</strong>
                </div>
                """, unsafe_allow_html=True)
            
            # Key Subjects
            st.markdown("### 🎯 Key Subjects to Focus")
            subjects_html = '<div style="background:#FFF8F0; border-radius:16px; padding:1rem; margin:0.5rem 0;"><ul>'
            for subject in stream_details.get('subjects', []):
                subjects_html += f'<li>{subject}</li>'
            subjects_html += '</ul></div>'
            st.markdown(subjects_html, unsafe_allow_html=True)
            
            # Skills to Develop
            st.markdown("### ✨ Skills to Develop")
            skills_html = '<div style="background:#FFF8F0; border-radius:16px; padding:1rem; margin:0.5rem 0;"><ul>'
            for skill in stream_details.get('skills', []):
                skills_html += f'<li>{skill}</li>'
            skills_html += '</ul></div>'
            st.markdown(skills_html, unsafe_allow_html=True)
            
            # Future Scope
            st.markdown("### 🚀 Future Scope")
            st.markdown(f"""
            <div style="background:#FFF8F0; border-radius:16px; padding:1rem; margin:0.5rem 0;">
                <p>{stream_details.get('future_scope', 'Excellent growth opportunities in this field')}</p>
            </div>
            """, unsafe_allow_html=True)
            
            # Top Companies
            st.markdown("### 🏢 Top Companies Hiring")
            companies_html = '<div style="background:#FFF8F0; border-radius:16px; padding:1rem; margin:0.5rem 0;"><ul>'
            for company in stream_details.get('top_companies', []):
                companies_html += f'<li>{company}</li>'
            companies_html += '</ul></div>'
            st.markdown(companies_html, unsafe_allow_html=True)
            
            # Education Path
            st.markdown("### 📚 Recommended Education Path")
            st.markdown(f"""
            <div style="background:#FFF8F0; border-radius:16px; padding:1rem; margin:0.5rem 0;">
                <p>{stream_details.get('education_path', 'Various educational pathways available')}</p>
            </div>
            """, unsafe_allow_html=True)
            
            # Certifications
            st.markdown("### 🎓 Valuable Certifications")
            certs_html = '<div style="background:#FFF8F0; border-radius:16px; padding:1rem; margin:0.5rem 0;"><ul>'
            for cert in stream_details.get('certifications', []):
                certs_html += f'<li>{cert}</li>'
            certs_html += '</ul></div>'
            st.markdown(certs_html, unsafe_allow_html=True)
            
            # Next Steps
            st.markdown("### 🎓 Next Steps")
            subjects_list = stream_details.get('subjects', ['relevant subjects'])
            skills_list = stream_details.get('skills', ['key skills'])
            certs_list = stream_details.get('certifications', ['relevant certifications'])
            stream_name = stream_details['name']
            
            st.markdown(f"""
            <div style="background:#FFF8F0; border-radius:16px; padding:1rem; margin:0.5rem 0;">
                <p>✅ Focus on developing strong foundations in {', '.join(subjects_list[:3])}</p>
                <p>✅ Build {', '.join(skills_list[:2])} skills through projects and internships</p>
                <p>✅ Connect with professionals in {stream_name} for mentorship</p>
                <p>✅ Research colleges and programs specializing in {stream_name}</p>
                <p>✅ Consider pursuing {certs_list[0] if certs_list else 'relevant certifications'} certification</p>
            </div>
            """, unsafe_allow_html=True)
        else:
            # Fallback - show basic information from the category
            cat_name = cat.get('name', 'Your Selected Stream')
            cat_score = cat.get('score', 0)
            st.markdown(f"""
            <div style="background:#FFF8F0; border-radius:16px; padding:1.2rem;">
                <strong>Selected Stream:</strong> {cat_name}<br>
                <strong>Match Score:</strong> {cat_score:.1f}%<br><br>
                <p>We recommend exploring opportunities in {cat_name}. This stream offers various career paths with good growth potential.</p>
            </div>
            """, unsafe_allow_html=True)
    
    st.markdown("<hr>", unsafe_allow_html=True)
    
    # ONLY PDF Download button (removed TXT and Print buttons)
    col1, col2, col3 = st.columns([1, 2, 1])
    with col2:
        if st.button("📥 Download Report (PDF)", type="primary", use_container_width=True):
            if st.session_state.selected_stream:
                with st.spinner("Generating PDF report..."):
                    try:
                        pdf_path = generate_pdf_report()
                        with open(pdf_path, "rb") as pdf_file:
                            pdf_data = pdf_file.read()
                        st.download_button(
                            label="💾 Save PDF Report",
                            data=pdf_data,
                            file_name=f"{st.session_state.student_name}_career_report.pdf",
                            mime="application/pdf",
                            key="download_pdf"
                        )
                        os.unlink(pdf_path)
                        st.success("✅ PDF Report generated successfully!")
                    except Exception as e:
                        st.error(f"Error generating PDF: {str(e)}")
    
    st.markdown("<br>", unsafe_allow_html=True)
    
    col1, col2 = st.columns(2)
    with col1:
        if st.button("← Back to Stream Details", use_container_width=True):
            st.session_state.page = 'stream_detail'
            st.rerun()
    with col2:
        if st.button("🏠 Start New Assessment", use_container_width=True):
            # Reset all session state
            for key in list(st.session_state.keys()):
                if key not in ['page']:
                    del st.session_state[key]
            st.session_state.page = 'welcome'
            st.rerun()
    
    st.markdown('</div>', unsafe_allow_html=True)

# Main
def main():
    if st.session_state.page == 'welcome':
        show_welcome()
    elif st.session_state.page == 'load_assessment':
        show_load_assessment()
    elif st.session_state.page == 'assessment':
        show_assessment()
    elif st.session_state.page == 'personality_choice':
        show_personality_choice()
    elif st.session_state.page == 'personality_assessment':
        show_personality_assessment()
    elif st.session_state.page == 'personality_result':
        show_personality_result()
    elif st.session_state.page == 'stream_comparison':  
        show_stream_comparison()  
    elif st.session_state.page == 'stream_selection':
        show_stream_selection()
    elif st.session_state.page == 'stream_detail':
        show_stream_detail()
    elif st.session_state.page == 'report':
        show_report()

if __name__ == "__main__":
    main()
