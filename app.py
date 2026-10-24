"""App factory.  OWNER: Person 1 (Backend lead).

Run locally:   flask --app app run --debug
Deploy:        gunicorn "app:create_app()"
"""
from flask import Flask, redirect, url_for
from flask_login import current_user
from werkzeug.middleware.proxy_fix import ProxyFix

from config import Config
from extensions import db, login_manager, limiter, csrf


def create_app():
    app = Flask(__name__)

    # Render puts the app behind a proxy. ProxyFix makes Flask see the real visitor's
    # IP address and the https scheme. Without it, the rate limiter would treat every
    # visitor as the same person and block everyone after a few requests.
    app.wsgi_app = ProxyFix(app.wsgi_app, x_for=1, x_proto=1, x_host=1)

    app.config.from_object(Config)

    db.init_app(app)
    login_manager.init_app(app)
    limiter.init_app(app)
    csrf.init_app(app)

    import models  # noqa: F401  (registers the models and the user_loader)
    from routes.auth import bp as auth_bp
    from routes.cards import bp as cards_bp
    from routes.found import bp as found_bp
    from routes.reports import bp as reports_bp

    app.register_blueprint(auth_bp)
    app.register_blueprint(cards_bp)
    app.register_blueprint(found_bp)
    app.register_blueprint(reports_bp)

    @app.route("/")
    def index():
        if current_user.is_authenticated:
            return redirect(url_for("cards.dashboard"))
        return redirect(url_for("auth.login"))

    @app.route("/healthz")
    def healthz():
        # Used by Render to check the app is alive. Does not touch the database.
        return "ok", 200

    with app.app_context():
        db.create_all()

    return app


if __name__ == "__main__":
    create_app().run(debug=True)