from flask import Flask

def create_app(config_class=None):
    app = Flask(__name__)

    if config_class is None:
        from app.config import Config
        app.config.from_object(Config)
    else:
        app.config.from_object(config_class)

    from app.extensions import db, login_manager
    db.init_app(app)
    login_manager.init_app(app)

    from app.auth import auth_bp
    from app.books import books_bp
    from app.authors import authors_bp

    app.register_blueprint(auth_bp)
    app.register_blueprint(books_bp)
    app.register_blueprint(authors_bp)

    from app.models.user import User

    @login_manager.user_loader
    def load_user(user_id):
        return User.query.get(int(user_id))

    login_manager.login_view = 'auth.login'
    login_manager.login_message = 'Please log in to access this page.'
    login_manager.login_message_category = 'info'

    return app