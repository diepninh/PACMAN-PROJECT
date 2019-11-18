# mira.py
# -------
# Licensing Information:  You are free to use or extend these projects for
# educational purposes provided that (1) you do not distribute or publish
# solutions, (2) you retain this notice, and (3) you provide clear
# attribution to UC Berkeley, including a link to http://ai.berkeley.edu.
# 
# Attribution Information: The Pacman AI projects were developed at UC Berkeley.
# The core projects and autograders were primarily created by John DeNero
# (denero@cs.berkeley.edu) and Dan Klein (klein@cs.berkeley.edu).
# Student side autograding was added by Brad Miller, Nick Hay, and
# Pieter Abbeel (pabbeel@cs.berkeley.edu).


# Mira implementation
import util
PRINT = True

class MiraClassifier:
    """
    Mira classifier.
    Note that the variable 'datum' in this code refers to a counter of features
    (not to a raw samples.Datum).
    """
    def __init__( self, legalLabels, max_iterations):
        self.legalLabels = legalLabels
        self.type = "mira"
        self.automaticTuning = False
        self.C = 1
        self.legalLabels = legalLabels
        self.max_iterations = max_iterations*2
        self.initializeWeightsToZero()

    def initializeWeightsToZero(self):
        "Resets the weights of each label to zero vectors"
        self.weights = {}
        for label in self.legalLabels:
            self.weights[label] = util.Counter() # this is the data-structure you should use

    def train(self, trainingData, trainingLabels, validationData, validationLabels):
        "Outside shell to call your method. Do not modify this method."

        self.features = trainingData[0].keys() # this could be useful for your code later...

        if (self.automaticTuning):
            Cgrid = [0.002, 0.004, 0.008]
        else:
            Cgrid = [self.C]

        return self.trainAndTune(trainingData, trainingLabels, validationData, validationLabels, Cgrid)

    def trainAndTune(self, trainingData, trainingLabels, validationData, validationLabels, Cgrid):
        """
        This method sets self.weights using MIRA.  Train the classifier for each value of C in Cgrid,
        then store the weights that give the best accuracy on the validationData.
        Use the provided self.weights[label] data structure so that
        the classify method works correctly. Also, recall that a
        datum is a counter from features to values for those features
        representing a vector of values.
        """
        max_acc, max_C, max_weights = max([self.get_accuracy_c_weight( c, trainingData, trainingLabels, validationData, validationLabels ) for c in Cgrid])
        self.weights = max_weights

    def get_accuracy_c_weight(self, c, trainingData, trainingLabels, validationData, validationLabels ):
        weights = self.weights.copy()
        max_acc, max_weights = float('-inf'), None
        for iteration in range(self.max_iterations):
            print "Starting iteration ", iteration, "..."
            for i in range(len(trainingData)):
                f = trainingData[i]
                ytrue = trainingLabels[i]
                score_max, ypred = max([
                    (f * weights[y],y) for y in self.legalLabels])
                if ypred != ytrue:
                    tau = self.get_tau(c, weights[ypred], weights[ytrue], f)
                    ftau = f.copy()
                    for key in ftau.keys():
                        ftau[key] = 1.0 * ftau[key] * tau
                    weights[ytrue] += ftau
                    weights[ypred] -= ftau
            accuracy = self.get_accuracy(weights, validationData, validationLabels)
            if accuracy > max_acc:
                max_acc = accuracy
                max_weights = weights.copy()
            print "iteration", iteration, "c =", c, "accuracy =", accuracy
        return max_acc, c, max_weights

    def get_tau(self, c, wypred, wytrue, f):
        sub = wypred-wytrue
        nominator = sub*f+1
        denominator = f*f*2
        #print 'tmp', nominator, denominator, 1.0*nominator/denominator
        return min(c, 1.0*nominator/denominator)

    def get_accuracy(self, weights, validationData, validationLabels):
        count = 0.0
        for i in range(len(validationData)):
            f = validationData[i]
            ytrue = validationLabels[i]
            score_max, ypred = max([
                (f * weights[y],y) for y in self.legalLabels])
            if ypred == ytrue:
                count += 1
        return count / len(validationData)

    def classify(self, data ):
        """
        Classifies each datum as the label that most closely matches the prototype vector
        for that label.  See the project description for details.
        Recall that a datum is a util.counter...
        """
        guesses = []
        for datum in data:
            vectors = util.Counter()
            for l in self.legalLabels:
                vectors[l] = self.weights[l] * datum
            guesses.append(vectors.argMax())
        return guesses

