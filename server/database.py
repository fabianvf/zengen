# Set up your database connection, schema, and data access functions
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

class Koan(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    koan_text = db.Column(db.String, nullable=False)
    image_url = db.Column(db.String, nullable=True)  # nullable=True allows for koans without images
