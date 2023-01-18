export FLASK_APP=apps.main.py
export FLASK_ENV=development

# ポート5000番はdockerプライベートレジストリのデフォルトと重複する
flask run -h 0.0.0.0 -p 5001