# bultin library

# external libraries
from sanic import Sanic
from sanic.response import text, json
from condor.dbutil import requires_db
from condor.models import Bibliography, Document


app = Sanic(__name__)


@app.route("/ping")
async def start(request):
    return text("pong")


@app.route("/bibliography")
@requires_db
async def format_list_bibliography(db, request):
    to_return = [{
        'eid': bib.eid,
        'description': bib.description,
        'created': bib.created,
        'modified': bib.modified
    } for bib in list_bibliography_from_db(db, count=10)]
    return json(to_return)


@app.route('/document')
@requires_db
async def list_documents(database, request):
    """
    List the documents associated with a bibliography.
    """
    bibliography_eid = request.args.get('bibliography', None)
    if not bibliography_eid:
        return json({
            'error': 'You must suply a bibliography eid.',
            'details': 'Fill in the bibliography field.'
        }, status=400)
    to_return = [
        {
            'eid': doc.eid,
            'title': doc.title,
            'description': doc.description,
            'created': doc.created,
            'modified': doc.modified
        }
        for doc in Document.list(database, bibliography_eid)
    ]
    return json(to_return)


def list_bibliography_from_db(db, count):
    """
    List all the document sets.
    """
    bibliography_sets = db.query(Bibliography).order_by(
        Bibliography.created.desc()
    ).limit(count)
    return bibliography_sets.all()


if __name__ == "__main__":
    app.run(
        debug=True,
        host="0.0.0.0",
        port=8000
    )
