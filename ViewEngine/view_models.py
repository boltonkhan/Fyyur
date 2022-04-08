"""Data models for the views."""

from Database.models import Artist, Venue, Show
import json
import datetime
from abc import ABC

from typing import List


class BaseView(ABC):
    """Abstract class of view models."""

    def __str__(self):
        """Return string representation of the object attributes."""
        return str(vars(self))

    def __repr__(self):
        """Return string representation of the object attributes."""
        return str(f"{self.__str__()}")


class VenueViewSum(BaseView):
    """The short version of venue object.

    :param name: name of the venue
    :name type: str
    :param id: venue id from db
    :id type: int
    :param upcoming_shows_count: number of upcoming event
    :upcoming_shows_count type: int
    """

    def __init__(self, name: str, id: int, upcoming_shows_count: int):
        """Create an instance of a view model."""
        super().__init__()
        self.name = name
        self.id = id
        self.upcoming_shows_count = int(upcoming_shows_count)


class VenueView(BaseView):
    """Venue view uses in /venues endpoint.

    :param city: name of the city venue is located in
    :city type: str
    :param state: name of the state cenue is located in
    :state type: str
    """

    def __init__(self, city: str, state: str):
        """Create an instance of a view model."""
        super().__init__()
        self.city = str(city)
        self.state = str(state)
        self.venues = []


class VenueSearchView(BaseView):
    """View model for /venues/search endpoint.

    :param count: number of venues found
    :count type: int
    """

    def __init__(self, count: int):
        """Create an instance of a view model."""
        super().__init__()
        self.count = count
        self.data = []


class ShowVenueView(BaseView):
    """View class represents short version of show object."""

    def __init__(self, artist_id: int, artist_name: str,
                 artist_image_link: str, start_time: datetime):
        """Create view model instance."""
        super().__init__()
        self.artist_id = artist_id
        self.artist_name = artist_name
        self.artist_image_link = artist_image_link
        self.start_time = start_time


class VenueDetailsView(BaseView):
    """View representation of venue details.

    @app.route('/venues/<int:venue_id>', methods=['GET'])
    """

    def __init__(self, id: int, name: str, genres: List[str], address: str,
                 city: str, state: str, phone: str, website: str,
                 facebook_link: str, seeking_talent: bool, image_link: str):
        """Create view model instance."""
        super().__init__()
        self.id = id
        self.name = name
        self.genres = genres
        self.address = address
        self.city = city
        self.state = state
        self.phone = phone
        self.website = website
        self.facebook_link = facebook_link
        self.seeking_talent = seeking_talent
        self.image_link = image_link
        self.past_shows = []
        self.upcoming_shows = []
        self.past_shows_count = 0
        self.upcoming_shows_count = 0


class ArtistViewSum(BaseView):
    """View model for element of the list: @app.route('/artists').

    :param artist_id: db id of the artist
    :artist_id type: int
    :param name: name of the artist
    :name type: str
    """

    def __init__(self, artist_id: int,
                 name: str, num_upcoming_shows: int = None
                 ):
        """Create view model instance."""
        super().__init__()
        self.id = artist_id
        self.name = name
        self.num_upcoming_shows = None    \
            if num_upcoming_shows is None \
            else num_upcoming_shows


class ArtistSearchView(BaseView):
    """View model for @app.route('/artists/search.

    :param count: the count of founded elements
    :count type: int
    """

    def __init__(self, count: int):
        """Create an instance of a view model."""
        super().__init__()
        self.count = count
        self.data = []


class ArtistDetailsView(BaseView):
    """View representation of artist details.

    @app.route('/artist/<int:artist_id>', methods=['GET'])
    """

    def __init__(self, id: int, name: str,
                 genres: List[str], city: str,
                 state: str, phone: str, website: str,
                 facebook_link: str, image_link: str,
                 seeking_venue: bool, seeking_description: str
                 ):
        """Create an instance of a view model."""
        super().__init__()
        self.id = id
        self.name = name
        self.city = city
        self.state = state
        self.phone = phone
        self.genres = genres
        self.website = website
        self.facebook_link = facebook_link
        self.image_link = image_link
        self.seeking_venue = seeking_venue
        self.seeking_description = seeking_description
        self.past_shows = []
        self.upcoming_shows = []
        self.past_shows_count = 0
        self.upcoming_shows_count = 0


class ShowArtistView(BaseView):
    """View representation of show for a given artists.

    @app.route('/artist/<int:artist_id>', methods=['GET'])
    """

    def __init__(self, venue_id: int, venue_name: str,
                 venue_image_link: str, start_time: datetime):
        """Create an instance of a view model."""
        super().__init__()
        self.venue_id = venue_id
        self.venue_name = venue_name
        self.venue_image_link = venue_image_link
        self.start_time = start_time


class ShowView(BaseView):
    """View representation of shows list element.

    @app.route('/shows')
    """

    def __init__(self, venue_id: int, venue_name: str,
                 artist_id: int, artist_name: str,
                 artist_image_link: str, start_time: datetime
                 ):
        """Create an instance of a view model."""
        super().__init__()
        self.venue_id = venue_id
        self.venue_name = venue_name
        self.artist_id = artist_id
        self.artist_name = artist_name
        self.artist_image_link = artist_image_link
        self.start_time = start_time
