from flask_sqlalchemy import SQLAlchemy

# Initialize SQLAlchemy without binding it to an app yet
db = SQLAlchemy()

class Lead(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(100), unique=True, nullable=False)
    company = db.Column(db.String(100), nullable=True)

    def __repr__(self):
        return f'<Lead {self.name}>'
