import read, copy
from util import *
from logical_classes import *

verbose = 0

class KnowledgeBase(object):
    def __init__(self, facts=[], rules=[]):
        self.facts = facts
        self.rules = rules
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
                    ind = self.rules.index(fact_rule)
                    self.rules[ind].asserted = True

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
        print("Asking {!r}".format(fact))
        if factq(fact):
            f = Fact(fact.statement)
            bindings_lst = ListOfBindings()
            # ask matched facts
            for fact in self.facts:
                binding = match(f.statement, fact.statement)
                if binding:
                    bindings_lst.add_bindings(binding, [fact])

            return bindings_lst if bindings_lst.list_of_bindings else []

        else:
            print("Invalid ask:", fact.statement)
            return []

    def kb_retract(self, fact):
        """Retract a fact from the KB

        Args:
            fact (Fact) - Fact to be retracted

        Returns:
            None
        """
        printv("Retracting {!r}", 0, verbose, [fact])
        
        ####################################################
        # Student code goes here
     
        if len(fact.supported_by) != 0:    # check if asserted first
            if fact.asserted:
                fact.asserted = False
            return

        if factq(fact):     # if "fact" is a fact
            fact = self._get_fact(fact)
            if fact:
                found = fact
                while found.supported_by:
                    found = found.supported_by[0][0]
                if (found != fact) and found.asserted:
                    return
                self.facts.remove(fact)
        else:   # else, aka "fact" is a rule
            fact = self._get_rule(fact)
            if fact:
                if fact.asserted:
                    return
                self.rules.remove(fact)

        for found_rule in fact.supports_rules:  # deletes inferred rules
            for fact_and_rule in found_rule.supported_by:
                # if found_rule in fact_and_rule:
                fact_and_rule.remove(fact)
                found_rule.supported_by.remove(fact_and_rule)
            if not found_rule.asserted:
                self.kb_retract(found_rule)                

        for found_fact in fact.supports_facts:  # deletes inferred facts
            for fact_and_rule in found_fact.supported_by:
                # if found_fact in fact_and_rule:
                fact_and_rule.remove(fact)
                found_fact.supported_by.remove(fact_and_rule)
            if not found_fact.asserted and len(found_fact.supported_by) < 2: 
                self.kb_retract(found_fact)


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
        ####################################################
        # Student code goes here
        
        binding = match(rule.lhs[0], fact.statement)
        lhs_element = []

        if binding:

            instance = instantiate(rule.rhs, binding)

            if (len(rule.lhs) > 1):

                for element in rule.lhs[1:]:
                    lhs_element.append(instantiate(element, binding))

                instance_rule = Rule([lhs_element, instance], [[fact, rule]])
                rule.supports_rules.append(instance_rule)
                fact.supports_rules.append(instance_rule)
                kb.kb_assert(instance_rule)

                return

            instance_fact = Fact(instance, [[fact, rule]])
            fact.supports_facts.append(instance_fact)
            rule.supports_facts.append(instance_fact)
            kb.kb_assert(instance_fact)