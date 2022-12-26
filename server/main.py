from flask_cors import CORS
import os
import config
from flask import Flask, request
from warehouse.inventory import Inventory
from api.endpoints import Barcode
from robots.robot import Robot
import json


app = Flask(__name__)
cors = CORS(app)
# Load the inventory and layout from the database
inventory = Inventory()
companydb = Barcode()
robot = Robot()




@app.route("/add", methods=["POST"])
def handler_barcode():

    params = request.json
    items = companydb.get_data(params["barcode"])
    if items:
        value = inventory.insert(items[0], items[1], items[2],
                                 items[3], 0)
        # items = inventory.get_by_id([value])
        items = inventory.get_all()
        # print("items")
        handle_robot_pickup_box_inbound(params["barcode"])

        return {"status": "OK",
                "data": items
                }
    else:
        return {"status": "error", "error": "invalid_barcode"}


@app.route("/list/<command>", methods=["GET"])
def handler(command):
    # response.headers.add('Access-Control-Allow-Origin', '*')
    if command == "all":
        response = inventory.get_all()
        return response
    response = {"status": "error", "error": "invalid_command"}
    return response


@app.route("/count", methods=["GET"])
def handler_count():
    # response.headers.add('Access-Control-Allow-Origin', '*')

    # all= inventory.row_length()
    try:
        delivered = inventory.row_length_status(6)
        instorage = inventory.row_length_status(3)
    except:
        delivered=0
        instorage=0
    print(delivered)
    return {"delivered": delivered, "instorage": instorage, "status": "OK"}
    # response = {"status": "error", "error": "invalid_command"}
    # return response


@app.route("/feedback/<command>", methods=["POST"])
def handle_command(command):
    # Extract the command and parameters from the request
    # command = request.json["feedback"]
    params = request.json

    # Dispatch the command to the appropriate handler
    if command == "inbound":
        return handle_robot_pickup_box_inbound(params)
    elif command == "robotDeliveredIn":
        return handle_robot_delivered_in(params)
    elif command == "outbound":
        return handle_robot_pickup_box_outbound(params)
    elif command == "robotPickUp":
        return handle_robot_pick_up(params)
    elif command == "robotDeliveredOut":
        return handle_robot_delivered_out(params)
    else:
        return {"status": "error", "error": "invalid_command"}


def handle_robot_pickup_box_inbound(barcode):
    # id = params["id"]
    # barcode = inventory.get_barcode([id])[0]
    print(barcode)
    res = robot.call_robot([barcode], "sendInboundTask")
    res = res.json()
    if res["status"] == "ok":
        inventory.update_status_barcode(barcode, 1)
        return {"status": "OK",
                "reply": "Robot going",
                "state": 1}

    return {"status": "error", "error": "invalid_command"}


def handle_robot_delivered_in(params):
    barcode = params["barcode"]
    location = params["location"]

    try:
        inventory.update_location(location, barcode,3)
        return {"status": "OK",
                "state": 3}
    except:
        return {"status": "error", "error": "invalid_command"}


def handle_robot_pickup_box_outbound(params):
    id = params["id"]
    barcode = inventory.get_barcode([id])[0]
    res = robot.call_robot(barcode, "sendOutboundTask")
    res = res.json()
    if res["status"] == "ok":
        inventory.update_status( id, 4)
        return {"status": "OK",
                "reply": "Robot going",
                "state": 4}

    return {"status": "error", "error": "invalid_command"}


def handle_robot_pick_up(params):
    barcode = params["barcode"]
    items=inventory.get_by_barcode([barcode])
    print(items)
    if items[0][7] >=3:
    
        inventory.update_status_barcode(
             barcode, 5)
        return {"status": "OK", "state":"5"}
    elif items[0][7] >= 0:
        inventory.update_status_barcode(
             barcode,2)
        return {"status": "OK", "state": "2"}
    return {"status": "error", "error": "invalid_command"}


def handle_robot_delivered_out(params):
    barcode = params["barcode"]

    try:
        inventory.update_status_barcode(
            barcode,6)
        return {"status": "OK",
                "state": 6}
    except:
        return {"status": "error", "error": "invalid_command"}


if __name__ == "__main__":
    app.run()
