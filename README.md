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

<br>

![Image](https://raw.githubusercontent.com/ErikaMelt/network_coverage_api/assets/104458004/ac625135-715c-4e4c-add4-8e7210247429)

<br>

The image above represents the network coverage API.

### CSV Data
The network coverage data is provided in a CSV file. 
The CSV file contains the following features and conversion from Lambert93 to GPS coordinates is done. 



