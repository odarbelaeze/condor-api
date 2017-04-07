# bultin library

# external libraries
from sanic import Sanic
from sanic.response import json

app = Sanic(__name__)

@app.route("/")
async def start(request):
    return json("hola": "mundo")


if __name__ == "__main__":
    app.run(
        debug=True,
        host="0.0.0.0",
        port=8000
    )
