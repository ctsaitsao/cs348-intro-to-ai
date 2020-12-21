# Assignment 1: Knowledge Base Basics

In this lab assignment, you are going to create a basic knowledge base (KB) to store and retrieve facts. The facts will be statements that includes predicates (e.g., Color, Size, Inst) that relate objects together.  For example:

Block1 is an instance of a rectangle.
- Inst(block1, rectangle)

Block1 is red
- Color(block1, red)

Block1 is large
- Size(block1, large)

Rectangles are blocks
- Isa(rectangle, block)

The knowledge base supports two main interfaces: `Assert`and `Ask`.

- `Assert`: Add facts into the knowledge base.
- `Ask`: ask queries and return a list of bindings for facts.

## Starter code

We provide you five files with code: `main.py`, `logical_classes.py`, `read.py`, `util.py` and `student_code.py`. (Details about these files are described at the end of this write-up.)

- `main.py` contains code for testing the KnowledgeBase
- `student_code.py` contains the `KnowledgeBase` class and is where you will be writing code.
- `logical_classes.py` contains classes for each type of logical component, e.g. `Fact`, `Rule`, etc.
- `util.py` contains several useful helper functions
- `read.py` contains functions that read statements from files or terminal. (You won't need to read/explore this file.)

There are also two data files: `statements_kb.txt` and `statements_kb2.txt`.  These files contain the facts and rules to be inserted into the KB. The provided tests use `statements_kb.txt`, and you may use `statements_kb2.txt` to generate your own tests.

## Your task

To get you started, the stubbed out code for the `KnowledgeBase.kb_assert` and `KnowledgeBase.kb_ask` methods are in `student_code.py`.  These methods are called by the tests in `main.py`.

Your task is two-part:

1. Implement storing facts in the KB
2. Implement retrieving facts from the KB

## Storing facts

Storing facts simply puts any new facts received into a list of facts.  Do not store a fact if it is already in the KB. Be careful to only put a Fact in the list and not just anything (i.e., check that the argument is a Fact).  Note that we expect the facts to be stored in a list (and not a set) to ensure that they are retrieved in a deterministic order.  This is not criticial to the function of the KB but is essential for the Auto Grader.

### Retrieving facts

The key idea is to find any facts in the KB that match the "asked" for fact.  Since the queried fact may contain a variable, matching facts might not be exact matches.  To help in finding matching facts, we provide a `match` method in `util.py`.  If a pair of facts match, then this method will return the `Bindings` that make the statements unify.

`Bindings` is a list of pairs (binding), where each pair is a variable (e.g., '?X') and a value (e.g., 'red').  Since it is a list, there may be multiple pairs.  Actually, there needs to be exactly one binding for each variable.  For example, in asking for '(color ?X red)', there will be only one binding, the one for '?X'.  But the query for '(color ?X ?Y)'' will result in bindings for '?X' and '?Y'.  See test 5 for an example of bindings containing more than one variable.

Since there may be many facts that match a queried fact, `kb_ask` needs to return a `ListOfBindings` (or False if no matching facts).  The ListOfBindings is exactly as the name implies, a list of Bindings, packaged up in a class with convenient accessors and such.  See tests 3 and 5 for examples of multiple bindings being returned from `kb_ask`.


### Testing

To test this lab, we'll create several testing files that contain a bunch of facts (similar to the ones provided). Each fact will be asserted one-by-one into the KB. After asserting the facts, a query will be constructed and the KB will be asked for a fact.  **We strongly recommend you make your own testing files. Please feel free to share them on Piazza.**. When sharing tests, please provide your rationale to the test, explain what you hope to test and/or how you developed the test.

## Looking ahead

Next week, we will be extending the KB.  We will introduce Rules which may also be asserted.  Given the Rules and Facts asserted, we will infer new Facts.  Finally, we will retract some facts and related facts that have been inferred.

As you implement this week's assignment, you may want to think ahead to how you would extend the KB to handle rules, inference, and retraction.  


\pagebreak

# Appendix: File Breakdown

Below is a description of each included file and the classes contained within each including a listing of their attributes. Each file has documentation in the code reflecting the information below (in most cases they are exactly the same). As you read through the attributes follow along in the corresponding files and make sure you're understanding the descriptions.

Attributes of each class are listed in the following format (_Note:_ if you see a type like `Fact|Rule` the `|` type is `or` and mean the type can be either Fact or Rule):

- `field_name` (`type`) - text description

## logical_classes.py

This file defines all basic structure classes.

### Fact

Represents a fact in our knowledge base. Has a statement containing the content of the fact, e.g. (isa Sorceress Wizard) and fields tracking which facts/rules in the KB it supports and is supported by.

**Attributes**

- `name` (`str`): 'fact', the name of this class
- `statement` (`Statement`): statement of this fact, basically what the fact actually says
- `asserted` (`bool`): flag indicating if fact was asserted instead of inferred from other rules in the KB
- `supported_by` (`listof Fact|Rule`): Facts/Rules that allow inference of the statement
- `supports_facts` (`listof Fact`): Facts that this fact supports
- `supports_rules` (`listof Rule`): Rules that this fact supports

### Rule

Represents a rule in our knowledge base. Has a list of statements (the LHS) containing the statements that need to be in our KB for us to infer the RHS statement. Also has fields tracking which facts/rules in the KB it supports and is supported by.

**Attributes**

- `name` (`str`): 'rule', the name of this class
- `lhs` (`listof Statement`): LHS statements of this rule
- `rhs` (`Statement`): RHS statment of this rule
- `asserted` (`bool`): flag indicating if rule was asserted instead of inferred from other rules/facts in the KB
- `supported_by` (`listof Fact|Rule`): Facts/Rules that allow inference of the statement
- `supports_facts` (`listof Fact`): Facts that this rule supports
- `supports_rules` (`listof Rule`): Rules that this rule supports

### Statement

Represents a statement in our knowledge base, e.g. (attacked Ai Nosliw), (diamonds Loot), (isa Sorceress Wizard), etc. These statements show up in Facts or on the LHS and RHS of Rules.

**Attributes**

- `predicate` (`str`) - the predicate of the statement, e.g. isa, hero, needs
- `terms` (`listof Term`) - list of terms (Variable or Constant) in the statement, e.g. `'Nosliw'` or `'?d'`

### Term

Represents a term (a Variable or Constant) in our knowledge base. It could be thought of as a super class of Variable and Constant, though there is no actual inheritance implemented in the code.

**Attributes**

- `term` (`Variable|Constant`) - The Variable or Constant that this term holds (represents)

### Variable

Represents a variable used in statements, e.g. `?x`.

**Attributes**

- `element` (`str`): The name of the variable, e.g. `'?x'`

### Constant

Represents a constant used in statements

**Attributes**

- `element` (`str`): The value of the constant, e.g. `'Nosliw'`

### Binding

Represents a binding of a constant to a variable, e.g. `'Nosliw'` might be bound to `'?d'`

**Attributes**

- `variable` (`str`): The name of the variable associated with this binding, e.g. `'?d'`
- `constant` (`str`): The value of the variable, e.g. `'Nosliw'`

### Bindings

Represents Binding(s) used while matching two statements

**Attributes**

- `bindings` (`listof Bindings`) - bindings involved in match
- `bindings_dict` (`dictof Bindings`) - bindings involved in match where key is bound variable and value is bound value, e.g. some_bindings.bindings_dict['?d'] => 'Nosliw'

**Methods**

- `add_binding(variable, value)` (`(Variable, Constant) => void`) - add a binding from a variable to a value
- `bound_to(variable)` (`(Variable) => Variable|Constant|False`) - check if variable is bound. If so return value bound to it, else False
- `test_and_bind(variable_verm,value_term)` (`(Term, Term) => bool`) - Check if variable_term already bound. If so return whether or not passed in value_term matches bound value. If not, add binding between variable_terma and value_term and return True.

### ListOfBindings

Container for multiple Bindings

**Methods**

- `add_bindings(bindings, facts_rules)` - (`(Bindings, listof Fact|Rule) => void`) - add given bindings to list of Bindings along with associated rules or facts

## read.py

This file has no classes but defines useful helper functions for reading input from the user or a file.

**Functions**

- `read_tokenize(file)` - (`(str) => (listof Fact, listof Rule)`) - takes a filename, reads the file and returns a fact list and rule list.
- `parse_input(e)` - (`(str) => (int, str | listof str)`) - parses input, cleaning it as it does and assigning labels

## util.py

This file has no classes but defines useful helper functions.

**Functions**

- `is_var(var)` (`(str|Variable|Constant|Term) => bool`) - check whether an element is a variable (either instance of Variable or string starting with `'?'`, e.g. `'?d'`)
- `match(state1, state2, bindings=None)` (`(Statement, Statement, Bindings) => Bindings|False`) - match two statements and return the associated bindings or False if there is no binding
- `match_recursive(terms1, terms2, bindings)` (`(listof Term, listof Term, Bindings) => Bindings|False`) - recursive helper for match
- `instantiate(statement, bindings)` (`(Statement, Bindings) => Statement|Term`)  - generate Statement from given statement and bindings. Constructed statement has bound values for variables if they exist in bindings.
- `vprint(message, level, verbose, data=[])` (`(str, int, int, listof any) => void`) - prints message if verbose > level, if data provided then formats message with given data

## student_code.py

This file defines the two classes you must implement, KnowledgeBase and InferenceEngine.

### KnowledgeBase

Represents a knowledge base and contains the two methods described in the writeup (`Assert` and `Ask`)
