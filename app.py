from flask import Flask, render_template, request

app = Flask(__name__, template_folder="web/public")

@app.route('/')
def index():
    return render_template("index.html")

@app.get("/key")
def get_key():
    return {"key": 100}

@app.route("/model", methods=["GET", "POST"])
def model_route():
    if request.method == "POST":
        return {"res": request.get_json()}

def main():
    app.run(debug=True)

if __name__ == "__main__":
    main()