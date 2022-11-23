import os
from privilege_db import PrivilegeDB
from flask import Flask, jsonify
from flask import abort
from flask import make_response
from flask import request
from curses.ascii import NUL

port = os.environ.get('PORT')
if port is None:
    port = 8050

app = Flask(__name__)

@app.errorhandler(404)
def not_found(error):
    return make_response(jsonify({'error': 'Not found in privilege'}), 404)



@app.route('/api/v1/test', methods=['GET'])
def get_test():
    return make_response(jsonify({'test': 'ok', 'port': port}), 200)



@app.route('/api/v1/privilege', methods=['GET'])
def get_privilege():
    db = PrivilegesDB()
    args = request.headers['X-User-Name']
    result = db.get_privilege(args)
    db.db_disconnect()
    if result is None:
        return Response(status=404)
    return result



@app.route('/api/v1/privilege/down', methods=['POST'])
def privilege_down():
    db = PrivilegesDB()
    args = request.json
    result = db.privilege_down(args)
    db.db_disconnect()
    return result



@app.route('/api/v1/privilege/up', methods=['POST'])
def privilege_up():
    db = PrivilegesDB()
    args = request.json
    db.privilege_up(args)
    db.db_disconnect()
    return Response(status=200)



@app.route('/api/v1/privilege/<string:ticket_uid>', methods=['DELETE'])
def privilege_return(ticket_uid):
    db = PrivilegesDB()
    username = request.headers['X-User-Name']
    db.privilege_return(ticketUid, username)
    db.db_disconnect()

    return Response(status=204)



if __name__ == '__main__':
    app.run(host="0.0.0.0", debug=True, port=int(port))