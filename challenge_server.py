import json

from flask import Flask
from flask import render_template
from flask import request
from flask_socketio import SocketIO
from flask_socketio import emit
from json2html import *

from logic import PayLoad

app = Flask(__name__)
# Allow anybody to connect
socketio = SocketIO(app, cors_allowed_origins='*')

app.config['DEBUG'] = True
app.config['SECRET_KEY'] = 'THISISMYSECRET'


@app.route('/productionplan', methods=['POST'])
def solve_payload():
    try:
        incoming_payload = json.loads(request.data)
        payload = PayLoad(incoming_payload)
        response = []

        if payload.feasible:

            sum_p = 0
            for pp in payload.powerplants:
                response.append({"name": pp["name"], "p": pp["p"]})
                sum_p += pp["p"]
            if sum_p != payload.load:
                response.append({"name": "SOLUTION", "p": "NOT FOUND"})
        else:
            response.append({"name": "SOLUTION Unfeasible", "p": payload.unfeasible_reason})

        monitoring_data = {"request": incoming_payload, "solution": response}

        monitoring_html = json2html.convert(json=monitoring_data,
                                            table_attributes="class=\"table table-bordered table-striped\"")

        # Emits the request ust processed:
        socketio.emit('request_processed', monitoring_html, namespace='/log', broadcast=True)

    except json.decoder.JSONDecodeError as e:
        # replace the body with JSON
        monitoring_data = json.dumps({
            "Bad Data": "JSON Decode Error",
            "Details": str(e),
            "IP Address": request.remote_addr})
        socketio.emit('request_processed', json2html.convert(json=monitoring_data), namespace='/log', broadcast=True)

    return json.dumps(response)


@app.route('/monitor', methods=['GET'])
def monitoring_page():
    """ Just display the monitoring page, the socket connection will update it... """
    return render_template("monitor.html")


@socketio.on('connect', namespace='/log')
def client_connect():
    """ Definion of a monitoring page connection to namespace log """
    # Emit a welcome message - will be the page title
    print('Got connection... ')
    emit('welcome', 'Powerplants Allocation Request Monitoring', namespace='/log')


if __name__ == '__main__':
    socketio.run(app, host='0.0.0.0', port=8888, debug=True)
