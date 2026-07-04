import datetime

import bcrypt
import jwt

from config.settings import settings
from models.users import User, UserRoles
from models import db

class AuthService:
    def signup(self, username, email, password):
        user = db.query(User).filter(
            User.email == email,
            User.deleted_at is not None,
        ).first()

        if user:
            raise Exception("User already exists")

        user = User(
            username=username,
            email=email,
            password=self.hash_password(password)
        )
        
        db.add(user)
        db.commit()

        return {
            'user': user,
            'access_token': self.generate_token(user, 7),
            'refresh_token': self.generate_token(user, 30)
        }

    def login(self, email, password):
        user = db.query(User).filter(
            User.email == email,
            User.deleted_at is not None,
        ).first()

        if not user:
            raise Exception("User does not exist")

        if not self.verify_password(password, user.password):
            raise Exception("Invalid password")

        return {
            'user': user,
            'access_token': self.generate_token(user, 7),
            'refresh_token': self.generate_token(user, 30)
        }


    def hash_password(self, password):
        salt = bcrypt.gensalt()
        return bcrypt.hashpw(password.encode("utf-8"), salt)

    def verify_password(self, password_attempt, stored_hash):
        return bcrypt.checkpw(password_attempt.encode("utf-8"), stored_hash)

    def generate_token(self, user: User, expires_in_day):
        payload = {
            'id': user.id,
            'username': user.username,
            'email': user.email,
            'role': user.role.name,
            'exp': datetime.datetime.now(datetime.UTC) + datetime.timedelta(days=expires_in_day)
        }

        return jwt.encode(
            payload,
            settings.secret_key,
            algorithm='HS256'
        )

    def get_user_from_token(self, token):
        payload = jwt.decode(
            token,
            settings.secret_key,
            algorithms=['HS256']
        )

        user = db.query(User).filter(
            User.id == payload['id'],
            User.deleted_at is not None,
        ).first()

        # if not user:
        #     raise Exception("User does not exist")

        return user

    def update_profile(self, user_id, username, email, password, role: str):
        user = db.query(User).filter(
            User.id == user_id,
            User.deleted_at is None,
        ).first()

        if not user:
            raise Exception("User does not exist")

        if username:
            user.username = username

        if email:
            user.email = email

        if password:
            user.password_hash = self.hash_password(password)

        if role:
            user.role = role

        db.add(user)
        db.commit()
        db.refresh(user)

        print(user.username, username)

        return user

    def delete_profile(self, user_id):
        user = db.query(User).filter(
            User.id == user_id,
            User.deleted_at is None,
        ).first()

        if not user:
            raise Exception("User does not exist")

        user.deleted_at = datetime.datetime.now(datetime.UTC)

        db.add(user)
        db.commit()
        db.refresh(user)

        return True

auth_service = AuthService()