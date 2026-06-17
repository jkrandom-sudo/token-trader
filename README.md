# Token Trader / 代币交易

A bilingual console trading game written with the Python standard library.

一个使用 Python 标准库编写的双语控制台代币交易小游戏。

## Features / 功能

- Buy, sell, or hold tokens over several trading days.
- Random price movement with difficulty-based volatility.
- Profit becomes the final score.
- Three difficulty levels with different days, starting cash, prices, and volatility.
- Bilingual UI: English and Chinese.
- Persistent JSON settings and top scores.
- Optional terminal bell sound with adjustable volume.
- Automated tests for core logic, persistence modules, sound, and menu gameplay.

## Requirements / 环境要求

- Python 3.9+
- No third-party dependencies.

## Run / 启动

```bash
python3 game.py
```

## Test / 测试

```bash
python3 -m py_compile game.py token_trader.py i18n.py settings.py score.py sound.py
python3 tests/run_tests.py
```

## How to Play / 玩法

1. Choose Play from the main menu.
2. Each day shows cash, tokens, current price, and trend.
3. Enter `buy N`, `sell N`, or `hold`.
4. Invalid trades do not advance the day.
5. At the end, final net worth determines score.
6. Type `q` to quit the current game.

## Difficulty / 难度

| Difficulty | Days | Cash | Start price | Volatility | Score bonus |
| --- | ---: | ---: | ---: | ---: | ---: |
| easy | 6 | 100 | 10 | 3 | 1x |
| normal | 8 | 120 | 12 | 5 | 2x |
| hard | 10 | 150 | 15 | 8 | 3x |

## Files / 文件

- `game.py` — console UI and menus.
- `token_trader.py` — core trading, pricing, scoring, and rating logic.
- `i18n.py` — bilingual strings.
- `settings.py` — JSON settings persistence.
- `score.py` — JSON score persistence.
- `sound.py` — terminal bell sound helper.
- `tests/` — automated unit tests.
