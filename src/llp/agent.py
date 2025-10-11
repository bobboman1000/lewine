from news import fetch_news, extract_article
from transformers import pipeline
from langchain.tools import Tool
from langchain.llms import HuggingFacePipeline
from langchain.chains import LLMChain
from langchain.agents import initialize_agent, AgentType
from config import sources, test_k

# Set up local summarizer
summarizer = pipeline("summarization", model="facebook/bart-large-cnn")
llm = HuggingFacePipeline(pipeline=summarizer)

def run_agent(rss_url):
    news_items = fetch_news(rss_url)
    summaries = []
    for item in news_items:
        article = extract_article(item['link'])
        summary = llm(article['text'])[0]['summary_text']
        summaries.append({
            'title': article['title'],
            'summary': summary,
            'full_text': article['text'],
            'link': item['link']
        })
    return summaries

if __name__ == "__main__":
    rss_urls = sources

    if test_k:
        rss_urls = rss_urls[:test_k]

    summaries = [run_agent(rss_url) for rss_url in rss_urls]
    for summary in summaries:
        print(f"Title: {summary['title']}")
        print(f"Summary: {summary['summary']}")
        print(f"Link: {summary['link']}\n")