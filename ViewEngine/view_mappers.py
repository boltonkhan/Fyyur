"""View engine - prepare view models to display."""

from Database.models import Artist, Venue, Show
from .view_models import *
import json


def create_venues_view():
    """Prepare view model for @app.route('/venues').

    rtype: `List[VenueView]`
    """
    venues_view = []
    areas = Venue.get_all_areas()

    for area in areas:
        ven_view = VenueView(city=area[0], state=area[1])
        vens = Venue.get_venues_by_area(ven_view.city, ven_view.state)

        for v in vens:
            up_shows_count = len(Show.get_upcoming_shows_by_venue(v.id))
            ven_view.venues.append(
                VenueViewSum(v.name, v.id, up_shows_count))

        venues_view.append(ven_view)

    return venues_view


def create_venue_search_view(name):
    """Prepare view model for @app.route('/venues/search').

    :param name: name of a Venue to find
    :name type: str
    :rtype: `List[VenueSearchView]`
    """
    search_view = None
    venues = Venue.search_by_name(name)

    if not venues:
        search_view = VenueSearchView(count=0)

    if venues:
        search_view = VenueSearchView(
            count=len(venues)
        )

        for ven in venues:
            search_view.data.append(
                VenueViewSum(
                    name=ven.name,
                    id=ven.id,
                    upcoming_shows_count=len(
                        Show.get_upcoming_shows_by_venue(ven.id))
                )
            )

    return search_view


def create_venue_detailed_view(ven_id: int):
    """Prepare data for @app.route('/venues/<int:venue_id>').

    :param ven_id: id of venue to take shows for
    :ven_id type: int
    """
    venue = Venue.get_by_id(ven_id)
    if not venue:
        return None

    view_venue = VenueDetailsView(
        id=venue.id,
        name=venue.name,
        genres=venue.genres,
        address=venue.address,
        city=venue.city,
        state=venue.state,
        phone=venue.phone,
        website=venue.website_link,
        facebook_link=venue.facebook_link,
        seeking_talent=venue.seeking_talent,
        image_link=venue.image_link
    )

    def dbshow_to_view(show):
        show = dict(show)
        return ShowVenueView(
            artist_id=show['Show'].artist_id,
            artist_name=show['name'],
            artist_image_link=show['image_link'],
            start_time=show['Show'].start_time
                                   .strftime('%Y-%m-%d %H:%S:%M')
            )

    past_shows = Show.get_past_shows_by_venue(ven_id)
    view_venue.past_shows_count = len(past_shows)
    view_venue.past_shows = list(map(dbshow_to_view, past_shows))

    upcoming_shows = Show.get_upcoming_shows_by_venue(ven_id)
    view_venue.upcoming_shows_count = len(upcoming_shows)
    view_venue.upcoming_shows = list(map(dbshow_to_view, upcoming_shows))

    return view_venue


def create_artists_view():
    """Create view model for @app.route('/artists')."""
    artist_list = []
    artists = Artist.get_all()

    for artist in artists:
        artist_list.append(
            ArtistViewSum(artist.id, artist.name)
        )

    return artist_list


def create_artist_search_view(name: str):
    """Create view model for the search artist endpoint.

    @app.route('/artists/search')
    """
    search_view = None
    artists = Artist.search_by_name(name)

    if not artists:
        search_view = ArtistSearchView(count=0)

    if artists:
        search_view = ArtistSearchView(count=len(artists))

        for artist in artists:
            num_upcom_shows =                                           \
                len(Show.get_upcoming_shows_by_artist(artist.id))
            search_view.data.append(
                ArtistViewSum(artist.id, artist.name, num_upcom_shows))

    return search_view


def create_artist_detail_view(artist_id):
    """Create view for @app.route('/artists/<int:artist_id>')."""
    db_artist = Artist.get_by_id(artist_id)

    artist = ArtistDetailsView(
        id=db_artist.id,
        name=db_artist.name,
        genres=db_artist.genres,
        city=db_artist.city,
        state=db_artist.state,
        phone=db_artist.phone,
        website=db_artist.website_link,
        facebook_link=db_artist.facebook_link,
        image_link=db_artist.image_link,
        seeking_venue=db_artist.seeking_venue,
        seeking_description=db_artist.seeking_description
    )

    def dbshow_to_view(dbshow):
        dbshow = dict(dbshow)
        return ShowArtistView(
            venue_id=dbshow['Show'].venue_id,
            venue_name=dbshow['name'],
            venue_image_link=dbshow['image_link'],
            start_time=dbshow['Show'].start_time
                                     .strftime('%Y-%m-%d %H:%S:%M')
        )

    past_shows = Show.get_past_shows_by_artist(artist_id)
    artist.past_shows = list(map(dbshow_to_view, past_shows))
    artist.past_shows_count = len(past_shows)

    upcom_shows = Show.get_upcoming_shows_by_artist(artist_id)
    artist.upcoming_shows = list(map(dbshow_to_view, past_shows))
    artist.upcoming_shows_count = len(upcom_shows)

    return artist


def create_shows_view():
    """Prepare show view model.

    @app.route('/shows')
    """
    shows = Show.get_shows()

    def dbshow_to_viewshow(show):
        show = list(show)
        return ShowView(
                    venue_id=show[0].venue_id,
                    venue_name=show[3],
                    artist_id=show[0].artist_id,
                    artist_name=show[1],
                    artist_image_link=show[2],
                    start_time=show[0].start_time
                                      .strftime('%Y-%m-%d %H:%S:%M')
                        )

    return list(map(dbshow_to_viewshow, shows))


def map_form_to_artist(form, artist=None, artist_id=None):
    """Map form data to an Artist object."""
    if artist is None:
        artist = Artist(
                    name=form.get("name", None),
                    city=form.get("city", None),
                    state=form.get("state", None),
                    phone=form.get("phone", None),
                    genres=form.getlist("genres", None),
                    image_link=form.get("image_link", None),
                    facebook_link=form.get("facebook_link", None),
                    website_link=form.get("website_link", None),
                    seeking_description=form.get(
                        "seeking_description", None),
                    seeking_venue=False if form.get(
                        "seeking_venue", None) is None else True
                )

        if artist_id:
            artist.id = artist_id
    else:
        artist.id = artist_id
        artist.name = form.get("name", None)
        artist.city = form.get("city", None)
        artist.state = form.get("state", None)
        artist.phone = form.get("phone", None)
        artist.genres = form.getlist("genres", None)
        artist.image_link = form.get("image_link", None)
        artist.facebook_link = form.get("facebook_link", None)
        artist.website_link = form.get("website_link", None)
        artist.seeking_description = form.get(
            "seeking_description", None)
        artist.seekin_venue = False \
            if form.get("seeking_venue", None) is None else True

    return artist


def map_form_to_venue(form, venue=None, venue_id=None):
    """Map form data to a Venue object."""
    if venue is None:
        venue = Venue(
                    name=form.get("name", None),
                    city=form.get("city", None),
                    state=form.get("state", None),
                    address=form.get("address", None),
                    phone=form.get("phone", None),
                    genres=form.getlist("genres", None),
                    image_link=form.get("image_link", None),
                    website_link=form.get("website_link", None),
                    facebook_link=form.get("facebook_link", None),
                    seeking_talent=False if form.get(
                        "seeking_talent", None) is None else True,
                    seeking_description=form.get(
                        "seeking_description", None)
                )

        if venue_id:
            venue.id = venue_id
    else:
        venue.id = venue.id
        venue.name = form.get("name", None)
        venue.city = form.get("city", None)
        venue.state = form.get("state", None)
        venue.address = form.get("address", None)
        venue.phone = form.get("phone", None)
        venue.genres = form.getlist("genres", None)
        venue.image_link = form.get("image_link", None)
        venue.website_link = form.get("website_link", None)
        venue.facebook_link = form.get("facebook_link", None)
        venue.seeking_talent = False \
            if form.get("seeking_talent", None) is None else True
        venue.seeking_description = form.get("seeking_description", None)

    return venue
