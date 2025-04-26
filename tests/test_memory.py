from pytest import MonkeyPatch
from spot2_challenge.memory import get_or_create_session, update_session
from spot2_challenge.schemas import ResponseFields

import fakeredis
import json

def test_get_or_create_session_creates_new(monkeypatch: MonkeyPatch):
    monkeypatch.setattr("spot2_challenge.memory.r", fakeredis.FakeStrictRedis())
    session = get_or_create_session("1")
    assert session.fields is not None
    assert session.history == []

def test_update_session(monkeypatch: MonkeyPatch):
    redis_mock = fakeredis.FakeStrictRedis()
    monkeypatch.setattr("spot2_challenge.memory.r", redis_mock)

    fields = ResponseFields(budget=20000, additional_fields={"view": "park"})
    update_session("2", fields, "User message", "Bot reply")

    stored = json.loads(redis_mock.get("2"))
    assert stored["fields"]["budget"] == 20000
    assert stored["fields"]["additional_fields"]["view"] == "park"
    assert stored["history"][0]["role"] == "user"
    assert stored["history"][1]["role"] == "assistant"