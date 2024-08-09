from config import db

class Lifter(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80), unique=True, nullable=False)
    weight = db.Column(db.Float, unique=False, nullable=False)
    
    # Relationship with PositionalPoint
    positional_points = db.relationship('PositionalPoints', backref='lifter', cascade="all, delete-orphan")

    def to_json(self):
        return {
            'id': self.id,
            "name": self.name,
            "weight": self.weight,
            "positionalPoints": [point.to_json() for point in self.positional_points]
        }

class PositionalPoints(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    points = db.Column(db.String(250), nullable=False)
    distances = db.Column(db.String(250), nullable=False)
    
    # Foreign key to Lifter
    lifter_id = db.Column(db.Integer, db.ForeignKey('lifter.id'), nullable=False)

    def to_json(self):
        return {
            'id': self.id,
            "points": self.points,
            "distances": self.distances
        }
    
class Resource(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80), unique=True, nullable=False)
    program = db.Column(db.String(100), unique=False, nullable=False)
    
    # Relationship with PositionalPoint
    links = db.relationship('Link', backref='Resource', cascade="all, delete-orphan")

    def to_json(self):
        return {
            'id': self.id,
            "name": self.name,
            "program": self.program,
            "links": [point.to_json() for point in self.links]
        }
    
class Link(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    link = db.Column(db.String(250), nullable=False)
    
    # Foreign key to Lifter
    resource_id = db.Column(db.Integer, db.ForeignKey('resource.id'), nullable=False)

    def to_json(self):
        return {
            'id': self.id,
            "link": self.link,
        }
