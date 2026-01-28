from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

class Voter(db.Model):
    __tablename__ = 'voters'
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    has_voted = db.Column(db.Boolean, default=False, nullable=False)

class Ballot(db.Model):
    __tablename__ = 'ballots'
    id = db.Column(db.Integer, primary_key=True)
    candidate_id = db.Column(db.String(100), nullable=False)
    timestamp = db.Column(db.DateTime, server_default=db.func.now())
