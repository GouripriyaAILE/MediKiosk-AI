from memory import get_memory, store_memory


def get_patient_memory(patient_name, complaint):
    result = get_memory(
        f"Previous medical history of {patient_name} related to {complaint}"
        
    )

    memories = []

    for memory in result:
        if memory.text not in memories:
            memories.append(memory.text)

    return memories[:3]


def generate_follow_up(memories, complaint):
    if not memories:
        return "How long have you been experiencing this problem?"

    previous_text = " ".join(memories).lower()

    if "cough" in previous_text and "fever" in complaint.lower():
        return (
            "You previously reported cough along with fever. "
            "Are you experiencing cough this time?"
        )

    if "fever" in previous_text:
        return (
            "You previously reported fever. "
            "When did the current fever start?"
        )

    return "Can you tell me more about your current symptoms?"


def store_patient_information(information):
    store_memory(
        information
    )


def ask_question(patient_name, complaint):
    memories = get_patient_memory(patient_name, complaint)

    follow_up = generate_follow_up(
        memories,
        complaint
    )

    return memories, follow_up