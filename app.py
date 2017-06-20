import json

from apistar import App, Route, Include, Response
from apistar.http import QueryParam as Param
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


class CondorSession(object):
    """
    Injects a condor db session.
    """
    @classmethod
    def build(cls):
        """
        Default db session from condor.
        """
        return condor_db.session()


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


def get_all_rankings(session: CondorSession) -> List[sc.Ranking]:
    """
    List all ranking matrices from the database.
    """
    return [sc.Ranking(matrix) for matrix in RankingMatrix.list(session)]


def get_ranking(eid, session: CondorSession) -> Response:
    ranking = RankingMatrix.find_by_eid(session, eid)
    if not ranking:
        return Response(
            {'message': 'The especified eid is not found on database'},
            status=404,
        )
    return Response(sc.Ranking(ranking))


def get_all_bibliographies(session: CondorSession) -> List[sc.Bibliography]:
    """
    List all bibliographies in the database.
    """
    return [sc.Bibliography(bib) for bib in Bibliography.list(session)]


def get_bibliography(eid, session: CondorSession) -> Response:
    bibliography = Bibliography.find_by_eid(session, eid)
    if not bibliography:
        return Response(
            {'message': 'The especified eid is not found on database'},
            status=404,
        )
    return Response(sc.Bibliography(bibliography))


def get_all_documents(bibliography: Param, session: CondorSession) -> Response:
    if not bibliography:
        return Response(
            {'message': 'The especified eid is not found on database'},
            status=400,
        )
    documents = [
        object_to_dict(doc, sc.Document.properties.keys())
        for doc in Document.list(session, bibliography)
    ]
    return Response(documents)


def get_document(eid, session: CondorSession) -> Response:
    document = Document.find_by_eid(session, eid)
    if not document:
        return Response(
            {'message': 'The especified eid is not found on database'},
            status=404,
        )
    return Response(object_to_dict(document, sc.Document.properties.keys()))


def get_all_matrices(session: CondorSession) -> List[sc.Matrix]:
    matrices = [
        object_to_dict(mat, sc.Matrix.properties.keys())
        for mat in TermDocumentMatrix.list(session)
    ]
    return matrices


def get_matrix(eid, session: CondorSession) -> Response:
    matrix = TermDocumentMatrix.find_by_eid(session, eid)
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
