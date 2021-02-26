from .. import db

class Vehicle(db.Model):
    """
    Create a Vehicles table
    """

    __tablename__ = 'vehicles'

    id = db.Column(db.Integer, primary_key=True)
    brand = db.Column(db.String(60), nullable=False)
    model = db.Column(db.String(200), nullable=False)
    year = db.Column(db.Integer)

    def __repr__(self):
        return '<Vehicle: {} {}>'.format(self.brand, self.model)

    def to_dict(self):
        return {
            "id": self.id,
            "brand": self.brand,
            "model": self.model,
            "year": self.year
        }

