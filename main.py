import random

import quart
import quart_cors
from quart import jsonify, request

from words import WORDS

# Note: Setting CORS to allow chat.openapi.com is required for ChatGPT to access your plugin
app = quart_cors.cors(quart.Quart(__name__), allow_origin="https://chat.openai.com")


@app.get("/new_word")
async def new_word():
    used_target_words = request.args.getlist("used_words")
    unused_words = [
        word for word in WORDS if word["target_word"] not in used_target_words
    ]

    if not unused_words:
        return jsonify({"error": "All words have been used"}), 400

    random_word = random.choice(unused_words)
    return jsonify(random_word)


@app.get("/logo.png")
async def plugin_logo():
    filename = "logo.png"
    return await quart.send_file(filename, mimetype="image/png")


@app.get("/.well-known/ai-plugin.json")
async def plugin_manifest():
    host = request.headers["Host"]
    with open("ai-plugin.json") as f:
        text = f.read()
        # This is a trick we do to populate the PLUGIN_HOSTNAME constant in the manifest
        text = text.replace("PLUGIN_HOSTNAME", f"https://{host}")
        return quart.Response(text, mimetype="text/json")


@app.get("/openapi.yaml")
async def openapi_spec():
    host = request.headers["Host"]
    with open("openapi.yaml") as f:
        text = f.read()
        # This is a trick we do to populate the PLUGIN_HOSTNAME constant in the OpenAPI spec
        text = text.replace("PLUGIN_HOSTNAME", f"https://{host}")
        return quart.Response(text, mimetype="text/yaml")


def main():
    app.run(debug=True, host="0.0.0.0", port=5002)


if __name__ == "__main__":
    main()
