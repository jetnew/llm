# LLM

Useful collection of LLM tools.

## Features

- `website.py`
  - `website_html(url)` - gets html given website url
  - `website_text(url)` - gets website text given website url
- `summarize.py`
  - `chunk_text(text)` - processes text into list of text chunks
  - `summarize(text, prompt)` - summarizes text, recursively if length exceeds context

## Setup

1. Create `.env` with `OPENAI_API_KEY=sk-...`.