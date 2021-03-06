"""
Function for the dataset splitting.
"""

import numpy as np

def split(input_matrix, labels, frac_training=0.8, kind="hold_out", k=4):
    """
    Splitting the data in three different set, one for training, one for
    validation, one for test. Each pattern of each set is selected randomly from
	the initial input_matrix.

    Parameters
    ----------
    input_matrix : numpy 2d array
        Input data matrix (containing also the labels) without the test set.
    frac_training : float
        Fraction of data to use in training, default is 0.8 .
    kind : string
        Kind of splitting ['hold_out, 'k_fold'], default is 'hold_out'.
    k : int
        Number of fold for k-fold splitting.

    Returns
    -------
    (numpy 2d array, numpy 2d array) if kind = 'hold-out'
    (numpy 2d array,  list of tuple) if kind = 'k-fold'
        If hold out return (train data matrix, validation data matrix).
        If k-fold return (data matrix, list of tuple containing 2 indexs).
        The index in the list represent the (idx1 = start, idx2 = stop) index
        to split for each fold. In order to not waste memory you can separate
        with this 2 index each train-val dataset before training the model.
        Note:
            to extract validation set just use the slicing: data[idx1, idx2]
            to extract train set just use
            numpy.delete(data, slice(idx1,idx2), axis = 0)

    """
    copy_data = np.copy(input_matrix) # Copy the dataset to not change original
#                                     # input_matrix
    copy_labels = np.copy(labels)     # Copy the labels to not change original
#                                     # labels
    if kind=="hold_out":
        idx=round(len(copy_data)*frac_training)
        # Data
        training_set=copy_data[0:idx,:]
        validation_set=copy_data[idx:,:]
        # Labels
        train_labels=copy_labels[0:idx,:]
        val_labels=copy_labels[idx:,:]
    elif kind=="k_fold":
        training_set, validation_set, train_labels, val_labels =k_fold(input_matrix, copy_labels, k)
    return training_set, validation_set, train_labels, val_labels


def function_counter(function):
    counter=-1
    def wrapper(*args,**kwargs):
        wrapper.counter+=1
        return function(*args,**kwargs)
    wrapper.counter=counter
    return wrapper

@function_counter
def k_fold(input_matrix, labels, k=4):
    """[Create a partition of the dataset in k-fold cross validation set and return the training set and the validation set for each fold recursively]

    Args:
        input_matrix ([type]): [description]
        k (int, optional): [description]. Defaults to 4.

    Returns:
        [numpy array], [numpy array], [numpy array], [numpy array]: [training set, validation set, train_labels, validation_labels]
    """
    if k < 2: raise Exception("Fold number must be greater than 2")
    idx_partition=int(len(input_matrix)/k)
    k_partition=k_fold.counter%k
    if k_partition<(k-1):
    	# Data
        training_set=np.delete(input_matrix, slice(k_partition*idx_partition,(k_partition+1)*idx_partition), axis=0)
        validation_set=input_matrix[k_partition*idx_partition:(k_partition+1)*idx_partition,:]
        # Labels
        train_labels=np.delete(labels, slice(k_partition*idx_partition,(k_partition+1)*idx_partition), axis=0)
        val_labels=labels[k_partition*idx_partition:(k_partition+1)*idx_partition,:]
    if k_partition==(k-1):
    	# Data
        training_set=np.delete(input_matrix, slice(k_partition*idx_partition,len(input_matrix)), axis=0)
        validation_set=input_matrix[k_partition*idx_partition:len(input_matrix),:]
        #Labels
        train_labels=np.delete(labels, slice(k_partition*idx_partition,len(input_matrix)), axis=0)
        val_labels=labels[k_partition*idx_partition:len(input_matrix),:]

    return training_set, validation_set, train_labels, val_labels


def k_fold_gen(input_matrix, labels, k=4):
    """[Create a partition of the dataset in k-fold cross validation set and return the training set and the validation set for each fold recursively]

    Args:
        input_matrix ([type]): [description]
        k (int, optional): [description]. Defaults to 4.

    Returns:
        [numpy array], [numpy array], [numpy array], [numpy array]: [training set, validation set, train_labels, validation_labels]
    """
    idx = int(len(input_matrix)/k)
    if k < 2: raise Exception("Fold number must be greater than 2")
    for i in range(k):
        if i <(k-1):
            end = (i+1)*idx
        elif i ==(k-1):
            end = len(input_matrix)
        else: end = -1
        # Data
        training_set=np.delete(input_matrix, slice(i*idx,end), axis=0)
        validation_set=input_matrix[i*idx:end,:]
        # Labels
        train_labels=np.delete(labels, slice(i*idx,end), axis=0)
        val_labels=labels[i*idx:end,:]
    
        yield training_set, validation_set, train_labels, val_labels

class StandardScaler:
    """
    Class for the normalization with respect to mean and std.
    """
    def __init__(self, kind = 'single'):
        """
        single
        vector
        """
        self.kind = kind

    def fit(self, data):
        self.mean = np.mean(data,axis=0)
        self.std = np.std(data,axis=0)
        if self.kind == 'vector':
            self.std = np.max(self.std)

    def fit_transform(self, data):
        self.fit(data)
        return self.transform(data)

    def transform(self, data):
        return ( data - self.mean ) / self.std

    def inverse_transform(self, data):
        return data*self.std+self.mean

class MinMaxScaler:
    """
    Class for the normalization in [0,1]
    """
    def fit(self, data):
        self.max=np.max(data,axis=0)
        self.min=np.min(data,axis=0)

    def fit_transform(self, data):
        self.fit(data)
        return self.transform(data)
    
    def transform(self, data):
        return (data-self.min)/(self.max-self.min)

    def inverse_transform(self, data):
        return data*(self.max-self.min)+self.min
