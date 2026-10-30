import time
from typing import TypedDict, Any
from dotenv import load_dotenv
from groq import RateLimitError
from langchain_groq import ChatGroq
from langgraph.graph import StateGraph, END
from langgraph.prebuilt import create_react_agent
from prompts import PLANNER_PROMPT, ARCHITECT_PROMPT, CODER_SYSTEM_PROMPT
from states import Plan, TaskPlan
from tools import coder_tools, read_file

load_dotenv()

llm = ChatGroq(model="openai/gpt-oss-120b", temperature=0.2, max_retries=6)


class GraphState(TypedDict, total=False):
    query: str
    plan: Any
    task_plan: Any
    current_step_index: int


def ask(schema, prompt, retries=3):
    last = None
    for method in ("json_schema", "function_calling"):
        for _ in range(retries):
            try:
                out = llm.with_structured_output(schema, method=method).invoke(prompt)
                if out is not None:
                    return out
            except RateLimitError as e:
                last = e
                print("[rate limit] 20 second ruk raha hun...")
                time.sleep(20)
            except Exception as e:
                last = e
                print(f"[retry] {method}: {str(e)[:100]}")
    raise last


def planner_node(state: GraphState) -> dict:
    print("\n--- Running Planner Agent ---")
    plan = ask(Plan, PLANNER_PROMPT.format(query=state["query"]))
    return {"plan": plan}


def architect_node(state: GraphState) -> dict:
    print("\n--- Running Architect Agent ---")
    task_plan = ask(
        TaskPlan,
        ARCHITECT_PROMPT.format(plan=state["plan"].model_dump_json()),
    )
    return {"task_plan": task_plan, "current_step_index": 0}


def coder_node(state: GraphState) -> dict:
    index = state["current_step_index"]
    steps = state["task_plan"].implementation_steps
    task = steps[index]

    print(f"\n--- Running Coder Agent ({index + 1}/{len(steps)}): {task.file_path} ---")

    existing = read_file.run(task.file_path)
    user_message = (
        f"File Path: {task.file_path}\n"
        f"Instructions: {task.task_description}\n"
        f"Existing Content: {existing}\n"
        "Write the full code and save it with the write_file tool."
    )

    agent = create_react_agent(llm, tools=coder_tools, prompt=CODER_SYSTEM_PROMPT)

    for attempt in range(6):
        try:
            agent.invoke({"messages": [("user", user_message)]})
            break
        except RateLimitError:
            print("[rate limit] 20 second ruk raha hun...")
            time.sleep(20)
    else:
        raise RuntimeError(f"Rate limit ki wajah se {task.file_path} nahi ban saki")

    time.sleep(10)  # agli file se pehle thora wait
    return {"current_step_index": index + 1}


def router_logic(state: GraphState) -> str:
    total = len(state["task_plan"].implementation_steps)
    return "coder" if state["current_step_index"] < total else "end"


workflow = StateGraph(GraphState)
workflow.add_node("planner", planner_node)
workflow.add_node("architect", architect_node)
workflow.add_node("coder", coder_node)
workflow.set_entry_point("planner")
workflow.add_edge("planner", "architect")
workflow.add_edge("architect", "coder")
workflow.add_conditional_edges("coder", router_logic, {"coder": "coder", "end": END})

app = workflow.compile()