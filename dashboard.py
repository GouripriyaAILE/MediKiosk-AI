import streamlit as st


def show_doctor_dashboard(
    patient_name,
    age,
    complaint,
    previous_memories,
    ayush_data,
    document_text,
    red_flags,
    clinical_summary
):
    st.title("👨‍⚕️ Doctor Dashboard")
    st.write("Patient clinical information collected by MediKiosk.")

    st.divider()

    # Patient Details
    st.header("👤 Patient Details")
    st.write(f"**Name:** {patient_name}")
    st.write(f"**Age:** {age}")

    st.divider()

    # Chief Complaint
    st.header("🩺 Chief Complaint")
    st.write(complaint)

    st.divider()

    # Previous History
    st.header("🧠 Previous History")

    if previous_memories:
        for memory in previous_memories:
            st.write("•", memory)
    else:
        st.write("No previous history found.")

    st.divider()

    # AYUSH Assessment
    st.header("🌿 AYUSH Assessment")

    for key, value in ayush_data.items():
        st.write(f"**{key}:** {value}")

    st.divider()

    # Medical Documents
    st.header("📄 Medical Documents")

    if document_text:
        st.text_area(
            "Extracted Medical Information",
            document_text,
            height=200
        )
    else:
        st.write("No medical document uploaded.")

    st.divider()

    # Triage
    st.header("🚨 Triage")

    if red_flags:
        st.error("⚠️ Priority Alert")

        for alert in red_flags:
            st.write("•", alert)
    else:
        st.success("No predefined red-flag terms detected.")

    st.divider()

    # Clinical Summary
    st.header("🧾 Clinical History Summary")

    st.text_area(
        "Physician-ready Summary",
        clinical_summary,
        height=400
    )