#! /usr/bin/python
# -*- coding: utf-8 -*-

__author__ = 'fyabc'


def order_of_play(objects):
    """Sort objects by the order of play.

    :param objects: Entities or events or triggers.
    :return: List of objects, sorted by order of play.
    """

    return sorted(objects, key=lambda o: o.oop)


def error_and_stop(game, event, msg):
    """Show an error message and stop the event.

    :param game:
    :param event:
    :param msg:
    :return:
    """

    game.error_stub(msg)
    event.disable()
    game.stop_subsequent_phases()


def validate_cost(player, card, msg_fn):
    """Validate the cost of the card.

    :param player:
    :param card:
    :param msg_fn: Callable to show the error message on the frontend.
    :return: The card can be played or not.
    :rtype: bool
    """

    if player.displayed_mana() < card.cost:
        msg_fn('You do not have enough mana!')
        return False
    return True


def validate_target(card, target, msg_fn):
    """Validate the target of the card.

    :param card:
    :param target:
    :param msg_fn:
    :return: The target is valid or not.
    :rtype: bool
    """

    if not card.check_target(target):
        msg_fn('This is not a valid target!')
        return False
    return True


def validate_play_size(player, msg_fn):
    """Validate the size of the play zone.

    :param player:
    :param msg_fn:
    :return: The minion can be put into the play zone.
    :rtype: bool
    """

    if player.full(Zone.Play):
        msg_fn('I cannot have more minions!')
        return False
    return True


class EnumMeta(type):
    @staticmethod
    def __new__(mcs, name, bases, ns):
        str2idx = {k: v for k, v in ns.items() if not k.startswith('_')}
        idx2str = {v: k for k, v in str2idx.items()}
        ns['Str2Idx'] = str2idx
        ns['Idx2Str'] = idx2str

        return super().__new__(mcs, name, bases, ns)


class EntityType(metaclass=EnumMeta):
    """An enumeration class, contains entity types."""

    Card = 0
    Hero = 1
    Enchantment = 2
    Player = 3


class Type(metaclass=EnumMeta):
    """An enumeration class, contains card types."""

    Minion = 0
    Spell = 1
    Weapon = 2
    HeroCard = 3
    Permanent = 4   # Permanent card, such as the seed of 'Sherazin, Corpse Flower'.


class Zone(metaclass=EnumMeta):
    """An enumeration class, contains zones of the card."""

    Invalid = 0
    Deck = 1
    Hand = 2
    Play = 3
    Secret = 4
    Graveyard = 5
    SetAside = 6
    Weapon = 7
    Hero = 8
    HeroPower = 9


class Rarity(metaclass=EnumMeta):
    """An enumeration class, contains rarities."""

    Derivative = -1
    Basic = 0
    Common = 1
    Rare = 2
    Epic = 3
    Legend = 4


class Race(metaclass=EnumMeta):
    """An enumeration class, contains races."""

    Beast = 0
    Murloc = 1
    Mech = 2
    Demon = 3
    Dragon = 4
    Totem = 5
    Elemental = 6


class Klass(metaclass=EnumMeta):
    """An enumeration class, contains classes."""

    Neutral = 0
    Druid = 1
    Hunter = 2
    Mage = 3
    Paladin = 4
    Priest = 5
    Rogue = 6
    Shaman = 7
    Warlock = 8
    Warrior = 9
    Monk = 10
    DeathKnight = 11


class Condition:
    """The class of conditions to get random cards or select cards."""

    pass


__all__ = [
    'order_of_play',
    'error_and_stop',

    'validate_cost',
    'validate_target',
    'validate_play_size',

    'Type', 'Zone', 'Rarity', 'Race', 'Klass', 'Condition',
]
