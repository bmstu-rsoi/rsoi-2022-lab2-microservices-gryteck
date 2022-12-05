import os
from flask import Flask, jsonify
from flask import abort
from flask import make_response
from flask import request
import requests
import datetime
import json
import uuid
from curses.ascii import NUL


app = Flask(__name__)

baseUrlPrivilege = 'http://10.5.0.4:8050'
baseUrlFlight = 'http://10.5.0.5:8060'
baseUrlTickets = 'http://10.5.0.6:8070' 

@app.route('/api/v1/test', methods=['GET'])
def get_test():
    return make_response(jsonify({'test': 'ok', 'port': port}), 200)



@app.errorhandler(404)
def not_found(error):
    return make_response(jsonify({'error': 'Not found in gateway'}), 404)



@app.route('/api/v1/flights', methods=['GET'])
def get_flights():
    page = request.args.get('page', default=0, type= int)
    size = request.args.get('size', default=0, type= int)
    response = requests.get('http://127.0.0.1:8060/api/v1/flights', params = {'page': page, 'size': size})
    return make_response(response.json(), 200)



@app.route('/api/v1/privilege', methods=['GET'])
def get_privilege():
    if 'X-User-Name' not in request.headers:
        abort(400)
    username = request.headers.get('X-User-Name')
    response = requests.get('http://privilege:8050/api/v1/privilege', params = {'username': username})
    return make_response(response.json(), 200)



@app.route('/api/v1/tickets', methods=['GET'])
def get_tickets():
    info_tickets = requests.get('http://127.0.0.1:8070/api/v1/tickets', headers=request.headers).json()

    for ticket in info_tickets:
        info_flights = requests.get('http://127.0.0.1:8060/api/v1/flights/exist', data=ticket['flight_number']).json()
        ticket['from_airport'] = info_flights['from_airport']
        ticket['to_airport'] = info_flights['to_airport']
        ticket['date'] = info_flights['date']
        ticket['price'] = info_flights['price']

    return info_tickets



@app.route('/api/v1/tickets/<string:ticket_uid>', methods=['GET'])
def get_ticket_by_uid(ticket_uid):
    info_tickets = requests.get('http://ticket:8070/api/v1/tickets/{ticket_uid}', headers=request.headers)
    if info_tickets.status_code != 200:
        return Response(status=404)
    info_tickets = info_tickets.json()
    info_flights = requests.get('http://flight:8060/api/v1/flights/exist', data=info_tickets['flight_)number']).json()

    response = dict()
    response['ticket_uid'] = ticket_uid
    response['flight_)number'] = info_tickets['flight_)number']
    response['from_airport'] = info_flights['from_airport']
    response['to_airport'] = info_flights['to_airport']
    response['date'] = info_flights['date']
    response['price'] = info_flights['price']
    response['status'] = info_tickets['status']

    return response



@app.route('/api/v1/tickets', methods=['POST'])
def buy_tickets():
    buy_info = request.json
    username = request.headers['X-User-Name']
    flight_exist = requests.get('http://flight:8060/api/v1/flights/exist', data=buy_info['flight_number']).json()
    if not flight_exist:
        return Response(status=404)
    data = {'username': username,
            'flight_number': flight_exist['flight_number'],
            'price': flight_exist['price'],
            'status': 'PAID'}
    ticket_uid = requests.post('http://ticket:8070/api/v1/tickets/buy', json=data)

    d = dict()
    d['ticket_uid'] = ticket_uid.text
    d['flight_number'] = flight_exist['flight_number']
    d['from_airport'] = flight_exist['from_airport']
    d['to_airport'] = flight_exist['to_airport']
    d['date'] = flight_exist['date']
    d['price'] = flight_exist['price']
    d['status'] = 'PAID'

    if buy_info['paidFromBalance']:
        data = {'username': username, 'ticket_uid': ticket_uid.text, 'price': int(flight_exist['price'])}
        paid_by_bonuses = int(requests.post('http://privilege:8050/api/v1/privilege/down', json=data).text)

        d['paidByMoney'] = data['price'] - paid_by_bonuses
        d['paidByBonuses'] = paid_by_bonuses
    else:
        data = {'username': username, 'ticket_uid': ticket_uid.text, 'price': int(flight_exist['price'])}
        requests.post('http://privilege:8050/api/v1/privilege/up', json=data)
        d['paidByMoney'] = flight_exist['price']
        d['paidByBonuses'] = 0
    privilege_info = requests.get('http://privilege:8050/api/v1/privilege', headers=request.headers).json()
    del privilege_info['history']
    d['privilege'] = privilege_info

    return response



@app.route('/api/v1/tickets/<string:ticket_uid>', methods=['DELETE'])
def return_ticket(ticket_uid):
    tickets_response = requests.delete('http://ticket:8070/api/v1/tickets/{ticket_uid}')
    if tickets_response.status_code != 204:
        return Response(status=404)

    privilege_response = requests.delete('http://privilege:8050/api/v1/privilege/{ticket_uid}', headers=request.headers)
    if privilege_response.status_code != 204:
        return Response(status=404)

    return Response(status=204)



@app.route('/api/v1/me', methods=['GET'])
def me():
    result = dict()
    result['tickets'] = get_tickets()
    result['privilege'] = get_privilege()
    del result['privilege']['history']
    return result



if __name__ == "__main__":
    port = int(os.environ.get("PORT", 8080))
    app.run(debug=True, port=port, host="0.0.0.0")