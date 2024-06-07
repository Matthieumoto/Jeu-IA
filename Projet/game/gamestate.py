class GameState:
    #C'est une pile en gros
    def __init__(self,states : dict) -> None:
        self.states = states
        self.current_state = []
    
    def modify_state(self,key : str):
        self.current_state.append(key)

    def lower_state(self):
        self.current_state.pop()

    def run(self):
        self.states[self.current_state[-1]]()

    
    
