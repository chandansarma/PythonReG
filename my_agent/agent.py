from langgraph.graph import END, START, StateGraph

from my_agent.utils.nodes import (
    generate_keywords_node,
    generate_summary_node,
    initialize_state_node,
    tool_call_node,
)
from my_agent.utils.state import StepState


def build_workflow() -> StateGraph:
    workflow = StateGraph(StepState)
    workflow.add_node("initialize", initialize_state_node)
    workflow.add_node("tool_call", tool_call_node)
    workflow.add_node("generate_keywords", generate_keywords_node)
    workflow.add_node("generate_summary", generate_summary_node)
    workflow.add_edge(START, "initialize")
    workflow.add_edge("initialize", "tool_call")
    workflow.add_edge("tool_call", "generate_keywords")
    workflow.add_edge("generate_keywords", "generate_summary")
    workflow.add_edge("generate_summary", END)
    return workflow


app = build_workflow().compile()


if __name__ == "__main__":
    initial_state = {
        "topic": "Python lists",
        "keywords": "",
        "summary": "",
        "status": "started",
    }

    print("Running small LangGraph example...\n")
    for event in app.stream(initial_state):
        print(event)
