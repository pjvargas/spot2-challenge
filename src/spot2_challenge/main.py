from fastapi import FastAPI
from dotenv import load_dotenv

from spot2_challenge.logic import call_openai
from spot2_challenge.memory import get_or_create_session, update_session
from spot2_challenge.schemas import BotResponse, UserMessage

load_dotenv()

app = FastAPI()

@app.post("/chat", response_model=BotResponse)
def chat(user_message: UserMessage):
    session = get_or_create_session(user_message.session_id)

    result = call_openai(user_message.message, session.fields)

    update_session(
        session_id=user_message.session_id,
        fields_update=result.new_data,
        user_message=user_message.message,
        bot_reply=result.reply
    )

    session = get_or_create_session(user_message.session_id)

    collected = {
        **session.fields.model_dump(exclude_unset=True),
    }

    return BotResponse(
        reply=result.reply,
        collected_fields=collected
    )