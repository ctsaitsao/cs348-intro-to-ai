# Assignment 5 - NLG 101

## Introduction
You are going to build a simple NLG system that is able to generate collections of sentences based the results of queries (ASKs) of a knowledge base (bootstrapped from facts.txt).

As usual, you will do your work in student_code.py. The test file for this assignment is tests.py, and the tests print out more verbose feedback than usual. Look at the tests to see what sort of sentences you should be generating.

### Function: SAY
Your first step is to take a look at the function SAY that takes a knowledge base and a statement and generates a sentence in English. SAY uses patterns associated with predicates to map statements onto sentences.  This generator simply takes a single fact and produces the sentence that expresses it.

A set of initial patterns are in the file language.txt. Each line is a predicate and the simple sentence that expresses it. The elements of the pattern are either constants (words) or references to arguments in the statement.

At this point:

* (on block1 block2) should map onto "Block1 is on block2."
* (knows person1 person2) will map onto "Person1 knows Person2."

Of course, we know that this second sentence isn't quite right. In order to correct this, you are going to add a check on each literal that first determines what the object is and then how to express it. The first piece of this involves using ASK to get the INST of the object and then checking to see if there is a specific method for expressing object of that type.

In the KB, there are facts about how to express different things that you can use to look things up.

After this:

* (knows person1 person2) should map onto "Bob knows Sam."

### Function: SAY_object
The function SAY currently calls SAY_object with the knowledge base and object. SAY_object currently returns the object but you are going to change it to return the term that is the appropriate reference for the object. Note that the code in the function currently looks up the INST of the object. You need to follow this to find the EXPRESS of the object and then, if there is a way to express it, the feature that is referenced. You will then return the features for that object in particular.

### Function: SAY_multiple (and SAY_reference)
Next, you want to deal with pronouns. To do this, you are going to use SAY_Multiple. It takes a list of statements to be generated and invokes SAY on each of them. But before it does so, it pulls the "focus" out of the first statement that is then handed to SAY. This becomes the "context" or "object_context." SAY, as it stands, already calls SAY_reference with an object and context. Right now, SAY_reference just returns the object and you need to modify it to return the appropriate pronoun when the object and the object_context match.

We are testing this against both people and objects.

### Function: INTRODUCE
You will now need to build INTRODUCE, a function that takes the unique identifier for an object (Block1, Person1, Table1) and writes a definition of it in English. Define will only make use of statements in the KB related to intrinsic features of an object (INST, SIZE, COLOR, HEIGHT, etc.) rather than relationships (ON, IN, INCLUDED, KNOWS, etc.).

To get to these, we can use the "kb_mentioned" method that takes a string that is the unique identifier for an object and returns all facts in the DB that reference that object. You are going to have to do a few things.  

* First,  you want to start making a distinction between features and relationships. If means building and running a query like the one in SAY_object.
* Then order the statements by their priority in English.
* Then using "INST" as the framework generate a sentence using your features as modifiers.

At the end of this, the following statements:

(INST Block2 Block)
(SIZE Block2 Large)
(COLOR Block2 Green)

Should generate:

"Block2 is a Large Green Block."

and

(INST Block1 Block)
(COLOR Block1 Red)
(SIZE Block1 Small)

Should generate:

"Block1 is a Small Red Block."

### Function: DESCRIBE
Once this is running, you want to write DESCRIBE that is like INTRODUCE but adds in statements that are relationships. That is, DESCRIBE will mention that Block1 is on Block2 and generate the language for it.

Of course, you have already mentioned one of the blocks so you need to figure out how to refer to it with a pronoun.

Given the facts in the KB, this means that passing "Block2" to DESCRIBE should end up with:

"Block2 is a Large Green Block. It is on top of Block2."
