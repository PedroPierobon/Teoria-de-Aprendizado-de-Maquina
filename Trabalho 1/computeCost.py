import numpy as np


def compute_cost(X, y, theta):
    # Initialize some useful values
    cost = 0

    # ===================== Your Code Here =====================
    # Instructions : Compute the cost of a particular choice of theta.
    #                You should set the variable "cost" to the correct value.
    

    # ==========================================================
    m = y.size
    model = X @ theta
    err = model - y
    err *= err
    sum_errs = err.sum()
    cost = sum_errs / (2*m)

    return cost
