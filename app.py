from pathlib import Path

import streamlit as st
from PIL import Image

from jev_router import TOOL_DESCRIPTIONS, select_tool
from tools import TOOLS


BASE_DIR = Path(__file__).resolve().parent
FAVICON_PATH = BASE_DIR / "favicon.png"

page_icon = Image.open(FAVICON_PATH) if FAVICON_PATH.exists() else None

st.set_page_config(
    page_title="JevRoute",
    page_icon=page_icon,
    layout="wide",
    initial_sidebar_state="expanded",
)


EXAMPLE_QUERIES = {
    "Choose an example": "",
    "Calculation": (
        "If I invest 50000 at 8 percent annually for 5 years, "
        "what amount will I receive?"
    ),
    "Current information": (
        "What are the latest major AI announcements today?"
    ),
    "Code generation": (
        "Write a Python function to perform binary search on a sorted list."
    ),
    "Code debugging": (
        "My Python program raises a KeyError when accessing a dictionary. "
        "Help me debug the issue."
    ),
    "Database": (
        "Write an SQL query to return the second highest salary from an employees table."
    ),
    "Summarization": (
        "Summarize the following content into five concise points: "
        "Artificial intelligence systems are increasingly being deployed..."
    ),
    "Research": (
        "Research current approaches for fully offline OCR on Android and compare the trade-offs."
    ),
    "Planning": (
        "Create a step-by-step development plan for a small e-commerce application."
    ),
}

if "query_input" not in st.session_state:
    st.session_state.query_input = ""


with st.sidebar:
    st.title("JevRoute")
    st.caption("Structured tool routing with TypeSafe Jev through OpenRouter.")

    st.divider()

    st.subheader("API configuration")

    api_key = st.text_input(
        "OpenRouter API key",
        type="password",
        placeholder="sk-or-v1-...",
        help="The key is used only for the request sent to OpenRouter.",
    )

    st.link_button(
        "Create an OpenRouter API key",
        "https://openrouter.ai/settings/keys",
        use_container_width=True,
    )

    st.caption(
        "For local development you can also place OPENROUTER_API_KEY in a .env file."
    )

    st.divider()

    st.subheader("Model")
    st.code("typesafe/jev-1.13", language=None)

    st.link_button(
        "Open the Jev model page",
        "https://openrouter.ai/typesafe/jev-1.13",
        use_container_width=True,
    )

    st.divider()

    st.subheader("Tool registry")
    st.metric("Available tools", len(TOOL_DESCRIPTIONS))

    with st.expander("View available tools"):
        for index, tool_name in enumerate(TOOL_DESCRIPTIONS, start=1):
            pretty_name = (
                tool_name.replace("_tool", "").replace("_", " ").title()
            )
            st.write(f"{index}. {pretty_name}")


st.title("Jev Tool Router")

st.write(
    "A small proof of concept that uses Jev only for natural-language "
    "tool selection. Jev chooses one tool from a fixed registry and returns "
    "the structured decision with confidence and probabilities."
)

st.info(
    "Flow: User query -> Jev decision model -> Tool classification -> "
    "Selected tool -> Mock execution"
)

st.subheader("Try the router")

example_name = st.selectbox(
    "Example query",
    options=list(EXAMPLE_QUERIES.keys()),
)

if st.button("Load example", use_container_width=False):
    st.session_state.query_input = EXAMPLE_QUERIES[example_name]

query = st.text_area(
    "Natural-language request",
    key="query_input",
    height=140,
    placeholder="Enter any request and let Jev choose the most appropriate tool.",
)

route_button = st.button(
    "Route request",
    type="primary",
    use_container_width=True,
)


if route_button:
    if not query.strip():
        st.warning("Enter a request before routing.")
        st.stop()

    try:
        with st.spinner("Routing request with Jev..."):
            result = select_tool(
                user_query=query,
                api_key=api_key if api_key.strip() else None,
            )

        selected_tool = result["tool"]
        confidence = float(result.get("confidence") or 0.0)
        probabilities = result.get("probabilities") or {}
        latency_ms = float(result.get("latency_ms") or 0.0)
        raw_response = result.get("raw_response") or {}

        st.divider()
        st.subheader("Routing decision")

        pretty_tool_name = (
            selected_tool.replace("_tool", "").replace("_", " ").title()
            if selected_tool
            else "Unknown"
        )

        result_col, confidence_col, latency_col, tools_col = st.columns(4)

        result_col.metric("Selected tool", pretty_tool_name)
        confidence_col.metric("Confidence", f"{confidence * 100:.2f}%")
        latency_col.metric("Latency", f"{latency_ms:.0f} ms")
        tools_col.metric("Candidate tools", len(probabilities))

        decision_tab, json_tab, execution_tab = st.tabs(
            ["Decision analysis", "Raw JSON", "Tool execution"]
        )

        with decision_tab:
            st.subheader("Probability distribution")

            if not probabilities:
                st.info("No probability distribution was returned.")
            else:
                sorted_probabilities = sorted(
                    probabilities.items(),
                    key=lambda item: float(item[1]),
                    reverse=True,
                )

                for rank, (tool_name, probability) in enumerate(
                    sorted_probabilities,
                    start=1,
                ):
                    probability = float(probability)
                    pretty_name = (
                        tool_name.replace("_tool", "").replace("_", " ").title()
                    )

                    left, right = st.columns([5, 1])

                    with left:
                        st.write(f"{rank}. {pretty_name}")
                        st.progress(max(0.0, min(probability, 1.0)))

                    with right:
                        st.write(f"{probability * 100:.2f}%")

        with json_tab:
            st.subheader("Complete Jev response")
            st.caption(
                "This is the structured response returned by the OpenRouter Decisions API."
            )
            st.json(raw_response, expanded=False)

        with execution_tab:
            st.subheader("Mock tool execution")

            st.write(
                "The tools are intentionally mocked. The purpose of this POC is "
                "to demonstrate Jev's tool-selection capability."
            )

            tool_function = TOOLS.get(selected_tool)

            if tool_function:
                st.success(tool_function(query))
            else:
                st.error(
                    f"The selected tool '{selected_tool}' is not registered in tools.py."
                )

    except Exception as exc:
        st.error(f"Routing failed: {exc}")


st.divider()
st.caption("JevRoute - Python, Streamlit, OpenRouter and TypeSafe Jev")
