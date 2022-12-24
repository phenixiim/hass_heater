# this test can be launched after commenting out `runDecisionEngine()` AND/OR `runDecisionEngineWithHysteresis()` and via those commands:
# cd tests
# python3 -m unittest *


import unittest
import sys
import os
from unittest.mock import MagicMock

relativePath = "../"
absolute_path = os.path.dirname(__file__)
sys.path.append(os.path.join(absolute_path,relativePath))

import engine
thing = engine

ENGINE_ON = 'engine_on'
ENGINE_OFF = 'engine_off'

thing.engineOn = MagicMock(return_value=ENGINE_ON)
thing.engineOff = MagicMock(return_value=ENGINE_OFF)
thing.isDecisionEngineBlocked = MagicMock(return_value=False)
thing.logger = MagicMock(return_value=None)
thing.testsDontRun = MagicMock(return_value=True)

def returnMockWithValue(value):
    return MagicMock(return_value=value)

class test_engine(unittest.TestCase):

    def test_runDecisionEngine(self):
        thing.getDesiredTemperature = returnMockWithValue(16)
        thing.getCurrentTemperature = returnMockWithValue(19)
        self.assertEqual(engine.runDecisionEngine(), ENGINE_OFF)

        thing.getDesiredTemperature = returnMockWithValue(16)
        thing.getCurrentTemperature = returnMockWithValue(15)
        self.assertEqual(engine.runDecisionEngine(), ENGINE_ON)

        thing.getDesiredTemperature = returnMockWithValue(16)
        thing.getCurrentTemperature = returnMockWithValue(15.5)
        self.assertEqual(engine.runDecisionEngine(), ENGINE_OFF)

if __name__ == '__main__':
    unittest.main()