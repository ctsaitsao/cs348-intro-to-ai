import reader
import student_code
from logical_classes import *
from kb import KnowledgeBase

fact_file = "facts.txt"
language_file = "patterns.txt"

kb = KnowledgeBase([], [])
facts,rules = reader.read_and_tokenize_facts_and_rules(fact_file)
patterns = reader.read_patterns(language_file)

for item in facts:
	kb.kb_add(Fact(item))
for item in rules:
	kb.kb_add(Rule(item))
for pattern in patterns:
	kb.kb_add_pattern(pattern)

print("\n-----------------------------\n")
print("Generating the basics for all of the facts:\n")
for fact in kb.facts:
	student_code.SAY(kb, fact.statement)
print("\n-----------------------------")



score = 0

def testing_references_no_pronouns(test, testNum):
	statement = test[0]
	sentence = test[1]
	score = 0
	print("\nTEST SET",testNum,"- Generating/Testing using appropriate object references but no pronouns:\n")
	# print("Testing:", statement)
	language = student_code.SAY(kb, statement)
	print("\nScoring:")
	if language == sentence:
		score = score + 1
		print("Passed.")
	else:
		print("Failed. Expected:", sentence)
	print("\n---> Score on this test:", str(score), "out of 1")
	print("\n-----------------------------")
	return score

def testing_references_with_pronouns(tests, testNum):
	score = 0
	statements = tests[0]
	sentences = tests[1]
	print("\nTEST SET",testNum,"- Generating/Testing using appropriate references and with pronouns:\n")
	# print("Statement set is:", ", ".join([st.__str__() for st in statements]), "\n")

	language = student_code.SAY_Mulitiple(kb, statements)
	print("\nScoring:")
	for generated,sentence in zip(language,sentences):
		if generated == sentence:
			print("Passed:", sentence)
			score += 2
		else:
			print("Failed. Expected:",sentence)
	print("\n---> Score on this test:", str(score), "out of", str(len(sentences)*2))
	print("\n-----------------------------")
	return score

def testing_INTRODUCTION(kb, test, testNum):
	object = test[0]
	sentence = test[1]
	print("\nTEST SET",testNum,"- Testing INTRODUCTION:\n")
	generated = student_code.INTRODUCE(kb,object)
	print("\nScoring:")
	if sentence == generated:
		print("Passed:", sentence)
		print("\n---> Score on this test: 2 out of 2")
		print("\n-----------------------------")
		return 2
	else:
		print("Failed. Expected:", sentence)
		print("\n---> Score on this test: 0 out of 2")
		print("\n-----------------------------")
		return 0

def testing_DESCRIBE(kb, test, testNum):
	object = test[0]
	sentences = test[1]
	print("\nTEST SET",testNum,"- Testing DESCRIBE:\n")
	generated = student_code.DESCRIBE(kb,object)
	score = 0
	print("\nScoring:")
	for generated_sentence,sentence in zip(generated,sentences):
		if sentence == generated:
			print("Passed:", sentence)
			score += 1
		else:
			print("Failed. Expected:", sentence)
	print("\n---> Score on this test:",score,"out of",len(sentences))
	print("\n-----------------------------")
	return score

test =[Statement(["KNOWS", "per1", "per2"]),"Bob knows Sally."]
score += testing_references_no_pronouns(test, 1) # worth 1

tests = [[Statement(["KNOWS", "per1", "per2"]),Statement(["LOVES", "per1", "per2"]),Statement(["HATES", "per2", "per1"])],
		 ["Bob knows Sally.","He loves Sally.","Sally hates him."]] # worth 6
score += testing_references_with_pronouns(tests, 2)

tests = [[Statement(["COLOR", "Block1", "Red"]),Statement(["ON", "Block1", "Block2"])],
		 ["Block1 is Red.","It is on Block2."]] # worth 4
score += testing_references_with_pronouns(tests, 3)

test = ["Block1","Block1 is a Small Red Block."]
score += testing_INTRODUCTION(kb, test, 4) # worth 2

test = ["Block2","Block2 is a Large Green Block."]
score += testing_INTRODUCTION(kb, test, 5) # worth 2

# test = ["Block2",["Block2 is a Large Green Block.", "Block2 is on Block2."]]
# score += testing_DESCRIBE(kb, test, 6) # worth 2

print("\nFinal Score:", str(score), "(out of 15)")
