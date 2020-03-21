from event.app import app


@app.route("/")
def base():
    return "Hey there"
