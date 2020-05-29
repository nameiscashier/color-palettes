import run
from flask import Flask, request, jsonify

app = Flask(__name__)
cache = set()


@app.route('/api/get_colors', methods=['POST'])
def get_colors():
    query = request.json['query']
    global cache
    colors, error = run.run(query, cache)
    print(colors)
    for url in colors:
        cache.add(url)
    return jsonify({"colors": colors, "error": error})
