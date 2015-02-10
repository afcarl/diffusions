#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Test suite for diffusions package.

"""

from __future__ import print_function, division

import unittest as ut
import numpy as np

from diffusions import GBM, GBMparam
from diffusions import Vasicek, VasicekParam
from diffusions import CIR, CIRparam
from diffusions import Heston, HestonParam
from diffusions import SDE
from diffusions import nice_errors, ajd_drift, ajd_diff


class SDEParameterTestCase(ut.TestCase):
    """Test SDE, GBM classes."""

    def test_gbmparam_class(self):
        """Test parameter class."""

        mean, sigma = 1.5, .2
        param = GBMparam(mean, sigma)

        self.assertEqual(param.mean, mean)
        self.assertEqual(param.sigma, sigma)
        np.testing.assert_array_equal(param.theta, np.array([mean, sigma]))
        np.testing.assert_array_equal(param.mat_k0,
                                      np.array([mean - sigma**2/2]))
        np.testing.assert_array_equal(param.mat_k1, np.array([[0]]))
        np.testing.assert_array_equal(param.mat_h0, np.array([[sigma**2]]))
        np.testing.assert_array_equal(param.mat_h1, np.array([[[0]]]))


class HelperFunctionsTestCase(ut.TestCase):
    """Test helper functions."""

    def test_nice_errors(self):
        """Test nice errors function."""

        nvars, nobs, nsim = 2, 3, 11
        sim = 1
        size = (nobs, nsim, nvars)
        new_size = (nobs, nsim*2, nvars)
        errors = np.random.normal(size=size)
        treated_errors = nice_errors(errors, sim)

        self.assertEqual(treated_errors.shape, new_size)
        np.testing.assert_almost_equal(treated_errors.mean(sim), 0)
        np.testing.assert_almost_equal(treated_errors.std(sim),
                                       np.ones((nobs, nvars)))

    def test_ajd_drift_gbm(self):
        """Test AJD drift function for GBM model."""

        mean, sigma = 1.5, .2
        param = GBMparam(mean, sigma)
        nvars, nsim = 1, 2
        size = (nsim, nvars)
        state = np.ones(size)
        drift = state * (mean - sigma**2/2)

        self.assertEqual(ajd_drift(state, param).shape, size)
        np.testing.assert_array_equal(ajd_drift(state, param), drift)

    def test_ajd_diff_gbm(self):
        """Test AJD diffusion function for GBM model."""

        mean, sigma = 1.5, .2
        param = GBMparam(mean, sigma)
        nvars, nsim = 1, 2
        size = (nsim, nvars)
        state = np.ones(size)
        diff = np.ones((nsim, nvars, nvars)) * sigma

        self.assertEqual(ajd_diff(state, param).shape, (nsim, nvars, nvars))
        np.testing.assert_array_equal(ajd_diff(state, param), diff)

    def test_ajd_drift_vasicek(self):
        """Test AJD drift function for Vasicek model."""

        mean, kappa, sigma = 1.5, 1, .2
        param = VasicekParam(mean, kappa, sigma)
        nvars, nsim = 1, 2
        size = (nsim, nvars)
        state = np.ones(size)
        drift = kappa * (mean - state)

        self.assertEqual(ajd_drift(state, param).shape, size)
        np.testing.assert_array_equal(ajd_drift(state, param), drift)

    def test_ajd_diff_vasicek(self):
        """Test AJD diffusion function for Vasicek model."""

        mean, kappa, sigma = 1.5, 1, .2
        param = VasicekParam(mean, kappa, sigma)
        nvars, nsim = 1, 2
        size = (nsim, nvars)
        state = np.ones(size)
        diff = np.ones((nsim, nvars, nvars)) * sigma

        self.assertEqual(ajd_diff(state, param).shape, (nsim, nvars, nvars))
        np.testing.assert_array_equal(ajd_diff(state, param), diff)

    def test_ajd_drift_cir(self):
        """Test AJD drift function for CIR model."""

        mean, kappa, sigma = 1.5, 1, .2
        param = CIRparam(mean, kappa, sigma)
        nvars, nsim = 1, 2
        size = (nsim, nvars)
        state = np.ones(size)
        drift = kappa * (mean - state)

        self.assertEqual(ajd_drift(state, param).shape, size)
        np.testing.assert_array_equal(ajd_drift(state, param), drift)

    def test_ajd_diff_cir(self):
        """Test AJD diffusion function for CIR model."""

        mean, kappa, sigma = 1.5, 1, .2
        param = CIRparam(mean, kappa, sigma)
        nvars, nsim = 1, 2
        size = (nsim, nvars)
        state_val = 4
        state = np.ones(size)*state_val
        diff = sigma * state_val**.5 * np.ones((nsim, nvars, nvars))

        self.assertEqual(ajd_diff(state, param).shape, (nsim, nvars, nvars))
        np.testing.assert_array_equal(ajd_diff(state, param), diff)

    def test_ajd_drift_heston(self):
        """Test AJD drift function for Heston model."""

        mean_r, mean_v, kappa, sigma, rho = .01, .2, 1.5, .2, -.5
        param = HestonParam(mean_r=mean_r, mean_v=mean_v, kappa=kappa,
                            sigma=sigma, rho=rho)
        nvars, nsim = 2, 3
        size = (nsim, nvars)
        state = np.ones(size)
        drift = np.ones(size)
        drift_r = mean_r - state[:, 1]**2/2
        drift_v = kappa * (mean_v - state[:, 1])
        drift = np.vstack([drift_r, drift_v]).T

        self.assertEqual(ajd_drift(state, param).shape, drift.shape)
        np.testing.assert_almost_equal(ajd_drift(state, param), drift)

    def test_ajd_diff_heston(self):
        """Test AJD diffusion function for Heston model."""

        mean_r, mean_v, kappa, sigma, rho = .01, .2, 1.5, .2, -.0
        param = HestonParam(mean_r=mean_r, mean_v=mean_v, kappa=kappa,
                            sigma=sigma, rho=rho)
        nvars, nsim = 2, 3
        size = (nsim, nvars)
        state = np.ones(size)
        diff = np.ones((nsim, nvars, nvars))
        var = np.array([[1, sigma*rho], [sigma*rho, sigma**2]])
        var = ((np.ones((nsim, nvars, nvars)) * var).T * state[:, 1]).T
        diff = np.linalg.cholesky(var)

        self.assertEqual(ajd_diff(state, param).shape, diff.shape)
        np.testing.assert_array_equal(ajd_diff(state, param), diff)


class SimulationTestCase(ut.TestCase):
    """Test simulation capabilities."""

    def test_gbm_simupdate(self):
        """Test simulation update of the GBM model."""

        mean, sigma = 1.5, .2
        param = GBMparam(mean, sigma)
        gbm = GBM(param)
        gbm.ndiscr, gbm.interval = 2, .5
        nvars, nsim = 1, 2
        size = (nsim, nvars)
        state = np.ones(size)
        error = np.zeros(size)

        new_state = gbm.update(state, error)
        loc = state * (mean - sigma**2/2)
        scale = np.ones((nsim, nvars, nvars)) * sigma
        delta = gbm.interval / gbm.ndiscr
        new_state_compute = loc * delta + (scale * error).sum(1) * delta**.5

        self.assertEqual(new_state.shape, size)
        np.testing.assert_array_equal(new_state, new_state_compute)

    def test_vasicek_simupdate(self):
        """Test simulation update of the Vasicek model."""

        mean, kappa, sigma = 1.5, 1, .2
        param = VasicekParam(mean, kappa, sigma)
        vasicek = Vasicek(param)
        vasicek.ndiscr, vasicek.interval = 2, .5
        nvars, nsim = 1, 2
        size = (nsim, nvars)
        state = np.ones(size)
        error = np.zeros(size)

        new_state = vasicek.update(state, error)
        loc = kappa * (mean - state)
        scale = np.ones((nsim, nvars, nvars)) * sigma
        delta = vasicek.interval / vasicek.ndiscr
        new_state_compute = loc * delta + (scale * error).sum(1) * delta**.5

        self.assertEqual(new_state.shape, size)
        np.testing.assert_array_equal(new_state, new_state_compute)

    def test_cir_simupdate(self):
        """Test simulation update of the CIR model."""

        mean, kappa, sigma = 1.5, 1, .2
        param = CIRparam(mean, kappa, sigma)
        cir = CIR(param)
        cir.ndiscr, cir.interval = 2, .5
        nvars, nsim = 1, 2
        size = (nsim, nvars)
        state_val = 4
        state = np.ones(size) * state_val
        error = np.zeros(size)

        new_state = cir.update(state, error)
        loc = kappa * (mean - state)
        scale = np.ones((nsim, nvars, nvars)) * sigma * state**.5
        delta = cir.interval / cir.ndiscr
        new_state_compute = loc * delta + (scale * error).sum(1) * delta**.5

        self.assertEqual(new_state.shape, size)
        np.testing.assert_array_equal(new_state, new_state_compute)

    def test_heston_simupdate(self):
        """Test simulation update of the Heston model."""

        mean_r, mean_v, kappa, sigma, rho = .01, .2, 1.5, .2**.5, -.5
        param = HestonParam(mean_r=mean_r, mean_v=mean_v, kappa=kappa,
                            sigma=sigma, rho=rho)
        heston = Heston(param)
        heston.ndiscr, heston.interval = 2, .5
        nvars, nsim = 2, 3
        size = (nsim, nvars)
        state = np.ones(size)
        error = np.vstack([np.zeros(nsim), np.ones(nsim)]).T

        new_state = heston.update(state, error)
        drift_r = mean_r - state[:, 1]**2/2
        drift_v = kappa * (mean_v - state[:, 1])
        loc = np.vstack([drift_r, drift_v]).T

        var = np.array([[1, sigma*rho], [sigma*rho, sigma**2]])
        var = ((np.ones((nsim, nvars, nvars)) * var).T * state[:, 1]).T
        scale = np.linalg.cholesky(var)

        delta = heston.interval / heston.ndiscr
        new_state_compute = loc * delta
        for i in range(nsim):
            new_state_compute[i] += (scale[i] * error[i]).sum(1) * delta**.5

        self.assertEqual(new_state.shape, size)
        np.testing.assert_almost_equal(new_state, new_state_compute)

    def test_gbm_simulation(self):
        """Test simulation of the GBM model."""

        nvars = 1
        mean, sigma = 1.5, .2
        param = GBMparam(mean, sigma)
        gbm = GBM(param)
        start, nperiods, interval, ndiscr, nsim = 1, 5, .5, 3, 4
        nobs = int(nperiods / interval)
        paths = gbm.simulate(start, interval, ndiscr, nobs, nsim)

        self.assertEqual(paths.shape, (nobs+1, 2*nsim, nvars))

        nsim = 1
        paths = gbm.simulate(start, interval, ndiscr, nobs, nsim)

        self.assertEqual(paths.shape, (nobs+1, 2*nsim, nvars))

    def test_vasicek_simulation(self):
        """Test simulation of the Vasicek model."""

        nvars = 1
        mean, kappa, sigma = 1.5, .1, .2
        param = VasicekParam(mean, kappa, sigma)
        vasicek = Vasicek(param)
        start, nperiods, interval, ndiscr, nsim = 1, 5, .5, 3, 4
        nobs = int(nperiods / interval)
        paths = vasicek.simulate(start, interval, ndiscr, nobs, nsim)

        self.assertEqual(paths.shape, (nobs+1, 2*nsim, nvars))

    def test_cir_simulation(self):
        """Test simulation of the CIR model."""

        nvars = 1
        mean, kappa, sigma = 1.5, .1, .2
        param = CIRparam(mean, kappa, sigma)
        cir = CIR(param)
        start, nperiods, interval, ndiscr, nsim = 1, 5, .5, 3, 4
        nobs = int(nperiods / interval)
        paths = cir.simulate(start, interval, ndiscr, nobs, nsim)

        self.assertEqual(paths.shape, (nobs+1, 2*nsim, nvars))

    def test_heston_simulation(self):
        """Test simulation of the Heston model."""

        nvars = 2
        mean_r, mean_v, kappa, sigma, rho = .01, .2, 1.5, .2**.5, -.5
        param = HestonParam(mean_r=mean_r, mean_v=mean_v, kappa=kappa,
                            sigma=sigma, rho=rho)
        heston = Heston(param)
        start, nperiods, interval, ndiscr, nsim = [1, mean_v], 5, .5, 3, 4
        nobs = int(nperiods / interval)
        paths = heston.simulate(start, interval, ndiscr, nobs, nsim)

        self.assertEqual(paths.shape, (nobs+1, 2*nsim, nvars))


if __name__ == '__main__':
    ut.main()
