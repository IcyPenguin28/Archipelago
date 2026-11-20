from __future__ import annotations
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from .client import DotDContext

def install_element_rando(ctx: DotDContext):
    """
    Allows elements to be shuffled away as items, rather than
    being able to switch between all 8 at any time.
    \nElem0s (fire and poison) are put on essentially infinite cooldown to disable them specifically.
    """
    routine_elem0 = bytes([
        0x0C, 0x00, 0x43, 0x10,
        0x70, 0x1D, 0x22, 0x8E,
        0x08, 0x00, 0x40, 0x14,
        0x24, 0x00, 0x22, 0x82,
        0xA6, 0x00, 0x04, 0x3C,
        0x02, 0x00, 0x40, 0x10,
        0xA0, 0xC6, 0x84, 0x34,
        0x04, 0x00, 0x84, 0x24,
        0x00, 0x00, 0x82, 0x80,
        0x03, 0x00, 0x40, 0x10,
        0x00, 0x00, 0x00, 0x00,
        0x93, 0x94, 0x0D, 0x08,
        0x00, 0x00, 0x00, 0x00,
        0xA4, 0x94, 0x0D, 0x08,
        0x00, 0x00, 0x00, 0x00
    ])
    hook_elem0 = bytes([
        0x6B, 0xFE, 0x7F, 0x08
    ])
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

    ctx.memory.write_bytes(0x01FFF9AC, routine_elem0)
    ctx.memory.write_bytes(0x00365244, hook_elem0)
    ctx.memory.write_bytes(0x01FFFA00, routine)
    ctx.memory.write_bytes(0x00369A2C, hook1)
    ctx.memory.write_bytes(0x00369A34, hook2)
    ctx.memory.write_bytes(0x00369A58, hook3)
    ctx.memory.write_bytes(0x00369A64, hook3)
    ctx.memory.write_bytes(0x00369A8C, hook3)
    ctx.memory.write_bytes(0x00369BB4, hook4)


def install_armor_ownership_byte_split(ctx: DotDContext):
    """
    Distinguishes between owning a piece of armor and having opened its chest.
    \nIn vanilla, armor ownership is the same byte saying the chest has been opened.
    Since chests are AP locations and armor pieces are AP items, this distinction has to be made.
    """
    ctx.memory.write_bytes(0x0039C2CC, bytes([
        0x21, 0x00, 0x83, 0x90,  # lbu v1, 0x21(a0)
    ]))


def install_chapter_unlock_byte_split(ctx: DotDContext):
    """
    Distinguishes between finishing a level and having it unlocked in chapter mode.
    \nIn vanilla, the flag that a level is completed is the same one that unlocks it in chapter mode.
    Since level completions are AP locations and level unlocks are AP items, this distinction has to be made.
    """
    ctx.memory.write_bytes(0x003BDCC4, bytes([
        0x54, 0x02, 0x45, 0x90
    ]))


def install_chapter_mode_permanent_unlock(ctx: DotDContext):
    """
    Unlocks Chapter Mode immediately.
    \nBy default on a New Game, chapter mode is disabled and story mode is.
    Since this AP runs exclusively in chapter mode, we need to do the opposite.
    """
    ctx.memory.write_bytes(0x005E7CB0, bytes([
        0x01, 0x00, 0x03, 0x34
    ]))


def install_story_mode_permanent_lock(ctx: DotDContext):
    """
    Locks Story Mode immediately.
    \nBy default on a New Game, story mode is enabled and chapter mode is not.
    Since this AP runs exclusively in chapter mode, we need to do the opposite.
    """
    ctx.memory.write_bytes(0x005E7C78, bytes([
        0x01, 0x00, 0x05, 0x34
    ]))


def install_empty_blue_gems(ctx: DotDContext):
    """
    Makes it so that all Blue Gem Clusters give 0 EXP.
    \nSince we get XP from the server, we need to disable acquiring it from the Blue Gem Clusters themselves.
    """
    ctx.memory.write_u32(0x009FEB14, 0)


def install_hyper_enemies(ctx: DotDContext):
    """
    Doubles the speed and strength of all non-boss enemies.
    """
    ctx.memory.write_bytes(0x002FB794, bytes([
        0x00, 0x40, 0x02, 0x3C
    ]))


def install_armor_fixes(ctx: DotDContext):
    """
    Restores originally-intended functionality to certain armor pieces.
    """
    ctx.memory.write_bytes(0x0034E464, bytes([
        0xFF, 0xF7, 0x03, 0x24
    ]))
    ctx.memory.write_bytes(0x0034E474, bytes([
        0x00, 0x08, 0x63, 0x34
    ]))
    ctx.memory.write_bytes(0x0033C0BC, bytes([
        0xCC, 0x0E, 0x89, 0x8C
    ]))
    ctx.memory.write_bytes(0x0033C0C4, bytes([
        0xCC, 0x0E, 0x88, 0xAC
    ]))
    ctx.memory.write_bytes(0x0033D214, bytes([
        0xCC, 0x0E, 0x82, 0x8E
    ]))
    ctx.memory.write_bytes(0x00343C78, bytes([
        0xCC, 0x0E, 0x24, 0x8E
    ]))
    ctx.memory.write_bytes(0x00343C80, bytes([
        0xCC, 0x0E, 0x23, 0xAE,
        0xCC, 0x0E, 0x23, 0x8E
    ]))
    ctx.memory.write_bytes(0x00343C90, bytes([
        0xCC, 0x0E, 0x23, 0xAE
    ]))
    ctx.memory.write_bytes(0x0036E4DC, bytes([
        0xCC, 0x0E, 0x03, 0x8E
    ]))
    ctx.memory.write_bytes(0x0036E4E4, bytes([
        0xCC, 0x0E, 0x02, 0xAE,
        0xCC, 0x0E, 0x02, 0x8E
    ]))
    ctx.memory.write_bytes(0x0036E4F4, bytes([
        0xCC, 0x0E, 0x02, 0xAE
    ]))


def install_enemy_health_mult_override(ctx: DotDContext):
    health_bytes = [0x80, 0x3F]         # 1.0
    if ctx.enemy_health == 1:
        health_bytes = [0x00, 0x3F]     # 0.5
    elif ctx.enemy_health == 2:
        health_bytes = [0x00, 0x40]     # 2.0
    health_bytes.extend([0x02, 0x3C])   # Rest of the instruction (lui v0)
    ctx.memory.write_bytes(0x002FB77C, bytes(health_bytes))


def install_story_mode_string_override(ctx: DotDContext):
    """
    Override the Story Mode Over string with a custom AP-related one
    """
    # Override pointer in text object to point to custom string
    ctx.memory.write_bytes(0x00A1AD98, bytes([
        0xF0, 0xB2, 0xA9, 0x00
    ]))

    # The custom string in question
    ctx.memory.write_string(ctx.memory.read_pointer(0x00A1AD98), ctx.story_mode_string)