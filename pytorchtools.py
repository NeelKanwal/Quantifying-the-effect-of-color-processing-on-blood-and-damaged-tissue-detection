import numpy as np
import torch
import os
from datetime import datetime


class EarlyStopping_v2:
    """Early stops the training if validation loss doesn't improve after a given patience."""
    def __init__(self, patience=5, verbose=False, delta=0, path='checkpoint.pt', timestamp=0000, trace_func=print):
        self.patience = patience
        self.verbose = verbose
        self.counter = 0
        self.timestamp = timestamp
        self.best_score = None
        self.early_stop = False
        self.val_loss_min = np.Inf
        self.delta = delta
        self.path = path
        self.trace_func = trace_func
    def __call__(self, val_loss, model, epoch, timestamp, path):
        score = -val_loss
        if self.best_score is None:
            self.best_score = score
            self.save_checkpoint(val_loss, model, epoch, timestamp, path)
        elif score < self.best_score + self.delta:
            self.counter += 1
            self.trace_func(f'EarlyStopping counter: {self.counter} out of {self.patience}')
            if self.counter >= self.patience:
                self.early_stop = True
        else:
            self.best_score = score
            self.save_checkpoint(val_loss, model, epoch, timestamp, path)
            self.counter = 0
    def save_checkpoint(self, val_loss, model, epoch, timestamp, path):
        path_w = f"{path}/model_checkpoints"
        if not os.path.exists(os.path.join(os.getcwd(), path_w)):
            os.mkdir(os.path.join(os.getcwd(), path_w))
            print("\nDirectory for model checkpoints created.")
        sav_path = f"{path_w}/Epoch:{epoch}_{timestamp}.dat"
        if self.verbose:
            self.trace_func(f'Validation loss decreased ({self.val_loss_min:.3f} --> {val_loss:.3f}). \nSaving model to path...{sav_path}')
        state_dict = model.state_dict()
        torch.save({'model': state_dict}, sav_path)
        self.val_loss_min = val_loss