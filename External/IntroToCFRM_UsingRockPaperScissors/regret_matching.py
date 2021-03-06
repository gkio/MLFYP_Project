from __future__ import division
from random import random
import numpy as np
import pandas as pd
import os


'''
    Use regret-matching algorithm to play Scissors-Rock-Paper.
'''

class RPS:
    actions = ['ROCK', 'PAPER', 'SCISSORS']
    n_actions = 3
    utilities = pd.DataFrame([
        # ROCK  PAPER  SCISSORS
        [ 0,    -1,    1], # ROCK
        [ 1,     0,   -1], # PAPER
        [-1,     1,    0]  # SCISSORS
    ], columns=actions, index=actions)


class Player:
    def __init__(self, name):
        self.strategy, self.avg_strategy,\
        self.strategy_sum, self.regret_sum = np.zeros((4, RPS.n_actions))
        self.name = name

    def __repr__(self):
        return self.name

    def update_strategy(self, i, which_player_forprint):
        """
        set the preference (strategy) of choosing an action to be proportional to positive regrets
        e.g, a strategy that prefers PAPER can be [0.2, 0.6, 0.2]
        """
        self.strategy = np.copy(self.regret_sum)
        self.strategy[self.strategy < 0] = 0  # reset negative regrets to zero

        # Q: Why set negative regrets to zero?
        # A: The strategy performance history is being tracked by strategy_sum.
        # 'Strategy' has it's negative regrets set to zero because it needs to
        # evaluate new hand.


        summation = sum(self.strategy)
        # Q: But then why is sum of 'Strategy' being calculated if it doesn't
        # consider negative regrets?
        # A: Probably because you can't normalise with a array that has negative numbers
        # Better Answer: It would make sense to think that a more negative value would
        # correspond to a bad action to take and so it would seem to be clever to not
        # play that option. For sake of simplictly, we only consider positive values
        # (Not dividing by zero etc)



        if summation > 0:
            # normalise
            self.strategy /= summation
        else:
            # uniform distribution to reduce exploitability
            self.strategy = np.repeat(1 / RPS.n_actions, RPS.n_actions)

        self.strategy_sum += self.strategy

   

        f = open('strategy_stats_RPS.txt','a+')
        if which_player_forprint == "p1":
            f.write("\nGAME_NUMBER: " + str(i) +"\n\t" + "\nPlayer_no: " + which_player_forprint + "\n\tself.self_strategy: " + str(self.strategy) +"\n\t" + "self.strategy_sum: " + str(self.strategy_sum) + "\n")
        else:
            f.write("\nPlayer_no: " + which_player_forprint + "\n\tself.self_strategy: " + str(self.strategy) +"\n\t" + "self.strategy_sum: " + str(self.strategy_sum) + "\n")
        f.close()


    def regret(self, my_action, opp_action, i, which_player_forprint):
        """
        we here define the regret of not having chosen an action as the difference between the utility of that action
        and the utility of the action we actually chose, with respect to the fixed choices of the other player.

        compute the regret and add it to regret sum.
        """
        result = RPS.utilities.loc[my_action, opp_action] # At this point, it can the winner is established
        facts = RPS.utilities.loc[:, opp_action].values
        regret = facts - result
        self.regret_sum += regret

        # Q: what is the difference between a regret_sum and strategy_sum?
        # A: regret_sum has affect on action(). straegy_sum is used for learn_avg_strategy

        f = open('strategy_stats_RPS.txt','a+')
        if which_player_forprint == "p2":
            f.write("\nPlayer_no: " + which_player_forprint + "\n\tself.regret_sum: " + str(self.regret_sum) +"\n\n***********************************************")
        else:
            f.write("\nPlayer_no: " + which_player_forprint + "\n\tself.regret_sum: " + str(self.regret_sum) +"\n")
        f.close()



    def action(self, i, which_player_forprint, use_avg=False):
        """
        select an action according to strategy probabilities
        """
        strategy = self.avg_strategy if use_avg else self.strategy
        act = np.random.choice(RPS.actions, p=strategy)  # Very important to understand this. This forms the basis for creating a good utility matrix in other game contexts (Poker).
        # This is not just a uniform distribution, although initially it is. It changes shape throughout the game depending on how the strategy looks.

        f = open('strategy_stats_RPS.txt','a+')
        f.write("\nPlayer_no: " + which_player_forprint + "\n\tAction: " + str(act) +"\n")
        f.close()

        return act

    def learn_avg_strategy(self):
        # averaged strategy converges to Nash Equilibrium
        summation = sum(self.strategy_sum)
        if summation > 0:
            self.avg_strategy = self.strategy_sum / summation
        else:
            self.avg_strategy = np.repeat(1/RPS.n_actions, RPS.n_actions)


        f = open('strategy_stats_RPS.txt','a+')
        f.write("\nself.strategy_sum: " + str(self.strategy_sum) + "\n")
        f.close()




class Game:
    def __init__(self, max_game=5):
        self.p1 = Player('Player1')
        self.p2 = Player('Player2')
        self.max_game = max_game

    def winner(self, a1, a2):
        result = RPS.utilities.loc[a1, a2]
        if result == 1:     return self.p1
        elif result == -1:  return self.p2
        else:               return 'Draw'

    def play(self, avg_regret_matching=False):
        def play_regret_matching():
            for i in range(0, self.max_game):
                self.p1.update_strategy(i, "p1")
                self.p2.update_strategy(i, "p2")
                a1 = self.p1.action(i, "p1")
                a2 = self.p2.action(i, "p2")
                self.p1.regret(a1, a2, i, "p1")
                self.p2.regret(a2, a1, i, "p2")


                winner = self.winner(a1, a2)
                num_wins[winner] += 1

        def play_avg_regret_matching():
            for i in range(0, self.max_game):
                a1 = self.p1.action(i, "p1", use_avg=True)
                a2 = self.p2.action(i, "p2", use_avg=True)
                winner = self.winner(a1, a2)
                num_wins[winner] += 1

        num_wins = {
            self.p1: 0,
            self.p2: 0,
            'Draw': 0
        }

        play_regret_matching() if not avg_regret_matching else play_avg_regret_matching()
        print(num_wins)

    def conclude(self):
        """
        let two players conclude the average strategy from the previous strategy stats
        """
        self.p1.learn_avg_strategy()
        self.p2.learn_avg_strategy()


if __name__ == '__main__':
    # os.remove("strategy_stats_RPS.txt")
    game = Game()

    print('==== Use simple regret-matching strategy === ')
    game.play()
    print('==== Use averaged regret-matching strategy === ')
    game.conclude()
    game.play(avg_regret_matching=True)
