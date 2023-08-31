import matplotlib.pyplot as plt
from IPython.display import clear_output
from keras.callbacks import Callback


class PlotLosses(Callback):
    def on_train_begin(self, logs={}):
        self.losses = []
        self.val_losses = []

    def on_epoch_end(self, epoch, logs={}):
        loss_mse = logs.get("loss")
        val_loss_mse = logs.get("val_loss")
        self.losses.append(loss_mse)
        self.val_losses.append(val_loss_mse)

        clear_output(wait=True)
        plt.plot(self.losses[2:], label="loss")
        plt.plot(self.val_losses[2:], label="val_loss")
        plt.legend()
        plt.yscale("log")
        plt.show()


plot_losses = PlotLosses()
