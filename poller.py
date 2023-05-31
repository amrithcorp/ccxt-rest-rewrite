from common.prices import PriceService
from common.state_manager import StateManager
from time import sleep
from datetime import datetime

state_manager = StateManager()
state = state_manager.get_state()

price_service = PriceService(state_manager)
while(True):
    print(f"polling assets @ {datetime.utcnow().timestamp()}")
    for i in state['prices']:
        price_service.get_price(i)
    sleep(state['config']['poll_interval_seconds'])