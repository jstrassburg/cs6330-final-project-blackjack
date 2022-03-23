import argparse
from blackjack.Games import GamesFactory, Winner


class Program:
    args = None
    parser = argparse.ArgumentParser(description="Plays games of Blackjack")

    @staticmethod
    def main():
        program = Program()
        program.run()

    def run(self):
        self.add_arguments_and_parse()
        print(f"Playing {self.args.games_to_play} games of type {self.args.game_type}...")

        results = dict()
        for game_number in range(self.args.games_to_play):
            game = GamesFactory.create(self.args.game_type)
            winner = game.play()
            print(f"Played game number: {game_number}, {winner}")
            results[winner] = results[winner] + 1 if winner in results else 1

        print(f"\nResults after {self.args.games_to_play} games of type {self.args.game_type}:")
        print(f"\tDealer won: {results[Winner.Dealer]}")
        print(f"\tPlayer won: {results[Winner.Player]}")

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
