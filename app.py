# bultin library

# external libraries
from sanic import Sanic
from sanic.response import tex

app = Sanic(__name__)

@app.route("/ping")
async def start(request):
    return text("pong")


if __name__ == "__main__":
    app.run(
        debug=True,
        host="0.0.0.0",
        port=8000
    )
