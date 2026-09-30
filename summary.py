def generate_summary(
    patient_name,
    age,
    complaint,
    ayush_data,
    previous_memories,
    document_text
):
    summary = f"""
CLINICAL HISTORY SUMMARY
========================

Patient Name: {patient_name}
Age: {age}

CHIEF COMPLAINT
---------------
{complaint}

PREVIOUS INFORMATION
--------------------
"""

    if previous_memories:
        for memory in previous_memories:
            summary += f"- {memory}\n"
    else:
        summary += "No previous information found.\n"

    summary += """

AYUSH ASSESSMENT
----------------
"""

    for key, value in ayush_data.items():
        summary += f"{key}: {value}\n"

    summary += """

MEDICAL DOCUMENT INFORMATION
----------------------------
"""

    if document_text and document_text.strip():
        summary += document_text
    else:
        summary += "No medical document uploaded."

    summary += """

--------------------------------
This summary contains collected
patient information for clinical
review. It is not a diagnosis.
"""

    return summary