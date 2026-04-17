from flask import Flask
from extensions import db, jwt
from flask_cors import CORS

def create_app():
    app = Flask(__name__)
    CORS(app)

    app.config.from_object("config.Config")

    db.init_app(app)
    jwt.init_app(app)

    from routes.auth_routes import auth_bp
    from routes.chat_routes import chat_bp

    app.register_blueprint(auth_bp)
    app.register_blueprint(chat_bp)

    from database.models import User

    with app.app_context():
        db.create_all()

    return app


app = create_app()

if __name__ == "__main__":
    app.run(debug=True)
