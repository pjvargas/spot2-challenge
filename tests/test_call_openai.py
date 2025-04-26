from pytest import MonkeyPatch
from spot2_challenge.logic import call_openai
from spot2_challenge.schemas import ResponseFields

def test_call_openai_returns_valid_response(monkeypatch: MonkeyPatch):
    class FakeResponse:
        choices = [
            type('obj', (object,), {
                "message": type('msg', (object,), 
                {
                    "content": '{"data": {"budget": 10000, "city": "Lima", "additional_fields": {}}, "reply": "Got it!"}'
                })()
            })()
        ]

    def fake_create(**kwargs):
        return FakeResponse()

    monkeypatch.setattr("openai.chat.completions.create", fake_create)

    fields = ResponseFields()
    result = call_openai("I want a house", fields)

    assert result.new_data.budget == 10000
    assert result.new_data.city == "Lima"
    assert result.reply == "Got it!"