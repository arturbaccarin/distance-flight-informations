import re
import csv
import requests
from bs4 import BeautifulSoup
from requests import Response


def parse_fligth_data(flight_data_response: Response) -> dict[str, str]:
    """Parse a HTML to get flight data.

    Args:
        flight_data_response (Response): reponse to get raw data

    Returns:
        dict[str, str]: flight informations
    """
    pattern = re.compile("\d{1,2} hours \d{1,2} minutes")
    flight_time = pattern.findall(flight_data_response.text)[0]

    pattern = re.compile("\d+ kilometers")
    distance_km = pattern.findall(flight_data_response.text)[0]

    soup = BeautifulSoup(flight_data_response.text, "html.parser")
    airportboxes = soup("table", class_="airportbox")
    title = soup.find("div", class_="artical-content").find("h1").text

    pattern = re.compile("L.+?<")
    gps_coordinates_from = pattern.findall(str(airportboxes[0]))[0][:-1]
    gps_coordinates_to = pattern.findall(str(airportboxes[1]))[0][:-1]
    return {
        "title": title,
        "flight_time": flight_time,
        "distance_km": distance_km,
        "gps_coordinates_from": gps_coordinates_from,
        "gps_coordinates_to": gps_coordinates_to,
    }


def request_flight_data(flight_search_data: tuple[str]) -> Response:
    """Request website to get information aboute flight distance.

    Args:
        flight_search_data (tuple[str]): a tuple with two airports (IATA Code)

    Raises:
        Exception: some airport is not find

    Returns:
        Response: raw data to be parsed
    """
    iata_from = flight_search_data[0]
    iata_to = flight_search_data[1]
    response = requests.get(
        f"https://www.airportdistancecalculator.com/flight-{iata_from}-to-{iata_to}.html"
    )
    if response.status_code == 200:
        return response
    else:
        raise Exception("Bad request")


def get_search_data() -> tuple[str]:
    """Get the IATA codes from airport name or city.

    Returns:
        tuple[str]: a tuple with two airports (IATA Code)
    """
    from_city = "Brasília"
    iata_from_city = parse_airport_iata_code(request_airport_iata_code(from_city))
    to_city = "Curitiba"
    iata_to_city = parse_airport_iata_code(request_airport_iata_code(to_city))

    return (iata_from_city, iata_to_city)


def parse_airport_iata_code(airport_response: Response) -> str:
    """Parse a HTML to get IATA code.

    Args:
        airport_response (Response): raw data to be parsed

    Returns:
        str: IATA Code
    """
    soup = BeautifulSoup(airport_response.text, "html.parser")
    airport_datatable = soup.find("table", class_="datatable")
    if airport_datatable:
        airport_datatable_row = soup.find("table", class_="datatable")("tr")
        iata_airport_code = airport_datatable_row[-1]("td")[-1].text
        return iata_airport_code
    return


def request_airport_iata_code(airport: str) -> Response:
    """Request website with airport name or city to get IATA Code.

    Args:
        airport (str): airport city or airport name

    Returns:
        Response: raw data to be parsed
    """
    url_request = "https://www.iata.org/en/publications/directories/code-search/"
    params = {
        "airport.search": airport,
    }
    return requests.get(url_request, params=params)


def save_csv_file(data_to_save: dict[str, str]) -> None:
    """Save data in a csv file

    Args:
        data_to_save (dict[str, str]): data to be saved
    """
    with open("flight_data.csv", "w", encoding="utf8", newline="") as csv_file:
        fieldnames = data_to_save.keys()
        csv_writer = csv.DictWriter(csv_file, fieldnames=fieldnames)
        csv_writer.writeheader()
        csv_writer.writerow(data_to_save)
