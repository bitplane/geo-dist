import matplotlib.pyplot as plt
from IPython.display import clear_output
from keras.callbacks import Callback


class PlotLosses(Callback):
    def on_train_begin(self, logs={}):
        self.losses = []
        self.val_losses = []

    def on_epoch_end(self, epoch, logs={}):
        self.losses.append(logs.get("loss"))
        self.val_losses.append(logs.get("val_loss"))

        clear_output(wait=True)
        plt.plot(self.losses, label="loss")
        plt.plot(self.val_losses, label="val_loss")
        plt.legend()
        plt.show()


plot_losses = PlotLosses()
