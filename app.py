from flask import Flask, render_template, request
from dotenv import load_dotenv
import requests
import json
import os

load_dotenv()

app = Flask(__name__, template_folder="web/public")

AI_POST_HEADERS = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:123.0) Gecko/20100101 Firefox/123.0",
    "Accept": "application/json",
    "Accept-Language": "en-US,en;q=0.5",
    "Content-Type": "application/json",
    "Authorization": f"Bearer {os.environ['OLLAMA_TOKEN']}",
    "Sec-Fetch-Dest": "empty",
    "Sec-Fetch-Mode": "cors",
    "Sec-Fetch-Site": "same-origin",
    "Sec-GPC": "1",
}

@app.route('/')
def index():
    return render_template("index.html")

@app.route("/model", methods=["POST"])
def model_route():
    return request.get_json()
    
@app.route("/model_attrs")
def get_model_attrs():
    response_initial = requests.post(
        "http://localhost:3000/ollama/api/generate",
        headers=AI_POST_HEADERS,
        data=json.dumps({
            "model": "modelgen:latest",
            "prompt": request.args.get("keywords"),
            "stream": False,
        }),
    )

    response_final = requests.post(
        "http://localhost:3000/ollama/api/generate",
        headers=AI_POST_HEADERS,
        data=json.dumps({
            "model": "modelgen-out:latest",
            "prompt": json.loads(response_initial.text)["response"],
            "stream": False,
        }),
    )

    response_text_final: str = json.loads(response_final.text)["response"]

    
    # parse for the first set of brackets

    bracket_level = 0
    start_bracket_index = -1
    for i, char in enumerate(response_text_final):
        if char == "[":
            bracket_level += 1
            if start_bracket_index == -1:
                start_bracket_index = i
        elif char == "]":
            bracket_level -= 1
            if bracket_level == 0:
                return response_text_final[start_bracket_index:i + 1]
            
    return "TODO didn't find a matched set of brackets"


def main():
    app.run(debug=True)

if __name__ == "__main__":
    main()