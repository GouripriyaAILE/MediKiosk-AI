RED_FLAGS = {
    "chest pain": "Chest pain reported",
    "difficulty breathing": "Difficulty breathing reported",
    "breathing difficulty": "Breathing difficulty reported",
    "severe bleeding": "Severe bleeding reported",
    "unconscious": "Loss of consciousness reported",
    "fainted": "Fainting reported",
    "seizure": "Seizure reported",
    "severe abdominal pain": "Severe abdominal pain reported",
    "stroke": "Possible stroke-related symptom mentioned"
}


def detect_red_flags(text):
    text = text.lower()

    alerts = []

    for keyword, message in RED_FLAGS.items():
        if keyword in text:
            alerts.append(message)

    return list(set(alerts))