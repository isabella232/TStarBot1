from __future__ import absolute_import
from __future__ import division
from __future__ import print_function

from enum import Enum
from enum import unique
from collections import namedtuple

from pysc2.lib.typeenums import UNIT_TYPEID as UNIT_TYPE


@unique
class ALLY_TYPE(Enum):
  SELF = 1
  ALLY = 2
  NEUTRAL = 3
  ENEMY = 4


@unique
class PLAYER_FEATURE(Enum):
  PLAYER_ID = 0
  MINERALS = 1
  VESPENE = 2
  FOOD_USED = 3
  FOOD_CAP = 4
  FOOD_ARMY = 5
  FOOD_WORKER = 6
  IDLE_WORKER_COUNT = 7
  ARMY_COUNT = 8
  WARP_GATE_COUNT = 9
  LARVA_COUNT = 10


NEUTRAL_DESTRUCTABLEROCKEX14X4 = 638
NEUTRAL_UNBUILDABLEROCKSDESTRUCIBLE = 472


PLACE_COLLISION_BUILDINGS = {
    UNIT_TYPE.NEUTRAL_MINERALFIELD.value,
    UNIT_TYPE.NEUTRAL_MINERALFIELD750.value,
    UNIT_TYPE.NEUTRAL_VESPENEGEYSER.value,
    UNIT_TYPE.NEUTRAL_DESTRUCTIBLEROCK6X6.value,
    UNIT_TYPE.NEUTRAL_DESTRUCTIBLEROCKEX1DIAGONALHUGEBLUR.value,
    NEUTRAL_DESTRUCTABLEROCKEX14X4,
    NEUTRAL_UNBUILDABLEROCKSDESTRUCIBLE,
    UNIT_TYPE.ZERG_EXTRACTOR.value,
    UNIT_TYPE.ZERG_SPAWNINGPOOL.value,
    UNIT_TYPE.ZERG_ROACHWARREN.value,
    UNIT_TYPE.ZERG_HYDRALISKDEN.value,
    UNIT_TYPE.ZERG_HATCHERY.value,
    UNIT_TYPE.ZERG_EVOLUTIONCHAMBER.value,
    UNIT_TYPE.ZERG_BANELINGNEST.value,
    UNIT_TYPE.ZERG_INFESTATIONPIT.value,
    UNIT_TYPE.ZERG_SPIRE.value,
    UNIT_TYPE.ZERG_ULTRALISKCAVERN.value,
    UNIT_TYPE.ZERG_NYDUSNETWORK.value,
    UNIT_TYPE.ZERG_SPINECRAWLER.value,
    UNIT_TYPE.ZERG_SPORECRAWLER.value,
    UNIT_TYPE.ZERG_LURKERDENMP.value,
    UNIT_TYPE.ZERG_LAIR.value,
    UNIT_TYPE.ZERG_HIVE.value,
    UNIT_TYPE.ZERG_GREATERSPIRE.value
}


MAXIMUM_NUM = {
    UNIT_TYPE.ZERG_SPAWNINGPOOL.value: 1,
    UNIT_TYPE.ZERG_ROACHWARREN.value: 1,
    UNIT_TYPE.ZERG_HYDRALISKDEN.value: 1,
    UNIT_TYPE.ZERG_HATCHERY.value: 6,
    UNIT_TYPE.ZERG_EVOLUTIONCHAMBER.value: 2,
    UNIT_TYPE.ZERG_BANELINGNEST.value: 1,
    UNIT_TYPE.ZERG_INFESTATIONPIT.value: 1,
    UNIT_TYPE.ZERG_SPIRE.value: 1,
    UNIT_TYPE.ZERG_ULTRALISKCAVERN.value: 1,
    UNIT_TYPE.ZERG_NYDUSNETWORK.value: 1,
    UNIT_TYPE.ZERG_LURKERDENMP.value: 1,
    UNIT_TYPE.ZERG_LAIR.value: 1,
    UNIT_TYPE.ZERG_HIVE.value: 1,
    UNIT_TYPE.ZERG_ZERGLING.value: 20,
    UNIT_TYPE.ZERG_GREATERSPIRE.value: 1
}


AttackAttr = namedtuple('AttackAttr', ('can_attack_ground', 'can_attack_air'))


ATTACK_FORCE = {
    UNIT_TYPE.ZERG_LARVA.value: AttackAttr(False, False),
    UNIT_TYPE.ZERG_DRONE.value: AttackAttr(True, False),
    UNIT_TYPE.ZERG_ZERGLING.value: AttackAttr(True, False),
    UNIT_TYPE.ZERG_BANELING.value: AttackAttr(True, False),
    UNIT_TYPE.ZERG_ROACH.value: AttackAttr(True, False),
    UNIT_TYPE.ZERG_ROACHBURROWED.value: AttackAttr(True, False),
    UNIT_TYPE.ZERG_RAVAGER.value: AttackAttr(True, False),
    UNIT_TYPE.ZERG_HYDRALISK.value: AttackAttr(True, True),
    UNIT_TYPE.ZERG_LURKERMP.value: AttackAttr(True, False),
    UNIT_TYPE.ZERG_LURKERMPBURROWED.value: AttackAttr(True, False),
    UNIT_TYPE.ZERG_VIPER.value: AttackAttr(False, False),
    UNIT_TYPE.ZERG_MUTALISK.value: AttackAttr(True, True),
    UNIT_TYPE.ZERG_CORRUPTOR.value: AttackAttr(False, True),
    UNIT_TYPE.ZERG_BROODLORD.value: AttackAttr(True, False),
    UNIT_TYPE.ZERG_SWARMHOSTMP.value: AttackAttr(False, False),
    UNIT_TYPE.ZERG_LOCUSTMP.value: AttackAttr(True, False),
    UNIT_TYPE.ZERG_INFESTOR.value: AttackAttr(False, False),
    UNIT_TYPE.ZERG_ULTRALISK.value: AttackAttr(True, False),
    UNIT_TYPE.ZERG_BROODLING.value: AttackAttr(True, False),
    UNIT_TYPE.ZERG_OVERLORD.value: AttackAttr(False, False),
    UNIT_TYPE.ZERG_OVERSEER.value: AttackAttr(False, False),
    UNIT_TYPE.ZERG_QUEEN.value: AttackAttr(True, True),
    UNIT_TYPE.ZERG_CHANGELING.value: AttackAttr(False, False),
    UNIT_TYPE.ZERG_SPINECRAWLER.value: AttackAttr(True, False),
    UNIT_TYPE.ZERG_SPORECRAWLER.value: AttackAttr(False, True),
    UNIT_TYPE.ZERG_NYDUSCANAL.value: AttackAttr(False, False)
}


COMBAT_TYPES = {
    UNIT_TYPE.ZERG_ZERGLING.value,
    UNIT_TYPE.ZERG_BANELING.value,
    UNIT_TYPE.ZERG_ROACH.value,
    UNIT_TYPE.ZERG_ROACHBURROWED.value,
    UNIT_TYPE.ZERG_RAVAGER.value,
    UNIT_TYPE.ZERG_HYDRALISK.value,
    UNIT_TYPE.ZERG_LURKERMP.value,
    UNIT_TYPE.ZERG_LURKERMPBURROWED.value,
    UNIT_TYPE.ZERG_MUTALISK.value,
    UNIT_TYPE.ZERG_CORRUPTOR.value,
    UNIT_TYPE.ZERG_BROODLORD.value,
    UNIT_TYPE.ZERG_ULTRALISK.value
    #UNIT_TYPE.ZERG_LOCUSTMP.value,
    #UNIT_TYPE.ZERG_BROODLING.value
}


class MAP(object):
  WIDTH = 200.0
  HEIGHT = 176.0
  LEFT = 24.0
  RIGHT = 24.0
  TOP = 37.0
  BOTTOM = 4.0
