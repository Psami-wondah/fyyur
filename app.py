# ----------------------------------------------------------------------------#
# Imports
# ----------------------------------------------------------------------------#


from flask import Flask, render_template
from flask_moment import Moment
import logging
from logging import Formatter, FileHandler
from forms import *
from flask_migrate import Migrate
from controllers import artist, show, venue
from utils import format_datetime

from exts import db


# ----------------------------------------------------------------------------#
# App Config.
# ----------------------------------------------------------------------------#


def register_extensions(app):
    db.init_app(app)
    ...


def create_app(config):
    app = Flask(__name__)
    app.config.from_object(config)

    register_extensions(app)
    return app


app = create_app(config="config")

app.register_blueprint(artist.artist_page)
app.register_blueprint(show.show_page)
app.register_blueprint(venue.venue_page)


moment = Moment(app)
migrate = Migrate(app=app, db=db)

# TODO: connect to a local postgresql database - Done

# ----------------------------------------------------------------------------#
# Filters.
# ----------------------------------------------------------------------------#



app.jinja_env.filters["datetime"] = format_datetime


# ----------------------------------------------------------------------------#
# Controllers.
# ----------------------------------------------------------------------------#


@app.route("/")
def index():
    return render_template("pages/home.html")


@app.errorhandler(404)
def not_found_error(error):
    return render_template("errors/404.html"), 404


@app.errorhandler(500)
def server_error(error):
    return render_template("errors/500.html"), 500


if not app.debug:
    file_handler = FileHandler("error.log")
    file_handler.setFormatter(
        Formatter("%(asctime)s %(levelname)s: %(message)s [in %(pathname)s:%(lineno)d]")
    )
    app.logger.setLevel(logging.INFO)
    file_handler.setLevel(logging.INFO)
    app.logger.addHandler(file_handler)
    app.logger.info("errors")

# ----------------------------------------------------------------------------#
# Launch.
# ----------------------------------------------------------------------------#

# Default port:
if __name__ == "__main__":
    app.run()

# Or specify port manually:

# if __name__ == "__main__":
# port = int(os.environ.get('PORT', 5000))
# app.run(host="0.0.0.0", port=8000)
