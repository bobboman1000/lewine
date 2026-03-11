from langchain.chat_models import ChatOpenAI
from langchain_community.llms.huggingface_pipeline import HuggingFacePipeline
from langchain_core.prompts import PromptTemplate
from transformers import AutoTokenizer, AutoModelForCausalLM, pipeline
from langchain.chains import LLMChain

def get_local_summarizer():
    summarizer = pipeline("summarization", model="facebook/bart-large-cnn")
    return HuggingFacePipeline(pipeline=summarizer)

def get_local_agent(model_name: str = "deepseek-ai/DeepSeek-R1-Distill-Qwen-1.5B"):

    # Load tokenizer and model
    tokenizer = AutoTokenizer.from_pretrained(model_name)
    model = AutoModelForCausalLM.from_pretrained(model_name, device_map="auto", torch_dtype="auto")

    # Build the text generation pipeline
    generator = pipeline("text-generation", model=model, tokenizer=tokenizer, max_new_tokens=1024)

    return generator

def get_openai_agent():
    # Step 1: Prepare the LLM
    llm = ChatOpenAI(model_name="gpt-4", temperature=0.7)

    # Step 2: Prompt template
    prompt_template = PromptTemplate.from_template("""
    You are a professional news anchor. Given a list of news items, create a coherent, engaging news show script.
    Use a human tone, vary your transitions between stories, and maintain clarity and professionalism.
    Include an intro, smooth transitions, and a closing outro.

    News Items:
    {news_items}

    Now write the full news show script.
    """)

    # Step 3: LangChain chain
    chain = LLMChain(llm=llm, prompt=prompt_template)

    return chain
