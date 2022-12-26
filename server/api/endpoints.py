# Class for updating database from remote server

import pyodbc


class Barcode:
    def __init__(self):

        # self.conn = pyodbc.connect('Driver={SQL Server};'
        #                       'Server=vps.airlab.id,49156;'
        #                       'Database=stock_data;'
        #                       'Username = superadmin;'
        #                       'Password = Changeyourpwd36689.;'
        #                            'Trusted_Connection=yes;')
        self.conn = pyodbc.connect('Driver={SQL Server};'
                                   'Server=DESKTOP-C0N77N0\TEW_SQLEXPRESS;'
                                   'Database=stock_data2;'
                                   'Trusted_Connection=yes;')
        self.cursor = self.conn.cursor()


    def get_data(self, barcode):
        # cursor = self.conn.cursor()
        self.cursor.execute("""
            SELECT * FROM barcode_detail WHERE barcode = ?
        """, (barcode))

        items = self.cursor.fetchone()
        return items


# # # # Some other example server values are
# # # # server = 'localhost\sqlexpress' # for a named instance
# # # # server = 'myserver,port' # to specify an alternate port
# # # server = 'tcp:myserver.database.windows.net'
# # # database = 'mydb'
# # # username = 'myusername'
# # # password = 'mypassword'
# # # # ENCRYPT defaults to yes starting in ODBC Driver 18. It's good to always specify ENCRYPT=yes on the client side to avoid MITM attacks.
# # # cnxn = pyodbc.connect('DRIVER={ODBC Driver 18 for SQL Server};SERVER='+server +
# # #                       ';DATABASE='+database+';ENCRYPT=yes;UID='+username+';PWD=' + password)
# # # cursor = cnxn.cursor()


# # # # Connect to the database
# mydb = mysql.connector.connect(
#     host='vps.airlab.id',
#     user='superadmin',
#     password='changeyourpwd36689.',
#     port=49228,
#     database='stock_data'
# )
# # # cursor = mydb.cursor()

# # # # Execute a SELECT query
# # # cursor.execute("SELECT * FROM barcode_detail")
# # # # Fetch the results
# # # results = cursor.fetchall()

# # # # Process the results
# # # print(results)

# # # # Close the connection
# # # mydb.close()

# import pymssql

# conn = pymssql.connect(
#     host=r'vps.airlab.id:49228',
#     user=r'superadmin',
#     password=r'changeyourpwd36689.',
#     database='stock_data'
# )
# cursor = conn.cursor(as_dict=True)
# cursor.execute(
#     'Select top 4 barcode from barcode_detail ')
# data = cursor.fetchall()


# cursor.close()

# conn = pymssql.connect("vps.airlab.id:49227", "superadmin",
    #    "changeyourpwd36689", "stock_data")
# cursor = conn.cursor()
# cursor.execute('SELECT * FROM barcode_detail')

# # # print(cursor.fetchall())
# # # conn.close()

# server = 'vps.airlab.id,49227'
# database = 'stock_data'
# username = 'superadmin'
# password = 'changeyourpwd36689.'

# # conn = pyodbc.connect('?sted_Connection=yes;")
# cursor = conn.cursor()
# cursor.execute('SELECT * FROM barcode_detail')

# print(cursor.fetchall())
# conn.close()


# import os

# from flask import Blueprint, jsonify, request

# from warehouse import Inventory, Layout
# from robots import Robot

# api = Blueprint("api", __name__)

# # Initialize the warehouse and robots
# inventory = Inventory()
# layout = Layout()
# robots = {}
# for id in os.environ["ROBOT_IDS"]:
#     host = os.environ[f"ROBOT_{id}_HOST"]
#     port = os.environ[f"ROBOT_{id}_PORT"]
#     robots[id] = Robot(id, host, port)


# @api.route("/robots/<robot_id>/command", methods=["POST"])
# def send_command(robot_id):
#     # Extract the command and parameters from the request
#     command = request.json["command"]
#     params = request.json.get("params", {})

#     # Send the command to the specified robot
#     response = robots[robot_id].send_command(command, **params)
#     return jsonify(response)


# @api.route("/robots/<robot_id>/status", methods=["GET"])
# def get_status(robot_id):
#     # Retrieve the status of the specified robot
#     status = robots[robot_id].get_status()
#     return jsonify(status)


# @api.route("/warehouse/inventory", methods=["POST"])
# def update_inventory():
#     # Extract the location and item from the request
#     location = request.json["location"]
#     item = request.json["item"]
