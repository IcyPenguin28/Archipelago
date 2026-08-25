from __future__ import annotations
from typing import TYPE_CHECKING
from BaseClasses import Region
if TYPE_CHECKING:
    from .world import DotDWorld

SHUFFLEABLE_CHAPTERS = [
    "Catacombs", "Twilight Falls", "Valley of Avalar", "Dragon City",
    "Attack of the Golem", "Ruins of Warfang", "The Dam",
    "The Destroyer", "Burned Lands", "Floating Islands"
]

def create_and_connect_regions(world: DotDWorld) -> None:
    create_all_regions(world)
    connect_regions(world)


def create_all_regions(world: DotDWorld) -> None:
    regions = [
        Region("Menu", world.player, world.multiworld),
        Region("Gallery", world.player, world.multiworld),
        Region("Catacombs", world.player, world.multiworld),
        Region("Twilight Falls", world.player, world.multiworld),
        Region("Valley of Avalar", world.player, world.multiworld),
        Region("Dragon City", world.player, world.multiworld),
        Region("Attack of the Golem", world.player, world.multiworld),
        Region("Ruins of Warfang", world.player, world.multiworld),
        Region("The Dam", world.player, world.multiworld),
        Region("The Destroyer", world.player, world.multiworld),
        Region("Burned Lands", world.player, world.multiworld),
        Region("Floating Islands", world.player, world.multiworld),
        Region("Malefor's Lair", world.player, world.multiworld),
    ]
    world.multiworld.regions += regions


def connect_regions(world: DotDWorld) -> None:
    player = world.player

    if world.options.shuffle_chapter_order:
        shuffled = list(SHUFFLEABLE_CHAPTERS)
        world.random.shuffle(shuffled)
    else:
        shuffled = list(SHUFFLEABLE_CHAPTERS)

    # Support UT
    if hasattr(world.multiworld, "re_gen_passthrough") \
            and isinstance(world.multiworld.re_gen_passthrough, dict) \
            and world.game in world.multiworld.re_gen_passthrough:
        # UT YAML-less
        shuffled = world.chapter_order
    else:
        # Normal generation, handled via AP
        world.chapter_order = shuffled

    # Get regions
    menu    = world.get_region("Menu")
    gallery = world.get_region("Gallery")
    malefor = world.get_region("Malefor's Lair")
    regions = [world.get_region(name) for name in shuffled]

    # First chapter is always free, no item is needed
    menu.connect(regions[0])

    # Connect menu to gallery for free just for my own sake
    menu.connect(gallery, "Menu to Gallery")

    for i, region in enumerate(regions):
        next_region = regions[i + 1] if i + 1 < len(regions) else malefor
        def make_rule(n):
            return lambda state: state.count("Progressive Chapter Unlock", player) >= n
        region.connect(next_region, f"Chapter {i + 1} to Chapter {i + 2}", make_rule(i + 1))