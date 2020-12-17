import json
from datetime import datetime

import requests


BASE_URL = "http://meteor.iung.pulawy.pl/data2.php"
STATIONS = {
    "pogorzelec": 214
}


def downloader(station: int):
    response = requests.get(BASE_URL, params={"s": station})
    if not response.ok:
        return False
    print("Response:", response.status_code, response.url)

    file_name = datetime.now().isoformat()
    with open(f"data/raw/{file_name}.txt", 'w') as f:
        print("File write raw:", f.name)
        f.write(response.text)

    return file_name


def text_processor(input_string: str) -> str:
    string_stream = input_string.replace("\n", "").split(" ")

    for i, string in enumerate(string_stream):
        if string[0].isalpha():
            json_string = f'"{string[:-1]}":'
            string_stream[i] = json_string

    output_string = " ".join(string_stream)
    return output_string


def parser(file_name):
    with open(f"data/raw/{file_name}.txt", 'r') as f:
        print("File open:", f.name)
        processed_text = text_processor(f.read())

        with open(f"data/json/{file_name}.json", 'w') as f:
            json_text = json.loads(processed_text)
            json.dump(json_text, f, sort_keys=True, indent=4)
            print("File dump:", f.name)


def get_meteo_json(station: int):
    file_name = downloader(station)

    if not file_name:
        print("Unable to download data")
        return None

    parser(file_name)


if __name__ == "__main__":
    station = STATIONS["pogorzelec"]

    get_meteo_json(station)
