#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Generic Model

"""
from __future__ import print_function, division

#import numpy as np

from diffusions import GBM, GBMparam
from diffusions import plot_trajectories, plot_final_distr


def try_gmm():
    mean, sigma = 1.5, .2
    theta_true = GBMparam(mean, sigma)
    gbm = GBM(theta_true)

    x0, nperiods, interval, ndiscr, nsim = 1, 500, .5, 10, 30
    nobs = int(nperiods / interval)
    paths = gbm.simulate(x0, interval, ndiscr, nobs, nsim)
    data = paths[:, 0, 0]
    data = data[1:] - data[:-1]

    #plot_final_distr(data/interval)

    mean, sigma = 2.5, .4
    theta_start = GBMparam(mean, sigma)
    res = gbm.gmmest(theta_start, data=data, instrlag=2)
    res.print_results()


def try_simulation():
    mean, sigma = .05, .2
    theta_true = GBMparam(mean, sigma)
    gbm = GBM(theta_true)

    x0, nperiods, interval, ndiscr, nsim = 1, 500, .5, 10, 2
    nobs = int(nperiods / interval)
    paths = gbm.simulate(x0, interval, ndiscr, nobs, nsim)
    data = paths[:, 0, 0]
    data = data[1:] - data[:-1]

    plot_trajectories(data, interval)


def try_marginal():
    mean, sigma = .05, .2
    theta_true = GBMparam(mean, sigma)
    gbm = GBM(theta_true)

    x0, nperiods, interval, ndiscr, nsim = 1, 500, .5, 10, 20
    nobs = int(nperiods / interval)
    paths = gbm.simulate(x0, interval, ndiscr, nobs, nsim)
    data = paths[:, :, 0]
    data = data[1:] - data[:-1]

    plot_final_distr(data/interval)


if __name__ == '__main__':

    try_marginal()
#    try_simulation()
#    try_gmm()
