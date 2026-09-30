import streamlit as st
import speech_recognition as sr
from pypdf import PdfReader
from docx import Document
from agent import ask_question, store_patient_information
from summary import generate_summary
from triage import detect_red_flags
from dashboard import show_doctor_dashboard
from integration import show_integration
st.set_page_config(
    page_title="MediKiosk AI",
    page_icon="🩺",
    layout="wide"
)
st.markdown("""
<style>

.main {
    background-color: #f7f9fc;
}

.block-container {
    padding-top: 2rem;
    padding-bottom: 2rem;
}

h1 {
    font-size: 2.5rem;
    font-weight: 700;
}

h2 {
    font-weight: 650;
}

h3 {
    font-weight: 600;
}

[data-testid="stSidebar"] {
    background-color: #f1f5f9;
}

[data-testid="stSidebar"] * {
    color: #1f2937 !important;
}


[data-testid="stSidebar"] h1 {
    font-size: 1.5rem;
}

.stButton > button {
    border-radius: 10px;
    min-height: 45px;
    font-weight: 600;
}

.stTextInput > div > div,
.stTextArea > div > div,
.stSelectbox > div > div {
    border-radius: 10px;
}

.stFileUploader {
    border-radius: 10px;
}
.hero {
    padding: 30px;
    border-radius: 18px;
    background: #e8f1f8;
    margin-bottom: 25px;
}

.hero-title {
    font-size: 2.4rem;
    font-weight: 700;
    color: #12344d !important;
}

.hero-subtitle {
    font-size: 1.3rem;
    font-weight: 600;
    margin-top: 6px;
    color: #28536b !important;
}

.hero-description {
    font-size: 1rem;
    margin-top: 12px;
    line-height: 1.6;
    color: #374151 !important;
}
.section-card {
    background: white;
    padding: 22px;
    border-radius: 15px;
    margin: 15px 0;
    border: 1px solid #e5e7eb;
}

.section-title {
    font-size: 1.35rem;
    font-weight: 700;
    color: #12344d !important;
}

.section-subtitle {
    margin-top: 5px;
    color: #4b5563 !important;
}
.sidebar-status {
    padding: 14px;
    border-radius: 12px;
    background: white;
    border: 1px solid #e5e7eb;
    color: #374151 !important;
    font-size: 0.9rem;
    line-height: 1.6;
}


</style>
""", unsafe_allow_html=True)

st.divider()
st.sidebar.title("🩺 MediKiosk")
st.sidebar.caption("Patient Case-Taking System")

st.sidebar.divider()

menu = st.sidebar.radio(
    "Navigate",
    [
        "📝 Patient Case-Taking",
        "🔄 New Consultation",
        "👨‍⚕️ Doctor Dashboard",
        "🔗 HIS + ABDM"
    ]
)
st.sidebar.divider()

st.sidebar.markdown("""
<div class="sidebar-status">
    <b>🟢 System Status</b><br>
    MediKiosk AI is ready
</div>
""", unsafe_allow_html=True)
if menu == "🔗 HIS + ABDM":
    show_integration()
if menu == "🔄 New Consultation":
    st.header("🔄 New Consultation")

    consultation_name = st.text_input(
        "Patient Name",
        key="nav_consultation_name"
    )

    consultation_complaint = st.text_area(
        "Current Health Problem",
        key="nav_consultation_complaint"
    )

    if st.button("🔍 Recall Previous History", key="nav_recall"):

        if consultation_name and consultation_complaint:

            previous_memories, follow_up = ask_question(
                consultation_name,
                consultation_complaint
            )

            st.subheader("🧠 Previous Information")

            if previous_memories:
                for memory in previous_memories:
                    st.info(memory)
            else:
                st.info("No previous information found.")

            st.subheader("💬 Adaptive Follow-up")
            st.write(follow_up)

        else:
            st.warning(
                "Please enter the patient's name and current complaint."
            )
if menu == "👨‍⚕️ Doctor Dashboard":

    data = st.session_state.get("patient_data", {})

    if data:

        show_doctor_dashboard(
            data["patient_name"],
            data["age"],
            data["complaint"],
            data["previous_memories"],
            data["ayush_data"],
            data["document_text"],
            data["red_flags"],
            data["clinical_summary"]
        )

    else:
        st.warning(
            "Please complete the patient case-taking first."
        )
if "show_dashboard" not in st.session_state:
    st.session_state.show_dashboard = False
if "patient_data" not in st.session_state:
    st.session_state.patient_data = {}
st.markdown("""
<div class="hero">
    <div class="hero-title">🩺 MediKiosk AI</div>
    <div class="hero-subtitle">
        Intelligent Patient Case-Taking & Clinical History Assistant
    </div>
    <div class="hero-description">
        Capture patient information through voice and touch,
        recall previous history, digitize medical documents,
        and prepare a structured clinical summary for the physician.
    </div>
</div>
""", unsafe_allow_html=True)



st.divider()

st.markdown("""
<div class="section-card">
    <div class="section-title">👤 Patient Registration</div>
    <div class="section-subtitle">
        Enter the patient's basic information to begin the consultation.
    </div>
</div>
""", unsafe_allow_html=True)




patient_name = st.text_input("Patient Name")

age = st.number_input(
    "Age",
    min_value=1,
    max_value=120,
    step=1
)
st.divider()
st.markdown("""
<div class="section-card">
    <div class="section-title">🌿 AYUSH Patient Assessment</div>
    <div class="section-subtitle">
        Provide the following information for the patient's clinical history.
    </div>
</div>
""", unsafe_allow_html=True)
prakriti = st.selectbox(
    "1. Prakriti (Body Constitution)",
    ["Select", "Vata", "Pitta", "Kapha", "Vata-Pitta", "Pitta-Kapha", "Vata-Kapha", "Tridosha"]
)

vikriti = st.selectbox(
    "2. Vikriti (Current Imbalance)",
    ["Select", "Vata", "Pitta", "Kapha", "Vata-Pitta", "Pitta-Kapha", "Vata-Kapha", "Tridosha"]
)

sara = st.selectbox(
    "3. Sara (Tissue Quality)",
    ["Select", "Excellent", "Good", "Average", "Poor"]
)

samhanana = st.selectbox(
    "4. Samhanana (Body Compactness)",
    ["Select", "Well-developed", "Moderate", "Poor"]
)

pramana = st.selectbox(
    "5. Pramana (Body Measurements)",
    ["Select", "Proportionate", "Underweight", "Overweight"]
)

satmya = st.selectbox(
    "6. Satmya (Adaptability)",
    ["Select", "Good", "Moderate", "Poor"]
)

sattva = st.selectbox(
    "7. Sattva (Mental Strength)",
    ["Select", "Strong", "Moderate", "Weak"]
)

ahara_shakti = st.selectbox(
    "8. Ahara Shakti (Digestive Capacity)",
    ["Select", "High", "Moderate", "Low"]
)

vyayama_shakti = st.selectbox(
    "9. Vyayama Shakti (Exercise Capacity)",
    ["Select", "High", "Moderate", "Low"]
)

vaya = st.selectbox(
    "10. Vaya (Age)",
    ["Select", "Bala – Childhood", "Madhya – Adult", "Vriddha – Elderly"]
)
st.divider()
st.markdown("""
<div class="section-card">
    <div class="section-title">📄 Medical Document Upload</div>
    <div class="section-subtitle">
        Upload prescriptions, laboratory reports, or discharge summaries.
    </div>
</div>
""", unsafe_allow_html=True)

uploaded_file = st.file_uploader(
    "Upload your prescription, lab report, or discharge summary",
    type=["pdf", "docx"]
)
extracted_text = ""
if uploaded_file is not None:
    st.success(f"Uploaded: {uploaded_file.name}")

    

    if uploaded_file.name.endswith(".pdf"):
        reader = PdfReader(uploaded_file)

        for page in reader.pages:
            text = page.extract_text()
            if text:
                extracted_text += text + "\n"

    elif uploaded_file.name.endswith(".docx"):
        document = Document(uploaded_file)

        for paragraph in document.paragraphs:
            extracted_text += paragraph.text + "\n"

    if extracted_text.strip():
        st.subheader("📋 Digitized Medical Information")
        st.text_area(
            "Extracted text",
            extracted_text,
            height=250
        )
    else:
        st.warning(
            "No readable text was found in this document."
        )
st.divider()

st.markdown("""
<div class="section-card">
    <div class="section-title">🩺 Health Information</div>
    <div class="section-subtitle">
        Describe the patient's current health concern using text or voice.
    </div>
</div>
""", unsafe_allow_html=True)

complaint = st.text_area(
    "What is your main health problem?",
    placeholder="Example: I have fever and cough..."
)
st.write("🎤 Or speak your health problem")

if st.button("🎙️ Start Voice Input"):
    recognizer = sr.Recognizer()

    try:
        with sr.Microphone() as source:
            st.info("Listening... Please speak now.")
            audio = recognizer.listen(source, timeout=5, phrase_time_limit=10)

        voice_text = recognizer.recognize_google(audio)

        st.success("Voice captured successfully!")
        st.write("You said:")
        st.write(voice_text)

        st.session_state["voice_complaint"] = voice_text

    except sr.WaitTimeoutError:
        st.warning("No speech detected. Please try again.")

    except sr.UnknownValueError:
        st.warning("Sorry, I could not understand your voice.")

    except sr.RequestError:
        st.error("Speech recognition service is unavailable.")
if "voice_complaint" in st.session_state:
    complaint = st.session_state["voice_complaint"]

if st.button("Continue"):
    st.session_state.show_dashboard = False
    if not patient_name or not complaint:
        st.warning("Please enter your name and health problem.")

    else:

        # 1. Recall previous information FIRST
        previous_memories, follow_up = ask_question(
            patient_name,
            complaint
        )
        st.session_state.patient_data["patient_name"] = patient_name
        st.session_state.patient_data["age"] = age
        st.session_state.patient_data["complaint"] = complaint
        st.session_state.patient_data["previous_memories"] = previous_memories
        ayush_data = {
        "Prakriti": prakriti,
        "Vikriti": vikriti,
        "Sara": sara,
        "Samhanana": samhanana,
        "Pramana": pramana,
        "Satmya": satmya,
        "Sattva": sattva,
        "Ahara Shakti": ahara_shakti,
        "Vyayama Shakti": vyayama_shakti,
        "Vaya": vaya
        }
        st.session_state.patient_data["ayush_data"] = ayush_data
        clinical_summary = generate_summary(
          patient_name,
          age,
          complaint,
          ayush_data,
          previous_memories,
          extracted_text if uploaded_file else ""
        ) 
        st.session_state.patient_data["clinical_summary"] = clinical_summary
        red_flags = detect_red_flags(
            complaint + " " + extracted_text
        )
        st.session_state.patient_data["red_flags"] = red_flags
        st.session_state.patient_data["document_text"] = extracted_text

        st.subheader("🚨 Triage Check")

        if red_flags:
            st.error("⚠️ Priority Alert")

            for alert in red_flags:
                st.write("•", alert)

            st.warning(
                "Please inform medical staff for appropriate assessment."
            )
        else:
            st.success("No predefined red-flag terms detected.")
    
    st.subheader("🧾 Clinical History Summary")
 
    st.text_area(
    "Physician-ready summary",
    clinical_summary,
    height=500
    )
    st.success("Information recorded successfully.")

    st.subheader("🧠 Hindsight Memory Recall")
    st.caption(
    "Previous patient information is recalled to support "
    "more relevant follow-up questions."
    )

    if previous_memories:

            st.info(
                "I found previous information related to this complaint."
            )

            for memory in previous_memories:
                st.write("•", memory)

    else:

            st.info(
                "This appears to be new information for this patient."
            )
    st.subheader("Adaptive Follow-up Question")

    st.write(f"💬 {follow_up}")
        # 2. Store current visit AFTER recall
    information = f"""
        Patient {patient_name} is {age} years old.

        Current complaint: {complaint}

        AYUSH Assessment:
        Prakriti: {prakriti}
        Vikriti: {vikriti}
        Sara: {sara}
        Samhanana: {samhanana}
        Pramana: {pramana}
        Satmya: {satmya}
        Sattva: {sattva}
        Ahara Shakti: {ahara_shakti}
        Vyayama Shakti: {vyayama_shakti}
        Vaya: {vaya}
        """
     

    store_patient_information(information)
st.divider()

if st.button("👨‍⚕️ Open Doctor Dashboard"):
    st.session_state.show_dashboard = True

if st.session_state.show_dashboard:

    data = st.session_state.patient_data

    if data:
        show_doctor_dashboard(
            data["patient_name"],
            data["age"],
            data["complaint"],
            data["previous_memories"],
            data["ayush_data"],
            data["document_text"],
            data["red_flags"],
            data["clinical_summary"]
        )
    else:
        st.warning("Please complete the patient information first.")
st.divider()

st.subheader("🔄 Consultation")

if st.button("🆕 Start New Consultation"):
    st.session_state.show_dashboard = False
    st.session_state.new_consultation = True
    st.success("New consultation started.")
if st.session_state.get("new_consultation", False):

    st.header("🧑‍⚕️ New Patient Consultation")

    consultation_name = st.text_input(
        "Patient Name",
        key="consultation_name"
    )

    consultation_complaint = st.text_area(
        "What is your current health problem?",
        key="consultation_complaint"
    )

    if st.button("🔍 Recall Previous History"):

        if consultation_name and consultation_complaint:

            previous_memories, follow_up = ask_question(
                consultation_name,
                consultation_complaint
            )

            st.subheader("🧠 Previous Information")

            if previous_memories:
                for memory in previous_memories:
                    st.info(memory)
            else:
                st.info("No previous information found.")

            st.subheader("💬 Adaptive Follow-up")

            st.write(follow_up)

        else:
            st.warning(
                "Please enter the patient's name and current complaint."
            )
st.divider()

st.subheader("🔗 Health Record Integration")

if st.button("🏥 Open HIS + ABDM Integration"):
    st.session_state.show_integration = True

if st.session_state.get("show_integration", False):
    show_integration()