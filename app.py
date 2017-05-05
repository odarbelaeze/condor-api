# bultin library

# external libraries
from sanic import Sanic
from sanic.response import json
from condor.dbutil import requires_db
from condor.models import RankingMatrix

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

if __name__ == "__main__":
    app.run(
        debug=True,
        host="0.0.0.0",
        port=8000
    )
