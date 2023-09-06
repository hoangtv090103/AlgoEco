from sklearn import datasets, neighbors
from pandas import DataFrame as df
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score


def preprocess(dataset):
    dataset = df(dataset)  # covert to matrix
    dataset = dataset.drop(0, 0)  # delete header
    dataset = dataset.drop(0, 1)  # delete index
    dataset = dataset.shuffle()
    return dataset


class KNearestNeighbor:
    def __init__(self, dataset=datasets.load_iris(), k=3):
        self.k = k
        self.X = dataset.data
        self.y = dataset.target
        self.labels = dataset.target_names
        self.X_train, self.X_test, self.y_train, self.y_test = train_test_split(self.X, self.y, test_size=0.2)
        self.y_prediction = self._get_prediction()
        self.test_labels = [self.labels[i] for i in self.y_test]
        self.pred_labels = [self.labels[i] for i in self.y_prediction]
        self.accuracy = accuracy_score(self.y_test, self.y_prediction)

    def _get_prediction(self):
        clf = neighbors.KNeighborsClassifier(n_neighbors=self.k, p=2)
        clf.fit(self.X_train, self.y_train)
        return clf.predict(self.X_test)
