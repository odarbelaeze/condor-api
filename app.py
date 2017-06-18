import json

from apistar import App, Route, http, Response
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


def get_all_rankings() -> Response:
    db = condor_db.session()
    rankings = [
        object_to_dict(matrix, sc.Ranking.properties.keys())
        for matrix in RankingMatrix.list(db)
    ]
    db.commit()
    return Response(rankings)


def get_ranking(eid) -> Response:
    db = condor_db.session()
    ranking = RankingMatrix.find_by_eid(db, eid)
    if not ranking:
        return Response(
            {'message': 'The especified eid is not found on database'},
            status=404,
        )
    db.commit()
    return Response(object_to_dict(ranking, sc.Ranking.properties.keys()))


def get_all_bibliographies() -> Response:
    db = condor_db.session()
    bibliographies = [
        object_to_dict(bib, sc.Bibliography.properties.keys())
        for bib in Bibliography.list(db)
    ]
    db.commit()
    return Response(bibliographies)


def get_bibliography(eid) -> Response:
    db = condor_db.session()
    bibliography = Bibliography.find_by_eid(db, eid)
    if not bibliography:
        return Response(
            {'message': 'The especified eid is not found on database'},
            status=404,
        )
    db.commit()
    return Response(
        object_to_dict(bibliography, sc.Bibliography.properties.keys())
    )


def get_all_documents(query_params: http.QueryParams) -> Response:
    db = condor_db.session()
    bibliography_eid = query_params["bibliography_eid"]
    if not bibliography_eid:
        return Response(
            {'message': 'The especified eid is not found on database'},
            status=404,
        )
    documents = [
        object_to_dict(doc, sc.Document.properties.keys())
        for doc in Document.list(db, bibliography_eid)
    ]
    db.commit()
    return Response(documents)


def get_document(eid) -> Response:
    db = condor_db.session()
    document = Document.find_by_eid(db, eid)
    if not document:
        return Response(
            {'message': 'The especified eid is not found on database'},
            status=404,
        )
    db.commit()
    return Response(object_to_dict(document, sc.Document.properties.keys()))


def get_all_matrices() -> Response:
    db = condor_db.session()
    matrices = [
        object_to_dict(mat, sc.Matrix.properties.keys())
        for mat in TermDocumentMatrix.list(db)
    ]
    db.commit()
    return Response(matrices)


def get_matrix(eid) -> Response:
    db = condor_db.session()
    matrix = TermDocumentMatrix.find_by_eid(db, eid)
    if not matrix:
        return Response(
            {'message': 'The especified eid is not found on database'},
            status=404,
        )
    db.commit()
    return Response(object_to_dict(matrix, sc.Matrix.properties.keys()))


routes = [
    Route('/ranking', 'GET', get_all_rankings),
    Route('/ranking/{eid}', 'GET', get_ranking),

    Route('/bibliography', 'GET', get_all_bibliographies),
    Route('/bibliography/{eid}', 'GET', get_bibliography),

    Route('/document', 'GET', get_all_documents),
    Route('/document/{eid}', 'GET', get_document),

    Route('/matrix', 'GET', get_all_matrices),
    Route('/matrix/{eid}', 'GET', get_matrix)
]

app = App(routes=routes)
