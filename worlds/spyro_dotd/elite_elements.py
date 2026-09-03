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