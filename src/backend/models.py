from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

class Movie(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(250), nullable=False)
    release_date = db.Column(db.String(50))
    vote_average = db.Column(db.Float)
    overview = db.Column(db.Text()) 
    poster_path = db.Column(db.String(250))