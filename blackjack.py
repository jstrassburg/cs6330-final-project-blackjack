import argparse
from blackjack.Games import GamesFactory, Winner
from blackjack.Strategies import qlp
from pprint import pprint


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
        csv = open(f"{self.args.game_type}.csv", 'w')
        csv.write('winner,dealer_score,player_score\n')

        results = {
            Winner.Player: 0,
            Winner.Dealer: 0,
            Winner.Push: 0
        }
        for game_number in range(self.args.games_to_play):
            print(f"Starting game number: {game_number}")
            game = GamesFactory.create(self.args.game_type, self.args.bet)
            (winner, dealer_score, player_score) = game.play()
            print(f"Played game number: {game_number}, {winner} - player: {player_score} - dealer: {dealer_score}\n")
            csv.write(f"{winner},{dealer_score},{player_score}\n")
            results[winner] = results[winner] + 1 if winner in results else 1

        print(f"\nResults after {self.args.games_to_play} games of type {self.args.game_type}:")
        print(f"\tDealer won: {results[Winner.Dealer]}")
        print(f"\tPlayer won: {results[Winner.Player]}")
        print(f"\tPush: {results[Winner.Push]}\n")

        if self.args.game_type == 'QLearningPolicyGame':
            # q_table = qlp.get_table()
            # pprint(q_table)
            for state in range(2, 22):
                print(f"state: {state} - best action: {qlp.best_action(state)}")

        csv.close()

    def add_arguments_and_parse(self):
        self.parser.add_argument('--games', dest='games_to_play', default=1000, type=int,
                                 help='The number of games to play. Default 1000.')
        self.parser.add_argument('--game-type', dest='game_type', default='FixedPolicyGame',
                                 choices=['FixedPolicyGame', 'QLearningPolicyGame', 'OptimizedPolicyGame',
                                          'NeuralFittedPolicyGame', 'TreeBasedPolicyGame'],
                                 help='The type of game to play. Default: FixedPolicyGame')
        self.parser.add_argument('--bet', dest='bet', default=500, type=int,
                                 help='The bet increment. Default $500')
        self.args = self.parser.parse_args()


def main():
    Program.main()


if __name__ == "__main__":
    main()
