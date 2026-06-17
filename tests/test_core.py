import unittest

import token_trader as core


class FixedRng:
    def __init__(self, values):
        self.values = list(values)

    def randint(self, low, high):
        return self.values.pop(0)


class TestCore(unittest.TestCase):
    def test_config_fallback(self):
        self.assertEqual(core.config("bad"), core.config("normal"))

    def test_new_state(self):
        state = core.new_state("easy")
        self.assertEqual(state["cash"], 100)
        self.assertEqual(state["price"], 10)
        self.assertEqual(state["history"], [10])

    def test_next_price_has_floor(self):
        self.assertEqual(core.next_price(2, "easy", FixedRng([-3])), 1)
        self.assertEqual(core.next_price(10, "easy", FixedRng([2])), 12)

    def test_normalize_action(self):
        self.assertEqual(core.normalize_action("hold"), ("hold", 0))
        self.assertEqual(core.normalize_action("b 2"), ("buy", 2))
        self.assertEqual(core.normalize_action("sell 3"), ("sell", 3))
        self.assertEqual(core.normalize_action("buy 0"), (None, None))
        self.assertEqual(core.normalize_action("bad"), (None, None))

    def test_apply_action(self):
        state = core.new_state("easy")
        self.assertTrue(core.apply_action(state, "buy", 3))
        self.assertEqual(state["cash"], 70)
        self.assertEqual(state["tokens"], 3)
        self.assertFalse(core.apply_action(state, "buy", 99))
        self.assertTrue(core.apply_action(state, "sell", 2))
        self.assertEqual(state["cash"], 90)
        self.assertEqual(state["tokens"], 1)
        self.assertFalse(core.apply_action(state, "sell", 9))
        self.assertFalse(core.apply_action(state, None, None))

    def test_advance_day_and_worth_score(self):
        state = core.new_state("easy")
        core.apply_action(state, "buy", 5)
        core.advance_day(state, FixedRng([3]))
        self.assertEqual(state["day"], 2)
        self.assertEqual(state["price"], 13)
        self.assertEqual(core.net_worth(state), 115)
        self.assertEqual(core.score_for(state), 15)

    def test_trend(self):
        self.assertEqual(core.trend([10]), "flat")
        self.assertEqual(core.trend([10, 12]), "up")
        self.assertEqual(core.trend([10, 8]), "down")
        self.assertEqual(core.trend([10, 10]), "flat")

    def test_final_rating(self):
        self.assertEqual(core.final_rating(150), "tycoon")
        self.assertEqual(core.final_rating(60), "broker")
        self.assertEqual(core.final_rating(1), "rookie")
        self.assertEqual(core.final_rating(0), "broke")


if __name__ == "__main__":
    unittest.main()
