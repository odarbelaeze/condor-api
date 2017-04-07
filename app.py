# bultin library

# external libraries
from sanic import Sanic
from sanic.response import text, json
from condor.dbutil import requires_db
from condor.models import BibliographySet


app = Sanic(__name__)


@app.route("/ping")
async def start(request):
    return text("pong")


@app.route("/list")
@requires_db
async def join_list(db, request):
    to_return = [{
        'eid': bib.eid,
        'description': bib.description,
        'created': bib.created,
        'modified': bib.modified
    } for bib in list_db(db, count=10)]
    return json(to_return)


def list_db(db, count):
    """
    List all the document sets.
    """
    bibliography_sets = db.query(BibliographySet).order_by(
        BibliographySet.created.desc()
    ).limit(count)
    return bibliography_sets.all()

if __name__ == "__main__":
    app.run(
        debug=True,
        host="0.0.0.0",
        port=8000
    )
