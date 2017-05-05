# bultin library

# external libraries
from sanic import Sanic
from sanic.response import text, json
from condor.dbutil import requires_db
from condor.models import Bibliography, TermDocumentMatrix


app = Sanic(__name__)


@app.route("/ping")
async def start(request):
    return text("pong")


@app.route("/bibliography")
@requires_db
async def format_list_bibliography(db, request):
    to_return = [{
        "eid": bib.eid,
        "description": bib.description,
        "created": bib.created,
        "modified": bib.modified
    } for bib in list_bibliography_from_db(db, count=10)]
    return json(to_return)


def list_bibliography_from_db(db, count):
    """
    List all the document sets.
    """
    bibliography_sets = db.query(Bibliography).order_by(
        Bibliography.created.desc()
    ).limit(count)
    return bibliography_sets.all()


@app.route("/document_matrix")
@requires_db
async def format_term_document_matrix(db, request):
    to_return = [{
        "bibliography_eid": document.bibliography_eid,
        "bibliography_options": document.bibliography_options,
        "processing_options": document.processing_options,
        "term_list_path": document.term_list_path,
        "matrix_path": document.matrix_path
    } for document in list_term_document_matrix_from_db(db, count=10)]
    return json(to_return)


def list_term_document_matrix_from_db(db, count):
    """
    Lis all the term document matrix
    """
    document_matrix_sets = db.query(TermDocumentMatrix).order_by(
        TermDocumentMatrix.created.desc()
    ).limit(count)
    return document_matrix_sets.all()


if __name__ == "__main__":
    app.run(
        debug=True,
        host="0.0.0.0",
        port=8000
    )
