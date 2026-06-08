import random
import unittest

from game import LiarGame, Phase, Winner, normalize_answer


PLAYERS = [
    (1, "Alpha"),
    (2, "Bravo"),
    (3, "Charlie"),
    (4, "Delta"),
]


class LiarGameTests(unittest.TestCase):
    def make_game(self) -> LiarGame:
        return LiarGame(PLAYERS, "떡볶이", "음식", rng=random.Random(1))

    def test_voting_non_liar_makes_liars_win(self) -> None:
        game = self.make_game()
        non_liar = game.citizens()[0]
        game.start_discussion()
        game.start_vote()
        for voter in game.players:
            game.submit_vote(voter.user_id, non_liar.user_id)

        result = game.resolve_vote()

        self.assertEqual(result.target, non_liar)
        self.assertEqual(game.phase, Phase.ENDED)
        self.assertEqual(game.winner, Winner.LIARS)

    def test_voting_liar_then_wrong_guess_makes_citizens_win(self) -> None:
        game = self.make_game()
        liar = game.liars()[0]
        game.start_vote()
        for voter in game.players:
            game.submit_vote(voter.user_id, liar.user_id)

        game.resolve_vote()
        guess = game.resolve_guess(liar.user_id, "라면")

        self.assertFalse(guess.correct)
        self.assertEqual(game.winner, Winner.CITIZENS)

    def test_voting_liar_then_correct_guess_makes_liars_win(self) -> None:
        game = self.make_game()
        liar = game.liars()[0]
        game.start_vote()
        for voter in game.players:
            game.submit_vote(voter.user_id, liar.user_id)

        game.resolve_vote()
        guess = game.resolve_guess(liar.user_id, " 떡 볶 이 ")

        self.assertTrue(guess.correct)
        self.assertEqual(game.winner, Winner.LIARS)

    def test_tie_makes_liars_win(self) -> None:
        game = self.make_game()
        first, second = game.players[:2]
        game.start_vote()
        game.submit_vote(1, first.user_id)
        game.submit_vote(2, first.user_id)
        game.submit_vote(3, second.user_id)
        game.submit_vote(4, second.user_id)

        result = game.resolve_vote()

        self.assertTrue(result.tied)
        self.assertEqual(game.winner, Winner.LIARS)

    def test_answer_normalization_removes_spacing_and_symbols(self) -> None:
        self.assertEqual(normalize_answer(" 떡-볶 이! "), "떡볶이")


if __name__ == "__main__":
    unittest.main()
