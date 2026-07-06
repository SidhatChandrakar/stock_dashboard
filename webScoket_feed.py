# Import necessary modules
import asyncio
import json
import ssl
import upstox_client
import websockets
from google.protobuf.json_format import MessageToDict
import requests

import MarketDataFeed_pb2 as pb
from values import *

def get_market_data_feed_authorize(api_version, configuration):
    """Get authorization for market data feed."""
    api_instance = upstox_client.WebsocketApi(
        upstox_client.ApiClient(configuration))
    api_response = api_instance.get_market_data_feed_authorize(api_version)
    return api_response


def decode_protobuf(buffer):
    """Decode protobuf message."""
    feed_response = pb.FeedResponse()
    feed_response.ParseFromString(buffer)
    return feed_response


async def fetch_market_data():
    """Fetch market data using WebSocket and print it."""

    # Create default SSL context
    ssl_context = ssl.create_default_context()
    ssl_context.check_hostname = False
    ssl_context.verify_mode = ssl.CERT_NONE

    # Configure OAuth2 access token for authorization
    configuration = upstox_client.Configuration()

    api_version = '2.0'
    configuration.access_token = accs_tkn

    # Get market data feed authorization
    response = get_market_data_feed_authorize(
        api_version, configuration)

    # Connect to the WebSocket with SSL context
    async with websockets.connect(response.data.authorized_redirect_uri, ssl=ssl_context) as websocket:
        print('Connection established')

        await asyncio.sleep(1)  # Wait for 1 second

        # Data to be sent over the WebSocket (DEFAULT DATA TO BE SENT)
        data = {
            "guid": "someguid",
            "method": "sub",
            "data": {
                "mode": "full",
                "instrumentKeys": ["NSE_INDEX|Nifty 50"]
            }
        }

        # # CODE FOR OPTION CHAIN
        # url = "https://api.upstox.com/v2/option/chain"
        # headers = {
        #     'Content-Type': 'application/json',
        #     'Accept': 'application/json',
        #     'Authorization': f'Bearer {accs_tkn}',  # Replace with your access token
        # }
        # params = {
        #     'instrument_key': 'NSE_INDEX|NIFTY 21800 PE',
        #     'expiry_date': '2024-03-28'  # Replace with the desired expiry date
        # }
        # response = requests.get(url, headers=headers, params=params)
        # if response.status_code == 200:
        #     data = json.loads(response.text)
        #     option_chain = data['data']
        #     # Extract instrument keys from the option chain data
        #     instrument_keys = [option['call_options']['instrument_key'] for option in option_chain]
        #     instrument_keys += [option['put_options']['instrument_key'] for option in option_chain]

        #     # Subscribe to instrument keys in the WebSocket feed
        #     for instrument_key in instrument_keys:
        #         data = {
        #             "guid": "someguid",
        #             "method": "sub",
        #             "data": {
        #                 "mode": "full",
        #                 "instrumentKeys": [instrument_key]
        #             }
        #         }

            # Convert data to binary and send over WebSocket
        binary_data = json.dumps(data).encode('utf-8')
        await websocket.send(binary_data)
        print("Subscription request sent!")
        # Continuously receive and decode data from WebSocket
        while True:
            message = await websocket.recv()
            decoded_data = decode_protobuf(message)
            # Convert the decoded data to a dictionary
            data_dict = MessageToDict(decoded_data)
            # Print the dictionary representation
            # print(json.dumps(data_dict))
            print(data_dict)
        else:
            print("Failed to fetch option chain data!")

# Execute the function to fetch market data
asyncio.run(fetch_market_data())