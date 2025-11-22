from src.fastapi_client_generator import FastapiClientGenerator

# api_client_generator = FastapiClientGenerator(
#     api_spec_url="https://beeceptor.com/docs/storefront-sample.json", client_name="example-package"
# ).generate()

api_client_generator = FastapiClientGenerator(
    api_spec_url="https://api.bol.com/retailer/public/apispec/Retailer%20API%20-%20v10",
    client_name="bol_com_package",
).generate()

# api_client_generator = FastapiClientGenerator(
#     api_spec_url="https://api.weather.gov/openapi.json",
#     client_name="weather",
# ).generate()
