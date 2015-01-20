#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Generic Model

"""
from __future__ import print_function, division

import numpy as np
import matplotlib.pylab as plt
import seaborn as sns

__all__ = ['SDE']


class SDE(object):

    r"""Generic Model.

    Given the generic continuous-time diffusion model

    .. math::
        dY_{t}=\mu\left(Y_{t},\theta_{0}\right)dt
            +\sigma\left(Y_{t},\theta_{0}\right)dW_{t}

    we can discretize it as

    .. math::
        Y_{t}\approx Y_{t}+\mu\left(Y_{t-h},\theta_{0}\right)h
            +\sigma\left(Y_{t-h},\theta_{0}\right)\sqrt{h}\varepsilon_{t}.

    Attributes
    ----------

    Methods
    -------

    """

    def __init__(self, theta_true=None):
        self.paths = None
        self.eps = None
        self.theta_true = theta_true

    def euler_loc(self, x, theta):
        return self.drift(x, theta) * self.h

    def euler_scale(self, x, theta):
        return self.diff(x, theta) * self.h**.5

    def sim(self, z, error):
        """Euler update function for return equation.

        """
        M = error.shape[0]
        return self.euler_loc(z, self.theta_true) / M \
            + self.euler_scale(z, self.theta_true) / M**.5 * error

    def simulate(self, x0, h, M, N, S):
        """Simulate observations from the model.

        Parameters
        ----------
        x0 : array_like
            Starting value for simulation
        h : float
            Interval length
        M : int
            Number of discretization points inside unit interval
        N : int
            Number of points to simulate in one series
        S : int
            Number of time series to simulate

        """
        # Interval length
        self.h = h
        # Number of points
        self.N = N
        size = (N, M, S)
        self.eps = np.random.normal(size=size, scale=h**.5)
        x = np.ones((N, S)) * x0

        for n in range(N-1):
            x[n+1] = reduce(self.sim, self.eps[n], x[n])

        if S > 1:
            self.paths = x
        else:
            self.paths = x.flatten()

    def plot_trajectories(self, num):
        if self.paths is None:
            print('Simulate data first!')
        else:
            x = np.arange(0, self.h * self.N, self.h)
            plt.plot(x, self.paths[:, :num])
            plt.xlabel('$t$')
            plt.ylabel('$x_t$')
            plt.show()

    def plot_final_distr(self):
        if self.paths is None:
            print('Simulate data first!')
        else:
            data = self.paths[-1]
            sns.kdeplot(data)
            plt.xlabel('x')
            plt.ylabel('f')
            plt.show()


def reduce(sim, eps, x):
    for e in eps:
        x = sim(x, e)
    return x


if __name__ == '__main__':
    pass
