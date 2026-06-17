"""Core logic for Token Trader."""
import random

DIFFICULTY_CONFIG = {
    "easy": {"days": 6, "cash": 100, "start_price": 10, "volatility": 3, "bonus": 1},
    "normal": {"days": 8, "cash": 120, "start_price": 12, "volatility": 5, "bonus": 2},
    "hard": {"days": 10, "cash": 150, "start_price": 15, "volatility": 8, "bonus": 3},
}


def config(difficulty):
    return DIFFICULTY_CONFIG.get(difficulty, DIFFICULTY_CONFIG["normal"])


def new_state(difficulty):
    cfg = config(difficulty)
    return {"day": 1, "cash": cfg["cash"], "tokens": 0, "price": cfg["start_price"], "history": [cfg["start_price"]], "difficulty": difficulty}


def next_price(price, difficulty, rng=None):
    rng = rng or random
    change = rng.randint(-config(difficulty)["volatility"], config(difficulty)["volatility"])
    return max(1, price + change)


def normalize_action(text):
    parts = text.strip().lower().split()
    if not parts:
        return None, None
    action = parts[0]
    if action in ("hold", "h"):
        return "hold", 0
    if action not in ("buy", "b", "sell", "s") or len(parts) != 2:
        return None, None
    if not parts[1].isdigit():
        return None, None
    amount = int(parts[1])
    if amount <= 0:
        return None, None
    return ("buy" if action in ("buy", "b") else "sell"), amount


def apply_action(state, action, amount):
    if action == "hold":
        return True
    if action == "buy":
        cost = state["price"] * amount
        if cost > state["cash"]:
            return False
        state["cash"] -= cost
        state["tokens"] += amount
        return True
    if action == "sell":
        if amount > state["tokens"]:
            return False
        state["tokens"] -= amount
        state["cash"] += state["price"] * amount
        return True
    return False


def advance_day(state, rng=None):
    state["day"] += 1
    state["price"] = next_price(state["price"], state["difficulty"], rng)
    state["history"].append(state["price"])


def net_worth(state):
    return state["cash"] + state["tokens"] * state["price"]


def score_for(state):
    cfg = config(state["difficulty"])
    profit = net_worth(state) - cfg["cash"]
    return max(0, profit) * cfg["bonus"]


def trend(history):
    if len(history) < 2:
        return "flat"
    if history[-1] > history[-2]:
        return "up"
    if history[-1] < history[-2]:
        return "down"
    return "flat"


def final_rating(score):
    if score >= 150:
        return "tycoon"
    if score >= 60:
        return "broker"
    if score > 0:
        return "rookie"
    return "broke"
