from fastapi_client_generator import FastapiClientGenerator

from tests.fastapi_instance import fastapi_instance

FastapiClientGenerator(client_name="the-notorious-big").from_fastapi(fastapi_instance)
