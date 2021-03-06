"""
Activation functions for the layers of the MLP.
"""

import numpy as np
from scipy.special import expit #sigmoide

#%%% ACTIVATION FUCNTIONS %%%
# Sigmoid function
sigmoid = lambda x, a : expit(a * x)
sigmoid_derivative = lambda x, a : a * expit(a * x) * (1 - expit( a * x ))
# Linear function
lin = lambda x, a : a * x
lin_der = lambda x, a : a * x/x
# Relu
relu = lambda x, a : a * np.maximum(0, x)
relu_der = lambda x, a : a * np.heaviside(x, 1)
# Tanh
tanh = lambda x, a : np.tanh(a * x)
tanh_der = lambda x, a : a*(1 - np.tanh(a * x)**2)
# Elu
elu = lambda x, a: a * (np.exp(x) - 1) * np.heaviside(-x, 1) + \
                   x * np.heaviside(x, 1)
elu_der = lambda x, a : a * np.exp(x) * np.heaviside(-x, 1) + \
                        1 * np.heaviside(x, 1)
# Leaky relu
lrelu = lambda x, a: 0.01 * x * np.heaviside(-x, 1) + \
                     x * np.heaviside(x, 1)
lrelu_der = lambda x, a : 0.01 * x/x * np.heaviside(-x, 1) + \
                          1 * np.heaviside(x, 1)



def actv_funcs(f_name):
    """
    Function that given the activation function name return the relative
    activation function.

    Parameters
    ----------
    f_name : string
        The name of the function:
            - linear
            - sigmoid
            - relu
            - tanh
            - elu
            - lrelu

    Returns
    -------
    python function
        The activation function with name 'f_name'. If the input name doesn't
        exist the returned function is the sigmoid.
    """
    dict_actv = {"linear" : lin,
                 "sigmoid": sigmoid,
                 "relu"   : relu,
                 "tanh"   : tanh,
                  "elu"   : elu,
                  "lrelu"   : lrelu}
    if f_name not in dict_actv:
        print(f'Activation function {f_name} not found.', end = ' ')
        print(f'Adding the sigmoid activation function.')
    return dict_actv.get(f_name, sigmoid)

def dactv_funcs(f_name):
    """
    Function that given the activation function name return the relative
    derivative of the activation function.

    Parameters
    ----------
    f_name : string
        The name of the function:
            - linear
            - sigmoid
            - relu
            - tanh
            - elu

    Returns
    -------
    python function
        The derivative of the activation function with name 'f_name'. If the
        input name doesn't exist the returned function is the sigmoid.
    """
    derivative = {"linear" : lin_der,
                  "sigmoid": sigmoid_derivative,
                  "relu"   : relu_der,
                  "tanh"   : tanh_der,
                  "elu"    : elu_der,
                  "lrelu"   : lrelu_der}
    if f_name not in derivative:
        print(f'Activation function {f_name} not found.', end = ' ')
        print(f'Adding the derivative of sigmoid activation function.')
    return derivative.get(f_name, sigmoid_derivative)
