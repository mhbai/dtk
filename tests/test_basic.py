# -*- coding: utf-8 -*-

from .context import dispersion

import unittest
import json


class BasicTestSuite(unittest.TestCase):
	"""Basic test cases."""

	T={
	    'f1':{'b': 2, 'a': 1, 'e': 1, 'i': 1, 'k': 1, 'm': 1, 'n': 1, 'p': 1, 'u': 1}, 
		'f2':{'a': 2, 'b': 2, 'e': 1, 'n': 1, 'q': 1, 's': 1, 't': 1, 'w': 1}, 
		'f3':{'a': 3, 'b': 2, 'c': 1, 'e': 1, 'g': 1, 's': 1, 't': 1}, 
		'f4':{'a': 4, 'b': 2, 'e': 1, 'g': 1, 'h': 1, 't': 1}, 
		'f5':{'a': 5, 'b': 2, 'h': 1, 'e': 1, 'x': 1}
	}

	def test_Entropy(self):
		L=dispersion.Entropy(self.T)
		self.assertEqual("%.3f"%L["a"],"2.149")

	def test_DC(self):
		L=dispersion.DC(self.T)
		self.assertEqual("%.3f"%L["a"],"0.937")

	def test_SD(self):
		L=dispersion.SD(self.T)
		self.assertEqual("%.3f"%L["a"],"1.581")

	def test_VC(self):
		L=dispersion.VC(self.T)
		self.assertEqual("%.3f"%L["a"],"0.527")

	def test_JD(self):
		L=dispersion.JD(self.T)
		self.assertEqual("%.3f"%L["a"],"0.736")

	def test_IDF(self):
		L=dispersion.IDF(self.T)
		self.assertEqual("%.3f"%L["a"],"0.000")

	def test_CS(self):
		L=dispersion.CS(self.T)
		self.assertEqual("%.3f"%L["a"],"3.333")

	def test_LD(self):
		L=dispersion.LD(self.T)
		self.assertEqual("%.3f"%L["a"],"0.944")

	def test_JU(self):
		L=dispersion.JU(self.T)
		self.assertEqual("%.3f"%L["a"],"11.047")

	def test_RAF(self):
		L=dispersion.RAF(self.T)
		self.assertEqual("%.3f"%L["a"],"14.053")

	def test_CD(self):
		L=dispersion.CD(self.T)
		self.assertEqual("%.3f"%L["a"],"0.926")

	def test_CU(self):
		L=dispersion.CU(self.T)
		self.assertEqual("%.3f"%L["a"],"14.108")

if __name__ == '__main__':
    unittest.main()

