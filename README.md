# Distance Flight Informations

> Receive information about distance between two airports from their names through requests.

### Requirements
- Python 3.9+
- Docker

### Setup
1. Install requirements: `pip install -r requirements.txt`;
2. Enter in *mock_website* folder;
3. Create the docker image: `docker build --tag mock-flask .`;
4. Build and run the container: `docker run --name mock-cntnr -d -p 5000:5000 mock-flask`.

### Observations
- Docker is used to run a mock website used in tests.

### What is used in this project
- Python: requests, beautifulsoup, pytest;
- Regex;
- CSV;
- Docker.

### Future Improvements
- Add input in airport names;
- Get more information about the airports.

