class Action():

    action = ''
    winning = {'R': 'S', 'P': 'R', 'S': 'P'}
    losing = {'R': 'P', 'P': 'S', 'S': 'R'}

    def __init__(self, action):
        self.action = action

    def __eq__(self, other):
        return self.action == other.action
    
    def __gt__(self, other):
        return self.winning[self.action] == other.action

class Player():
    name = ""

    def __init__(self, name="player"):
        self.name = name

    def set_name(self, name):
        self.name = name

    def play_action(self, action):
        return Action(action)

    def receive_result(self, own, other, winning):
        pass



def main():
    pass


if __name__ == "__main__":
    main()
