class GameState:
    
    def __init__(self):
        self.players = []  
        self.board = []   
        self.pot = 0
        self.max_bet = 0
        self.active_player_index = 0
        self.phase = 'shuffle'  
        self.deck = []
        
    def to_dict(self):
        return {
            'players': self.players,
            'board': self.board,
            'pot': self.pot,
            'max_bet': self.max_bet,
            'active_player_index': self.active_player_index,
            'phase': self.phase
        }
    
    @staticmethod
    def from_dict(data):
        """Recréer depuis un dict"""
        state = GameState()
        state.players = data['players']
        state.board = data['board']
        state.pot = data['pot']
        state.max_bet = data['max_bet']
        state.active_player_index = data['active_player_index']
        state.phase = data['phase']
        return state