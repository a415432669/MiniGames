#! /usr/bin/python
# -*- coding: utf-8 -*-

"""Classic package."""

from MyHearthStone.ext import Minion, Spell, Weapon
from MyHearthStone.ext import std_events

__author__ = 'fyabc'

PackageID = 1


###############
# Neutral (0) #
###############


############
# Mage (3) #
############

# 冰枪术(1030002) -> 荣誉室

class 炎爆术(Spell):
    _data = {
        'id': 1030013, 'package': PackageID,
        'type': 1, 'rarity': 3, 'klass': 3, 'cost': 10,
        'have_target': True,
    }

    def run(self, target):
        return [std_events.damage_events(self.game, self, target, 10)]


class 大法师安东尼达斯(Minion):
    _data = {
        'id': 1030014, 'package': PackageID,
        'rarity': 4, 'klass': 3, 'cost': 7, 'attack': 5, 'health': 7,
    }


###############
# Warrior (8) #
###############


class 血吼(Weapon):
    _data = {
        'id': 1080013, 'package': PackageID,
        'type': 2, 'rarity': 3, 'klass': 8, 'cost': 7, 'attack': 7, 'health': 1,
    }
