from flask import Flask, request, jsonify
from flask_cors import CORS
from main import interpretText
import json
app = Flask(__name__)
CORS(app)


@app.route('/interpret', methods=['POST'])
def interpret():
    data = request.get_json()
    value = data['params']['value']

    ts, console, exceptions, lexerErrors, gen = interpretText(value)

    ts = json.dumps(ts, default=lambda o: o.__dict__)
    ts = json.loads(ts)

    console = json.dumps(console, default=lambda o: o.__dict__)
    console = json.loads(console)

    exceptions = json.dumps(exceptions, default=lambda o: o.__dict__)
    exceptions = json.loads(exceptions)

    lexerErrors = json.dumps(lexerErrors, default=lambda o: o.__dict__)
    lexerErrors = json.loads(lexerErrors)

    return jsonify({
        'ts': ts['symbols'],
        'console': console,
        'exceptions': exceptions,
        'lexerErrors': lexerErrors,
        'gen': gen.get_final_code()
    })


if __name__ == '__main__':
    app.run(debug=True)