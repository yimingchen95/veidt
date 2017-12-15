# coding: utf-8
# Copyright (c) Materials Virtual Lab
# Distributed under the terms of the BSD License.

"""
Define abstract base classes.
"""

import abc
import six
from monty.json import MSONable
from sklearn.base import TransformerMixin, BaseEstimator

import pandas as pd


class Describer(six.with_metaclass(abc.ABCMeta, BaseEstimator, MSONable, TransformerMixin)):
    """
    Base class for a Describer, i.e., something that converts an object to a
    describer, typically a numerical representation useful for machine
    learning.
    """

    def fit(self, objs, targets=None):
        """Fit the describer.
        In the case that the describer relies on parameters calculated from training data, this method should be rewritten to store the fitted parameters
        """
        return self

    def transform(self, objs):
        """Transform the input objects"""
        return self.describe_all(objs).values

    @abc.abstractmethod
    def describe(self, obj):
        """
        Converts an obj to a descriptor vector.

        :param obj: Object
        :return: Descriptor for a structure. Recommended format is a pandas
            Dataframe object with the column names as intuitive names.
            For example, a simple site describer of the fractional coordinates
            (this is usually a bad describer, so it is just for illustration
            purposes) can be generated as::

                print(pd.DataFrame(s.frac_coords, columns=["a", "b", "c"]))
                          a         b         c
                0  0.000000  0.000000  0.000000
                1  0.750178  0.750178  0.750178
                2  0.249822  0.249822  0.249822

            Pandas dataframes can be dumped to a variety of formats (json, csv,
            etc.) easily. Note that a dataframe should be used even if you have
            only one line, i.e., do not use Series objects unless you know
            what you are doing.
        """
        pass

    def describe_all(self, objs):
        """
        Convenience method to convert a list of objects to a list of
        descriptors. Default implementation simply loops a call to describe, but
        in some instances, a batch implementation may be more efficient.

        :param objs: List of objects

        :return: Concatenated descriptors for all objects. Recommended format
            is a pandas DataFrame. Default implement returns a list of
            descriptors generated by a loop call to describe for each obj.
        """
        return pd.concat([self.describe(o) for o in objs])


class Model(six.with_metaclass(abc.ABCMeta, BaseEstimator, MSONable)):
    """
    Abstract Base class for a Model. Basically, it usually wraps around a deep
    learning package, e.g., the Sequential Model in Keras, but provides for
    transparent conversion of arbitrary input and outputs.
    """

    @abc.abstractmethod
    def fit(self, features, targets, **kwargs):
        """

        :param features: Numerical input feature list or numpy array with dim (m, n)
            where m is the number of data and n is the feature dimension
        :param targets: Numerical output target list, or numpy array with dim (m, )
        """
        pass

    @abc.abstractmethod
    def predict(self, inputs):
        """
        Predict the values given a set of inputs based on fitted model.

        :param inputs: List of inputs

        :return: List of output objects
        """
        pass


