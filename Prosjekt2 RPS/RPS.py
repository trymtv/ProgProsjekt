"""
Module for the game rock, paper, scissors.
"""

from random import randint
from matplotlib import pyplot


class Action():
    """
    Class representing an action.
    """
    winning = {'R': 'S', 'P': 'R', 'S': 'P'}
    losing = {'R': 'P', 'P': 'S', 'S': 'R'}

    def __init__(self, action):
        self.action = action

    def __str__(self):
        return str(self.action)

    def __eq__(self, other):
        return self.action == other.action

    def __ne__(self, other):
        return self.action != other.action

    def __gt__(self, other):
        return self.winning[self.action] == other.action

    @staticmethod
    def wins_against(action):
        print("The played action: " + Action.losing[action])
        return Action.losing[action]


class Player():
    """
    The player superclass.
    """
    actions = ['R', 'P', 'S']

    def __init__(self, name="player"):
        self.name = name
        self.score = 0
        self.games = 0

    def __str__(self):
        return self.name

    def set_name(self, name):
        self.name = name

    @ staticmethod
    def play_action(action):
        return Action(action)

    def receive_result(self, other, winning):
        self.games += 1
        if winning:
            self.score += 1

    def get_results(self):
        return self.name + ": score=" + str(self.score) + ", games=" + str(self.games)


class RandomPlayer(Player):
    """
    A player choosing all its actions randomly.
    """

    def play_action(self):
        return Action(self.actions[randint(0, 2)])


class SequentialPlayer(Player):

    """
    A player choosing actions from a determined sequence.
    """

    def __init__(self, name):
        super().__init__(name)
        self.counter = 0

    def increment(self):
        self.counter += 1
        if self.counter >= len(self.actions):
            self.counter = 0

    def play_action(self):
        self.increment()
        print("sequential spiller: " + self.actions[self.counter])
        return Action(self.actions[self.counter])


class MostCommonPlayer(Player):

    """
    A player chosing its actions based on trying to win
    against the most common move from the opponent.
    """

    def __init__(self, name):
        super().__init__(name)
        self.opponent_actions = {'R': 0, 'P': 0, 'S': 0}
        self.most_common = self.actions[randint(0, 2)]

    def receive_result(self, other, winning):
        super().receive_result(other, winning)
        self.opponent_actions[str(other)] += 1
        if self.opponent_actions[str(other)] > self.opponent_actions[self.most_common]:
            self.most_common = str(other)
        print(self.opponent_actions)

    def play_action(self):
        if self.opponent_actions[self.most_common] == 0:
            return Action(self.actions[randint(0, 2)])
        return Action(Action.wins_against(self.most_common))


class Historian(Player):

    """
    A player looking at the last n number of moves and sees
    what the former most likely move after that is.
    """

    def __init__(self, name, remember):
        super().__init__(name)
        self.former_sequences = {}
        self.remember = remember
        self.last_moves = [""] * (remember + 1)
        self.sequence = ""

    def receive_result(self, other, winning):
        super().receive_result(other, winning)
        self.last_moves = self.last_moves[1:]
        self.last_moves.append("")
        self.last_moves[-1] = other.action
        if self.last_moves[0] != "":
            self.sequence = "".join(self.last_moves[:self.remember])
            if self.sequence not in self.former_sequences:
                self.former_sequences[self.sequence] = {'R': 0, 'P': 0, 'S': 0}
            self.former_sequences[self.sequence][self.last_moves[-1]] += 1

    def play_action(self):
        last_moves = "".join(self.last_moves[1:])
        if last_moves in self.former_sequences:
            former_moves = self.former_sequences[last_moves]
            action_guess = max(former_moves, key=former_moves.get)
        else:
            action_guess = self.actions[randint(0, 2)]
        print(action_guess)
        return Action(Action.wins_against(action_guess))


class SingleGame():

    """
    A single game for playing rps with two players.
    """

    def __init__(self, player1, player2):
        # self.players = (player1, player2)
        self.player1 = player1
        self.player2 = player2
        self.player1_won = False
        self.player2_won = False
        self.player1_action = None
        self.player2_action = None

    def perform_game(self):
        self.player1_action = self.player1.play_action()
        self.player2_action = self.player2.play_action()

        if self.player1_action != self.player2_action:
            if self.player1_action > self.player2_action:
                self.player1_won = True
            else:
                self.player2_won = True
        self.player1.receive_result(self.player2_action, self.player1_won)
        self.player2.receive_result(self.player1_action, self.player2_won)

    def show_result(self):
        if self.player1_won:
            print(str(self.player1) + " won with " + str(self.player1_action))
        elif self.player2_won:
            print(str(self.player2) + " won with " + str(self.player2_action))
        else:
            print("Draw")


class Tournament():

    """
    Helper class for making multiple games and tracking stats.
    """

    def __init__(self, player1, player2, number_of_games):
        self.player1 = player1
        self.player2 = player2
        self.number_of_games = number_of_games
        self.game_number = 0
        self.player1_wins = 0
        self.player2_wins = 0
        self.win_stats = [[], []]

    def arrange_single_game(self):
        game = SingleGame(self.player1, self.player2)
        game.perform_game()
        if game.player1_won:
            self.player1_wins += 1
        elif game.player2_won:
            self.player2_wins += 1
        game.show_result()
        del game

    def arrange_tournament(self):
        for i in range(self.number_of_games):
            self.arrange_single_game()
            self.game_number += 1
            if (i + 1) % 10 == 0:
                self.win_stats[0].append(self.player1_wins / self.player2_wins)
                self.win_stats[1].append(i)
        pyplot.plot(self.win_stats[1], self.win_stats[0])
        pyplot.show()
        print(self.player1_wins)
        print(self.player2_wins)


def choose_player(num):
    players = [RandomPlayer, SequentialPlayer, MostCommonPlayer, Historian]
    choise = int(input(f"Player {num}:"))
    name = input("Name: ")
    if choise == 3:
        remember = int(input("Remember: "))
        return Historian(name, remember)
    return players[choise](name)


def main():
    while True:
        print("0) Random\n 1) Sequenial\n 2) MostCommon\n 3) Historian")
        player1 = choose_player(1)
        player2 = choose_player(2)
        number_of_games = int(input("Number of games: "))
        turney = Tournament(player1, player2, number_of_games)
        turney.arrange_tournament()


if __name__ == "__main__":
    main()
