# bultin library

# external libraries
from sanic import Sanic
from sanic.response import text, json
from condor.dbutil import requires_db
from condor.models import Bibliography, RankingMatrix, \
    TermDocumentMatrix, Document


app = Sanic(__name__)


@app.route("/ping")
async def start(request):
    return text("pong")


@app.route("/ranking", methods=["GET"])
@requires_db
async def list_rankings(db, request):
    ranking_matrices = [
        {
            "eid": matrix.eid,
            "term_document_matrix_eid": matrix.term_document_matrix_eid,
            "kind": matrix.kind,
            "build_options": matrix.build_options,
            "ranking_matrix_path": matrix.ranking_matrix_path
        }
        for matrix in RankingMatrix.list(db)
    ]
    return json(ranking_matrices)


@app.route("/ranking/<eid>", methods=["GET"])
@requires_db
async def ranking(db, request, eid):
    ranking_matrices = RankingMatrix.find_by_eid(db, eid)
    if not ranking_matrices:
        return json({
            "message": "The especified eid is not found on database"
        }, status=404)
    return json({
            "eid": ranking_matrices.eid,
            "term_document_matrix_eid":
                    ranking_matrices.term_document_matrix_eid,
            "kind": ranking_matrices.kind,
            "build_options": ranking_matrices.build_options,
            "ranking_matrix_path": ranking_matrices.ranking_matrix_path
    })


@app.route("/bibliography")
@requires_db
async def list_bibliographies(db, request):
    bibliographies = [
        {
            "eid": bib.eid,
            "description": bib.description,
            "created": bib.created,
            "modified": bib.modified
        }
        for bib in Bibliography.list(db)
    ]
    return json(bibliographies)


@app.route("/bibliography/<eid>")
@requires_db
async def bibliography(db, request, eid):
    """
    Bibliography associated with a blibliography eid
    """
    bibliography = Bibliography.find_by_eid(db, eid)

    if not bibliography:
        return json({
            "message": "The especified eid is not found on database"
        }, status=404)

    return json({
        "eid": bibliography.eid,
        "description": bibliography.description,
        "created": bibliography.created,
        "modified": bibliography.modified
    })


@app.route('/document')
@requires_db
async def list_documents(database, request):
    """
    List the documents associated with a bibliography.
    """
    bibliography_eid = request.args.get('bibliography', None)
    if not bibliography_eid:
        return json(
            {
                'error': 'You must suply a bibliography eid.',
                'details': 'Fill in the bibliography field.'
            },
            status=400
        )

    documents = [
        {
            'eid': doc.eid,
            'title': doc.title,
            'description': doc.description,
            'created': doc.created,
            'modified': doc.modified
        }
        for doc in Document.list(database, bibliography_eid)
    ]
    return json(documents)


@app.route('/document/<eid>')
@requires_db
async def document(database, request, eid):
    doc = Document.find_by_eid(database, eid)
    if not doc:
        return json({
            'message': 'The especified eid is not found on database.',
        }, status=404)
    return json({
        'eid': doc.eid,
        'title': doc.title,
        'description': doc.description,
        'created': doc.created,
        'modified': doc.modified
    })



@app.route("/matrix")
@requires_db
async def list_term_document_matrices(db, request):
    document_matrices = [
        {
            "eid": document.eid,
            "bibliography_eid": document.bibliography_eid,
            "bibliography_options": document.bibliography_options,
            "processing_options": document.processing_options,
            "term_list_path": document.term_list_path,
            "matrix_path": document.matrix_path
        }
        for document in TermDocumentMatrix.list(db)
    ]
    return json(document_matrices)


@app.route("/matrix/<eid>")
@requires_db
async def term_document_matrix(db, request, eid):
    document_matrices = TermDocumentMatrix.find_by_eid(db, eid)
    if not document_matrices:
        return json({
            "message": "The especified eid is not found on database"
        }, status=404)
    return json({
            "eid": document_matrices.eid,
            "bibliography_eid": document_matrices.bibliography_eid,
            "bibliography_options": document_matrices.bibliography_options,
            "processing_options": document_matrices.processing_options,
            "term_list_path": document_matrices.term_list_path,
            "matrix_path": document_matrices.matrix_path
    })


if __name__ == "__main__":
    app.run(
        debug=True,
        host="0.0.0.0",
        port=8000,
        log_config=None,
    )
