# bultin library

# external libraries
from sanic import Sanic
from sanic.response import text, json
from condor.dbutil import requires_db
from condor.models import Bibliography, RankingMatrix

app = Sanic(__name__)


@app.route("/ping")
async def start(request):
    return text("pong")

@app.route("/matrix", methods=["GET", "POST"])
@requires_db
async def matrix(db, request):
    if request.method == "GET":
        ranking_matrices = [
            {
                "kind": matrix.kind,
                "build_options": matrix.build_options,
                "ranking_matrix_path": matrix.ranking_matrix_path
            }
            for matrix in list_ranking_matrix(db, count=10)
        ]
        return json(ranking_matrices)
    elif request.method == "POST":
        return json({"ping": "pong"})

def list_ranking_matrix(db, count):
    """
    List all ranking matrices
    """
    ranking_matrices = db.query(RankingMatrix).order_by(
        RankingMatrix.created.desc()
    ).limit(count)
    return ranking_matrices

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
