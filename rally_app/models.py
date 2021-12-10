from sqlalchemy_utils import URLType
from rally_app import db
from rally_app.utils import FormEnum
from flask_login import UserMixin


class eventCategory(FormEnum):
    """Categories of rally events."""
    ETHIOPIAN = 'Ethiopian'
    ERITREAN = 'Eritrean'
    AFGANTISTIAN = 'Afgantistian'
    ISREAL = 'Isreal'
    IRAQ = 'Iraq'
    OTHER = 'Other'


class RallyLocation(db.Model):
    """Rally spot model."""
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(80), nullable=False)
    address = db.Column(db.String(200), nullable=False)
    event_id = db.Column(db.Integer, db.ForeignKey('rally_event.id'))
    event = db.relationship("RallyEvent", back_populates="location")

    def __str__(self):
        return str(self.title)


class RallyEvent(db.Model):
    """Rally event model."""
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80), nullable=False)
    price = db.Column(db.Float(precision=2), nullable=False)
    category = db.Column(db.Enum(eventCategory), default=eventCategory.OTHER)
    photo_url = db.Column(URLType)
    location = db.relationship("RallyLocation", back_populates="event")

class User(db.Model, UserMixin):
    """User model."""
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(50), nullable=False)
    password = db.Column(db.String(150), nullable=False)
    # shopping_list_events = db.relationship(
        # 'RallyEvent', secondary='event_location', back_populates='event_location')

    def __str__(self):
        return f'{self.username}'


event_location_table = db.Table('event_location',
                                db.Column('event_id', db.Integer,
                                          db.ForeignKey('rally_event.id')),
                                db.Column('location_id', db.Integer,
                                          db.ForeignKey('rally_location.id'))
                                )

event_user_table = db.Table('event_user',
                            db.Column('user_id', db.Integer,
                                      db.ForeignKey('user.id')),
                            db.Column('event_id', db.Integer,
                                      db.ForeignKey('rally_event.id'))
                            )