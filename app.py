from flask import Flask, render_template, send_from_directory, request
from dotenv import load_dotenv
import requests
import json
import os
import time

load_dotenv()

app = Flask(__name__, template_folder="web/build", static_folder="web/build/static")

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

@app.route("/")
def index():
    return render_template("index.html")

# @app.route("/model", methods=["POST"])
# def model_route():
#     return request.get_json()
    
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


POLL_TIMEOUT = 5
@app.route("/model/")
def get_model():
    response_llm = requests.post(
        "http://localhost:3000/ollama/api/generate",
        headers=AI_POST_HEADERS,
        data=json.dumps({
            "model": "modelgen-new:latest",
            "prompt": request.args.get("keywords"),
            "stream": False,
        }),
    )
    # horns_prompt = " A horn that sprawls out from its forehead, twisting and turning in intricate whorls reminiscent of the bark of a maple tree. Each twirl and curl is adorned with a subtle, warm hue that deepens towards the base, resembling the rich autumn colors of a maple leaf. The horn's texture is rough and gnarled, evoking the ridged surface of a maple tree bark."
    [horns_prompt, eyes_prompt] = json.loads(response_llm.text)["response"].split("\n")
    
    print([horns_prompt, eyes_prompt])
    return json.dumps([
        gen_mesh_url(horns_prompt),
        gen_mesh_url(eyes_prompt),
    ])


def gen_mesh_url(prompt: str):
    # image
    response_gen_image_session = requests.post(
        "https://api.csm.ai:5566/tti-sessions",
        headers={
            "x-api-key": os.environ['CSM_API_KEY'],
            "Content-Type": "application/json",
        },
        data=json.dumps({
            "prompt": prompt,
        }),
    )
    print(response_gen_image_session.text)
    image_session_code = json.loads(response_gen_image_session.text)["data"]["session_code"]
    print(image_session_code)

    # wait for image to complete
    image_status = ""
    while image_status != "completed":
        time.sleep(POLL_TIMEOUT)

        response_get_image = requests.get(
            f"https://api.csm.ai:5566/tti-sessions/{image_session_code}",
            headers={
                "x-api-key": os.environ['CSM_API_KEY'],
                "Content-Type": "application/json",
            },
        )
        print(response_get_image.text)
        image_status = json.loads(response_get_image.text)["data"]["status"]

    image_url = json.loads(response_get_image.text)["data"]["image_url"]
    print(image_url)

    # mesh
    response_gen_mesh_session = requests.post(
        "https://api.csm.ai:5566/image-to-3d-sessions",
        headers={
            "x-api-key": os.environ['CSM_API_KEY'],
            "Content-Type": "application/json",
        },
        data=json.dumps({
            "image_url": image_url,
        })
    )
    print(response_gen_mesh_session.text)
    mesh_session_code = json.loads(response_gen_mesh_session.text)["data"]["session_code"]
    print(mesh_session_code)

    mesh_status = ""
    while mesh_status != "spin_generate_done":
        time.sleep(POLL_TIMEOUT)

        response_await_spins = requests.get(
            f"https://api.csm.ai:5566/image-to-3d-sessions/{mesh_session_code}",
            headers={
                "x-api-key": os.environ['CSM_API_KEY'],
                "Content-Type": "application/json",
            },
        )
        print(response_await_spins.text)
        # mesh_status = json.loads(response_await_spins.text)["data"].get("status")

    # response_request_mesh = requests.post(
    #     f"https://api.csm.ai:5566/image-to-3d-sessions/get-3d/{mesh_session_code}",
    #     headers={
    #         "x-api-key": os.environ['CSM_API_KEY'],
    #         "Content-Type": "application/json",
    #     },
    #     data=json.dumps({
    #         "selected_spin_index": 0,
    #         "selected_spin": json.loads(response_await_spins.text)["data"]["spins"][0]["image_url"],
    #         "image_url": json.loads(response_await_spins.text)["data"]["image_url"],
    #         "coarse": False,
    #     }),
    # )
    response_request_mesh = requests.post(
        f"https://api.csm.ai:5566/image-to-3d-sessions/get-3d/preview/{mesh_session_code}",
        headers={
            "x-api-key": os.environ['CSM_API_KEY'],
            "Content-Type": "application/json",
        },
        data=json.dumps({
            "selected_spin_index": 0,
            "selected_spin": json.loads(response_await_spins.text)["data"]["spins"][0]["image_url"],
        }),
    )
    print(response_request_mesh.text)
    mesh_status = json.loads(response_request_mesh.text)["data"].get("status")

    while mesh_status != "preview_done":
        time.sleep(POLL_TIMEOUT)

        response_await_mesh = requests.get(
            f"https://api.csm.ai:5566/image-to-3d-sessions/{mesh_session_code}",
            headers={
                "x-api-key": os.environ['CSM_API_KEY'],
                "Content-Type": "application/json",
            },
        )
        print(response_await_mesh.text)
        mesh_status = json.loads(response_await_mesh.text)["data"].get("status")

    response_get_mesh = requests.get(
        f"https://api.csm.ai:5566/image-to-3d-sessions/get-mesh/{mesh_session_code}",
        headers={
            "x-api-key": os.environ['CSM_API_KEY'],
            "Content-Type": "application/json",
        },
    )
    mesh_url = json.loads(response_get_mesh.text)["data"][0]["preview_mesh_url_glb"]
    print(mesh_url)

    return mesh_url

def main():
    app.run(debug=True)

if __name__ == "__main__":
    main()