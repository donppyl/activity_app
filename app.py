import streamlit as st
import random
import json
from datetime import datetime, date
import time

# ── Page Config ──────────────────────────────────────────────────────────────
st.set_page_config(
    page_title="FamilyFun Hub 🎉",
    page_icon="🎉",
    layout="wide",
    initial_sidebar_state="expanded",
)

# ── Custom CSS ────────────────────────────────────────────────────────────────
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Fredoka+One&family=Nunito:wght@400;600;700;800&display=swap');

html, body, [class*="css"] {
    font-family: 'Nunito', sans-serif;
}

/* Background */
.stApp {
    background: linear-gradient(135deg, #FFF9F0 0%, #FFF0E6 50%, #F0F4FF 100%);
}

/* Headers */
h1 { font-family: 'Fredoka One', cursive !important; color: #FF6B6B !important; }
h2 { font-family: 'Fredoka One', cursive !important; color: #4ECDC4 !important; }
h3 { font-family: 'Fredoka One', cursive !important; color: #FF8E53 !important; }

/* Sidebar */
section[data-testid="stSidebar"] {
    background: linear-gradient(180deg, #FF6B6B 0%, #FF8E53 50%, #FFC947 100%);
    color: white;
}
section[data-testid="stSidebar"] .css-1d391kg { color: white; }
section[data-testid="stSidebar"] label { color: white !important; font-weight: 700 !important; }
section[data-testid="stSidebar"] h1, 
section[data-testid="stSidebar"] h2, 
section[data-testid="stSidebar"] h3 { color: white !important; }

/* Cards */
.fun-card {
    background: white;
    border-radius: 20px;
    padding: 1.5rem;
    box-shadow: 0 8px 30px rgba(0,0,0,0.08);
    border-left: 6px solid #FF6B6B;
    margin-bottom: 1rem;
    transition: transform 0.2s;
}
.fun-card:hover { transform: translateY(-3px); }
.fun-card.teal { border-left-color: #4ECDC4; }
.fun-card.orange { border-left-color: #FF8E53; }
.fun-card.purple { border-left-color: #A78BFA; }
.fun-card.yellow { border-left-color: #FFC947; }

/* Activity badge */
.badge {
    display: inline-block;
    padding: 4px 14px;
    border-radius: 50px;
    font-size: 0.75rem;
    font-weight: 800;
    text-transform: uppercase;
    letter-spacing: 0.5px;
    margin: 2px;
}
.badge-indoor { background: #E0F2FE; color: #0284C7; }
.badge-outdoor { background: #D1FAE5; color: #059669; }
.badge-creative { background: #FDE68A; color: #D97706; }
.badge-learning { background: #EDE9FE; color: #7C3AED; }
.badge-active { background: #FFE4E6; color: #E11D48; }

/* Big emoji display */
.big-emoji {
    font-size: 5rem;
    text-align: center;
    display: block;
    animation: bounce 1s infinite alternate;
}
@keyframes bounce {
    from { transform: translateY(0); }
    to { transform: translateY(-12px); }
}

/* Metric cards */
.metric-row {
    display: flex;
    gap: 1rem;
    flex-wrap: wrap;
    margin-bottom: 1.5rem;
}
.metric-card {
    flex: 1;
    min-width: 120px;
    background: white;
    border-radius: 16px;
    padding: 1rem;
    text-align: center;
    box-shadow: 0 4px 15px rgba(0,0,0,0.06);
}
.metric-number {
    font-family: 'Fredoka One', cursive;
    font-size: 2.5rem;
    line-height: 1;
}
.metric-label { font-size: 0.8rem; color: #888; font-weight: 600; }

/* Spinner result */
.spinner-result {
    text-align: center;
    padding: 2rem;
    background: linear-gradient(135deg, #FF6B6B, #FF8E53);
    border-radius: 24px;
    color: white;
    font-family: 'Fredoka One', cursive;
    font-size: 1.8rem;
    box-shadow: 0 10px 40px rgba(255,107,107,0.3);
    margin: 1rem 0;
}

/* Timer display */
.timer-display {
    font-family: 'Fredoka One', cursive;
    font-size: 4rem;
    text-align: center;
    color: #FF6B6B;
    background: white;
    border-radius: 20px;
    padding: 1.5rem;
    box-shadow: 0 8px 30px rgba(0,0,0,0.08);
}

/* Chore item */
.chore-item {
    display: flex;
    align-items: center;
    padding: 0.75rem 1rem;
    background: white;
    border-radius: 12px;
    margin-bottom: 0.5rem;
    box-shadow: 0 3px 12px rgba(0,0,0,0.05);
    font-weight: 600;
}

/* Hide Streamlit branding */
#MainMenu {visibility: hidden;}
footer {visibility: hidden;}

/* Button styling */
.stButton > button {
    background: linear-gradient(135deg, #FF6B6B, #FF8E53) !important;
    color: white !important;
    border: none !important;
    border-radius: 50px !important;
    padding: 0.5rem 1.5rem !important;
    font-family: 'Fredoka One', cursive !important;
    font-size: 1rem !important;
    box-shadow: 0 4px 15px rgba(255,107,107,0.3) !important;
    transition: all 0.2s !important;
}
.stButton > button:hover {
    transform: translateY(-2px) !important;
    box-shadow: 0 8px 25px rgba(255,107,107,0.4) !important;
}
</style>
""", unsafe_allow_html=True)

# ── Data ──────────────────────────────────────────────────────────────────────
ACTIVITIES = [
    {"name": "Backyard Scavenger Hunt", "emoji": "🔍", "type": "outdoor", "age": "4+", "time": "45 min", "players": "2-8",
     "desc": "Hide items around the yard and give clues. First to find all wins a special treat!", "materials": "Paper, pen, small objects"},
    {"name": "Family Board Game Night", "emoji": "🎲", "type": "indoor", "age": "6+", "time": "60 min", "players": "2-6",
     "desc": "Pick your favorite board game and make it a tournament. Loser does dishes!", "materials": "Board game"},
    {"name": "Sidewalk Chalk Art", "emoji": "🎨", "type": "outdoor", "age": "3+", "time": "30 min", "players": "1-10",
     "desc": "Transform your driveway into a masterpiece. Draw each other's silhouettes!", "materials": "Chalk"},
    {"name": "Kitchen Science Experiments", "emoji": "🧪", "type": "learning", "age": "5+", "time": "40 min", "players": "1-4",
     "desc": "Make volcanoes with baking soda & vinegar, grow crystals, or make slime!", "materials": "Baking soda, vinegar, food coloring"},
    {"name": "Family Talent Show", "emoji": "🎤", "type": "creative", "age": "All", "time": "60 min", "players": "3+",
     "desc": "Everyone performs their hidden talent. Vote for categories like funniest, most creative!", "materials": "Optional costumes & props"},
    {"name": "Obstacle Course", "emoji": "🏃", "type": "active", "age": "4+", "time": "30 min", "players": "2-8",
     "desc": "Set up a course with pillows, hula hoops, and chairs. Time each other!", "materials": "Pillows, chairs, hula hoops"},
    {"name": "Movie Marathon", "emoji": "🎬", "type": "indoor", "age": "All", "time": "180 min", "players": "2-10",
     "desc": "Pick a theme (e.g., superhero movies) and watch back-to-back with themed snacks!", "materials": "TV, popcorn, cozy blankets"},
    {"name": "Cookie Baking Contest", "emoji": "🍪", "type": "creative", "age": "4+", "time": "90 min", "players": "2-6",
     "desc": "Each team decorates cookies with different themes. Judge by taste and looks!", "materials": "Cookie mix, icing, sprinkles"},
    {"name": "Nature Walk & Bingo", "emoji": "🌿", "type": "outdoor", "age": "4+", "time": "45 min", "players": "2-6",
     "desc": "Make bingo cards with nature items (bird, red flower, pinecone) before heading out!", "materials": "Paper, pencils"},
    {"name": "Family Photo Shoot", "emoji": "📸", "type": "creative", "age": "All", "time": "30 min", "players": "2+",
     "desc": "Create funny scenes and costumes, then have a proper photo shoot. Print your favorites!", "materials": "Phone/camera, props"},
    {"name": "Build a Fort", "emoji": "🏰", "type": "indoor", "age": "3+", "time": "45 min", "players": "2-6",
     "desc": "Gather every blanket and pillow in the house to build the ultimate blanket fort kingdom!", "materials": "Blankets, pillows, chairs"},
    {"name": "Backyard Camping", "emoji": "⛺", "type": "outdoor", "age": "5+", "time": "All night", "players": "2-8",
     "desc": "Set up a tent, tell stories under the stars, and make s'mores! No phones allowed!", "materials": "Tent, sleeping bags, flashlights"},
    {"name": "DIY Tie-Dye", "emoji": "🌈", "type": "creative", "age": "5+", "time": "60 min", "players": "2-8",
     "desc": "Tie-dye old white t-shirts and watch the magic happen. Each person gets their own pattern!", "materials": "White shirts, rubber bands, tie-dye kit"},
    {"name": "Family Trivia Night", "emoji": "🧠", "type": "learning", "age": "8+", "time": "45 min", "players": "4+",
     "desc": "Team up for a trivia game. Mix easy, medium, and hard questions across topics!", "materials": "Trivia cards or phone"},
    {"name": "Water Balloon Fight", "emoji": "💦", "type": "active", "age": "4+", "time": "20 min", "players": "2-10",
     "desc": "Fill up a hundred water balloons and have an epic summer battle in the backyard!", "materials": "Water balloons, water"},
]

CHORES = [
    {"name": "Sweep the floor", "emoji": "🧹", "points": 10},
    {"name": "Set the table", "emoji": "🍽️", "points": 5},
    {"name": "Feed the pet", "emoji": "🐾", "points": 8},
    {"name": "Take out trash", "emoji": "🗑️", "points": 10},
    {"name": "Water the plants", "emoji": "🌿", "points": 7},
    {"name": "Vacuum living room", "emoji": "🧼", "points": 15},
    {"name": "Wash dishes", "emoji": "🫧", "points": 12},
    {"name": "Make your bed", "emoji": "🛏️", "points": 5},
    {"name": "Clean bathroom", "emoji": "🚿", "points": 20},
    {"name": "Do laundry", "emoji": "👕", "points": 15},
    {"name": "Organize toys", "emoji": "🧸", "points": 8},
    {"name": "Wipe counters", "emoji": "✨", "points": 7},
]

TRIVIA_QUESTIONS = [
    {"q": "What is the largest planet in our solar system?", "a": "Jupiter", "options": ["Saturn", "Jupiter", "Neptune", "Uranus"], "difficulty": "Easy"},
    {"q": "How many legs does a spider have?", "a": "8", "options": ["6", "8", "10", "12"], "difficulty": "Easy"},
    {"q": "What color do you get when you mix blue and yellow?", "a": "Green", "options": ["Purple", "Orange", "Green", "Brown"], "difficulty": "Easy"},
    {"q": "What is the capital of France?", "a": "Paris", "options": ["London", "Berlin", "Paris", "Madrid"], "difficulty": "Easy"},
    {"q": "How many sides does a hexagon have?", "a": "6", "options": ["5", "6", "7", "8"], "difficulty": "Medium"},
    {"q": "What gas do plants absorb from the air?", "a": "Carbon dioxide", "options": ["Oxygen", "Nitrogen", "Carbon dioxide", "Hydrogen"], "difficulty": "Medium"},
    {"q": "Which ocean is the largest?", "a": "Pacific", "options": ["Atlantic", "Indian", "Pacific", "Arctic"], "difficulty": "Medium"},
    {"q": "What is 7 × 8?", "a": "56", "options": ["48", "54", "56", "64"], "difficulty": "Medium"},
    {"q": "What is the chemical symbol for gold?", "a": "Au", "options": ["Go", "Gd", "Au", "Ag"], "difficulty": "Hard"},
    {"q": "How many bones are in the adult human body?", "a": "206", "options": ["186", "196", "206", "216"], "difficulty": "Hard"},
    {"q": "What is the smallest country in the world?", "a": "Vatican City", "options": ["Monaco", "San Marino", "Vatican City", "Liechtenstein"], "difficulty": "Hard"},
    {"q": "What year did the first moon landing happen?", "a": "1969", "options": ["1965", "1967", "1969", "1972"], "difficulty": "Medium"},
]

# ── Session State ─────────────────────────────────────────────────────────────
def init_state():
    defaults = {
        "completed_activities": [],
        "chore_assignments": {},
        "points": {},
        "family_members": ["Mom", "Dad", "Alex", "Sam"],
        "trivia_score": {"correct": 0, "total": 0},
        "current_question": None,
        "answered": False,
        "spinner_result": None,
        "timer_running": False,
        "timer_end": None,
    }
    for k, v in defaults.items():
        if k not in st.session_state:
            st.session_state[k] = v

init_state()

# ── Sidebar ───────────────────────────────────────────────────────────────────
with st.sidebar:
    st.markdown("# 🎉 FamilyFun Hub")
    st.markdown("---")
    
    page = st.radio("Navigate", 
        ["🏠 Home", "🎯 Activity Picker", "🧹 Chore Chart", "🧠 Trivia Time", "⏱️ Family Timer", "👥 Family Setup"],
        label_visibility="collapsed"
    )
    
    st.markdown("---")
    st.markdown("### 🏆 Leaderboard")
    if st.session_state.points:
        sorted_pts = sorted(st.session_state.points.items(), key=lambda x: x[1], reverse=True)
        medals = ["🥇", "🥈", "🥉", "🎖️"]
        for i, (member, pts) in enumerate(sorted_pts):
            medal = medals[i] if i < len(medals) else "⭐"
            st.markdown(f"{medal} **{member}**: {pts} pts")
    else:
        st.markdown("*No points yet! Complete chores to earn points.*")
    
    st.markdown("---")
    total_done = len(st.session_state.completed_activities)
    st.markdown(f"✅ **{total_done}** activities done this week!")

# ── Pages ──────────────────────────────────────────────────────────────────────
page_name = page.split(" ", 1)[1]

# HOME
if page_name == "Home":
    col1, col2 = st.columns([2, 1])
    with col1:
        st.markdown("# 🎉 Welcome to FamilyFun Hub!")
        st.markdown("### *Your family's adventure starts here*")
        st.markdown("""
        <div class="fun-card">
            <h3>What can you do here?</h3>
            <p>🎯 <b>Activity Picker</b> — Spin for a random family activity or browse by type</p>
            <p>🧹 <b>Chore Chart</b> — Assign chores and earn points for completing them</p>
            <p>🧠 <b>Trivia Time</b> — Test your family's knowledge with fun questions</p>
            <p>⏱️ <b>Family Timer</b> — Countdown timer for games and activities</p>
        </div>
        """, unsafe_allow_html=True)
    
    with col2:
        st.markdown('<span class="big-emoji">🏠</span>', unsafe_allow_html=True)

    st.markdown("---")
    st.markdown("## 🌟 Featured Activities Today")
    
    featured = random.sample(ACTIVITIES, min(3, len(ACTIVITIES)))
    cols = st.columns(3)
    colors = ["", "teal", "orange"]
    for i, act in enumerate(featured):
        with cols[i]:
            badge_class = f"badge-{act['type']}"
            st.markdown(f"""
            <div class="fun-card {colors[i]}">
                <div style="font-size:2.5rem;text-align:center">{act['emoji']}</div>
                <h3 style="text-align:center;margin:0.5rem 0">{act['name']}</h3>
                <p style="color:#666;font-size:0.9rem">{act['desc']}</p>
                <div style="margin-top:0.5rem">
                    <span class="badge {badge_class}">{act['type']}</span>
                    <span class="badge" style="background:#F3F4F6;color:#666">⏱ {act['time']}</span>
                    <span class="badge" style="background:#F3F4F6;color:#666">👥 {act['players']}</span>
                </div>
            </div>
            """, unsafe_allow_html=True)

    st.markdown("---")
    col1, col2, col3, col4 = st.columns(4)
    with col1:
        st.markdown(f"""<div class="fun-card teal" style="text-align:center">
            <div style="font-size:2rem">🎯</div>
            <div style="font-family:'Fredoka One',cursive;font-size:2rem;color:#4ECDC4">{len(ACTIVITIES)}</div>
            <div style="color:#888;font-size:0.8rem;font-weight:600">ACTIVITIES</div>
        </div>""", unsafe_allow_html=True)
    with col2:
        st.markdown(f"""<div class="fun-card orange" style="text-align:center">
            <div style="font-size:2rem">🧹</div>
            <div style="font-family:'Fredoka One',cursive;font-size:2rem;color:#FF8E53">{len(CHORES)}</div>
            <div style="color:#888;font-size:0.8rem;font-weight:600">CHORES</div>
        </div>""", unsafe_allow_html=True)
    with col3:
        st.markdown(f"""<div class="fun-card purple" style="text-align:center">
            <div style="font-size:2rem">🧠</div>
            <div style="font-family:'Fredoka One',cursive;font-size:2rem;color:#A78BFA">{len(TRIVIA_QUESTIONS)}</div>
            <div style="color:#888;font-size:0.8rem;font-weight:600">TRIVIA Q's</div>
        </div>""", unsafe_allow_html=True)
    with col4:
        st.markdown(f"""<div class="fun-card yellow" style="text-align:center">
            <div style="font-size:2rem">👥</div>
            <div style="font-family:'Fredoka One',cursive;font-size:2rem;color:#FFC947">{len(st.session_state.family_members)}</div>
            <div style="color:#888;font-size:0.8rem;font-weight:600">FAMILY MEMBERS</div>
        </div>""", unsafe_allow_html=True)

# ACTIVITY PICKER
elif page_name == "Activity Picker":
    st.markdown("# 🎯 Activity Picker")
    
    tab1, tab2 = st.tabs(["🎰 Random Spin", "📋 Browse All"])
    
    with tab1:
        st.markdown("### Spin the wheel for your next adventure!")
        
        col1, col2, col3 = st.columns([1, 2, 1])
        with col2:
            # Filters
            filter_type = st.selectbox("Filter by type", ["All", "indoor", "outdoor", "creative", "learning", "active"])
            filter_age = st.selectbox("Filter by age group", ["All ages", "4+", "5+", "6+", "8+"])
            
            if st.button("🎰 SPIN FOR AN ACTIVITY!", use_container_width=True):
                filtered = ACTIVITIES
                if filter_type != "All":
                    filtered = [a for a in filtered if a["type"] == filter_type]
                
                if filtered:
                    picked = random.choice(filtered)
                    st.session_state.spinner_result = picked
                else:
                    st.warning("No activities match your filters!")
        
        if st.session_state.spinner_result:
            act = st.session_state.spinner_result
            st.markdown(f"""
            <div class="spinner-result">
                <div style="font-size:4rem">{act['emoji']}</div>
                <div>{act['name']}</div>
                <div style="font-size:1rem;font-weight:400;margin-top:0.5rem;opacity:0.9">{act['desc']}</div>
            </div>
            """, unsafe_allow_html=True)
            
            col1, col2, col3 = st.columns(3)
            with col1:
                st.info(f"⏱️ **Time:** {act['time']}")
            with col2:
                st.info(f"👥 **Players:** {act['players']}")
            with col3:
                st.info(f"🎒 **Materials:** {act['materials']}")
            
            if st.button("✅ Mark as Done!", use_container_width=True):
                if act['name'] not in st.session_state.completed_activities:
                    st.session_state.completed_activities.append(act['name'])
                    st.balloons()
                    st.success(f"Awesome! '{act['name']}' added to your completed list!")
    
    with tab2:
        st.markdown("### All Family Activities")
        
        col1, col2 = st.columns(2)
        with col1:
            search = st.text_input("🔍 Search activities", placeholder="Type to search...")
        with col2:
            type_filter = st.multiselect("Filter by type", ["indoor", "outdoor", "creative", "learning", "active"],
                                          default=["indoor", "outdoor", "creative", "learning", "active"])
        
        filtered = [a for a in ACTIVITIES 
                    if a["type"] in type_filter 
                    and (search.lower() in a["name"].lower() or search.lower() in a["desc"].lower() or not search)]
        
        st.markdown(f"*Showing {len(filtered)} activities*")
        
        for act in filtered:
            colors_map = {"indoor": "", "outdoor": "teal", "creative": "orange", "learning": "purple", "active": "yellow"}
            card_color = colors_map.get(act["type"], "")
            st.markdown(f"""
            <div class="fun-card {card_color}">
                <div style="display:flex;align-items:center;gap:1rem">
                    <div style="font-size:2.5rem">{act['emoji']}</div>
                    <div style="flex:1">
                        <b style="font-size:1.1rem">{act['name']}</b>
                        <span class="badge badge-{act['type']}" style="margin-left:0.5rem">{act['type']}</span>
                        <p style="color:#666;margin:0.3rem 0 0">{act['desc']}</p>
                        <div style="margin-top:0.5rem">
                            <span class="badge" style="background:#F3F4F6;color:#666">⏱ {act['time']}</span>
                            <span class="badge" style="background:#F3F4F6;color:#666">👥 {act['players']}</span>
                            <span class="badge" style="background:#F3F4F6;color:#666">🔞 {act['age']}</span>
                            <span class="badge" style="background:#F3F4F6;color:#666">🎒 {act['materials']}</span>
                        </div>
                    </div>
                </div>
            </div>
            """, unsafe_allow_html=True)

# CHORE CHART
elif page_name == "Chore Chart":
    st.markdown("# 🧹 Family Chore Chart")
    st.markdown("Assign chores, earn points, and keep the house sparkling!")
    
    tab1, tab2 = st.tabs(["📋 Chore Board", "🏆 Points & Rewards"])
    
    with tab1:
        # Initialize points for family members
        for member in st.session_state.family_members:
            if member not in st.session_state.points:
                st.session_state.points[member] = 0
        
        st.markdown("### Assign Chores to Family Members")
        
        cols = st.columns(2)
        for i, chore in enumerate(CHORES):
            with cols[i % 2]:
                assigned = st.session_state.chore_assignments.get(chore["name"], {})
                assignee = assigned.get("assignee", "Unassigned")
                done = assigned.get("done", False)
                
                bg = "#E8F5E9" if done else "white"
                check = "✅" if done else "⬜"
                
                st.markdown(f"""
                <div style="background:{bg};border-radius:12px;padding:0.75rem 1rem;
                            margin-bottom:0.5rem;box-shadow:0 3px 12px rgba(0,0,0,0.05);
                            display:flex;align-items:center;gap:0.5rem">
                    <span style="font-size:1.5rem">{chore['emoji']}</span>
                    <span style="flex:1;font-weight:600">{chore['name']}</span>
                    <span style="background:#FFF9C4;padding:2px 8px;border-radius:20px;
                                 font-size:0.8rem;font-weight:700;color:#F57F17">{chore['points']} pts</span>
                    <span style="font-size:1rem">{check}</span>
                </div>
                """, unsafe_allow_html=True)
                
                a_col, b_col = st.columns(2)
                with a_col:
                    new_assignee = st.selectbox(
                        f"Assign", 
                        ["Unassigned"] + st.session_state.family_members,
                        index=(["Unassigned"] + st.session_state.family_members).index(assignee) 
                              if assignee in (["Unassigned"] + st.session_state.family_members) else 0,
                        key=f"assign_{chore['name']}",
                        label_visibility="collapsed"
                    )
                with b_col:
                    if st.button("✅ Done" if not done else "↩️ Undo", key=f"done_{chore['name']}"):
                        if not done and new_assignee != "Unassigned":
                            st.session_state.chore_assignments[chore["name"]] = {"assignee": new_assignee, "done": True}
                            st.session_state.points[new_assignee] = st.session_state.points.get(new_assignee, 0) + chore["points"]
                            st.success(f"🎉 +{chore['points']} points for {new_assignee}!")
                            st.rerun()
                        elif done:
                            old_assignee = st.session_state.chore_assignments[chore["name"]]["assignee"]
                            st.session_state.chore_assignments[chore["name"]] = {"assignee": old_assignee, "done": False}
                            st.session_state.points[old_assignee] = max(0, st.session_state.points.get(old_assignee, 0) - chore["points"])
                            st.rerun()
                        else:
                            st.warning("Please assign to a family member first!")
                
                # Update assignment (not done status)
                if new_assignee != assignee and not done:
                    st.session_state.chore_assignments[chore["name"]] = {"assignee": new_assignee, "done": False}
    
    with tab2:
        st.markdown("### 🏆 Points Leaderboard")
        
        if st.session_state.points:
            sorted_pts = sorted(st.session_state.points.items(), key=lambda x: x[1], reverse=True)
            medals = ["🥇", "🥈", "🥉", "🎖️", "⭐", "🌟"]
            
            for i, (member, pts) in enumerate(sorted_pts):
                medal = medals[i] if i < len(medals) else "⭐"
                bar_width = int((pts / max(p for _, p in sorted_pts + [("", 1)]) * 100))
                st.markdown(f"""
                <div style="background:white;border-radius:16px;padding:1rem 1.5rem;
                            margin-bottom:0.75rem;box-shadow:0 4px 15px rgba(0,0,0,0.06)">
                    <div style="display:flex;align-items:center;gap:1rem;margin-bottom:0.5rem">
                        <span style="font-size:1.8rem">{medal}</span>
                        <span style="font-size:1.2rem;font-weight:800">{member}</span>
                        <span style="margin-left:auto;font-family:'Fredoka One',cursive;
                                     font-size:1.5rem;color:#FF6B6B">{pts} pts</span>
                    </div>
                    <div style="background:#F3F4F6;border-radius:10px;height:10px;overflow:hidden">
                        <div style="background:linear-gradient(90deg,#FF6B6B,#FF8E53);
                                    height:100%;width:{bar_width}%;border-radius:10px;
                                    transition:width 0.5s"></div>
                    </div>
                </div>
                """, unsafe_allow_html=True)
        else:
            st.info("Complete chores to earn points!")
        
        st.markdown("---")
        st.markdown("### 🎁 Reward Ideas")
        rewards = [
            ("50 pts", "🎬 Movie pick night"),
            ("100 pts", "🍦 Ice cream outing"),
            ("200 pts", "🎮 Extra screen time (1 hr)"),
            ("300 pts", "🎉 Special dinner choice"),
            ("500 pts", "🎢 Family outing of choice"),
        ]
        cols = st.columns(len(rewards))
        for col, (pts, reward) in zip(cols, rewards):
            with col:
                st.markdown(f"""
                <div style="background:white;border-radius:12px;padding:1rem;text-align:center;
                            box-shadow:0 4px 15px rgba(0,0,0,0.06)">
                    <div style="font-size:1.8rem">{reward.split()[0]}</div>
                    <div style="font-family:'Fredoka One',cursive;color:#FF6B6B">{pts}</div>
                    <div style="font-size:0.8rem;color:#666">{' '.join(reward.split()[1:])}</div>
                </div>
                """, unsafe_allow_html=True)
        
        if st.button("🔄 Reset All Points"):
            st.session_state.points = {}
            st.session_state.chore_assignments = {}
            st.success("All points and chores reset!")
            st.rerun()

# TRIVIA TIME
elif page_name == "Trivia Time":
    st.markdown("# 🧠 Family Trivia Time!")
    
    col1, col2, col3 = st.columns(3)
    with col1:
        st.markdown(f"""<div class="fun-card teal" style="text-align:center">
            <div style="font-size:1.5rem">✅</div>
            <div style="font-family:'Fredoka One',cursive;font-size:2rem;color:#4ECDC4">{st.session_state.trivia_score['correct']}</div>
            <div style="color:#888;font-size:0.8rem;font-weight:600">CORRECT</div>
        </div>""", unsafe_allow_html=True)
    with col2:
        st.markdown(f"""<div class="fun-card" style="text-align:center">
            <div style="font-size:1.5rem">📊</div>
            <div style="font-family:'Fredoka One',cursive;font-size:2rem;color:#FF6B6B">{st.session_state.trivia_score['total']}</div>
            <div style="color:#888;font-size:0.8rem;font-weight:600">TOTAL</div>
        </div>""", unsafe_allow_html=True)
    with col3:
        pct = int(st.session_state.trivia_score['correct'] / max(st.session_state.trivia_score['total'], 1) * 100)
        st.markdown(f"""<div class="fun-card orange" style="text-align:center">
            <div style="font-size:1.5rem">🎯</div>
            <div style="font-family:'Fredoka One',cursive;font-size:2rem;color:#FF8E53">{pct}%</div>
            <div style="color:#888;font-size:0.8rem;font-weight:600">ACCURACY</div>
        </div>""", unsafe_allow_html=True)
    
    st.markdown("---")
    
    difficulty = st.select_slider("Choose difficulty", options=["Easy", "Medium", "Hard", "All"])
    
    col1, col2 = st.columns([1, 4])
    with col1:
        if st.button("🎲 New Question"):
            pool = TRIVIA_QUESTIONS if difficulty == "All" else [q for q in TRIVIA_QUESTIONS if q["difficulty"] == difficulty]
            if pool:
                st.session_state.current_question = random.choice(pool)
                st.session_state.answered = False
    with col2:
        if st.button("🔄 Reset Score"):
            st.session_state.trivia_score = {"correct": 0, "total": 0}
            st.session_state.current_question = None
            st.rerun()
    
    if st.session_state.current_question:
        q = st.session_state.current_question
        
        diff_colors = {"Easy": "#D1FAE5", "Medium": "#FDE68A", "Hard": "#FFE4E6"}
        diff_text_colors = {"Easy": "#059669", "Medium": "#D97706", "Hard": "#E11D48"}
        
        st.markdown(f"""
        <div class="fun-card" style="margin-top:1rem">
            <div style="display:flex;align-items:center;gap:0.5rem;margin-bottom:0.75rem">
                <span class="badge" style="background:{diff_colors.get(q['difficulty'],'#eee')};
                             color:{diff_text_colors.get(q['difficulty'],'#333')}">{q['difficulty']}</span>
            </div>
            <h2 style="color:#333 !important;font-size:1.4rem !important">{q['q']}</h2>
        </div>
        """, unsafe_allow_html=True)
        
        if not st.session_state.answered:
            for option in q["options"]:
                if st.button(f"  {option}  ", key=f"opt_{option}", use_container_width=True):
                    st.session_state.trivia_score["total"] += 1
                    if option == q["a"]:
                        st.session_state.trivia_score["correct"] += 1
                        st.balloons()
                        st.success(f"🎉 CORRECT! The answer is {q['a']}!")
                    else:
                        st.error(f"❌ Not quite! The correct answer is **{q['a']}**")
                    st.session_state.answered = True
                    st.rerun()
        else:
            st.info(f"✅ Answer: **{q['a']}**")
            st.markdown("Click '🎲 New Question' to continue!")
    else:
        st.markdown("""
        <div style="text-align:center;padding:3rem;background:white;border-radius:20px;
                    box-shadow:0 8px 30px rgba(0,0,0,0.05)">
            <div style="font-size:4rem">🧠</div>
            <h3 style="color:#888">Press 'New Question' to start!</h3>
        </div>
        """, unsafe_allow_html=True)

# FAMILY TIMER
elif page_name == "Family Timer":
    st.markdown("# ⏱️ Family Timer")
    st.markdown("Perfect for games, activities, and chore timing!")
    
    col1, col2 = st.columns([1, 1])
    
    with col1:
        st.markdown("### Set Timer")
        mins = st.number_input("Minutes", min_value=0, max_value=60, value=5, step=1)
        secs = st.number_input("Seconds", min_value=0, max_value=59, value=0, step=5)
        
        timer_name = st.text_input("What's this timer for?", placeholder="e.g., Clean up time!")
        
        col_a, col_b = st.columns(2)
        with col_a:
            if st.button("▶️ START TIMER", use_container_width=True):
                total_seconds = mins * 60 + secs
                if total_seconds > 0:
                    st.session_state.timer_running = True
                    st.session_state.timer_end = time.time() + total_seconds
                    st.session_state.timer_name = timer_name or "Family Timer"
        with col_b:
            if st.button("⏹️ STOP", use_container_width=True):
                st.session_state.timer_running = False
                st.session_state.timer_end = None
    
    with col2:
        st.markdown("### Timer Display")
        
        if st.session_state.timer_running and st.session_state.timer_end:
            remaining = st.session_state.timer_end - time.time()
            if remaining > 0:
                m = int(remaining // 60)
                s = int(remaining % 60)
                st.markdown(f"""
                <div class="timer-display">
                    <div style="font-size:1rem;color:#888;margin-bottom:0.5rem">{st.session_state.get('timer_name', 'Timer')}</div>
                    <div>{m:02d}:{s:02d}</div>
                    <div style="font-size:1rem;color:#4ECDC4;margin-top:0.5rem">⏱️ Running...</div>
                </div>
                """, unsafe_allow_html=True)
                time.sleep(1)
                st.rerun()
            else:
                st.session_state.timer_running = False
                st.balloons()
                st.markdown("""
                <div class="timer-display" style="background:linear-gradient(135deg,#4ECDC4,#26A69A);color:white">
                    <div style="font-size:3rem">🎉</div>
                    <div>TIME'S UP!</div>
                </div>
                """, unsafe_allow_html=True)
        else:
            total_secs = mins * 60 + secs
            m = total_secs // 60
            s = total_secs % 60
            st.markdown(f"""
            <div class="timer-display" style="opacity:0.6">
                <div style="font-size:1rem;color:#888;margin-bottom:0.5rem">Ready to start</div>
                <div>{m:02d}:{s:02d}</div>
            </div>
            """, unsafe_allow_html=True)
        
        st.markdown("---")
        st.markdown("### ⚡ Quick Timers")
        quick_times = [("1 min", 60), ("3 min", 180), ("5 min", 300), ("10 min", 600)]
        q_cols = st.columns(4)
        for col, (label, seconds) in zip(q_cols, quick_times):
            with col:
                if st.button(label, use_container_width=True, key=f"quick_{seconds}"):
                    st.session_state.timer_running = True
                    st.session_state.timer_end = time.time() + seconds
                    st.session_state.timer_name = f"{label} Timer"
                    st.rerun()

# FAMILY SETUP
elif page_name == "Family Setup":
    st.markdown("# 👥 Family Setup")
    
    col1, col2 = st.columns([1, 1])
    
    with col1:
        st.markdown("### Your Family Members")
        
        for i, member in enumerate(st.session_state.family_members):
            m_col, d_col = st.columns([3, 1])
            with m_col:
                new_name = st.text_input(f"Member {i+1}", value=member, key=f"member_{i}", label_visibility="collapsed")
                if new_name != member:
                    # Update points key if name changed
                    if member in st.session_state.points:
                        pts = st.session_state.points.pop(member)
                        st.session_state.points[new_name] = pts
                    st.session_state.family_members[i] = new_name
            with d_col:
                if st.button("🗑️", key=f"del_{i}") and len(st.session_state.family_members) > 1:
                    if member in st.session_state.points:
                        del st.session_state.points[member]
                    st.session_state.family_members.pop(i)
                    st.rerun()
        
        if len(st.session_state.family_members) < 8:
            if st.button("➕ Add Family Member"):
                st.session_state.family_members.append(f"Member {len(st.session_state.family_members) + 1}")
                st.rerun()
    
    with col2:
        st.markdown("### 📊 Family Stats")
        total_points = sum(st.session_state.points.values())
        total_chores_done = sum(1 for c in st.session_state.chore_assignments.values() if c.get("done"))
        
        st.markdown(f"""
        <div class="fun-card teal">
            <h3>📈 This Week</h3>
            <p>👥 <b>{len(st.session_state.family_members)}</b> family members</p>
            <p>🧹 <b>{total_chores_done}</b> chores completed</p>
            <p>🏆 <b>{total_points}</b> total points earned</p>
            <p>🎯 <b>{len(st.session_state.completed_activities)}</b> activities done</p>
        </div>
        """, unsafe_allow_html=True)
        
        st.markdown("### 🔄 Reset Options")
        if st.button("🔄 Reset Weekly Stats", use_container_width=True):
            st.session_state.chore_assignments = {}
            st.session_state.points = {}
            st.session_state.completed_activities = []
            st.session_state.trivia_score = {"correct": 0, "total": 0}
            st.success("All stats reset for a new week! 🎉")
            st.rerun()
