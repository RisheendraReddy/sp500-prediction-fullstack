# Navigation Troubleshooting

## Issue: Links Not Working

If clicking navigation links doesn't change pages, try these solutions:

## Solution 1: Hard Refresh

Clear browser cache:
- **Mac**: Cmd + Shift + R
- **Windows/Linux**: Ctrl + Shift + R

## Solution 2: Check Browser Console

1. Open DevTools (F12)
2. Go to Console tab
3. Click a navigation link
4. Look for errors

Common errors:
- `Cannot read property 'pathname' of undefined` → Router issue
- `Module not found` → Import issue
- `Cannot read property 'map' of undefined` → Component issue

## Solution 3: Verify React Router

Check if react-router-dom is installed:
```bash
npm list react-router-dom
```

If not installed:
```bash
npm install react-router-dom
```

## Solution 4: Use HashRouter (Alternative)

If BrowserRouter doesn't work, switch to HashRouter:

1. In `src/App.jsx`, change:
   ```jsx
   import { BrowserRouter as Router, ... } from 'react-router-dom'
   ```
   to:
   ```jsx
   import { HashRouter as Router, ... } from 'react-router-dom'
   ```

2. URLs will use `#` (e.g., `http://localhost:3000/#/train`)

## Solution 5: Restart Dev Server

1. Stop the server (Ctrl+C)
2. Clear cache:
   ```bash
   rm -rf node_modules/.vite
   ```
3. Restart:
   ```bash
   npm run dev
   ```

## Solution 6: Check File Imports

Verify all page files exist:
```bash
ls src/pages/
```

Should show:
- Home.jsx
- Train.jsx
- Predict.jsx
- Models.jsx

## Solution 7: Add Debug Logging

The updated App.jsx now includes console.log when clicking links.
Check browser console to see if clicks are registered.

## Quick Test

1. Open browser console (F12)
2. Click "Train Model" link
3. Check console for: "Navigating to: /train"
4. Check URL bar - should change to `/train`

If you see the log but URL doesn't change → Router issue
If you don't see the log → Click event not firing

## Still Not Working?

Try the alternative App.jsx:
1. Rename current: `mv src/App.jsx src/App-browser.jsx`
2. Use alternative: `mv src/App-alternative.jsx src/App.jsx`
3. Restart dev server

