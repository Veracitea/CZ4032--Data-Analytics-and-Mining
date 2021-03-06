from .Mine_Classi_Alg import (
    M2Classi,
    generateCARs,
    CARlist,
    top_rules
)
from .Structure import TransactionDB


class CBA():
    """Class for training a testing the
    CBA Algorithm.

    Parameters:
    -----------
    support : float
    confidence : float
    algorithm : string
        Algorithm for building a classifier.
    maxlen : int
        maximum length of mined rules
    """

    def __init__(self, support=0.10, confidence=0.5, maxlen=10, algorithm="m2"):
        if 0 > support or support > 1:
            raise Exception("support must be on the interval <0;1>")
        if 0 > confidence or confidence > 1:
            raise Exception("confidence must be on the interval <0;1>")
        if maxlen < 1:
            raise Exception("maxlen cannot be negative or 0")

        self.support = support * 100
        self.confidence = confidence * 100
        self.algorithm = algorithm
        self.maxlen = maxlen
        self.pre = None
        self.target_class = None

        self.available_algorithms = { #REQUIRED FOR PYFIN DO NOT REMOVE
            "m2": M2Classi
        }

    def rule_model_accuracy(self, txns):
        """Takes a TransactionDB and outputs
        accuracy of the classifier
        """
        if not self.pre:
            raise Exception("CBA must be trained using fit method first")
        if not isinstance(txns, TransactionDB):
            raise Exception("txns must be of type TransactionDB")

        return self.pre.test_transactions(txns)

    def fit(self, transactions, top_rules_args={}):
        """Trains the model based on input transaction
        and returns self.
        """
        if not isinstance(transactions, TransactionDB):
            raise Exception("transactions must be of type TransactionDB")

        self.target_class = transactions.header[-1]

        used_algorithm = self.available_algorithms[self.algorithm]

        cars = None

        if not top_rules_args:
            cars = generateCARs(transactions, support=self.support, confidence=self.confidence, maxlen=self.maxlen)
        else:
            rules = top_rules(transactions.string_representation, appearance=transactions.appeardict, **top_rules_args)
            cars = CARlist(rules)

        self.pre = used_algorithm(cars, transactions).build()

        return self

    def predict(self, X):
        """Method that can be used for predicting
        classes of unseen cases.

        CBA.fit must be used before predicting.
        """
        if not self.pre:
            raise Exception("CBA must be train using fit method first")

        if not isinstance(X, TransactionDB):
            raise Exception("X must be of type TransactionDB")

        return self.pre.predict_all(X)

    def predict_probability(self, X):
        """Method for predicting probablity of
        given classification
??
        CBA.fit must be used before predicting probablity.
        """

        return self.pre.predict_probability_all(X)

    def predict_matched_rules(self, X):
        """for each data instance, returns a rule that
        matched it according to the CBA order (sorted by
        confidence, support and length)
        """

        return self.pre.predict_matched_rule_all(X)




