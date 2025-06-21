import os
import requests
import random
from dotenv import load_dotenv
from PIL import Image, ImageDraw, ImageFont
import logging
from io import BytesIO
import os
import json


BASE_DIR = os.path.dirname(os.path.abspath(__file__))

# Load environment variables from .env file
load_dotenv()

# Set up logging for better error tracking
logging.basicConfig(filename='post_quote.log', level=logging.INFO)

# Load the Facebook token from the environment variable
access_token = os.getenv('FB_ACCESS_TOKEN')

# Your correct Facebook Page ID
page_id = os.getenv('FB_PAGE_ID')

# Pexels API Key
pexels_api_key = os.getenv('PEXELS_API_KEY')  # Ensure you store this in your .env file


def fetch_random_story():
    url = 'https://short-story-api.onrender.com/api/short_stories/random?exclude='
    exclude_file = os.path.join(BASE_DIR, "exclude_id_story.txt")
    # Load excluded IDs
    try:
        with open(exclude_file, "r", encoding="utf-8") as f:
            exclude_ids = {int(line.strip()) for line in f if line.strip().isdigit()}
    except FileNotFoundError:
        exclude_ids = set()

    params = ",".join(map(str, exclude_ids))

    try:
        # Make the GET request
        response = requests.get(url+params, verify=True)

        if response.status_code == 200:
            data = response.json()
            return (
                    data["id"],
                    data["title"],
                    data["content"],
                    data["theme"],
                    data["genre"],
                    data["moral_lesson"]
                )
        else:
            logging.error(f"Failed to fetch quote: {response.status_code}")
            return "Default fallback quote.", "Unknown author"
    except Exception as e:
        logging.error(f"Error fetching quote: {str(e)}")
        return "Default fallback story.", "Unknown author"


def fetch_background_image(query="nature"):
    page = random.randint(1, 10)  # Random page number between 1 and 10
    url = f"https://api.pexels.com/v1/search?query={query}&page={page}&per_page=15"  # 15 images per page

    headers = {
        'Authorization': pexels_api_key
    }

    try:
        response = requests.get(url, headers=headers)

        if response.status_code == 200:
            data = response.json()
            random_image = random.choice(data['photos'])  # Select a random image from the returned photos
            image_url = random_image['src']['original']  # Get the URL of the random image
            return image_url
        else:
            logging.error(f"Failed to fetch background image: {response.status_code}")
            return None
    except Exception as e:
        logging.error(f"Error fetching background image: {str(e)}")
        return None


def download_image(url):
    try:
        response = requests.get(url)
        if response.status_code == 200:
            image = Image.open(BytesIO(response.content))
            return image
        else:
            logging.error(f"Failed to download image: {response.status_code}")
            return None
    except Exception as e:
        logging.error(f"Error downloading image: {str(e)}")
        return None
    

def wrap_text(text, font, draw, max_width):
    lines = []
    words = text.split(' ')
    line = ""

    for word in words:
        # Try adding the word to the line
        test_line = line + " " + word if line else word
        # Get the bounding box (bbox) of the text
        bbox = draw.textbbox((0, 0), test_line, font=font)
        width = bbox[2] - bbox[0]  # bbox[2] is the right side, bbox[0] is the left side

        # If the line exceeds max_width, add the current line to lines and start a new one
        if width <= max_width:
            line = test_line
        else:
            lines.append(line)
            line = word

    # Add the last line
    if line:
        lines.append(line)

    return lines


def generate_image_with_moral(title, moral_lesson, theme):
    # --- 1. Background sourcing (unchanged) ---------------------------------
    background_url = fetch_background_image(theme)
    if background_url and (img := download_image(background_url)):
        background_image = img
    else:
        background_image = Image.new("RGB", (800, 400), (255, 255, 255))

    width, height = background_image.size

    # semi‑transparent dark overlay for legibility
    overlay = Image.new("RGBA", (width, height), (0, 0, 0, 128))
    background_image.paste(overlay, (0, 0), overlay)

    draw = ImageDraw.Draw(background_image)

    # --- 2. Two fonts (quote big, title smaller) -----------------------------
    font_path = os.path.join(BASE_DIR, "PlayfairDisplay-VariableFont_wght.ttf")
    try:
        quote_font = ImageFont.truetype(font_path, 200)   # 200 pt for the quote
        title_font = ImageFont.truetype(font_path, 120)   # 120 pt for the title  # <<<
    except IOError:                                       # font fallback
        quote_font = title_font = ImageFont.load_default()

    text_color = (255, 255, 255)
    padding = 30
    max_w = width - 2 * padding
    block_spacing = 20

    # --- 3. Prepare and wrap each block separately ---------------------------
    quote_text  = f'"{moral_lesson}"'
    title_text  = f'({title})'

    quote_lines = wrap_text(quote_text, quote_font, draw, max_w)
    title_lines = wrap_text(title_text, title_font, draw, max_w)

    # --- 4. Compute total height for perfect vertical centering --------------
    def line_h(line, fnt):
        bbox = draw.textbbox((0, 0), line, font=fnt)
        return bbox[3] - bbox[1]

    total_h = sum(line_h(l, quote_font) for l in quote_lines) + \
              sum(line_h(l, title_font) for l in title_lines)

    y = (height - total_h) // 2

    # --- 5. Draw the quote (big) then the title (small) ----------------------
    for line in quote_lines:
        w = draw.textlength(line, font=quote_font)
        draw.text(((width - w) // 2, y), line, font=quote_font, fill=text_color)
        y += line_h(line, quote_font)

    y += block_spacing

    for line in title_lines:
        w = draw.textlength(line, font=title_font)
        draw.text(((width - w) // 2, y), line, font=title_font, fill=text_color)
        y += line_h(line, title_font)

    # --- 6. Return PNG as BytesIO -------------------------------------------
    output = BytesIO()
    background_image.save(output, format="PNG")
    output.seek(0)
    return output



def get_random_hashtags():
    hashtags = [
        # Story and literature
        "#ShortStory", "#BedtimeTales", "#StoryTime", "#MiniFiction", "#FlashFiction",
        "#ReadEveryday", "#FictionLovers", "#StoryOfTheDay", "#KidsStory", "#Storytelling",

        # Emotions & themes
        "#FeelGoodStory", "#WholesomeRead", "#InspiringTales", "#Heartwarming", "#LifeLessons",

        # Audience
        "#ForTheKids", "#ChildrensBooks", "#YoungReaders", "#MoralStories", "#ParentingTips",

        # Trending/general
        "#DailyReads", "#PositiveVibes", "#RainyDayReads", "#MindfulParenting", "#ImaginationTime"
    ]

    return ' '.join(random.sample(hashtags, 5))



# Function to upload the image to Facebook
def upload_image_to_facebook(image_stream, id, title, content, genre, theme, moral_lesson):
    url = f'https://graph.facebook.com/{page_id}/photos'
    payload = {
        'access_token': access_token,
        'message': f'{title} ({genre}, {theme}) \n\n{content}\n\n\nMoral Lesson: {moral_lesson}   \n\n #{genre.replace(" ","_")} #{theme.replace(" ", "_")} {get_random_hashtags()}'
    }

    files = {
        'file': ('quote_image.png', image_stream, 'image/png')
    }

    response = requests.post(url, data=payload, files=files)

    if response.status_code == 200:
        with open(os.path.join(BASE_DIR, "exclude_id_story.txt"), "a", encoding="utf-8") as f:
            f.write(f"{id}\n") 
        logging.info("Successfully uploaded the quote image to Facebook")
    else:
        logging.error(f"Failed to upload image: {response.text}")

# Fetch a random quote from the API
id, title, content, theme, genre, moral_lesson  = fetch_random_story()

# Generate the image with the quote and background
image_stream = generate_image_with_moral(title, moral_lesson, theme)

# Upload the image to Facebook


def post_short_story():
    if(id and image_stream):
        print("Now uploading short story...")
        upload_image_to_facebook(image_stream, id,  title, content, genre, theme, moral_lesson)
        print("Short Story uploaded!")