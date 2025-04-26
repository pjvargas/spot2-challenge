from fastapi.testclient import TestClient
from pytest import MonkeyPatch
from spot2_challenge.main import app

client = TestClient(app)

def test_chat_basic(monkeypatch: MonkeyPatch):
    class FakeResponse:
        choices = [
            type('obj', (object,), {
                "message": type('msg', (object,),
                    {
                        "content": '{"data": {"budget": 15000, "city": "New York", "additional_fields": {}}, "reply": "Saved!"}'
                    }
                )()
            })()
        ]

    def fake_create(**kwargs):
        return FakeResponse()

    monkeypatch.setattr("openai.chat.completions.create", fake_create)

    response = client.post("/chat", json={"session_id": "test_basic", "message": "I want an apartment in New York with a 15000 budget"})

    assert response.status_code == 200
    body = response.json()
    assert body["reply"] == "Saved!"
    assert body["collected_fields"]["budget"] == 15000
    assert body["collected_fields"]["city"] == "New York"

def test_chat_updates_existing_session(monkeypatch: MonkeyPatch):
    class FirstFakeResponse:
        choices = [type('obj', (object,), {"message": type('msg', (object,), {"content": '{"data": {"budget": 25000, "city": "Paris", "additional_fields": {}}, "reply": "First save!"}'})()})()]

    def fake_create_first(**kwargs):
        return FirstFakeResponse()

    monkeypatch.setattr("openai.chat.completions.create", fake_create_first)

    session_id = "test_update"

    response1 = client.post("/chat", json={"session_id": session_id, "message": "I want a property in Paris with 25000 budget"})
    assert response1.status_code == 200
    body1 = response1.json()
    assert body1["collected_fields"]["budget"] == 25000
    assert body1["collected_fields"]["city"] == "Paris"

    class SecondFakeResponse:
        choices = [type('obj', (object,), {"message": type('msg', (object,), {"content": '{"data": {"real_estate_type": "apartment"}, "reply": "Type updated!"}'})()})()]

    def fake_create_second(**kwargs):
        return SecondFakeResponse()

    monkeypatch.setattr("openai.chat.completions.create", fake_create_second)

    response2 = client.post("/chat", json={"session_id": session_id, "message": "I'm looking for an apartment"})
    assert response2.status_code == 200
    body2 = response2.json()
    assert body2["collected_fields"]["real_estate_type"] == "apartment"
    assert body2["collected_fields"]["budget"] == 25000
    assert body2["collected_fields"]["city"] == "Paris"

def test_chat_with_additional_fields(monkeypatch: MonkeyPatch):
    class FakeResponse:
        choices = [
            type('obj', (object,), {
                "message": type('msg', (object,), {
                    "content": '{"data": {"budget": 12000, "city": "Barcelona", "additional_fields": {"pet_friendly": "yes"}}, "reply": "Saved with additional info!"}'
                })()
            })()
        ]

    def fake_create(**kwargs):
        return FakeResponse()

    monkeypatch.setattr("openai.chat.completions.create", fake_create)

    response = client.post("/chat", json={"session_id": "test_additional", "message": "I want a pet-friendly apartment in Barcelona with 12000 budget"})

    assert response.status_code == 200
    body = response.json()
    assert body["collected_fields"]["budget"] == 12000
    assert body["collected_fields"]["city"] == "Barcelona"
    assert "pet_friendly" in body["collected_fields"]["additional_fields"] and body["collected_fields"]["additional_fields"]["pet_friendly"] == "yes"

def test_chat_with_partial_data(monkeypatch: MonkeyPatch):
    class FakeResponse:
        choices = [
            type('obj', (object,), {
                "message": type('msg', (object,), {
                    "content": '{"data": {"city": "Tokyo", "additional_fields": {}}, "reply": "Got the city, still need more information."}'
                })()
            })()
        ]

    def fake_create(**kwargs):
        return FakeResponse()

    monkeypatch.setattr("openai.chat.completions.create", fake_create)

    response = client.post("/chat", json={"session_id": "test_partial", "message": "I'm looking for something in Tokyo"})

    assert response.status_code == 200
    body = response.json()
    assert body["collected_fields"]["city"] == "Tokyo"
    assert body["collected_fields"]["budget"] is None
    assert body["collected_fields"]["real_estate_type"] is None

def test_chat_with_invalid_input(monkeypatch: MonkeyPatch):
    class FakeResponse:
        choices = [
            type('obj', (object,), {
                "message": type('msg', (object,), {
                    "content": '{"data": {}, "reply": "I could not detect valid information, could you please clarify?"}'
                })()
            })()
        ]

    def fake_create(**kwargs):
        return FakeResponse()

    monkeypatch.setattr("openai.chat.completions.create", fake_create)

    response = client.post("/chat", json={"session_id": "test_invalid", "message": "asldkfjaslkdfj"})

    assert response.status_code == 200
    body = response.json()
    assert body["collected_fields"]["budget"] is None
    assert body["collected_fields"]["city"] is None
    assert body["collected_fields"]["real_estate_type"] is None
    assert body["collected_fields"]["total_size_requirement"] is None
    assert body["collected_fields"]["additional_fields"] == {}