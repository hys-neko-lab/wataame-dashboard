from flask import Flask, url_for, redirect
from flask_migrate import Migrate
from flask_sqlalchemy import SQLAlchemy
from flask_wtf.csrf import CSRFProtect
from flask_login import LoginManager

# インスタンス生成とLoginManager設定
db = SQLAlchemy()
csrf = CSRFProtect()
login_manager = LoginManager()
login_manager.login_view = "auth.signin"

def create_app():
    app = Flask(__name__)

    # Flaskのコンフィグ(適宜変更)
    app.config.from_mapping(
        SQLALCHEMY_DATABASE_URI = 
            "mysql://{username}:{password}@{hostname}/{dbname}"
            .format(**{
                'username': 'wata-ame',
                'password': '3qPfyqCYuu_3k',
                'hostname': 'localhost',
                'dbname': 'clouduser'
            }),
        SQLALCHEMY_TRACK_MODIFICATIONS = False,
        SQLALCHEMY_ECHO = False,
        SECRET_KEY = "G9f+djU441GNGrEK",
        WTF_CSRF_SECRET_KEY = "tIynXXTchlWlU5oV",
    )

    # アプリを各々に教えておく
    db.init_app(app)
    Migrate(app, db)
    csrf.init_app(app)
    login_manager.init_app(app)

    # Blueprintの登録
    from apps.dashboard import views as dashboard_views
    from apps.compute import views as compute_views
    from apps.auth import views as auth_views
    from apps.resource import views as resource_views
    from apps.keypair import views as keypair_views
    from apps.network import views as network_views
    from apps.storage import views as storage_views
    from apps.container import views as container_views
    from apps.serverless import views as serverless_views

    app.register_blueprint(dashboard_views.dashboard, url_prefix="/dashboard")
    app.register_blueprint(auth_views.auth, url_prefix="/auth")
    app.register_blueprint(compute_views.compute, url_prefix="/compute")
    app.register_blueprint(resource_views.resource, url_prefix="/resource")
    app.register_blueprint(keypair_views.keypair, url_prefix="/keypair")
    app.register_blueprint(network_views.network, url_prefix="/network")
    app.register_blueprint(storage_views.storage, url_prefix="/storage")
    app.register_blueprint(container_views.container, url_prefix="/container")
    app.register_blueprint(serverless_views.serverless, url_prefix="/serverless")

    """
    新たにサービス追加する場合：
    from apps.sample import views as sample_views
    app.register_blueprint(sample_views.sample, url_prefix="/sample")
    """

    # ルート直下のリソースGETに対する処理
    @app.route("/")
    def index():
        return redirect(url_for("dashboard.index"))

    @app.route("/favicon.ico")
    def favicon():
        return app.send_static_file("favicon.ico")

    return app
