# geo_dist_prep/model.py

import numpy as np
from geo_dist_prep.schemas.base import Base
from geo_dist_prep.schemas.training_data import TrainingData
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker


def preprocess_features(lat1, lon1, lat2, lon2):
    """
    Given two points, return the raw features as a 4-dimensional vector:
      [lat1, lon1, lat2, lon2]
    """
    return [lat1, lon1, lat2, lon2]


def load_training_data(database_url):
    """
    Loads training data from the TrainingData table without augmentation.
    Each sample returns raw features [lat1, lon1, lat2, lon2],
    and the target is row.distance.
    """
    engine = create_engine(database_url)
    Base.metadata.create_all(engine)
    Session = sessionmaker(bind=engine)
    session = Session()
    data = session.query(TrainingData).all()
    session.close()

    if not data:
        raise ValueError("No training data found in the database!")

    X_list = []
    y_list = []
    for row in data:
        X_list.append(preprocess_features(row.y1, row.x1, row.y2, row.x2))
        y_list.append(row.distance)
    X = np.array(X_list, dtype=np.float32)
    y = np.array(y_list, dtype=np.float32)
    return X, y


def build_distance_model():
    """
    Build a large feed-forward neural network for road distance prediction.
    The model accepts a 4-dimensional input (raw coordinates).
    """
    from tensorflow.keras import layers, models

    inputs = layers.Input(shape=(4,), name="features")
    x = layers.Dense(512, activation="relu")(inputs)
    x = layers.BatchNormalization()(x)
    x = layers.Dropout(0.4)(x)
    x = layers.Dense(256, activation="relu")(x)
    x = layers.BatchNormalization()(x)
    x = layers.Dropout(0.4)(x)
    x = layers.Dense(128, activation="relu")(x)
    x = layers.BatchNormalization()(x)
    x = layers.Dense(64, activation="relu")(x)
    x = layers.BatchNormalization()(x)
    x = layers.Dense(32, activation="relu")(x)
    output = layers.Dense(1, activation="linear", name="distance", dtype="float32")(x)
    model = models.Model(inputs=inputs, outputs=output)
    model.compile(optimizer="adam", loss="mean_squared_error", metrics=["mae"])
    return model
