#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Generic parameter class
~~~~~~~~~~~~~~~~~~~~~~~

"""
from __future__ import print_function, division

__all__ = ['GenericParam']


class GenericParam(object):

    """Parameter storage for GBM model.

    Attributes
    ----------
    mean : float
        Mean of the process
    sigma : float
        Instantaneous standard deviation

    """

    def __init__(self):
        """Initialize class.

        """
        pass

    def update_ajd(self):
        """Update AJD representation.

        """
        raise NotImplementedError('Must be overridden')

    @classmethod
    def from_theta(cls, theta):
        """Update attributes from parameter vector.

        Parameters
        ----------
        theta : (nparams, ) array
            Parameter vector

        """
        raise NotImplementedError('Must be overridden')

    def get_model_name(self):
        """Return model name.

        Returns
        -------
        str
            Parameter vector

        """
        raise NotImplementedError('Must be overridden')

    def get_names(self):
        """Return parameter names.

        Returns
        -------
        list of str
            Parameter names

        """
        raise NotImplementedError('Must be overridden')

    def get_theta(self):
        """Return vector of parameters.

        Returns
        -------
        array
            Parameter vector

        """
        raise NotImplementedError('Must be overridden')

    def __str__(self):
        """String representation.

        """
        show = self.get_model_name() + ' parameters:\n'
        for name, param in zip(self.get_names(), self.get_theta()):
            show += name + ' = ' + str(param) + ', '
        return show[:-2]

    def __repr__(self):
        """String representation.

        """
        return self.__str__()