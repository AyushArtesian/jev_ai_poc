def create_mock_tool(display_name):
    def tool(query):
        return f"{display_name} selected for: {query}"

    return tool


TOOLS = {
    "calculator_tool": create_mock_tool("Calculator Tool"),
    "web_search_tool": create_mock_tool("Web Search Tool"),
    "code_generator_tool": create_mock_tool("Code Generator Tool"),
    "code_debugger_tool": create_mock_tool("Code Debugger Tool"),
    "database_tool": create_mock_tool("Database Tool"),
    "summarizer_tool": create_mock_tool("Summarizer Tool"),
    "translation_tool": create_mock_tool("Translation Tool"),
    "email_writer_tool": create_mock_tool("Email Writer Tool"),
    "document_writer_tool": create_mock_tool("Document Writer Tool"),
    "data_analysis_tool": create_mock_tool("Data Analysis Tool"),
    "chart_generator_tool": create_mock_tool("Chart Generator Tool"),
    "file_reader_tool": create_mock_tool("File Reader Tool"),
    "image_analysis_tool": create_mock_tool("Image Analysis Tool"),
    "research_tool": create_mock_tool("Research Tool"),
    "planning_tool": create_mock_tool("Planning Tool"),
    "reasoning_tool": create_mock_tool("Reasoning Tool"),
    "general_llm_tool": create_mock_tool("General LLM Tool"),
    "human_review_tool": create_mock_tool("Human Review Tool"),
}
