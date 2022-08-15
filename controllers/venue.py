from models import Venue, Show
from flask import render_template, request, flash, Blueprint, redirect, url_for
from datetime import datetime
from exts import db
from forms import VenueForm

venue_page = Blueprint("venue_page", __name__, template_folder="templates")

#  Venues
#  ----------------------------------------------------------------


@venue_page.route("/venues")
def venues():
    # TODO: replace with real venues data.
    #       num_upcoming_shows should be aggregated based on number of upcoming shows per venue. - Done
    venues = (
        Venue.query.with_entities(Venue.city, Venue.state)
        .group_by(Venue.city, Venue.state)
        .all()
    )


    def get_venue_obj(venue: Venue):
        upcoming_shows = Show.query.filter(
            Show.venue_id == venue.id, Show.start_time >= datetime.today()
        )
        return {
            "id": venue.id,
            "name": venue.name,
            "num_upcoming_shows": upcoming_shows.count(),
        }

    data = [
        {
            "city": location[0],
            "state": location[1],
            "venues": list(
                map(
                    get_venue_obj,
                    Venue.query.filter(
                        Venue.city == location[0], Venue.state == location[1]
                    ),
                )
            ),
        }
        for location in venues
    ]

    return render_template("pages/venues.html", areas=data)


@venue_page.route("/venues/search", methods=["POST"])
def search_venues():
    # TODO: implement search on artists with partial string search. Ensure it is case-insensitive. - Done
    # seach for Hop should return "The Musical Hop".
    # search for "Music" should return "The Musical Hop" and "Park Square Live Music & Coffee"
    search_term = request.form.get("search_term", "")
    data = Venue.query.filter(Venue.name.ilike(f"%{search_term}%"))

    def get_venue_obj(venue: Venue):
        upcoming_shows = Show.query.filter(
            Show.venue_id == venue.id, Show.start_time >= datetime.today()
        )
        return {
            "id": venue.id,
            "name": venue.name,
            "num_upcoming_shows": upcoming_shows.count(),
        }

    response = {"count": data.count(), "data": list(map(get_venue_obj, data))}
    return render_template(
        "pages/search_venues.html",
        results=response,
        search_term=request.form.get("search_term", ""),
    )


@venue_page.route("/venues/<int:venue_id>")
def show_venue(venue_id):
    # shows the venue page with the given venue_id
    # TODO: replace with real venue data from the venues table, using venue_id - Done

    venue = Venue.query.get(venue_id)
    venue_shows = Show.query.join(Venue).filter(Show.venue_id==venue_id)

    def get_show_obj(show: Show):
        return {
            "artist_id": show.artist_id,
            "artist_name": show.artist.name,
            "artist_image_link": show.artist.image_link,
            "start_time": str(show.start_time),
        }

    past_shows = venue_shows.filter(Show.start_time < datetime.today())
    upcoming_shows = venue_shows.filter(Show.start_time >= datetime.today())
    past_shows_count = past_shows.count()
    upcoming_shows_count = upcoming_shows.count()

    past_shows = list(map(get_show_obj, past_shows))
    upcoming_shows = list(map(get_show_obj, upcoming_shows))

    data = {
        "id": venue.id,
        "name": venue.name,
        "genres": venue.genres,
        "address": venue.address,
        "city": venue.city,
        "state": venue.state,
        "phone": venue.phone,
        "website": venue.website_link,
        "facebook_link": venue.facebook_link,
        "seeking_talent": venue.seeking_talent,
        "seeking_description": venue.seeking_description,
        "image_link": venue.image_link,
        "past_shows": past_shows,
        "upcoming_shows": upcoming_shows,
        "past_shows_count": past_shows_count,
        "upcoming_shows_count": upcoming_shows_count,
    }
    return render_template("pages/show_venue.html", venue=data)


#  Create Venue
#  ----------------------------------------------------------------


@venue_page.route("/venues/create", methods=["GET"])
def create_venue_form():
    form = VenueForm()
    return render_template("forms/new_venue.html", form=form)


@venue_page.route("/venues/create", methods=["POST"])
def create_venue_submission():
    form = VenueForm(request.form)

    new_venue = Venue(
        name=form.name.data,
        city=form.city.data,
        state=form.state.data,
        address=form.address.data,
        phone=form.phone.data,
        genres=form.genres.data,
        image_link=form.image_link.data,
        facebook_link=form.facebook_link.data,
        website_link=form.website_link.data,
        seeking_talent=form.seeking_talent.data,
        seeking_description=form.seeking_description.data,
    )

    # TODO: insert form data as a new Venue record in the db, instead - Done
    try:
        db.session.add(new_venue)
        flash("Venue " + new_venue.name + " was successfully listed!")
        db.session.commit()
    except Exception as e:
        db.session.rollback()
        flash(f"Venue was not added due to an error: {e}", "error")
    finally:
        db.session.close()
    # TODO: modify data to be the data object returned from db insertion  - Done

    # on successful db insert, flash success  - Done

    # TODO: on unsuccessful db insert, flash an error instead.  - Done
    # e.g., flash('An error occurred. Venue ' + data.name + ' could not be listed.')
    # see: http://flask.pocoo.org/docs/1.0/patterns/flashing/
    return render_template("pages/home.html")


@venue_page.route("/venues/<venue_id>", methods=["DELETE"])
def delete_venue(venue_id):
    # TODO: Complete this endpoint for taking a venue_id, and using
    # SQLAlchemy ORM to delete a record. Handle cases where the session commit could fail.  - Done
    try:
        venue = Venue.query.get(venue_id)
        db.session.delete(venue)

        db.session.commit()
        flash(f"Venue was Succesfully deleted")
    except Exception as e:
        db.session.rollback()
        flash(f"Venue was not deleted due to an error: {e}", "error")
    finally:
        db.session.close()

    # BONUS CHALLENGE: Implement a button to delete a Venue on a Venue Page, have it so that  - Done
    # clicking that button delete it from the db then redirect the user to the homepage  - Done
    return None


@venue_page.route("/venues/<int:venue_id>/edit", methods=["GET"])
def edit_venue(venue_id):
    venue = Venue.query.get(venue_id)
    form = VenueForm(obj=venue)
    # TODO: populate form with values from venue with ID <venue_id>
    return render_template("forms/edit_venue.html", form=form, venue=venue)


@venue_page.route("/venues/<int:venue_id>/edit", methods=["POST"])
def edit_venue_submission(venue_id):
    # TODO: take values from the form submitted, and update existing
    form = VenueForm(request.form)
    venue = Venue.query.get(venue_id)
    venue.name = form.name.data
    venue.city = form.city.data
    venue.state = form.state.data
    venue.address = form.address.data
    venue.phone = form.phone.data
    venue.genres = form.genres.data
    venue.image_link = form.image_link.data
    venue.facebook_link = form.facebook_link.data
    venue.website_link = form.website_link.data
    venue.seeking_talent = form.seeking_talent.data
    venue.seeking_description = form.seeking_description.data

    # TODO: insert form data as a new Venue record in the db, instead  - Done
    try:
        db.session.commit()
        flash(f"Venue was Succesfully edited")
    except Exception as e:
        db.session.rollback()
        flash(f"Venue was not added due to an error: {e}", "error")
    finally:
        db.session.close()
    # venue record with ID <venue_id> using the new attributes
    return redirect(url_for("show_venue", venue_id=venue_id))
