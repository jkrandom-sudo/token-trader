import io
import unittest
from unittest import mock

import game


class StackedInput:
    def __init__(self, values):
        self.values = list(values)

    def __call__(self, prompt=""):
        if not self.values:
            raise EOFError(prompt)
        return self.values.pop(0)


def base_settings():
    return {"lang": "en", "sound": False, "volume": 1, "difficulty": "easy"}


class TestGame(unittest.TestCase):
    def capture(self, func, *args):
        output = io.StringIO()
        with mock.patch("sys.stdout", output):
            result = func(*args)
        return result, output.getvalue()

    def test_show_header(self):
        _, text = self.capture(game.show_header, base_settings())
        self.assertIn("Token Trader", text)

    def test_show_help(self):
        with mock.patch("builtins.input", StackedInput([""])):
            _, text = self.capture(game.show_help, base_settings())
        self.assertIn("Help", text)

    def test_show_scores_empty(self):
        with mock.patch.object(game.score_mod, "load", return_value=[]), mock.patch("builtins.input", StackedInput([""])):
            _, text = self.capture(game.show_scores, base_settings())
        self.assertIn("No scores", text)

    def test_show_scores_with_entries(self):
        rows = [{"name": "Ada", "score": 99, "difficulty": "easy"}]
        with mock.patch.object(game.score_mod, "load", return_value=rows), mock.patch("builtins.input", StackedInput([""])):
            _, text = self.capture(game.show_scores, base_settings())
        self.assertIn("Ada 99", text)

    def test_settings_menu_updates_and_saves(self):
        settings = base_settings()
        with mock.patch("builtins.input", StackedInput(["1", "2", "3", "4", "b"])), mock.patch.object(game.settings_mod, "save") as save:
            game.settings_menu(settings)
        self.assertEqual(settings["lang"], "zh")
        self.assertTrue(settings["sound"])
        self.assertEqual(settings["volume"], 2)
        self.assertEqual(settings["difficulty"], "normal")
        save.assert_called_once_with(settings)

    def test_play_round_trades_and_invalid(self):
        settings = base_settings()
        inputs = ["buy 5", "sell 2", "bad", "hold", "sell 3", "hold", "hold"]
        prices = [12, 14, 13, 15, 16]
        with mock.patch.object(game.core, "next_price", side_effect=prices), mock.patch("builtins.input", StackedInput(inputs)):
            result, text = self.capture(game.play_round, settings)
        self.assertEqual(result, 13)
        self.assertIn("Trade accepted", text)
        self.assertIn("Invalid action", text)
        self.assertIn("Final worth", text)

    def test_play_round_quits(self):
        settings = base_settings()
        with mock.patch("builtins.input", StackedInput(["q"])):
            with self.assertRaises(game.QuitGame):
                game.play_round(settings)

    def test_main_menu_unknown_then_quit(self):
        with mock.patch.object(game.settings_mod, "load", return_value=base_settings()), mock.patch("builtins.input", StackedInput(["x", "q"])):
            _, text = self.capture(game.main_menu)
        self.assertIn("Unknown choice", text)
        self.assertIn("Bye", text)

    def test_main_menu_play_saves_score(self):
        with mock.patch.object(game.settings_mod, "load", return_value=base_settings()), mock.patch.object(game, "play_round", return_value=42), mock.patch.object(game.score_mod, "add") as add, mock.patch("builtins.input", StackedInput(["p", "Ada", "", "q"])):
            game.main_menu()
        add.assert_called_once_with("Ada", 42, "easy")

    def test_main_menu_play_without_name(self):
        with mock.patch.object(game.settings_mod, "load", return_value=base_settings()), mock.patch.object(game, "play_round", return_value=42), mock.patch.object(game.score_mod, "add") as add, mock.patch("builtins.input", StackedInput(["p", "", "", "q"])):
            _, text = self.capture(game.main_menu)
        add.assert_not_called()
        self.assertIn("Score not saved", text)

    def test_main_menu_routes(self):
        with mock.patch.object(game.settings_mod, "load", return_value=base_settings()), mock.patch.object(game, "show_help") as help_fn, mock.patch.object(game, "settings_menu") as settings_fn, mock.patch.object(game, "show_scores") as scores_fn, mock.patch("builtins.input", StackedInput(["h", "s", "c", "q"])):
            game.main_menu()
        help_fn.assert_called_once()
        settings_fn.assert_called_once()
        scores_fn.assert_called_once()


if __name__ == "__main__":
    unittest.main()
