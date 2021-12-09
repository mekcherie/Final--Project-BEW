from sqlalchemy_utils import URLType
from rally_app import db
from rally_app.utils import FormEnum
from flask_login import UserMixin

class eventCategory(FormEnum):
    """Categories of rally events."""
    PRODUCE = 'Produce'
    DELI = 'Deli'
    BAKERY = 'Bakery'
    PANTRY = 'Pantry'
    FROZEN = 'Frozen'
    OTHER = 'Other'

class Rallyspot(db.Model):
    """Rally spot model."""
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(80), nullable=False)
    address = db.Column(db.String(200), nullable=False)
    events = db.relationship('Rallyevent', back_populates='spot')
    created_by_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    created_by = db.relationship('User')        

    def __str__(self):
        return str(self.title)

class Rallyevent(db.Model):
    """Rally event model."""
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80), nullable=False)
    price = db.Column(db.Float(precision=2), nullable=False)
    category = db.Column(db.Enum(eventCategory), default=eventCategory.OTHER)
    photo_url = db.Column(URLType)
    spot_id = db.Column(db.Integer, db.ForeignKey('rally_spot.id'), nullable=False)
    spot = db.relationship('Rallyspot', back_populates='events')
    created_by_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    created_by = db.relationship('User')

class User(db.Model, UserMixin):
    """User model."""
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(50), nullable=False)
    password = db.Column(db.String(150), nullable=False)
    shopping_list_events = db.relationship('Rallyevent', secondary='shopping_list', back_populates = 'shopping_list')
    def __str__(self):
        return f'{self.username}'

shopping_list_table = db.Table('shopping_list',
    db.Column('rallyevent_id', db.Integer, db.ForeignKey('rally_event.id')),
    db.Column('user_id', db.Integer, db.ForeignKey('user.id'))
)