from basemodel import (
    Model,
    db
)
from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash




class User(UserMixin, Model):
    """Model for user accounts."""

    __tablename__ = 'flasklogin'
    __table_args__ = {'extend_existing': True}

    id = db.Column(db.Integer,
                   primary_key=True)
    name = db.Column(db.String,
                     nullable=False,
                     unique=False)
    email = db.Column(db.String(40),
                      unique=True,
                      nullable=False)
    password = db.Column(db.String(200),
                         primary_key=False,
                         unique=False,
                         nullable=False)
    website = db.Column(db.String(60),
                        index=False,
                        unique=False,
                        nullable=True)
    created_on = db.Column(db.DateTime,
                           index=False,
                           unique=False,
                           nullable=True)
    last_login = db.Column(db.DateTime,
                           index=False,
                           unique=False,
                           nullable=True)


    def set_password(self, password):
        """Create hashed password."""
        self.password = generate_password_hash(password, method='sha256')

    def check_password(self, password):
        """Check hashed password."""
        return check_password_hash(self.password, password)

    def __repr__(self):
        return '<User {}>'.format(self.username)


class Channels(Model):
    """Model for user accounts."""

    __tablename__ = 'channels'
    __table_args__ = {'extend_existing': True}

    id = db.Column(db.Integer,
                   primary_key=True)
    channel_name = db.Column(db.String,
                     nullable=False,
                     unique=False)
    playlist_id = db.Column(db.String(100),
                      unique=True,
                      nullable=True)
    username = db.Column(db.String(200),
                         primary_key=False,
                         unique=False,
                         nullable=False)
    password = db.Column(db.String(100),
                        index=False,
                        unique=False,
                        nullable=True)
    category = db.Column(db.String(50),
                         primary_key=False,
                         unique=False,
                         nullable=False)
    xmlrpc = db.Column(db.String(150),
                        index=False,
                        unique=False,
                        nullable=True)
    time_created = db.Column(db.DateTime,
                           index=False,
                           unique=False,
                           nullable=True)
    channel_id = db.Column(db.Boolean,
                         primary_key=False,
                         unique=False,
                         nullable=False)
    youtube_id = db.Column(db.String,
                         primary_key=False,
                         unique=False,
                         nullable=False)
    """
    website = db.Column(db.Integer,
                     nullable=False,
                     unique=False)
    """

class Websites(Model):
    """Model for user accounts."""

    __tablename__ = 'websites'
    __table_args__ = {'extend_existing': True}

    id = db.Column(db.Integer,
                   primary_key=True)
    website = db.Column(db.String(150),
                     nullable=False,
                     unique=True)
    password = db.Column(db.String(150),
                      unique=True,
                      nullable=True)
    xmlrpc =    db.Column(db.String(150),
                      unique=True,
                      nullable=False)

class Parentsku(Model):
    """Model for the stations table"""
    __tablename__ = 'parentskus'
    __table_args__ = {'extend_existing': True}
    p_id = db.Column(db.Integer, primary_key = True)
    parent_sku = db.Column(db.Unicode)
    featured = db.Column(db.Boolean, default=False)
    encorestock = db.Column(db.Integer, default=0)
    inboundstock = db.Column(db.Integer, default=0)
    day1 = db.Column(db.Integer, default=0)
    day3 = db.Column(db.Integer, default=0)
    day7 = db.Column(db.Integer, default=0)
    day14 = db.Column(db.Integer, default=0)
    day28 = db.Column(db.Integer, default=0)
    #childsku = db.relationship('Quantities.child_sku', backref='owner')


    def __init__(self, parent_sku, featured, encorestock, inboundstock,day1, day3, day7, day14, day28):
        self.parent_sku = parent_sku
        self.featured = featured
        self.encorestock = encorestock
        self.inboundstock = inboundstock
        self.day1 = day1
        self.day3 = day3
        self.day7 = day7
        self.day14 = day14
        self.day28 = day28
    @property
    def serialize(self):
       """Return object data in easily serializable format"""
       return {
            'p_id': self.p_id,
            'parent_sku': self.parent_sku,
            'featured': self.featured,
            'encorestock' : self.encorestock,
            'inboundstock' : self.inboundstock,
            'day1' : self.day1,
            'day3': self.day3,
            'day7': self.day7,
            'day14': self.day14,
            'day28': self.day28
           # This is an example how to deal with Many2Many relations


       }
class Notifs(Model):

    __tablename__='notif_settings'
    __table_args__ = {'extend_existing': True}


    id = db.Column(db.Integer, primary_key = True)
    funnel_name = db.Column(db.Unicode)
    sms = db.Column(db.Boolean)
    email = db.Column(db.Boolean)




    @property
    def serialize(self):
       """Return object data in easily serializable format"""
       return {
           "id" : self.id,
           "funnel_name" : self.funnel_name,
           "sms" : self.sms,
           "email" : self.email
       }
    @property
    def serialize_many2many(self):
       """
       Return object's relations in easily serializable format.
       NB! Calls many2many's serialize property.
       """
       return [ item.serialize for item in self.many2many]


class Funnels(Model):
    """Model for the stations table"""
    __tablename__ = 'funnel_identities'
    __table_args__ = {'extend_existing': True}
    id = db.Column(db.Integer, primary_key = True)
    funnel_name = db.Column(db.Unicode)
    funnel_id = db.Column(db.Unicode)
    view_id = db.Column(db.Unicode)
    stats_link = db.Column(db.Unicode)
    optin = db.Column(db.Unicode)

    @property
    def serialize(self):
       """Return object data in easily serializable format"""
       return {
           'id': self.id,
           'funnel_name': self.funnel_name,
           'funnel_id': self.funnel_sku,
           # This is an example how to deal with Many2Many relations
           'view_id': self.view_id,
           'stats_link' : self.stats_link,
            "optin" : self.optin

       }

       def __init__(self, funnel_name,funnel_id, stats_link, view_id, optin):
           self.funnel_name = funnel_name
           self.funnel_id = funnel_id
           self.view_id = self.view_id
           self.stats_link = self.stats_link
           self.optin = self.optin


