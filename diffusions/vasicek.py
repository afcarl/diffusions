#!/usr/bin/env python
# -*- coding: utf-8 -*-
r"""
Vasicek model for interest rates
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Suppose that :math:`r_{t}` evolves according to

.. math::
    dr_{t}=\kappa\left(\mu-r_{t}\right)dt+\eta dW_{t}.

"""
from __future__ import print_function, division

import numpy as np

from .generic_model import SDE

__all__ = ['Vasicek', 'VasicekParam']


class VasicekParam(object):

    """Parameter storage for Vasicek model.

    Attributes
    ----------
    mean : float
        Mean of the process
    kappa : float
        Mean reversion speed
    eta : float
        Instantaneous standard deviation

    """

    def __init__(self, mean=.5, kappa=1.5, eta=.1):
        """Initialize class.

        Parameters
        ----------
        mean : float
            Mean of the process
        kappa : float
            Mean reversion speed
        eta : float
            Instantaneous standard deviation

        """
        self.mean = mean
        self.kappa = kappa
        self.eta = eta
        self.update_ajd()

    def update_ajd(self):
        """Update AJD representation.

        """
        # AJD parameters
        self.mat_k0 = self.kappa * self.mean
        self.mat_k1 = -self.kappa
        self.mat_h0 = self.eta**2
        self.mat_h1 = 0

    def get_theta(self):
        """Return vector of parameters.

        Returns
        -------
        (3, ) array
            Parameter vector

        """
        return np.array([self.mean, self.kappa, self.eta])

    def update(self, theta):
        """Update attributes from parameter vector.

        Parameters
        ----------
        theta : (nparams, ) array
            Parameter vector

        """
        [self.mean, self.kappa, self.eta] = theta
        self.update_ajd()


class Vasicek(SDE):

    """Vasicek model.

    Attributes
    ----------

    Methods
    -------

    """

    def __init__(self, theta_true=None):
        """Initialize the class.

        """
        super(Vasicek, self).__init__(theta_true)

    def drift(self, state, theta):
        """Drift function.

        Parameters
        ----------
        state : (nvars, nsim) array_like
            Current value of the process
        theta : parameter instance
            Model parameter

        Returns
        -------
        scalar
            Drift value

        """
        return theta.kappa * (theta.mean - state)

    def diff(self, state, theta):
        """Diffusion (instantaneous volatility) function.

        Parameters
        ----------
        state : (nvars, nsim) array_like
            Current value of the process
        theta : parameter instance
            Model parameter

        Returns
        -------
        scalar
            Diffusion value

        """
        return theta.eta


if __name__ == '__main__':
    pass
