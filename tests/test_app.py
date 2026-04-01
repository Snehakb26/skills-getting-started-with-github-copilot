def test_root_redirect(client):
    """Test that GET / redirects to /static/index.html"""
    response = client.get("/")
    assert response.status_code == 200
    assert response.url.path == "/static/index.html"


def test_get_activities(client):
    """Test GET /activities returns all activities"""
    response = client.get("/activities")
    assert response.status_code == 200
    data = response.json()
    assert isinstance(data, dict)
    assert "Chess Club" in data
    assert "Programming Class" in data
    # Check structure of one activity
    chess_club = data["Chess Club"]
    assert "description" in chess_club
    assert "schedule" in chess_club
    assert "max_participants" in chess_club
    assert "participants" in chess_club
    assert isinstance(chess_club["participants"], list)


def test_signup_success(client):
    """Test successful signup for an activity"""
    response = client.post("/activities/Chess%20Club/signup", params={"email": "newstudent@mergington.edu"})
    assert response.status_code == 200
    data = response.json()
    assert "message" in data
    assert "newstudent@mergington.edu" in data["message"]
    assert "Chess Club" in data["message"]

    # Verify the participant was added
    response = client.get("/activities")
    activities = response.json()
    assert "newstudent@mergington.edu" in activities["Chess Club"]["participants"]


def test_signup_activity_not_found(client):
    """Test signup for non-existent activity"""
    response = client.post("/activities/NonExistent/signup", params={"email": "test@mergington.edu"})
    assert response.status_code == 404
    data = response.json()
    assert "detail" in data
    assert "Activity not found" in data["detail"]


def test_signup_already_signed_up(client):
    """Test signup when already signed up"""
    # First signup
    client.post("/activities/Chess%20Club/signup", params={"email": "test@mergington.edu"})
    # Try again
    response = client.post("/activities/Chess%20Club/signup", params={"email": "test@mergington.edu"})
    assert response.status_code == 400
    data = response.json()
    assert "detail" in data
    assert "already signed up" in data["detail"]


def test_unregister_success(client):
    """Test successful unregister from an activity"""
    # First signup
    client.post("/activities/Programming%20Class/signup", params={"email": "removeme@mergington.edu"})
    # Then unregister
    response = client.delete("/activities/Programming%20Class/signup", params={"email": "removeme@mergington.edu"})
    assert response.status_code == 200
    data = response.json()
    assert "message" in data
    assert "removeme@mergington.edu" in data["message"]
    assert "Programming Class" in data["message"]

    # Verify the participant was removed
    response = client.get("/activities")
    activities = response.json()
    assert "removeme@mergington.edu" not in activities["Programming Class"]["participants"]


def test_unregister_activity_not_found(client):
    """Test unregister from non-existent activity"""
    response = client.delete("/activities/NonExistent/signup", params={"email": "test@mergington.edu"})
    assert response.status_code == 404
    data = response.json()
    assert "detail" in data
    assert "Activity not found" in data["detail"]


def test_unregister_not_signed_up(client):
    """Test unregister when not signed up"""
    response = client.delete("/activities/Chess%20Club/signup", params={"email": "notsignedup@mergington.edu"})
    assert response.status_code == 404
    data = response.json()
    assert "detail" in data
    assert "not signed up" in data["detail"]