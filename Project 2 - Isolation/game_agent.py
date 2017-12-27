"""Finish all TODO items in this file to complete the isolation project, then
test your agent's strength against a set of known agents using tournament.py
and include the results in your report.
"""
import random

class SearchTimeout(Exception):
    """Subclass base exception for code clarity. """
    pass


def custom_score(game, player):
    """
    This score is the difference between own_moves and the opponent moves,
    penalizing further the edge and corner moves with different weights: the
    corner moves are penalized more severely as it's thought that they in general
    are not desirable. 

    Parameters
    ----------
    game : `isolation.Board`
        An instance of `isolation.Board` encoding the current state of the
        game (e.g., player locations and blocked cells).

    player : object
        A player instance in the current game (i.e., an object corresponding to
        one of the player objects `game.__player_1__` or `game.__player_2__`.)

    Returns
    -------
    float
        The heuristic value of the current game state to the specified player.
    """
    if game.is_loser(player):
        return float("-inf")

    if game.is_winner(player):
        return float("inf")
    
    my_moves = game.get_legal_moves(player)
    opp_moves = game.get_legal_moves(game.get_opponent(player))
    edge_moves = []
    for i in range(game.height):
        for j in range(game.width):
            if i==0 or i==game.height-1:
                if j==0 or j==game.width-1:
                    edge_moves.append((i,j))
                    
    my_edge_moves = [move for move in my_moves if move in edge_moves]
    opp_edge_moves = [move for move in opp_moves if move in edge_moves]
    
    my_corner_moves =  [move for move in my_moves if move in edge_moves and move[0]==move[1]]
    opp_corner_moves = [move for move in opp_moves if move in edge_moves and move[0]==move[1]]
    
    score = float(len(my_moves) - len(my_edge_moves) - 2*len(my_corner_moves)
                 - len(opp_moves) + len(opp_edge_moves) + 2*len(opp_corner_moves))
    return score


def custom_score_2(game, player):
    """
    The score is the difference between 'own' and opponent moves but penalizing
    if the move in on either of the 4 corners of the board.

    Note: this function should be called from within a Player instance as
    `self.score()` -- you should not need to call this function directly.

    Parameters
    ----------
    game : `isolation.Board`
        An instance of `isolation.Board` encoding the current state of the
        game (e.g., player locations and blocked cells).

    player : object
        A player instance in the current game (i.e., an object corresponding to
        one of the player objects `game.__player_1__` or `game.__player_2__`.)

    Returns
    -------
    float
        The heuristic value of the current game state to the specified player.
    """
    if game.is_winner(player):
        return float("+inf")

    if game.is_loser(player):
        return float("-inf")
    
    my_legal_moves = game.get_legal_moves()
    opp_legal_moves = game.get_legal_moves(game.get_opponent(player))
    
    my_moves_not_corner = [move for move in my_legal_moves if move!=(0,0) 
                                                        and move!=(game.height-1,0)
                                                        and move != (0,game.width-1)
                                                        and move!= (game.height-1,game.width-1)]
    opp_moves_not_corner = [move for move in opp_legal_moves if move!=(0,0) 
                                                        and move!=(game.height-1,0)
                                                        and move != (0,game.width-1)
                                                        and move!= (game.height-1,game.width-1)]
    
    return float(len(my_moves_not_corner) - len(opp_moves_not_corner))   

def custom_score_3(game, player):
    """
    The score is calculated by taking the ratio of the number of available
    own_moves to those of the opponent moves. This is similar to looking at the
    differnce between the numbers of moves but with a different scaling. 
    
    Note: this function should be called from within a Player instance as
    `self.score()` -- you should not need to call this function directly.

    Parameters
    ----------
    game : `isolation.Board`
        An instance of `isolation.Board` encoding the current state of the
        game (e.g., player locations and blocked cells).

    player : object
        A player instance in the current game (i.e., an object corresponding to
        one of the player objects `game.__player_1__` or `game.__player_2__`.)

    Returns
    -------
    float
        The heuristic value of the current game state to the specified player.
    """
    if game.is_winner(player):
        return float("+inf")

    if game.is_loser(player):
        return float("-inf")
    
    my_legal_moves = game.get_legal_moves()
    opp_legal_moves = game.get_legal_moves(game.get_opponent(player))
    
    if len(opp_legal_moves)>0:
        score = float(len(my_legal_moves)/len(opp_legal_moves))
    else:
        score = float(len(my_legal_moves))
        
    
    return score


class IsolationPlayer:
    """Base class for minimax and alphabeta agents -- this class is never
    constructed or tested directly.

    ********************  DO NOT MODIFY THIS CLASS  ********************

    Parameters
    ----------
    search_depth : int (optional)
        A strictly positive integer (i.e., 1, 2, 3,...) for the number of
        layers in the game tree to explore for fixed-depth search. (i.e., a
        depth of one (1) would only explore the immediate sucessors of the
        current state.)

    score_fn : callable (optional)
        A function to use for heuristic evaluation of game states.

    timeout : float (optional)
        Time remaining (in milliseconds) when search is aborted. Should be a
        positive value large enough to allow the function to return before the
        timer expires.
    """
    def __init__(self, search_depth=3, score_fn=custom_score, timeout=10.):
        self.search_depth = search_depth
        self.score = score_fn
        self.time_left = None
        self.TIMER_THRESHOLD = timeout


class MinimaxPlayer(IsolationPlayer):
    """Game-playing agent that chooses a move using depth-limited minimax
    search. You must finish and test this player to make sure it properly uses
    minimax to return a good move before the search time limit expires.
    """

    def get_move(self, game, time_left):
        """Search for the best move from the available legal moves and return a
        result before the time limit expires.

        **************  YOU DO NOT NEED TO MODIFY THIS FUNCTION  *************

        For fixed-depth search, this function simply wraps the call to the
        minimax method, but this method provides a common interface for all
        Isolation agents, and you will replace it in the AlphaBetaPlayer with
        iterative deepening search.

        Parameters
        ----------
        game : `isolation.Board`
            An instance of `isolation.Board` encoding the current state of the
            game (e.g., player locations and blocked cells).

        time_left : callable
            A function that returns the number of milliseconds left in the
            current turn. Returning with any less than 0 ms remaining forfeits
            the game.

        Returns
        -------
        (int, int)
            Board coordinates corresponding to a legal move; may return
            (-1, -1) if there are no available legal moves.
        """
        self.time_left = time_left

        # Initialize the best move so that this function returns something
        # in case the search fails due to timeout
        best_move = (-1, -1)

        try:
            return self.minimax(game, self.search_depth)

        except SearchTimeout:
            pass  # Handle any actions required after timeout as needed

        # Return the best move from the last completed search iteration
        return best_move
    
    def minimax(self, game, depth):
        if self.time_left() < self.TIMER_THRESHOLD:
            raise SearchTimeout()
        return self.minimax_wrapper(game,depth)[1]
    
    def active_player(self,game):
        if game.active_player==self:
            return True
        else:
            return False
        
    def minimax_wrapper(self,game,depth):
        if self.time_left() < self.TIMER_THRESHOLD:
            raise SearchTimeout()

        if (depth==0) or (len(game.get_legal_moves(self))==0):
            return (self.score(game,self), game.get_player_location(self))   
        
        if self.active_player(game):
            best_value = float("-inf")
            best_move = (-1,-1)
            for move in game.get_legal_moves():
                new_game = game.forecast_move(move)
                value = self.minimax_wrapper(new_game,depth-1)[0]
                if value>best_value:
                    best_move = move
                    best_value = value
                    
            return (best_value,best_move)
        else:
            best_value = float("+inf")
            best_move = (-1,-1)
            for move in game.get_legal_moves():
                new_game = game.forecast_move(move)
                value = self.minimax_wrapper(new_game,depth-1)[0]
                if value<best_value:
                    best_move = move
                    best_value = value
                    
            return (best_value,best_move)


class AlphaBetaPlayer(IsolationPlayer):
    """Game-playing agent that chooses a move using iterative deepening minimax
    search with alpha-beta pruning. You must finish and test this player to
    make sure it returns a good move before the search time limit expires.
    """

    def get_move(self, game, time_left):
        """Search for the best move from the available legal moves and return a
        result before the time limit expires.

        Modify the get_move() method from the MinimaxPlayer class to implement
        iterative deepening search instead of fixed-depth search.

        **********************************************************************
        NOTE: If time_left() < 0 when this function returns, the agent will
              forfeit the game due to timeout. You must return _before_ the
              timer reaches 0.
        **********************************************************************

        Parameters
        ----------
        game : `isolation.Board`
            An instance of `isolation.Board` encoding the current state of the
            game (e.g., player locations and blocked cells).

        time_left : callable
            A function that returns the number of milliseconds left in the
            current turn. Returning with any less than 0 ms remaining forfeits
            the game.

        Returns
        -------
        (int, int)
            Board coordinates corresponding to a legal move; may return
            (-1, -1) if there are no available legal moves.
        """
        self.time_left = time_left
        move = (-1, -1)
        
        depth = 1
        while depth<float("+inf"):
            try:
                move = self.alphabeta(game,depth)
                depth +=1
            except SearchTimeout:
                break
        return move
            

    def alphabeta(self, game, depth, alpha=float("-inf"), beta=float("inf")):
        """Implement depth-limited minimax search with alpha-beta pruning as
        described in the lectures.

        This should be a modified version of ALPHA-BETA-SEARCH in the AIMA text
        https://github.com/aimacode/aima-pseudocode/blob/master/md/Alpha-Beta-Search.md

        **********************************************************************
            You MAY add additional methods to this class, or define helper
                 functions to implement the required functionality.
        **********************************************************************

        Parameters
        ----------
        game : isolation.Board
            An instance of the Isolation game `Board` class representing the
            current game state

        depth : int
            Depth is an integer representing the maximum number of plies to
            search in the game tree before aborting

        alpha : float
            Alpha limits the lower bound of search on minimizing layers

        beta : float
            Beta limits the upper bound of search on maximizing layers

        Returns
        -------
        (int, int)
            The board coordinates of the best move found in the current search;
            (-1, -1) if there are no legal moves

        Notes
        -----
            (1) You MUST use the `self.score()` method for board evaluation
                to pass the project tests; you cannot call any other evaluation
                function directly.

            (2) If you use any helper functions (e.g., as shown in the AIMA
                pseudocode) then you must copy the timer check into the top of
                each helper function or else your agent will timeout during
                testing.
        """
        
        # Book keeping:
        if self.time_left() < self.TIMER_THRESHOLD:
            raise SearchTimeout()
          
        return self.alphabeta_wrapper(game,depth)[1]
    
    def active_player(self,game):
        if game.active_player==self:
            return True
        else:
            return False
        
    def alphabeta_wrapper(self, game, depth, alpha=float("-inf"), beta=float("+inf")):
        
        if self.time_left() < self.TIMER_THRESHOLD:
            raise SearchTimeout()

        if (depth==0) or (len(game.get_legal_moves(self))==0):
            return (self.score(game,self), game.get_player_location(self))   
        
        if self.active_player(game):
            best_value = float("-inf")
            best_move = (-1,-1)
            for move in game.get_legal_moves():
                new_game = game.forecast_move(move)
                value = self.alphabeta_wrapper(new_game,depth-1, alpha, beta)[0]
                if value>best_value:
                    best_move = move
                    best_value = value
                if best_value >= beta:
                    return (best_value, best_move)
                else:
                    alpha = max(best_value,alpha)
                
            return (best_value,best_move)
        else:
            best_value = float("+inf")
            best_move = (-1,-1)
            for move in game.get_legal_moves():
                new_game = game.forecast_move(move)
                value = self.alphabeta_wrapper(new_game,depth-1, alpha, beta)[0]
                if value<best_value:
                    best_move = move
                    best_value = value
                if best_value<=alpha:
                    return (best_value, best_move)
                else:
                    beta = min(best_value, beta)
                    
            return (best_value,best_move)