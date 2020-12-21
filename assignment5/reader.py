"""" 
Reader has three outwards facing functions for reading in and tokenizing the definitions 
for facts and rules, actions, and plans. Each of the reasders returns a list (or two lists
in the case of facts/rules) of the elements defined in the files.
"""

def read_and_tokenize_facts_and_rules(file):
    """Reads in a file and processes contents into lists of facts and rules.

    Args:
        file (file): A txt file with facts of the form (predicate subject
        object) such as "fact: (isa cube block)". As well, there are rules with
        a right and left hand side that are essentially (fact1 and fact2) ->
        (fact3) such as "rule: ((inst ?x ?y) (isa ?y ?z)) -> (inst ?x ?z)".
        These facts and rules each go on a new line in the file and are looped
        over to build the two seperate lists of facts and rules.

    Returns:
        A list of Facts and Rules.
    """
    file = open(file, "r")
    facts = []
    rules =[]
    for line in file:
        element = parse_fact_and_rule_element(line)         
        if element[0] == "Fact":
            facts.append(element[1])
        elif element[0] == "Rule":
            rules.append([element[1],element[2]])
    file.close()
    return facts,rules


def parse_fact_and_rule_element(element):
    """
    Parses a line, assigning labels and splitting rules into LHS & RHS

    Args:
        e (string): Input string to parse

    Returns:
        (number, string | listof string): label, then parsed input
    """
    if len(element) == 0:
        return [None]
    elif "#" in element:
        return [None]
    elif not "(" in element:
        return [None]
    elif "->" in element:
        lhs,rhs = element.split("->")
        rhs = rhs.replace(")", "").replace("(", "").rstrip().strip().split()
        lhs = lhs.rstrip(") ").strip("( ").replace("(", "").split(")")
        lhs = list(map(lambda x: x.rstrip().strip().split(), lhs))
        return ["Rule", lhs, rhs]
    else:
        fact = element.replace(")", "").replace("(", "").rstrip().strip().split()
        return ["Fact", fact]


def read_and_tokenize_actions(file):
    """
    Reads in a file of actions.

    Args:
        file (file): A txt file of actions defining name, object definitions, preconditions, 
        adds and deletes

    Returns:
        A list of actions
    """
    file = open(file, "r")
    actions = []
    action = []
    for line in file:
        if len(line) == 0 or "#" in line or not "(" in line:
            if action: 
                actions.append(action)
            action = []
        else:
            element = parse_action_element(line)
            action.append(element)
    if action: 
        actions.append(action)
    file.close()
    return actions

def parse_action_element(element):
    """
    Parses an line that is a part of an action

    Args:
        e (string): Input string to parse

    Returns:
        The action element broken into components
    """
    if "Action:" in element:
        element = element.replace("Action:","")
        result = ["Action:"]
        result.append(element.replace(")", "").replace("(", "").rstrip().strip().split())
        return result
    if "Objects:" in element:
        result = ["Objects:"]
        element = element.replace("Objects:","")
    elif "Preconditions:" in element:
        result = ["Preconditions:"]
        element = element.replace("Preconditions:","")
    elif "Add:" in element:
        result = ["Add:"]
        element = element.replace("Add:","")
    elif "Delete:" in element:
        result = ["Delete:"]
        element = element.replace("Delete:","")
    elements = map(lambda x: x.strip().rstrip().split(" "), element.replace("(","").split(")")[:-1])
    result.append(list(elements)[:-1])
    return result

def read_patterns(file):

    file = open(file, "r")
    patterns = []
    for line in file:
    	if len(line) > 5:
    		pattern = line.split(": ")
    		patterns.append(pattern)
    file.close()
    return patterns