import os
from typing import TypedDict, Annotated
import langchain
from dotenv import load_dotenv
from langchain_groq import ChatGroq
from langgraph.graph import StateGraph, START, END

load_dotenv()

llm = ChatGroq(model="groq/compound-mini", temperature=0.2)

def merge_score_dicts(existing :dict, updateddict :dict) -> dict:
    if existing is None:
        return updateddict
    return {**existing, **updateddict}
 
class AnalyzerState(TypedDict):
    raw_input : str
    safety_scores : Annotated[dict[str, int], merge_score_dicts]


#nodes

def toxicity_node(state : AnalyzerState)  -> dict:
    prompt = (
        """Analyze the following text for prfanity, aggression, hate speech, or toxicity.
        Provide a score between 0 to 100, where 0 means perfectly clean and 100 means highly toxic.
        Return ONLY the plain integer number, nothing else.
        """
        f"Text :\n{state['raw_input']}"
    )
    response = llm.invoke(prompt)

    try:
        score = int(response.content.strip())
    except ValueError:
        score = 0

    return {"safety_scores":  {"toxicity_level": score}}


def copyright_node(state: AnalyzerState) -> dict:
    prompt = (
        """Analyze the following text. Judge if it sounds plagiarized, unoriginal,
        or presents a corporate trademark risk. Provide a score between 0 and 100,
        where 0 means entirely original and 100 means high risk.
        Return ONLY plain integer number, nothing else."""
        f"\nText:\n\n{state['raw_input']}"
    )

    response = llm.invoke(prompt)

    try:
        score = int(response.content.strip())
    except ValueError:
        score = 0

    return {"safety_scores": {"copyright_risk": score}}

def culture_node(state :AnalyzerState) -> dict:
    prompt = (
        """Analyze the following text for regional sensitivity, political landmines, or cultural insesitivity taht might offend a global audience. Provide a score between 0 and 100, where 0 means completely safe and 100 means highly offensie\n\n"""
        f"Text :\n{state['raw_input']}"
    )
    response = llm.invoke(prompt)

    try:
        score = int(response.content.strip())
    except ValueError:
        score = 0

    return {"safety_scores" : {"cultural_insensitivity" : score}}


builder = StateGraph(AnalyzerState)


builder.add_node("toxicity_node",toxicity_node)
builder.add_node("copyright_check", copyright_node)
builder.add_node("culture_node", culture_node)


builder.add_edge(START, "toxicity_node")
builder.add_edge(START, "copyright_check")
builder.add_edge(START, "culture_node")


builder.add_edge("toxicity_node", END)
builder.add_edge("copyright_check",END)
builder.add_edge("culture_node", END)


app = builder.compile()

sample_script = """Yo guys!! Welcome back to the stream. Today we will understand about the socio-economic condition of India during the rule of Nand dynasty. This was the time when Vishnugupt Chanakya gathered army, and build his own decible a warior name Chandragupt, who later became the king of magadh. Earlier there were malpractices in the society, like untouchability and other, but Chandragupt abolished all in his rule in his kingdom. Later he changed his mind, became cruel. He targeted Brahaman's and raped them."""


initial_state = {
    "raw_input": sample_script,
    "safety_scores": {}
}

final_state = app.invoke(initial_state)

print(final_state['safety_scores'])