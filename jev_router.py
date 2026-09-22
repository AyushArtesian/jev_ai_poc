import os
import time
from pathlib import Path

import requests
from dotenv import load_dotenv


# --------------------------------------------------
# Environment
# --------------------------------------------------

BASE_DIR = Path(__file__).resolve().parent
load_dotenv(BASE_DIR / ".env")

ENV_API_KEY = os.getenv("OPENROUTER_API_KEY")


# --------------------------------------------------
# OpenRouter / Jev
# --------------------------------------------------

OPENROUTER_URL = "https://openrouter.ai/api/alpha/decisions"
JEV_MODEL = "typesafe/jev-1.13"


# --------------------------------------------------
# Tool definitions
# --------------------------------------------------

TOOL_DESCRIPTIONS = {

    "calculator_tool": (
        "Use for arithmetic, percentages, equations, numerical calculations, "
        "financial math, statistics calculations, or tasks whose main purpose "
        "is computing a numerical result."
    ),

    "web_search_tool": (
        "Use when the user needs current, recent, live, changing, or internet-based "
        "information such as news, current events, prices, recent research, "
        "latest announcements, or information that may have changed."
    ),

    "code_generator_tool": (
        "Use when the user asks to write, generate, implement, or create source code."
    ),

    "code_debugger_tool": (
        "Use when the user provides code, an error, stack trace, exception, "
        "or asks to diagnose and fix a programming problem."
    ),

    "database_tool": (
        "Use for SQL, database design, joins, normalization, schemas, PostgreSQL, "
        "MySQL, MongoDB, indexing, transactions, or DBMS-related work."
    ),

    "summarizer_tool": (
        "Use when the user asks to summarize, shorten, condense, or extract "
        "important information from provided content."
    ),

    "translation_tool": (
        "Use when the primary task is translating text from one language to another."
    ),

    "email_writer_tool": (
        "Use for drafting, rewriting, improving, or responding to professional "
        "emails and business communication."
    ),

    "document_writer_tool": (
        "Use for reports, proposals, case studies, essays, project documentation, "
        "or other structured written documents."
    ),

    "data_analysis_tool": (
        "Use when the task involves analyzing data, identifying trends, aggregating "
        "values, comparing data, or finding patterns."
    ),

    "chart_generator_tool": (
        "Use when the user specifically wants a chart, graph, histogram, line chart, "
        "bar chart, scatter plot, or other visualization."
    ),

    "file_reader_tool": (
        "Use when the user wants to inspect, read, or extract information from "
        "a PDF, DOCX, TXT, CSV, or another provided file."
    ),

    "image_analysis_tool": (
        "Use when the user provides an image and wants it inspected, described, "
        "understood, or analyzed."
    ),

    "research_tool": (
        "Use for in-depth research requiring information gathering, comparison, "
        "synthesis, and analysis across multiple sources."
    ),

    "planning_tool": (
        "Use when the user requests a roadmap, project plan, implementation plan, "
        "study plan, schedule, or structured sequence of steps."
    ),

    "reasoning_tool": (
        "Use for logic problems, analytical reasoning, puzzles, decision analysis, "
        "or tasks where structured reasoning is the primary requirement."
    ),

    "general_llm_tool": (
        "Use for general explanations, definitions, brainstorming, general knowledge, "
        "creative writing, or requests that don't require another specialized tool."
    ),

    "human_review_tool": (
        "Use when the request is highly ambiguous, lacks enough information, "
        "requires human approval, or cannot confidently be assigned to another tool."
    ),
}


# --------------------------------------------------
# Router
# --------------------------------------------------

def select_tool(user_query, api_key=None):

    # Sidebar key takes priority.
    # .env key remains useful during local development.
    key = api_key or ENV_API_KEY

    if not key:
        raise RuntimeError(
            "OpenRouter API key is required."
        )

    key = key.strip()

    payload = {
        "model": JEV_MODEL,

        "state": {
            "user_query": user_query
        },

        "questions": {
            "selected_tool": {

                "type": "choice",

                "instructions": (
                    "Select exactly one tool that is most appropriate for handling "
                    "the user's request. Determine the primary intent and choose "
                    "the best matching tool."
                ),

                "criteria": TOOL_DESCRIPTIONS
            }
        }
    }

    headers = {
        "Authorization": f"Bearer {key}",
        "Content-Type": "application/json"
    }

    start = time.perf_counter()

    response = requests.post(
        OPENROUTER_URL,
        headers=headers,
        json=payload,
        timeout=30
    )

    latency_ms = (time.perf_counter() - start) * 1000

    if not response.ok:
        raise RuntimeError(
            f"OpenRouter API error {response.status_code}: "
            f"{response.text}"
        )

    data = response.json()

    answers = data.get("answers", {})
    decision = answers.get("selected_tool")

    if not decision:
        raise RuntimeError(
            f"No selected_tool answer returned. Response: {data}"
        )

    return {
        "tool": decision.get("choice"),
        "confidence": decision.get("confidence"),
        "probabilities": decision.get("probabilities", {}),
        "model": data.get("model", JEV_MODEL),
        "usage": data.get("usage", {}),
        "latency_ms": latency_ms,
        "raw_response": data
    }