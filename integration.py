import streamlit as st


def show_integration():

    st.title("🔗 HIS + ABDM Integration")

    st.write(
        "Mock integration screen for sending the collected clinical "
        "history to the hospital information system and ABDM ecosystem."
    )

    st.divider()

    st.subheader("🏥 Hospital Information System (HIS)")

    st.text_input("Hospital ID", value="MEDI-HOSP-001")
    st.text_input("Patient ID", value="Generated after registration")

    if st.button("📤 Send to HIS"):
        st.success("Clinical history successfully sent to HIS (Demo).")

    st.divider()

    st.subheader("🪪 ABDM Integration")

    st.text_input("ABHA ID", placeholder="Enter ABHA ID")

    if st.button("🔄 Sync with ABDM"):
        st.success("Patient information synced with ABDM (Demo).")

    st.divider()

    st.info(
        "⚠️ This is a prototype integration. "
        "No real hospital or ABDM data is transmitted."
    )