import main as rm_poker
from treys import *
class HandEvaluation():

    def __init__(self, card_holding, playerID, evaluation = None, event = "Preflop"):
        self.card_holding = card_holding
        self.card_a, self.card_b = self.parse_cards()
        self.evaluation = self.evaluate(event)
        self.rc = ''
        self.event = event
        self.playerID = playerID

    def __str__(self):
        st = "{}\t\t Player ID: {}\n".format(self.event, self.playerID) if self.event=="Preflop" else "{}\t\t\t Player ID: {}\n".format(self.event, self.playerID) 
        st += "Cards: {}{}\n".format(Card.int_to_pretty_str(self.hand[0]), Card.int_to_pretty_str(self.hand[1]))
        st += "Board {}{}{}\n".format(Card.int_to_pretty_str(self.board[0]), Card.int_to_pretty_str(self.board[1]), Card.int_to_pretty_str(self.board[2]))
        st += "Evaluation: {} ({}), Rank_Class: {}, \n".format(self.evaluation[0], self.evaluation[2], self.evaluation[1]) if self.event=="Preflop" else "Evaluation: {} ({}), Rank_Class: {}, \n-----------------".format(self.evaluation[0], self.evaluation[2], self.evaluation[1])
        return st

    def parse_cards(self):
        a, b = self.card_holding.get_card(0) , self.card_holding.get_card(1)
        a_rank, a_suit = a
        b_rank, b_suit = b
        
        a_card = Card.new(str(a_rank) + str(a_suit))
        b_card = Card.new(str(b_rank) + str(b_suit))
    
        return [a_card, b_card]

    def setup_board(self, board, random, hand = None):
        #Example board -- DEBUG
        b = []
        if board == None and random == 'False': #FLOP
            #import from file giving hand status
            b = [
                Card.new('Ah'),
                Card.new('Kd'),
                Card.new('Jc')
            ]
        if board == None and random == 'True': #PREFLOP
            deck = Deck()
            b = deck.draw(3)
        return b

    def evaluate(self, event):
        evaluator = rm_poker.Evaluator()
        if event == "Preflop":
            self.hand = self.parse_cards()
            self.board = self.setup_board(None, 'True', self.hand)
            evaluation = evaluator.evaluate(self.hand, self.board)
            rc = self.rank_class(evaluator, evaluation)
            score_desc = evaluator.class_to_string(rc)
            return evaluation, rc, score_desc, event 
        
        elif event == "Flop":
            self.hand = self.parse_cards()
            self.board = self.setup_board(None, 'False')     # Only pass in none for now
            evaluation = evaluator.evaluate(self.hand, self.board)
            rc = self.rank_class(evaluator, evaluation)
            score_desc = evaluator.class_to_string(rc)
            return evaluation, rc, score_desc, event

    def rank_class(self, evaluator, evaluation):
        rc = evaluator.get_rank_class(evaluation)
        return rc

    def get_evaluation(self):
        return self.evaluation
