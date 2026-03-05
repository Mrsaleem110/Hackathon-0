# LinkedIn Agentic Sphere - Create Post Button Setup

## Quick Setup (2 minutes)

### Step 1: Install Tampermonkey
1. Go to your browser's extension store:
   - **Chrome**: https://chrome.google.com/webstore/detail/tampermonkey/dhdgffkkebhmkfjojejmpbldmpobp55f
   - **Firefox**: https://addons.mozilla.org/en-US/firefox/addon/tampermonkey/
   - **Edge**: https://microsoftedge.microsoft.com/addons/detail/tampermonkey/iikmkjmpaadaobahmlepeloendndfohd
2. Click "Add to [Browser]"
3. Confirm the installation

### Step 2: Add the Userscript
1. Click the **Tampermonkey icon** in your browser toolbar
2. Select **"Create a new script"**
3. Delete the default template
4. Copy and paste the entire content from `linkedin_create_post_button.js`
5. Press **Ctrl+S** to save
6. The script is now active!

### Step 3: Test It
1. Go to: https://www.linkedin.com/company/agentic-sphere/
2. You should see a **"✨ Create Post"** button appear at the top
3. Click it to open the post editor

## What It Does

- ✅ Adds a stylish purple button to your Agentic Sphere page
- ✅ Automatically finds and clicks LinkedIn's native "Create a post" button
- ✅ Works every time you visit the page
- ✅ No installation or setup required beyond Tampermonkey

## Customization

Want to change the button style? Edit these lines in the script:

```javascript
// Change button text
button.textContent = '✨ Create Post';

// Change button color (gradient)
background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);

// Change button size
font-size: 14px;
padding: 8px 16px;
```

## Troubleshooting

**Button doesn't appear?**
- Make sure Tampermonkey is enabled
- Check that you're on the Agentic Sphere company page
- Refresh the page (F5)

**Button doesn't work?**
- LinkedIn's page structure may have changed
- Try clicking the native "Create a post" button manually
- Update the script with new selectors if needed

## Alternative: Browser Extension

If you want a more permanent solution, you can convert this to a full Chrome extension. Let me know if you'd like that!
