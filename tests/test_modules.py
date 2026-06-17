import io
import json
import tempfile
import unittest
from pathlib import Path

import i18n
import score as score_mod
import settings as settings_mod
from sound import Sound


class TestI18n(unittest.TestCase):
    def test_translation_and_fallback(self):
        self.assertEqual(i18n.t("en", "title"), "Token Trader")
        self.assertEqual(i18n.t("zh", "title"), "代币交易")
        self.assertEqual(i18n.t("missing", "title"), "Token Trader")
        self.assertEqual(i18n.t("en", "missing"), "missing")

    def test_formatting_error_returns_text(self):
        self.assertEqual(i18n.t("en", "finished"), "Final worth {worth}. Score {score}. Rating: {rating}")


class TestSettings(unittest.TestCase):
    def test_load_defaults_missing_file(self):
        with tempfile.TemporaryDirectory() as tmp:
            path = Path(tmp) / "settings.json"
            self.assertEqual(settings_mod.load(path), settings_mod.DEFAULTS)

    def test_load_sanitizes_invalid_values(self):
        with tempfile.TemporaryDirectory() as tmp:
            path = Path(tmp) / "settings.json"
            path.write_text(json.dumps({"lang": "fr", "sound": "yes", "volume": 9, "difficulty": "bad"}), encoding="utf-8")
            self.assertEqual(settings_mod.load(path), settings_mod.DEFAULTS)

    def test_save_and_cycle(self):
        with tempfile.TemporaryDirectory() as tmp:
            path = Path(tmp) / "settings.json"
            data = settings_mod.DEFAULTS.copy()
            settings_mod.cycle_lang(data)
            settings_mod.toggle_sound(data)
            settings_mod.cycle_volume(data)
            settings_mod.cycle_difficulty(data)
            settings_mod.save(data, path)
            self.assertEqual(settings_mod.load(path), data)


class TestScore(unittest.TestCase):
    def test_load_missing_file_and_non_list(self):
        with tempfile.TemporaryDirectory() as tmp:
            path = Path(tmp) / "scores.json"
            self.assertEqual(score_mod.load(path), [])
            path.write_text("{}", encoding="utf-8")
            self.assertEqual(score_mod.load(path), [])

    def test_add_sorts_and_trims(self):
        with tempfile.TemporaryDirectory() as tmp:
            path = Path(tmp) / "scores.json"
            for idx in range(12):
                score_mod.add(f"p{idx}", idx, "easy", path)
            scores = score_mod.load(path)
            self.assertEqual(len(scores), score_mod.MAX_SCORES)
            self.assertEqual(scores[0]["score"], 11)
            self.assertEqual(scores[-1]["score"], 2)


class TestSound(unittest.TestCase):
    def test_beep_respects_enabled_and_volume(self):
        output = io.StringIO()
        Sound(True, 2, output).correct()
        self.assertEqual(output.getvalue(), "\a\a")
        output = io.StringIO()
        Sound(False, 2, output).win()
        self.assertEqual(output.getvalue(), "")
        output = io.StringIO()
        Sound(True, 0, output).lose()
        self.assertEqual(output.getvalue(), "")

    def test_named_sounds(self):
        output = io.StringIO()
        sound = Sound(True, 1, output)
        sound.incorrect()
        sound.win()
        sound.lose()
        self.assertEqual(output.getvalue(), "\a\a\a\a\a\a\a")


if __name__ == "__main__":
    unittest.main()
