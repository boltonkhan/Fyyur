"""Db models and manipulate data layer."""

import sqlalchemy
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.dialects.postgresql import ARRAY
from flask_migrate import Migrate
from datetime import datetime
from typing import List
from sqlalchemy import func

db = SQLAlchemy()


def db_setup(app):
    """Define app context and db context.

    :param app: flask application context
    :app type: `Flask`
    rtype: `SQLAlchemy`
    """
    app.config.from_object('config')
    db.app = app
    db.init_app(app)
    migrate = Migrate(app, db)
    return db


class Venue(db.Model):
    """Db representation of Venue object."""

    __tablename__ = 'Venue'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(120), nullable=False)
    city = db.Column(db.String(120), nullable=False)
    state = db.Column(db.String(120), nullable=False)
    address = db.Column(db.String(120), nullable=False)
    genres = db.Column(db.ARRAY(db.String()), nullable=False)
    phone = db.Column(db.String(120))

    image_link = db.Column(db.String(500))
    facebook_link = db.Column(db.String(120))
    website_link = db.Column(db.String(120))

    seeking_talent = db.Column(db.Boolean, default=False)
    seeking_description = db.Column(db.String())

    shows = db.relationship('Show', backref='venue',
                            cascade='save-update, merge, delete', lazy=True)

    def __init__(self, name: str, city: str, state: str,
                 address: str, genres: List[str],  phone: str = None,
                 image_link: str = None, website_link: str = None,
                 facebook_link: str = None, seeking_talent: bool = False,
                 seeking_description: str = None
                 ):
        """Create a venue object."""
        default_image = "https://source.unsplash.com/U90sC5WWaZo"

        self.name = name
        assert name is not None and name != "",                           \
            ("Parameter `name` is required!")
        self.city = city
        assert city is not None and city != "",                           \
            ("Parameter `city` is required!")
        self.state = state
        assert state is not None and state != "",                         \
            ("Parameter `state` is required!")
        self.address = address
        assert address is not None and address != "",                     \
            ("Parameter `address` is required!")
        self.phone = phone
        self.genres = genres
        assert genres is not None and genres != "",                       \
            ("Parameter `genres` is required!")
        self.image_link = image_link if image_link else default_image
        self.website_link = None if not website_link else website_link
        self.facebook_link = None if not facebook_link else facebook_link
        self.seeking_talent = False if not seeking_talent else True
        self.seeking_description = None if not seeking_description       \
            else seeking_description

    def __repr__(self):
        """Return representation of the object."""
        return f"{vars(self)}"

    def insert(self):
        """Insert new element into db."""
        db.session.add(self)
        db.session.flush()
        db.session.commit()
        return self

    def update(self):
        """Update existing element in db."""
        db.session.commit()

    def delete(self):
        """Delete element from db."""
        db.session.delete(self)
        db.session.commit()

    @classmethod
    def get_by_id(cls, id: int):
        """Get venue by id.

        :param id: id from the db
        :id type: int
        :return: venue object
        :rtype: `Venue`
        """
        return Venue.query.get(id)

    @classmethod
    def get_all_areas(cls):
        """Get areas (city and state) venues are located in.

        :return: a collection af location
        :rtype: `Tuple(city, state)`
        """
        return db.session                                       \
            .query(Venue.city, Venue.state)                     \
            .group_by(Venue.city, Venue.state).all()

    @classmethod
    def get_venues_by_area(cls, city, state):
        """Return all venues from provided location.

        :param city: city the venues is located in
        :city type: str
        :param state: state the venues is located in
        :state type: str
        :return: a collection of venues from the location
        "rtype: `Venue`
        """
        return Venue.query.filter(
            Venue.city == city and Venue.state == state).all()

    @classmethod
    def search_by_name(cls, name):
        """Return all venues contain searching string in a name.

        :param name: string to look for
        :name type: str
        return: a collection of venues
        :rtype: `List[Venue]`
        """
        return Venue.query \
                    .filter(func.lower(Venue.name)
                                .contains(f"%{name.lower()}%")).all()


class Artist(db.Model):
    """Db representation of an Artist object."""

    __tablename__ = 'Artist'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(120), nullable=False)
    city = db.Column(db.String(120), nullable=False)
    state = db.Column(db.String(120), nullable=False)
    phone = db.Column(db.String(120))
    genres = db.Column(db.ARRAY(db.String()), nullable=False)

    image_link = db.Column(db.String(500))
    facebook_link = db.Column(db.String(120))
    website_link = db.Column(db.String(120))

    seeking_venue = db.Column(db.Boolean, default=False)
    seeking_description = db.Column(db.String())

    shows = db.relationship('Show', backref='artist',
                            cascade='save-update, merge, delete', lazy=True)

    def __init__(self, name: str, city: str,
                 state: str, genres: List[str],
                 phone: str = None, image_link: str = None,
                 facebook_link: str = None, website_link: str = None,
                 seeking_venue: bool = None, seeking_description: str = None
                 ):
        """Create an artist object."""
        default_image = "https://source.unsplash.com/U90sC5WWaZo"

        self.name = name
        assert name is not None and name != "",                 \
            ("`name` is required.")
        self.city = city
        assert city is not None and city != "",                 \
            ("`city` is required.")
        self.state = state
        assert state is not None and state != "",               \
            ("`state` is required.")
        self.genres = genres
        assert genres is not None and genres != [],             \
            ("`genres` is required.")
        self.phone = None if not phone else phone
        self.image_link = default_image                         \
            if not image_link else image_link
        self.facebook_link = None                               \
            if not facebook_link else facebook_link
        self.website_link = None                                \
            if not website_link else website_link
        self.seeking_description = None                         \
            if not seeking_description else seeking_description
        self.seeking_venue = False                              \
            if not seeking_venue else True

    def __repr__(self):
        """Return representation of the object."""
        return f"{vars(self)}"

    def insert(self):
        """Insert new element into db."""
        db.session.add(self)
        db.session.flush()
        db.session.commit()
        return self

    def update(self):
        """Update existing element in db."""
        db.session.commit()
        return self

    def delete(self):
        """Delete element from db."""
        db.session.delete(self)
        db.session.commit()

    @classmethod
    def get_by_id(cls, id: int):
        """Return artist with a provided id.

        :param id: db id of an artist
        :id type: int
        """
        return Artist.query.get(id)

    @classmethod
    def get_all(cls):
        """Get all artists stored in the db."""
        return Artist.query.all()

    @classmethod
    def search_by_name(cls, name):
        """Return all artists contain searching string in a name.

        :param name: string to look for
        :name type: str
        :return: a collection of artists
        :rtype: `List[Artist]`
        """
        return Artist.query.filter(func.lower(Artist.name)
                                   .contains(f"%{name.lower()}%")).all()


class Show(db.Model):
    """Db representation of a Show object."""

    __tablename__ = "Show"

    id = db.Column(db.Integer, primary_key=True)
    artist_id = db.Column(
                    db.Integer,
                    db.ForeignKey('Artist.id'),
                    nullable=False
                )
    venue_id = db.Column(
                    db.Integer,
                    db.ForeignKey('Venue.id'),
                    nullable=False
                )
    start_time = db.Column(
                    db.DateTime,
                    default=datetime.now()
                )

    def __init__(self, artist_id: int, venue_id: int, start_time: datetime):
        """Init an object."""
        self.artist_id = artist_id
        self.venue_id = venue_id
        self.start_time = start_time

    def __repr__(self):
        """Return representation of the object."""
        return f"{vars(self)}"

    def insert(self):
        """Insert new element into db."""
        db.session.add(self)
        db.session.flush()
        db.session.commit()
        return self

    def update(self):
        """Update existing element in db."""
        db.session.commit()

    def delete(self):
        """Delete element from db."""
        db.session.delete(self)
        db.session.commit()

    @classmethod
    def get_shows(cls):
        """Get all shows."""
        return Show.query.join(Venue, Show.venue_id == Venue.id)          \
                         .join(Artist, Show.artist_id == Artist.id)       \
                         .add_columns(Artist.name, Artist.image_link,
                                      Venue.name)                         \
                         .all()

    @classmethod
    def get_past_shows_by_artist(cls, id: int):
        """Return all past shows of an artist.

        :param id: an artist id
        :id type: int
        :return: a collection of ditaled info about past shows
        :rtype: `Tuple`
        """
        current = datetime.now()
        return Show.query.join(Venue, Show.venue_id == Venue.id)      \
                         .join(Artist, Show.artist_id == Artist.id)   \
                         .add_columns(Venue.name, Venue.image_link)   \
                         .filter(Show.start_time < current)           \
                         .filter(Artist.id == id).all()

    @classmethod
    def get_upcoming_shows_by_artist(cls, id: int):
        """Return all upcoming shows of an artist.

        :param id: an artist id
        :id type: int
        :return: a collection of ditaled info about past shows
        :rtype: `Tuple`
        """
        current = datetime.now()
        return Show.query.join(Venue, Show.venue_id == Venue.id)      \
                         .join(Artist, Show.artist_id == Artist.id)   \
                         .add_columns(Venue.name, Venue.image_link)   \
                         .filter(Show.start_time > current)           \
                         .filter(Artist.id == id).all()

    @classmethod
    def get_past_shows_by_venue(cls, id: int):
        """Return all past shows in the venue.

        :param id: an venue id
        :id type: int
        :return: a collection of ditaled info about past shows
        """
        current = datetime.now()
        return Show.query.join(Venue, Show.venue_id == Venue.id)        \
                         .join(Artist, Show.artist_id == Artist.id)     \
                         .add_columns(Artist.name, Artist.image_link)   \
                         .filter(Show.start_time < current)             \
                         .filter(Venue.id == id).all()

    @classmethod
    def get_upcoming_shows_by_venue(cls, id: int):
        """Return all upcoming shows in the venue.

        :param id: an venue id
        :id type: int
        :return: a collection of ditaled info about past shows
        """
        current = datetime.now()
        return Show.query.join(Venue, Show.venue_id == Venue.id)        \
                         .join(Artist, Show.artist_id == Artist.id)     \
                         .add_columns(Artist.name, Artist.image_link)   \
                         .filter(Show.start_time > current)             \
                         .filter(Venue.id == id).all()
