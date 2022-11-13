from testapp import app
from testapp import db

with app.app_context():
    db.create_all()