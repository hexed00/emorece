# Emorce Token Bot (Python)

**Discord Token Live + Mass Joiner** — Railway ready. 50k+ tokens.

---

## Commands

| Command | Description |
|---------|-------------|
| `/token log` | Add tokens (paste or .txt) |
| `/token count` | Show token count |
| `/token preview` | Preview first 10 (masked) |
| `/token clear` | Clear all tokens |
| `/token output` | Download as .txt |
| `/emorce joiner` | Mass join to server |
| `/emorce start` | Alias for joiner |
| `/bot image` | Change bot avatar |
| `/bot banner` | Change bot banner |
| `/bot status` | Set activity/status |

---

## Setup Guide

### Part 1: Discord Developer Portal

**1. Create Application**
- Go to https://discord.com/developers/applications
- Click **New Application**
- Name it anything (e.g., `Emorce Live`)
- Accept terms → **Create**

**2. Create Bot**
- Left sidebar → **Bot**
- Click **Add Bot** → **Yes**
- Under **TOKEN** → click **Reset Token** → **Copy**
- Save this as `DISCORD_TOKEN` in your `.env`

**3. Enable Intents**
- Scroll to **Privileged Gateway Intents**
- Turn ON: **Message Content Intent**

**4. Get OAuth URL**
- Left sidebar → **OAuth2** → **URL Generator**
- **Scopes**: check `bot` + `applications.commands`
- **Permissions**: 
  - `Send Messages`
  - `Embed Links`
  - `Attach Files`
  - `Use Application Commands`
- Copy the generated URL at bottom

**5. Invite Bot**
- Open the URL → select your server → **Authorize**

**6. Get Application ID**
- Left sidebar → **General Information**
- Copy **Application ID** (Client ID)
- Save as `CLIENT_ID` (you won't need this for running, but save it)

**7. Get Your User ID**
- Discord → User Settings → **Advanced** → toggle **Developer Mode** ON
- Right-click your name anywhere → **Copy User ID**
- Save this to `OWNER_IDS` in `.env`

---

### Part 2: Local Test (Optional)

```bash
# 1. Extract the bot folder
cd emorce-py

# 2. Install Python 3.9+
# (if not already installed)

# 3. Install dependencies
pip install -r requirements.txt

# 4. Create .env from example
cp .env.example .env

# 5. Edit .env with your values
# DISCORD_TOKEN=your_bot_token
# OWNER_IDS=your_user_id

# 6. Run the bot
python src/main.py
```

You should see:
```
[Emorce] Logged in as YourBot#1234
[Emorce] Tokens loaded: 0
[Emorce] Synced X command(s)
```

In Discord, type `/` and you should see all commands.

---

### Part 3: Railway Deploy (Production)

**Step 1: Push to GitHub**
1. Create a **private** GitHub repo
2. Push entire `emorce-py` folder
3. Do NOT commit `.env` file

**Step 2: Create Railway Project**
1. Go to https://railway.app
2. Click **New Project**
3. Select **Deploy from GitHub repo**
4. Choose your repository
5. Railway auto-detects Python

**Step 3: Add Environment Variables**
- Click the service
- Go to **Variables** tab
- Add these:

```
DISCORD_TOKEN=paste_your_bot_token
OWNER_IDS=paste_your_user_id
LOCKED_CHANNEL_ID=
JOIN_DELAY_MS=800
MAX_CONCURRENT_JOINS=5
BOT_STATUS=Emorce Tokens
BOT_ACTIVITY=Watching
DATA_DIR=/data
```

**Step 4: Add Volume (for persistent storage)**
1. Click **+ New** → **Volume**
2. Mount path: `/data`
3. This keeps tokens.txt alive across restarts

**Step 5: Deploy**
- Railway auto-deploys on git push
- Or click **Deploy**
- Open **Deployments** → **View Logs**
- Wait for `[Emorce] Logged in as ...`

Done! Bot is live.

---

## Usage

### 1. Add Tokens
```
/token log tokens:MTA1...paste_all_tokens_here
```
Or attach a `.txt` file with one token per line.

### 2. Check Count
```
/token count
```

### 3. Preview
```
/token preview
```

### 4. Mass Join
```
/emorce joiner invite:https://discord.gg/xxxxx limit:5000 delay:800
```
Watch the progress embed update live.

### 5. Export Tokens
```
/token output
```
Downloads as `tokens.txt`.

---

## Permissions

- **Bot Owners** (OWNER_IDS) → can use ALL commands
- **Server Owner** → can use joiner on their own server only
- Optional **LOCKED_CHANNEL_ID** → all commands only work in that channel

---

## Environment Variables

| Variable | Required | Default | Notes |
|----------|----------|---------|-------|
| `DISCORD_TOKEN` | Yes | — | Bot token |
| `OWNER_IDS` | Yes | — | Comma-separated user IDs |
| `LOCKED_CHANNEL_ID` | No | empty | Restrict to channel |
| `JOIN_DELAY_MS` | No | 800 | Delay between joins (ms) |
| `MAX_CONCURRENT_JOINS` | No | 5 | Parallel join workers |
| `BOT_STATUS` | No | Emorce Tokens | Activity text |
| `BOT_ACTIVITY` | No | Watching | Playing/Watching/Listening/Competing |
| `DATA_DIR` | No | ./data | Token storage path |

---

## File Structure

```
emorce-py/
├── requirements.txt
├── railway.toml
├── .env.example
├── README.md
├── data/
│   └── tokens.txt          # token storage
└── src/
    ├── main.py             # main entry
    ├── commands/
    │   ├── __init__.py
    │   ├── token.py        # /token commands
    │   ├── joiner.py       # /emorce commands
    │   └── bot.py          # /bot commands
    └── utils/
        ├── __init__.py
        ├── token_manager.py
        ├── joiner.py
        └── permissions.py
```

---

## Troubleshooting

| Problem | Fix |
|---------|-----|
| Commands don't appear | Wait 1 min or restart bot |
| "Only bot owners…" | Add your user ID to `OWNER_IDS` |
| Joiner says no tokens | Use `/token log` first |
| Tokens disappear | Add Railway Volume at `/data` |
| Rate limited | Increase `JOIN_DELAY_MS` to 1500+ |
| Bot doesn't start | Check DISCORD_TOKEN in Railway |

---

**Emorce** — built for Axion.
