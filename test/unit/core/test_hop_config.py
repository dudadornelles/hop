from hop.core import HopConfig
import unittest

class TestHopConfig(unittest.TestCase):

    def test_get(self):
        config = HopConfig({
            'a': { 
                'b': 'c' 
            }
        })

        self.assertEquals(config.get('a'), { 'b': 'c' })
        self.assertEquals(config.get('1', 'default'), 'default')
        self.assertEquals(config.get('a.b'), 'c')
        self.assertEquals(config.get('d.f', 'default'), 'default')
