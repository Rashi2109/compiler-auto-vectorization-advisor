import pandas as pd

from sklearn.tree import DecisionTreeClassifier
from sklearn.preprocessing import LabelEncoder


class MLPredictor:

    def __init__(self):

        self.model = DecisionTreeClassifier()

        self.label_encoder = LabelEncoder()

    def train_model(self):

        # Load dataset
        data = pd.read_csv(
            "app/ml/training_data.csv"
        )

        # Features
        X = data[
            [
                "dependency",
                "loop_size",
                "array_accesses"
            ]
        ]

        # Labels
        y = self.label_encoder.fit_transform(
            data["best_option"]
        )

        # Train model
        self.model.fit(X, y)

    def predict_best_optimization(
        self,
        dependency,
        loop_size,
        array_accesses
    ):

        prediction = self.model.predict(
            [[
                dependency,
                loop_size,
                array_accesses
            ]]
        )

        result = self.label_encoder.inverse_transform(
            prediction
        )

        return result[0]
