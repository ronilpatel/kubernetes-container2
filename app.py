import json
import requests
from os import path

from flask import Flask, request


app = Flask(__name__)


def validate_file_contents(file_content):
    if file_content[0][0] != "product" or file_content[0][1] != "amount":
        raise


@app.route('/calculate_sum', methods=['POST'])
def calculate():
    payload = request.get_json()
    total = 0
    error_msg = ""

    try:
        file_obj = open("/home/" + payload.get("file"))
        # file_obj = open("/Ronil_PV_dir/" + payload.get("file"))
        data_content = [i.strip().split(",") for i in file_obj.readlines()]
        validate_file_contents(data_content)
        data_content = data_content[1:]

        for row in data_content:
            if row[0] == payload['product']:
                total += int(row[1])
    except:
        error_msg = "Input file not in CSV format."

    response = {
        "file": payload.get("file")
    }

    if error_msg:
        response["error"] = error_msg
    else:
        response["sum"] = total

    return json.loads(json.dumps(response))


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=9090)
