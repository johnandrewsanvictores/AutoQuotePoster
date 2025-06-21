import os
import requests
import random
from dotenv import load_dotenv
from PIL import Image, ImageDraw, ImageFont
import logging
from io import BytesIO

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

# Function to fetch a random quote from the API
def fetch_random_quote():
    url = 'https://zenquotes.io/api/quotes'

    try:
        # Make the GET request
        response = requests.get(url, verify=True)

        if response.status_code == 200:
            data = response.json()
            quote_data = random.choice(data)  # Select a random quote from the list
            quote = quote_data['q']
            author = quote_data['a']
            return quote, author  # Return both quote and author
        else:
            logging.error(f"Failed to fetch quote: {response.status_code}")
            return "Default fallback quote.", "Unknown author"
    except Exception as e:
        logging.error(f"Error fetching quote: {str(e)}")
        return "Default fallback quote.", "Unknown author"

# Function to fetch a background image from Pexels with random page and random index
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

# Function to download an image from URL
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

# Function to wrap text to fit in the image
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

# Function to generate an image with the quote text and a background
def generate_image_with_quote(quote, author):
    # Fetch a background image from Pexels (e.g., nature)
    background_url = fetch_background_image("nature")  # Customize the query as needed

    if background_url:
        background_image = download_image(background_url)
        if background_image:
            width, height = background_image.size
        else:
            # Fallback to a solid color if the image can't be fetched
            width, height = 800, 400
            background_image = Image.new('RGB', (width, height), (255, 255, 255))  # White background
    else:
        width, height = 800, 400
        background_image = Image.new('RGB', (width, height), (255, 255, 255))  # White background

    # Add black overlay for text contrast
    overlay = Image.new('RGBA', (width, height), (0, 0, 0, 128))  # Semi-transparent black
    background_image.paste(overlay, (0, 0), overlay)  # Apply overlay on top of the background

    # Create a draw object
    draw = ImageDraw.Draw(background_image)

    # Font settings (you can change the font and size)
    try:
        font_path = os.path.join(os.path.dirname(__file__), "PlayfairDisplay-VariableFont_wght.ttf")
        font = ImageFont.truetype(font_path, 200)  # Set the font size to 200
    except IOError:
        font = ImageFont.load_default()

    # Text settings
    text_color = (255, 255, 255)  # White text to stand out on dark images
    padding = 30  # Padding around the text

    # Prepare the quote text with triple quotes and the author
    full_text = f'" {quote} "\n- {author}\n'

    # Wrap the text to fit within the image width
    wrapped_lines = wrap_text(full_text, font, draw, width - 2 * padding)

    # Calculate total height of the wrapped text
    total_height = sum([draw.textbbox((0, 0), line, font=font)[3] - draw.textbbox((0, 0), line, font=font)[1] for line in wrapped_lines])

    # Calculate starting Y position to center the text
    y_position = (height - total_height) // 2

    # Draw each line
    for line in wrapped_lines:
        line_width, line_height = draw.textbbox((0, 0), line, font=font)[2], draw.textbbox((0, 0), line, font=font)[3] - draw.textbbox((0, 0), line, font=font)[1]
        x_position = (width - line_width) // 2  # Center horizontally
        draw.text((x_position, y_position), line, font=font, fill=text_color)
        y_position += line_height  # Move to the next line

    # Save the image to a BytesIO object (to upload it without saving to disk)
    image_stream = BytesIO()
    background_image.save(image_stream, format='PNG')
    image_stream.seek(0)  # Reset the stream to the beginning

    return image_stream


def get_random_hashtags():
    hashtags = [
        # General Motivation
        "#DailyQuote", "#QuoteOfTheDay", "#Motivation", "#InspireDaily", "#StayInspired",
        "#PositiveVibes", "#MindfulMoments", "#WisdomWednesday", "#SuccessMindset", "#DailyMotivation",

        # Life & Perspective
        "#LifeWisdom", "#LiveFully", "#LifeThoughts", "#DeepThoughts", "#LifeLessons",
        "#WordsToLiveBy", "#PerspectiveShift", "#MindsetMatters", "#PurposeDriven", "#GratitudeQuote",

        # Coding + Tech Inspiration
        "#CodeAndQuotes", "#DevWisdom", "#PythonQuotes", "#AutomatedInspo", "#ScriptedWisdom",
        "#DeveloperMotivation", "#TechMindset", "#AIWisdom", "#ProgrammingThoughts", "#BotWisdom",

        # Creativity & Positivity
        "#CreativeMindset", "#DreamBig", "#ThinkDifferent", "#SparkYourSoul", "#EmpowerYourself",

        # Trending or Social
        "#MondayMotivation", "#FridayFeels", "#WeekendWisdom", "#SelfGrowth", "#MentalWellness",
        "#Mindfulness", "#QuotesThatInspire", "#TruthBeTold", "#ReflectionTime", "#ZenZone"
    ]

    return ' '.join(random.sample(hashtags, 5))


# Function to upload the image to Facebook
def upload_image_to_facebook(image_stream, quote_to_post, author_to_post):
    url = f'https://graph.facebook.com/{page_id}/photos'
    payload = {
        'access_token': access_token,
        'message': f'"{quote_to_post}" \n -{author_to_post} \n\n{get_random_hashtags()}'
    }

    files = {
        'file': ('quote_image.png', image_stream, 'image/png')
    }

    response = requests.post(url, data=payload, files=files)

    if response.status_code == 200:
        logging.info("Successfully uploaded the quote image to Facebook")
    else:
        logging.error(f"Failed to upload image: {response.text}")

# Fetch a random quote from the API
quote_to_post, author_to_post = fetch_random_quote()

# Generate the image with the quote and background
image_stream = generate_image_with_quote(quote_to_post, author_to_post)


def post_quote():
    if(image_stream and quote_to_post):
        # Upload the image to Facebook
        print("Uploading quote...")
        upload_image_to_facebook(image_stream, quote_to_post, author_to_post)
        print("quote uploaded")

