# arsenal-reddit-bot

## Running the script

Build a `.env` file in the same directory with the following variables (**NOTE: never push this file**):  

```env
CLIENT_ID="client_id"
CLIENT_SECRET="client_secret"
REDDIT_USERNAME="username"
REDDIT_PASSWORD="password"
```

Set `environment variables` as:

```bash
set -a
source <filename>.env
set +a
```

Run the script as `python bot.py`
