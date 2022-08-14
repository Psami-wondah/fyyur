from models import Venue, Show
from flask import render_template, request, flash, Blueprint
from exts import db
from forms import ShowForm

show_page = Blueprint("show_page", __name__, template_folder="templates")


#  Shows
#  ----------------------------------------------------------------


@show_page.route("/shows")
def shows():
    # displays list of shows at /shows
    # TODO: replace with real venues data.

    def get_show_obj(show: Show):
        # venue =
        datum = {
            "venue_id": show.venue_id,
            "venue_name": show.venue.name,
            "artist_id": show.artist_id,
            "artist_name": show.artist.name,
            "artist_image_link": show.artist.image_link,
            "start_time": str(show.start_time),
        }
        return datum

    shows = Show.query.all()
    data = list(map(get_show_obj, shows))

    return render_template("pages/shows.html", shows=data)


@show_page.route("/shows/create")
def create_shows():
    # renders form. do not touch.
    form = ShowForm()
    return render_template("forms/new_show.html", form=form)


@show_page.route("/shows/create", methods=["POST"])
def create_show_submission():
    # called to create new shows in the db, upon submitting new show listing form
    form = ShowForm(request.form)
    # TODO: insert form data as a new Show record in the db, instead
    show = Show(
        artist_id=form.artist_id.data,
        venue_id=form.venue_id.data,
        start_time=form.start_time.data,
    )
    try:
        db.session.add(show)
        db.session.commit()
        flash("Show was successfully listed!")
    except Exception as e:
        db.session.rollback()
        flash(f"Show was not added due to an error: {e}", "error")
    finally:
        db.session.close()

    # on successful db insert, flash success

    # TODO: on unsuccessful db insert, flash an error instead.
    # e.g., flash('An error occurred. Show could not be listed.')  - Done
    # see: http://flask.pocoo.org/docs/1.0/patterns/flashing/
    return render_template("pages/home.html")
