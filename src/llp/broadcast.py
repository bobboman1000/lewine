from src.llp.agent import get_local_agent
from src.llp.news import News


def get_news_show_prompt(news_list: list[News]) -> str:
    prompt_intro = (
        "You are a professional TV news anchor. Given the following news stories, "
        "create a smooth, engaging, human-sounding news show script. Include an intro, transitions between stories, and "
        "a closing. Make it a short and concise update, not more than 100 words. Select the most important news."
        ""
        "\n\n"
    )

    formatted_news = "\n\n".join(
        f"Title: {n.title}\nSummary: {n.text}"
        for n in news_list
    )

    full_prompt = prompt_intro + formatted_news + "\n\nNews Show Script:\n"
    return full_prompt

def generate_news_show_script(news_list: list[News], get_generator: callable = get_local_agent) -> str:
    prompt = get_news_show_prompt(news_list)

    # Instruct models expect a user prompt format like below
    formatted_input = f"[INST] {prompt} [/INST]"

    generator = get_generator()
    print(f"Generating script with prompt length: {len(prompt)}")
    output = generator(formatted_input)[0]['generated_text']
    return output