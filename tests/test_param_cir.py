#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Test suite for CIR parameter class.

"""
from __future__ import print_function, division

import unittest as ut
import numpy as np
import numpy.testing as npt

from diffusions import CIRparam


class SDEParameterTestCase(ut.TestCase):
    """Test parameter classes."""

    def test_cirparam_class(self):
        """Test CIR parameter class."""

        mean, kappa, eta = 1.5, 1., .1
        param = CIRparam(mean, kappa, eta)

        self.assertEqual(param.get_model_name(), 'CIR')
        self.assertEqual(param.get_names(), ['mean', 'kappa', 'eta'])

        self.assertEqual(param.mean, mean)
        self.assertEqual(param.kappa, kappa)
        self.assertEqual(param.eta, eta)

        npt.assert_array_equal(param.get_theta(),
                               np.array([mean, kappa, eta]))

        theta = np.ones(3)
        param = CIRparam.from_theta(theta)
        npt.assert_array_equal(param.get_theta(), theta)

        mat_k0 = param.kappa * param.mean
        mat_k1 = -param.kappa
        mat_h0 = 0.
        mat_h1 = param.eta**2

        npt.assert_array_equal(param.mat_k0, mat_k0)
        npt.assert_array_equal(param.mat_k1, mat_k1)
        npt.assert_array_equal(param.mat_h0, mat_h0)
        npt.assert_array_equal(param.mat_h1, mat_h1)

        theta *= 2
        param.update(theta)
        npt.assert_array_equal(param.get_theta(), theta)

        mat_k0 = param.kappa * param.mean
        mat_k1 = -param.kappa
        mat_h0 = 0.
        mat_h1 = param.eta**2

        npt.assert_array_equal(param.mat_k0, mat_k0)
        npt.assert_array_equal(param.mat_k1, mat_k1)
        npt.assert_array_equal(param.mat_h0, mat_h0)
        npt.assert_array_equal(param.mat_h1, mat_h1)

        self.assertTrue(param.is_valid())
        param = CIRparam(mean, -kappa, eta)
        self.assertFalse(param.is_valid())
        param = CIRparam(mean, kappa, -eta)
        self.assertFalse(param.is_valid())


if __name__ == '__main__':
    ut.main()
