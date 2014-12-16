#!/usr/env/ python
#-*- coding: utf-8 -*-
from __future__ import print_function

import unittest
import operator
from pythonia.pythonia import dungeon

class TestDungeon(unittest.TestCase):
    
    def setUp(self):
        self.test_map = dungeon.Dungeon.load_from_file('map.txt')
    
    def test_load_from_file(self):
        self.assertEqual(self.test_map.width, 10)
        self.assertEqual(self.test_map.height, 6)
    
    def test_failed_loading(self):
        self.assertRaises(IOError, dungeon.Dungeon.load_from_file, 'inexistentmap.txt')
    
    def test_getitem(self):
        self.assertEqual(self.test_map[0, 0], '#')
        self.assertEqual(self.test_map[1, 1], ' ')
        self.assertEqual(self.test_map[6, 0], '#')
        self.assertRaises(IndexError, operator.getitem, self.test_map, (10, 0))
    
    def test_collide(self):
        self.assertTrue(self.test_map.collide(0, 0))
        self.assertFalse(self.test_map.collide(3, 3))
    
    def test_get_bounding_box(self):
        self.assertSetEqual(set(self.test_map._get_bounding_box(2, 2, 1)),
                                {(1,1), (2,1), (3,1),
                                 (1,2),        (3,2),
                                 (1,3), (2,3), (3,3)})
    
    def test_get_bounding_circle(self):
        self.assertSetEqual(set(self.test_map._get_bounding_circle(2, 2, 2)),
                                {(1,0), (2,0), (3,0),
                          (0,1),                      (4,1),
                          (0,2),                      (4,2),
                          (0,3),                      (4,3),
                                 (1,4), (2,4), (3,4)})
    
    def test_reveal(self):
        self.test_map.reveal(1, 1, 4)
        #    #######
        #    #P....
        self.assertEqual(self.test_map.show_at(6, 0), '#')
        self.assertEqual(self.test_map.show_at(7, 0), ' ')
    
    def test_reveal_adjacent_walls(self):
        x, y = 1, 1
        self.test_map._reveal_adjacent_walls(3, 1, x, y)
        self.assertEqual(self.test_map.show_at(3, 0), '#')
        self.assertEqual(self.test_map.show_at(4, 0), '#')
        self.assertEqual(self.test_map.show_at(2, 0), ' ')

    def test_clamp_in_map(self):
        x, y = -1, -1
        self.assertEqual(self.test_map._clamp_in_map(x, y), (0, 0))
        width = self.test_map.width
        height = self.test_map.height
        x = width
        y = height
        self.assertEqual(self.test_map._clamp_in_map(x, y), (width - 1, height - 1))
        
        
if __name__ == '__main__':
    unittest.main()
