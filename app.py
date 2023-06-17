import json
import requests
from os import path
import logging

from flask import Flask, request


app = Flask(__name__)


def validate_file_contents(file_content):
    if file_content[0][0] != "product" or file_content[0][1] != "amount":
        return True


@app.route('/calculate_sum', methods=['POST'])
def calculate():
    payload = request.get_json()
    total = 0
    error_msg = ""

    file_lines = []

    try:
        with open("/Ronil_PV_dir/" + payload.get("file"), "r") as file_obj:
            file_lines = file_obj.readlines()
            logging.error(file_lines)
            print(f"Read lines are: {file_lines}")
    except:
        return json.loads(json.dumps({
            "file": payload.get("file"),
            "error": "Input file not able to read."
        }))

    try:
        # file_obj = open("/Ronil_PV_dir/" + payload.get("file"))
        data_content = [i.replace(" ", "").strip().split(",") for i in file_lines]
        print(f"Data contents are: {data_content}")
        logging.error(data_content)
        result = validate_file_contents(data_content)
        logging.error(f"The result of validation is: {result}")
        if not result:
            raise

        data_content = data_content[1:]
        logging.error(f'data content is: {data_content}')

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
