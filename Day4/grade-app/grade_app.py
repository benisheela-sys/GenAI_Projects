import streamlit as st
import pandas as pd

st.set_page_config(
    page_title="Student Grade Manager",
    page_icon="📚",
    layout="wide"
)

# ---------- Session State ----------
if "students" not in st.session_state:
    st.session_state.students = []

if "reset_form" not in st.session_state:
    st.session_state.reset_form = False


# ---------- Grade Function ----------
def calculate_grade(mark):
    if mark >= 90:
        return "A+"
    elif mark >= 80:
        return "A"
    elif mark >= 70:
        return "B"
    elif mark >= 60:
        return "C"
    elif mark >= 50:
        return "D"
    else:
        return "F"


# ---------- Reset Values Before Widgets ----------
if st.session_state.reset_form:
    name_default = ""
    mark_default = 0
    st.session_state.reset_form = False
else:
    name_default = ""
    mark_default = 0


# ---------- Page Title ----------
st.title("📚 Student Grade Manager")

st.subheader("Add Student")

# ---------- Form ----------
with st.form("student_form", clear_on_submit=True):

    name = st.text_input("Student Name")

    mark = st.number_input(
        "Mark",
        min_value=0,
        max_value=100,
        value=0,
        step=1
    )

    submitted = st.form_submit_button("➕ Add Student")

    if submitted:
        if name.strip():

            st.session_state.students.append(
                {
                    "Name": name,
                    "Mark": mark,
                    "Grade": calculate_grade(mark)
                }
            )

            st.success(f"✅ {name} added successfully!")

        else:
            st.error("Please enter a student name.")


# ---------- Display Data ----------
if st.session_state.students:

    df = pd.DataFrame(st.session_state.students)

    st.subheader("📋 Student Records")

    st.dataframe(
        df,
        use_container_width=True,
        hide_index=True
    )

    average_mark = df["Mark"].mean()
    highest_mark = df["Mark"].max()
    lowest_mark = df["Mark"].min()

    st.subheader("📊 Statistics")

    col1, col2, col3 = st.columns(3)

    with col1:
        st.metric(
            "Class Average",
            f"{average_mark:.2f}"
        )

    with col2:
        st.metric(
            "Highest Mark",
            int(highest_mark)
        )

    with col3:
        st.metric(
            "Lowest Mark",
            int(lowest_mark)
        )

else:
    st.info("No students added yet.")