# FPL AI Recommender 🤖⚽

An automated Fantasy Premier League recommendation system powered by AI that generates weekly captain picks, differential suggestions, and transfer advice.

## 🚀 Features

- **AI-Powered Recommendations**: Uses Groq's Gemma 2 9B model for intelligent FPL advice
- **Automated Updates**: GitHub Actions runs weekly before the FPL deadline
- **Static Site**: Lightning-fast Vue.js frontend deployed on Vercel
- **Zero Cost**: Completely free using free tiers of all services

## 🛠️ Tech Stack

- **Backend**: Python + FPL API + Groq Cloud
- **Frontend**: Vue.js 3 + Vite
- **Automation**: GitHub Actions
- **Hosting**: Vercel
- **AI Model**: Gemma 2 9B (via Groq)

## 📦 Project Structure

```
fpl-recommender/
├── .github/workflows/    # GitHub Actions automation
├── data/                 # AI recommendations (picks.json)
├── scripts/              # Python data fetching & AI logic
├── src/                  # Vue.js frontend
│   ├── components/       # Vue components
│   └── App.vue           # Main app
├── public/               # Static assets
└── index.html            # Entry point
```

## 🔧 Setup Instructions

### 1. Prerequisites

- Node.js (v18+)
- Python (3.11+)
- GitHub account
- Groq API account (free)
- Vercel account (free)

### 2. Local Development

```bash
# Install Node dependencies
npm install

# Install Python dependencies
cd scripts
pip install -r requirements.txt

# Run Vue dev server
npm run dev

# Test Python script locally
cd scripts
python main.py
```

### 3. Get Groq API Key

1. Visit [Groq Console](https://console.groq.com/)
2. Sign up and create an API key
3. Save it for the next step

### 4. GitHub Setup

```bash
# Initialize Git
git init
git add .
git commit -m "Initial commit"

# Create repo on GitHub and push
git remote add origin https://github.com/YOUR_USERNAME/fpl-recommender.git
git branch -M main
git push -u origin main
```

### 5. Add GitHub Secret

1. Go to your GitHub repo
2. Settings → Secrets and variables → Actions
3. Click "New repository secret"
4. Name: `GROQ_API_KEY`
5. Value: [Your Groq API key]

### 6. Deploy to Vercel

1. Visit [Vercel](https://vercel.com)
2. Import your GitHub repository
3. Configure:
    - **Framework**: Vite
    - **Build Command**: `npm run build`
    - **Output Directory**: `dist`
4. Deploy!

## 🤖 How It Works

1. **Every Friday at 18:00 UTC**, GitHub Actions triggers
2. Python script fetches latest FPL data
3. Sends data to Groq API (Gemma 2 9B model)
4. AI generates recommendations in JSON format
5. Saves to `data/picks.json`
6. Changes are committed and pushed
7. Vercel auto-deploys with fresh data

## 📊 What You Get

- ⭐ **Captain Pick**: Best captain choice with reasoning
- 💎 **Differential**: Low-owned player with high potential
- 📈 **Transfers In**: Players to consider adding
- 📉 **Transfers Out**: Players to consider removing
- 💡 **General Advice**: Overall gameweek strategy

## 🔄 Manual Trigger

You can manually trigger the workflow:

1. Go to your GitHub repo
2. Actions tab
3. Select "Update FPL Picks"
4. Click "Run workflow"

## 📝 Customization

### Change Schedule

Edit [.github/workflows/update_fpl.yml](.github/workflows/update_fpl.yml):

```yaml
schedule:
    - cron: "0 18 * * 5" # Change this line
```

### Modify AI Prompt

Edit [scripts/main.py](scripts/main.py) to change what the AI analyzes.

### Styling

Edit Vue components in [src/components](src/components) and [src/App.vue](src/App.vue).

## 🚨 Troubleshooting

**Workflow not running?**

- Check if `GROQ_API_KEY` secret is set
- Verify GitHub Actions is enabled for your repo

**Data not updating?**

- Check Actions tab for error logs
- Verify Groq API key is valid

**Site not deploying?**

- Check Vercel dashboard for build logs
- Ensure `package.json` scripts are correct

## 📄 License

MIT License - Feel free to use and modify!

## 🙏 Credits

- FPL API: https://fantasy.premierleague.com/api/
- Groq Cloud: https://groq.com/
- Vue.js: https://vuejs.org/

---

**Made with ⚽ for FPL managers**
