# src from here --------------------------------------------------------------------------------
# #!/usr/bin/env python3
# # Time-stamp: "2024-09-07 01:09:38 (ywatanabe)"
# 
# import os
# 
# import mngs
# import numpy as np
# 
# 
# class EarlyStopping:
#     """
#     Early stops the training if the validation score doesn't improve after a given patience period.
# 
#     """
# 
#     def __init__(
#         self, patience=7, verbose=False, delta=1e-5, direction="minimize"
#     ):
#         """
#         Args:
#             patience (int): How long to wait after last time validation score improved.
#                             Default: 7
#             verbose (bool): If True, prints a message for each validation score improvement.
#                             Default: False
#             delta (float): Minimum change in the monitored quantity to qualify as an improvement.
#                             Default: 0
#         """
#         self.patience = patience
#         self.verbose = verbose
#         self.direction = direction
# 
#         self.delta = delta
# 
#         # default
#         self.counter = 0
#         self.best_score = np.Inf if direction == "minimize" else -np.Inf
#         self.best_i_global = None
#         self.models_spaths_dict = {}
# 
#     def is_best(self, val_score):
#         is_smaller = val_score < self.best_score - abs(self.delta)
#         is_larger = self.best_score + abs(self.delta) < val_score
#         return is_smaller if self.direction == "minimize" else is_larger
# 
#     def __call__(self, current_score, models_spaths_dict, i_global):
#         # The 1st call
#         if self.best_score is None:
#             self.save(current_score, models_spaths_dict, i_global)
#             return False
# 
#         # After the 2nd call
#         if self.is_best(current_score):
#             self.save(current_score, models_spaths_dict, i_global)
#             self.counter = 0
#             return False
# 
#         else:
#             self.counter += 1
#             if self.verbose:
#                 print(
#                     f"\nEarlyStopping counter: {self.counter} out of {self.patience}\n"
#                 )
#             if self.counter >= self.patience:
#                 if self.verbose:
#                     mngs.gen.print_block("Early-stopped.", c="yellow")
#                 return True
# 
#     def save(self, current_score, models_spaths_dict, i_global):
#         """Saves model when validation score decrease."""
# 
#         if self.verbose:
#             print(
#                 f"\nUpdate the best score: ({self.best_score:.6f} --> {current_score:.6f})"
#             )
# 
#         self.best_score = current_score
#         self.best_i_global = i_global
# 
#         for model, spath in models_spaths_dict.items():
#             mngs.io.save(model.state_dict(), spath)
# 
#         self.models_spaths_dict = models_spaths_dict
# 
# 
# if __name__ == "__main__":
#     pass
#     # # starts the current fold's loop
#     # i_global = 0
#     # lc_logger = mngs.ml.LearningCurveLogger()
#     # early_stopping = utils.EarlyStopping(patience=50, verbose=True)
#     # for i_epoch, epoch in enumerate(tqdm(range(merged_conf["MAX_EPOCHS"]))):
# 
#     #     dlf.fill(i_fold, reset_fill_counter=False)
# 
#     #     step_str = "Validation"
#     #     for i_batch, batch in enumerate(dlf.dl_val):
#     #         _, loss_diag_val = utils.base_step(
#     #             step_str,
#     #             model,
#     #             mtl,
#     #             batch,
#     #             device,
#     #             i_fold,
#     #             i_epoch,
#     #             i_batch,
#     #             i_global,
#     #             lc_logger,
#     #             no_mtl=args.no_mtl,
#     #             print_batch_interval=False,
#     #         )
#     #     lc_logger.print(step_str)
# 
#     #     step_str = "Training"
#     #     for i_batch, batch in enumerate(dlf.dl_tra):
#     #         optimizer.zero_grad()
#     #         loss, _ = utils.base_step(
#     #             step_str,
#     #             model,
#     #             mtl,
#     #             batch,
#     #             device,
#     #             i_fold,
#     #             i_epoch,
#     #             i_batch,
#     #             i_global,
#     #             lc_logger,
#     #             no_mtl=args.no_mtl,
#     #             print_batch_interval=False,
#     #         )
#     #         loss.backward()
#     #         optimizer.step()
#     #         i_global += 1
#     #     lc_logger.print(step_str)
# 
#     #     bACC_val = np.array(lc_logger.logged_dict["Validation"]["bACC_diag_plot"])[
#     #         np.array(lc_logger.logged_dict["Validation"]["i_epoch"]) == i_epoch
#     #     ].mean()
# 
#     #     model_spath = (
#     #         merged_conf["sdir"]
#     #         + f"checkpoints/model_fold#{i_fold}_epoch#{i_epoch:03d}.pth"
#     #     )
#     #     mtl_spath = model_spath.replace("model_fold", "mtl_fold")
#     #     models_spaths_dict = {model_spath: model, mtl_spath: mtl}
# 
#     #     early_stopping(loss_diag_val, models_spaths_dict, i_epoch, i_global)
#     #     # early_stopping(-bACC_val, models_spaths_dict, i_epoch, i_global)
# 
#     #     if early_stopping.early_stop:
#     #         print("Early stopping")
#     #         break

# test from here --------------------------------------------------------------------------------
#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import os
import sys
from pathlib import Path
import pytest
import numpy as np

# Add project root to Python path
project_root = str(Path(__file__).parent.parent.parent.parent)
if project_root not in sys.path:
    sys.path.insert(0, os.path.join(project_root, "src"))

from mngs..ai.EarlyStopping import *

class Test_MainFunctionality:
    def setup_method(self):
        # Setup test fixtures
        pass

    def teardown_method(self):
        # Clean up after tests
        pass

    def test_basic_functionality(self):
        # Basic test case
        pass

    def test_edge_cases(self):
        # Edge case testing
        pass

    def test_error_handling(self):
        # Error handling testing
        pass
