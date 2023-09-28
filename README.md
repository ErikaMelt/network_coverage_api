# Network Coverage API

The Network Coverage API is built using FastAPI and Poetry for dependency management. This API retrieves coordinates from an external address API, matches the coordinates with network coverage data stored in a CSV file, and provides coverage information for the nearest points.

## Features

- Fetch coordinates (longitude and latitude) from [External API](https://adresse.data.gouv.fr/api-doc/adresse) ```curl "https://api-adresse.data.gouv.fr/search/?q=8+bd+du+port"```
- Match coordinates with network coverage data within a specified tolerance.
- Select the N closest points to a target longitude and latitude.
- Generate a response containing network coverage data for matched points.
- Use a CSV file with the network coverage. 

## Getting Started

To get started with this API, follow these steps:

### Prerequisites

- Python 3.7+
- Poetry
- FastApi
- Pytest 

### Installation

1. Clone this repository:
   ```bash
   git clone https://github.com/ErikaMelt/network_coverage_api.git

Navigate to the project directory:
```cd network-coverage-api```

Install the project dependencies using Poetry:
```poetry install```

### Usage
Run the FastAPI application:
poetry run uvicorn app.main:app --reload
```Access the API at http://localhost:8000/docs```

### Endpoints
/network-coverage/: Retrieve network coverage data for a given address

<img src="https://github.com/ErikaMelt/network_coverage_api/assets/104458004/dff06dca-ffc6-42b4-a1cc-01c9e87120a1" alt="Network Coverage API" width="400" align="left">

The image above represents the network coverage API.

### CSV Data
- The network coverage data is provided in a CSV file. 
- The CSV file contains the following features and conversion from Lambert93 to GPS coordinates. 

<img src="https://github.com/ErikaMelt/network_coverage_api/assets/104458004/f0734032-15cc-4c1e-88d2-b0692a4fe407" alt="CSV Data" width="400" align="left">


- **Data Example**
<img src="https://github.com/ErikaMelt/network_coverage_api/assets/104458004/682409b8-e96d-4f36-b82f-2f2dadd9ebee" alt="CSV Data Example" width="400" align="left">

### Testing
To run the tests for this API, follow these steps:

1. Make sure you have installed the project dependencies using Poetry (as mentioned in the Installation section).
2. Open a terminal and navigate to the project directory.
3. Run the following command to execute the tests:
   ```bash
   poetry run python tests

The 9 tests should pass as shown in the image: 
<br>

![image](https://github.com/ErikaMelt/network_coverage_api/assets/104458004/d8b2ef32-0b5d-47c2-9c08-d55f85ef5a28)

