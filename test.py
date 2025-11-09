from src.fastapi_client_generator import FastapiClientGenerator
# from bol_com_package import Client

api_client_generator = FastapiClientGenerator(
    api_spec_url="https://beeceptor.com/docs/storefront-sample.json", client_name="example-package"
).generate()

api_client_generator = FastapiClientGenerator(
    api_spec_url="https://api.bol.com/retailer/public/apispec/Retailer%20API%20-%20v10",
    client_name="bol_com_package",
).generate()


# bol_client = Client()


# bol_client.retailer_shipping_labels.
