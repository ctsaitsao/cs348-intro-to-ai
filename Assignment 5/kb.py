from util import *
from logical_classes import *

verbose = 1

class KnowledgeBase(object):
    def __init__(self, facts=[], rules=[]):
        self.facts = facts
        self.rules = rules
        self.patterns = dict()
        self.ie = InferenceEngine()

    def __repr__(self):
        return 'KnowledgeBase({!r}, {!r})'.format(self.facts, self.rules)

    def __str__(self):
        string = "Knowledge Base: \n"
        string += "\n".join((str(fact) for fact in self.facts)) + "\n"
        string += "\n".join((str(rule) for rule in self.rules))
        return string

    def _get_fact(self, fact):
        """INTERNAL USE ONLY
        Get the fact in the KB that is the same as the fact argument

        Args:
            fact (Fact): Fact we're searching for

        Returns:
            Fact: matching fact
        """
        for kbfact in self.facts:
            if fact == kbfact:
                return kbfact

    def _get_rule(self, rule):
        """INTERNAL USE ONLY
        Get the rule in the KB that is the same as the rule argument

        Args:
            rule (Rule): Rule we're searching for

        Returns:
            Rule: matching rule
        """
        for kbrule in self.rules:
            if rule == kbrule:
                return kbrule

    def kb_add(self, fact_rule):
        """Add a fact or rule to the KB

        Args:
            fact_rule (Fact|Rule) - the fact or rule to be added

        Returns:
            None
        """
        printv("Adding {!r}", 1, verbose, [fact_rule])
        if isinstance(fact_rule, Fact):
            if fact_rule not in self.facts:
                self.facts.append(fact_rule)
                for rule in self.rules:
                    self.ie.fc_infer(fact_rule, rule, self)
            else:
                if fact_rule.supported_by:
                    ind = self.facts.index(fact_rule)
                    for f in fact_rule.supported_by:
                        self.facts[ind].supported_by.append(f)
                else:
                    ind = self.facts.index(fact_rule)
                    self.facts[ind].asserted = True

        elif isinstance(fact_rule, Rule):
            if fact_rule not in self.rules:
                self.rules.append(fact_rule)
                for fact in self.facts:
                    self.ie.fc_infer(fact, fact_rule, self)
            else:
                if fact_rule.supported_by:
                    ind = self.rules.index(fact_rule)
                    for f in fact_rule.supported_by:
                        self.rules[ind].supported_by.append(f)
                else:
                    ind = self.facts.index(fact_rule)
                    self.facts[ind].asserted = True

    def kb_remove(self, fact_rule):
        """Remove a fact or rule from the KB

        Args:
            fact_rule (Fact|Rule) - the fact or rule to be added

        Returns:
            None
        """
        printv("Removing {!r}", 1, verbose, [fact_rule])
        if fact_rule.supported_by:
            printv("Not removed because supported by other facts/rules", 0, verbose)
            if fact_rule.asserted:
                fact_rule.asserted = False
            return

        if isinstance(fact_rule, Fact) and fact_rule in self.facts:
            if fact_rule.supports_facts:
                printv("Removing supported facts", 1, verbose)
                for dependent in fact_rule.supports_facts:
                    for fact,rule in dependent.supported_by:
                        if fact == fact_rule:
                            dependent.supported_by.remove([fact,rule])
                    if len(dependent.supported_by) == 0 and not dependent.asserted:
                        self.kb_remove(dependent)
            if fact_rule.supports_rules:
                if verbose > 1: print("Removing supported rules")
                for dependent in fact_rule.supports_rules:
                    for fact,rule in dependent.supported_by:
                        if fact == fact_rule:
                            dependent.supported_by.remove([fact,rule])
                    if len(dependent.supported_by) == 0 and not dependent.asserted:
                        self.kb_remove(dependent)
            self.facts.remove(fact_rule)

        elif isinstance(fact_rule, Rule) and fact_rule in self.rules:
            if fact_rule.supports_facts:
                printv("Removing supported facts", 1, verbose)
                for dependent in fact_rule.supports_facts:
                    for fact,rule in dependent.supported_by:
                        if rule == fact_rule:
                            dependent.supported_by.remove([fact,rule])
                    if len(dependent.supported_by) == 0 and not dependent.asserted:
                        self.kb_remove(dependent)
            if fact_rule.supports_rules:
                printv("Removing supported rules", 1, verbose)
                for dependent in fact_rule.supports_rules:
                    for fact,rule in dependent.supported_by:
                        if rule == fact_rule:
                            dependent.supported_by.remove([fact,rule])
                    if len(dependent.supported_by) == 0 and not dependent.asserted:
                        self.kb_remove(dependent)
            self.rules.remove(fact_rule)

    def kb_assert(self, fact_rule):
        """Assert a fact or rule into the KB

        Args:
            fact_rule (Fact or Rule): Fact or Rule we're asserting
        """
        printv("Asserting {!r}", 0, verbose, [fact_rule])
        self.kb_add(fact_rule)

    def kb_ask(self, fact):
        """Ask if a fact is in the KB

        Args:
            fact (Fact) - Statement to be asked (will be converted into a Fact)

        Returns:
            listof Bindings|False - list of Bindings if result found, False otherwise
        """
        if isinstance(fact, Fact):
            bindings_lst = ListOfBindings()
            # ask matched facts
            for f in self.facts:
                binding = match(fact.statement, f.statement)
                if binding:
                    bindings_lst.add_bindings(binding, [f])
            return bindings_lst if bindings_lst.list_of_bindings else False
        else:
            print("Invalid ask:", fact)
            return False

            
            
    def kb_retract(self, fact):
        """Retract a fact from the KB

        Args:
            fact (Fact) - Fact to be retracted

        Returns:
            None
        """
        printv("Retracting {!r}", 0, verbose, [fact])
        if isinstance(fact, Fact):
            if fact in self.facts:
                kbf = self._get_fact(fact)
                self.kb_remove(kbf)
        else:
            print('Not a fact, not removed: %s' % (fact))


    def kb_mentioned(self, object):
        """Get all statements that reference this object in the KB

        Args:
            object

        Returns:
            list of facts in which the object is mentioned
        """
        mentions = []
        for f in self.facts:
            if f.statement.included(object):
                mentions.append(f)
        return mentions


    
    def kb_add_pattern(self, pattern):
        index = pattern[0]
        args = pattern[1].replace("\n","")
        args = args.replace("!arg","").split(" ")
        new_args =[]
        for arg in args:
        	try:
        		new_args.append(int(arg))
        	except:
        		new_args.append(arg)	
        patterns = self.patterns
        patterns[index]=new_args
 
        
    def kb_find_pattern(self, predicate):
        if predicate in self.patterns.keys():
            return self.patterns[predicate]



class InferenceEngine(object):
    def fc_infer(self, fact, rule, kb):
        """Forward-chaining to infer new facts and rules

        Args:
            fact (Fact) - A fact from the KnowledgeBase
            rule (Rule) - A rule from the KnowledgeBase
            kb (KnowledgeBase) - A KnowledgeBase

        Returns:
            Nothing
        """
        printv('Attempting to infer from {!r} and {!r} => {!r}', 1, verbose,
            [fact.statement, rule.lhs, rule.rhs])
        statement1 = fact.statement
        statement2 = rule.lhs[0]
        bindings = match(statement1, statement2)
        if len(rule.lhs) == 1 and bindings:
            new_fact = Fact(instantiate(rule.rhs, bindings), [[fact,rule]])
            print("INFERRING: ", str(new_fact), " FROM ", str(statement1), " AND ", str(rule))
            kb.kb_add(new_fact)
            new_fact = kb._get_fact(new_fact)
            fact.supports_facts.append(new_fact)
            rule.supports_facts.append(new_fact)
        elif bindings:
            new_lhs = []
            for statement in rule.lhs[1:]:
                new_lhs.append(instantiate(statement, bindings))
            new_rhs = instantiate(rule.rhs, bindings)
            new_rule = Rule([new_lhs, new_rhs], [[fact,rule]])
            kb.kb_add(new_rule)
            new_rule = kb._get_rule(new_rule)
            fact.supports_rules.append(new_rule)
            rule.supports_rules.append(new_rule)

	