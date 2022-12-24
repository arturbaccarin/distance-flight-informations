import flight_data as fd

if __name__ == "__main__":
    cities = fd.get_search_data()
    req = fd.request_flight_data(cities)
    dt_flgt = fd.parse_fligth_data(req)
    fd.save_csv_file(dt_flgt)
    print(dt_flgt)
