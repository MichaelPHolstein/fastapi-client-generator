from src.fastapi_client_generator import FastapiClientGenerator

# api_client_generator = FastapiClientGenerator(
#     api_spec_url="https://beeceptor.com/docs/storefront-sample.json", client_name="example-package"
# ).generate()

api_client_generator = FastapiClientGenerator(
    client_name="bol_com_package",
).from_file_path("assets/openapi-mock.json")

# api_client_generator = FastapiClientGenerator(
#     api_spec_url="https://api.weather.gov/openapi.json",
#     client_name="weather",
# ).generate()
