#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Test suite for realized moments.

"""
from __future__ import print_function, division

import unittest as ut
import numpy as np

from diffusions import GBM, GBMparam
from diffusions import Heston, HestonParam
from diffusions import CentTend, CentTendParam


class RealizedMomentsTestCase(ut.TestCase):
    """Test realized moments."""

    def test_gbm_relized_mom(self):
        """Test realized moments of GBM model."""
        mean, sigma = 1.5, .2
        param = GBMparam(mean, sigma)
        gbm = GBM(param)
        gbm.interval = .5

        nperiods = 10
        data = np.ones((2, nperiods))
        instrlag = 2

        depvar = gbm.realized_depvar(data)
        # Test shape of dependent variables
        self.assertEqual(depvar.shape, (3, nperiods))

        const = gbm.realized_const(param.get_theta())
        # Test shape of the intercept
        self.assertEqual(const.shape, (3, ))

        instr = gbm.instruments(data, instrlag=instrlag)
        ninstr = 1 + data.shape[0] * instrlag
        # Test shape of instrument matrix
        self.assertEqual(instr.shape, (ninstr, nperiods - instrlag))

        rmom, drmom = gbm.integrated_mom(param.get_theta(), data=data,
                                         instrlag=instrlag)
        nmoms = 3 * ninstr
        # Test shape of moments and gradients
        self.assertEqual(rmom.shape, (nperiods - instrlag, nmoms))
        self.assertEqual(drmom.shape, (nmoms, np.size(param.get_theta())))

    def test_heston_instruments(self):
        """Test realized moments of Heston model."""
        riskfree, lmbd, mean_v, kappa, eta, rho = 0., .01, .2, 1.5, .2**.5, -.5
        param = HestonParam(riskfree=riskfree, lmbd=lmbd,
                            mean_v=mean_v, kappa=kappa,
                            eta=eta, rho=rho)
        heston = Heston(param)
        heston.interval = .5

        nperiods = 10
        data = np.ones((2, nperiods))
        instrlag = 2

        instruments = heston.instruments(data[0], instrlag=instrlag)
        ninstr = 1
        shape = (nperiods, ninstr*instrlag + 1)

        # Test the shape of instruments
        self.assertEqual(instruments.shape, shape)

        instruments = heston.instruments(nobs=nperiods)
        ninstr = 0
        shape = (nperiods, ninstr*instrlag + 1)

        # Test the shape of instruments
        self.assertEqual(instruments.shape, shape)

    def test_heston_relized_mom(self):
        """Test realized moments of Heston model."""
        riskfree, lmbd, mean_v, kappa, eta, rho = 0., .01, .2, 1.5, .2**.5, -.5
        param = HestonParam(riskfree=riskfree, lmbd=lmbd,
                            mean_v=mean_v, kappa=kappa,
                            eta=eta, rho=rho)
        heston = Heston(param)
        heston.interval = .5
        nparams = param.get_theta().size
        nmoms = 4

        nperiods = 5
        ret = np.arange(nperiods)
        rvar = ret ** 2
        data = np.vstack([ret, rvar])
        instrlag = 2

        depvar = heston.realized_depvar(data)
        instr_data = np.vstack([rvar, rvar**2])
        ninstr = instr_data.shape[0]

        # Test shape of dependent variables
        self.assertEqual(depvar.shape, (nperiods, 3 * 4))

        mom, dmom = heston.integrated_mom(param.get_theta(),
                                          instr_data=instr_data,
                                          instr_choice='var', exact_jacob=True,
                                          data=data, instrlag=instrlag)
        nmoms_all = nmoms * (ninstr*instrlag + 1)
        mom_shape = (nperiods - instrlag, nmoms_all)

        # Test the shape of moment functions
        self.assertEqual(mom.shape, mom_shape)

        dmom_shape = (nmoms_all, nparams)

        # Test the shape of the Jacobian
        self.assertEqual(dmom.shape, dmom_shape)

        mom, dmom = heston.integrated_mom(param.get_theta(),
                                          instr_choice='const',
                                          data=data, instrlag=instrlag)
        nmoms_all = nmoms
        mom_shape = (nperiods - instrlag, nmoms_all)

        # Test the shape of moment functions
        self.assertEqual(mom.shape, mom_shape)

    def test_heston_coefs(self):
        """Test coefficients in descretization of Heston model.

        """
        riskfree, lmbd, mean_v, kappa, eta, rho = 0., .01, .2, 1.5, .2**.5, -.5
        param = HestonParam(riskfree=riskfree, lmbd=lmbd,
                            mean_v=mean_v, kappa=kappa,
                            eta=eta, rho=rho)
        heston = Heston(param)
        heston.interval = .1
        theta = param.get_theta()
        nparams = theta.size
        nmoms = 4
        aggh = 2

        self.assertIsInstance(heston.coef_big_a(theta, aggh), float)
        self.assertIsInstance(heston.coef_small_a(theta, aggh), float)
        self.assertIsInstance(heston.coef_big_c(theta, aggh), float)
        self.assertIsInstance(heston.coef_small_c(theta, aggh), float)

        self.assertEqual(heston.mat_a0(theta, aggh).shape, (4, 4))
        self.assertEqual(heston.mat_a1(theta, aggh).shape, (4, 4))
        self.assertEqual(heston.mat_a2(theta, aggh).shape, (4, 4))

        self.assertEqual(heston.mat_a(theta, aggh).shape, (4, 3*4))

        self.assertEqual(heston.realized_const(theta, aggh).shape, (4, ))
        self.assertEqual(heston.realized_const(theta, aggh)[0], 0)

        res = heston.depvar_unc_mean(theta, aggh)[1] \
            * (1 - heston.coef_big_a(theta, 1))

        self.assertEqual(heston.realized_const(theta, aggh)[1], res)

        res = heston.depvar_unc_mean(theta, aggh)[2] \
            * (1 - heston.coef_big_a(theta, 1)) \
            * (1 - heston.coef_big_a(theta, 1)**2)

        self.assertEqual(heston.realized_const(theta, aggh)[2], res)

        res = (heston.depvar_unc_mean(theta, aggh)[2] * (.5 - param.lmbd) \
            + heston.depvar_unc_mean(theta, aggh)[3]) \
            * (1 - heston.coef_big_a(theta, 1))

        self.assertAlmostEqual(heston.realized_const(theta, aggh)[3], res)

        dconst = heston.drealized_const(param.get_theta(), aggh)

        # Test derivative of intercept
        self.assertEqual(dconst.shape, (nmoms, nparams))

        dmat_a = heston.diff_mat_a(param.get_theta(), aggh)

        # Test derivative of matrix A
        self.assertEqual(len(dmat_a), nmoms)
        for mat in dmat_a:
            self.assertEqual(mat.shape, (3*nmoms, nparams))


if __name__ == '__main__':
    ut.main()