from typing import Dict
import fakeredis
import json

from spot2_challenge.schemas import ResponseFields, SessionData
from spot2_challenge.logging import logger

r = fakeredis.FakeStrictRedis()

def get_or_create_session(session_id: str) -> SessionData:
    existing = r.get(session_id)
    if existing:
        session_data = json.loads(existing)
        logger.info(f"Session {session_id} found in Redis: {session_data}")
        return SessionData(**json.loads(existing))
    
    logger.info(f"Session {session_id} not found. Creating new session.")
    
    new_session = SessionData(
        fields=ResponseFields(), 
        history=[]
    )
    r.set(session_id, new_session.model_dump_json())

    logger.info(f"New session {session_id} created: {new_session.model_dump()}")

    return new_session

def update_session(
    session_id: str, 
    fields_update: ResponseFields, 
    user_message: str, 
    bot_reply: str
):
    session = get_or_create_session(session_id)

    logger.info(f"Updating session {session_id} with fields: {fields_update.model_dump(exclude_unset=True)}")

    session.fields = session.fields.model_copy(update=fields_update.model_dump(exclude_unset=True))
    session.history.append({"role": "user", "content": user_message})
    session.history.append({"role": "assistant", "content": bot_reply})

    r.set(session_id, session.model_dump_json())

    logger.info(f"Session {session_id} updated and saved: {session.model_dump()}")