import json
import streamlit as st
from textwrap import dedent

from jev_router import select_tool, TOOL_DESCRIPTIONS
from tools import TOOLS


# ==========================================================
# PAGE CONFIG
# ==========================================================

st.set_page_config(
    page_title="JevRoute",
    page_icon="⚡",
    layout="wide",
    initial_sidebar_state="expanded"
)


# ==========================================================
# CUSTOM CSS
# ==========================================================

st.markdown(
    """
    <style>

    /* Main page */

    .block-container {
        max-width: 1180px;
        padding-top: 2.2rem;
        padding-bottom: 4rem;
    }

    /* Remove Streamlit top spacing */

    header[data-testid="stHeader"] {
        background: transparent;
    }

    /* Hero */

    .hero {
        padding: 24px 0 18px 0;
    }

    .hero-title {
        font-size: 3rem;
        font-weight: 800;
        letter-spacing: -1.8px;
        margin-bottom: 6px;
    }

    .gradient-text {
        background: linear-gradient(
            90deg,
            #8b5cf6,
            #3b82f6,
            #06b6d4
        );

        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
    }

    .hero-subtitle {
        font-size: 1.05rem;
        opacity: 0.72;
        max-width: 760px;
        line-height: 1.7;
    }

    /* Badge */

    .badge {
        display: inline-block;
        padding: 5px 12px;
        border: 1px solid rgba(139, 92, 246, 0.35);
        border-radius: 30px;
        background: rgba(139, 92, 246, 0.08);
        margin-bottom: 14px;
        font-size: 0.82rem;
        font-weight: 600;
    }

    /* Selected tool card */

    .tool-card {
        border: 1px solid rgba(148, 163, 184, 0.16);
        border-radius: 16px;
        padding: 22px 24px;
        background: rgba(30, 41, 59, 0.30);
        margin-bottom: 12px;
    }

    .tool-label {
        font-size: 0.80rem;
        opacity: 0.60;
        text-transform: uppercase;
        letter-spacing: 1px;
    }

    .tool-name {
        font-size: 1.75rem;
        font-weight: 700;
        margin-top: 8px;
    }

    /* Sidebar */

    section[data-testid="stSidebar"] {
        border-right: 1px solid rgba(148, 163, 184, 0.15);
    }

    /* Metrics */

    div[data-testid="stMetric"] {
        border: 1px solid rgba(148, 163, 184, 0.15);
        padding: 15px;
        border-radius: 12px;
        background: rgba(30, 41, 59, 0.22);
    }

    /* Buttons */

    .stButton > button {
        border-radius: 10px;
        font-weight: 600;
        min-height: 44px;
    }

    /* Hide footer */

    footer {
        visibility: hidden;
    }

    </style>
    """,
    unsafe_allow_html=True
)


# ==========================================================
# SIDEBAR
# ==========================================================

with st.sidebar:

    st.markdown("## ⚡ JevRoute")

    st.caption(
        "Structured AI tool routing powered by TypeSafe Jev via OpenRouter."
    )

    st.divider()

    st.markdown("### API Configuration")

    api_key = st.text_input(
        "OpenRouter API Key",
        type="password",
        placeholder="sk-or-v1-...",
        help="Your key is used only to make the API request."
    )

    st.link_button(
        "🔑 Create OpenRouter API Key",
        "https://openrouter.ai/settings/keys",
        use_container_width=True
    )

    st.caption(
        "Don't have a key? Sign in to OpenRouter and create one from the Keys page."
    )

    st.divider()

    st.markdown("### Model")

    st.code(
        "typesafe/jev-1.13",
        language=None
    )

    st.link_button(
        "View Jev on OpenRouter",
        "https://openrouter.ai/typesafe/jev-1.13",
        use_container_width=True
    )

    st.divider()

    st.markdown("### Router")

    st.metric(
        "Available Tools",
        len(TOOL_DESCRIPTIONS)
    )

    with st.expander("View tool registry"):

        for index, tool in enumerate(
            TOOL_DESCRIPTIONS.keys(),
            start=1
        ):

            pretty_name = (
                tool
                .replace("_tool", "")
                .replace("_", " ")
                .title()
            )

            st.write(
                f"**{index}. {pretty_name}**"
            )

    st.divider()

    st.caption(
        "The API key is never displayed in the interface."
    )


# ==========================================================
# HERO
# ==========================================================

st.markdown(
    dedent("""
    <div class="hero">
        <div class="badge">
            SYSTEM ONE • AI ROUTING POC
        </div>

        <div class="hero-title">
            Natural Language →
            <span class="gradient-text">
                Tool Selection
            </span>
        </div>

        <div class="hero-subtitle">
            JevRoute uses TypeSafe Jev as a dedicated decision model
            to classify natural-language requests and select the most
            appropriate tool from a predefined tool registry.
        </div>
    </div>
    """),
    unsafe_allow_html=True
)


# ==========================================================
# QUERY INPUT
# ==========================================================

st.markdown("### Try the router")

query = st.text_area(
    "Request",
    placeholder=(
        "Example: Search for the latest developments "
        "in multimodal AI models."
    ),
    height=120,
    label_visibility="collapsed"
)


# Example queries

example_col1, example_col2, example_col3 = st.columns(3)

with example_col1:
    if st.button(
        "🧮 Calculate compound interest",
        use_container_width=True
    ):
        st.session_state["example_query"] = (
            "Calculate compound interest on 50000 "
            "at 8 percent annually for 5 years."
        )

with example_col2:
    if st.button(
        "💻 Debug Python error",
        use_container_width=True
    ):
        st.session_state["example_query"] = (
            "My Python program throws a KeyError "
            "when accessing a dictionary. Help debug it."
        )

with example_col3:
    if st.button(
        "🌐 Latest AI news",
        use_container_width=True
    ):
        st.session_state["example_query"] = (
            "What are the latest major AI announcements today?"
        )


# Because textarea has already rendered,
# show selected example as info for next input.
if "example_query" in st.session_state:

    selected_example = st.session_state.pop(
        "example_query"
    )

    st.caption(
        f"Example: {selected_example}"
    )


route_button = st.button(
    "⚡ Route Request",
    type="primary",
    use_container_width=True
)


# ==========================================================
# ROUTING
# ==========================================================

if route_button:

    if not query.strip():

        st.warning(
            "Enter a request before routing."
        )

    elif not api_key:

        st.warning(
            "Add your OpenRouter API key from the sidebar."
        )

    else:

        try:

            with st.spinner(
                "Jev is evaluating the available tools..."
            ):

                result = select_tool(
                    query,
                    api_key=api_key
                )


            selected_tool = result["tool"]

            confidence = (
                result["confidence"] or 0
            )

            probabilities = (
                result["probabilities"] or {}
            )

            latency = result["latency_ms"]

            raw_response = result["raw_response"]


            st.divider()

            st.markdown("## Routing Decision")


            # ==================================================
            # RESULT CARD
            # ==================================================

            pretty_tool_name = (
                selected_tool
                .replace("_tool", "")
                .replace("_", " ")
                .title()
            )

            st.markdown(
                f"""
                <div class="tool-card">

                    <div class="tool-label">
                        Selected Tool
                    </div>

                    <div class="tool-name">
                        ⚡ {pretty_tool_name}
                    </div>

                </div>
                """,
                unsafe_allow_html=True
            )


            # ==================================================
            # METRICS
            # ==================================================

            metric1, metric2, metric3, metric4 = st.columns(4)

            metric1.metric(
                "Confidence",
                f"{confidence * 100:.2f}%"
            )

            metric2.metric(
                "Latency",
                f"{latency:.0f} ms"
            )

            metric3.metric(
                "Candidate Tools",
                len(probabilities)
            )

            metric4.metric(
                "Model",
                "Jev 1.13"
            )


            # ==================================================
            # TABS
            # ==================================================

            decision_tab, json_tab, execution_tab = st.tabs(
                [
                    "📊 Decision Analysis",
                    "🧾 Raw JSON",
                    "⚙️ Tool Execution"
                ]
            )


            # ==================================================
            # DECISION TAB
            # ==================================================

            with decision_tab:

                st.markdown(
                    "### Tool Probability Distribution"
                )

                sorted_probabilities = sorted(
                    probabilities.items(),
                    key=lambda item: item[1],
                    reverse=True
                )

                # Show all but emphasize ranking
                for index, (
                    tool_name,
                    probability
                ) in enumerate(
                    sorted_probabilities,
                    start=1
                ):

                    pretty_name = (
                        tool_name
                        .replace("_tool", "")
                        .replace("_", " ")
                        .title()
                    )

                    left, right = st.columns(
                        [4, 1]
                    )

                    with left:

                        label = (
                            f"**#{index} {pretty_name}**"
                            if index <= 3
                            else pretty_name
                        )

                        st.write(label)

                        st.progress(
                            min(
                                max(probability, 0),
                                1
                            )
                        )

                    with right:

                        st.write(
                            f"**{probability * 100:.2f}%**"
                        )


            # ==================================================
            # JSON TAB
            # ==================================================

            with json_tab:

                st.markdown(
                    "### Complete Jev Response"
                )

                st.caption(
                    "Raw structured response returned "
                    "through OpenRouter."
                )

                st.json(
                    raw_response,
                    expanded=True
                )

                with st.expander(
                    "View JSON as formatted text"
                ):

                    st.code(
                        json.dumps(
                            raw_response,
                            indent=2
                        ),
                        language="json"
                    )


            # ==================================================
            # TOOL EXECUTION TAB
            # ==================================================

            with execution_tab:

                st.markdown(
                    "### Mock Tool Execution"
                )

                st.caption(
                    "The POC focuses on tool selection. "
                    "Tool implementations are currently mocked."
                )

                tool_function = TOOLS.get(
                    selected_tool
                )

                if tool_function:

                    output = tool_function(
                        query
                    )

                    st.success(
                        output
                    )

                else:

                    st.error(
                        f"{selected_tool} is not "
                        "registered in tools.py."
                    )


        except Exception as error:

            st.error(
                f"Routing failed: {error}"
            )


# ==========================================================
# FOOTER
# ==========================================================

st.markdown("---")

st.caption(
    "JevRoute • Streamlit + Python + "
    "TypeSafe Jev + OpenRouter"
)