from __future__ import annotations

import asyncio
import time
import random
from typing import Any, Dict, Set, Optional

from enum import Enum

from worlds.AutoWorld import World
from NetUtils import ClientStatus
from CommonClient import CommonContext, ClientCommandProcessor, server_loop, gui_enabled


from .items import DotDItem, ITEM_NAME_TO_ID
from .elite_elements import DEFAULT_ELITE_ELEMENTS
from .options import DotDOptions
from .world import DotDWorld
from .locations import LOCATION_FLAG_ADDRESS_TO_NAME, LOCATION_NAME_TO_ID
from .pcsx2_interface.pine import Pine, struct
# from .interface import install_element_rando_hook

import logging
logging.getLogger("websockets").setLevel(logging.WARNING)

# Useful addresses
ADDR_SPYRO_CURRENT_HP = 0x9FEAE0
ADDR_SPYRO_BASE_HP = 0x9FEAE4
ADDR_CYNDER_CURRENT_HP = 0x9FEAE8
ADDR_CYNDER_BASE_HP = 0x9FEAEC
ADDR_SPYRO_CURRENT_MANA = 0x9FEAF8
ADDR_SPYRO_BASE_MANA = 0x9FEAFC
ADDR_CYNDER_CURRENT_MANA = 0x9FEB00
ADDR_CYNDER_BASE_MANA = 0x9FEB04
ADDR_SPYRO_CURRENT_FURY = 0x9FEB08
ADDR_CYNDER_CURRENT_FURY = 0x9FEB0C
ADDR_HEALTH_GEMS_COLLECTED = 0x9FEB6C
ADDR_MANA_GEMS_COLLECTED = 0x9FEB7C
ADDR_BONUS_HP_PER_UPGRADE = 0x9FEADC
ADDR_BONUS_MANA_PER_UPGRADE = 0x9FEAF4
ADDR_CURRENT_LEVEL = 0x9FE274
ADDR_NEXT_LEVEL = 0x9FE278
ADDR_PAUSE_FLAG = 0x7B7670
ADDR_CKS08GAMESTRUCTURE = 0x9FEA90
ADDR_CURRENT_LEVEL = 0x9FE274
ADDR_NEXT_LEVEL = 0x9FE278
ADDR_MENU_VALUE = 0x9FE308

# EXP Buckets
ADDR_SPYRO_UNSPENT_EXP = 0x9FEB18
ADDR_SPYRO_FIRE_EXP = 0x9FEB20
ADDR_SPYRO_ICE_EXP = 0x9FEB24
ADDR_SPYRO_EARTH_EXP = 0x9FEB28
ADDR_SPYRO_ELEC_EXP = 0x9FEB2C
ADDR_CYNDER_UNSPENT_EXP = 0x9FEB1C
ADDR_CYNDER_POISON_EXP = 0x9FEB34
ADDR_CYNDER_SHADOW_EXP = 0x9FEB38
ADDR_CYNDER_FEAR_EXP = 0x9FEB3C
ADDR_CYNDER_WIND_EXP = 0x9FEB40

# We'll use an unused 4-bytes in the Player_Current CKS08Player object (same place where Total Game Time is stored)
# to count how many blue gems the player has actually received ; it will be saved to the save file and loaded as normal.
# This will be used as protection against XP dupe on reconnect and XP loss if the player connects before selecting New game or Load game
ADDR_AP_BLUE_GEMS_COUNTER = 0x9FEA1C

# Game completion flag address: is set to 1 when Malefor is defeated
ADDR_FINAL_BOSS_DEFEATED = 0x9FECDE

# Armor addresses
ADDR_SPYRO_HELMET_SILVER = 0xA3E674
ADDR_SPYRO_HELMET_GOLD = 0xA3DDE0
ADDR_SPYRO_HELMET_FURY = 0xA3F070
ADDR_SPYRO_BRACERS_SILVER = 0xA3E1F4
ADDR_SPYRO_BRACERS_GOLD = 0xA3E824
ADDR_SPYRO_BRACERS_FURY = 0xA3DE28
ADDR_SPYRO_TAIL_SILVER = 0xA3DC78
ADDR_SPYRO_TAIL_GOLD = 0xA3E47C
ADDR_SPYRO_TAIL_FURY = 0xA3E218
ADDR_CYNDER_HELMET_SILVER = 0xA3E554
ADDR_CYNDER_HELMET_GOLD = 0xA3E848
ADDR_CYNDER_HELMET_FURY = 0xA3E728
ADDR_CYNDER_BRACERS_SILVER = 0xA3DD98
ADDR_CYNDER_BRACERS_GOLD = 0xA3EB3C
ADDR_CYNDER_BRACERS_FURY = 0xA3E4A0
ADDR_CYNDER_TAIL_SILVER = 0xA3E650
ADDR_CYNDER_TAIL_GOLD = 0xA3DDBC
ADDR_CYNDER_TAIL_FURY = 0xA3F0B8

# Chapter addresses
ADDR_CATACOMBS_CLEAR = 0x9FECD3
ADDR_FALLS_CLEAR = 0x9FECD4
ADDR_VALLEY_CLEAR = 0x9FECD5
ADDR_CITY_CLEAR = 0x9FECD6
ADDR_GOLEM_CLEAR = 0x9FECD7
ADDR_RUINS_CLEAR = 0x9FECD8
ADDR_DAM_CLEAR = 0x9FECDA
ADDR_DESTROYER_CLEAR = 0x9FECDB
ADDR_BURNED_CLEAR = 0x9FECDC
ADDR_ISLANDS_CLEAR = 0x9FECDD
ADDR_MALEFOR_CLEAR = 0x9FECDE

# Base pointer addresses
ADDR_PTR_CKGRPS08ENEMY = 0x9FDFC4
ADDR_PTR_CKGRPS08HERO = 0x9FDFC8

# Pointer to class values
# Every object of a given class has the same pointer value at offset 0x0
# Note that the class names can't be seen on PS2, but they can on Wii by following the pointer chain at offset 0x0
CLASS_PTR_CKS08GAMESTRUCTURE = 0x00788330
CLASS_PTR_CKHKS08HERO = 0x00786B60
CLASS_PTR_CKS08ENEMYELEMENTPOOL = 0x00785760
CLASS_PTR_CNODE = 0x00778AC0

# Element Rando scratch addresses
ADDR_FIRE_UNLOCKED = 0x00A6C6A0
ADDR_ICE_UNLOCKED = 0x00A6C6A1
ADDR_EARTH_UNLOCKED = 0x00A6C6A2
ADDR_ELEC_UNLOCKED = 0x00A6C6A3
ADDR_POISON_UNLOCKED = 0x00A6C6A4
ADDR_SHADOW_UNLOCKED = 0x00A6C6A5
ADDR_FEAR_UNLOCKED = 0x00A6C6A6
ADDR_WIND_UNLOCKED = 0x00A6C6A7

ALL_ELEMENTS_SET = {"Fire", "Electricity", "Ice", "Earth", "Poison", "Fear", "Wind", "Shadow"}

ELEMENT_NAME_TO_UNLOCKED_ADDRESS = {
    "Fire": ADDR_FIRE_UNLOCKED,
    "Electricity": ADDR_ELEC_UNLOCKED,
    "Ice": ADDR_ICE_UNLOCKED,
    "Earth": ADDR_EARTH_UNLOCKED,
    "Poison": ADDR_POISON_UNLOCKED,
    "Fear": ADDR_FEAR_UNLOCKED,
    "Wind": ADDR_WIND_UNLOCKED,
    "Shadow": ADDR_SHADOW_UNLOCKED
}

ITEM_NAME_TO_ELEMENT = {
    "Spyro's Fire": "Fire",
    "Spyro's Electricity": "Electricity",
    "Spyro's Ice": "Ice",
    "Spyro's Earth": "Earth",
    "Cynder's Poison": "Poison",
    "Cynder's Fear": "Fear",
    "Cynder's Wind": "Wind",
    "Cynder's Shadow": "Shadow",
}

# Pointer to class values
# Every object of a given class has the same pointer value at offset 0x0
# Note that the class names can't be seen on PS2, but they can on Wii by following the pointer chain at offset 0x0
CLASS_PTR_CKS08GAMESTRUCTURE = 0x00788330

ARMOR_NAME_TO_ADDRESS = {
    "Spyro Helmet Silver": ADDR_SPYRO_HELMET_SILVER,
    "Spyro Helmet Gold": ADDR_SPYRO_HELMET_GOLD,
    "Spyro Helmet Fury": ADDR_SPYRO_HELMET_FURY,
    "Spyro Bracers Silver": ADDR_SPYRO_BRACERS_SILVER,
    "Spyro Bracers Gold": ADDR_SPYRO_BRACERS_GOLD,
    "Spyro Bracers Fury": ADDR_SPYRO_BRACERS_FURY,
    "Spyro Tail Silver": ADDR_SPYRO_TAIL_SILVER,
    "Spyro Tail Gold": ADDR_SPYRO_TAIL_GOLD,
    "Spyro Tail Fury": ADDR_SPYRO_TAIL_FURY,
    "Cynder Helmet Silver": ADDR_CYNDER_HELMET_SILVER,
    "Cynder Helmet Gold": ADDR_CYNDER_HELMET_GOLD,
    "Cynder Helmet Fury": ADDR_CYNDER_HELMET_FURY,
    "Cynder Bracers Silver": ADDR_CYNDER_BRACERS_SILVER,
    "Cynder Bracers Gold": ADDR_CYNDER_BRACERS_GOLD,
    "Cynder Bracers Fury": ADDR_CYNDER_BRACERS_FURY,
    "Cynder Tail Silver": ADDR_CYNDER_TAIL_SILVER,
    "Cynder Tail Gold": ADDR_CYNDER_TAIL_GOLD,
    "Cynder Tail Fury": ADDR_CYNDER_TAIL_FURY
}

LEVEL_ID_TO_NAME = {
    #Matches the LVL### folders, 70 doesn't exist
    0:      "Main Menu",
    10:     "The Catacombs",
    20:     "Twilight Falls",
    30:     "Valley of Avalar",
    40:     "Dragon City",
    50:     "Attack of the Golem",
    60:     "Ruins of Warfang",
    80:     "The Dam",
    90:     "The Destroyer",
    100:    "Burned Lands",
    110:    "Floating Islands",
    120:    "Malefor's Lair"
}

ARMOR_NAME_TO_SCRATCH_ADDRESS = {
    name: addr + 0x05 for name, addr in ARMOR_NAME_TO_ADDRESS.items()
}

LEVEL_NAME_TO_ADDRESS = {
    "Catacombs":          ADDR_CATACOMBS_CLEAR,
    "Twilight Falls":     ADDR_FALLS_CLEAR,
    "Valley of Avalar":   ADDR_VALLEY_CLEAR,
    "Dragon City":        ADDR_CITY_CLEAR,
    "Attack of the Golem":ADDR_GOLEM_CLEAR,
    "Ruins of Warfang":   ADDR_RUINS_CLEAR,
    "The Dam":            ADDR_DAM_CLEAR,
    "The Destroyer":      ADDR_DESTROYER_CLEAR,
    "Burned Lands":       ADDR_BURNED_CLEAR,
    "Floating Islands":   ADDR_ISLANDS_CLEAR,
    "Malefor's Lair":     ADDR_MALEFOR_CLEAR,
}

LEVEL_NAME_TO_SCRATCH_ADDRESS = {
    name: addr + 0x11 for name, addr in LEVEL_NAME_TO_ADDRESS.items()
}

# Starting flag of the AP Catacombs chapter unlock (in vanilla this is an unused unlock)
ADDR_NEW_GAME_CATACOMBS_UNLOCK = 0x00A3CE4C

# Expected game ID for NTSC-U version of Dawn of the Dragon
# PINE's get_game_id() typically returns the disc serial, e.g. "SLUS-21820"
EXPECTED_GAME_ID = "SLUS-21820"

# Patching
ADDR_ARMOR_OWNERSHIP_CHECK_HOOK = 0x0039C2CC
ADDR_ARMOR_OWNERSHIP_CHECK_ROUTINE = 0x01FFED38

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
    "Ice": bytes([0x40, 0x7F, 0xFF]),
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

ELEMENT_NAME_TO_ID = {
    "Fire": 0,
    "Ice": 1,
    "Earth": 2,
    "Electricity": 3,
    "Poison": 4,
    "Shadow": 5,
    "Fear": 6,
    "Wind": 7,
    "Purple Fury": 8,
    "Dark Fury": 9
}

class MemoryReader:
    def __init__(self):
        # Slot 28011 is the PCSX2 default
        self.client = Pine(slot=28011)
        self._connected = False
        self._try_connect()

    def _try_connect(self) -> bool:
        """Attempt to connect (or reconnect) to PCSX2. Returns True on success."""
        try:
            self.client.connect()
            if self.client.is_connected():
                self._connected = True
                print("Connected to PCSX2 via PINE")
                return True
        except Exception as e:
            pass
        self._connected = False
        print("Could not connect to PCSX2. Is PINE enabled in Advanced Settings?")
        return False

    @property
    def is_connected(self) -> bool:
        return self._connected

    def _safe_op(self, op):
        """
        Wrap any PINE call so that a broken pipe / closed emulator is caught
        and turns the connection state to disconnected rather than crashing.
        Returns None on failure.
        """
        try:
            result = op()
            self._connected = True
            return result
        except Exception as e:
            if self._connected:
                print(f"[MemoryReader] Lost connection to PCSX2: {e}")
            self._connected = False
            return None

    def read_u32(self, ps2_address: int) -> Optional[int]:
        return self._safe_op(lambda: self.client.read_int32(ps2_address))

    def write_u32(self, ps2_address: int, value: int) -> bool:
        return self._safe_op(lambda: self.client.write_int32(ps2_address, value)) is not None

    def read_s32(self, ps2_address: int) -> Optional[int]:
        return self._safe_op(lambda: self.client.read_int32_signed(ps2_address))

    def write_s32(self, ps2_address: int, value: int) -> bool:
        return self._safe_op(lambda: self.client.write_int32_signed(ps2_address, value)) is not None

    def read_bytes(self, ps2_address: int, length: int) -> Optional[bytes]:
        return self._safe_op(lambda: self.client.read_bytes(ps2_address, length))

    def write_bytes(self, ps2_address: int, data: bytes) -> bool:
        return self._safe_op(lambda: self.client.write_bytes(ps2_address, data)) is not None

    def read_float(self, ps2_address: int) -> Optional[float]:
        data = self.read_bytes(ps2_address, 4)
        return struct.unpack("<f", data)[0] if data is not None else None

    def write_float(self, ps2_address: int, value: float) -> bool:
        return self._safe_op(lambda: self.client.write_float(ps2_address, value))

    def read_pointer(self, ps2_address: int) -> Optional[int]:
        address = self.read_u32(ps2_address)
        return address if address is not None and address > 0x00100000 and address < 0x1FFFFFFD else None

    def get_game_id(self) -> Optional[str]:
        return self._safe_op(lambda: self.client.get_game_id())


class DotDContext(CommonContext):
    game = "The Legend of Spyro: Dawn of the Dragon"

    def __init__(self, server_address, password):
        super().__init__(server_address, password)

        self.memory = MemoryReader()
        self.items_handling = 0b111

        self.chapter_order: list[str] = [
            "Catacombs", "Twilight Falls", "Valley of Avalar", "Dragon City",
            "Attack of the Golem", "Ruins of Warfang", "The Dam",
            "The Destroyer", "Burned Lands", "Floating Islands",
            "Malefor's Lair"
        ]

        self.elite_elements: dict[str, list[str]] = DEFAULT_ELITE_ELEMENTS.copy()

        self.current_level = None
        self.last_menu_value = b"\x00"

        # Pointers to useful game objects, such as hero data
        # The level watcher will update those pointers when needed
        self.addr_spyro_hero = None
        self.addr_cynder_hero = None

        # ---------------------------------------------------------------
        # Idempotency tracking (fix for !collect / reconnect double-apply)
        # ---------------------------------------------------------------
        # Track the highest item index we have already fully applied so that
        # a re-send of ReceivedItems (on reconnect or !collect) never adds
        # the same item twice.
        self._applied_item_index: int = 0
        # Cumulative totals the server *says* we should have right now.
        # Replayed on every ReceivedItems so we always converge to the
        # server's view of the world.
        self._total_blue_gems: int = 0
        self._total_health_gems: int = 0
        self._total_mana_gems: int = 0
        self._num_chapters_unlocked: int = 0

        # Item state variables
        self._session_blue_gems_at_connect: int = 0
        self._learned_fury: list[bool] = [True, True] # index 0 = Spyro, 1 = Cynder
        self._learned_wall_climbing = True
        self._learned_wall_running = True

        # Armor names received — set-based, naturally idempotent
        self._received_armor: Set[str] = set()
        # Same with learned elements
        self._learned_elements: Set[str] = ALL_ELEMENTS_SET

        # Default options values
        self.death_link_enabled = False
        self.player_dead = False
        self.learn_fury = 0
        self.shuffled_elements = set()
        self.learn_wall_climbing = False
        self.learn_wall_running = False
        self.random_elite_elements = 0

        # Prepare to fire an async task to check for when wall climbing/running can be learned
        self._wall_climbing_setter_task: Optional[asyncio.Task] = None
        self._wall_running_learner_task: Optional[asyncio.Task] = None

        # Whether game-version check has passed
        self._game_version_ok: bool = False
        # Whether final boss defeat has already been sent to the server
        self._goal_sent: bool = False

    # ------------------------------------------------------------------
    # Game version guard
    # ------------------------------------------------------------------
    def check_game_version(self) -> bool:
        """
        Read the disc serial from PCSX2 and verify it matches the expected
        NTSC-U version. Returns True if OK, False (and prints a message) if not.
        """
        game_id = self.memory.get_game_id()
        if game_id is None:
            print("[Version Check] Could not read game ID from PCSX2 — is the emulator running?")
            return False
        # PINE may return a string like "SLUS-21820 " with trailing whitespace
        game_id = game_id.strip()
        if game_id != EXPECTED_GAME_ID:
            print(
                f"[Version Check] FAILED: expected game ID '{EXPECTED_GAME_ID}' "
                f"but got '{game_id}'. "
                "Only the NTSC-U version is supported. Client will not operate."
            )
            return False
        print(f"[Version Check] OK ({game_id})")
        return True

    # ------------------------------------------------------------------
    # Archipelago hooks
    # ------------------------------------------------------------------
    async def server_auth(self, password_requested: bool = False):
        if password_requested and not self.password:
            await super(DotDContext, self).server_auth(password_requested)
        await self.get_username()
        await self.send_connect()
        print(f"Checked Locations: {self.checked_locations}")

    def on_package(self, cmd: str, args: dict):
        if cmd == "Connected":
            print("Connected to Archipelago!")

            # Get shuffled elements before resetting item state since _reset_item_state() seeds _learned_elements from it.
            self.shuffled_elements: Set = args["slot_data"].get("shuffled_elements", set())

            # -------------------------------------------------------
            # On (re)connection: reset cumulative counters and re-apply
            # ALL items from scratch so we always match the server's state.
            # -------------------------------------------------------
            # Handle item state update
            self._reset_item_state()
            self.apply_patches()

            # Handle death link
            self.death_link_enabled = bool(args["slot_data"].get("death_link", 0))
            print(f"Death Link is {self.death_link_enabled}")

            if self.death_link_enabled:
                asyncio.create_task(self.update_death_link(True))

            # Make note of chapter shuffle order for local use
            order = args["slot_data"].get("chapter_order")
            if order:
                self.chapter_order = order + ["Malefor's Lair"]
            
            # Always have the first chapter unlocked
            self.memory.write_bytes(LEVEL_NAME_TO_SCRATCH_ADDRESS[self.chapter_order[0]], b"\x01")
            # If the first chapter is Catacombs, we need to set the starting flag so the player doesn't lose the chapter when selecting New Game
            if self.chapter_order[0] == "Catacombs":
                self.memory.write_bytes(ADDR_NEW_GAME_CATACOMBS_UNLOCK, b"\x01")
            
            # Handle Learn Fury (current_key is useless. slot_data I believe stores ints instead. Which int means which option is found in options.py)
            self.learn_fury = args["slot_data"].get("learn_fury", 0)

            # Learn Fury
            # If learn_fury is disabled, fury is always unlocked
            if self.learn_fury == 0:
                self._learned_fury = [True, True]

            # Wall Climbing
            self.learn_wall_climbing = bool(args["slot_data"].get("learn_to_climb", 0))
            if not self.learn_wall_climbing:
                self._learned_wall_climbing = True

            # Wall Running
            self.learn_wall_running = bool(args["slot_data"].get("learn_to_wall_run", 0))
            if not self.learn_wall_running:
                self._learned_wall_running = True

            # Handle Shuffled Elements
            # Since elements can be already known on connection, 
            for element in self._learned_elements:
                scratch_addr = ELEMENT_NAME_TO_UNLOCKED_ADDRESS.get(element)
                if scratch_addr:
                    self.memory.write_bytes(scratch_addr, b"\x01")

            # Random Elite Elements
            self.random_elite_elements = args["slot_data"].get("random_elite_elements", 0)
            elems = args["slot_data"].get("elite_elements")
            if elems:
                self.elite_elements = elems

            # Set current level to None to reinit the level data / refetch pointers
            self.current_level = None

        elif cmd == "ReceivedItems":
            try:
                print("Receiving items...")
                # args["index"] is the server-side starting index of this batch.
                # When the server re-sends from index 0 (reconnect / !collect),
                # we reset and rebuild state from scratch to stay in sync.
                batch_start: int = args.get("index", 0)
                if batch_start == 0:
                    # Full resync from the server — rebuild from zero
                    self._reset_item_state()

                for net_item in args["items"]:
                    item_name = self.item_names.lookup_in_game(net_item.item)
                    print(f"Received {item_name} from player {net_item.player}")
                    self._accumulate_item(item_name)

                # Apply the newly-computed totals to game memory
                self._flush_item_state()

            except Exception as e:
                print(f"on_package encountered exception: {e}")


    # ------------------------------------------------------------------
    # Item state — idempotent accumulation + flush
    # ------------------------------------------------------------------
    def _reset_item_state(self):
        """
        Clear all accumulated item counts/flags so they can be rebuilt
        cleanly from a ReceivedItems replay.
        """
        self._total_blue_gems = 0
        self._total_health_gems = 0
        self._total_mana_gems = 0
        self._received_armor = set()
        self._num_chapters_unlocked = 0
        self._learned_fury = [False, False] # accumulate needs to restore the flags from false
        self._learned_wall_climbing = False

        # Handle Wall Running
        self._learned_wall_running = False
        if self._wall_running_learner_task and not self._wall_running_learner_task.done():
            self._wall_running_learner_task.cancel()
        self._wall_running_learner_task = None

        # Seed with the non-shuffled baseline so a full resync starts from
        # the correct "everything not in the shuffle pool" state
        self._learned_elements = ALL_ELEMENTS_SET.difference(self.shuffled_elements)


    def _accumulate_item(self, item_name: str):
        """
        Count / flag an item without writing to memory yet.
        All writes happen in _flush_item_state so we can compute net
        deltas and avoid double-applying on !collect / reconnect.
        """
        if "Blue Gem" in item_name:
            self._total_blue_gems += 1
        elif item_name == "Small Health Gem":
            self.handle_receive_health_gem_s()   # instant, one-shot
        elif item_name == "Small Mana Gem":
            self.handle_receive_mana_gem_s()
        elif "Red Life Crystal" in item_name:
            self._total_health_gems += 1
        elif "Green Magic Crystal" in item_name:
            self._total_mana_gems += 1
        elif any(k in item_name for k in ("Tail", "Bracers", "Helmet")):
            self._received_armor.add(item_name)
        elif "Chapter" in item_name:
            self._num_chapters_unlocked += 1
        elif "Fury" in item_name:
            if "Spyro" in item_name:
                self._learned_fury[0] = True
            elif "Cynder" in item_name:
                self._learned_fury[1] = True
            elif "Dragon's" in item_name:
                self._learned_fury[0] = True
                self._learned_fury[1] = True
        elif "Elements" in item_name:
            # Even if some are already unlocked from not being put into the shuffle pool,
            # setting them all to 1 will do what needs to be done every time.
            if "Spyro" in item_name:
                self._learned_elements.add("Fire")
                self._learned_elements.add("Electricity")
                self._learned_elements.add("Ice")
                self._learned_elements.add("Earth")
            elif "Cynder" in item_name:
                self._learned_elements.add("Poison")
                self._learned_elements.add("Fear")
                self._learned_elements.add("Wind")
                self._learned_elements.add("Shadow")
        elif item_name in ITEM_NAME_TO_ELEMENT:
            # Item is an individual element
            self._learned_elements.add(ITEM_NAME_TO_ELEMENT[item_name])
        elif item_name == "Wall Climbing":
            self._learned_wall_climbing = True
        elif item_name == "Wall Running":
            if not self._learned_wall_running:
                self._learned_wall_running = True
                if self._wall_running_learner_task and not self._wall_running_learner_task.done():
                    self._wall_running_learner_task.cancel()
                self._wall_running_learner_task = asyncio.create_task(wall_running_learner(self), name="wall running learner")
            

        # Instant consumables (Small Health Gem / Small Mana Gem) are handled inside
        # handle_receive_item because they are meant to be applied once per
        # receipt, not re-applied on reconnect.

    def _flush_item_state(self):
        """
        Write the server-authoritative item state to game memory.
        Called after every ReceivedItems batch so the game always reflects
        what the server says the player should have.
        """

        # XP: Only adjust the server-contributed portion; don't clobber in-world gains.
        # We track the delta between what we last wrote and what we're writing now.
        saved_blue_gems_count = self.memory.read_u32(ADDR_AP_BLUE_GEMS_COUNTER) or 0
        exp_delta = (self._total_blue_gems - saved_blue_gems_count) * 1000
        if exp_delta != 0:
            # Read EXP values and calculate the total EXP for each dragon
            spyro_unspent_exp = self.memory.read_u32(ADDR_SPYRO_UNSPENT_EXP) or 0
            fire_exp = self.memory.read_u32(ADDR_SPYRO_FIRE_EXP) or 0
            ice_exp = self.memory.read_u32(ADDR_SPYRO_ICE_EXP) or 0
            earth_exp = self.memory.read_u32(ADDR_SPYRO_EARTH_EXP) or 0
            elec_exp = self.memory.read_u32(ADDR_SPYRO_ELEC_EXP) or 0
            spyro_total_exp = spyro_unspent_exp + fire_exp + ice_exp + earth_exp + elec_exp
            
            cynder_unspent_exp = self.memory.read_u32(ADDR_CYNDER_UNSPENT_EXP) or 0
            poison_exp = self.memory.read_u32(ADDR_CYNDER_POISON_EXP) or 0
            shadow_exp = self.memory.read_u32(ADDR_CYNDER_SHADOW_EXP) or 0
            fear_exp = self.memory.read_u32(ADDR_CYNDER_FEAR_EXP) or 0
            wind_exp = self.memory.read_u32(ADDR_CYNDER_WIND_EXP) or 0
            cynder_total_exp = cynder_unspent_exp + poison_exp + shadow_exp + fear_exp + wind_exp

            exp_cap = 268000
            
            # Give EXP to Spyro, prevent it from going over cap and give excess to Cynder
            spyro_excess_exp = max(0, spyro_total_exp + exp_delta - exp_cap)
            spyro_unspent_exp += exp_delta - spyro_excess_exp
            spyro_total_exp += exp_delta - spyro_excess_exp
            # Same but for Cynder
            cynder_excess_exp = max(0, cynder_total_exp + spyro_excess_exp + exp_delta - exp_cap)
            cynder_unspent_exp += spyro_excess_exp + exp_delta - cynder_excess_exp
            # Give Cynder's excess EXP to Spyro
            if cynder_excess_exp > 0 and spyro_total_exp < exp_cap:
                spyro_excess_exp = max(0, spyro_total_exp + cynder_excess_exp - exp_cap)
                spyro_unspent_exp += cynder_excess_exp - spyro_excess_exp

            # Write the EXP to memory
            self.memory.write_u32(ADDR_SPYRO_UNSPENT_EXP, max(0, spyro_unspent_exp))
            self.memory.write_u32(ADDR_CYNDER_UNSPENT_EXP, max(0, cynder_unspent_exp))
        self.memory.write_u32(ADDR_AP_BLUE_GEMS_COUNTER, self._total_blue_gems)

        # Gem counts: these are continuously enforced by the setter tasks, so
        # just update the module-level globals that those tasks read.
        global health_gems_collected, mana_gems_collected
        health_gems_collected = self._total_health_gems
        mana_gems_collected = self._total_mana_gems

        # Armor: set scratch flags for everything we've received
        for armor_name in self._received_armor:
            scratch_addr = ARMOR_NAME_TO_SCRATCH_ADDRESS.get(armor_name)
            if scratch_addr:
                self.memory.write_bytes(scratch_addr, b"\x01")
        
        # Chapters: set scratch flags for all unlocked chapters
        for i in range(self._num_chapters_unlocked + 1):
            chapter_name = self.chapter_order[i]
            scratch_addr = LEVEL_NAME_TO_SCRATCH_ADDRESS.get(chapter_name)
            if scratch_addr:
                self.memory.write_bytes(scratch_addr, b"\x01")
        
        # Learn Fury
        # If learn_fury is disabled, fury is always unlocked
        if self.learn_fury == 0:
            self._learned_fury = [True, True]

        # Shuffled Elements: set scratch flags for everything we've received
        for element in self._learned_elements:
            scratch_addr = ELEMENT_NAME_TO_UNLOCKED_ADDRESS.get(element)
            if scratch_addr:
                self.memory.write_bytes(scratch_addr, b"\x01")

    # ------------------------------------------------------------------
    # Patches
    # ------------------------------------------------------------------
    def install_element_rando(self):
        routine = bytes([
            0x00, 0x00, 0x11, 0x24,
            0x24, 0x00, 0x44, 0x92,
            0x02, 0x00, 0x80, 0x10,
            0x21, 0x88, 0x23, 0x02,
            0x04, 0x00, 0x31, 0x26,
            0xA6, 0x00, 0x04, 0x3C,
            0xA0, 0xC6, 0x84, 0x34,
            0x21, 0x20, 0x91, 0x00,
            0x00, 0x00, 0x84, 0x90,
            0x02, 0x00, 0x80, 0x10,
            0x00, 0x00, 0x00, 0x00,
            0x70, 0x1D, 0x43, 0xAE,
            0x13, 0xA7, 0x0D, 0x08,
            0x01, 0x00, 0x11, 0x64
        ])
        hook1 = bytes([
            0x80, 0xFE, 0x7F, 0x08,
            0x00, 0x00, 0x03, 0x24
        ])

        hook2 = bytes([
            0x80, 0xFE, 0x7F, 0x08,
            0x25, 0x18, 0x80, 0x00
        ])

        hook3 = bytes([
            0x80, 0xFE, 0x7F, 0x08,
            0x00, 0x00, 0x00, 0x00
        ])

        hook4 = bytes([
            0x00, 0x00, 0x03, 0x24,
            0x80, 0xFE, 0x7F, 0x08
        ])

        self.memory.write_bytes(0x01FFFA00, routine)
        self.memory.write_bytes(0x00369A2C, hook1)
        self.memory.write_bytes(0x00369A34, hook2)
        self.memory.write_bytes(0x00369A58, hook3)
        self.memory.write_bytes(0x00369A64, hook3)
        self.memory.write_bytes(0x00369A8C, hook3)
        self.memory.write_bytes(0x00369BB4, hook4)
    def apply_patches(self):
        # ARMOR OWNERSHIP BYTE SPLIT
        self.memory.write_bytes(ADDR_ARMOR_OWNERSHIP_CHECK_ROUTINE, bytes([
            0x21, 0x00, 0x83, 0x90,  # lbu v1, 0x21(a0)
            0xB4, 0x70, 0x0E, 0x08,  # j 0x0039c2d0
            0x00, 0x00, 0x00, 0x00,  # nop
            0x00, 0x00, 0x00, 0x00,  # nop
        ]))
        self.memory.write_bytes(ADDR_ARMOR_OWNERSHIP_CHECK_HOOK, bytes([
            0x4E, 0xFB, 0x7F, 0x08,  # j 0x01FFED38
        ]))

        # CHAPTER UNLOCK BYTE SPLIT
        self.memory.write_bytes(0x003BDCC4, bytes([
            0x54, 0x02, 0x45, 0x90
        ]))

        # CHAPTER MENU PERMANENT UNLOCK PATCH
        self.memory.write_bytes(0x005E7CB0, bytes([
            0x01, 0x00, 0x03, 0x34
        ]))

        # STORY MODE PERMANENT LOCK PATCH
        self.memory.write_bytes(0x005E7C78, bytes([
            0x01, 0x00, 0x05, 0x34
        ]))

        # BLUE GEMS GIVE 0 EXP PATCH
        self.memory.write_u32(0x009FEB14, 0)

        # ELEMENT RANDO
        self.install_element_rando()

        print("Game patches applied.")

    def restore_scratch_flags(self):
        # Restore armor scratch flags from received armor set
        for armor_name in self._received_armor:
            scratch_addr = ARMOR_NAME_TO_SCRATCH_ADDRESS.get(armor_name)
            if scratch_addr:
                self.memory.write_bytes(scratch_addr, b"\x01")

        # Restore chapter scratch flags from chapter unlock count
        for i in range(self._num_chapters_unlocked + 1):
            chapter_name = self.chapter_order[i]
            scratch_addr = LEVEL_NAME_TO_SCRATCH_ADDRESS.get(chapter_name)
            if scratch_addr:
                self.memory.write_bytes(scratch_addr, b"\x01")

        # Restore element unlock scratch flags from received learned elements set
        for element in self._learned_elements:
            scratch_addr = ELEMENT_NAME_TO_UNLOCKED_ADDRESS.get(element)
            if scratch_addr:
                self.memory.write_bytes(scratch_addr, b"\x01")

        print("Scratch flags restored.")

    # ------------------------------------------------------------------
    # Death / kill
    # ------------------------------------------------------------------
    def on_deathlink(self, data: dict[str, Any]) -> None:
        super().on_deathlink(data)
        self.kill_player()

    def kill_player(self):
        if self.addr_spyro_hero and self.memory.read_bytes(self.addr_spyro_hero + 0x25, 1) == b"\x00":
            self.memory.write_u32(ADDR_SPYRO_CURRENT_HP, 0)
        elif self.addr_cynder_hero and self.memory.read_bytes(self.addr_cynder_hero + 0x25, 1) == b"\x01":
            self.memory.write_u32(ADDR_CYNDER_CURRENT_HP, 0)
        self.player_dead = True

    # ------------------------------------------------------------------
    # Legacy per-item receive handlers (still used for instant consumables)
    # ------------------------------------------------------------------
    def handle_receive_health_gem_s(self):
        # Base hp values are 300 and each health upgrade adds 100 max health in vanilla
        # Could be changed with a setting in the future by overwriting base and upgrade values in memory
        spyro_max_hp = 300 + 100 * (health_gems_collected // 4)
        spyro_hp = self.memory.read_u32(ADDR_SPYRO_CURRENT_HP) or 0
        spyro_hp += 15
        if spyro_hp > spyro_max_hp:
            spyro_hp = spyro_max_hp
        self.memory.write_u32(ADDR_SPYRO_CURRENT_HP, spyro_hp)

        cynder_max_hp = 300 + 100 * (health_gems_collected // 5)
        cynder_hp = self.memory.read_u32(ADDR_CYNDER_CURRENT_HP) or 0
        cynder_hp += 15
        if cynder_hp > cynder_max_hp:
            cynder_hp = cynder_max_hp
        self.memory.write_u32(ADDR_CYNDER_CURRENT_HP, cynder_hp)

    def handle_receive_mana_gem_s(self):
        # Base mana values are 300 and each mana upgrade adds 100 max mana in vanilla
        # Could be changed with a setting in the future by overwriting base and upgrade values in memory
        spyro_max_mana = 300 + 100 * (mana_gems_collected // 5)
        spyro_mana = self.memory.read_u32(ADDR_SPYRO_CURRENT_MANA) or 0
        spyro_mana += 15
        if spyro_mana > spyro_max_mana:
            spyro_mana = spyro_max_mana
        self.memory.write_u32(ADDR_SPYRO_CURRENT_MANA, spyro_mana)

        cynder_max_mana = 300 + 100 * (mana_gems_collected // 4)
        cynder_mana = self.memory.read_u32(ADDR_CYNDER_CURRENT_MANA) or 0
        cynder_mana += 15
        if cynder_mana > cynder_max_mana:
            cynder_mana = cynder_max_mana
        self.memory.write_u32(ADDR_CYNDER_CURRENT_MANA, cynder_mana)

    # ------------------------------------------------------------------
    # Goal completion
    # ------------------------------------------------------------------
    async def send_goal_completion(self):
        """Send the game-complete status to the Archipelago server."""
        if not self._goal_sent and self.slot:
            await self.send_msgs([{"cmd": "StatusUpdate", "status": ClientStatus.CLIENT_GOAL}])
            self._goal_sent = True
            print("Goal sent: Malefor defeated!")

    # ------------------------------------------------------------------
    # Hero pointers (dragon data in levels)
    # ------------------------------------------------------------------
    def update_hero_pointers(self) -> bool:
        """
        Retrieve the pointers for the CKHkS08Hero objects for Spyro and Cynder by following a pointer chain,
        then update the saved pointers with the values read or None if the read didn't succeed.
        """
        success = False
        # Base pointer to CKS08GrpHero is in a CKS08GameManager object, which is a global object (in GAME.KP2, so static)
        # This pointer is always null on the main menu and during loading screens
        # CKS08GameManager -> CKGrpS08Hero -> some group members stuff -> CKHkS08Hero (one for Spyro one for Cynder)
        if (addr_ckgrps08hero := self.memory.read_pointer(ADDR_PTR_CKGRPS08HERO)):
            if (addr_group_members := self.memory.read_pointer(addr_ckgrps08hero + 0x30)):
                if ((addr_spyro := self.memory.read_pointer(addr_group_members))
                        and (addr_cynder := self.memory.read_pointer(addr_group_members + 0x4))):
                    # We check to make sure that these are indeed CKHkS08Hero objects by checking the class pointer value
                    if (self.memory.read_u32(addr_spyro) == CLASS_PTR_CKHKS08HERO
                            and self.memory.read_u32(addr_cynder) == CLASS_PTR_CKHKS08HERO):
                        self.addr_spyro_hero = addr_spyro
                        self.addr_cynder_hero = addr_cynder
                        success = True
                        print(f"Spyro CKHkS08Hero object start address: {hex(addr_spyro)} | Cynder CKHkS08Hero object start address: {hex(addr_cynder)}")

        if not success:
            # Overwrite whatever previous pointer value with None
            self.addr_spyro_hero = None
            self.addr_cynder_hero = None
            print(f"Could not get Hero pointers.")
        return success

 # ------------------------------------------------------------------
    # Elite Enemy stuff
    # ------------------------------------------------------------------
    def edit_elite_data(self, elite_name: str) -> bool:
        """
        Edit data for the specified Elite enemy by first following a pointer chain
        to find the CKS08EnemyElementPool objects corresponding to the enemy type of the Elite,
        and then calling edit_mask_data for each object.
        On other versions, these objects are also used for decorative parts and armors that can be broken,
        however those were removed on PS2 and only the Elite masks remain.
        """
        success = False
        # Base pointer to CKS08GrpEnemy is in a CKS08GameManager object, which is a global object (in GAME.KP2, so static)
        # This pointer is always null on the main menu, during loading screens and in Malefor's Lair (no enemies)
        # CKS08GameManager -> CKGrpS08Enemy -> CKCommonBaseGroup -> CKGrpS08PoolEnemy -> CKS08EnemyElementPool[]
        if (addr_ckgrps08enemy := self.memory.read_pointer(ADDR_PTR_CKGRPS08ENEMY)):
            if (addr_ckcommonbasegroup := self.memory.read_pointer(addr_ckgrps08enemy + 0x2C)):
                addr_ckgrps08poolenemy = self.memory.read_pointer(addr_ckcommonbasegroup + 0x18)
                print(f"CKGrpS08Enemy address: {hex(addr_ckgrps08enemy)}")
                print(f"CKCommonBaseGroup address: {hex(addr_ckcommonbasegroup)}")

                while (addr_ckgrps08poolenemy and success == False):
                    # Check enemy type and the array of CKS08EnemyElementPool objects
                    if (self.memory.read_bytes(addr_ckgrps08poolenemy + 0x2C, 1) == ENEMY_NAME_TO_ID.get(elite_name)
                            and (addr_array_cks08enemyelementpool := self.memory.read_pointer(addr_ckgrps08poolenemy + 0x3C))
                            and (array_size := self.memory.read_u32(addr_ckgrps08poolenemy + 0x44)) is not None):
                        print(f"Enemy Pool for {elite_name} found at {hex(addr_ckgrps08poolenemy)}")
                        masks = []
                        for i in range(array_size):
                            if (mask := self.memory.read_pointer(addr_array_cks08enemyelementpool + (i * 4))):
                                if self.memory.read_u32(mask) == CLASS_PTR_CKS08ENEMYELEMENTPOOL:
                                    masks.append(mask)

                        for i, mask in enumerate(masks):
                            j = 0 if len(self.elite_elements.get(elite_name)) <= i else i
                            if (success := self.edit_mask_data(mask, elite_name, self.elite_elements.get(elite_name)[j])) == False:
                                break
                    # Enemy pools have a pointer to the next pool (null if last)
                    addr_ckgrps08poolenemy = self.memory.read_pointer(addr_ckgrps08poolenemy + 0x14)

        if not success:
            print(f"Could not properly edit Elite data for {elite_name}.")
        return success

    def edit_mask_data(self, addr_cks08enemyelementpool: int, elite_name: str, element_name: str) -> bool:
        """
        Overwrite data for the specified CKS08EnemeyElementPool (mask) based on the element.
        This includes the durability, wrong element damage multiplier, element ID,
        mask glow size and color and color of the mask geometry itself.
        """
        success = False
        # CKS08EnemyElementPool -> CKS08EnemyElement[] -> CKS08EnemyElement -> CGlowNodeFX / CNode
        # While technically an array of CKS08EnemyElement objects, the size is always 1, so we can just take the first element
        if (addr_array := self.memory.read_pointer(addr_cks08enemyelementpool + 0x4)):
            if (addr_cks08enemyelement := self.memory.read_pointer(addr_array)):
                if (addr_cglownodefx := self.memory.read_pointer(addr_cks08enemyelement + 0x5C)):
                    # Element ID
                    self.memory.write_u32(addr_cks08enemyelementpool + 0x14, ELEMENT_NAME_TO_ID.get(element_name))
                    print(f"Set element for mask at {hex(addr_cks08enemyelementpool)} to {element_name} for {elite_name}.")
                        
                    # Mask durability
                    durability = ELITE_ELEMENT_TO_BASE_DURABILITY.get(element_name)
                    self.memory.write_float(addr_cks08enemyelementpool + 0x18, durability)
                    print(f"Set base durability to {durability} for {element_name} mask.")
                    
                    # Damage multiplier for wrong element and melee
                    wrong_elem_multipler = durability / 10000
                    self.memory.write_float(addr_cks08enemyelementpool + 0x1C, wrong_elem_multipler)
                    print(f"Set wrong element damage multiplier to {wrong_elem_multipler} for {element_name} mask.")
                    
                    # Glow size and color
                    # Unfortunately, the glows in Floating Islands are just too broken so we won't bother with those
                    if elite_name != "Wyvern" and elite_name != "Hero Grublin":
                        self.memory.write_bytes(addr_cglownodefx + 0x48, ELITE_ELEMENT_TO_GLOW_COLOR.get(element_name))
                        self.memory.write_float(addr_cglownodefx + 0x40, ELITE_NAME_TO_GLOW_SIZE.get(elite_name))
                        print(f"Edited glow data for {elite_name}'s {element_name} mask.")

                    # Mask geometry color
                    if (addr_cnode := self.memory.read_pointer(addr_cks08enemyelement + 0x4C)):
                        success = self.edit_cnode_texture(addr_cnode, 0, ELITE_ELEMENT_TO_MASK_COLOR.get(element_name))

        if not success:
            print(f"Could not properly edit {element_name} mask data for {elite_name}.")
        return success

    def edit_cnode_texture(self, addr_cnode: int, ptr_texture: int, color: bytes = bytes([0xFF, 0xFF, 0xFF])) -> bool:
        """
        Edit the texture pointer of a CNode object and its color blend (defaults to white).
        The game is perfectly fine with null texture pointers and will render a solid
        color based on the color blend value.
        """
        success = False
        # CNode -> CGeometry -> CMaterial -> something related to texture -> the texture
        # The RGB value for the color blend is in the CGeometry object
        if self.memory.read_u32(addr_cnode) == CLASS_PTR_CNODE:
            if (addr_cgeometry := self.memory.read_pointer(addr_cnode + 0x1C)):
                if (addr_cmaterial := self.memory.read_pointer(addr_cgeometry + 0x24)):
                    if (addr_something_texture := self.memory.read_pointer(addr_cmaterial + 0x4)):
                        self.memory.write_u32(addr_something_texture, ptr_texture)
                        self.memory.write_bytes(addr_cgeometry + 0x20, color)
                        success = True
                        print(f"Set texture pointer {hex(ptr_texture)} and color {bytes.hex(color)} for CNode object at {hex(addr_cnode)}.")

        if not success:
            print(f"Could not edit CNode texture at address {hex(addr_cnode)}.")
        return success


# ---------------------------------------------------------------------------
# Globals (gem totals mirrored into memory by setter tasks)
# ---------------------------------------------------------------------------
health_gems_collected = 0
mana_gems_collected = 0


# ---------------------------------------------------------------------------
# Background tasks
# ---------------------------------------------------------------------------

async def emulator_watchdog(ctx: DotDContext):
    """
    Periodically tries to reconnect to PCSX2 if the connection was lost.
    Also re-checks the game version and re-applies patches after reconnection.
    """
    while True:
        try:
            currently_connected = ctx.memory.is_connected

            if not currently_connected:
                # Try to reconnect silently
                reconnected = ctx.memory._try_connect()
                if reconnected:
                    print("[Watchdog] Reconnected to PCSX2.")
                    # Re-validate game version on reconnect
                    if not ctx.check_game_version():
                        ctx._game_version_ok = False
                        print("[Watchdog] Wrong game version after reconnect — pausing operations.")
                    else:
                        ctx._game_version_ok = True
                        # Re-apply patches and restore flags since emulator memory was wiped
                        if ctx.slot:
                            ctx.apply_patches()
                            ctx.restore_scratch_flags()
                            ctx._flush_item_state()
        except Exception as e:
            print(f"[Watchdog] Unexpected error: {e}")

        await asyncio.sleep(3.0)


async def location_watcher(ctx: DotDContext):
    while True:
        try:
            if not ctx.memory.is_connected or not ctx._game_version_ok or not ctx.current_level or ctx.current_level == "Main Menu":
                await asyncio.sleep(1.0)
                continue

            for address, location_name in LOCATION_FLAG_ADDRESS_TO_NAME.items():
                try:
                    data = ctx.memory.read_bytes(address, 1)
                    if data is None:
                        continue
                    collected = int.from_bytes(data, byteorder="little")
                except Exception as e:
                    print(f"Error in location_watcher: {e}")
                    continue

                if (collected == 1 and not "Objective" in location_name) or collected == 2:
                    location_id = LOCATION_NAME_TO_ID[location_name]
                    if location_id not in ctx.checked_locations:
                        print(f"Check found: {location_name}")
                        ctx.checked_locations.add(location_id)
                        await ctx.check_locations([location_id])

            await asyncio.sleep(0.1)
        except Exception as e:
            print(f"Fatal error in location_watcher: {e}")
            await asyncio.sleep(1.0)


async def health_gem_setter(ctx: DotDContext):
    while True:
        try:
            if ctx.memory.is_connected and ctx._game_version_ok:
                ctx.memory.write_u32(ADDR_HEALTH_GEMS_COLLECTED, health_gems_collected)
        except Exception as e:
            print(f"Error in health_gem_setter: {e}")
        await asyncio.sleep(0.1)


async def mana_gem_setter(ctx: DotDContext):
    while True:
        try:
            if ctx.memory.is_connected and ctx._game_version_ok:
                ctx.memory.write_u32(ADDR_MANA_GEMS_COLLECTED, mana_gems_collected)
        except Exception as e:
            print(f"Error in mana_gem_setter: {e}")
        await asyncio.sleep(0.1)


async def fury_points_setter(ctx: DotDContext):
    while True:
        try:
            if ctx.memory.is_connected and ctx._game_version_ok:
                if not ctx._learned_fury[0]:
                    ctx.memory.write_u32(ADDR_SPYRO_CURRENT_FURY, 0)
                if not ctx._learned_fury[1]:
                    ctx.memory.write_u32(ADDR_CYNDER_CURRENT_FURY, 0)
        except Exception as e:
            print(f"Error in fury_points_setter: {e}")
        await asyncio.sleep(0.1)


async def death_watcher(ctx: DotDContext):
    while True:
        try:
            if ctx.slot and ctx.death_link_enabled and ctx.memory.is_connected and ctx._game_version_ok:
                # Check if the CKS08GameStructure object (the global object that holds our HP values) exists
                # and that the game is not paused/loading to avoid sending deaths on game (re)boot
                if (ctx.memory.read_u32(ADDR_CKS08GAMESTRUCTURE) == CLASS_PTR_CKS08GAMESTRUCTURE
                        and ctx.memory.read_bytes(ADDR_PAUSE_FLAG, 1) == b"\x00"):
                    spyro_hp = ctx.memory.read_u32(ADDR_SPYRO_CURRENT_HP)
                    cynder_hp = ctx.memory.read_u32(ADDR_CYNDER_CURRENT_HP)

                    # Guard against None (disconnected)
                    if spyro_hp is None or cynder_hp is None:
                        await asyncio.sleep(0.1)
                        continue

                    if spyro_hp == 0 or cynder_hp == 0:
                        if not ctx.player_dead:
                            current_time = time.time()
                            if current_time - ctx.last_death_link > 12.0:
                                ctx.player_dead = True
                                await ctx.send_death(death_text="Spyro and Cynder have fallen!")
                    else:
                        ctx.player_dead = False
        except Exception as e:
            print(f"Error in death_watcher: {e}")
        await asyncio.sleep(0.1)


async def goal_watcher(ctx: DotDContext):
    """
    Polls the final boss defeat flag. When set, sends goal completion to the server.
    Only active once connected to the server and game version is confirmed.
    """
    while True:
        try:
            if ctx.slot and ctx.memory.is_connected and ctx._game_version_ok and not ctx._goal_sent and ctx.current_level and ctx.current_level != "Main Menu":
                data = ctx.memory.read_bytes(ADDR_FINAL_BOSS_DEFEATED, 1)
                if data is not None and int.from_bytes(data, byteorder="little") == 1:
                    await ctx.send_goal_completion()
        except Exception as e:
            print(f"Error in goal_watcher: {e}")
        await asyncio.sleep(0.5)


async def level_watcher(ctx: DotDContext):
    """
    Everything that needs to be edited once per level load is done here.
    Once the level ID changes from FFFFFFFF to a valid level,
    it means the game is done reading the level files and deserializing objects,
    and the rest of the loading screen is spent just initializing states and stuff.
    Data that was never meant to be overwritten once loaded is already loaded in memory at this point
    and can be freely edited. Changes will last for as long as the level is loaded.
    Pointers to dynamic objects that need to be used later such as the Hero data are also fetched here.
    """
    while True:
        try:
            if ctx.memory.is_connected and ctx._game_version_ok:
                curr_level = ctx.memory.read_u32(ADDR_CURRENT_LEVEL)

                if curr_level is None or curr_level == 0xFFFFFFFF:
                    ctx.current_level = None
                    ctx.addr_spyro_hero = None
                    ctx.addr_cynder_hero = None
                    if ctx._wall_climbing_setter_task and not ctx._wall_climbing_setter_task.done():
                        ctx._wall_climbing_setter_task.cancel()
                        try:
                            await ctx._wall_climbing_setter_task
                        except asyncio.CancelledError:
                            pass
                    await asyncio.sleep(0.1)
                    continue

                if (level_name := LEVEL_ID_TO_NAME.get(curr_level)) != ctx.current_level:
                    ctx.current_level = level_name
                    print(f"[Level Watcher] Current Level : {level_name}")

                    # Update the necessary pointers
                    if ctx.update_hero_pointers():

                        # If wall climbing has not yet been learned, create a task to lock the ability
                        if not ctx._learned_wall_climbing:
                            if not ctx._wall_climbing_setter_task or ctx._wall_climbing_setter_task.done():
                                ctx._wall_climbing_setter_task = asyncio.create_task(wall_climbing_setter(ctx), name="wall climbing setter")

                        # If wall running has not yet been learned, set these bytes at offsets +0x9E0 from the base hero pointers to decimal 9,999
                        # This will disable wall running for the rest of the level
                        if not ctx._learned_wall_running:
                            ctx.memory.write_float(ctx.addr_spyro_hero + 0x9E0, 9999.0)
                            ctx.memory.write_float(ctx.addr_cynder_hero + 0x9E0, 9999.0)

                    # Edit Elites data
                    if ctx.random_elite_elements != 0 and (elites := LEVEL_NAME_TO_ELITES.get(level_name)):
                        for elite_name in elites:
                            ctx.edit_elite_data(elite_name)


                if level_name == "Main Menu":
                    menu_value = ctx.memory.read_bytes(ADDR_MENU_VALUE, 1) or b"\x00"

                    # If the menu value is 0x9 (can see New game/Load game) or 0x12 (Load menu with all 5 save slots),
                    # we know that the current data will be overwritten and some items will be lost
                    # Once this menu value changes, we can write back the items to memory
                    if ctx.last_menu_value == b"\x09" or ctx.last_menu_value == b"\x12":
                        if menu_value != b"\x09" and menu_value != b"\x12":
                            ctx._flush_item_state()
                            print("[Level Watcher] Restored item state after New/Load game")

                    ctx.last_menu_value = menu_value

        except Exception as e:
            print(f"Error in level_watcher: {e}")
        await asyncio.sleep(1.0)


async def wall_climbing_setter(ctx: DotDContext):
    """
    Periodically set the wall climb flag to 1 if not learned, otherwise set it to 0 and end the task.
    """
    while True:
        if ctx.addr_spyro_hero is None or ctx.addr_cynder_hero is None:
            await asyncio.sleep(0.1)
            continue

        if ctx.memory.read_u32(ctx.addr_spyro_hero) == CLASS_PTR_CKHKS08HERO and ctx.memory.read_u32(ctx.addr_cynder_hero) == CLASS_PTR_CKHKS08HERO:
            # Restore wall climbing and end the task if learned
            if ctx._learned_wall_climbing:
                ctx.memory.write_bytes(ctx.addr_spyro_hero + 0x1678, b"\x00")
                ctx.memory.write_bytes(ctx.addr_cynder_hero + 0x1678, b"\x00")
                break

            # Lock wall climbing
            ctx.memory.write_bytes(ctx.addr_spyro_hero + 0x1678, b"\x01")
            ctx.memory.write_bytes(ctx.addr_cynder_hero + 0x1678, b"\x01")
        await asyncio.sleep(0.1)


async def wall_running_learner(ctx: DotDContext):
    """
    Waits until the game signals it's safe to re-enable wall running
    (Hero pointers exist and are not stale), then flips it to the vanilla of decimal 0.25. If a reset happens
    mid-wait, _reset_item_state() cancels this task directly.
    """
    while True:
        # Heroes don't exist on the main menu
        if ctx.current_level == "Main Menu":
            break

        if ctx.addr_spyro_hero is not None and ctx.addr_cynder_hero is not None:
            if ctx.memory.read_u32(ctx.addr_spyro_hero) == CLASS_PTR_CKHKS08HERO and ctx.memory.read_u32(ctx.addr_cynder_hero) == CLASS_PTR_CKHKS08HERO:
                break

        await asyncio.sleep(0.1)

    # TODO: Write float instead unless u32 works.
    ctx.memory.write_float(ctx.addr_spyro_hero + 0x9E0, 0.25)
    ctx.memory.write_float(ctx.addr_cynder_hero + 0x9E0, 0.25)

# ---------------------------------------------------------------------------
# Entry point
# ---------------------------------------------------------------------------
def main(*args: str):
    async def _main(connect: str | None, password: str | None):
        ctx = DotDContext(None, None)

        # Version check before doing anything else
        if ctx.memory.is_connected:
            ctx._game_version_ok = ctx.check_game_version()
            if not ctx._game_version_ok:
                print("Wrong game version detected. Client will run but memory operations are disabled.")
                print("Please load the NTSC-U version of Dawn of the Dragon and restart the client.")
        else:
            # Not connected to PCSX2 yet; the watchdog will check version when it connects
            ctx._game_version_ok = False

        ctx.server_task = asyncio.create_task(server_loop(ctx), name="server loop")
        watcher_task = asyncio.create_task(location_watcher(ctx), name="location watcher")
        health_gem_task = asyncio.create_task(health_gem_setter(ctx), name="health gem task")
        mana_gem_task = asyncio.create_task(mana_gem_setter(ctx), name="mana gem task")
        fury_task = asyncio.create_task(fury_points_setter(ctx), name="fury task")
        death_task = asyncio.create_task(death_watcher(ctx), name="death watcher")
        goal_task = asyncio.create_task(goal_watcher(ctx), name="goal watcher")
        level_task = asyncio.create_task(level_watcher(ctx), name="level watcher")
        watchdog_task = asyncio.create_task(emulator_watchdog(ctx), name="emulator watchdog")

        if gui_enabled:
            ctx.run_gui()
        ctx.run_cli()

        await ctx.exit_event.wait()

        # Cancel all background tasks
        for task in (watcher_task, health_gem_task, mana_gem_task, fury_task, death_task, goal_task, level_task, watchdog_task):
            task.cancel()
            try:
                await task
            except asyncio.CancelledError:
                pass

        await ctx.shutdown()

    # TODO: Handle command line args
    asyncio.run(_main(None, None))


if __name__ == "__main__":
    import sys
    main(*sys.argv[1:])