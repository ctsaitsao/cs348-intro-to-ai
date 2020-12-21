# Extract Credit Assignment: Augment the KB with "Explain"

In this extra credit (optional) assignment, you are going to extend the Knowledge Base (KB) with the `Explain` function. The function explains how a Fact or a Rule is supported by other Facts and Rules in the KB and whether it is asserted. 

The starter code is nearly the same as the original starter code for Assignment 2, but the **correct completion Assignment 2 is not a pre-requisite** for doing this EC assignment. In fact, a correctly implemented `Explain` function could prove to be a valuable tool for debugging the Assignment 2 code if you are/were unable to complete it correctly. 

## Starter code

As noted, this starter code builds on top of the starter code of Assignment 2. The code stub you should implement is contained in `student_code.py`, and the provided test cases are in `main.py`.

## Your task

Your task is to implement the `Explain` function to trace the supports behind a Rule or a Fact - i.e. implement the `KnowledgeBase.kb_explain` method. 

### Output format requirements for `KnowledgeBase.kb_explain`

The function should take either a Fact or a Rule that may or may not exist in the KB as argument and *return a single string as its output*. The output string should contain either a single line of error message, or one or more lines of text delineating how the input is supported in the KB. 

Outputs from valid inputs should have the following format: 
```
fact: (eats nyala leaves)
  SUPPORTED BY
    fact: (eats herbivore leaves) ASSERTED
    rule: ((eats herbivore leaves)) -> (eats nyala leaves) ASSERTED
```
The above example denotes the situation where the fact on line 1 is supported by the fact on line 3 and the rule on line 4. 

The indentation level of each line indicates the line's relationship to the ones before it. Each indent is characterized by two consecutive spaces. Here, the keyword "SUPPORTED BY" on line 2 has one more indent before it than the fact on line 1. This describes a support -- consists of one fact and one rule -- for the fact on line 1. The fact on line 3 and the rule on line 4 each has an additional indent than the support on line 2. This indicates that they together form the basis for the support. 

Note that line 3 and line 4 are concluded with the "ASSERTED" keyword, which it is missing from line 1. This keyword indicates that the fact / rule has been asserted. In the case where the fact on line 1 is supported, line 1 will also be appended with the keyword. Note that whether a fact is asserted should not interfere with how you handle its supports. 

A line depicting a Fact should be generated in the same format as demonstrated in the example:
- start with the appropriate amount of indentation;
- continue with the keyword "fact: ", maintaining a single space between the colon and the subsequent content;
- follow up with the Statement converted to string;
- if the Fact is asserted, append " ASSERTED" in the end, making sure that only one space exists between the statement string and the keyword. 

Generating a line for a Rule should follow a similar procedure: instead of generating the Statement, enclose the left hand side statements, in order, in a pair of parenthesis; follow up with " -> " and the right hand side statement. Two adjacent statements in the left hand side should be separated with ", ". Of course, the start of the statement should instead be "rule: ".

If the Fact queried is not in the KB, kb_explain should return "Fact is not in the KB"; for a missing Rule, it should return "Rule is not in the KB". Any input other than Fact or Rule instances should lead to returning False. 

If the same fact or rule is used in multiple supports, you must repeat its own supports along with it every time it appears. As with Assignment 2, you may assume that there are no circular dependencies (supports). The supports of a Fact / Rule should be presented in the order specified by its `supported_by` list. When delivering each support pair, the Fact should be placed before the Rule. 

### Testing

To grade this lab, we'll run test cases similar to the ones provided. Since the main test naively compares your output line-by-line against a predefined string, make sure that your output precisely match the expected output. Again, please feel free to share your own test cases on Piazza. When sharing tests, please provide your rationale to the test, explain what you hope to test and/or how you developed the test.
