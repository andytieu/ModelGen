from flask import Flask, render_template, request

app = Flask(__name__, template_folder="web/public")

@app.route('/')
def index():
    return render_template("index.html")

@app.route("/model", methods=["POST"])
def model_route():
    return request.get_json()

def main():
    app.run(debug=True)

if __name__ == "__main__":
    main()