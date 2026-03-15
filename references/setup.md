# Setup Guide

## Installation

```bash
uv sync
```

## Authentication

### Option A: Automatic Login (Recommended)

```bash
uv run gemini-web auth login
```

This starts Chrome in debugging mode with a persistent profile at `~/Library/Application Support/gemini-web/chrome-profile/` (macOS).

**For AI Agents**: When the program shows "登录完成后，按 Enter 键自动获取 Cookie...":
1. Wait for Chrome to open
2. Tell user: "Chrome has opened. Please login to Gemini, then tell me when you're done."
3. When user confirms, send Enter: `process(action=write, data="\n", sessionId=<session_id>)`

### Option B: Manual Cookie Configuration

1. Open Chrome → https://gemini.google.com
2. Login to your Google account
3. DevTools (F12) → Application → Cookies → https://gemini.google.com
4. Copy these cookies:
   - `__Secure-1PSID`
   - `__Secure-1PSIDTS`
5. Create config:

```bash
mkdir -p ~/.config/gemini-web
cat > ~/.config/gemini-web/cookies.json << 'EOF'
{
  "secure_1psid": "YOUR_PSID_VALUE",
  "secure_1psidts": "YOUR_PSIDTS_VALUE"
}
EOF
```

Replace with actual cookie values from browser.

## Best Practice: Incognito Mode

For longer-lasting cookies:
1. Open Chrome Incognito
2. Visit https://gemini.google.com and login
3. Get cookies
4. Close Incognito immediately
5. Cookies last weeks instead of hours

Reference: https://github.com/HanaokaYuzu/Gemini-API/issues/6

## Data Directories

- Config: `~/.config/gemini-web/cookies.json`
- Sessions: `~/Library/Application Support/gemini-web/sessions.db`
- Images: `~/Library/Application Support/gemini-web/images/`
