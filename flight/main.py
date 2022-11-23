import os
from flight_db import FlightDB
from flask import Flask, jsonify
from flask import abort
from flask import make_response
from flask import request
from curses.ascii import NUL

port = os.environ.get('PORT')
if port is None:
    port = 8060

app = Flask(__name__)

@app.errorhandler(404)

def not_found(error):
    return make_response(jsonify({'error': 'Not found in flights'}), 404)

@app.route('/api/v1/test', methods=['GET'])
def get_test():
    return make_response(jsonify({'test': 'ok', 'port': port}), 200)



@app.route('/api/v1/flights', methods=['GET'])
def get_flights():
    page = request.args.get('page', default=0, type= int)
    size = request.args.get('size', default=0, type= int)
    db = FlightDB()
    items = db.get_flightss()
    result = {'page': page, 'pageSize': size, 'totalElements': len(items),  'items': items}
    return make_response(jsonify(result), 200)



@app.route('/api/v1/flights/exist', methods=['GET'])
def flight_exist():
    db = FlightsDB()
    args = request.data.decode()
    result = db.flight_exist(args)
    db.db_disconnect()
    if result is False:
        return Response(status=404)
    return result



if __name__ == '__main__':
    app.run(host="0.0.0.0", debug=True, port=int(port))