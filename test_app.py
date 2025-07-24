import pytest
import requests
import json
from unittest.mock import patch, MagicMock
from app import app, GITHUB_API_BASE_URL

@pytest.fixture
def client():
    """Configures the Flask test client."""
    app.config['TESTING'] = True
    with app.test_client() as client:
        yield client

def test_get_octocat_gists_success(client):
    """
    Tests the /octocat endpoint for successful gist retrieval.
    Mocks the requests.get call to simulate GitHub API response.
    """
    mock_gists_data = [
        {"id": "123", "public": True, "description": "test gist 1", "url": "https://api.github.com/gists/123"},
        {"id": "456", "public": True, "description": "test gist 2", "url": "https://api.github.com/gists/456"},
        {"id": "789", "public": False, "description": "private gist", "url": "https://api.github.com/gists/789"} # Should be filtered out
    ]
    
    with patch('requests.get') as mock_get:
        mock_response = MagicMock()
        mock_response.status_code = 200
        mock_response.json.return_value = mock_gists_data
        mock_response.raise_for_status.return_value = None # No HTTP error
        mock_get.return_value = mock_response

        response = client.get("/octocat")
        data = json.loads(response.data)

        assert response.status_code == 200
        assert isinstance(data, list)
        assert len(data) == 2  # Only public gists
        assert any(gist['id'] == '123' for gist in data)
        assert any(gist['id'] == '456' for gist in data)
        assert not any(gist['id'] == '789' for gist in data) # Ensure private is excluded
        mock_get.assert_called_once_with(f"{GITHUB_API_BASE_URL}/users/octocat/gists")

def test_get_non_existent_user_gists(client):
    """
    Tests the API for a non-existent user, expecting a 404 response.
    Mocks a 404 from GitHub API.
    """
    with patch('requests.get') as mock_get:
        mock_response = MagicMock()
        mock_response.status_code = 404
        mock_response.json.return_value = {"message": "Not Found"}
        mock_response.raise_for_status.side_effect = requests.exceptions.HTTPError(response=mock_response)
        mock_get.return_value = mock_response

        response = client.get("/nonexistentuser123")
        data = json.loads(response.data)

        assert response.status_code == 404
        assert "error" in data
        assert "not found or has no public gists" in data["error"]
        mock_get.assert_called_once_with(f"{GITHUB_API_BASE_URL}/users/nonexistentuser123/gists")

def test_github_api_internal_error(client):
    """
    Tests the API when GitHub API returns a 500 error.
    """
    with patch('requests.get') as mock_get:
        mock_response = MagicMock()
        mock_response.status_code = 500
        mock_response.json.return_value = {"message": "Server Error"}
        mock_response.raise_for_status.side_effect = requests.exceptions.HTTPError(response=mock_response)
        mock_get.return_value = mock_response

        response = client.get("/someuser")
        data = json.loads(response.data)

        assert response.status_code == 500
        assert "error" in data
        assert "Failed to retrieve gists from GitHub API." in data["error"]
        mock_get.assert_called_once_with(f"{GITHUB_API_BASE_URL}/users/someuser/gists")

def test_network_connection_error(client):
    """
    Tests the API when there's a network connection issue to GitHub API.
    """
    with patch('requests.get') as mock_get:
        mock_get.side_effect = requests.exceptions.ConnectionError("Test connection error")

        response = client.get("/anyuser")
        data = json.loads(response.data)

        assert response.status_code == 500
        assert "error" in data
        assert "Cannot connect to GitHub API." in data["error"]
        mock_get.assert_called_once_with(f"{GITHUB_API_BASE_URL}/users/anyuser/gists")

def test_empty_username(client):
    """
    Tests that requesting the root path or empty user returns a JSON 404 error
    """
    response = client.get("/") # Accessing root with no user
    data = json.loads(response.data)

    assert response.status_code == 404 # Flask's default for unmatched routes
    assert "error" in data
    assert "Resource not found or invalid URL." in data["error"]
    assert response.headers['Content-Type'] == 'application/json'
