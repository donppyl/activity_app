# 🎉 FamilyFun Hub

A fun, interactive family activity app built with Streamlit!

## Features

- 🎯 **Activity Picker** — Spin for a random family activity or browse 15+ curated activities
- 🧹 **Chore Chart** — Assign chores, track completion, and earn points
- 🧠 **Trivia Time** — Fun quiz questions in Easy/Medium/Hard difficulty
- ⏱️ **Family Timer** — Countdown timer for games and activities
- 👥 **Family Setup** — Customize your family members and reset weekly stats

## Run Locally

```bash
pip install -r requirements.txt
streamlit run app.py
```

Then open http://localhost:8501

## Deploy to Streamlit Community Cloud (Free!)

1. Push this folder to a GitHub repository
2. Go to https://share.streamlit.io
3. Sign in with GitHub
4. Click "New app" → select your repo → set `app.py` as the main file
5. Click "Deploy!" — your app will be live in minutes!

## Deploy to Other Platforms

### Heroku
```bash
# Add a Procfile:
echo "web: streamlit run app.py --server.port $PORT --server.address 0.0.0.0" > Procfile
git push heroku main
```

### Railway / Render
- Connect your GitHub repo
- Set start command: `streamlit run app.py --server.port $PORT --server.address 0.0.0.0`

No database or external services needed — all state is stored in Streamlit session state!
