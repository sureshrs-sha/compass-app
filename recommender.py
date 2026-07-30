# recommender.py
# Takes a user's mastery scores and returns an ordered learning roadmap

from skill_graph import SKILLS

def topological_sort(skills):
    visited = set()
    order = []

    def visit(skill_id):
        if skill_id in visited:
            return
        visited.add(skill_id)
        for prereq in skills[skill_id]["prerequisites"]:
            visit(prereq)
        order.append(skill_id)

    for skill_id in skills:
        visit(skill_id)

    return order

def generate_roadmap(mastery_scores):
    """
    mastery_scores: dict of {skill_id: score (0.0 to 1.0)}
    Returns an ordered list of skills the user should learn next.
    """
    sorted_skills = topological_sort(SKILLS)

    roadmap = []
    for skill_id in sorted_skills:
        score = mastery_scores.get(skill_id, 0.0)

        # Check if prerequisites are sufficiently mastered
        prereqs = SKILLS[skill_id]["prerequisites"]
        prereqs_met = all(mastery_scores.get(p, 0.0) >= 0.5 for p in prereqs)

        # Gap score: how much they still need to learn
        gap_score = 1.0 - score

        # Only include skills they haven't mastered and whose prereqs are met
        if gap_score > 0.2 and prereqs_met:
            roadmap.append({
                "skill_id": skill_id,
                "label": SKILLS[skill_id]["label"],
                "description": SKILLS[skill_id]["description"],
                "gap_score": round(gap_score, 2),
                "current_score": round(score, 2)
            })

    # Sort by gap score (biggest gaps first)
    roadmap.sort(key=lambda x: x["gap_score"], reverse=True)

    return roadmap


if __name__ == "__main__":
    # Quick test
    test_scores = {
        "phone_basics": 0.9,
        "text_messaging": 0.6,
        "email_basics": 0.2,
        "video_calls": 0.0,
        "messaging_apps": 0.0,
        "scam_awareness": 0.0
    }

    roadmap = generate_roadmap(test_scores)
    print("Recommended learning path:")
    for i, skill in enumerate(roadmap, 1):
        print(f"{i}. {skill['label']} (gap: {skill['gap_score']})")
        