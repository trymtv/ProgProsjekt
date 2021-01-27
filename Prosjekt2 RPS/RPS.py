from random import randint


class Action():

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


class Player():

    def __init__(self, name="player"):
        self.name = name
        self.score = 0
        self.games = 0

    def __str__(self):
        return self.name

    def set_name(self, name):
        self.name = name

    @staticmethod
    def play_action(action):
        return Action(action)

    def receive_result(self, other, winning):
        self.games += 1
        if winning:
            self.score += 1

    def get_results(self):
        return self.name + ": score=" + str(self.score) + ", games=" + str(self.games)


class RandomPlayer(Player):

    actions = ['R', 'P', 'S']

    def play_action(self):
        return Action(self.actions[randint(0, 2)])


class SequentialPlayer(Player):

    sequence = ['R', 'P', 'S']

    def __init__(self, name):
        super().__init__(name)
        self.counter = 0

    def increment(self):
        self.counter += 1
        if self.counter >= len(self.sequence):
            self.counter = 0

    def play_action(self):
        self.increment()
        return Action(self.sequence[self.counter])


class MostCommonPlayer(Player):

    def __init__(self, name):
        super.__init__(name)
        self.opponent_actions = {'R': 0, 'P': 0, 'S': 0}


class SingleGame():

    def __init__(self, player1, player2):
        #self.players = (player1, player2)
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

    def __init__(self, player1, player2, number_of_games):
        self.player1 = player1
        self.player2 = player2
        self.number_of_games = number_of_games

    def arrange_single_game(self):
        game = SingleGame(self.player1, self.player2)
        game.perform_game()
        game.show_result()
        del game

    def arrange_tournament(self):
        for _ in range(self.number_of_games):
            self.arrange_single_game()


def main():
    player1 = RandomPlayer("player1")
    player2 = SequentialPlayer("player2")
    turney = Tournament(player1, player2, 1)
    turney.arrange_tournament()
    print(player1.get_results())
    print(player2.get_results())


if __name__ == "__main__":
    main()
