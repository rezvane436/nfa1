from typing import NamedTuple

def match(pattern, string):

    class Node(NamedTuple):
        star:   bool
        char:   str

    class SearchState(NamedTuple):
        chars_consumed: int
        node_number:    int

    # Get the node list
    nodes = []
    for (i, char) in enumerate(pattern):
        if char == '*':
            continue
        if i+1 < len(pattern) and pattern[i+1] == '*':
            nodes.append(Node(star=True, char=char))
        else:
            nodes.append(Node(star=False, char=char))

    def expand(state):
        "Yield all the successors to the state."
        if state.node_number == len(nodes):
            return
        node = nodes[state.node_number]
        if node.star:
		    yield SearchState(
                state.chars_consumed,
                state.node_number + 1
            )
        if state.chars_consumed < len(string):
            current_char = string[state.chars_consumed]
            if node.char == '.' or current_char == node.char:
                yield SearchState(
                    state.chars_consumed + 1,
                    state.node_number + (0 if node.star else 1)
                )

    # Perform the search
    seen = set()
    final_state = SearchState(
        chars_consumed  = len(string), 
        node_number     = len(nodes)
    )
    initial_state = SearchState(0, 0)
    stack = [initial_state]
    while stack:
        state = stack.pop()
        if state == final_state:
            return True
        for next_state in expand(state):
            if next_state not in seen:
                stack.append(next_state)
                seen.add(next_state)
    return False