# Complete Discord Developer Portal Setup Guide

Step-by-step with screenshots description for Emorce Token Bot.

---

## Step 1: Create a Discord Application

1. Open https://discord.com/developers/applications
2. Click the **New Application** button (top right)
3. Enter a name: `Emorce Live` (or whatever you want)
4. Accept the Developer Terms of Service
5. Click **Create**

You're now in your application dashboard.

---

## Step 2: Create a Bot User

1. Left sidebar, click **Bot**
2. Click **Add Bot** button
3. Click **Yes, do it!** to confirm

You now have a bot user. You should see the bot's avatar and name.

---

## Step 3: Get Your Bot Token

1. Under your bot name, you should see **TOKEN**
2. Click **Reset Token** → **Yes, do it!**
3. Click **Copy** (next to the token)
4. Paste this somewhere safe — this is your `DISCORD_TOKEN`

⚠️ **Never share this token with anyone.**

---

## Step 4: Enable Message Content Intent

This allows the bot to read message content (needed for some features).

1. Scroll down to **Privileged Gateway Intents**
2. Toggle **Message Content Intent** to ON
3. Click **Save Changes**

---

## Step 5: Generate Invite URL

This is how you invite the bot to your server.

1. Left sidebar, click **OAuth2** → **URL Generator**
2. Under **SCOPES**, check:
   - ✓ `bot`
   - ✓ `applications.commands`
3. Under **BOT PERMISSIONS**, check:
   - ✓ `Send Messages`
   - ✓ `Embed Links`
   - ✓ `Attach Files`
   - ✓ `Use Application Commands`
4. Scroll to bottom → **Generated URL**
5. Copy the URL

---

## Step 6: Invite the Bot to Your Server

1. Open the copied URL in a new browser tab
2. Discord will ask you to authorize
3. Select the server you want the bot in (from dropdown)
4. Click **Authorize**

The bot is now in your server! Go to Discord and you should see your bot user in the member list.

---

## Step 7: Get Your Application ID

1. Left sidebar, click **General Information**
2. Copy **Application ID** (also called Client ID)
3. Save this (you'll need it if registering commands via CLI later)

---

## Step 8: Get Your Discord User ID

1. In Discord, go to **User Settings** → **Advanced**
2. Toggle **Developer Mode** ON
3. Go back to any server
4. Right-click your own username → **Copy User ID**
5. Save this as `OWNER_IDS` in your `.env`

---

## Creating .env File

Now you have all the info. Create a file named `.env` in the bot folder:

```env
DISCORD_TOKEN=your_bot_token_here
OWNER_IDS=your_user_id_here
LOCKED_CHANNEL_ID=
JOIN_DELAY_MS=800
MAX_CONCURRENT_JOINS=5
BOT_STATUS=Emorce Tokens
BOT_ACTIVITY=Watching
DATA_DIR=./data
```

Replace:
- `your_bot_token_here` with the token you copied in Step 3
- `your_user_id_here` with your Discord user ID from Step 8

---

## Testing Locally (Optional)

```bash
pip install -r requirements.txt
python src/main.py
```

In Discord, type `/` and you should see all bot commands appear.

---

## Railway Deploy

Once you're happy locally:

1. Create a private GitHub repo
2. Push the bot folder
3. Go to https://railway.app
4. Create new project from GitHub
5. Add environment variables (same as your `.env`)
6. Deploy

That's it! The bot will auto-sync commands and be ready to use.

---

## Permissions Recap

- **OWNER_IDS**: Comma-separated Discord user IDs who can use ALL commands
  Example: `123456789,987654321`
- **LOCKED_CHANNEL_ID**: (Optional) If set, ALL slash commands only work in this channel
  - Find channel ID: Right-click channel → Copy Channel ID

---

**You're all set!**

Invite your server owner(s) and they can use `/token log` to start adding tokens.
