import requests
from config import HOST, ROBOT_PORT

class Robot:
    def call_robot(self, barcode, command):
        # Set the API endpoint URL
        # command can be sendInboundTask or sendOutboundTask
        url = "http://"+HOST+":"+ROBOT_PORT+"/robot/"+command
        # Set the API request headers
        headers = {"Content-Type": "application/json"}
        # Set the API request payload (data to be sent to the API)
        payload = {"barcode": barcode}
        # Send a POST request to the API
        response = requests.post(url, headers=headers, json=payload)

        return response
        # # Print the API response status code
        # print(response.status_code)

        # # Print the API response content
        # print(response.content)
