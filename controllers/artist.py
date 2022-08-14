from models import Venue, Show, Artist
from flask import render_template, request, flash, Blueprint, redirect, url_for
from datetime import datetime
from exts import db
from forms import ArtistForm

artist_page = Blueprint("artist_page", __name__, template_folder="templates")


#  Artists
#  ----------------------------------------------------------------
@artist_page.route("/artists")
def artists():
    # TODO: replace with real data returned from querying the database  - Done
    artists = Artist.query.all()
    return render_template("pages/artists.html", artists=artists)


@artist_page.route("/artists/search", methods=["POST"])
def search_artists():
    # TODO: implement search on artists with partial string search. Ensure it is case-insensitive.
    # seach for "A" should return "Guns N Petals", "Matt Quevado", and "The Wild Sax Band".
    # search for "band" should return "The Wild Sax Band".  - Done
    search_term = request.form.get("search_term", "")
    data = Artist.query.filter(Artist.name.ilike(f"%{search_term}%"))

    def get_artis_obj(artist: Artist):
        upcoming_shows = Show.query.filter(
            Show.artist_id == artist.id, Show.start_time >= datetime.today()
        )
        return {
            "id": artist.id,
            "name": artist.name,
            "num_upcoming_shows": upcoming_shows.count(),
        }

    response = {
        "count": data.count(),
        "data": list(map(get_artis_obj, data)),
    }
    return render_template(
        "pages/search_artists.html",
        results=response,
        search_term=request.form.get("search_term", ""),
    )


@artist_page.route("/artists/<int:artist_id>")
def show_artist(artist_id):
    # shows the artist page with the given artist_id
    # TODO: replace with real artist data from the artist table, using artist_id  - Done

    artist = Artist.query.get(artist_id)
    shows = Show.query.filter(Show.artist_id == artist_id)

    def get_show_obj(show: Show):
        return {
            "venue_id": show.venue_id,
            "venue_name": show.venue.name,
            "venue_image_link": show.venue.image_link,
            "start_time": str(show.start_time),
        }

    past_shows = shows.filter(Show.start_time < datetime.today())
    upcoming_shows = shows.filter(Show.start_time >= datetime.today())

    past_shows = list(map(get_show_obj, past_shows))
    upcoming_shows = list(map(get_show_obj, upcoming_shows))

    data = {
        "id": artist.id,
        "name": artist.name,
        "genres": artist.genres,
        "city": artist.city,
        "state": artist.state,
        "phone": artist.phone,
        "website": artist.website_link,
        "facebook_link": artist.facebook_link,
        "seeking_venue": artist.seeking_venue,
        "seeking_description": artist.seeking_description,
        "image_link": artist.image_link,
        "past_shows": past_shows,
        "upcoming_shows": upcoming_shows,
        "past_shows_count": len(past_shows),
        "upcoming_shows_count": len(upcoming_shows),
    }

    return render_template("pages/show_artist.html", artist=data)


#  Update
#  ----------------------------------------------------------------
@artist_page.route("/artists/<int:artist_id>/edit", methods=["GET"])
def edit_artist(artist_id):
    artist = Artist.query.get(artist_id)
    form = ArtistForm(obj=artist)
    # TODO: populate form with fields from artist with ID <artist_id>
    return render_template("forms/edit_artist.html", form=form, artist=artist)


@artist_page.route("/artists/<int:artist_id>/edit", methods=["POST"])
def edit_artist_submission(artist_id):
    form = ArtistForm(request.form)
    artist = Artist.query.get(artist_id)

    artist.name = form.name.data
    artist.city = form.city.data
    artist.state = form.state.data
    artist.phone = form.phone.data
    artist.genres = form.genres.data
    artist.image_link = form.image_link.data
    artist.facebook_link = form.facebook_link.data
    artist.website_link = form.website_link.data
    artist.seeking_venue = form.seeking_venue.data
    artist.seeking_description = form.seeking_description.data

    # TODO: take values from the form submitted, and update existing
    # artist record with ID <artist_id> using the new attributes  - Done
    try:
        db.session.commit()
        flash(f"Artist was Succesfully edited")
    except Exception as e:
        db.session.rollback()
        flash(f"Artist was not added due to an error: {e}", "error")
    finally:
        db.session.close()
    return redirect(url_for("show_artist", artist_id=artist_id))


#  Create Artist
#  ----------------------------------------------------------------


@artist_page.route("/artists/create", methods=["GET"])
def create_artist_form():
    form = ArtistForm()
    return render_template("forms/new_artist.html", form=form)


@artist_page.route("/artists/create", methods=["POST"])
def create_artist_submission():
    # called upon submitting the new artist listing form
    form = ArtistForm(request.form)
    # TODO: insert form data as a new Venue record in the db, instead  - Done
    artist = Artist(
        name=form.name.data,
        city=form.city.data,
        state=form.state.data,
        phone=form.phone.data,
        genres=form.genres.data,
        image_link=form.image_link.data,
        facebook_link=form.facebook_link.data,
        website_link=form.website_link.data,
        seeking_venue=form.seeking_venue.data,
        seeking_description=form.seeking_description.data,
    )
    # TODO: modify data to be the data object returned from db insertion
    try:
        db.session.add(artist)

        db.session.commit()
        flash("Artist " + artist.name + " was successfully listed!")
    except Exception as e:
        db.session.rollback()
        flash(f"Artist was not added due to an error: {e}", "error")
    finally:
        db.session.close()
    # on successful db insert, flash success
    # TODO: on unsuccessful db insert, flash an error instead.
    # e.g., flash('An error occurred. Artist ' + data.name + ' could not be listed.')  - Done
    return render_template("pages/home.html")
