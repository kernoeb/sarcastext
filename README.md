A simple Telegram bot...


Copy the template and add your token:

```
cp config.ini.example config.ini
```

```
[DEFAULT]
token = YOURTOKEN:HERE
```

> `config.ini` is gitignored, so your token stays local and is never committed.

### Prerequisites

- Python 3.9+
- Dependencies: `pip install -r requirements.txt`

> Note: this bot now uses the async API of `python-telegram-bot` (v22+).
> Enable inline mode for your bot via [@BotFather](https://t.me/BotFather) first.

Run with: `python3 sarcastext.py`

### Development

Lint and format with [ruff](https://docs.astral.sh/ruff/):

```
pip install -r requirements-dev.txt
ruff check .       # lint
ruff format .      # format
```
