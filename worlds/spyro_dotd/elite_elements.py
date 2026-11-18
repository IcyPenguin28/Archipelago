from __future__ import annotations

from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from .world import DotDWorld

DEFAULT_ELITE_ELEMENTS = {
    "Grublin":      ["Shadow"],
    "Grublin Fly":  ["Earth"],
    "Axe Orc":      ["Electricity", "Fear"],
    "Troll":        ["Fire", "Ice", "Poison"],
    "Crossbow Orc": ["Poison", "Wind"],
    "Hero Orc":     ["Earth", "Electricity", "Fear"],
    "Wyvern":       ["Ice", "Wind"],
    "Hero Grublin": ["Fire", "Shadow"]
}

# Enemy data
ENEMY_NAME_TO_ID = {
    "Grublin":      b"\x00",
    "Grublin Fly":  b"\x01",
    "Hero Grublin": b"\x02",
    "Crossbow Orc": b"\x03",
    "Axe Orc":      b"\x04",
    "Hero Orc":     b"\x05",
    "Troll":        b"\x06",
    "Shadow":       b"\x07",
    "Wyvern":       b"\x08"
}

LEVEL_NAME_TO_ELITES = {
    "The Catacombs": ["Grublin"],
    "Twilight Falls": ["Grublin Fly"],
    "Valley of Avalar": ["Axe Orc"],
    "Ruins of Warfang": ["Troll"],
    "The Dam": ["Crossbow Orc"],
    "Burned Lands": ["Hero Orc"],
    "Floating Islands": ["Wyvern", "Hero Grublin"],
}

# These are base durabilities manually calculated in a way so that the masks can be broken in solo with lvl 1 elements, no armors and base mana
# Masks are very weird and somehow take more damage from dmg/second attacks like Dragon Fire every frame (Elite itself takes normal damage)
# They also take damage while the enemy is blocking, even if the enemy itself doesn't
# Most Elites have green gem clusters nearby so these durabilities could be buffed a little
ELITE_ELEMENT_TO_BASE_DURABILITY = {
    "Fire": 900.0,
    "Ice": 600.0,
    "Earth": 500.0,
    "Electricity": 200.0,
    "Poison": 500.0,
    "Shadow": 1000.0,
    "Fear": 1000.0,
    "Wind": 500.0
}

ELITE_ELEMENT_TO_MASK_COLOR = {
    "Fire": bytes([0xAF, 0x4F, 0x00]),
    "Ice": bytes([0x20, 0x7F, 0xFF]),
    "Earth": bytes([0x00, 0x67, 0x22]),
    "Electricity": bytes([0xAF, 0x96, 0x00]),
    "Poison": bytes([0x55, 0x99, 0x00]),
    "Shadow": bytes([0x00, 0x00, 0x24]),
    "Fear": bytes([0x69, 0x00, 0x00]),
    "Wind": bytes([0x69, 0x69, 0x8F])
}

# Unfortunately, most Elite glows do not have the correct flags that allow to display darker colors (they get more transparent instead)
# These flags are read when deserializing the object, but editing those flags once the object has been deserialized does nothing,
# which is a shame because otherwise the fix would have been very easy
ELITE_ELEMENT_TO_GLOW_COLOR = {
    "Fire": bytes([0xFF, 0xAF, 0x00, 0xBF]),
    "Ice": bytes([0x7F, 0xCF, 0xFF, 0x7F]),
    "Earth": bytes([0x00, 0xFF, 0x00, 0x7F]),
    "Electricity": bytes([0xFF, 0xF4, 0x00, 0x8F]),
    "Poison": bytes([0xBB, 0xFF, 0x00, 0x9F]),
    "Shadow": bytes([0x00, 0x00, 0xFF, 0x9F]),   #Can't do black so blue it is
    "Fear": bytes([0xFF, 0x00, 0x00, 0x8F]),
    "Wind": bytes([0xFF, 0xFF, 0xFF, 0x9F])
}

ELITE_NAME_TO_GLOW_SIZE = {
    "Grublin":      3.0,
    "Grublin Fly":  3.0,
    "Axe Orc":      5.0,
    "Troll":        9.0,
    "Crossbow Orc": 4.0,
    "Hero Orc":     8.0
}

def get_elite_elements(world: DotDWorld):
    elites = DEFAULT_ELITE_ELEMENTS.copy()
    if world.options.random_elite_elements != 0:
        pool = ["Fire", "Ice", "Earth", "Electricity", "Poison", "Shadow", "Fear", "Wind"]
        for elite in elites.keys():
            # random unique
            if world.options.random_elite_elements == 2:
                element = world.random.choice(pool)
                elites[elite] = [element]
                pool.remove(element)
            # random normal
            else:
                elites[elite] = world.random.sample(pool, k=len(elites[elite]))

    # Support UT
    if hasattr(world.multiworld, "re_gen_passthrough") \
            and isinstance(world.multiworld.re_gen_passthrough, dict) \
            and world.game in world.multiworld.re_gen_passthrough:
        # UT YAML-less
        elites = world.elite_elements
    else:
        # Normal generation, handled via AP
        world.elite_elements = elites