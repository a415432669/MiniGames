#! /usr/bin/python
# -*- coding: utf-8 -*-

"""Base classes of enchantment."""

__author__ = 'fyabc'


class Enchantment:
    """Base class of enchantment.

    Information from <https://hearthstone.gamepedia.com/Enchantment>:
        An enchantment, also known as a buff or debuff, is a special effect gained by a minion,
        or in rarer occasions by a weapon.

        Most enchantments belong to minions while on the battlefield.
        However, some enchantments affect cards of other types, and some are active while in the player's hand.
        Enchantments may be granted permanently, or temporarily by an aura.
    """
    pass


class OngoingEffect(Enchantment):
    """Ongoing enchantment.

    Information from <https://hearthstone.gamepedia.com/Enchantment>:
        Ongoing effects are minion, weapon, and boss Hero Power abilities which grant special effects
        on an ongoing basis. Ongoing effects are often referred to as auras, particularly those which grant
        temporary enchantments to other targets.
    """
    pass