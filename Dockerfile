# Build stage for dependencies
FROM python:3.9 as python-base
RUN mkdir -p /network_coverage_api
WORKDIR /network_coverage_api

# Copy the pyproject.toml and .env file
COPY pyproject.toml .
COPY .env .
COPY gunicorn_config.py .

# Copy the network_data_cleaned.csv file into the data folder
COPY network_coverage_api ./network_coverage_api
COPY tests ./tests

RUN pip3 install poetry python-dotenv gunicorn

RUN poetry config virtualenvs.create false
RUN poetry install

EXPOSE 3100

CMD ["gunicorn", "-k", "uvicorn.workers.UvicornWorker", "-c", "gunicorn_config.py", "network_coverage_api.app.main:app"]