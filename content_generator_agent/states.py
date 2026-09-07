#so now we are creating a graph, and the first thing you create is a state

import os

from typing import TypedDict

class State(TypedDict):
    topic : str
    summary : str
    score : str


