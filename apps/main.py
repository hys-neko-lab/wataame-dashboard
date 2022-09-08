from flask import Flask, url_for, redirect
from flask_migrate import Migrate
from flask_sqlalchemy import SQLAlchemy
from flask_wtf.csrf import CSRFProtect
from flask_login import LoginManager

# インスタンス生成とLoginManagerのエンドポイント設定
db = SQLAlchemy()
csrf = CSRFProtect()
login_manager = LoginManager()
login_manager.login_view = "auth.signin"
login_manager.login_message = ""

def create_app():
    app = Flask(__name__)

    # Flaskのコンフィグ(適宜変更)
    app.config.from_mapping(
        SQLALCHEMY_DATABASE_URI=f"mysql://wata-ame:3qPfyqCYuu_3k@localhost/clouduser",
        SQLALCHEMY_TRACK_MODIFICATIONS=False,
        SECRET_KEY = "G9f+djU441GNGrEK",
        WTF_CSRF_SECRET_KEY="tIynXXTchlWlU5oV",
    )

    # アプリを各々に教えておく
    db.init_app(app)
    Migrate(app, db)
    csrf.init_app(app)
    login_manager.init_app(app)

    # Blueprintの登録
    from apps.dashboard import views as dashboard_views
    app.register_blueprint(dashboard_views.dashboard, url_prefix="/dashboard")

    from apps.auth import views as auth_views
    app.register_blueprint(auth_views.auth, url_prefix="/auth")

    from apps.compute import views as compute_views
    app.register_blueprint(compute_views.compute, url_prefix="/compute")

    from apps.resource import views as resource_views
    app.register_blueprint(resource_views.resource, url_prefix="/resource")

    from apps.keypair import views as keypair_views
    app.register_blueprint(keypair_views.keypair, url_prefix="/keypair")

    from apps.network import views as network_views
    app.register_blueprint(network_views.network, url_prefix="/network")

    from apps.storage import views as storage_views
    app.register_blueprint(storage_views.storage, url_prefix="/storage")

    from apps.container import views as container_views
    app.register_blueprint(container_views.container, url_prefix="/container")

    from apps.serverless import views as serverless_views
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