from src.app import activities


def test_get_activities_returns_seeded_data(client):
    response = client.get("/activities")

    assert response.status_code == 200
    body = response.json()
    assert "Chess Club" in body
    assert body["Chess Club"]["participants"] == activities["Chess Club"]["participants"]


def test_signup_adds_participant(client):
    email = "new.student@mergington.edu"

    response = client.post("/activities/Chess Club/signup", params={"email": email})

    assert response.status_code == 200
    assert email in activities["Chess Club"]["participants"]


def test_signup_unknown_activity_returns_404(client):
    response = client.post("/activities/Nope/signup", params={"email": "a@mergington.edu"})

    assert response.status_code == 404


def test_signup_duplicate_email_returns_400(client):
    existing = activities["Chess Club"]["participants"][0]

    response = client.post("/activities/Chess Club/signup", params={"email": existing})

    assert response.status_code == 400
    assert activities["Chess Club"]["participants"].count(existing) == 1


def test_signup_full_activity_returns_400(client):
    activity = activities["Chess Club"]
    activity["participants"] = [f"s{i}@mergington.edu" for i in range(activity["max_participants"])]

    response = client.post("/activities/Chess Club/signup", params={"email": "late@mergington.edu"})

    assert response.status_code == 400
    assert "late@mergington.edu" not in activity["participants"]


def test_unregister_removes_participant(client):
    email = activities["Chess Club"]["participants"][0]

    response = client.delete("/activities/Chess Club/unregister", params={"email": email})

    assert response.status_code == 200
    assert email not in activities["Chess Club"]["participants"]


def test_unregister_not_signed_up_returns_400(client):
    response = client.delete(
        "/activities/Chess Club/unregister", params={"email": "nobody@mergington.edu"}
    )

    assert response.status_code == 400


def test_unregister_unknown_activity_returns_404(client):
    response = client.delete("/activities/Nope/unregister", params={"email": "a@mergington.edu"})

    assert response.status_code == 404
