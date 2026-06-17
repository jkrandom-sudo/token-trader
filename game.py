"""Console game for Token Trader."""
import score as score_mod
import settings as settings_mod
import token_trader as core
from i18n import t
from sound import Sound


class QuitGame(Exception):
    pass


def _print(text=""):
    print(text)


def show_header(settings):
    _print("=" * 32)
    _print(t(settings["lang"], "title"))
    _print("=" * 32)


def show_help(settings):
    show_header(settings)
    _print(t(settings["lang"], "help_title"))
    _print(t(settings["lang"], "help_text"))
    input(t(settings["lang"], "press_enter"))


def show_scores(settings):
    show_header(settings)
    _print(t(settings["lang"], "scores"))
    scores = score_mod.load()
    if not scores:
        _print(t(settings["lang"], "no_scores"))
    for idx, item in enumerate(scores, 1):
        _print(f"{idx}. {item.get('name', '?')} {item.get('score', 0)} ({item.get('difficulty', '?')})")
    input(t(settings["lang"], "press_enter"))


def settings_menu(settings):
    while True:
        show_header(settings)
        _print(t(settings["lang"], "settings"))
        _print(f"{t(settings['lang'], 'lang')}: {settings['lang']}")
        _print(f"{t(settings['lang'], 'sound')}: {t(settings['lang'], 'on' if settings['sound'] else 'off')}")
        _print(f"{t(settings['lang'], 'volume')}: {settings['volume']}")
        _print(f"{t(settings['lang'], 'difficulty')}: {settings['difficulty']}")
        choice = input(t(settings["lang"], "settings_menu") + "\n" + t(settings["lang"], "choice")).strip().lower()
        if choice == "1":
            settings_mod.cycle_lang(settings)
        elif choice == "2":
            settings_mod.toggle_sound(settings)
        elif choice == "3":
            settings_mod.cycle_volume(settings)
        elif choice == "4":
            settings_mod.cycle_difficulty(settings)
        elif choice == "b":
            settings_mod.save(settings)
            return
        else:
            _print(t(settings["lang"], "unknown"))


def play_round(settings):
    lang = settings["lang"]
    difficulty = settings["difficulty"]
    cfg = core.config(difficulty)
    snd = Sound(settings["sound"], settings["volume"])
    state = core.new_state(difficulty)

    show_header(settings)
    while state["day"] <= cfg["days"]:
        _print(t(lang, "status", day=state["day"], days=cfg["days"], cash=state["cash"], tokens=state["tokens"], price=state["price"], trend=core.trend(state["history"])))
        text = input(t(lang, "action_prompt")).strip().lower()
        if text == "q":
            raise QuitGame()
        action, amount = core.normalize_action(text)
        if not core.apply_action(state, action, amount):
            _print(t(lang, "invalid"))
            snd.incorrect()
            continue
        _print(t(lang, "accepted"))
        snd.correct()
        if state["day"] < cfg["days"]:
            core.advance_day(state)
        else:
            break

    worth = core.net_worth(state)
    score = core.score_for(state)
    rating_key = core.final_rating(score)
    _print(t(lang, "finished", worth=worth, score=score, rating=t(lang, rating_key)))
    if score > 0:
        snd.win()
    else:
        snd.lose()
    return score


def main_menu():
    settings = settings_mod.load()
    while True:
        show_header(settings)
        choice = input(t(settings["lang"], "main_menu") + "\n" + t(settings["lang"], "choice")).strip().lower()
        if choice == "p":
            try:
                result = play_round(settings)
            except QuitGame:
                result = 0
            if result > 0:
                name = input(t(settings["lang"], "name_prompt")).strip()
                if name:
                    score_mod.add(name, result, settings["difficulty"])
                    _print(t(settings["lang"], "saved"))
                else:
                    _print(t(settings["lang"], "not_saved"))
            input(t(settings["lang"], "press_enter"))
        elif choice == "h":
            show_help(settings)
        elif choice == "s":
            settings_menu(settings)
        elif choice == "c":
            show_scores(settings)
        elif choice == "q":
            _print(t(settings["lang"], "bye"))
            return
        else:
            _print(t(settings["lang"], "unknown"))


if __name__ == "__main__":
    main_menu()
