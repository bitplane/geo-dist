#!/usr/bin/env python3
"""
Training script for road distance prediction using raw coordinates,
with a large model architecture, GPU optimizations, and TensorBoard grid logging.
This script imports functions from model.py and GridImageCallback from view.py.
"""

import os
from datetime import datetime

import numpy as np
from geo_dist_prep.model.model import build_distance_model, load_training_data
from geo_dist_prep.model.view import GridImageCallback
from sklearn.model_selection import train_test_split
from tensorflow.keras import callbacks
from tensorflow.keras.mixed_precision import set_global_policy

# Enable mixed precision (set to 'float32' to disable)
set_global_policy("mixed_float16")

# --- Directory Setup ---
CACHE_DIR = ".cache"
LOGS_DIR = os.path.join(CACHE_DIR, "logs")
MODELS_DIR = os.path.join(CACHE_DIR, "models")
os.makedirs(LOGS_DIR, exist_ok=True)
os.makedirs(MODELS_DIR, exist_ok=True)
run_name = f"run_{datetime.now().strftime('%Y%m%d_%H%M%S')}"
LOG_DIR = os.path.join(LOGS_DIR, run_name)
MODEL_DIR = os.path.join(MODELS_DIR, run_name)
os.makedirs(LOG_DIR, exist_ok=True)
os.makedirs(MODEL_DIR, exist_ok=True)

DB_PATH = os.path.join(CACHE_DIR, "geonames.db")
DATABASE_URL = f"sqlite:///{DB_PATH}"


def main():
    print("Loading training data (raw coordinates only, no augmentation)...")
    X, y = load_training_data(DATABASE_URL)
    print(f"Loaded {X.shape[0]} samples with {X.shape[1]} features each.")

    # Split data into training and validation sets.
    X_train, X_val, y_train, y_val = train_test_split(
        X, y, test_size=0.2, random_state=42
    )

    # Compute region bounds from validation data's destination coordinates (columns 2 and 3).
    dest_lats = X_val[:, 2]  # lat2 values
    dest_lons = X_val[:, 3]  # lon2 values
    region_max_lat = np.max(dest_lats)
    region_min_lat = np.min(dest_lats)
    region_min_lon = np.min(dest_lons)
    region_max_lon = np.max(dest_lons)
    # Define region bounds as ((max_lat, min_lon), (min_lat, max_lon))
    region_bounds = ((region_max_lat, region_min_lon), (region_min_lat, region_max_lon))

    # Set your home coordinates as provided.
    home_coords = (53.667430, -2.955674)

    model = build_distance_model()
    model.summary()

    tensorboard_cb = callbacks.TensorBoard(log_dir=LOG_DIR)
    grid_cb = GridImageCallback(
        home_coords, region_bounds, grid_shape=(256, 256), log_dir=LOG_DIR, freq=1
    )
    cb_list = [tensorboard_cb, grid_cb]

    print("Starting training with GPU optimizations (mixed precision)...")
    _ = model.fit(
        X_train,
        y_train,
        validation_data=(X_val, y_val),
        epochs=500,
        batch_size=256,
        callbacks=cb_list,
    )

    model_save_path = os.path.join(MODEL_DIR, "trained_model_raw_features.keras")
    model.save(model_save_path)
    print(f"Model saved to {model_save_path}")


if __name__ == "__main__":
    main()
