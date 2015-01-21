#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Geometric Brownian Motion

"""
from __future__ import print_function, division

import numpy as np
import numdifftools as nd

from statsmodels.tsa.tsatools import lagmat

from .generic_model import SDE

__all__ = ['GBM']


class GBMparam(object):

    """Parameter storage for GBM model.

    """

    def __init__(self, mean=0, sigma=.2):
        """Initialize class.

        Parameters
        ----------
        sigma : float

        """
        self.mean = mean
        self.sigma = sigma
        self.theta = [mean, sigma]


class GBM(SDE):

    r"""Geometric Brownian Motion.

    Suppose that :math:`S_{t}` evolves according to

    .. math::
        \frac{dS_{t}}{S_{t}}=\mu dt+\sigma dW_{t}.

    In logs:

    .. math::
        d\log S_{t}=\left(\mu-\frac{1}{2}\sigma^{2}\right)dt+\sigma dW_{t}.

    After integration on the interval :math:`\left[t,t+h\right]`:

    .. math::
        r_{t,h}=\log\frac{S_{t+h}}{S_{t}}
            =\left(\mu-\frac{1}{2}\sigma^{2}\right)h
            +\sigma\sqrt{h}\varepsilon_{t+h},

    where :math:`\varepsilon_{t}\sim N\left(0,1\right)`.

    Attributes
    ----------

    Methods
    -------

    """

    def __init__(self, theta_true=None):
        """Initialize the class.

        """
        super().__init__(theta_true)

    def drift(self, x, theta):
        """Drift function.

        Parameters
        ----------
        state : array
            Current state of the process
        theta : GBMparam instance
            Parameter object

        Returns
        -------
        scalar
            Drift value

        """
        return theta.mean - theta.sigma**2/2

    def diff(self, x, theta):
        """Diffusion (instantaneous volatility) function.

        Parameters
        ----------
        state : array
            Current state of the process
        theta : GBMparam instance
            Parameter object

        Returns
        -------
        scalar
            Diffusion value

        """
        return theta.sigma

    def betamat(self, theta):
        """Coefficients in linear representation of the first moment.

        Parameters
        ----------
        theta : array
            Parameters

        Returns
        -------
        float
            Constant coefficient

        """
        theta = GBMparam(mean=theta[0], sigma=theta[1])
        loc = self.exact_loc(0, theta)
        if not isinstance(loc, float):
            raise ValueError('Location and scale should be scalars!')
        return np.array([loc, 0], dtype=float)

    def gammamat(self, theta):
        """Coefficients in linear representation of the second moment.

        Parameters
        ----------
        theta : array
            Parameters

        Returns
        -------
        float
            Constant coefficient

        """
        theta = GBMparam(mean=theta[0], sigma=theta[1])
        loc = self.exact_loc(0, theta)
        scale = self.exact_scale(0, theta)
        if not isinstance(scale, float):
            raise ValueError('Location and scale should be scalars!')
        return np.array([loc**2 + scale**2, 0], dtype=float)

    def dbetamat(self, theta):
        """Derivative of the first moment coefficients (numerical).

        Parameters
        ----------
        theta : array
            Parameters

        Returns
        -------
        array
            Derivatives of the coefficient

        """
        return nd.Jacobian(self.betamat)(theta)

    def dgammamat(self, theta):
        """Derivative of the second moment coefficients (numerical).

        Parameters
        ----------
        theta : array
            Parameters

        Returns
        -------
        array
            Derivatives of the coefficient

        """
        return nd.Jacobian(self.gammamat)(theta)

    def dbetamat_exact(self, theta):
        """Derivative of the first moment coefficients (exact).

        Parameters
        ----------
        theta : array
            Parameters

        Returns
        -------
        array
            Derivatives of the coefficient

        """
        mean, sigma = theta
        return np.array([[self.interval, - sigma * self.interval], [0, 0]])

    def dgammamat_exact(self, theta):
        """Derivative of the second moment coefficients (exact).

        Parameters
        ----------
        theta : array
            Parameters

        Returns
        -------
        array
            Derivatives of the coefficient

        """
        mean, sigma = theta
        return np.array([[2 * self.interval**2 * (mean - sigma**2/2),
                         2 * sigma * self.interval
                         - 2 * sigma * self.interval**2
                         * (mean - sigma**2/2)], [0, 0]])

    def momcond(self, theta, data=None):
        """Moment function.

        Parameters
        ----------
        theta : array
            Model parameters
        data : array
            Whatever data is necessary to compute moment function

        Returns
        -------
        moments : array, nobs x nmoms
            Moment restrictions
        dmoments : array, nmoms x nparams
            Average derivative of the moment restrictions

        """
        datalag = 1
        instrlag = 2
        lagdata = lagmat(data, maxlag=datalag)[datalag:]
        nobs = lagdata.shape[0]
        datamat = np.hstack([np.ones((nobs, 1)), lagdata])

        errors = np.vstack([data[datalag:] - datamat.dot(self.betamat(theta)),
                            data[datalag:]**2
                            - datamat.dot(self.gammamat(theta))])

        instruments = np.hstack([np.ones((nobs, 1)),
                                 lagmat(data[:-datalag], maxlag=instrlag)]).T

        mom, dmom = [], []
        for instr in instruments:
            mom.append(errors * instr)
            meandata = (datamat.T * instr).mean(1)
            dtheta = -np.vstack([meandata.dot(self.dbetamat(theta)),
                                 meandata.dot(self.dgammamat(theta))])
            dmom.append(dtheta)

        mom = np.vstack(mom)
        dmom = np.vstack(dmom)

        return mom.T, dmom


if __name__ == '__main__':
    pass
