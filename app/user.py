from app import login_manager
from flask_login import UserMixin

fake_db = {'admin': {'password': 'p@$$w0rd'}}

@login_manager.user_loader
def load_user(email: str):  # could also be an asynchronous function
    user = fake_db.get(email)
    return user
