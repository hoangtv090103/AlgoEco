import csv

import numpy as np
from sklearn import neighbors
from sklearn.metrics import accuracy_score
from sklearn.model_selection import train_test_split

TARGET_NAMES = {"Iris-setosa": 0, "Iris-versicolor": 1, "Iris-virginica": 2}


def preprocess(dataset):
    dataset = np.array(list(dataset))  # covert to matrix
    dataset = np.delete(dataset, 0, 0)  # delete header
    dataset = np.delete(dataset, 0, 1)  # delete index
    return dataset


class KNearestNeighbor:
    def __init__(self, dataset=None, k=3):
        dataset = preprocess(dataset)
        self.k = k
        self.X = np.array(dataset[:, :-1], dtype=float)
        self.y = np.array([TARGET_NAMES[i] for i in dataset[:, -1]], dtype=int)
        self.labels = np.unique(
            ["Iris-setosa", "Iris-versicolor", "Iris-virginica"]
        )  # dataset.target_names
        self.X_train, self.X_test, self.y_train, self.y_test = train_test_split(
            self.X, self.y, test_size=0.2
        )
        self.y_prediction = self._get_prediction()
        self.test_labels = [self.labels[i] for i in self.y_test]
        self.pred_labels = [self.labels[i] for i in self.y_prediction]
        self.accuracy = accuracy_score(self.y_test, self.y_prediction)

    def _get_prediction(self):
        clf = neighbors.KNeighborsClassifier(n_neighbors=self.k, p=2)
        clf.fit(self.X_train, self.y_train)
        return clf.predict(self.X_test)


def run(path, k):
    dataset = csv.reader(open(path, "r"), delimiter=",")
    knn = KNearestNeighbor(dataset, k)
    print("Accuracy:", knn.accuracy)
    return knn.accuracy
