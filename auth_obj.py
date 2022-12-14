from functools import wraps
from hashlib import sha1
from flask import redirect, url_for, render_template, make_response
from secrets import token_urlsafe

SECRET_KEY = "ELECdiagrams"

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
        def inner(*args, **kwargs):
            session_id = self.session.get("id")
            session_token = self.session.get("token")
            user = self.users.query.filter_by(id=session_id).first()
            if user:
                if user.token == session_token:
                    return func(*args, **kwargs)
            return redirect(url_for(self.url_redirect))
        return inner

    @staticmethod
    def encrypt_psw(pwd):
        key = sha1(pwd.encode("utf-8"))
        key.update(SECRET_KEY.encode("utf-8"))
        return key.hexdigest()

    def login_check(self, func):
        @wraps(func)
        def inner(*args):
            if self.request.method == "POST" and len(self.request.form) == 2: #check the len of the form to distinguish between login or new_user form
                user_email = self.request.form["email"]
                user_pwd = self.encrypt_psw(self.request.form["pwd"])
                user = self.users.query.filter_by(email=user_email).first()
                if user:
                    if user.pwd == user_pwd:
                        user.token = token_urlsafe()
                        self.session["id"] = user.id
                        self.session["token"] = user.token
                        self.db.session.add(user)
                        self.db.session.commit()
                        res = make_response(redirect(url_for(self.home_url)))
                        res.set_cookie("name", user.name)
                        return res
                return render_template("login.html", message="**User or password incorrect**")    
            return func(*args)
        return inner
        