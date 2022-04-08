"""Run the file and generate test data for the project.

This is separated script. To generate sample data,
the script should be run after database migration.
"""

from Database.models import Artist, Show, Venue

"""Venue test data."""

venue1 = Venue(
    name="The Musical Hop",
    genres=["Jazz", "Reggae", "Swing", "Classical", "Folk"],
    address="1015 Folsom Street",
    city="San Francisco",
    state="CA",
    phone="123-123-1234",
    image_link="https://images.unsplash.com/photo-1543900694-133f37abaaa5?"
               "ixlib=rb-1.2.1&"
               "ixid=eyJhcHBfaWQiOjEyMDd9&auto=format&fit=crop&w=400&q=60",
    website_link="https://www.themusicalhop.com",
    facebook_link="https://www.facebook.com/TheMusicalHop",
    seeking_talent=True,
    seeking_description="We are on the lookout for a local "
                        "artist to play every two weeks. Please call us."
)

venue2 = Venue(
    name="The Dueling Pianos Bar",
    genres=["Classical", "R&B", "Hip-Hop"],
    address="335 Delancey Street",
    city="New York",
    state="NY",
    phone="914-003-1132",
    website_link="https://www.theduelingpianos.com",
    facebook_link="https://www.facebook.com/theduelingpianos",
    seeking_talent=False,
    image_link="https://images.unsplash.com/"
               "photo-1497032205916-ac775f0649ae?ixlib=rb-1.2.1&"
               "ixid=eyJhcHBfaWQiOjEyMDd9&auto=format&fit=crop&w=750&q=80",
    seeking_description=''
)

venue3 = Venue(
    name="Park Square Live Music & Coffee",
    genres=["Rock n Roll", "Jazz", "Classical", "Folk"],
    address="34 Whiskey Moore Ave",
    city="San Francisco",
    state="CA",
    phone="415-000-1234",
    website_link="https://www.parksquarelivemusicandcoffee.com",
    facebook_link="https://www.facebook.com/ParkSquareLiveMusicAndCoffee",
    seeking_talent=False,
    image_link="https://images.unsplash.com/"
               "photo-1485686531765-ba63b07845a7?"
               "ixlib=rb-1.2.1&ixid=eyJhcHBfaWQiOjEyMDd9&"
               "auto=format&fit=crop&w=747&q=80",
    seeking_description=""
)

"""Artist test data."""

artist1 = Artist(
    name="Guns N Petals",
    genres=["Rock n Roll"],
    city="San Francisco",
    state="CA",
    phone="326-123-5000",
    website_link="https://www.gunsnpetalsband.com",
    facebook_link="https://www.facebook.com/GunsNPetals",
    seeking_venue=True,
    seeking_description="Looking for shows to perform at in "
                        "the San Francisco Bay Area!",
    image_link="https://images.unsplash.com/photo-1549213783-8284d0336c4f?"
               "ixlib=rb-1.2.1&ixid=eyJhcHBfaWQiOjEyMDd9&auto=format&"
               "fit=crop&w=300&q=80"
)

artist2 = Artist(
    name="Matt Quevedo",
    genres=["Jazz"],
    city="New York",
    state="NY",
    phone="300-400-5000",
    facebook_link="https://www.facebook.com/mattquevedo923251523",
    seeking_venue=False,
    image_link="https://images.unsplash.com/"
               "photo-1495223153807-b916f75de8c5?ixlib=rb-1.2.1&"
               "ixid=eyJhcHBfaWQiOjEyMDd9&auto=format&fit=crop&w=334&q=80",
)

artist3 = Artist(
    name="The Wild Sax Band",
    genres=["Jazz", "Classical"],
    city="San Francisco",
    state="CA",
    phone="432-325-5432",
    seeking_venue=False,
    image_link="https://images.unsplash.com/"
               "photo-1558369981-f9ca78462e61?ixlib=rb-1.2.1&"
               "ixid=eyJhcHBfaWQiOjEyMDd9&auto=format&fit=crop&w=794&q=80"
)

"""Show test data."""

show1 = Show(
    venue_id=1,
    artist_id=1,
    start_time="2019-05-21T21:30:00.000Z"
)

show2 = Show(
    venue_id=3,
    artist_id=2,
    start_time="2019-06-15T23:00:00.000Z"
)

show3 = Show(
    venue_id=3,
    artist_id=3,
    start_time="2035-04-01T20:00:00.000Z"
)

show4 = Show(
    venue_id=3,
    artist_id=3,
    start_time="2035-04-08T20:00:00.000Z"
)

show5 = Show(
    venue_id=3,
    artist_id=3,
    start_time="2035-04-15T20:00:00.000Z"
)

"""Insert object created above to the db."""

venues = [venue1, venue2, venue3]
artists = [artist1, artist2, artist3]
shows = [show1, show2, show3, show4, show5]


def run():
    """Insert data into the database."""
    for v in venues:
        Venue.insert(v)

    for a in artists:
        Artist.insert(a)

    for s in shows:
        Show.insert(s)


if __name__ == '__main__':
    """Main entry point."""
    try:
        # run()
        pass
    except Exception as e:
        print(f"Somethong went wrong. Details: {e}")
    else:
        print("Data loaded.")
