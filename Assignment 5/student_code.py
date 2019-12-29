import reader, kb
from logical_classes import *

ADJ_ORDER = ["QUANTITY", "QUALITY", "SIZE", "AGE", "SHAPE", "COLOR", "PROPER", "PURPOSE"]

def SAY(knowbase, statement, context=False):
    index = statement.predicate
    text = statement.terms
    pattern = knowbase.kb_find_pattern(index)
    sentence = []

    # Used to track where you are in the statement to help determine the role that an object plays
    role = 0

    if pattern:
        first = True
        for p in pattern:
            if isinstance(p,int):

                object = text[p-1].term.element

                # Once you have an object, decide if you are going to refer to it with a pronoun
                object = SAY_reference(knowbase, object, context, role)

                role = role + 1

                # Say the object using direction from its type
                object = SAY_object(knowbase, object)

                if first:
                    object = object.capitalize()
                    first = False

                sentence.append(object)
            else:
                object = SAY_object(knowbase,p)

                if first:
                    object = object.capitalize()
                    first = False
                sentence.append(object)

        sentence_string = " ".join(sentence)+"."
        print("Generating from:", str(statement), "->\t",  sentence_string)
        return sentence_string
    else:
        return False


def SAY_object(knowbase, object):
    # Get what the object's TYPE is using INST
    query =["INST", object, "?X"]
    binds = knowbase.kb_ask(Fact(query))
    if binds == False:
        return object
    else:
        bind = binds[0]
        type = bind.bound_to(Variable("?X")).element

    # Step 1:
    # Now you have to get the feature used to "EXPRESS" this TYPE
    # If there is a way to EXPRESS this TYPE, now you look it up
    # The form looks similar to the query for INST above

    e_query = ["EXPRESS", type, "?X"]
    e_binds = knowbase.kb_ask(Fact(e_query))
    if e_binds == False:
        return object
    else:
        e_bind = e_binds[0]
        feat = e_bind.bound_to(Variable("?X")).element

    # Step 2:
    # And then you look up the value of the feature that you will use to refer to this object
    # Again, the form is generally similar to INST query above

    v_query = [feat, object, "?X"]
    v_binds = knowbase.kb_ask(Fact(v_query))
    if v_binds == False:
        return object 
    else:
        v_bind = v_binds[0]
        value = v_bind.bound_to(Variable("?X")).element 

    # Finally, return the value
    return value

def SAY_Mulitiple(knowbase, statements):
    focus = statements[0].terms[0].term.element
    output = [SAY(knowbase,statements[0])]
    # print(output)
    for statement in statements[1:]:
        output.append(SAY(knowbase,statement,focus))
    return output


def SAY_reference(knowbase, object, object_context, position):

    roles = ["?S", "?O", "?P"] # forms: subject, (direct) object, possessive

    # If the object var is the same as the object_context,
    # then we want to get a pronoun for it.
    if object == object_context:
        # The first step is to get its gender.
        query = ["GENDER", object, "?X"]
        bind = knowbase.kb_ask(Fact(query))
        if bind:
            gender = bind[0].bound_to(Variable("?X")).element
        else:
            gender = "NEUTRAL"

        # Now that we've got the gender, we have to use it to get the
        # relevant REFERENCE from the knowledgebase
        # in general, the form looks quite similar to the few lines above

        # Step 1:
        # construct a query

        r_query = ["REFERENCE", gender, "?X", "?Y", "?Z"]

        # Step 2:
        # use kb_ask to get back binds

        r_bind = knowbase.kb_ask(Fact(r_query))
        if r_bind == False:
            return object
        else:
            subj = r_bind[0].bound_to(Variable("?X")).element
            obj = r_bind[0].bound_to(Variable("?Y")).element
            poss = r_bind[0].bound_to(Variable("?Z")).element

        # Step 3: write a couple of lines to
        # use the roles, position and bind together
        # to extract and return a replacement for object

        if position == 0:
            return subj
        elif position == 1:
            return obj
        else:
            return poss

    else:
        # if the object is not the same as the object_context,
        # we just want to return it
        return object


def INTRODUCE(kb, object):
    statements = kb.kb_mentioned(object)

    ordered = [0]*8
    intro_lst = []

    for i in range(len(statements)):    
        trm = statements[i].statement.terms[1]
        pred = statements[i].statement.predicate
        el = trm.term.element
        e_query = ["INST", el, "?X"]
        binds = kb.kb_ask(Fact(e_query))
        if pred == "INST":
            ordered.append(statements[i]) 
        if binds ==  True:
            statements.remove(statements[i])   
        else:
            for quality in ADJ_ORDER:
                if pred == quality:
                    ind = ADJ_ORDER.index(quality)
                    ordered[ind] = statements[i]

    for j in range(len(ordered)):   
        if ordered[j] == False:
            continue
        else:
            trm_2 = ordered[j].statement.terms[1]
            el_2 = trm_2.term.element
            intro_lst.append(trm_2.term.element)
    introduce = ' '.join(intro_lst)

    sentence = str(object) + " is a " + str(introduce) + '.'
    # print(sentence)
    return sentence

def DESCRIBE(kb, object):   # NOT GRADED
    statements = kb.kb_mentioned(object)
    print("<<NOT YET IMPLEMENTED>>")
    return ["a","b"]