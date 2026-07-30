# skill_graph.py
# Defines the digital literacy skill graph as a DAG

SKILLS = {
    "phone_basics": {
        "label": "Phone Basics",
        "description": "Turning on your phone, navigating the home screen, and opening apps.",
        "prerequisites": []
    },
    "text_messaging": {
        "label": "Text Messaging",
        "description": "Sending and receiving text messages.",
        "prerequisites": ["phone_basics"]
    },
    "email_basics": {
        "label": "Email Basics",
        "description": "Reading, writing, and sending emails.",
        "prerequisites": ["phone_basics"]
    },
    "video_calls": {
        "label": "Video Calls",
        "description": "Making video calls using apps like FaceTime or Zoom.",
        "prerequisites": ["text_messaging"]
    },
    "messaging_apps": {
        "label": "Messaging Apps",
        "description": "Using apps like WhatsApp or Facebook Messenger.",
        "prerequisites": ["text_messaging"]
    },
    "scam_awareness": {
        "label": "Scam Awareness",
        "description": "Identifying and avoiding online scams and suspicious messages.",
        "prerequisites": ["email_basics", "messaging_apps"]
    },
}

