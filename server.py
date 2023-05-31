from flask import Flask, Response
from common.state_manager import StateManager

app = Flask(__name__)

file_path = "state.json"

state_manager = StateManager(file_path)

@app.route('/<asset_pair>')
def show_price(asset_pair):
    current_state = state_manager.get_state()
    
    if asset_pair not in current_state['prices']:
        return "no_such_asset_pair", 400
    
    asset_info = current_state['prices'][asset_pair]
    return {
        "symbol" : asset_pair,
        "percent_change" : asset_info['percent_change'],
        "price" : asset_info['price'],
        "timestamp" : asset_info['time_stamp']
    }

if __name__ == "__main__":
    app.run(debug=True)
