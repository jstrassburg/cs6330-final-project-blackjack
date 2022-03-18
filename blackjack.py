import argparse
from Games import GamesFactory


class Program:
    args = None
    parser = argparse.ArgumentParser(description="Plays games of Blackjack")

    @staticmethod
    def main():
        program = Program()
        program.run()

    def run(self):
        self.add_arguments_and_parse()
        print(f"Playing {self.args.games_to_play} games of type {self.args.game_type}")

        game = GamesFactory.create(self.args.game_type)
        print(type(game))

    def add_arguments_and_parse(self):
        self.parser.add_argument('--games', dest='games_to_play', default=1000,
                                 help='The number of games to play. Default 1000.')
        self.parser.add_argument('--game-type', dest='game_type', default='SimplifiedGame', choices=['SimplifiedGame'],
                                 help='The type of game to play. Default: SimplifiedGame')
        self.args = self.parser.parse_args()


def main():
    Program.main()


if __name__ == "__main__":
    main()
