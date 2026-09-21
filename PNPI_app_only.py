import streamlit as st
import pandas as pd
from PIL import Image, ImageFilter
import base64
from io import BytesIO

st.set_page_config(page_title="PNPI - Pak Navy Polytechnic Institute", layout="wide", page_icon="⚓")

def get_base64_blurred_flag():
    try:
        img = Image.new("RGB", (1920, 1080), "#01411C")
        for x in range(300):
            for y in range(1080):
                img.putpixel((x, y), (255, 255, 255))
        img = img.filter(ImageFilter.GaussianBlur(radius=50))
        buf = BytesIO()
        img.save(buf, format="PNG")
        return base64.b64encode(buf.getvalue()).decode()
    except Exception:
        return ""

bg_image = get_base64_blurred_flag()

st.markdown(f"""
<style>
[data-testid="stAppViewContainer"] {{
    background-image:url("data:image/png;base64,{bg_image}");
    background-size:cover;
    background-position:center;
    background-attachment:fixed;
}}
[data-testid="stHeader"] {{background:rgba(0,0,0,0);}}
[data-testid="stSidebar"] {{background-color:rgba(255,255,255,.92);}}
h1,h2,h3,h4,h5,h6,p,div {{
    color:#0b3d2e;
    font-family:"Segoe UI",Tahoma,Geneva,Verdana,sans-serif;
}}
.stButton>button {{
    background-color:#01411C;
    color:white;
    border-radius:10px;
    border:none;
    padding:10px 24px;
    font-weight:bold;
}}
.stButton>button:hover {{background-color:#025c2b;color:white;}}
</style>
""", unsafe_allow_html=True)

# Header
c1, c2 = st.columns([1, 4])
with c1:
    try:
        st.image(Image.open("logo.png"), width=150)
    except Exception:
        st.info("Add logo.png")
with c2:
    st.title("Pak Navy Polytechnic Institute (PNPI)")
    st.subheader("West Wharf Road, Karachi")

st.markdown("---")

choice = st.sidebar.selectbox("Navigation Menu", [
    "Home", "Mechatronic Engineering", "Faculty & Courses",
    "Student Results", "Campus Life"
])

# Home
if choice == "Home":
    st.header("Welcome to PNPI")
    try:
        st.image(Image.open("college.png"), caption="PNPI Campus", use_container_width=True)
    except Exception:
        st.info("Add college.png")
    st.write("""
    **Pak Navy Polytechnic Institute (PNPI)** is a technical education
    institution located at West Wharf Road, Karachi. The institute focuses
    on practical technical education, innovation, engineering skills, and
    professional development.
    """)
    st.info("📍 Location: West Wharf Road, Karachi, Pakistan")
    st.info("🏫 Total Classrooms: 20 Modern Classrooms")

# Mechatronic Engineering
elif choice == "Mechatronic Engineering":
    st.header("Mechatronic Engineering Technology")
    st.write("""
    Our Mechatronic Engineering program integrates mechanical, electronics,
    computer, and control systems. It is designed as a 5-semester technical
    program with theoretical and practical learning.
    """)

    st.subheader("Classrooms")
    try:
        st.image(Image.open("classroom.png"),
                 caption="20 Classrooms available for students",
                 use_container_width=True)
    except Exception:
        st.info("Add classroom.png")

    st.subheader("Semester Breakdown & Subjects")
    sem_data = {
        "Semester 1": ["Applied Mathematics","Applied Physics","Basic Electrical Engineering","Workshop Practice","Computer Fundamentals","Engineering Drawing","Communication Skills","Islamic Studies"],
        "Semester 2": ["Applied Mathematics II","Electronic Devices","Digital Logic Design","Mechanical Workshop","Programming Fundamentals","Technical Writing","Pakistan Studies"],
        "Semester 3": ["Microprocessors","Electrical Machines","Fluid Mechanics","Instrumentation","CAD/CAM","Industrial Management","Professional Ethics"],
        "Semester 4": ["Robotics & Automation","Control Systems","PLC & SCADA","Embedded Systems","Project Management"],
        "Semester 5": ["Mechatronics System Design","Industrial IoT","AI in Automation","Final Year Project","Industrial Training"]
    }
    for sem, subjects in sem_data.items():
        with st.expander(f"📘 {sem} — 8 Students per Class"):
            for subject in subjects:
                st.write(f"• {subject}")

    st.subheader("Mechatronic Labs")
    for col, filename, caption in zip(
        st.columns(3),
        ["lab1.png","lab2.png","lab3.png"],
        ["Electronics Lab","Robotics Lab","Automation Lab"]
    ):
        with col:
            try:
                st.image(Image.open(filename), caption=caption, use_container_width=True)
            except Exception:
                st.info(f"Add {filename}")

# Faculty
elif choice == "Faculty & Courses":
    st.header("Faculty & Study Courses")
    st.subheader("Our Faculty")
    teachers = {
        "Engr. Ahmed Khan": "Head of Mechatronics Department",
        "Dr. Sana Malik": "Senior Lecturer — Mathematics",
        "Engr. Bilal Hussain": "Lab Instructor — Robotics",
        "Prof. Fatima Ali": "Lecturer — Electrical Engineering",
        "Engr. Usman Tariq": "Lecturer — Computer Systems"
    }
    for name, role in teachers.items():
        st.write(f"👨‍🏫 **{name}** — {role}")

    st.subheader("Study Course Overview")
    st.write("""
    The Mechatronic Engineering course is designed around modern industrial
    requirements. Students study mechanical systems, electronics,
    programming, automation, robotics, control systems, and practical
    laboratory applications.
    """)

    st.subheader("📚 PNPI Central Library")
    try:
        st.image(Image.open("library.png"), caption="PNPI Central Library",
                 use_container_width=True)
    except Exception:
        st.info("Add library.png")

# Results
elif choice == "Student Results":
    st.header("Student Result Portal")
    st.write("Enter your details to view the sample Semester 1 result.")

    with st.form("login_form"):
        student_name = st.text_input("Student Name")
        roll_number = st.text_input("Roll Number")
        submit = st.form_submit_button("View Result")

    if submit:
        if student_name.strip() and roll_number.strip():
            st.success(f"Welcome, {student_name.strip()} ({roll_number.strip()})")

            subjects_marks = {
                "Applied Mathematics": 75,
                "Applied Physics": 55,
                "Basic Electrical Engineering": 80,
                "Workshop Practice": 65,
                "Computer Fundamentals": 45,
                "Engineering Drawing": 70,
                "Communication Skills": 50,
                "Islamic Studies": 85
            }

            df = pd.DataFrame(list(subjects_marks.items()),
                              columns=["Subject", "Marks (%)"])
            df["Status"] = df["Marks (%)"].apply(
                lambda x: "PASS" if x >= 60 else "FAIL"
            )
            fail_count = sum(x < 60 for x in subjects_marks.values())

            st.subheader("Semester 1 Result")
            st.dataframe(df, use_container_width=True, hide_index=True)
            st.metric("Average Marks", f"{df['Marks (%)'].mean():.1f}%")
            st.metric("Failed Subjects", fail_count)

            st.markdown("### Final Status")
            if fail_count == 0:
                st.success("🎉 PASS — Excellent Performance!")
            elif fail_count <= 2:
                st.warning(f"⚠️ RE-EXAM REQUIRED — {fail_count} subject(s) are below the passing mark.")
            else:
                st.error(f"❌ FAIL — {fail_count} subjects are below the passing mark.")
        else:
            st.error("Please enter both Student Name and Roll Number.")

# Campus Life
elif choice == "Campus Life":
    st.header("Campus Life at PNPI")
    st.subheader("🏏 Cricket Group")

    for col, filename, caption in zip(
        st.columns(3),
        ["cricket1.png","cricket2.png","cricket3.png"],
        ["Cricket Practice","Bowling Practice","Match Day"]
    ):
        with col:
            try:
                st.image(Image.open(filename), caption=caption, use_container_width=True)
            except Exception:
                st.info(f"Add {filename}")

    st.subheader("☕ College Canteen")
    try:
        st.image(Image.open("canteen.png"),
                 caption="Student Canteen — Relax & Recharge",
                 use_container_width=True)
    except Exception:
        st.info("Add canteen.png")

    st.write("Our canteen provides a comfortable place for students and staff to relax and enjoy food and refreshments.")

st.markdown("---")
st.caption("⚓ Pak Navy Polytechnic Institute (PNPI) | West Wharf Road, Karachi | Mechatronic Engineering")
