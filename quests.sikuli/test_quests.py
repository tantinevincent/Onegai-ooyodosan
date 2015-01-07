import unittest
from quests import Quests

class QuestsTestCase(unittest.TestCase):
    def testQuestTypeBd(self):
        quests = Quests("fight", [1,2])
        self.assertEqual(quests.getTypeImage(), "quest_type_fight.png")
        
    def testTwoQuests(self):
        quests = Quests("fight", ["bd1","bd2"])
        quest_list = quests.getAllImages()
        self.assertEqual(len(quest_list), 2)
        self.assertEqual(quest_list[0], "quest_bd1.png")
        self.assertEqual(quest_list[1], "quest_bd2.png")
        
    def testEmptyQuest(self):
        quests = Quests("fight", [])
        quest_list = quests.getAllImages()
        self.assertEqual(len(quest_list), 0)
        
if __name__ == "__main__":
    unittest.main()