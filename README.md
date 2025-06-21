# AutoQuotePoster

AutoQuotePoster is a Python automation script that fetches inspirational quotes and short stories, generates background images using the Pexels API, and posts the final output to a Facebook Page. It’s perfect for maintaining consistent and engaging social media content without manual effort.

The project is hosted on [Render](https://render.com) and posts automatically every day at **6 AM and 6 PM Philippine Time**.

---

## 🔑 Features

- 📝 Fetches quotes and short stories dynamically
- 🖼️ Uses royalty-free images from Pexels for backgrounds
- 🧠 Automatically overlays text onto images using Pillow
- 📤 Posts directly to Facebook via Graph API
- 🕑 Scheduled posting (2x daily)
- ☁️ Can be hosted on Render or PythonAnywhere (Free Tier)

---

## 🚀 Setup Instructions

### 1. Clone the repository

```bash
git clone https://github.com/johnandrewsanvictores/AutoQuotePoster.git
cd AutoQuotePoster
```

### 2. Install dependencies

```bash
pip install -r requirements.txt
```

### 3. Add your environment variables

Create a `.env` file in the project root with the following keys:

```env
FB_PAGE_ID=your_facebook_page_id
FB_PAGE_TOKEN=your_long_lived_facebook_page_token
PEXELS_API_KEY=your_pexels_api_key
```

### 4. Run the script manually

```bash
python main.py
```

---

## ☁️ Deploying on Render (Free)

### A. Prerequisites
- A [Render account](https://render.com/)
- Your code pushed to a public or private GitHub repo

### B. Steps

1. Go to [Render Cron Jobs](https://dashboard.render.com/new/cron)
2. Set the job name: `AutoQuotePoster`
3. Pick your repo and branch
4. Set the **Start Command**:

```bash
python post_quotes.py
```

5. Set the **Schedule** to:

```bash
0 22,10 * * * 
```

🕘 This means 6 AM & 6 PM Philippine Time (UTC+8)

6. Set environment variables in the **Environment** tab:
    - `FB_PAGE_ID`
    - `FB_PAGE_TOKEN`
    - `PEXELS_API_KEY`

7. Click **Create Cron Job**

That’s it—Render will now run your script twice a day.

---

## 📦 Requirements

Listed in `requirements.txt`:

```
requests
python-dotenv
pillow
```

Install with:

```bash
pip install -r requirements.txt
```

---

## 📌 Notes

- Facebook tokens must be valid and long-lived
- Pexels API has daily request limits depending on your plan
- Use appropriate font sizes and image resolutions for best Facebook post quality
- `.env` file should never be committed — add it to `.gitignore`

---
