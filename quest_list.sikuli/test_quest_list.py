import unittest
from quest_list import QuestList

class QuestsTestCase(unittest.TestCase):
    def testQuestTypeBd(self):
        quests = QuestList("bd", [1,2])
        self.assertEqual(quests.getQuestTypeImage(), "quest_type_bd.png")
        
    def testTwoQuests(self):
        quests = QuestList("bd", [1,2])
        quest_list = quests.getAllQuestImages()
        self.assertEqual(len(quest_list), 2)
        self.assertEqual(quest_list[0], "quest_bd1.png")
        self.assertEqual(quest_list[1], "quest_bd2.png")
        
    def testEmptyQuest(self):
        quests = QuestList("bd", [])
        quest_list = quests.getAllQuestImages()
        self.assertEqual(len(quest_list), 0)
        
if __name__ == "__main__":
    unittest.main()