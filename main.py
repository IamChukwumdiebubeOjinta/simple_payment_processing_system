import uvicorn
import logging
from fastapi import FastAPI
from routes import payment_route
from fastapi.openapi.utils import get_openapi

# from pydantic_extra_types import

app = FastAPI()
app.include_router(payment_route.router)


def custom_openapi():
    """
    Generates the OpenAPI schema for the Payment Processing API.

    Returns:
        dict: The OpenAPI schema.
    """
    if app.openapi_schema:
        return app.openapi_schema
        
    openapi_schema = get_openapi(
        title="Payment Processing API",
        version="2.5.0",
        summary="A system for handling payments info correctly",
        description="",
        routes=app.routes,
    )

    app.openapi_schema = openapi_schema
    return app.openapi_schema

custom_openapi()



if __name__ == '__main__':
    logging.basicConfig(level=logging.INFO)
    uvicorn.run("main:app", host="127.0.0.1", port=5000, reload=True)