import collections

class ClassAssocationRule():

    """ClassAssociationRule (CAR) is defined by:

    1) antecedent(Item/a set of items that a Transaction has to satisfy)
    2) consequent(Target class of a Transaction that antecedent, one item)
    3) support(how many transactions satisfy the rule approcimately)
    4) confidence(support[antecedent+consequent]/support[antecedent]);relative
       degree of certainty that consequent holds given antecedent
    5) id 

    
    __lt__ (lesser than) and __gt__ (greater than) operators are overriden for sorting of cars list
    
    
    Parameters
    ----------
    antecedent: Antecedent
    consequent: Consequent
    support: float
    confidence: float
        
    Attributes
    ----------
    antecedent
    consequent
    support
    confidence
    rid: int (rule id)
    support_count: int (absolute support count)
    marked: bool
    class_cases_covered: collections.Counter (counter for determining which transactions arecovered by the antecedent)
    replace: set of ClassAssociationRule (set of rules that have higher precedence than this rule and can replace it in M2Classi.)
    """

    id = 0

    def __init__(self, antecedent, consequent, support, confidence):
        self.antecedent = antecedent
        self.consequent = consequent
        self.support = support
        self.confidence = confidence
        self.rulelen = len(antecedent) + 1
        self.rid = ClassAssocationRule.id

        ClassAssocationRule.id += 1

        self.support_count = 0
        
        self.marked = False
        
        self.class_cases_covered = collections.Counter()
        self.replace = set()
        
        
    def __gt__(self, other):
        """
        refers to "greater than" and is a precedence operator.
        Checking if this rule has higher precedence.
        FYI rules have hierarchy according confidence, support, length and id.
        """
        if (self.confidence > other.confidence):
            return True
        elif (self.confidence == other.confidence and
              self.support > other.support):
            return True
        elif (self.confidence == other.confidence and
              self.support == other.support and
              self.rulelen < other.rulelen):
            return True
        elif(self.confidence == other.confidence and
              self.support == other.support and
              self.rulelen == other.rulelen and
              self.rid < other.rid):
            return True
        else:
            return False
    
    def __lt__(self, other):
        """
        refers to "lesser than", a rule precedence operator
        """
        return not self > other
    
    def __len__(self):
        """
        returns the length of this rule 
        """
        return len(self.antecedent) + len(self.consequent)


    def __repr__(self):
        args = [self.antecedent.string(), "{" + self.consequent.string() + "}", self.support, self.confidence, self.rulelen, self.rid]
        text = "CAR {} => {} sup: {:.2f} conf: {:.2f} len: {}, id: {}".format(*args)

        return text
