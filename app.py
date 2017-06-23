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


def ping():
    """
    Simple healthcheck endpoint.
    """
    return "pong"


def get_all_rankings(session: CondorSession) -> List[sc.Ranking]:
    """
    List all ranking matrices from the database.
    """
    return [sc.Ranking(matrix) for matrix in RankingMatrix.list(session)]


def get_ranking(eid, session: CondorSession) -> Response:
    """
    List the ranking that has the specified eid from the database.
    """
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
    """
    List the bibliography that has the specified eid from the database.
    """
    bibliography = Bibliography.find_by_eid(session, eid)
    if not bibliography:
        return Response(
            {'message': 'The especified eid is not found on database'},
            status=404,
        )
    return Response(sc.Bibliography(bibliography))


def get_all_documents(bibliography: Param, session: CondorSession) -> Response:
    """
    List all documents that are related to a specific bibliography
    from the the database.
    """
    if not bibliography:
        return Response(
            {'message': 'The especified eid is not found on database'},
            status=400,
        )
    documents = [
        sc.Document(doc) for doc in Document.list(session, bibliography)
    ]
    return Response(documents)


def get_document(eid, session: CondorSession) -> Response:
    """
    List the document that has the specified eid from the database.
    """
    document = Document.find_by_eid(session, eid)
    if not document:
        return Response(
            {'message': 'The especified eid is not found on database'},
            status=404,
        )
    return Response(sc.Document(document))


def get_all_matrices(session: CondorSession) -> List[sc.Matrix]:
    """
    List all matrices in the database.
    """
    return [sc.Matrix(mat) for mat in TermDocumentMatrix.list(session)]


def create_bibliography(session: CondorSession, descriptor: sc.BibliographyDescriptor) -> Response:
    """
    reate a bibliography.
    """
    description = descriptor.get('description')
        or 'Document set from {count} {kind} files.'.format(
        count=len(descriptor.get('files')),
        kind=descriptor.get('kind')
    )
    bib = Bibliography(description=description)
    session.add(bib)
    session.flush()

    mappings = Document.mappings_from_files(
        list([file.name for file in descriptor.get('files')]),
        kind,
        full_text_path=descriptor.get('fulltext'),
        force=descriptor.get('no_cache'),
        bibliography_eid=bib.eid
    )

    if descriptor.get('languages'):
        bib.description += ' Filtered to {}.'.format(
            ', '.join(descriptor.get('languages'))
        )
        mappings = [
            m
            for m in mappings
            if m.get('language', 'english').lower() in descriptor.get('languages')
        ]

    session.bulk_insert_mappings(
        Document,
        mappings
    )

    session.commit()


def create_matrix(
        descriptor: sc.MatrixDescriptor, session: CondorSession) -> Response:
    """
    Create a term document matrix.
    """
    bibliography = Bibliography.find_by_eid(session, descriptor.get('bibliography'))
    if bibliography is None:
        return Response(
            {
                'message': 'The especified bibliography eid is not found on database'
            },
            status=404,
        )
    td_matrix = TermDocumentMatrix.from_bibliography_set(
        bibliography,
        regularise=descriptor.get('regularise'),
        fields=descriptor.get('fields')
    )
    session.add(td_matrix)
    session.commit()
    return Response(sc.Matrix(td_matrix))


def get_matrix(eid, session: CondorSession) -> Response:
    """
    List the matrix that has the specified eid from the database.
    """
    matrix = TermDocumentMatrix.find_by_eid(session, eid)
    if not matrix:
        return Response(
            {'message': 'The especified eid is not found on database'},
            status=404,
        )
    return Response(sc.Matrix(matrix))


routes = [
    Route('/ping', 'GET', ping),

    Route('/document', 'GET', get_all_documents),
    Route('/document/{eid}', 'GET', get_document),

    Route('/bibliography', 'GET', get_all_bibliographies),
    Route('/bibliography/{eid}', 'GET', get_bibliography),

    Route('/matrix', 'GET', get_all_matrices),
    Route('/matrix', 'POST', create_matrix),
    Route('/matrix/{eid}', 'GET', get_matrix),

    Route('/ranking', 'GET', get_all_rankings),
    Route('/ranking/{eid}', 'GET', get_ranking),

    Include('/docs', docs_routes),
    Include('/static', static_routes),
]

app = App(routes=routes)
