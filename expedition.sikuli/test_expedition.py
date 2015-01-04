import unittest
from expedition import Expedition

class ExpeditionTestCase(unittest.TestCase):
    def testExpeditionNumEqualsZero(self):
        self.assertRaises(ValueError, Expedition, 0)
    def testExpeditionNumLessThanTen(self):
        exp = Expedition(2)
        self.assertEqual(exp.getImage(), "expedition_02.png")
    def testExpeditionNumEqualsTen(self):
        exp = Expedition(10)
        self.assertEqual(exp.getImage(), "expedition_10.png")
    def testExpeditionNumGreaterThanTen(self):
        exp = Expedition(11)
        self.assertEqual(exp.getImage(), "expedition_11.png")
    def testWorldWithExpeditionOne(self):
        exp = Expedition(1)
        self.assertEqual(exp.getWorldImage(), "world_1.png")
    def testWorldWithExpeditionEight(self):
        exp = Expedition(8)
        self.assertEqual(exp.getWorldImage(), "world_1.png")
    def testWorldWithExpeditionNine(self):
        exp = Expedition(9)
        self.assertEqual(exp.getWorldImage(), "world_2.png")
        
if __name__ == "__main__":
    unittest.main()