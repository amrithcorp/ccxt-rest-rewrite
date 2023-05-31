from common.state_manager import StateManager
import random
from stellar_sdk import (
    Server,
    Asset
)
import ccxt
from datetime import datetime
class PriceService:
    state_manager = None
    
    def __init__(self, state_manager : StateManager):
        self.state_manager = state_manager
        initial_state = self.state_manager.get_state()
        self.horizon_server = Server(initial_state['config']['horizon_url'])
        self.binance_client = ccxt.binanceus()

    def get_price(self, asset_pair) -> None:
        state = self.state_manager.get_state()
        if asset_pair not in state['prices']:
            return KeyError
        price_info = {}
        if state['price_specific_config'][asset_pair]['mode'] == "ccxt":
            price_info = self.get_ccxt_price(asset_pair, state)
        if state['price_specific_config'][asset_pair]['mode']== "sdex":
            price_info = self.get_sdex_price(asset_pair, state)
        state['prices'][asset_pair] = price_info
        self.state_manager.write_state(state)

    def get_ccxt_price(self, asset_pair, state) -> dict:
        asset_name = asset_pair.split('-')[0] + '/'  + asset_pair.split('-')[1]
        ohlcv = self.binance_client.fetch_ohlcv(asset_name, '1m', limit=1)[0]
        return {
            "percent_change" : 100*((ohlcv[1]-ohlcv[4])/ohlcv[4]),
            "time_stamp" : ohlcv[0],
            "price" : ohlcv[1],
            "previous_price" : ohlcv[4]
        }

    def get_sdex_price(self, asset_pair, state) -> dict:
        search_paths = self.horizon_server.strict_receive_paths(
            source = [Asset(
            state['price_specific_config'][asset_pair]['asset'].split(':')[0],
            state['price_specific_config'][asset_pair]['asset'].split(':')[1]
            )],
            destination_asset=Asset(
                state['config']['sdex_stable_asset'].split(':')[0],
                state['config']['sdex_stable_asset'].split(':')[1],                
            ),
            destination_amount=str(state['config']['stable_asset_amount'])
        ).call()
        percent_change = 0
        time_stamp = int(datetime.utcnow().timestamp())
        price = 0
        previous_price = 0

        if len(search_paths['_embedded']['records']) > 0 : 
            chosen_path = search_paths['_embedded']['records'][0]
            price = round(float(chosen_path['destination_amount']) / float(chosen_path['source_amount']),7)
            previous_price = state['prices'][asset_pair]['price']
            percent_change = ((price-previous_price)/previous_price)*100
        return {
            "percent_change" : percent_change,
            "time_stamp" : time_stamp,
            "price" : price,
            "previous_price" : previous_price
        }