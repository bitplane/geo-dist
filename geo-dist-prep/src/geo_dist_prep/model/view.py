# geo_dist_prep/view.py
import numpy as np
import tensorflow as tf
from geo_dist_prep.model import preprocess_features


class GridImageCallback(tf.keras.callbacks.Callback):
    def __init__(
        self,
        home_coords,
        region_bounds,
        grid_shape=(256, 256),
        log_dir="./logs",
        freq=1,
    ):
        """
        Logs a 256x256 image grid to TensorBoard, where each pixel represents
        the predicted road distance from the given home coordinates.
        Also prints 10 random raw grid values for debugging.

        home_coords: (home_lat, home_lon) for your home.
        region_bounds: ((max_lat, min_lon), (min_lat, max_lon)) defining the region.
        grid_shape: Tuple defining the grid dimensions.
        log_dir: Directory for TensorBoard logs.
        freq: Log every 'freq' epochs.
        """
        super().__init__()
        self.home_coords = home_coords
        self.region_bounds = region_bounds
        self.grid_shape = grid_shape
        self.freq = freq
        self.file_writer = tf.summary.create_file_writer(log_dir)

    def on_epoch_end(self, epoch, logs=None):
        if (epoch + 1) % self.freq != 0:
            return

        (max_lat, min_lon), (min_lat, max_lon) = self.region_bounds
        lats = np.linspace(max_lat, min_lat, self.grid_shape[0])
        lons = np.linspace(min_lon, max_lon, self.grid_shape[1])
        mesh_lons, mesh_lats = np.meshgrid(lons, lats)
        flat_lats = mesh_lats.flatten()
        flat_lons = mesh_lons.flatten()

        home_lat, home_lon = self.home_coords
        # Build features for each grid point: [home_lat, home_lon, grid_lat, grid_lon]
        features = np.array(
            [
                preprocess_features(home_lat, home_lon, lat, lon)
                for lat, lon in zip(flat_lats, flat_lons)
            ],
            dtype=np.float32,
        )
        preds = self.model.predict(features, verbose=0)
        grid = preds.reshape(self.grid_shape)

        # Robust normalization using the 1st and 99th percentiles.
        low = np.percentile(grid, 1)
        high = np.percentile(grid, 99)
        if high - low > 0:
            grid_clipped = np.clip(grid, low, high)
            grid_norm = (grid_clipped - low) / (high - low)
        else:
            grid_norm = np.zeros_like(grid)

        grid_image = grid_norm[np.newaxis, ..., np.newaxis]
        with self.file_writer.as_default():
            tf.summary.image("Road Distance Grid (Robust Norm)", grid_image, step=epoch)

        # Print 10 random raw grid values for debugging.
        flat_grid = grid.flatten()
        if flat_grid.size >= 10:
            indices = np.random.choice(flat_grid.size, 10, replace=False)
            print(f"Epoch {epoch + 1}: Random grid values: {flat_grid[indices]}")
        else:
            print(f"Epoch {epoch + 1}: Grid too small to sample random values.")
        print(f"Logged grid image at epoch {epoch + 1}")
