export FLASK_APP=apps.main.py
export FLASK_ENV=development

flask db init
flask db migrate
flask db upgrade