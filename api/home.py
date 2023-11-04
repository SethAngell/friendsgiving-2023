from flask import Flask, jsonify, request, make_response, redirect
from menu import get_menu, add_all_items_to_menu
from guests import get_guest_list, add_guest_to_guest_list
import json
from flask_cors import CORS
import os


app = Flask(__name__)
app.config["CORS_HEADERS"] = "Content-Type"
CORS(app, resources={r"/api/*": {"origins": "*"}})


@app.route("/")
def hello_world():
    return "<p>Hello, World!</p>"


@app.route("/api/menu", methods=["GET", "POST"])
def menu():
    if request.method == "GET":
        menu = get_menu()
        response = make_response(menu.serialize())
        response.headers["Content-Type"] = "application/json"
        response.headers.add("Access-Control-Allow-Origin", "*")
        return response
    else:
        print(request.form)
        add_guest_to_guest_list(request.form)
        add_all_items_to_menu(request.form)
        redirect_url = '///Users/sethangell/Developer/friendsgiving/frontend/index.html' if app.debug else 'https://friendsgiving.doublel.studio'
        return redirect(redirect_url, code=302)

@app.route("/api/guests", methods=["GET", "POST"])
def guests():
    if request.method == "GET":
        guest_list = get_guest_list()
        response = make_response(guest_list.serialize())
        response.headers["Content-Type"] = "application/json"
        return response
    else:
        add_guest_to_guest_list(request.form)


if __name__ == "__main__":
    debug = bool(os.getenv('PRODUCTION', False)) == False
    print(debug)
    app.run(host="0.0.0.0", port=8012, debug=debug)
