#!/usr/bin/python
# -*- coding: utf-8  -*-
"""
=========================================================================
        msproteomicstools -- Mass Spectrometry Proteomics Tools
=========================================================================

Copyright (c) 2013, ETH Zurich
For a full list of authors, refer to the file AUTHORS.

This software is released under a three-clause BSD license:
 * Redistributions of source code must retain the above copyright
   notice, this list of conditions and the following disclaimer.
 * Redistributions in binary form must reproduce the above copyright
   notice, this list of conditions and the following disclaimer in the
   documentation and/or other materials provided with the distribution.
 * Neither the name of any author or any participating institution
   may be used to endorse or promote products derived from this software
   without specific prior written permission.
--------------------------------------------------------------------------
THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS "AS IS"
AND ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE
IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE
ARE DISCLAIMED. IN NO EVENT SHALL ANY OF THE AUTHORS OR THE CONTRIBUTING
INSTITUTIONS BE LIABLE FOR ANY DIRECT, INDIRECT, INCIDENTAL, SPECIAL,
EXEMPLARY, OR CONSEQUENTIAL DAMAGES (INCLUDING, BUT NOT LIMITED TO,
PROCUREMENT OF SUBSTITUTE GOODS OR SERVICES; LOSS OF USE, DATA, OR PROFITS;
OR BUSINESS INTERRUPTION) HOWEVER CAUSED AND ON ANY THEORY OF LIABILITY,
WHETHER IN CONTRACT, STRICT LIABILITY, OR TORT (INCLUDING NEGLIGENCE OR
OTHERWISE) ARISING IN ANY WAY OUT OF THE USE OF THIS SOFTWARE, EVEN IF
ADVISED OF THE POSSIBILITY OF SUCH DAMAGE.
--------------------------------------------------------------------------
$Maintainer: Pedro Navarro$
$Authors: Pedro Navarro$
--------------------------------------------------------------------------
"""

import unittest
import os

import msproteomicstoolslib.format.SWATHScoringMapper as mapper
import msproteomicstoolslib.format.SWATHScoringReader as reader
from msproteomicstoolslib.algorithms.alignment.MRExperiment import MRExperiment as Experiment

def doTest(self, runs):
    self.assertEqual(len(runs), 4)
    self.assertEqual(runs[0].get_id(), "0_0")
    self.assertEqual(runs[1].get_id(), "1_0")
    self.assertEqual(runs[2].get_id(), "2_0")
    self.assertEqual(runs[3].get_id(), "3_0")

    self.assertEqual(runs[0].get_openswath_filename(), "split_hroest_K120808_combined.featureXML")
    self.assertIsNone(runs[0].get_aligned_filename())

    self.assertEqual(len(list(runs[0])), 1)
    self.assertEqual(len(list(runs[1])), 1)
    self.assertEqual(len(list(runs[2])), 1)
    self.assertEqual(len(list(runs[3])), 1)

    self.assertIsNotNone(runs[0].getPrecursorGroup("17365_TLDTAAEKIVETATR/3_run0"))
    self.assertIsNone(runs[0].getPrecursorGroup("19365_TLDTAAEKIVETATR/3_run0"))

class TestUnitScoringMapperOpenSWATH(unittest.TestCase):

    def setUp(self):
        self.dirname = os.path.dirname(os.path.abspath(__file__))
        self.topdir = os.path.join(os.path.join(self.dirname, ".."), "..")
        self.datadir = os.path.join(os.path.join(self.topdir, "test"), "data")
        self.datadir_gui = os.path.join(self.datadir, "gui")

    def test_newReader(self):
        filename = os.path.join(self.datadir, "dataset3.csv")
        filename_mzml = os.path.join(self.datadir, "dataset3.mzML")
        r = reader.SWATHScoringReader.newReader([filename], "openswath", "complete")
        self.assertTrue(True)

    def test_parse_files(self):

        filename = os.path.join(self.datadir_gui, "dataset3.csv")
        filename_mzml = os.path.join(self.datadir_gui, "dataset3.mzML")
        r = reader.SWATHScoringReader.newReader([filename], "openswath", readmethod="gui", errorHandling="loose")

        new_exp = Experiment()
        new_exp.runs = r.parse_files(True)
        multipeptides = new_exp.get_all_multipeptides(1.0, verbose=False)

        # Build map of the PeptideName/Charge to the individual multipeptide
        peakgroup_map = {}
        mapper.buildPeakgroupMap(multipeptides, peakgroup_map)

        self.assertEqual(len(peakgroup_map.keys()), 2)
        self.assertEqual(sorted(list(peakgroup_map.keys())), ['testpeptide/0', 'testpeptide/0_pr'])

if __name__ == '__main__':
    unittest.main()


