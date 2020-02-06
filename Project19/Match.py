class Match:
    
    def __init__(self, home, away, home_goals, away_goals, b365, bw, iw, lb):
        self.home = home
        self.away = away
        res = home_goals - away_goals
        if res == 0:  # 0 for draw, 1 for home wins, 2 for away wins
            self.r = 0
        elif res > 0:
            self.r = 1
        else:
            self.r = 2
        self.b365 = b365
        self.bw = bw
        self.iw = iw
        self.lb = lb
  
    
