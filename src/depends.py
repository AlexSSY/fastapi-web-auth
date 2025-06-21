from fastapi import Depends, Cookie, HTTPException

from . import config, db, storage


session_token_dep = Cookie(default=None, alias=config.COOKIE_NAME)


def get_current_user(session_token = session_token_dep):
    user_class = config.get_user_class()
    
    if session_token is None:
        raise HTTPException(status_code=401, detail='session_token not provided')
    
    user_id = storage.retrieve(session_token)
    if user_id is None:
        raise HTTPException(status_code=401, detail='invalid session_token')
    
    with db.SessionLocal() as session:
        user = session.get(user_class, user_id)
        if user is None:
            raise HTTPException(status_code=401, detail='session_token expired')
        return user


user_dependency = Depends(get_current_user)
