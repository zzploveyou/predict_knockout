# coding:utf-8

from collections import defaultdict
from copy import deepcopy

WIN_SCORE = 1
LOSS_SCORE = 0
TIE_SCORE = 0

class Team:

    def __init__(self, name, score):
        self.name = name
        self.score = score

    def win(self):
        global WIN_SCORE
        self.score += WIN_SCORE

    def loss(self):
        global LOSS_SCORE
        self.score += LOSS_SCORE
    
    def tie(self):
        global TIE_SCORE
        self.score += TIE_SCORE
    def __str__(self):
        return "{}: {}".format(self.name, self.score)


class Match:
    def __init__(self, names, scores):
        self.teams = []
        for name, score in zip(names, scores):
            self.teams.append(Team(name, score))
    def getind(self, name):
        for idx, team in enumerate(self.teams):
            if name == team.name:
                return idx
    def one_defeat(self, name1, name2):
        self.teams[self.getind(name1)].win()
        self.teams[self.getind(name2)].loss()
    def one_tie(self, name1, name2):
        self.teams[self.getind(name1)].tie()
        self.teams[self.getind(name1)].tie()
    def pairs(self):
        names, scores = [], []
        for team in self.teams:
            names.append(team.name)
            scores.append(team.score)
        return names, scores
    def __str__(self):
        self.teams.sort(key=lambda team:team.score, reverse=True)
        res = ""
        for team in self.teams:
            res += "{}: {}\t".format(team.name, team.score)
        res += "\n"
        return res
    def top(self, n=2):
        self.teams.sort(key=lambda team:team.score, reverse=True)
        res = []
        for i in range(n):
            res.append(self.teams[i].name)
        for i in range(n, len(self.teams)):
            # 与第二名同积分
            if self.teams[i].score == self.teams[n-1].score:
                res.append(self.teams[i].name)
        return res

def com(names):
    # 产生比赛对.
    from itertools import combinations
    # return combinations(names, 2)
    coms = [('SKT', 'C9'), 
        ('SKT', 'AHQ'), 
        ('SKT', 'EDG'), 
        ('C9', 'AHQ'), 
        ('C9', 'EDG'), 
        ('AHQ', 'EDG')]
    return coms

def predict(names, scores, coms, predict_team, n=2):
    match = Match(names, scores)
    matchs = defaultdict(lambda : [])
    matchs[match] = []
    for name1, name2 in coms:
        now_matchs = deepcopy(matchs.keys())
        for m in matchs.keys():
            tmp = deepcopy(m)
            m.one_defeat(name1, name2)
            tmp.one_defeat(name2, name1)
            matchs[tmp] = deepcopy(matchs[m])
            matchs[m].append("{} > {}".format(name1, name2))
            matchs[tmp].append("{} > {}".format(name2, name1))
    idx = 1
    for m, winteams in matchs.items():
        # 预测某队在所有比赛结束后积分居前n名的可能性
        if predict_team in m.top(n):
            print "可能性: {}".format(idx)
            idx += 1
            print m
            for wt in winteams:
                print wt
            print
def main():
    # 对名
    names = ["SKT", "C9", "AHQ", "EDG"]
    # 目前积分
    scores = [3, 2, 1, 0]
    coms = com(names)
    predict_team = "EDG"
    n = 2
    predict(names, scores, coms, predict_team, n=2)

if __name__ == '__main__':
    main()
