# AI Employee Vault - Web UI

Beautiful black and golden Next.js UI for the AI Employee Vault platform. Production-ready for Vercel deployment.

## Features

- 🎨 Beautiful black and golden design
- ⚡ Built with Next.js 14+
- 📱 Fully responsive (mobile, tablet, desktop)
- 🚀 Optimized for Vercel deployment
- 🔄 Real-time stats API integration
- ♿ Accessible components
- 🎯 Smooth animations and transitions

## Quick Start

### Development

```bash
npm install
npm run dev
```

Open [http://localhost:3000](http://localhost:3000) in your browser.

### Production Build

```bash
npm run build
npm start
```

## Deployment to Vercel

### Option 1: Using Vercel CLI

```bash
npm install -g vercel
vercel
```

### Option 2: GitHub Integration

1. Push this folder to GitHub
2. Go to [vercel.com](https://vercel.com)
3. Import the repository
4. Select the `web-ui` directory as root
5. Deploy

### Option 3: Direct Upload

```bash
vercel --prod
```

## Project Structure

```
web-ui/
├── app/
│   ├── api/
│   │   └── stats/
│   │       └── route.js
│   ├── components/
│   │   ├── Header.js
│   │   ├── Hero.js
│   │   ├── Stats.js
│   │   ├── Features.js
│   │   ├── Platforms.js
│   │   ├── Metrics.js
│   │   ├── Actions.js
│   │   ├── Footer.js
│   │   └── *.css
│   ├── globals.css
│   ├── layout.js
│   ├── page.js
│   └── page.css
├── public/
├── next.config.js
├── package.json
├── vercel.json
└── .gitignore
```

## Environment Variables

Create a `.env.local` file for local development:

```
NEXT_PUBLIC_API_URL=http://localhost:3000
```

## Components

- **Header**: Navigation and status badge
- **Hero**: Main landing section with CTA buttons
- **Stats**: Key metrics display
- **Features**: Core features grid
- **Platforms**: Connected platforms showcase
- **Metrics**: System performance metrics
- **Actions**: Call-to-action buttons
- **Footer**: Links and information

## Styling

All components use CSS modules with a consistent black (#0a0e27, #1a1f3a) and golden (#d4af37, #f0e68c) color scheme.

## API Routes

- `GET /api/stats` - Returns system statistics

## Browser Support

- Chrome (latest)
- Firefox (latest)
- Safari (latest)
- Edge (latest)

## License

© 2026 AI Employee Vault. All rights reserved.
