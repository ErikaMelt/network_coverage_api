from fastapi import FastAPI

from network_coverage_api.app import routes

app = FastAPI()
app.include_router(routes.router)
