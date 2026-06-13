"""
Tests for the Mergington High School Activities API

These tests verify the core functionality of the FastAPI application:
- Retrieving all available activities
- Signing up a student for an activity
- Unregistering a student from an activity
"""

import pytest
from fastapi.testclient import TestClient
from src.app import app


@pytest.fixture
def client():
    """Create a TestClient for the FastAPI application"""
    return TestClient(app)


def test_get_activities(client):
    """Test retrieving all available activities"""
    # Arrange
    # No setup needed; activities are predefined in the app
    
    # Act
    response = client.get("/activities")
    
    # Assert
    assert response.status_code == 200
    activities = response.json()
    assert isinstance(activities, dict)
    assert "Chess Club" in activities
    assert "Programming Class" in activities
    assert "Gym Class" in activities
    
    # Verify activity structure
    chess_club = activities["Chess Club"]
    assert "description" in chess_club
    assert "schedule" in chess_club
    assert "max_participants" in chess_club
    assert "participants" in chess_club


def test_signup_success(client):
    """Test successfully signing up a student for an activity"""
    # Arrange
    email = "newstudent@mergington.edu"
    activity_name = "Basketball Team"
    response = client.get("/activities")
    initial_participants = len(response.json()[activity_name]["participants"])
    
    # Act
    response = client.post(
        f"/activities/{activity_name}/signup",
        params={"email": email}
    )
    
    # Assert
    assert response.status_code == 200
    result = response.json()
    assert "message" in result
    assert email in result["message"]
    assert activity_name in result["message"]
    
    # Verify the participant was added
    response = client.get("/activities")
    updated_participants = response.json()[activity_name]["participants"]
    assert len(updated_participants) == initial_participants + 1
    assert email in updated_participants


def test_unregister_success(client):
    """Test successfully unregistering a student from an activity"""
    # Arrange
    email = "michael@mergington.edu"
    activity_name = "Chess Club"
    response = client.get("/activities")
    initial_participants = response.json()[activity_name]["participants"]
    assert email in initial_participants
    initial_count = len(initial_participants)
    
    # Act
    response = client.delete(
        f"/activities/{activity_name}/signup",
        params={"email": email}
    )
    
    # Assert
    assert response.status_code == 200
    result = response.json()
    assert "message" in result
    assert email in result["message"]
    assert activity_name in result["message"]
    
    # Verify the participant was removed
    response = client.get("/activities")
    updated_participants = response.json()[activity_name]["participants"]
    assert len(updated_participants) == initial_count - 1
    assert email not in updated_participants
