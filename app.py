# bultin library

# external libraries
from sanic import Sanic
from sanic.response import text

@app.route("/ping")
async def start(request):
    return text("pong")


if __name__ == "__main__":
    app.run(
        debug=True,
        host="0.0.0.0",
        port=8000
    )
