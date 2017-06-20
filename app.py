import json

from apistar import App, Route, Include, http, Response
from apistar.docs import docs_routes
from apistar.schema import List
from apistar.statics import static_routes
import condor.dbutil as condor_db
import schemas as sc
from condor.models import (
    Bibliography,
    RankingMatrix,
    TermDocumentMatrix,
    Document
)


def object_to_dict(obj, fields):
    def to_serializable(value):
        try:
            json.dumps(value)
            return value
        except Exception:
            return str(value)
    return {
        field: to_serializable(getattr(obj, field)) for field in fields
    }


def ping():
    return "pong"


def get_all_rankings() -> List[sc.Ranking]:
    """
    List all ranking matrices from the database.
    """
    session = condor_db.session()
    return [sc.Ranking(matrix) for matrix in RankingMatrix.list(session)]


def get_ranking(eid) -> Response:
    db = condor_db.session()
    ranking = RankingMatrix.find_by_eid(db, eid)
    if not ranking:
        return Response(
            {'message': 'The especified eid is not found on database'},
            status=404,
        )
    return Response(sc.Ranking(ranking))


def get_all_bibliographies() -> List[sc.Bibliography]:
    session = condor_db.session()
    return [sc.Bibliography(bib) for bib in Bibliography.list(session)]


def get_bibliography(eid) -> Response:
    db = condor_db.session()
    bibliography = Bibliography.find_by_eid(db, eid)
    if not bibliography:
        return Response(
            {'message': 'The especified eid is not found on database'},
            status=404,
        )
    return Response(sc.Bibliography(bibliography))


def get_all_documents(bibliography: http.QueryParam) -> Response:
    db = condor_db.session()
    if not bibliography:
        return Response(
            {'message': 'The especified eid is not found on database'},
            status=400,
        )
    documents = [
        object_to_dict(doc, sc.Document.properties.keys())
        for doc in Document.list(db, bibliography)
    ]
    return Response(documents)


def get_document(eid) -> Response:
    db = condor_db.session()
    document = Document.find_by_eid(db, eid)
    if not document:
        return Response(
            {'message': 'The especified eid is not found on database'},
            status=404,
        )
    return Response(object_to_dict(document, sc.Document.properties.keys()))


def get_all_matrices() -> List[sc.Matrix]:
    db = condor_db.session()
    matrices = [
        object_to_dict(mat, sc.Matrix.properties.keys())
        for mat in TermDocumentMatrix.list(db)
    ]
    return matrices


def get_matrix(eid) -> Response:
    db = condor_db.session()
    matrix = TermDocumentMatrix.find_by_eid(db, eid)
    if not matrix:
        return Response(
            {'message': 'The especified eid is not found on database'},
            status=404,
        )
    return Response(object_to_dict(matrix, sc.Matrix.properties.keys()))


routes = [
    Route('/ping', 'GET', ping),

    Route('/ranking', 'GET', get_all_rankings),
    Route('/ranking/{eid}', 'GET', get_ranking),

    Route('/bibliography', 'GET', get_all_bibliographies),
    Route('/bibliography/{eid}', 'GET', get_bibliography),

    Route('/document', 'GET', get_all_documents),
    Route('/document/{eid}', 'GET', get_document),

    Route('/matrix', 'GET', get_all_matrices),
    Route('/matrix/{eid}', 'GET', get_matrix),

    Include('/docs', docs_routes),
    Include('/static', static_routes),
]

app = App(routes=routes)
