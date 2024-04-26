class TDGame:
    def __int__(self, player_1, player_2):
        self.current_player = 0  # 0: player_1, 1: player_2
        self.playersType = [player_1, player_2]  # human(H), minimax(M), alpha-beta(AB), random(R)
        self.evaluation = 0
