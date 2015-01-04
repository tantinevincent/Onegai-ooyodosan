import unittest
from fleet import Fleet

class ExpeditionTestCase(unittest.TestCase):
    def testFleetZero(self):
        self.assertRaises(ValueError, Fleet, 0)
    def testFleetOneMarks(self):
        fleet = Fleet(1)
        self.assertEqual(fleet.getImage(), "fleet_1_mark.png")
    def testFleetOneNotSelectedMark(self):
        fleet = Fleet(1)
        self.assertEqual(fleet.getNotSelectedImage(), "fleet_1_mark_not_selected.png")
    def testFleetOneAllMarks(self):
        fleet = Fleet(1)
        marks = fleet.getAllImages()
        self.assertEqual(len(marks), 2)
        self.assertEqual(marks[0], "fleet_1_flagship_mark.png")
        self.assertEqual(marks[1], "fleet_1_mark.png")
    def testFleetTwoAllMarks(self):
        fleet = Fleet(2)
        marks = fleet.getAllImages()
        self.assertEqual(len(marks), 1)
        self.assertEqual(marks[0], "fleet_2_mark.png")
        
if __name__ == "__main__":
    unittest.main()