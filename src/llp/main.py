import os
from config import sources, test_k
from news import get_news, News
from src.llp.agent import get_local_summarizer
from src.llp.broadcast import generate_news_show_script
from src.llp.speak import text_to_speech
from src.llp.translate import auto_translate_to_modern_greek

rss_urls = sources

if test_k:
    rss_urls = rss_urls[:test_k]

# Fetch News
print("Fetching News...")
news = get_news(rss_urls)
summarize = get_local_summarizer()
summarized_news = [
    News(news_entry.title, summarize(news_entry.text), news_entry.link)
    for news_entry in news
]

# Prepare Script for News Show
print("Preparing Script...")
broadcast_script = generate_news_show_script(summarized_news[:2])

# checkpoint
# Check if the file exists
if os.path.isfile("checkpoint.txt"):
    # File exists → read it
    with open("checkpoint.txt", "r") as file:
        broadcast_script = file.read()
    print("File exists. Its content is:\n")
else:
    # File does not exist → create and write text
    with open("checkpoint.txt", "w") as file:
        file.write(broadcast_script)

# Translate into any Language
print("Translating...")
audio = auto_translate_to_modern_greek(broadcast_script)

# Run Text-to-Speech
print("Broadcast Start...")
text_to_speech(audio)
