# 🔑 Create GitHub Personal Access Token - Step by Step

Follow these exact steps to create your token:

## Step 1: Open GitHub Settings

1. **Open this link in your browser:**
   👉 https://github.com/settings/tokens

2. You'll see "Personal access tokens" page

## Step 2: Generate New Token

1. Click the **"Generate new token"** button (top right)
2. You'll see two options:
   - **"Generate new token (classic)"** ← Choose this one
   - "Generate new token (fine-grained)"

3. Click **"Generate new token (classic)"**

## Step 3: Configure Token

You'll see a form. Fill it out like this:

### Note (Description)
```
Fire Prediction System Deployment
```
(This is just a label for you to remember what the token is for)

### Expiration
- Select: **90 days** (or "No expiration" if you prefer)

### Select Scopes (IMPORTANT!)
Check ONLY these boxes:

✅ **repo** (check the main "repo" box - this will auto-check all sub-items)
   - ✅ repo:status
   - ✅ repo_deployment
   - ✅ public_repo
   - ✅ repo:invite
   - ✅ security_events

That's it! Don't check anything else.

## Step 4: Generate Token

1. Scroll to the bottom
2. Click the green **"Generate token"** button

## Step 5: Copy Your Token

⚠️ **VERY IMPORTANT:**

1. You'll see a green box with your token (starts with `ghp_`)
2. **COPY IT IMMEDIATELY** - you'll only see it once!
3. It looks like: `ghp_xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx`

📋 **Copy the entire token** (click the copy icon next to it)

## Step 6: Come Back Here

Once you have copied your token:
1. Keep it safe (don't share it publicly)
2. Paste it back here so I can use it to push your code
3. The token will only be used once and won't be saved anywhere public

---

## ⚠️ Security Note

- This token gives access to your repositories
- Don't share it in public places
- It will only be stored in your local git config
- You can always revoke it later at: https://github.com/settings/tokens

---

## 🆘 Troubleshooting

**Can't find the page?**
- Make sure you're logged into GitHub
- Try this direct link: https://github.com/settings/tokens/new

**Don't see "Generate new token" button?**
- You might need to verify your password first
- GitHub may ask for 2FA if you have it enabled

---

Ready? Go create your token and paste it here! 🚀
