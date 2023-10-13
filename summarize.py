from dotenv import load_dotenv
load_dotenv()
import openai
import tiktoken
enc = tiktoken.encoding_for_model("gpt-3.5-turbo")
from concurrent.futures import ThreadPoolExecutor, as_completed


def llm(prompt, text, model="gpt-3.5-turbo"):
    return openai.ChatCompletion.create(
        model=model,
        messages=[
            dict(role="system", content=prompt),
            dict(role="user", content=text)
        ],
        temperature=0
    )["choices"][0]["message"]["content"]


def tokenize(text):
    return enc.encode(text)


def token_cost(text, model="gpt-3.5-turbo", token_type="output"):
    if model == "gpt-4":
        if token_type == "input":
            cost_per_1k = 0.03
        if token_type == "output":
            cost_per_1k = 0.06
    if model == "gpt-3.5-turbo":
        if token_type == "input":
            cost_per_1k = 0.0015
        if token_type == "output":
            cost_per_1k = 0.002
    return round(len(tokenize(text)) / 1000 * cost_per_1k, 4)


def chunk_text(text, max_tokens_per_chunk=4096):
    tokens = tokenize(text)
    text_chunks = []
    for i in range(0, len(tokens), max_tokens_per_chunk):
        text_chunk = enc.decode(tokens[i:i + max_tokens_per_chunk])
        text_chunks.append(text_chunk)
    return text_chunks


def summarize(text, prompt, model="gpt-3.5-turbo", max_summary_length=700):
    prompt_length = len(tokenize(prompt))
    tokens_per_chunk = 4096 - prompt_length - max_summary_length
    summaries = []

    while len(summaries) != 1:
        text_chunks = chunk_text(text, tokens_per_chunk)
        summaries = []

        with ThreadPoolExecutor(max_workers=128) as executor:
            futures = [executor.submit(llm, prompt, text_chunk, model) for text_chunk in text_chunks]

            for future in as_completed(futures):
                summary = future.result()
                summaries.append(summary)

        text = "\n\n".join(summaries)

    return text


if __name__ == "__main__":
    from website import website_text
    text = website_text("https://news.ycombinator.com/item?id=37863415")
    print("Summary:\n\n", summarize(text, "What's the best advice?"))