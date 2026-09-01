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
        "Catacombs Health Gem"
    ],
    "Catacombs Waterfall Base": [
        "Catacombs Blue Gem - Waterfall Room Right",
        "Catacombs Blue Gem - Waterfall Room Near Breakable Stones",
        "Catacombs Mana Gem"
    ],
    "Catacombs Waterfall": [
        "Catacombs Blue Gem - Waterfall Room Under Right Breakable Stone",
        "Catacombs Blue Gem - Waterfall Room Under Left Breakable Stone",
        "Catacombs Blue Gem - Waterfall Room Pillars 2",
        "Catacombs Blue Gem - Waterfall Room Top Left",
        "Catacombs Blue Gem - Waterfall Room Pillars 1",
        "Catacombs Blue Gem - Waterfall Room Save Point",
        "Catacombs Blue Gem - Before Wind Horn",
        "Catacombs Elite",
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
    "VoA Post-Village": [   # All locations reachable after saving the village without any other abilities
        "VoA Blue Gem - Near Passageway Right",
        "VoA Blue Gem - Island",
        "VoA Blue Gem - Hidden Area",
        "VoA Blue Gem - Above Passageway",
        "VoA Blue Gem - Near Meadow Cave",
        "VoA Blue Gem - Cheetah Village",
        "VoA Blue Gem - Between Passageway and Hidden Area"
        "VoA Blue Gem - On Top of Platform Near Island",
        "VoA Blue Gem - Right of Big Waterfall",
        "VoA Blue Gem - Near Raft",
        "VoA Blue Gem - Behind Supply Cave",
        "VoA Blue Gem - Near Cheetah Village",
        "VoA Blue Gem - Under Platform Near Island",
        "VoA Blue Gem - Left of Big Waterfall",
        "VoA Blue Gem - Near Supply Cave",
        "VoA Health Gem - Big Oak",
        "VoA Mana Gem - Island",
        "VoA Armor Chest - Big Waterfall"
    ],
    "VoA Elite Cliff": [
        "VoA Blue Gem - Near Elite",
        "VoA Elite",
        "VoA Health Gem - Near Elite",
    ],
    "VoA Above Meadow Cave": [
        "VoA Blue Gem - Above Meadow Cave",
        "VoA Armor Chest - Above Meadow Cave"
    ],
    "VoA Meadow Cave": [
        "Objective Complete - Find Meadow",
        "VoA Armor Chest - Meadow"
    ],
    "VoA Hermit Cave": [
        "VoA Blue Gem - Hermit Area Tunnels",
        "VoA Health Gem - Hermit Area Tunnels",
    ],
    "VoA Hermit Cave Beyond Wind": [
        "VoA Blue Gem - Near Hermit"
        "VoA Armor Chest - Hermit",
        "VoA Mana Gem - Near Hermit",
        "Objective Complete - Find the Hermit"
    ],
    "VoA Post-Hermit": [
        "VoA Mana Gem - Behind Gate"
        "Valley of Avalar Cleared",
        "Objective Complete - Find the Supply Cave",
        "Objective Complete - Find the Raft",
        "Objective Complete - Bring the Raft to Meadow",
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


def connect_subregions_voa(world: DotDWorld):
    """
    Splits Twilight Falls into sub-regions so individual Twilight Falls locations
    don't need to restate the same base item requirements redundantly
    """
    player = world.player
    voa = world.get_region("Valley of Avalar")

    post_village = Region("VoA Post-Village", player, world.multiworld)
    above_meadow_cave = Region("VoA Above Meadow Cave", player, world.multiworld)
    meadow_cave = Region("Voa Meadow Cave", player, world.multiworld)
    elite_cliff = Region("VoA Elite Cliff", player, world.multiworld)
    hermit_cave = Region("VoA Hermit Cave", player, world.multiworld)
    hermit_cave_beyond_wind = Region("VoA Hermit Cave Beyond Wind", player, world.multiworld)
    post_hermit = Region("VoA Post-Hermit", player, world.multiworld)

    voa.connect(post_village, "VoA Entrance -> Post-Village", \
                rule=lambda state: state.can_reach_location("Objective Complete - Save the Cheetah Village", player))
    post_village.connect(above_meadow_cave, "VoA Post-Village -> Above Meadow Cave", \
                rule=lambda state: state.has("Wall Climbing", player))
    post_village.connect(meadow_cave, "VoA Post-Village -> Meadow Cave")
    # NOTE: You can get to the top of the elite cliff just with flight, so a setting may be in order.
    post_village.connect(elite_cliff, "VoA Post-Village -> Elite Cliff", \
                rule=lambda state: state.has_all(("Wall Climbing", "Wall Running"), player))
    post_village.connect(hermit_cave, "VoA Post-Village -> Hermit Cave", \
                rule=lambda state: state.can_reach_location("Objective Complete - Find Meadow", player))
    hermit_cave.connect(hermit_cave_beyond_wind, "VoA Hermit Cave -> Hermit Cave Beyond Wind", \
                rule=lambda state: state.has_all(("Wall Climbing", "Wall Running"), player))
    hermit_cave_beyond_wind.connect(post_hermit, "VoA Hermit Cave Beyond Wind-> Post-Hermit", \
                rule=lambda state: state.can_reach_location("Objective Complete - Find the Hermit", player))

def connect_subregions_aotg(world: DotDWorld):
    # LMFAO, AotG moment xD
    pass
    