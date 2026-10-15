from copy import deepcopy

from fastapi.testclient import TestClient

import src.app as app_module


client = TestClient(app_module.app)


def reset_activities():
    app_module.activities = deepcopy({
        "Chess Club": {
            "description": "Learn strategies and compete in chess tournaments",
            "schedule": "Fridays, 3:30 PM - 5:00 PM",
            "max_participants": 12,
            "participants": ["michael@mergington.edu", "daniel@mergington.edu"],
        },
        "Programming Class": {
            "description": "Learn programming fundamentals and build software projects",
            "schedule": "Tuesdays and Thursdays, 3:30 PM - 4:30 PM",
            "max_participants": 20,
            "participants": ["emma@mergington.edu", "sophia@mergington.edu"],
        },
        "Gym Class": {
            "description": "Physical education and sports activities",
            "schedule": "Mondays, Wednesdays, Fridays, 2:00 PM - 3:00 PM",
            "max_participants": 30,
            "participants": ["john@mergington.edu", "olivia@mergington.edu"],
        },
    })


def test_duplicate_signup_is_rejected():
    reset_activities()

    response = client.post("/activities/Chess%20Club/signup?email=michael@mergington.edu")

    assert response.status_code == 409
    assert "already signed up" in response.json()["detail"].lower()


def test_signup_rejects_when_activity_is_full():
    reset_activities()
    activity = "Chess Club"
    activity_data = app_module.activities[activity]
    activity_data["participants"] = [f"user{i}@mergington.edu" for i in range(activity_data["max_participants"])]

    response = client.post(f"/activities/{activity.replace(' ', '%20')}/signup?email=new@mergington.edu")

    assert response.status_code == 409
    assert "full" in response.json()["detail"].lower()


def test_invalid_email_is_rejected():
    reset_activities()

    response = client.post("/activities/Chess%20Club/signup?email=not-an-email")

    assert response.status_code == 422
