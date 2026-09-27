from langchain_ollama import ChatOllama
from langchain_core.output_parsers import StrOutputParser
from langchain_core.prompts import ChatPromptTemplate

from my_agent.utils.state import StepState
from my_agent.utils.tools import get_default_topic, get_topic_details

llm = ChatOllama(model="gemma:2b", temperature=0.3)

keywords_prompt = ChatPromptTemplate.from_messages([
    ("user", "Give 3 short keywords for: {topic}")
])
keywords_chain = keywords_prompt | llm | StrOutputParser()

summary_prompt = ChatPromptTemplate.from_messages([
    ("system", "Answer briefly in 2 sentences."),
    ("user", "Explain this topic: {topic}. Use these keywords: {keywords}")
])
summary_chain = summary_prompt | llm | StrOutputParser()


def initialize_state_node(state: StepState) -> StepState:
    current = dict(state)
    current.setdefault("topic", get_default_topic())
    current.setdefault("keywords", "")
    current.setdefault("summary", "")
    current.setdefault("status", "started")
    # print("[OBSERVABILITY] initialize node:", current)
    return current


def tool_call_node(state: StepState) -> StepState:
    current = dict(state)
    topic = current.get("topic") or get_default_topic()
    details = get_topic_details(topic)
    current["status"] = "tool_called"
    current["summary"] = details["description"]
    # print("[OBSERVABILITY] tool node:", current)
    return current


def generate_keywords_node(state: StepState) -> StepState:
    current = dict(state)
    topic = current.get("topic") or get_default_topic()
    current["keywords"] = keywords_chain.invoke({"topic": topic})
    current["status"] = "keywords_done"
    # print("[OBSERVABILITY] keywords node:", current)
    return current


def generate_summary_node(state: StepState) -> StepState:
    current = dict(state)
    topic = current.get("topic") or get_default_topic()
    keywords = current.get("keywords") or ""
    current["summary"] = summary_chain.invoke({
        "topic": topic,
        "keywords": keywords,
    })
    current["status"] = "summary_done"
    # print("[OBSERVABILITY] summary node:", current)
    return current
