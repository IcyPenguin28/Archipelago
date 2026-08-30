from __future__ import annotations

from typing import TYPE_CHECKING

from BaseClasses import ItemClassification, Location

from . import items
from .items import DotDItem
from .regions import CATACOMBS_SUBREGION_LOCATIONS, TWILIGHT_FALLS_SUBREGION_LOCATIONS

if TYPE_CHECKING:
    from .world import DotDWorld


# Every location must have a unique integer ID associated with it.
# We will have a lookup from location name to ID here that, in world.py, we will import and bind to the world class.
# Even if a location doesn't exist on specific options, it must be present in this lookup.

# Lookup reference: 1-99: Blue Gem Clusters
#                   101-120: Health Gems
#                   201-220: Mana Gems
#                   301-308: Elite Enemies
#                   401-420: Armor Chests
#                   501-510: Level Clears
#                   601-604: Gallery Unlocks
#                   701-722: Objectives Complete
LOCATION_NAME_TO_ID = {
    "Catacombs Blue Gem - Weight Room": 1,
    "Catacombs Blue Gem - Waterfall Room Under Right Breakable Stone": 2,
    "Catacombs Blue Gem - Waterfall Room Under Left Breakable Stone": 3,
    "Catacombs Blue Gem - Waterfall Room Pillars 2": 4,
    "Catacombs Blue Gem - Waterfall Room Top Left": 5,
    "Catacombs Blue Gem - Waterfall Room Pillars 1": 6,
    "Catacombs Blue Gem - Waterfall Room Right": 7,
    "Catacombs Blue Gem - Waterfall Room Near Breakable Stones": 8,
    "Catacombs Blue Gem - Waterfall Room Save Point": 9,
    "Catacombs Blue Gem - Before Wind Horn": 10,
    "TF Blue Gem - Hero Grublin": 11,
    "TF Blue Gem - Behind Vines": 12,
    "TF Blue Gem - Bottom of Waterfall": 13,
    "TF Blue Gem - Near Save Point": 14,
    "TF Blue Gem - Before Wind Tunnel": 15,
    "TF Blue Gem - In Waterfall": 16,
    "TF Blue Gem - End of Level": 17,
    "VoA Blue Gem - Near Passageway Right": 18,
    "VoA Blue Gem - Near Elite": 19,
    "VoA Blue Gem - Island": 20,
    "VoA Blue Gem - Hidden Area": 21,
    "VoA Blue Gem - Above Passageway": 22,
    "VoA Blue Gem - Near Hermit": 23,
    "VoA Blue Gem - Hermit Area Tunnels": 24,
    "VoA Blue Gem - Near Meadow Cave": 25,
    "VoA Blue Gem - Above Meadow Cave": 26,
    "VoA Blue Gem - Cheetah Village": 27,
    "VoA Blue Gem - Between Passageway and Hidden Area": 28,
    "VoA Blue Gem - On Top of Platform Near Island": 29,
    "VoA Blue Gem - Right of Big Waterfall": 30,
    "VoA Blue Gem - Near Raft": 31,
    "VoA Blue Gem - Behind Supply Cave": 32,
    "VoA Blue Gem - Near Cheetah Village": 33,
    "VoA Blue Gem - Under Platform Near Island": 34,
    "VoA Blue Gem - Left of Big Waterfall": 35,
    "VoA Blue Gem - Near Supply Cave": 36,
    "DC Blue Gem - First Save Point": 37,
    "DC Blue Gem - Behind Catapult": 38,
    "DC Blue Gem - Near Armor Chest": 39,
    "DC Blue Gem - Behind Shadow Gate Near Doors": 40,
    "DC Blue Gem - Above Fire": 41,
    "DC Blue Gem - Near Torches Gate": 42,
    "DC Blue Gem - Beginning of Remparts": 43,
    "DC Blue Gem - Broken Stairs Top": 44,
    "DC Blue Gem - Broken Stairs Bottom": 45,
    "RoW Blue Gem - Left Path Platform Under Trap": 46,
    "RoW Blue Gem - Right Path Between Malefor Mural and Lever": 47,
    "RoW Blue Gem - Bridge Left": 48,
    "RoW Blue Gem - Bridge Right": 49,
    "RoW Blue Gem - Up Right Path Near Key": 50,
    "RoW Blue Gem - Left Path Long Platform": 51,
    "RoW Blue Gem - Left Path Round Platform": 52,
    "RoW Blue Gem - Left Path Near Wallrun": 53,
    "RoW Blue Gem - Left Path Near Trap": 54,
    "RoW Blue Gem - Right Path Near Malefor Mural": 55,
    "RoW Blue Gem - Right Path Near Tuning Forks": 56,
    "RoW Blue Gem - Right Path Near Lever": 57,
    "RoW Blue Gem - Left Path Small Pillar": 58,
    "Dam Blue Gem - Near Save Point Left": 59,
    "Dam Blue Gem - Near Save Point Right": 60,
    "Dam Blue Gem - Middle": 61,
    "Dam Blue Gem - Near Earth Wall": 62,
    "Dam Blue Gem - Top": 63,
    "Destroyer Blue Gem - Right Wrist Left": 64,
    "Destroyer Blue Gem - Right Wrist Right": 65,
    "Destroyer Blue Gem - Right Shoulder Left": 66,
    "Destroyer Blue Gem - Right Shoulder Right": 67,
    "Destroyer Blue Gem - Left Arm": 68,
    "Destroyer Blue Gem - Hip Near Enemies": 69,
    "Destroyer Blue Gem - Hip Near Dark Crystal": 70,
    "Destroyer Blue Gem - Under Right Armpit": 71,
    "BL Blue Gem - Bridge Before Last Ring Right": 72,
    "BL Blue Gem - Last Ring Area Far Right": 73,
    "BL Blue Gem - Last Ring Area Far Left": 74,
    "BL Blue Gem - After Last Ring Left": 75,
    "BL Blue Gem - Bridge Before Last Ring Left": 76,
    "BL Blue Gem - After Last Ring Right": 77,
    "BL Blue Gem - Before Third Ring Middle": 78,
    "BL Blue Gem - After Third Ring": 79,
    "BL Blue Gem - Before Third Ring Left": 80,
    "BL Blue Gem - Before Third Ring Right": 81,
    "FI Blue Gem - Big Bonus Island Ground": 82,
    "FI Blue Gem - Lower Save Point Island Near Torch": 83,
    "FI Blue Gem - Big Bonus Island Middle": 84,
    "FI Blue Gem - Big Bonus Island Left": 85,
    "FI Blue Gem - Big Bonus Island Top": 86,
    "FI Blue Gem - Big Bonus Island Right": 87,
    "FI Blue Gem - Small Island Behind Wyvern Elite": 88,
    "FI Blue Gem - Troll Island Top": 89,
    "FI Blue Gem - Above Doors": 90,
    "FI Blue Gem - Wyvern Elite Island": 91,
    "FI Blue Gem - Lower Save Point Island": 92,
    "FI Blue Gem - Torch Island Near Mana Gem": 93,
    "FI Blue Gem - Small Island Near Torch": 94,
    "FI Blue Gem - Big Island Near Doors": 95,
    "FI Blue Gem - Hero Grublin Elite Island Middle": 96,
    "FI Blue Gem - Hero Grublins": 97,
    "FI Blue Gem - Hero Grublin Elite Island Top": 98,
    "FI Blue Gem - Troll Island Left": 99,
    "Catacombs Health Gem": 101,
    "TF Health Gem": 102,
    "VoA Health Gem - Big Oak": 103,
    "VoA Health Gem - Near Elite": 104,
    "VoA Health Gem - Hermit Area Tunnels": 105,
    "DC Health Gem - Behind Bottom Shadow Gate Near Fire": 106,
    "DC Health Gem - Torches": 107,
    "DC Health Gem - Remparts Left": 108,
    "AotG Health Gem": 109,
    "RoW Health Gem - Right Path Behind Vines": 110,
    "RoW Health Gem - Left Path Trap": 111,
    "RoW Health Gem - Up Right Path Near Key": 112,
    "Dam Health Gem - Behind Shadow Gate After Hero Orc": 113,
    "Dam Health Gem - Behind Left Shadow Gate": 114,
    "Destroyer Health Gem - Right Arm": 115,
    "Destroyer Health Gem - Left Arm": 116,
    "BL Health Gem - Before Third Ring": 117,
    "BL Health Gem - Elite": 118,
    "FI Health Gem - Big Bonus Island": 119,
    "FI Health Gem - Hero Grublin Elite Island": 120,
    "Catacombs Mana Gem": 201,
    "TF Mana Gem - Near Crystals": 202,
    "TF Mana Gem - Before Wind Tunnel": 203,
    "VoA Mana Gem - Behind Gate": 204,
    "VoA Mana Gem - Near Hermit": 205,
    "VoA Mana Gem - Island": 206,
    "DC Mana Gem - Near Pool Wheel": 207,
    "DC Mana Gem - Remparts Right": 208,
    "AotG Mana Gem": 209,
    "RoW Mana Gem - Up Right Path After Falling Stones": 210,
    "RoW Mana Gem - Left Path Behind Vines": 211,
    "RoW Mana Gem - Up Left Path Behind Shadow Gate": 212,
    "Dam Mana Gem - Wooden Platform": 213,
    "Dam Mana Gem - Behind Earth Wall": 214,
    "Destroyer Mana Gem - Right Arm": 215,
    "Destroyer Mana Gem - Mouth": 216,
    "BL Mana Gem - Under Bridge": 217,
    "BL Mana Gem - Hero Orc": 218,
    "BL Mana Gem - Under Last Ring Area": 219,
    "FI Mana Gem": 220,
    "Catacombs Elite": 301,
    "TF Elite": 302,
    "VoA Elite": 303,
    "RoW Elite": 304,
    "Dam Elite": 305,
    "BL Elite": 306,
    "FI Elite - Wyvern": 307,
    "FI Elite - Hero Grublin": 308,
    "TF Armor Chest - Behind Vines": 401,
    "TF Armor Chest - Near Elite": 402,
    "VoA Armor Chest - Above Meadow Cave": 403,
    "VoA Armor Chest - Meadow": 404,
    "VoA Armor Chest - Big Waterfall": 405,
    "VoA Armor Chest - Hermit": 406,
    "DC Armor Chest - Behind Top Shadow Gate Near Fire": 407,
    "DC Armor Chest - Near Second Save Point": 408,
    "DC Armor Chest - Troll": 409,
    "AotG Armor Chest": 410,
    "RoW Armor Chest - Up Right Path Under Earth Slab": 411,
    "RoW Armor Chest - Left Path Near Key": 412,
    "Dam Armor Chest - Right Pillar": 413,
    "Dam Armor Chest - Hero Orc": 414,
    "Destroyer Armor Chest - Right Arm": 415,
    "Destroyer Armor Chest - Torso": 416,
    "BL Armor Chest - Orcs": 417,
    "BL Armor Chest - Behind Dark Crystal": 418,
    "The Catacombs Cleared": 501,
    "Twilight Falls Cleared": 502,
    "Valley of Avalar Cleared": 503,
    "Dragon City Cleared": 504,
    "Attack of the Golem Cleared": 505,
    "Ruins of Warfang Cleared": 506,
    "The Dam Cleared": 507,
    "The Destroyer Cleared": 508,
    "Burned Lands Cleared": 509,
    "Floating Islands Cleared": 510,
    # "Spyro Gallery Unlock": 601,
    # "Cynder Gallery Unlock": 602,
    "Alliance Gallery Unlock": 603,
    "Scenery Gallery Unlock": 604,
    "Objective Complete - Reach the Enchanted Forest": 701,
    "Objective Complete - Save the Cheetah Village": 702,
    "Objective Complete - Find Meadow": 703,
    "Objective Complete - Find the Hermit": 704,
    "Objective Complete - Find the Supply Cave": 705,
    "Objective Complete - Find the Raft": 706,
    "Objective Complete - Bring the Raft to Meadow": 707,
    "Objective Complete - Extinguish the Fire": 708,
    "Objective Complete - Fill the Pool with Water": 709,
    "Objective Complete - Find a Bucket": 710,
    "Objective Complete - Protect the Catapult": 711,
    "Objective Complete - Destroy the Siege Tower (first)": 712,
    "Objective Complete - Escort the Artillery Mole to the Catapult": 713,
    "Objective Complete - Destroy the Siege Tower (second)": 714,
    "Objective Complete - Destroy the last two Siege Towers": 715,
    "Objective Complete - Close the City Gates": 716,
    "Objective Complete - Open the Gates to the Ruins of Warfang": 717,
    "Objective Complete - Open the Floodgates to the Dam": 718,
    "Objective Complete - Open the Main Floodgate": 719,
    "Objective Complete - Destroy all the crystals of the Destroyer": 720,
    "Objective Complete - Reach the Volcano": 721,
    "Objective Complete - Torches Lit 8/8": 722
}

# If the flag at one of these addresses == 1, then the item at the location has been collected
# Unless it is an objective, in which case we need to look for a value of 2 (Complete, since 1 is Active and shows in the Objectives Menu)
# Note that it is not required to have the objective set to Active first for the game to set it to Complete. It can very well
# go from 0 to 2 directly. In fact, the Close the City Gates objective is kinda buggy and only set to Active if you don't have the armor
# chest collected and don't skip the troll dying cutscene, but it is always set to Complete when you close the doors regardless
LOCATION_FLAG_ADDRESS_TO_NAME = {
    # 0x9fecdf: "Spyro Gallery Unlock",
    # 0x9fece0: "Cynder Gallery Unlock",
    0x9fece1: "Alliance Gallery Unlock",
    0x9fece3: "Scenery Gallery Unlock",
    0xa3edc4: "Catacombs Blue Gem - Weight Room",
    0xa3ee0c: "Catacombs Blue Gem - Waterfall Room Under Right Breakable Stone",
    0xa3ee30: "Catacombs Blue Gem - Waterfall Room Under Left Breakable Stone",
    0xa3ee54: "Catacombs Blue Gem - Waterfall Room Pillars 2",
    0xa3ee78: "Catacombs Blue Gem - Waterfall Room Top Left",
    0xa3ee9c: "Catacombs Blue Gem - Waterfall Room Pillars 1",
    0xa3eec0: "Catacombs Blue Gem - Waterfall Room Right",
    0xa3eee4: "Catacombs Blue Gem - Waterfall Room Near Breakable Stones",
    0xa3ef2c: "Catacombs Blue Gem - Waterfall Room Save Point",
    0xa3ef50: "Catacombs Blue Gem - Before Wind Horn",
    0xa3eb84: "TF Blue Gem - Hero Grublin",
    0xa3ebcc: "TF Blue Gem - Behind Vines",
    0xa3ec5c: "TF Blue Gem - Bottom of Waterfall",
    0xa3ec80: "TF Blue Gem - Near Save Point",
    0xa3eca4: "TF Blue Gem - Before Wind Tunnel",
    0xa3ecc8: "TF Blue Gem - In Waterfall",
    0xa3ecec: "TF Blue Gem - End of Level",
    0xa3dc9c: "VoA Blue Gem - Near Passageway Right",
    0xa3dce4: "VoA Blue Gem - Near Elite",
    0xa3dd50: "VoA Blue Gem - Island",
    0xa3de4c: "VoA Blue Gem - Hidden Area",
    0xa3de70: "VoA Blue Gem - Above Passageway",
    0xa3dedc: "VoA Blue Gem - Near Hermit",
    0xa3df00: "VoA Blue Gem - Hermit Area Tunnels",
    0xa3df24: "VoA Blue Gem - Near Meadow Cave",
    0xa3df48: "VoA Blue Gem - Above Meadow Cave",
    0xa3df6c: "VoA Blue Gem - Cheetah Village",
    0xa3dfb4: "VoA Blue Gem - Between Passageway and Hidden Area",
    0xa3dfd8: "VoA Blue Gem - On Top of Platform Near Island",
    0xa3dffc: "VoA Blue Gem - Right of Big Waterfall",
    0xa3e020: "VoA Blue Gem - Near Raft",
    0xa3e08c: "VoA Blue Gem - Behind Supply Cave",
    0xa3e284: "VoA Blue Gem - Near Cheetah Village",
    0xa3eb60: "VoA Blue Gem - Under Platform Near Island",
    0xa3ed34: "VoA Blue Gem - Left of Big Waterfall",
    0xa3ed58: "VoA Blue Gem - Near Supply Cave",
    0xa3e62c: "DC Blue Gem - First Save Point",
    0xa3e698: "DC Blue Gem - Behind Catapult",
    0xa3e6bc: "DC Blue Gem - Near Armor Chest",
    0xa3e74c: "DC Blue Gem - Behind Shadow Gate Near Doors",
    0xa3e770: "DC Blue Gem - Above Fire",
    0xa3e794: "DC Blue Gem - Near Torches Gate",
    0xa3e7b8: "DC Blue Gem - Beginning of Remparts",
    0xa3e7dc: "DC Blue Gem - Broken Stairs Top",
    0xa3e800: "DC Blue Gem - Broken Stairs Bottom",
    0xa3e890: "RoW Blue Gem - Left Path Platform Under Trap",
    0xa3e8b4: "RoW Blue Gem - Right Path Between Malefor Mural and Lever",
    0xa3e98c: "RoW Blue Gem - Bridge Left",
    0xa3e9b0: "RoW Blue Gem - Bridge Right",
    0xa3e9d4: "RoW Blue Gem - Up Right Path Near Key",
    0xa3e9f8: "RoW Blue Gem - Left Path Long Platform",
    0xa3ea1c: "RoW Blue Gem - Left Path Round Platform",
    0xa3ea40: "RoW Blue Gem - Left Path Near Wallrun",
    0xa3ea64: "RoW Blue Gem - Left Path Near Trap",
    0xa3ea88: "RoW Blue Gem - Right Path Near Malefor Mural",
    0xa3eaac: "RoW Blue Gem - Right Path Near Tuning Forks",
    0xa3ead0: "RoW Blue Gem - Right Path Near Lever",
    0xa3eaf4: "RoW Blue Gem - Left Path Small Pillar",
    0xa3e3a4: "Dam Blue Gem - Near Save Point Left",
    0xa3e3c8: "Dam Blue Gem - Near Save Point Right",
    0xa3e4c4: "Dam Blue Gem - Middle",
    0xa3e4e8: "Dam Blue Gem - Near Earth Wall",
    0xa3e50c: "Dam Blue Gem - Top",
    0xa3e188: "Destroyer Blue Gem - Right Wrist Left",
    0xa3e1ac: "Destroyer Blue Gem - Right Wrist Right",
    0xa3e2a8: "Destroyer Blue Gem - Right Shoulder Left",
    0xa3e2cc: "Destroyer Blue Gem - Right Shoulder Right",
    0xa3e314: "Destroyer Blue Gem - Left Arm",
    0xa3e338: "Destroyer Blue Gem - Hip Near Enemies",
    0xa3e35c: "Destroyer Blue Gem - Hip Near Dark Crystal",
    0xa3e380: "Destroyer Blue Gem - Under Right Armpit",
    0xa3e140: "BL Blue Gem - Bridge Before Last Ring Right",
    0xa3ed7c: "BL Blue Gem - Last Ring Area Far Right",
    0xa3ef74: "BL Blue Gem - Last Ring Area Far Left",
    0xa3ef98: "BL Blue Gem - After Last Ring Left",
    0xa3efbc: "BL Blue Gem - Bridge Before Last Ring Left",
    0xa3efe0: "BL Blue Gem - After Last Ring Right",
    0xa3f004: "BL Blue Gem - Before Third Ring Middle",
    0xa3f028: "BL Blue Gem - After Third Ring",
    0xa3f04c: "BL Blue Gem - Before Third Ring Left",
    0xa3f094: "BL Blue Gem - Before Third Ring Right",
    0xa3d9cc: "FI Blue Gem - Big Bonus Island Ground",
    0xa3d9f0: "FI Blue Gem - Lower Save Point Island Near Torch",
    0xa3da14: "FI Blue Gem - Big Bonus Island Middle",
    0xa3da5c: "FI Blue Gem - Big Bonus Island Left",
    0xa3daa4: "FI Blue Gem - Big Bonus Island Top",
    0xa3dac8: "FI Blue Gem - Big Bonus Island Right",
    0xa3db10: "FI Blue Gem - Small Island Behind Wyvern Elite",
    0xa3db34: "FI Blue Gem - Troll Island Top",
    0xa3db58: "FI Blue Gem - Above Doors",
    0xa3dba0: "FI Blue Gem - Wyvern Elite Island",
    0xa3dbc4: "FI Blue Gem - Lower Save Point Island",
    0xa3dbe8: "FI Blue Gem - Torch Island Near Mana Gem",
    0xa3dc0c: "FI Blue Gem - Small Island Near Torch",
    0xa3dc30: "FI Blue Gem - Big Island Near Doors",
    0xa3dcc0: "FI Blue Gem - Hero Grublin Elite Island Middle",
    0xa3df90: "FI Blue Gem - Hero Grublins",
    0xa3e0d4: "FI Blue Gem - Hero Grublin Elite Island Top",
    0xa3e0f8: "FI Blue Gem - Troll Island Left",
    0xa3eda0: "Catacombs Health Gem",
    0xa3ec38: "TF Health Gem",
    0xa3dd08: "VoA Health Gem - Big Oak",
    0xa3dd2c: "VoA Health Gem - Near Elite",
    0xa3dd74: "VoA Health Gem - Hermit Area Tunnels",
    0xa3e5e4: "DC Health Gem - Behind Bottom Shadow Gate Near Fire",
    0xa3e608: "DC Health Gem - Torches",
    0xa3e6e0: "DC Health Gem - Remparts Left",
    0xa3e59c: "AotG Health Gem",
    0xa3e8d8: "RoW Health Gem - Right Path Behind Vines",
    0xa3e944: "RoW Health Gem - Left Path Trap",
    0xa3e968: "RoW Health Gem - Up Right Path Near Key",
    0xa3e3ec: "Dam Health Gem - Behind Shadow Gate After Hero Orc",
    0xa3e458: "Dam Health Gem - Behind Left Shadow Gate",
    0xa3e11c: "Destroyer Health Gem - Right Arm",
    0xa3e1d0: "Destroyer Health Gem - Left Arm",
    0xa3e068: "BL Health Gem - Before Third Ring",
    0xa3e260: "BL Health Gem - Elite",
    0xa3da38: "FI Health Gem - Big Bonus Island",
    0xa3da80: "FI Health Gem - Hero Grublin Elite Island",
    0xa3ede8: "Catacombs Mana Gem",
    0xa3ebf0: "TF Mana Gem - Near Crystals",
    0xa3ec14: "TF Mana Gem - Before Wind Tunnel",
    0xa3de04: "VoA Mana Gem - Behind Gate",
    0xa3de94: "VoA Mana Gem - Near Hermit",
    0xa3deb8: "VoA Mana Gem - Island",
    0xa3e5c0: "DC Mana Gem - Near Pool Wheel",
    0xa3e704: "DC Mana Gem - Remparts Right",
    0xa3e578: "AotG Mana Gem",
    0xa3e86c: "RoW Mana Gem - Up Right Path After Falling Stones",
    0xa3e8fc: "RoW Mana Gem - Left Path Behind Vines",
    0xa3e920: "RoW Mana Gem - Up Left Path Behind Shadow Gate",
    0xa3e410: "Dam Mana Gem - Wooden Platform",
    0xa3e434: "Dam Mana Gem - Behind Earth Wall",
    0xa3e164: "Destroyer Mana Gem - Right Arm",
    0xa3e2f0: "Destroyer Mana Gem - Mouth",
    0xa3e044: "BL Mana Gem - Under Bridge",
    0xa3eba8: "BL Mana Gem - Hero Orc",
    0xa3f0dc: "BL Mana Gem - Under Last Ring Area",
    0xa3daec: "FI Mana Gem",
    0xa3ef08: "Catacombs Elite",
    0xa3ed10: "TF Elite",
    0xa3e0b0: "VoA Elite",
    0xa3eb18: "RoW Elite",
    0xa3e530: "Dam Elite",
    0xa3e23c: "BL Elite",
    0xa3db7c: "FI Elite - Wyvern",
    0xa3dc54: "FI Elite - Hero Grublin",
    0xa3dc78: "TF Armor Chest - Behind Vines",
    0xa3eb3c: "TF Armor Chest - Near Elite",
    0xa3dd98: "VoA Armor Chest - Above Meadow Cave",
    0xa3ddbc: "VoA Armor Chest - Meadow",
    0xa3dde0: "VoA Armor Chest - Big Waterfall",
    0xa3de28: "VoA Armor Chest - Hermit",
    0xa3e650: "DC Armor Chest - Behind Top Shadow Gate Near Fire",
    0xa3e674: "DC Armor Chest - Near Second Save Point",
    0xa3e728: "DC Armor Chest - Troll",
    0xa3e554: "AotG Armor Chest",
    0xa3e824: "RoW Armor Chest - Up Right Path Under Earth Slab",
    0xa3e848: "RoW Armor Chest - Left Path Near Key",
    0xa3e47c: "Dam Armor Chest - Right Pillar",
    0xa3e4a0: "Dam Armor Chest - Hero Orc",
    0xa3e1f4: "Destroyer Armor Chest - Right Arm",
    0xa3e218: "Destroyer Armor Chest - Torso",
    0xa3f070: "BL Armor Chest - Orcs",
    0xa3f0b8: "BL Armor Chest - Behind Dark Crystal",
    0x9fecd3: "The Catacombs Cleared",
    0x9fecd4: "Twilight Falls Cleared",
    0x9fecd5: "Valley of Avalar Cleared",
    0x9fecd6: "Dragon City Cleared",
    0x9fecd7: "Attack of the Golem Cleared",
    0x9fecd8: "Ruins of Warfang Cleared",
    0x9fecda: "The Dam Cleared",
    0x9fecdb: "The Destroyer Cleared",
    0x9fecdc: "Burned Lands Cleared",
    0x9fecdd: "Floating Islands Cleared",
    0xa618d0: "Objective Complete - Reach the Enchanted Forest",
    0xa76400: "Objective Complete - Save the Cheetah Village",
    0xa76402: "Objective Complete - Find Meadow",
    0xa76403: "Objective Complete - Find the Hermit",
    0xa76404: "Objective Complete - Find the Supply Cave",
    0xa76406: "Objective Complete - Find the Raft",
    0xa76407: "Objective Complete - Bring the Raft to Meadow",
    0xa76420: "Objective Complete - Extinguish the Fire",
    0xa76421: "Objective Complete - Fill the Pool with Water",
    0xa76422: "Objective Complete - Find a Bucket",
    0xa76423: "Objective Complete - Protect the Catapult",
    0xa76424: "Objective Complete - Destroy the Siege Tower (first)",
    0xa76425: "Objective Complete - Escort the Artillery Mole to the Catapult",
    0xa76426: "Objective Complete - Destroy the Siege Tower (second)",
    0xa76427: "Objective Complete - Destroy the last two Siege Towers",
    0xa76428: "Objective Complete - Close the City Gates",
    0xa734d0: "Objective Complete - Open the Gates to the Ruins of Warfang",
    0xa77ab1: "Objective Complete - Open the Floodgates to the Dam",
    0xa77ab3: "Objective Complete - Open the Main Floodgate",
    0xa77ad0: "Objective Complete - Destroy all the crystals of the Destroyer",
    0xa77af1: "Objective Complete - Reach the Volcano",
    0xa77b12: "Objective Complete - Torches Lit 8/8"
}

# Each Location instance must correctly report the "game" it belongs to.
# To make this simple, it is common practice to subclass the basic Location class and override the "game" field.
class DotDLocation(Location):
    game = "The Legend of Spyro: Dawn of the Dragon"

# Let's make one more helper method before we begin actually creating locations.
# Later on in the code, we'll want specific subsections of LOCATION_NAME_TO_ID.
# To reduce the chance of copy-paste errors writing something like {"Chest": LOCATION_NAME_TO_ID["Chest"]},
# let's make a helper method that takes a list of location names and returns them as a dict with their IDs.
# Note: There is a minor typing quirk here. Soem functions want location addresses to be an "int | None",
# so, while our function here only ever returns dict[str, int], we annotate it as dict[str, int | None].
def get_location_names_with_ids(location_names: list[str]) -> dict[str, int | None]:
    return {location_name: LOCATION_NAME_TO_ID[location_name] for location_name in location_names}

def create_all_locations(world: DotDWorld) -> None:
    create_regular_locations(world)
    create_events(world)

def create_regular_locations(world: DotDWorld) -> None:
    # Finally, we need to put the Locations ("checks") into their regions.
    # Once again, before we do anything, we can grab our regions we created by using world.get_region()
    gallery = world.get_region("Gallery")
    catacombs = world.get_region("Catacombs")
    twilight_falls = world.get_region("Twilight Falls")
    valley_of_avalar = world.get_region("Valley of Avalar")
    dragon_city = world.get_region("Dragon City")
    attack_of_the_golem = world.get_region("Attack of the Golem")
    ruins_of_warfang = world.get_region("Ruins of Warfang")
    the_dam = world.get_region("The Dam")
    the_destroyer = world.get_region("The Destroyer")
    burned_lands = world.get_region("Burned Lands")
    floating_islands = world.get_region("Floating Islands")
    malefors_lair = world.get_region("Malefor's Lair")

    # We can add locations to region by simply using the region.add_locations_helper.
    # For this, you need to have a dict of location names to their IDs (i.e. a subset of location_name_to_id)
    # Aha! So that's why we made that "get_location_names_with_ids" helper method earlier.
    # You also ened to pass your overridden Location class.
    gallery_locations = get_location_names_with_ids(
        [
            # "Spyro Gallery Unlock",
            # "Cynder Gallery Unlock",
            "Alliance Gallery Unlock",
            "Scenery Gallery Unlock"
        ]
    )

    # Top-level locations should only contain locations that do not
    # require any additional logic to access beyond having access to the chapter itself
    catacombs_locations = get_location_names_with_ids(
        [
            # Every location in Catacombs is blocked by at least the first set of vines
        ]
    )

    twilight_falls_locations = get_location_names_with_ids(
        [
            "TF Blue Gem - In Waterfall",
            "TF Blue Gem - Bottom of Waterfall",
            "TF Blue Gem - Near Save Point",
            "TF Blue Gem - Before Wind Tunnel",
            "TF Blue Gem - Hero Grublin",
            "TF Mana Gem - Near Crystals",
            "TF Mana Gem - Before Wind Tunnel",
            "TF Armor Chest - Near Elite",
            "TF Elite",
            "Objective Complete - Reach the Enchanted Forest",
            # "TF Blue Gem - Behind Vines" and "TF Armor Chest - Behind Vines"
            # now live in TF Beyond Vines.
            # "TF Health Gem", "TF Blue Gem - End of Level", and
            # "Twilight Falls Cleared" now live in TF End of Level.
        ]
    )

    valley_of_avalar_locations = get_location_names_with_ids(
        [
            "VoA Blue Gem - Cheetah Village",
            "VoA Blue Gem - Near Meadow Cave",
            "VoA Blue Gem - Above Meadow Cave",
            "VoA Blue Gem - Near Cheetah Village",
            "VoA Blue Gem - Near Elite",
            "VoA Blue Gem - Under Platform Near Island",
            "VoA Blue Gem - On Top of Platform Near Island",
            "VoA Blue Gem - Island",
            "VoA Blue Gem - Right of Big Waterfall",
            "VoA Blue Gem - Left of Big Waterfall",
            "VoA Blue Gem - Near Supply Cave",
            "VoA Blue Gem - Behind Supply Cave",
            "VoA Blue Gem - Near Raft",
            "VoA Blue Gem - Above Passageway",
            "VoA Blue Gem - Near Passageway Right",
            "VoA Blue Gem - Between Passageway and Hidden Area",
            "VoA Blue Gem - Hidden Area",
            "VoA Blue Gem - Hermit Area Tunnels",
            "VoA Blue Gem - Near Hermit",
            "VoA Health Gem - Big Oak",
            "VoA Health Gem - Near Elite",
            "VoA Health Gem - Hermit Area Tunnels",
            "VoA Mana Gem - Island",
            "VoA Mana Gem - Near Hermit",
            "VoA Mana Gem - Behind Gate",
            "VoA Armor Chest - Above Meadow Cave",
            "VoA Armor Chest - Meadow",
            "VoA Armor Chest - Big Waterfall",
            "VoA Armor Chest - Hermit",
            "VoA Elite",
            "Objective Complete - Save the Cheetah Village",
            "Objective Complete - Find Meadow",
            "Objective Complete - Find the Hermit",
            "Objective Complete - Find the Supply Cave",
            "Objective Complete - Find the Raft",
            "Objective Complete - Bring the Raft to Meadow",
            "Valley of Avalar Cleared"
        ]
    )

    dragon_city_locations = get_location_names_with_ids(
        [
            "DC Blue Gem - Above Fire",
            "DC Blue Gem - Near Torches Gate",
            "DC Blue Gem - First Save Point",
            "DC Blue Gem - Beginning of Remparts",
            "DC Blue Gem - Behind Catapult",
            "DC Blue Gem - Broken Stairs Top",
            "DC Blue Gem - Broken Stairs Bottom",
            "DC Blue Gem - Near Armor Chest",
            "DC Blue Gem - Behind Shadow Gate Near Doors",
            "DC Health Gem - Behind Bottom Shadow Gate Near Fire",
            "DC Health Gem - Torches",
            "DC Health Gem - Remparts Left",
            "DC Mana Gem - Near Pool Wheel",
            "DC Mana Gem - Remparts Right",
            "DC Armor Chest - Behind Top Shadow Gate Near Fire",
            "DC Armor Chest - Near Second Save Point",
            "DC Armor Chest - Troll",
            "Objective Complete - Extinguish the Fire",
            "Objective Complete - Fill the Pool with Water",
            "Objective Complete - Find a Bucket",
            "Objective Complete - Protect the Catapult",
            "Objective Complete - Destroy the Siege Tower (first)",
            "Objective Complete - Escort the Artillery Mole to the Catapult",
            "Objective Complete - Destroy the Siege Tower (second)",
            "Objective Complete - Destroy the last two Siege Towers",
            "Objective Complete - Close the City Gates",
            "Dragon City Cleared"
        ]
    )

    attack_of_the_golem_locations = get_location_names_with_ids(
        [
            "AotG Health Gem",
            "AotG Mana Gem",
            "AotG Armor Chest",
            "Attack of the Golem Cleared"
        ]
    )

    ruins_of_warfang_locations = get_location_names_with_ids(
        [
            "RoW Blue Gem - Bridge Left",
            "RoW Blue Gem - Bridge Right",
            "RoW Blue Gem - Right Path Near Malefor Mural",
            "RoW Blue Gem - Right Path Between Malefor Mural and Lever",
            "RoW Blue Gem - Right Path Near Lever",
            "RoW Blue Gem - Right Path Near Tuning Forks",
            "RoW Blue Gem - Up Right Path Near Key",
            "RoW Blue Gem - Left Path Small Pillar",
            "RoW Blue Gem - Left Path Long Platform",
            "RoW Blue Gem - Left Path Round Platform",
            "RoW Blue Gem - Left Path Near Wallrun",
            "RoW Blue Gem - Left Path Near Trap",
            "RoW Blue Gem - Left Path Platform Under Trap",
            "RoW Health Gem - Right Path Behind Vines",
            "RoW Health Gem - Up Right Path Near Key",
            "RoW Health Gem - Left Path Trap",
            "RoW Mana Gem - Up Right Path After Falling Stones",
            "RoW Mana Gem - Left Path Behind Vines",
            "RoW Mana Gem - Up Left Path Behind Shadow Gate",
            "RoW Armor Chest - Up Right Path Under Earth Slab",
            "RoW Armor Chest - Left Path Near Key",
            "RoW Elite",
            "Objective Complete - Open the Gates to the Ruins of Warfang",
            "Ruins of Warfang Cleared"
        ]
    )

    the_dam_locations = get_location_names_with_ids(
        [
            "Dam Blue Gem - Middle",
            "Dam Blue Gem - Near Save Point Left",
            "Dam Blue Gem - Near Save Point Right",
            "Dam Blue Gem - Near Earth Wall",
            "Dam Blue Gem - Top",
            "Dam Health Gem - Behind Left Shadow Gate",
            "Dam Health Gem - Behind Shadow Gate After Hero Orc",
            "Dam Mana Gem - Wooden Platform",
            "Dam Mana Gem - Behind Earth Wall",
            "Dam Armor Chest - Right Pillar",
            "Dam Armor Chest - Hero Orc",
            "Dam Elite",
            "Objective Complete - Open the Floodgates to the Dam",
            "Objective Complete - Open the Main Floodgate",
            "The Dam Cleared"
        ]
    )

    the_destroyer_locations = get_location_names_with_ids(
        [
            "Destroyer Blue Gem - Left Arm",
            "Destroyer Blue Gem - Hip Near Enemies",
            "Destroyer Blue Gem - Hip Near Dark Crystal",
            "Destroyer Blue Gem - Right Wrist Left",
            "Destroyer Blue Gem - Right Wrist Right",
            "Destroyer Blue Gem - Under Right Armpit",
            "Destroyer Blue Gem - Right Shoulder Left",
            "Destroyer Blue Gem - Right Shoulder Right",
            "Destroyer Health Gem - Left Arm",
            "Destroyer Health Gem - Right Arm",
            "Destroyer Mana Gem - Right Arm",
            "Destroyer Mana Gem - Mouth",
            "Destroyer Armor Chest - Torso",
            "Destroyer Armor Chest - Right Arm",
            "Objective Complete - Destroy all the crystals of the Destroyer",
            "The Destroyer Cleared"
        ]
    )

    burned_lands_locations = get_location_names_with_ids(
        [
            "BL Blue Gem - Before Third Ring Left",
            "BL Blue Gem - Before Third Ring Middle",
            "BL Blue Gem - Before Third Ring Right",
            "BL Blue Gem - After Third Ring",
            "BL Blue Gem - Bridge Before Last Ring Right",
            "BL Blue Gem - Bridge Before Last Ring Left",
            "BL Blue Gem - Last Ring Area Far Left",
            "BL Blue Gem - Last Ring Area Far Right",
            "BL Blue Gem - After Last Ring Left",
            "BL Blue Gem - After Last Ring Right",
            "BL Health Gem - Before Third Ring",
            "BL Health Gem - Elite",
            "BL Mana Gem - Hero Orc",
            "BL Mana Gem - Under Last Ring Area",
            "BL Mana Gem - Under Bridge",
            "BL Armor Chest - Orcs",
            "BL Armor Chest - Behind Dark Crystal",
            "BL Elite",
            "Objective Complete - Reach the Volcano",
            "Burned Lands Cleared"
        ]
    )

    floating_islands_locations = get_location_names_with_ids(
        [
            "FI Blue Gem - Hero Grublins",
            "FI Blue Gem - Above Doors",
            "FI Blue Gem - Big Island Near Doors",
            "FI Blue Gem - Small Island Near Torch",
            "FI Blue Gem - Big Bonus Island Middle",
            "FI Blue Gem - Big Bonus Island Left",
            "FI Blue Gem - Big Bonus Island Right",
            "FI Blue Gem - Big Bonus Island Top",
            "FI Blue Gem - Big Bonus Island Ground",
            "FI Blue Gem - Torch Island Near Mana Gem",
            "FI Blue Gem - Lower Save Point Island Near Torch",
            "FI Blue Gem - Lower Save Point Island",
            "FI Blue Gem - Wyvern Elite Island",
            "FI Blue Gem - Small Island Behind Wyvern Elite",
            "FI Blue Gem - Troll Island Left",
            "FI Blue Gem - Troll Island Top",
            "FI Blue Gem - Hero Grublin Elite Island Top",
            "FI Blue Gem - Hero Grublin Elite Island Middle",
            "FI Health Gem - Big Bonus Island",
            "FI Health Gem - Hero Grublin Elite Island",
            "FI Mana Gem",
            "FI Elite - Wyvern",
            "FI Elite - Hero Grublin",
            "Objective Complete - Torches Lit 8/8",
            "Floating Islands Cleared"
        ]
    )

    gallery.add_locations(gallery_locations, DotDLocation)
    catacombs.add_locations(catacombs_locations, DotDLocation)
    twilight_falls.add_locations(twilight_falls_locations, DotDLocation)
    valley_of_avalar.add_locations(valley_of_avalar_locations, DotDLocation)
    dragon_city.add_locations(dragon_city_locations, DotDLocation)
    attack_of_the_golem.add_locations(attack_of_the_golem_locations, DotDLocation)
    ruins_of_warfang.add_locations(ruins_of_warfang_locations, DotDLocation)
    the_dam.add_locations(the_dam_locations, DotDLocation)
    the_destroyer.add_locations(the_destroyer_locations, DotDLocation)
    burned_lands.add_locations(burned_lands_locations, DotDLocation)
    floating_islands.add_locations(floating_islands_locations, DotDLocation)

    # Place sub-region locations using the dicts from regions.py
    place_subregion_locations(world, CATACOMBS_SUBREGION_LOCATIONS)
    place_subregion_locations(world, TWILIGHT_FALLS_SUBREGION_LOCATIONS)


def create_events(world: DotDWorld) -> None:
    from worlds.generic.Rules import set_rule
    malefors_lair = world.get_region("Malefor's Lair")
    
    victory_location = DotDLocation(world.player, "Defeat Malefor", None, malefors_lair)
    victory_location.place_locked_item(
        DotDItem("Victory", ItemClassification.progression, None, world.player)
    )

    player = world.player
    fury_option = world.options.learn_fury.current_key

    if fury_option == "both_together":
        set_rule(victory_location,
            lambda state: state.has("Dragon's Fury", player))
    elif fury_option == "both_separate":
        # Either dragon alone can build an entire fury bar, so either fury item is sufficient
        set_rule(victory_location,
            lambda state: state.has("Spyro's Fury", player) and state.has("Cynder's Fury", player))
    elif fury_option == "spyro":
        set_rule(victory_location,
            lambda state: state.has("Spyro's Fury", player))
    elif fury_option == "cynder":
        set_rule(victory_location,
            lambda state: state.has("Cynder's Fury", player))
    # else: no rule required. Both dragons can automatically build fury
    malefors_lair.locations.append(victory_location)


def place_subregion_locations(world: DotDWorld, subregion_map: dict[str, list[str]]) -> None:
    for region_name, location_names in subregion_map.items():
        region = world.get_region(region_name)
        region.add_locations(get_location_names_with_ids(location_names), DotDLocation)