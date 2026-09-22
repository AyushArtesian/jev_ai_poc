import os
import time
from pathlib import Path

import requests
from dotenv import load_dotenv


BASE_DIR = Path(__file__).resolve().parent
load_dotenv(BASE_DIR / ".env")

ENV_API_KEY = os.getenv("OPENROUTER_API_KEY")
if ENV_API_KEY:
    ENV_API_KEY = ENV_API_KEY.strip()


OPENROUTER_URL = "https://openrouter.ai/api/alpha/decisions"
JEV_MODEL = "typesafe/jev-1.13"


TOOL_DESCRIPTIONS = {
    "calculator_tool": (
        "Use when the primary task involves arithmetic, percentages, equations, "
        "financial mathematics, statistics calculations, numerical computation, "
        "or obtaining a numeric result."
    ),
    "web_search_tool": (
        "Use when answering requires current, recent, live, changing, or "
        "internet-based information such as current news, prices, weather, "
        "events, recent announcements, or latest developments."
    ),
    "code_generator_tool": (
        "Use when the user wants source code written, generated, implemented, "
        "or created in Python, JavaScript, Java, C++, C#, or another language."
    ),
    "code_debugger_tool": (
        "Use when the user provides code, an error, exception, stack trace, "
        "failing program, or asks to diagnose and fix programming problems."
    ),
    "database_tool": (
        "Use for SQL queries, joins, normalization, database schemas, PostgreSQL, "
        "MySQL, MongoDB, indexing, transactions, DBMS concepts, or other "
        "database-related tasks."
    ),
    "summarizer_tool": (
        "Use when the main request is to summarize, shorten, condense, extract "
        "key points, or create a concise version of supplied content."
    ),
    "translation_tool": (
        "Use when the primary task is translating text from one language into another."
    ),
    "email_writer_tool": (
        "Use when the user wants to draft, rewrite, improve, or respond to an "
        "email, professional message, or business communication."
    ),
    "document_writer_tool": (
        "Use for writing reports, proposals, essays, case studies, project "
        "documentation, technical documentation, or structured documents."
    ),
    "data_analysis_tool": (
        "Use when the user needs a dataset analyzed, trends identified, data "
        "aggregated, values compared, statistics interpreted, or patterns found."
    ),
    "chart_generator_tool": (
        "Use when the main request is specifically to create a chart, graph, "
        "histogram, bar chart, line chart, scatter plot, or visualization."
    ),
    "file_reader_tool": (
        "Use when the user provides or refers to a file such as PDF, DOCX, TXT, "
        "CSV, or another document and wants its contents read or extracted."
    ),
    "image_analysis_tool": (
        "Use when the user provides an image and asks to understand, inspect, "
        "describe, extract information from, or analyze the image."
    ),
    "research_tool": (
        "Use for in-depth research that requires gathering, comparing, "
        "synthesizing, and organizing information from multiple sources."
    ),
    "planning_tool": (
        "Use when the user requests a roadmap, implementation strategy, project "
        "plan, development plan, study plan, schedule, or structured sequence of actions."
    ),
    "reasoning_tool": (
        "Use for logical reasoning, analytical problems, puzzles, decision analysis, "
        "conceptual comparisons, or tasks requiring structured reasoning."
    ),
    "general_llm_tool": (
        "Use for general knowledge, explanations, definitions, brainstorming, "
        "conversation, creative writing, or tasks that do not require another "
        "specialized tool."
    ),
    "human_review_tool": (
        "Use when the request is highly ambiguous, missing critical information, "
        "requires human approval, or cannot confidently be assigned to another tool."
    ),
}


def select_tool(user_query: str, api_key: str | None = None):
    key = api_key or ENV_API_KEY

    if not key:
        raise RuntimeError(
            "OpenRouter API key is required. Enter it in the sidebar or add "
            "OPENROUTER_API_KEY to the .env file."
        )

    key = key.strip()

    payload = {
        "model": JEV_MODEL,
        "state": {
            "user_query": user_query,
        },
        "questions": {
            "selected_tool": {
                "type": "choice",
                "instructions": (
                    "Select exactly one tool that is most appropriate for handling "
                    "the user's request. Determine the primary intent of the user "
                    "and choose the best matching tool from the available options."
                ),
                "criteria": TOOL_DESCRIPTIONS,
            }
        },
    }

    headers = {
        "Authorization": f"Bearer {key}",
        "Content-Type": "application/json",
    }

    start_time = time.perf_counter()

    response = requests.post(
        OPENROUTER_URL,
        headers=headers,
        json=payload,
        timeout=30,
    )

    latency_ms = (time.perf_counter() - start_time) * 1000

    if not response.ok:
        raise RuntimeError(
            f"OpenRouter API error {response.status_code}: {response.text}"
        )

    data = response.json()
    answers = data.get("answers", {})
    decision = answers.get("selected_tool")

    if not decision:
        raise RuntimeError(
            "Jev did not return a 'selected_tool' decision. "
            f"Response: {data}"
        )

    return {
        "tool": decision.get("choice"),
        "confidence": decision.get("confidence"),
        "probabilities": decision.get("probabilities", {}),
        "model": data.get("model", JEV_MODEL),
        "usage": data.get("usage", {}),
        "latency_ms": latency_ms,
        "raw_response": data,
    }
