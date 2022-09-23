from functools import wraps
from flask import redirect, url_for
from secrets import token_urlsafe

class Auth:

    def __init__(self, session, users, url_redirect: str, home_url: str, request: object, db):
        self.session = session
        self.users = users
        self.url_redirect = url_redirect
        self.request = request
        self.db = db
        self.home_url = home_url

    def auth(self, func):
        @wraps(func)
        def inner(*args):
            session_id = self.session.get("id")
            session_token = self.session.get("token")
            user = self.users.query.filter_by(id=session_id).first()
            if user:
                if user.token == session_token:
                    return func(*args)
            return redirect(url_for(self.url_redirect))
        return inner

    def login_check(self, func):
        @wraps(func)
        def inner(*args):
            if self.request.method == "POST":
                print(self.request.form)
                user_email = self.request.form["email"]
                user_pwd = self.request.form["pwd"]
                user = self.users.query.filter_by(email=user_email).first()
                if user:
                    if user.pwd == user_pwd:
                        user.token = token_urlsafe()
                        self.session["id"] = user.id
                        self.session["token"] = user.token
                        self.db.session.add(user)
                        self.db.session.commit()
                        return redirect(url_for(self.home_url))
            return func(*args)
        return inner
        