import os
from ticket_db import TicketDB
from flask import Flask, jsonify
from flask import abort
from flask import make_response
from flask import request
from curses.ascii import NUL


app = Flask(__name__)

@app.errorhandler(404)
def not_found(error):
    return make_response(jsonify({'error': 'Not found in ticket'}), 404)



@app.route('/api/v1/test', methods=['GET'])
def get_test():
    return make_response(jsonify({'test': 'ok', 'port': port}), 200)



@app.route('/api/v1/tickets', methods=['GET'])
def get_tickets():
    page = request.args.get('page', default=0, type= int)
    size = request.args.get('size', default=0, type= int)
    db = TicketDB()
    items = db.get_tickets()
    result = {'page': page, 'pageSize': size, 'totalElements': len(items),  'items': items}
    return make_response(jsonify(result), 200)



@app.route('/api/v1/tickets/<string:ticket_uid>', methods=['GET'])
def get_ticket_by_uid(ticket_uid):
    username = request.headers['X-User-Name']
    db = TicketDB()
    result = db.get_ticket_by_uid(ticket_uid, username)
    db.db_disconnect()
    if not result:
        return make_response(jsonify({'error': 'Not found in ticket'}), 404)
    return result



@app.route('/api/v1/tickets/buy', methods=['POST'])
def buy_ticket():

    db = TicketDB()
    tickets = db.get_tickets()
    if not request.json:
        return Response(status=404)
    new_ticket = {
        'ticket_uid': request.json['ticket_uid'],
        'username': request.json['username'],
        'flight_number': request.json['flight_number'],
        'price': request.json['price'],
        'status': request.json['status']
    }
    db.buy_ticket(new_ticket)
    return make_response(jsonify(new_ticket[0]), 200)



@app.route('/api/v1/tickets/<string:ticket_uid>', methods=['DELETE'])
def return_ticket():
    db = TicketDB()
    ticket_uid = request.form['ticket_uid']
    result = db.return_ticket(ticket_uid)
    if result != '':
        return make_response(jsonify({'ticket_uid': ticket_uid}), 201)
    else:
        return make_response(jsonify({}), 400)



if __name__ == "__main__":
    port = int(os.environ.get("PORT", 8070))
    app.run(debug=True, port=port, host="0.0.0.0")