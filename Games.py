class GameNotImplementedException(ValueError):
    pass


class GamesFactory:
    @staticmethod
    def create(game_class):
        if game_class == 'SimplifiedGame':
            return SimplifiedGame()
        else:
            raise GameNotImplementedException()


class Game:
    pass


class SimplifiedGame(Game):
    pass
