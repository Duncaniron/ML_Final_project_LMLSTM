from sklearn.neighbors import KNeighborsClassifier
from sklearn.preprocessing import StandardScaler
from sklearn.decomposition import PCA
import os
import numpy as np
import logging

class KNN:
    def __init__(self, n, angle):
        self.model = KNeighborsClassifier(n_neighbors=n, metric="cityblock")
        self.angle = angle

    def _remove_landmark(self, data, part):
        if part == 'mouth':
            newdata = np.concatenate((data[:48], data[68]))
        elif part == 'eyebrow':
            newdata = np.concatenate((data[:17], data[27:]))
        else:
            logging.error('Parts can only be mouth or eyebrow!!!')

        return newdata
    
    def _data_preprocessing(self, data):
        #scaler = StandardScaler()
        #data = scaler.fit_transform(data)

        return data

    def load_data(self, filepath):
        self.x_train = []
        self.y_train = []
        self.map = dict()
        self.people_idx = dict()
        people = set()
        filepath = os.path.join(filepath, str(self.angle))
        for root, dirs, files in os.walk(filepath):
            for name in files:
                person = os.path.split(root)[1]
                if person not in people:
                    people.add(person)
                    self.map[person] = len(people)
                path = os.path.join(root, name)
                data = np.load(path, allow_pickle=True)
                data = np.array(data)
                data = self._remove_landmark(data, 'eyebrow')
                data = data.flatten()
                self.x_train.append(data)
                self.y_train.append(self.map[person])

    def train_model(self):
        self.x_train = self._data_preprocessing(self.x_train)
        self.pca = PCA(n_components=10)
        self.x_train = self.pca.fit_transform(self.x_train)
        self.model.fit(self.x_train, self.y_train)

    def predict(self, landmark):
        landmark = self._remove_landmark(landmark, 'eyebrow')
        landmark = landmark.flatten().reshape(-1, 1).reshape(1, -1)
        landmark = self._data_preprocessing(landmark)
        landmark = self.pca.transform(landmark)
        idx = self.model.predict(landmark)
        set_margin = 35                 # set margin for determine intruder
        for key in self.map:
            if self.map[key] == idx:
                name = key
                break
        margin_avg = self._get_margin(landmark, idx)
        if margin_avg > set_margin:
            name = "Intruder"
        return name 

    def _get_margin(self, landmark, idx):
        distances, neighbors = self.model.kneighbors(landmark, return_distance=True)
        distances = distances[0]
        neighbors = neighbors[0]
        margin = 0
        count = 0
        for neighbor, distance in zip(neighbors, distances):
            if idx[0] == self.y_train[neighbor]:
                margin += distance
                count += 1
        margin_avg = margin / count
        return margin_avg

test = KNN(1, 14)
test.load_data('./example/landmark_nba')
