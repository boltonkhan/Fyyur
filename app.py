"""Main module of the application.

Reponsible for all the bussiness logic,
consists of series of controllers to control user flow and views.
"""

import json
import dateutil.parser
import babel
from datetime import datetime
from flask import Flask, render_template, request,\
                  Response, flash, redirect, url_for, abort
from flask_moment import Moment
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.exc import SQLAlchemyError
from flask_migrate import Migrate
import logging
from logging import Formatter, FileHandler
from flask_wtf import FlaskForm
from flask_wtf.csrf import CSRFProtect
from ViewEngine.validators import *
from ViewEngine.forms import *
from Database.models import db_setup, Venue, Show, Artist
from ViewEngine.view_mappers import *
from werkzeug.exceptions import HTTPException
from ViewEngine.validators import *


"""Init app context."""

app = Flask(__name__)
moment = Moment(app)
db = db_setup(app)
csrf = CSRFProtect(app)

"""Utilities, helpers."""


def format_datetime(value, format='medium'):
    """Format date."""
    date = dateutil.parser.parse(value)
    if format == 'full':
        format = "EEEE MMMM, d, y 'at' h:mma"
    elif format == 'medium':
        format = "EE MM, dd, y h:mma"
    return babel.dates.format_datetime(date, format, locale='en')


app.jinja_env.filters['datetime'] = format_datetime


class Err:
    """Object to handel error data.

    :param msg: error message
    :msg type: str
    :param code: http code if exists
    :code type: int, optional, default None
    """

    def __init__(self, msg, code=None):
        """Create an object.

        :param msg: error message
        :msg type: str
        :param code: error code, mainy for http status code
        :code type: int, optional, default None
        """
        self.code = code
        self.msg = msg

    def __repr__(self):
        """Return a string representation."""
        return f"Error: {self.msg}, status_code: {self.code}."

    def __str__(self):
        """Return a string representation."""
        return self.__repr__()


"""Controllers."""


@app.route('/')
def index():
    """Display main page."""
    return render_template('pages/home.html')


@app.route('/venues')
def venues():
    """Display venues grouped by the location/area."""
    err = None

    try:
        data = create_venues_view()

        if data is None:
            err = Err(code=404, msg="Venue data didn't find.")

    except SQLAlchemyError as e:
        err = Err(code=500, msg=e)

    except BaseException as e:
        err = Err(code=500, msg=e)

    finally:
        if err:
            app.logger.error(f"{err} \n {request.__dict__}")
            abort(err.code)

    return render_template('pages/venues.html', areas=data)


@app.route('/venues/search', methods=['POST'])
def search_venues():
    """Search venues by name."""
    search_name = request.form.get('search_term', '')
    err = None

    try:
        response = create_venue_search_view(search_name)
        if response is None:
            err = Err(code=404, msg="Venue data didn't find.")

    except SQLAlchemyError:
        err = Err(code=500, msg=e)

    except BaseException as e:
        err = Err(code=500, msg=e)

    finally:
        if err:
            app.logger.error(f"{err} \n {request.__dict__}")
            abort(err.code)

    return render_template('pages/search_venues.html',
                           results=response, search_term=search_name)


@app.route('/venues/<int:venue_id>', methods=['GET'])
def show_venue(venue_id):
    """Display venue detailed page.

    :param venue_id: id of the location
    :id type: int
    """
    err = None

    try:
        data = create_venue_detailed_view(venue_id)

        if data is None:
            err = Err(code=404, msg=f"Venue data didn't find.")

    except SQLAlchemyError as e:
        err = 500

    except HTTPException as e:
        err = Err(code=e.code, msg=e)

    except BaseException as e:
        err = Err(code=500, msg=e)

    finally:
        if err:
            app.logger.error(f"{err} \n {request.__dict__}")
            abort(err.code)

    return render_template('pages/show_venue.html', venue=data)


@app.route('/venues/create', methods=['GET'])
def create_venue_form():
    """Get venue create form."""
    form = VenueForm()
    return render_template('forms/new_venue.html', form=form)


@app.route('/venues/create', methods=['POST'])
def create_venue_submission():
    """Create new venue object."""
    form = VenueForm(request.form)

    if request.method == 'POST' and form.validate():
        try:
            venue = Venue(
                name=request.form.get('name', None),
                city=request.form.get('city', None),
                state=request.form.get('state', None),
                address=request.form.get('address', None),
                genres=request.form.getlist('genres', None),
                phone=request.form.get('phone', None),
                website_link=request.form.get('website_link', None),
                facebook_link=request.form.get('facebook_link', None),
                image_link=request.form.get('image_link', None),
                seeking_talent=request.form.get('seeking_talent', None),
                seeking_description=request.form
                                    .get('seeking_description', None)
                )

            added_venue = Venue.insert(venue)

            err = None

        except AssertionError as e:
            err = Err(code=404, msg=e)

        except TypeError as e:
            err = Err(code=404, msg=e)

        except HTTPException as e:
            err = Err(code=e.code, msg=e)

        except SQLAlchemyError as e:
            err = Err(code=500, msg=e)
            db.session.rollback()

        except BaseException as e:
            err = Err(code=500, msg=e)
        else:
            flash(f"Venue {added_venue.name} was successfully listed!")

        finally:
            if err:
                app.logger.error(f"{err} \n {request.__dict__}")
                flash(f"An error occurred. "
                      f"Venue {request.form['name']} could not be listed.")

            db.session.close()
            return render_template('pages/home.html')

    return render_template('forms/new_venue.html', form=form)


@app.route('/venues/<venue_id>', methods=['DELETE'])
def delete_venue(venue_id):
    """Delete venue from db.

    :param venue_id: id in the db of venue to delete
    :venue_id: int
    """
    err = None

    try:
        to_delete = Venue.get_by_id(venue_id)
        if to_delete is None:
            err = Err(
                code=404, msg=f"Venue data didn't find.")

        Venue.delete(to_delete)

    except SQLAlchemyError as e:
        err = Err(code=500, msg=e)
        db.session.rollback()

    except HTTPException as e:
        err = Err(code=e.code, msg=e)

    except BaseException as e:
        err = Err(code=500, msg=e)

    else:
        flash(f"Venue was successfully deleted!")

    finally:
        if err:
            app.logger.error(f"{err} \n {request.__dict__}")
            flash(f"An error occurred. Venue could not be deleted.")
        db.session.close()

    return url_for('index')


@app.route('/artists')
def artists():
    """Return a list of artist."""
    err = None

    try:
        data = create_artists_view()
        if data is None:
            err = Err(code=404, msg=f"Artists can not be found.")

    except SQLAlchemyError as e:
        err = Err(code=500, msg=e)

    except HTTPException as e:
        err = Err(code=e.code, msg=e)

    except BaseException as e:
        err = Err(code=500, msg=e)

    finally:
        if err:
            app.logger.error(f"{err} \n {request.__dict__}")
            abort(err.code)

    return render_template('pages/artists.html', artists=data)


@app.route('/artists/search', methods=['POST'])
def search_artists():
    """Search an artist by name."""
    search_phrase = request.form.get('search_term', '')
    err = None

    try:
        response = create_artist_search_view(search_phrase)

        if response is None:
            err = Err(code=404, msg=f"Artists can not be found.")

    except SQLAlchemyError as e:
        err = Err(code=500, msg=e)

    except HTTPException as e:
        err = Err(code=e.code, msg=e)

    except BaseException as e:
        err = Err(code=500, msg=e)

    finally:
        if err:
            app.logger.error(f"{err} \n {request.__dict__}")
            abort(err.code)

    return render_template('pages/search_artists.html',
                           results=response, search_term=search_phrase)


@app.route('/artists/<int:artist_id>')
def show_artist(artist_id):
    """Display the artist page."""
    err = None

    try:
        data = create_artist_detail_view(artist_id)

        if data is None:
            err = Err(code=404, msg=f"Artist can be found.")

    except SQLAlchemyError as e:
        err = Err(code=500, msg=e)

    except HTTPException as e:
        err = Err(code=e.code, msg=e)

    except BaseException as e:
        err = Err(code=500, msg=e)

    finally:
        if err:
            app.logger.error(f"{err} \n {request.__dict__}")
            abort(err.code)

    return render_template('pages/show_artist.html', artist=data)


@app.route('/artists/<int:artist_id>/edit', methods=['GET'])
def edit_artist(artist_id):
    """Display edit form to edit artist data."""
    err = None

    try:
        artist = Artist.get_by_id(artist_id)

        if artist is None:
            err = Err(code=404, msg=f"Artist can not be found.")

        form = ArtistForm(formdata=request.form, obj=artist)
        for genre in artist.genres:
            for i,k in enumerate(form.genres.choices):
                if genre in k:
                    form.genres.data.append(genre)
        
        form.seeking_venue.data = artist.seeking_venue
                    

    except SQLAlchemyError as e:
        err = Err(code=500, msg=e)

    except HTTPException as e:
        err = Err(code=e.code, msg=e)

    except BaseException as e:
        err = Err(code=500, msg=e)

    finally:
        if err:
            app.logger.error(f"{err} \n {request.__dict__}")
            abort(err.code)

    return render_template(
            'forms/edit_artist.html', form=form, artist=artist)


@app.route('/artists/<int:artist_id>/edit', methods=['POST'])
def edit_artist_submission(artist_id):
    """Edit artis data."""
    err = None

    form = ArtistForm(request.form)
    artist = map_form_to_artist(request.form, artist_id=artist_id)

    if request.method == 'POST' and form.validate():

        try:
            artist = Artist.get_by_id(artist_id)
            if artist is None:
                err = Err(code=404, msg=f"Artist can not be found.")

            artist = map_form_to_artist(
                request.form, artist=artist, artist_id=artist_id)
            artist = Artist.update(artist)

        except SQLAlchemyError as e:
            err = Err(code=500, msg=e)

        except HTTPException as e:
            err = Err(code=e.code, msg=e)

        except BaseException as e:
            err = Err(code=500, msg=e)

        else:
            flash(f"Artist {artist.name} was successfully edited!")

        finally:
            if err:
                app.logger.error(f"{err} \n {request.__dict__}")
                flash(f"An error occurred.")

            db.session.close()
            return redirect(url_for('show_artist', artist_id=artist_id))

    return render_template(
            'forms/edit_artist.html', form=form, artist=artist)


@app.route('/venues/<int:venue_id>/edit', methods=['GET'])
def edit_venue(venue_id):
    """Return venue edit form.."""
    err = None

    try:
        venue = Venue.get_by_id(venue_id)
        if venue is None:
            err = Err(code=404, msg=f"Venue can not be found.")

        form = VenueForm(formdata=request.form, obj=venue)
        for genre in venue.genres:
            for i,k in enumerate(form.genres.choices):
                if genre in k:
                    form.genres.data.append(genre)

        form.seeking_talent.data = venue.seeking_talent

    except SQLAlchemyError as e:
        err = Err(code=500, msg=e)

    except HTTPException as e:
        err = Err(code=e.code, msg=e)

    except BaseException as e:
        err = Err(code=500, msg=e)

    finally:
        if err:
            app.logger.error(f"{err} \n {request.__dict__}")
            abort(err.code)

    return render_template(
        'forms/edit_venue.html', form=form, venue=venue)


@app.route('/venues/<int:venue_id>/edit', methods=['POST'])
def edit_venue_submission(venue_id):
    """Edit venue data submition."""
    err = None
    print(request.form)
    form = VenueForm(request.form)
    venue = map_form_to_venue(request.form, venue_id=venue_id)

    if request.method == 'POST' and form.validate():
        try:
            venue = Venue.get_by_id(venue_id)
            if venue is None:
                err = Err(code=404, msg=f"Venue can not be found.")

            venue = map_form_to_venue(request.form, venue, venue_id)
            Venue.update(venue)

        except SQLAlchemyError as e:
            err = Err(code=500, msg=e)

        except HTTPException as e:
            err = Err(code=e.code, msg=e)

        except BaseException as e:
            err = Err(code=500, msg=e)

        else:
            flash(f"Venue {venue.name} was successfully edited!")

        finally:
            if err:
                flash(f"An error occurred.")
                app.logger.error(f"{err} \n {request.__dict__}")
            db.session.close()

            return redirect(url_for('show_venue', venue_id=venue_id))

    return render_template(
        'forms/edit_venue.html', form=form, venue=venue)


@app.route('/artists/create', methods=['GET'])
def create_artist_form():
    """Create an artist."""
    form = ArtistForm()
    return render_template('forms/new_artist.html', form=form)


@app.route('/artists/create', methods=['POST'])
def create_artist_submission():
    """Create an artist in a database."""
    err = None
    form = ArtistForm()

    if request.method == 'POST' and form.validate():

        try:
            artist = map_form_to_artist(request.form)
            artist = Artist.insert(artist)

        except AssertionError as e:
            err = Err(code=404, msg=e)

        except TypeError as e:
            err = Err(code=404, msg=e)

        except HTTPException as e:
            err = Err(code=e.code, msg=e)

        except SQLAlchemyError as e:
            err = Err(code=500, msg=e)
            db.session.rollback()

        except BaseException as e:
            err = Err(code=500, msg=e)

        else:
            flash(f"Artist {artist.name} was successfully listed!")

        finally:
            if err:
                app.logger.error(f"{err} \n {request.__dict__}")
                flash(f"An error occurred. "
                      f"Artist {request.form['name']} could not be listed.")

            db.session.close()
            return render_template('pages/home.html')

    return render_template('forms/new_artist.html', form=form)


@app.route('/shows')
def shows():
    """Display list of shows."""
    err = None

    try:
        data = create_shows_view()
        if data is None:
            err = Err(
                code=404, msg="Venue can not be found.")

    except HTTPException as e:
        err = Err(code=e.code, msg=e)

    except SQLAlchemyError as e:
        err = Err(code=500, msg=e)
        db.session.rollback()

    except BaseException as e:
        err = Err(code=500, msg=e)

    finally:
        if err:
            app.logger.error(f"{err} \n {request.__dict__}")
            abort(err.code)

        db.session.close()

    return render_template('pages/shows.html', shows=data)


@app.route('/shows/create')
def create_shows():
    """Return create a show form."""
    form = ShowForm()
    return render_template('forms/new_show.html', form=form)


@app.route('/shows/create', methods=['POST'])
def create_show_submission():
    """Create a new show."""
    err = None
    form = ShowForm()

    if request.method == 'POST':
        try:

            artist_id = request.form['artist_id']
            venue_id = request.form['venue_id']
            artist = Artist.get_by_id(artist_id)
            venue = Venue.get_by_id(venue_id)

            show = Show(
                artist_id=artist_id,
                venue_id=venue_id,
                start_time=request.form['start_time']
                )

            show = Show.insert(show)

        except TypeError as e:
            err = Err(code=404, msg=e)

        except HTTPException as e:
            err = Err(code=e.code, msg=e)

        except SQLAlchemyError as e:
            err = Err(code=500, msg=e)

        except BaseException as e:
            err = Err(code=500, msg=e)

        else:
            flash('Show was successfully listed!')

        finally:
            if err:
                app.logger.error(f"{err} \n {request.__dict__}")
                flash('An error occurred. Show could not be listed.')

            db.session.close()

    return render_template('pages/home.html')


@app.errorhandler(404)
def not_found_error(error):
    """404 status code page."""
    return render_template('errors/404.html'), 404


@app.errorhandler(500)
def server_error(error):
    """500 status code page."""
    return render_template('errors/500.html'), 500


if not app.debug:
    file_handler = FileHandler('error.log')
    file_handler.setFormatter(
        Formatter(
            '%(asctime)s %(levelname)s: '
            '%(message)s [in %(pathname)s:%(lineno)d]'
            )
    )
    app.logger.setLevel(logging.INFO)
    file_handler.setLevel(logging.INFO)
    app.logger.addHandler(file_handler)
    app.logger.info('errors')


if __name__ == '__main__':
    app.run(debug=True)

'''
if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port)
'''
