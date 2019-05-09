import random as rnd
import numpy as np

POOR = 1
GOOD = 2
EXCELLENT = 3

training = [
    ["Tom", np.array([6, 6, 6, 6, 6, 6]), EXCELLENT],
    ["Peter", np.array([1, 1, 1, 1, 1, 1]), POOR],
    ["Jane", np.array([3, 6, 4, 4, 4, 4]), GOOD],
    ["Jack", np.array([6, 2, 2, 5, 3, 3]), GOOD],
    ["Mary", np.array([4, 4, 5, 4, 3, 5]), GOOD],
    ["Phyllis", np.array([4, 2, 2, 6, 2, 3]), GOOD],
    ["Ron", np.array([2, 4, 3, 2, 1, 2]), POOR],
    ["Diane", np.array([5, 4, 6, 6, 4, 6]), EXCELLENT],
    ["Fiona", np.array([5, 5, 5, 5, 3, 5]), EXCELLENT],
    ["Rodger", np.array([2, 2, 2, 3, 2, 1]), POOR]
]

unknown = [
    ["Joy", np.array([3, 2, 2, 3, 4, 1])],
    ["Bob", np.array([6, 1, 1, 1, 1, 1])],
    ["Sam", np.array([2, 3, 2, 3, 6, 4])]
]


def dist(arr1, arr2, _norm=np.linalg.norm):
    if arr1.size != arr2.size:
        return False
    else:
        return _norm(arr1 - arr2)


def knn(entry, data):
    distances = np.empty((len(data), 2))

    for index in range(0, len(data)):
        distances[index][0] = data[index][2]
        distances[index][1] = dist(data[index][1], entry[1])

    # Some python sorcery to order array by the second column, ascending
    distances = distances[distances[:, 1].argsort()[::1]]

    result = np.zeros(3)
    for index in range(0, 3):
        result[int(distances[index][0] - 1)] += 1 / 3

    return result


def subspace_knn(entry, data, n):
    indexes = rnd.sample(range(1, 6), n)
    # I had some problems with sticky references, hence the following
    sub = np.copy(data)
    subentry = np.copy(entry)
    subentry[1] = entry[1][indexes]
    for index in range(0, len(data)):
        sub[index][1] = data[index][1][[indexes]]
    return knn(subentry, sub)


def print_result(entry, result):
    print(entry[0], " has the grades ", entry[1])
    print("The probabilities for different statuses are as follows:")
    print(" [Poor | Good | Excellent]\n", result, "\n")


print("1: Simple KNN:")
for vector in unknown:
    print_result(vector, knn(vector, training))

print("\n2: KNN with bagging and committee approach.")
print("The bagging chooses a random subset of between 2 and 8 feature vectors from the training data.")
print("Then, it calculates 300 of those subsets, and average out the results.")
print("I consider the training date too sparse for any weighing of votes to make sense.")

a = np.zeros(3)
for vector in unknown:
    for i in range(0, 300):
        a += knn(vector, rnd.sample(training, rnd.choice(range(3, len(training)))))
    a = a / 300
    print_result(vector, a)

print("\n3: KNN with subspace modeling and committee approach.")
print("2 to 5 of the grades, selected at random, are used for each iteration")
print("This is done by creating a mask for the feature vector, and then applying it equally")
a = np.zeros(3)
for vector in unknown:
    for i in range(0, 300):
        a += subspace_knn(vector, training, rnd.choice(range(2, 6)))
    a = a / 300
    print_result(vector, a)

print("4: It would seem that where simple KNN gives probabilities in multiples of 1/k, bagging gives greater variance,")
print("while I saw subspace modelling give a probability of more than 90% over 300 averaged iterations...")
print("With a training set this small, it's really hard to say anything conclusively, but I would wager both bagging")
print("and subspace are more useful than simple KNN.")
