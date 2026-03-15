# How to Get Instagram & Facebook Credentials

## Instagram Credentials

### Option 1: Business Account (Recommended)

1. Go to https://business.facebook.com/
2. Log in with your Facebook account
3. Click **Settings** (bottom left) → **Apps and Websites**
4. Click **Add Apps**
5. Search for "Instagram" and add the Instagram app
6. Go to **Roles** → **Assign Users** to get your Business Account ID
7. Generate an **Access Token**:
   - Settings → Apps and Websites → Instagram
   - Click **Generate Token**
   - Copy the token (starts with `IGAB_...`)

**What you need:**
- `INSTAGRAM_ACCESS_TOKEN` - The token you generated
- `INSTAGRAM_BUSINESS_ACCOUNT_ID` - Your Instagram business account ID (numeric)

### Option 2: Personal Account

1. Go to https://developers.facebook.com/
2. Create a new app (type: **Business**)
3. Add **Instagram Basic Display** product
4. In Settings → Basic, copy your **App ID**
5. Generate an access token with `instagram_basic` scope
6. Get your Instagram account ID from your profile

---

## Facebook Credentials

1. Go to https://developers.facebook.com/
2. Create a new app (type: **Business**)
3. Add **Facebook Login** product
4. Go to **Settings → Basic** and copy your **App ID** and **App Secret**
5. Create a Page Access Token:
   - Go to **Tools → Access Token Generator**
   - Select your Facebook page
   - Generate token with these scopes:
     - `pages_manage_posts`
     - `pages_read_engagement`
6. Copy the token (starts with `EAAB...`)

**What you need:**
- `FACEBOOK_ACCESS_TOKEN` - The page access token
- `FACEBOOK_PAGE_ID` - Your Facebook page ID (numeric)

---

## Quick Reference

| Credential | Where to Find | Format |
|-----------|---------------|--------|
| INSTAGRAM_ACCESS_TOKEN | Facebook Business Manager | Starts with `IGAB_` or `EAAB_` |
| INSTAGRAM_BUSINESS_ACCOUNT_ID | Instagram Settings | Numeric ID |
| FACEBOOK_ACCESS_TOKEN | Facebook Developers | Starts with `EAAB_` |
| FACEBOOK_PAGE_ID | Facebook Page Settings | Numeric ID |

---

## Once You Have Credentials

1. Open `.env` file in this directory
2. Replace these lines:
   ```
   INSTAGRAM_ACCESS_TOKEN=your_instagram_access_token_here
   INSTAGRAM_BUSINESS_ACCOUNT_ID=your_business_account_id_here
   FACEBOOK_ACCESS_TOKEN=your_facebook_access_token_here
   FACEBOOK_PAGE_ID=your_facebook_page_id_here
   ```

3. With your actual credentials:
   ```
   INSTAGRAM_ACCESS_TOKEN=IGAB_xxxxxxxxxxxx
   INSTAGRAM_BUSINESS_ACCOUNT_ID=123456789
   FACEBOOK_ACCESS_TOKEN=EAAB_xxxxxxxxxxxx
   FACEBOOK_PAGE_ID=987654321
   ```

4. Save the file

5. Test with:
   ```bash
   python config.py
   ```

---

## Troubleshooting

**Token expired?**
- Regenerate from Facebook Business Manager or Developers portal

**Can't find Business Account ID?**
- Go to Instagram Settings → Account → Business Account ID

**Permission denied errors?**
- Make sure token has correct scopes: `pages_manage_posts`, `pages_read_engagement`

**Still having issues?**
- Check that your app is in Development or Live mode
- Verify your Facebook page is connected to your app
