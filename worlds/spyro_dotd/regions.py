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

CATACOMBS_SUBREGION_LOCATIONS = {
    "Catacombs Beyond Vines": [
        "Catacombs Blue Gem - Weight Room",
    ],
    "Catacombs Waterfall Base": [
        "Catacombs Blue Gem - Waterfall Room Under Right Breakable Stone",
        "Catacombs Blue Gem - Waterfall Room Under Left Breakable Stone",
        "Catacombs Blue Gem - Waterfall Room Right",
        "Catacombs Blue Gem - Waterfall Room Near Breakable Stones",
        "Catacombs Health Gem",
        "Catacombs Mana Gem",
        "Catacombs Elite"
    ],
    "Catacombs Waterfall": [
        "Catacombs Blue Gem - Waterfall Room Pillars 2",
        "Catacombs Blue Gem - Waterfall Room Top Left",
        "Catacombs Blue Gem - Waterfall Room Pillars 1",
        "Catacombs Blue Gem - Waterfall Room Save Point",
        "Catacombs Blue Gem - Before Wind Horn",
        "The Catacombs Cleared"
    ],
}

TWILIGHT_FALLS_SUBREGION_LOCATIONS = {
    "TF Beyond Vines": [
        "TF Blue Gem - Behind Vines",
        "TF Armor Chest - Behind Vines"
    ],
    "TF End of Level": [
        "TF Health Gem",
        "TF Blue Gem - End of Level",
        "Twilight Falls Cleared",
        "Objective Complete - Reach the Enchanted Forest"
    ]
}

VALLEY_OF_AVALAR_SUBREGION_LOCATIONS = {
    "VoA Elite Cliff": [
        "VoA Blue Gem - Near Elite",
        "VoA Elite",
        "VoA Health Gem - Near Elite"
    ],
    "VoA Hermit Cave - Beyond Wind": [
        
    ]

}

def create_and_connect_regions(world: DotDWorld) -> None:
    create_all_regions(world)
    connect_regions(world)

    connect_subregions_catacombs(world)
    connect_subregions_tf(world)


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
    menu.connect(gallery, "Menu -> Gallery")

    # Make every chapter connect to the menu in a hub & spoke pattern
    for i, region in enumerate(regions[1:], start=1):
        def make_rule(n):
            return lambda state: state.count("Progressive Chapter Unlock", player) >= n
        menu.connect(region, f"Menu -> Chapter {i + 1}", make_rule(i))

    # Malefor's Lair unlocks once every other chapter has been unlocked
    menu.connect(malefor, "Menu -> Malefor's Lair",
                 lambda state: state.count("Progressive Chapter Unlock", player) >= len(regions))


def connect_subregions_catacombs(world: DotDWorld):
    """
    Splits Catacombs into sub-regions so individual Catacombs locations
    don't need to restate the same base item requirements redundantly
    """
    player = world.player
    catacombs = world.get_region("Catacombs")

    beyond_vines = Region("Catacombs Beyond Vines", player, world.multiworld)
    waterfall_base = Region("Catacombs Waterfall Base", player, world.multiworld)
    waterfall = Region("Catacombs Waterfall", player, world.multiworld)

    world.multiworld.regions += [beyond_vines, waterfall_base, waterfall]

    catacombs.connect(beyond_vines, "Catacombs Entrance -> Beyond Vines", \
                      rule=lambda state: state.has_any(("Spyro's Fire", "Cynder's Poison"), player))
    beyond_vines.connect(waterfall_base, "Catacombs Beyond Vines -> Waterfall Base", \
                          rule=lambda state: state.has("Spyro's Electricity", player))
    waterfall_base.connect(waterfall, "Catacombs Waterfall Base -> Waterfall", \
                           rule=lambda state: state.has("Wall Climbing"))


def connect_subregions_tf(world: DotDWorld):
    """
        Splits Twilight Falls into sub-regions so individual Twilight Falls locations
        don't need to restate the same base item requirements redundantly
        """
    player = world.player
    tf = world.get_region("Twilight Falls")

    eol = Region("TF End of Level", player, world.multiworld)
    beyond_vines = Region("TF Beyond Vines", player, world.multiworld)

    world.multiworld.regions += [beyond_vines, eol]

    tf.connect(eol, "TF Entrance -> End of Level", \
               rule=lambda state: state.has_all(("Wall Climbing", "Chain Swinging"), player))
    tf.connect(beyond_vines, "TF Entrance -> Beyond Vines", \
               rule=lambda state: state.has_any(("Spyro's Fire", "Poison"), player))