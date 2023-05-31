import json

class StateManager:

    file_path = None

    def __init__(self,file_path = "state.json"):
        self.file_path = file_path
        
    def get_state(self) -> dict:
        with open(self.file_path) as state_file:
            state =  json.load(state_file)
            state_file.close()
            return state 
        
    def write_state(self, new_state) -> None:
        with open(self.file_path, "w") as state_file:
            json.dump(new_state, state_file, indent=4)
