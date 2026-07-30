# assessment.py
# Defines the assessment questions and scoring logic

QUESTIONS = [
    {
        "skill_id": "phone_basics",
        "question": "Can you turn on your phone and open an app?",
        "options": [
            ("Not at all", 0.0),
            ("I need help with this", 0.2),
            ("I can do it sometimes", 0.5),
            ("Yes, I can do this comfortably", 1.0)
        ]
    },
    {
        "skill_id": "text_messaging",
        "question": "Can you send a text message to a friend or family member?",
        "options": [
            ("Not at all", 0.0),
            ("I need help with this", 0.2),
            ("I can do it sometimes", 0.5),
            ("Yes, I can do this comfortably", 1.0)
        ]
    },
    {
        "skill_id": "email_basics",
        "question": "Can you read and reply to an email?",
        "options": [
            ("Not at all", 0.0),
            ("I need help with this", 0.2),
            ("I can do it sometimes", 0.5),
            ("Yes, I can do this comfortably", 1.0)
        ]
    },
    {
        "skill_id": "video_calls",
        "question": "Can you make a video call using FaceTime or Zoom?",
        "options": [
            ("Not at all", 0.0),
            ("I need help with this", 0.2),
            ("I can do it sometimes", 0.5),
            ("Yes, I can do this comfortably", 1.0)
        ]
    },
    {
        "skill_id": "messaging_apps",
        "question": "Can you send a message using WhatsApp or Facebook Messenger?",
        "options": [
            ("Not at all", 0.0),
            ("I need help with this", 0.2),
            ("I can do it sometimes", 0.5),
            ("Yes, I can do this comfortably", 1.0)
        ]
    },
    {
        "skill_id": "scam_awareness",
        "question": "Can you spot a suspicious message or email that might be a scam?",
        "options": [
            ("Not at all", 0.0),
            ("I need help with this", 0.2),
            ("I can do it sometimes", 0.5),
            ("Yes, I can do this comfortably", 1.0)
        ]
    },
]

def compute_mastery(answers):
    """
    answers: dict of {skill_id: score (0.0 to 1.0)}
    Returns a mastery scores dict.
    """
    return answers
