import json

import condor.dbutil as condor_db
from apistar import App, Route
from condor.models import (
    Bibliography,
    RankingMatrix,
    TermDocumentMatrix,
    Document
)


def condor_table_to_dict(condor_table):
    def to_serializable(value):
        try:
            json.dumps(value)
            return value
        except Exception:
            return str(value)

    dict_content = {
        key: to_serializable(condor_table.__dict__[key])
        for key in condor_table.__dict__.keys()
        if key is not '_sa_instance_state'
    }
    return dict_content


def get_all_rankings():
    db = condor_db.session()
    rankings = [
        condor_table_to_dict(matrix)
        for matrix in RankingMatrix.list(db)
    ]
    db.commit()
    return rankings


def get_ranking(eid):
    db = condor_db.session()
    ranking = RankingMatrix.find_by_eid(db, eid)
    if not ranking:
        return {
            'message': 'The especified eid is not found on database'
        }
    db.commit()
    return condor_table_to_dict(ranking)


def get_all_bibliographies():
    db = condor_db.session()
    bibliographies = [
        condor_table_to_dict(bib)
        for bib in Bibliography.list(db)
    ]
    db.commit()
    return bibliographies


def get_bibliography(eid):
    db = condor_db.session()
    bibliography = Bibliography.find_by_eid(db, eid)
    if not bibliography:
        return {
            'message': 'The especified eid is not found on database'
        }
    db.commit()
    return condor_table_to_dict(bibliography)


def get_all_documents():
    db = condor_db.session()
    bibliography_eid = request.args.get('bibliography', None)
    if not bibliography_eid:
        return {
            'message': 'The especified eid is not found on database'
        }

    documents = [
        condor_table_to_dict(doc)
        for doc in Document.list(db, bibliography_eid)
    ]
    db.commit()
    return documents


def get_document(eid):
    db = condor_db.session()
    document = Document.find_by_eid(db, eid)
    if not document:
        return {
            'message': 'The especified eid is not found on database.',
        }
    db.commit()
    return condor_table_to_dict(document)


def get_all_matrices():
    db = condor_db.session()
    matrices = [
        condor_table_to_dict(mat)
        for mat in TermDocumentMatrix.list(db)
    ]
    db.commit()
    return matrices


def get_matrix(eid):
    db = condor_db.session()
    matrix = TermDocumentMatrix.find_by_eid(db, eid)
    if not matrix:
        return {
            'message': 'The especified eid is not found on database'
        }
    db.commit()
    return condor_table_to_dict(matrix)


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
