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
        "Catacombs Blue Gem - Waterfall Room Pillars 1",
        "Catacombs Blue Gem - Waterfall Room Pillars 2",
        "Catacombs Blue Gem - Waterfall Room Top Left",
        "Catacombs Blue Gem - Waterfall Room Under Right Breakable Stone",
        "Catacombs Blue Gem - Waterfall Room Under Left Breakable Stone",
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
        "TF Blue Gem - End of Level",
        "TF Health Gem",
        "Objective Complete - Reach the Enchanted Forest",
        "Twilight Falls Cleared"
    ]
}

VALLEY_OF_AVALAR_SUBREGION_LOCATIONS = {
    "VoA Post-Village": [   # All locations reachable after saving the village without any other abilities
        "VoA Blue Gem - Near Cheetah Village",
        "VoA Blue Gem - Near Meadow Cave",
        "VoA Blue Gem - Under Platform Near Island",
        "VoA Blue Gem - On Top of Platform Near Island",
        "VoA Blue Gem - Island",
        "VoA Blue Gem - Right of Big Waterfall",
        "VoA Blue Gem - Left of Big Waterfall",
        "VoA Blue Gem - Near Supply Cave",
        "VoA Blue Gem - Behind Supply Cave",
        "VoA Blue Gem - Above Passageway",
        "VoA Blue Gem - Near Passageway Right",
        "VoA Blue Gem - Between Passageway and Hidden Area",
        "VoA Blue Gem - Hidden Area",
        "VoA Blue Gem - Near Raft",
        "VoA Health Gem - Big Oak",
        "VoA Mana Gem - Island",
        "VoA Armor Chest - Big Waterfall"
    ],
    "VoA Elite Cliff": [
        "VoA Blue Gem - Near Elite",
        "VoA Health Gem - Near Elite",
        "VoA Elite"
    ],
    "VoA Above Meadow Cave": [
        "VoA Blue Gem - Above Meadow Cave",
        "VoA Armor Chest - Above Meadow Cave"
    ],
    "VoA Meadow Cave": [
        "VoA Armor Chest - Meadow",
        "Objective Complete - Find Meadow"
    ],
    "VoA Hermit Cave": [
        "VoA Blue Gem - Hermit Area Tunnels",
        "VoA Health Gem - Hermit Area Tunnels"
    ],
    "VoA Hermit Cave Beyond Wind": [
        "VoA Blue Gem - Near Hermit",
        "VoA Mana Gem - Near Hermit",
        "VoA Armor Chest - Hermit",
        "Objective Complete - Find the Hermit"
    ],
    "VoA Post-Hermit": [
        "VoA Mana Gem - Behind Gate",
        "Objective Complete - Find the Supply Cave",
        "Objective Complete - Find the Raft",
        "Objective Complete - Bring the Raft to Meadow",
        "Valley of Avalar Cleared"
    ]
}

DRAGON_CITY_SUBREGION_LOCATIONS = {
    "DC Ramparts": [
        "DC Blue Gem - Beginning of Ramparts",
        "DC Blue Gem - Behind Catapult",
        "DC Health Gem - Ramparts Left",
        "DC Mana Gem - Ramparts Right",
        "Objective Complete - Protect the Catapult",
        "Objective Complete - Destroy the Siege Tower (first)",
        "Objective Complete - Escort the Artillery Mole to the Catapult",
        "Objective Complete - Destroy the Siege Tower (second)",
        "Objective Complete - Destroy the last two Siege Towers"
    ],
    "DC Ramparts Back Exit": [
        "DC Blue Gem - Broken Stairs Top",
        "DC Blue Gem - Broken Stairs Bottom",
        "DC Blue Gem - Near Armor Chest",
        "DC Armor Chest - Near Second Save Point"
    ],
    "DC City Gates": [
        "DC Blue Gem - Behind Shadow Gate Near Doors",
        "DC Armor Chest - Troll"
    ],
    "DC End of Level": [
        "Objective Complete - Close the City Gates",
        "Dragon City Cleared"
    ]
}

RUINS_OF_WARFANG_SUBREGION_LOCATIONS = {
    "RoW Lower Left Trap Road": [
        "RoW Blue Gem - Left Path Near Wallrun",
        "RoW Blue Gem - Left Path Near Trap"
    ],
    "RoW Upper Right": [
        "RoW Blue Gem - Up Right Path Near Key",
        "RoW Health Gem - Up Right Path Near Key",
        "RoW Mana Gem - Up Right Path After Falling Stones",
        "RoW Armor Chest - Up Right Path Under Earth Slab"
    ],
    "RoW Upper Left": [
        "RoW Mana Gem - Up Left Path Behind Shadow Gate",
        "RoW Health Gem - Left Path Trap"
    ],
    "RoW End of Level": [
        "Objective Complete - Open the Gates to the Ruins of Warfang",
        "Ruins of Warfang Cleared"
    ]
}

THE_DAM_SUBREGION_LOCATIONS = {
    "Dam Right Weight Gate": [
        "Dam Blue Gem - Near Save Point Left",
        "Dam Blue Gem - Near Save Point Right",
        "Dam Blue Gem - Near Earth Wall",
        "Dam Blue Gem - Top",
        "Dam Health Gem - Behind Shadow Gate After Hero Orc",
        "Dam Mana Gem - Behind Earth Wall",
        "Dam Armor Chest - Right Pillar",
        "Dam Armor Chest - Hero Orc",
        "Dam Elite",
        "Objective Complete - Open the Floodgates to the Dam",
        "Objective Complete - Open the Main Floodgate",
        "The Dam Cleared"
    ]
}

THE_DESTROYER_SUBREGION_LOCATIONS = {
    "Destroyer Top Half": [
        "Destroyer Blue Gem - Right Shoulder Left",
        "Destroyer Blue Gem - Right Shoulder Right",
        "Destroyer Armor Chest - Right Arm"
    ],
    "Destroyer Armpit and Beyond": [
        "Destroyer Blue Gem - Under Right Armpit",
        "Destroyer Health Gem - Right Arm",
        "Destroyer Mana Gem - Right Arm",
        "Destroyer Mana Gem - Mouth",
        "Objective Complete - Destroy all the crystals of the Destroyer",
        "The Destroyer Cleared"
    ],
}

BURNED_LANDS_SUBREGION_LOCATIONS = {
    "BL Beyond Climbing Wall": [
        "BL Blue Gem - Bridge Before Last Ring Right",
        "BL Blue Gem - Bridge Before Last Ring Left",
        "BL Blue Gem - Last Ring Area Far Left",
        "BL Blue Gem - Last Ring Area Far Right",
        "BL Blue Gem - After Last Ring Left",
        "BL Blue Gem - After Last Ring Right",
        "BL Mana Gem - Under Bridge",
        "Objective Complete - Reach the Volcano",
        "Burned Lands Cleared"
    ]
}

FLOATING_ISLANDS_SUBREGION_LOCATIONS = {
    "FI Beyond Torch Door": [
        "FI Blue Gem - Troll Island Left",
        "FI Blue Gem - Troll Island Top",
        "FI Blue Gem - Hero Grublin Elite Island Top",
        "FI Blue Gem - Hero Grublin Elite Island Middle",
        "FI Health Gem - Hero Grublin Elite Island",
        "FI Elite - Wyvern",
        "FI Elite - Hero Grublin",
        "Floating Islands Cleared"
    ]
}

def create_and_connect_regions(world: DotDWorld) -> None:
    create_all_regions(world)
    connect_regions(world)

    # Connect subregions
    # Yes, comments shouldn't state the obvious...
    # but I have trouble finding this block of code and this comment helps
    connect_subregions_catacombs(world)
    connect_subregions_tf(world)
    connect_subregions_voa(world)
    connect_subregions_dc(world)
    connect_subregions_aotg(world)
    connect_subregions_row(world)
    connect_subregions_dam(world)
    connect_subregions_destroyer(world)
    connect_subregions_bl(world)
    connect_subregions_fi(world)


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
                      rule=lambda state: state.has_any((world.element_items["Fire"], world.element_items["Poison"]), player))
    beyond_vines.connect(waterfall_base, "Catacombs Beyond Vines -> Waterfall Base", \
                          rule=lambda state: state.has(world.element_items["Electricity"], player))
    waterfall_base.connect(waterfall, "Catacombs Waterfall Base -> Waterfall", \
                           rule=lambda state: state.has("Wall Climbing", player))


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
               rule=lambda state: state.has("Wall Climbing", player))
               # rule=lambda state: state.has_all(("Wall Climbing", "Chain Swinging"), player)) # Swap when and if we can gate swinging
    tf.connect(beyond_vines, "TF Entrance -> Beyond Vines", \
               rule=lambda state: state.has_any((world.element_items["Fire"], world.element_items["Poison"]), player))


def connect_subregions_voa(world: DotDWorld):
    """
    Splits Valley of Avalar into sub-regions so individual Valley of Avalar locations
    don't need to restate the same base item requirements redundantly
    """
    player = world.player
    voa = world.get_region("Valley of Avalar")

    post_village = Region("VoA Post-Village", player, world.multiworld)
    above_meadow_cave = Region("VoA Above Meadow Cave", player, world.multiworld)
    meadow_cave = Region("VoA Meadow Cave", player, world.multiworld)
    elite_cliff = Region("VoA Elite Cliff", player, world.multiworld)
    hermit_cave = Region("VoA Hermit Cave", player, world.multiworld)
    hermit_cave_beyond_wind = Region("VoA Hermit Cave Beyond Wind", player, world.multiworld)
    post_hermit = Region("VoA Post-Hermit", player, world.multiworld)

    world.multiworld.regions += [post_village, above_meadow_cave, meadow_cave, elite_cliff, \
                                 hermit_cave, hermit_cave_beyond_wind, post_hermit]

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


def connect_subregions_dc(world: DotDWorld):
    """
    Splits Dragon City into sub-regions so individual Dragon City locations
    don't need to restate the same base item requirements redundantly
    """
    player = world.player
    dc = world.get_region("Dragon City")

    ramparts = Region("DC Ramparts", player ,world.multiworld)
    back_exit = Region("DC Ramparts Back Exit", player, world.multiworld)
    city_gates = Region("DC City Gates", player, world.multiworld)
    eol = Region("DC End of Level", player, world.multiworld)

    world.multiworld.regions += [ramparts, back_exit, city_gates, eol]

    dc.connect(ramparts, "DC Entrance -> Ramparts", \
               rule=lambda state: state.can_reach_location("Objective Complete - Extinguish the Fire", player))
    ramparts.connect(back_exit, "DC Ramparts -> Ramparts Back Exit", \
                rule=lambda state: state.can_reach_location("Objective Complete - Protect the Catapult", player))
    back_exit.connect(city_gates, "DC Ramparts Back Exit -> City Gates", \
                rule=lambda state: state.has("Wall Climbing", player))
    city_gates.connect(eol, "DC City Gates -> End of Level", \
                rule=lambda state: state.has(world.element_items["Fire"], player))


def connect_subregions_aotg(world: DotDWorld):
    """
    Splits Attack of the Golem into sub-regions so individual Attack of the Golem locations
    don't need to restate the same base item requirements redundantly
    """
    # LMFAO, AotG moment xD
    pass


def connect_subregions_row(world: DotDWorld):
    """
    Splits Ruins of Warfang into sub-regions so individual Ruins of Warfang locations
    don't need to restate the same base item requirements redundantly
    """
    player = world.player
    row = world.get_region("Ruins of Warfang")

    trap_road = Region("RoW Lower Left Trap Road", player, world.multiworld)
    upper_right = Region("RoW Upper Right", player, world.multiworld)
    upper_left = Region("RoW Upper Left", player, world.multiworld)
    eol = Region("RoW End of Level", player, world.multiworld)

    world.multiworld.regions += [trap_road, upper_left, upper_right, eol]

    row.connect(trap_road, "RoW Entrance -> Trap Road", \
                rule=lambda state: state.has("Wall Climbing", player))
    row.connect(upper_right, "RoW Entrance -> Upper Right", \
                rule=lambda state: state.has_all((world.element_items["Fear"], "Wall Climbing", world.element_items["Earth"], "Wall Running"), player))
                # rule=lambda state: state.has_all((world.element_items["Fear"], "Wall Climbing", world.element_items["Earth"], "Chain Swinging", "Wall Running"), player)) # Swap when and if we can gate swinging
    row.connect(upper_left, "RoW Entrance -> Upper Left", \
                rule=lambda state: state.has_all((world.element_items["Fire"], world.element_items["Shadow"], "Wall Climbing"), player))
                # rule=lambda state: state.has_all((world.element_items["Fire"], world.element_items["Shadow"], "Wall Climbing", "Chain Swinging"), player))    # Swap when and if we can gate swinging
    row.connect(eol, "RoW Entrance -> End of Level", \
                rule=lambda state: state.has_all(("Wall Climbing", world.element_items["Fear"], world.element_items["Electricity"], world.element_items["Shadow"], world.element_items["Fire"], world.element_items["Earth"], "Wall Running"), player))
                # rule=lambda state: state.has_all(("Wall Climbing", world.element_items["Fear"], world.element_items["Electricity"], world.element_items["Shadow"], world.element_items["Fire"], "Chain Swinging", world.element_items["Earth"], "Wall Running"), player)) # Swap when and if we can gate swinging


def connect_subregions_dam(world: DotDWorld):
    """
    Splits Dam into sub-regions so individual Dam locations
    don't need to restate the same base item requirements redundantly
    """
    player = world.player
    dam = world.get_region("The Dam")

    right_weight_gate = Region("Dam Right Weight Gate", player, world.multiworld)

    world.multiworld.regions += [right_weight_gate]

    # Requires Shadow to access the weight and wall climbing to get it up to the nearby floodgate
    dam.connect(right_weight_gate, "Dam Entrance -> Right Weight Gate", \
                rule=lambda state: state.has_all(("Wall Climbing", world.element_items["Shadow"]), player))


def connect_subregions_destroyer(world: DotDWorld):
    """
    Splits Destroyer into sub-regions so individual Destroyer locations
    don't need to restate the same base item requirements redundantly
    """
    player = world.player
    destroyer = world.get_region("The Destroyer")

    top_half = Region("Destroyer Top Half", player, world.multiworld)
    armpit = Region("Destroyer Armpit and Beyond", player, world.multiworld)

    world.multiworld.regions += [top_half, armpit]

    destroyer.connect(top_half, "Destroyer Entrance -> Top Half", \
                rule=lambda state: state.has("Wall Running", player))
    top_half.connect(armpit, "Destroyer Top Half -> Armpit and Beyond", \
                rule=lambda state: state.has("Wall Climbing", player))


def connect_subregions_bl(world: DotDWorld):
    """
    Splits Burned Lands into sub-regions so individual Burned Lands locations
    don't need to restate the same base item requirements redundantly
    """
    player = world.player
    bl = world.get_region("Burned Lands")

    beyond_climbing_wall = Region("BL Beyond Climbing Wall", player, world.multiworld)

    world.multiworld.regions += [beyond_climbing_wall]

    bl.connect(beyond_climbing_wall, "BL Entrance -> Beyond Climbing Wall", \
               rule=lambda state: state.has("Wall Climbing", player))


def connect_subregions_fi(world: DotDWorld):
    """
    Splits Floating Islands into sub-regions so individual Floating Islands locations
    don't need to restate the same base item requirements redundantly
    """
    player = world.player
    fi = world.get_region("Floating Islands")

    beyond_torch_door = Region("FI Beyond Torch Door", player, world.multiworld)

    world.multiworld.regions += [beyond_torch_door]

    fi.connect(beyond_torch_door, "FI Entrance -> Beyond Torch Door", \
               rule=lambda state: state.can_reach_location("Objective Complete - Torches Lit 8/8", player))


