#! /usr/bin/python
# -*- coding: utf-8 -*-

import random

from MyHearthStone import ext
from MyHearthStone.ext import Minion, Spell, Hero, HeroPower
from MyHearthStone.ext import std_events
from MyHearthStone.utils.game import Zone, order_of_play

__author__ = 'fyabc'


###############
# Warrior (9) #
###############


# Warrior (8)
class Warrior(Hero):
    data = {
        'id': 8,
        'klass': 9, 'hero_power': 8,
    }


class 全副武装(HeroPower):
    data = {
        'id': 8,
        'klass': 9, 'is_basic': True, 'cost': 2,
    }

    def run(self, target, **kwargs):
        return [std_events.GainArmor(self.game, self, self.game.get_hero(self.player_id), 2)]


# 战歌指挥官 (90000)
class 战歌指挥官(Minion):
    data = {
        'id': 90000,
        'klass': 9, 'cost': 3, 'attack': 2, 'health': 3,
    }

    # TODO


# 库卡隆精英卫士 (90001)
ext.blank_minion({
    'id': 90001,
    'klass': 9, 'cost': 4, 'attack': 4, 'health': 3,
    'charge': True,
})


# 旋风斩 (90002)
class 旋风斩(Spell):
    data = {
        'id': 90002,
        'type': 1, 'klass': 9, 'cost': 1,
    }
    ext.add_dh_bonus_data(data, 1)

    def run(self, target, **kwargs):
        targets = ext.collect_all_minions(self, False, oop=True)
        return [std_events.AreaDamage(self.game, self, targets, [self.dh_values[0] for _ in targets])]


# 冲锋 (90003)
class 冲锋(Spell):
    data = {
        'id': 90003,
        'type': 1, 'klass': 9, 'cost': 1,
        'po_tree': '$HaveTarget',
    }

    can_do_action = ext.require_minion
    check_target = ext.checker_minion

    def run(self, target, **kwargs):
        # TODO
        return []


# 顺劈斩 (90004)
class 顺劈斩(Spell):
    data = {
        'id': 90004,
        'type': 1, 'klass': 9, 'cost': 2,
    }
    ext.add_dh_bonus_data(data, 2)

    def can_do_action(self, msg_fn=None):
        super_result = super().can_do_action(msg_fn=msg_fn)

        if self.zone == Zone.Hand and len(self.game.get_zone(Zone.Play, 1 - self.player_id)) < 2:
            if msg_fn:
                msg_fn('Your opponent must have at least 2 minions!')
            return self.Inactive

        return super_result

    def run(self, target, **kwargs):
        """Deal damage in random order.

        See <https://hearthstone.gamepedia.com/Damage#Advanced_rules> and its explanation on "Multi-Shot" for details.
        """
        zone = self.game.get_zone(Zone.Play, 1 - self.player_id)
        if len(zone) == 0:
            return []
        elif len(zone) < 2:
            real_targets = zone
        else:
            real_targets = random.sample(zone, 2)
        return [std_events.AreaDamage(self.game, self, real_targets, [self.dh_values[0] for _ in real_targets])]


# 斩杀 (90005)
class 斩杀(Spell):
    data = {
        'id': 90005,
        'type': 1, 'klass': 9, 'cost': 2,
        'po_tree': '$HaveTarget',
    }

    # TODO: checkers

    def run(self, target, **kwargs):
        # TODO
        return []


# 英勇打击 (90006)
class 英勇打击(Spell):
    data = {
        'id': 90006,
        'type': 1, 'klass': 9, 'cost': 2,
    }

    def run(self, target, **kwargs):
        # TODO
        return []


# 盾牌格挡 (90007)

# 炽炎战斧 (90008)
ext.blank_weapon({
    'id': 90008,
    'type': 2, 'klass': 9, 'cost': 3, 'attack': 3, 'health': 2,
})

# 奥金斧 (90009)
