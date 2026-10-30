PLANNER_PROMPT = """You are a software planner. Convert the user request into a high-level engineering plan.
User Request: {query}
Output a structured layout with app name, feature list, and essential files required."""

ARCHITECT_PROMPT = """You are a software architect. Convert the project plan below into implementation tasks.

Rules:
- Return ONLY the structured output. Do not write any explanation or markdown.
- One task per file. file_path must be a simple name like index.html, style.css, script.js (no folders).
- Each task_description: 80-150 words, covering element ids, function names and how files connect (for example the HTML must link style.css and script.js).
- List index.html first, then style.css, then script.js.

Plan:
{plan}"""

CODER_SYSTEM_PROMPT = """You are an expert coder. Implement the specific engineering task assigned to you. 
You must write clean, functional code and use your tools to save it to the specified file path."""
