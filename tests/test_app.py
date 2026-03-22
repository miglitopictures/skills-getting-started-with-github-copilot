import pytest
from fastapi.testclient import TestClient
from src.app import app

client = TestClient(app)

# Initial activities data for reference (mirrors the in-memory data in app.py)
initial_activities = {
    "Chess Club": {
        "description": "Learn strategies and compete in chess tournaments",
        "schedule": "Fridays, 3:30 PM - 5:00 PM",
        "max_participants": 12,
        "participants": ["michael@mergington.edu", "daniel@mergington.edu"]
    },
    "Programming Class": {
        "description": "Learn programming fundamentals and build software projects",
        "schedule": "Tuesdays and Thursdays, 3:30 PM - 4:30 PM",
        "max_participants": 20,
        "participants": ["emma@mergington.edu", "sophia@mergington.edu"]
    },
    "Gym Class": {
        "description": "Physical education and sports activities",
        "schedule": "Mondays, Wednesdays, Fridays, 2:00 PM - 3:00 PM",
        "max_participants": 30,
        "participants": ["john@mergington.edu", "olivia@mergington.edu"]
    },
    "Basketball Team": {
        "description": "Competitive basketball team for intramural and regional tournaments",
        "schedule": "Mondays and Thursdays, 4:00 PM - 5:30 PM",
        "max_participants": 15,
        "participants": ["james@mergington.edu"]
    },
    "Tennis Club": {
        "description": "Learn and practice tennis skills on the school courts",
        "schedule": "Tuesdays and Saturdays, 3:00 PM - 4:30 PM",
        "max_participants": 12,
        "participants": ["lucas@mergington.edu", "ava@mergington.edu"]
    },
    "Art Studio": {
        "description": "Explore painting, drawing, and sculpture techniques",
        "schedule": "Wednesdays and Fridays, 3:30 PM - 5:00 PM",
        "max_participants": 18,
        "participants": ["isabella@mergington.edu"]
    },
    "Music Band": {
        "description": "Join the school band and perform at concerts and events",
        "schedule": "Mondays and Wednesdays, 4:00 PM - 5:30 PM",
        "max_participants": 25,
        "participants": ["mia@mergington.edu", "noah@mergington.edu"]
    },
    "Debate Club": {
        "description": "Develop critical thinking and public speaking through competitive debates",
        "schedule": "Tuesdays, 3:30 PM - 5:00 PM",
        "max_participants": 16,
        "participants": ["alexander@mergington.edu"]
    },
    "Science Club": {
        "description": "Conduct experiments and explore advanced scientific concepts",
        "schedule": "Thursdays, 3:30 PM - 5:00 PM",
        "max_participants": 20,
        "participants": ["grace@mergington.edu", "benjamin@mergington.edu"]
    }
}

class TestRootEndpoint:
    def test_root_redirect(self):
        response = client.get("/")
        assert response.status_code == 200
        assert response.url.path == "/static/index.html"

class TestActivitiesEndpoint:
    def test_get_activities_success(self):
        response = client.get("/activities")
        assert response.status_code == 200
        data = response.json()
        assert isinstance(data, dict)
        assert len(data) == 9  # Based on initial data
        assert "Chess Club" in data
        assert data["Chess Club"]["description"] == initial_activities["Chess Club"]["description"]
        assert data["Chess Club"]["participants"] == initial_activities["Chess Club"]["participants"]

class TestSignupEndpoint:
    def test_signup_success(self):
        # Sign up a new student for an existing activity
        response = client.post("/activities/Chess Club/signup?email=newstudent@mergington.edu")
        assert response.status_code == 200
        data = response.json()
        assert data["message"] == "Signed up newstudent@mergington.edu for Chess Club"
        
        # Verify the student was added
        response = client.get("/activities")
        activities = response.json()
        assert "newstudent@mergington.edu" in activities["Chess Club"]["participants"]

    def test_signup_activity_not_found(self):
        response = client.post("/activities/NonExistent Activity/signup?email=test@mergington.edu")
        assert response.status_code == 404
        data = response.json()
        assert data["detail"] == "Activity not found"

    def test_signup_already_signed_up(self):
        # First, sign up
        client.post("/activities/Programming Class/signup?email=test@mergington.edu")
        
        # Try to sign up again
        response = client.post("/activities/Programming Class/signup?email=test@mergington.edu")
        assert response.status_code == 400
        data = response.json()
        assert data["detail"] == "Student already signed up for this activity"

class TestUnregisterEndpoint:
    def test_unregister_success(self):
        # First, sign up a student
        client.post("/activities/Tennis Club/signup?email=test@mergington.edu")
        
        # Then unregister
        response = client.delete("/activities/Tennis Club/signup?email=test@mergington.edu")
        assert response.status_code == 200
        data = response.json()
        assert data["message"] == "Unregistered test@mergington.edu from Tennis Club"
        
        # Verify the student was removed
        response = client.get("/activities")
        activities = response.json()
        assert "test@mergington.edu" not in activities["Tennis Club"]["participants"]

    def test_unregister_activity_not_found(self):
        response = client.delete("/activities/NonExistent Activity/signup?email=test@mergington.edu")
        assert response.status_code == 404
        data = response.json()
        assert data["detail"] == "Activity not found"

    def test_unregister_not_signed_up(self):
        response = client.delete("/activities/Gym Class/signup?email=notsignedup@mergington.edu")
        assert response.status_code == 400
        data = response.json()
        assert data["detail"] == "Student not signed up for this activity"