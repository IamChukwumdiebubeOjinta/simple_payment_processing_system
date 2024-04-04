import logging
from fastapi import FastAPI
from fastapi.openapi.utils import get_openapi

config = FastAPI()

# def get_openapi_schema(config):
#     if config.openapi_schema:
#         return config.openapi_schema
#     openapi_schema = get_openapi(
#         title="Payment Processing API",
#         version="2.5.0",
#         summary="A system for handling payments info correctly",
#         description="",
#         routes=app.routes,
        
#     )
#     config.openapi_schema = openapi_schema
#     return config.openapi_schema

# def set_openapi_schema(schema):
#     # Perform any necessary validations or transformations on the schema
#     config.openapi_schema = schema

# def custom_openapi(app):
#     try:
#         schema = get_openapi_schema(app)
#         set_openapi_schema(schema)
#         return config.openapi_schema
#     except Exception as e:
#         logging.error(f"Error in custom_openapi: {str(e)}")

def custom_openapi(app):
    if config.openapi_schema:
        return config.openapi_schema
    openapi_schema = get_openapi(
        title="Users Registration & Products API",
        version="2.5.0",
        summary="This is a simple user auth and product app",
        description="",
        routes=app.routes,
        
    )
    config.openapi_schema = openapi_schema
    return config.openapi_schema
