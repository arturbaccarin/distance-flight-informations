from os.path import exists
from os import remove
import requests
import pytest
import csv
from main import (
    request_flight_data,
    request_airport_iata_code,
    parse_airport_iata_code,
    parse_fligth_data,
    save_csv_file,
    get_search_data,
)


def test_should_return_200_when_request_aiport_iata_code():
    response = request_airport_iata_code("São Paulo")
    assert response.status_code == 200


def test_should_return_none_when_airport_not_find_in_get_airport():
    response = requests.get("http://127.0.0.1:5000/not_find_airport")
    assert not parse_airport_iata_code(response)


def test_should_return_a_string_when_airport_is_find_in_get_aiport():
    response = requests.get("http://127.0.0.1:5000/find_airport")
    assert len(parse_airport_iata_code(response)) == 3
    assert isinstance(parse_airport_iata_code(response), str)


def test_should_return_200_when_both_airports_are_correct():
    response = request_flight_data(("BSB", "GRU"))
    assert response.status_code == 200


def test_should_raise_error_when_some_airport_is_wrong():
    with pytest.raises(Exception) as e_info:
        request_flight_data(("123", "GRU"))
    assert e_info.value.args[0] == "Bad request"


def test_should_return_a_dict_with_flight_data():
    response = requests.get("http://127.0.0.1:5000/correct_airports")
    flight_data = parse_fligth_data(response)
    assert isinstance(flight_data, dict)
    assert len(flight_data.keys()) == 5
    assert (
        flight_data["title"]
        == "Distance From Brasilia International Airport to Afonso Pena Airport (BSB - CWB Distance)"
    )
    assert flight_data["flight_time"] == "1 hours 20 minutes"
    assert flight_data["distance_km"] == "1082 kilometers"
    assert (
        flight_data["gps_coordinates_from"]
        == "Latitude: S 15° 52' 9'' Longitude: W 47° 55' 15''"
    )
    assert (
        flight_data["gps_coordinates_to"]
        == "Latitude: S 25° 31' 42.6'' Longitude: W 49° 10' 32.9''"
    )


def test_should_save_a_csv_file():
    save_csv_file({"a": 1, "b": 2, "c": 3})
    assert exists("flight_data.csv")
    with open("flight_data.csv", "r", encoding="utf8") as csv_file:
        csv_reader = csv.reader(csv_file)
        csv_data = list(csv_reader)
    assert csv_data[0] == ["a", "b", "c"]
    assert csv_data[-1] == ["1", "2", "3"]
    remove("flight_data.csv")


def test_should_return_a_tuple_with_iata_codes():
    search_data = get_search_data()
    assert search_data == ("BSB", "CWB")


# integration test
# request + parse
def test_should_return_200_and_get_iata_code_when_airport_is_correct():
    response = request_airport_iata_code("Brasília")
    assert response.status_code == 200
    iata_code = parse_airport_iata_code(response)
    assert iata_code == "BSB"


def test_should_return_200_and_get_data_flight_when_both_airports_are_correct():
    response = request_flight_data(("BSB", "SDU"))
    assert response.status_code == 200
    flight_data = parse_fligth_data(response)
    assert isinstance(flight_data, dict)
