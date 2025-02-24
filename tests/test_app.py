import pytest
import sys
import os

# Ensure the project root is in sys.path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from app import app  # Import the Flask app

@pytest.fixture
def client():
    """Creates a test client for the Flask app."""
    app.testing = True
    return app.test_client()

def test_home(client):
    """Test the home page route."""
    response = client.get('/')
    assert response.status_code == 200
    assert b"<!DOCTYPE html>" in response.data  # Ensures it returns an HTML page

def test_resume_1(client):
    """Test the /resume_1 route."""
    response = client.get('/resume_1')
    assert response.status_code == 200
    assert b"<!DOCTYPE html>" in response.data

def test_resume_2(client):
    """Test the /resume_2 route."""
    response = client.get('/resume_2')
    assert response.status_code == 200
    assert b"<!DOCTYPE html>" in response.data

def test_resume_template(client):
    """Test the /resume_template route."""
    response = client.get('/resume_template')
    assert response.status_code == 200
    assert b"<!DOCTYPE html>" in response.data

if __name__ == "__main__":
    pytest.main()