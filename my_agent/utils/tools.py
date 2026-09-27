def get_default_topic() -> str:
    return "Python lists"


def get_topic_details(topic: str) -> dict:
    topic_data = {
        "Python lists": {
            "difficulty": "beginner",
            "category": "python",
            "description": "A list stores multiple values in one variable."
        },
        "Machine learning": {
            "difficulty": "intermediate",
            "category": "ai",
            "description": "A method where systems learn patterns from data."
        },
    }
    return topic_data.get(topic, {
        "difficulty": "beginner",
        "category": "general",
        "description": "General topic explanation."
    })
