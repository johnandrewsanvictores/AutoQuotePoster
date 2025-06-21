# AutoQuotePoster

AutoQuotePoster is a Python automation script that fetches inspirational quotes and short stories, generates background images using the Pexels API, and posts the final output to a Facebook Page. It’s perfect for maintaining consistent and engaging social media content without manual effort.

The project is hosted on PythonAnywhere (Free Tier) and posts automatically every day at **6 AM and 6 PM Philippine Time**.

---

## 🔑 Features

- 📝 Fetches quotes and short stories dynamically
- 🖼️ Uses royalty-free images from Pexels for backgrounds
- 🧠 Automatically overlays text onto images using Pillow
- 📤 Posts directly to Facebook via Graph API
- 🕑 Scheduled posting (2x daily)
- ☁️ Can be hosted on PythonAnywhere (Free Tier)

---

## 🚀 Setup Instructions

### 1. Clone the repository

```bash
git clone https://github.com/johnandrewsanvictores/AutoQuotePoster.git
cd AutoQuotePoster
```

### 2. Install dependencies

On PythonAnywhere, open a Bash console and run:

```bash
pip3 install --user -r requirements.txt
```

### 3. Add your environment variables

Create a `.env` file in the project root with:

```env
FB_PAGE_ID=your_facebook_page_id
FB_PAGE_TOKEN=your_long_lived_facebook_page_token
PEXELS_API_KEY=your_pexels_api_key
```

Ensure this file is created in the directory where your `main.py` or `post_quotes.py` resides.

### 4. Run the script manually (for testing)

```bash
python3 main.py
```

---

## ☁️ Deploying on PythonAnywhere (Free)

### A. Schedule the task

1. Go to **Tasks** in the PythonAnywhere dashboard.
2. Click **Add a new scheduled task**.
3. Set the command:

```bash
cd /home/yourusername/AutoQuotePoster && python3 main.py
```

4. Set time:

- Add one task for `6:00` (AM)
- Add another for `18:00` (6 PM)

Make sure the time zone in your PythonAnywhere account is set to UTC+8 (Philippine Time) or adjust times accordingly.

5. Save both tasks.

### B. Notes

- Ensure your `.env` file stays in the correct directory.
- If you update code, pull latest changes:

```bash
cd /home/yourusername/AutoQuotePoster
git pull
```

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
pip3 install --user -r requirements.txt
```

---

## 📌 Notes

- Facebook tokens must be valid and long-lived.
- Pexels API has daily request limits depending on your plan.
- Use appropriate font sizes and image resolutions for best Facebook post quality.
- `.env` file should never be committed — add it to `.gitignore`.
