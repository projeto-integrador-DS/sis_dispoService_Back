from login import login_manager

from app import app


login_manager.init_app(app)


