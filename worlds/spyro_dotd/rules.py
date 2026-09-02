from __future__ import annotations
from typing import TYPE_CHECKING
from worlds.generic.Rules import set_rule, add_rule
if TYPE_CHECKING:
    from .world import DotDWorld

def set_all_rules(world: DotDWorld) -> None:
    set_location_rules(world)

def set_location_rules(world: DotDWorld):
    # Define all locations that may need rules attached to them
    # spyro_gallery = world.get_location("Spyro Gallery Unlock")
    # cynder_gallery = world.get_location("Cynder Gallery Unlock")
    alliance_gallery = world.get_location("Alliance Gallery Unlock")
    scenery_gallery  = world.get_location("Scenery Gallery Unlock")
    
    # Max Fire requires 70,500 EXP, Max Poison requires 68,500
    # NOTE: In order to make the experience more balanced and not require the player to dump every bit of their earned EXP into Fire and Poison, this number may need to increase.
    #       That being said, EXP gained from sourced outside of Blue Gems may make the experience more balanced by default.
    # set_rule(spyro_gallery, \
    #          lambda state: state.count("Blue Gem Cluster", world.player) >= 70)
    # set_rule(cynder_gallery, \
    #          lambda state: state.count("Blue Gem Cluster", world.player) >= 70)
    
    # Scenery Gallery unlocked when Burned Lands is cleared
    set_rule(scenery_gallery, \
             lambda state: state.can_reach_location("Burned Lands Cleared", world.player))

    # NOTE: The location rules set here are for extra locations that don't fall neatly under sub-regions in regions.py
    #       For example: Although it is at the waterfall base sub-region, which requires (Fire or Poison) and Electricity,
    #       the Catacombs Elite still needs Shadow to break the mask and Wall Climbing to beat the Golem to trigger the Elite's spawn.

    # Catacombs Location Logic
    set_rule(world.get_location("The Catacombs Cleared"), \
             lambda state: state.has("Cynder's Wind", world.player))
    set_rule(world.get_location("Catacombs Elite"), \
             lambda state: state.has("Cynder's Shadow", world.player))

    # Twilight Falls Location Logic
    set_rule(world.get_location("TF Elite"), \
             lambda state: state.has("Spyro's Earth", world.player))

    # Valley of Avalar Location Logic
    set_rule(world.get_location("VoA Elite"), \
             lambda state: state.has_all(("Spyro's Electricity", "Cynder's Fear"), world.player))
    set_rule(world.get_location("VoA Mana Gem - Behind Gate"), \
             lambda state: state.can_reach_location("Objective Complete - Find the Supply Cave", world.player))
    set_rule(world.get_location("VoA Armor Chest - Big Waterfall"), \
             lambda state: state.has("Wall Climbing", world.player))

    # Dragon City Location Logic
    set_rule(world.get_location("DC Blue Gem - Broken Stairs Top"), \
             lambda state: state.has("Wall Climbing", world.player))
    set_rule(world.get_location("DC Blue Gem - Broken Stairs Bottom"), \
             lambda state: state.has("Wall Climbing", world.player))
    set_rule(world.get_location("DC Blue Gem - Behind Shadow Gate Near Doors"), \
             lambda state: state.has("Cynder's Shadow", world.player))
    set_rule(world.get_location("DC Health Gem - Behind Bottom Shadow Gate Near Fire"), \
             lambda state: state.has("Cynder's Shadow", world.player))
    set_rule(world.get_location("DC Health Gem - Torches"), \
             lambda state: state.has_all(("Spyro's Fire", "Cynder's Wind", "Wall Climbing"), world.player))
    set_rule(world.get_location("DC Armor Chest - Behind Top Shadow Gate Near Fire"), \
             lambda state: state.has("Cynder's Shadow", world.player))
    

    # Attack of the Golem Location Logic
    set_rule(world.get_location("Attack of the Golem Cleared"), \
             lambda state: state.has("Wall Climbing", world.player))

    # Ruins of Warfang Location Logic
    set_rule(world.get_location("RoW Health Gem - Right Path Behind Vines"), \
             lambda state: state.has_any(("Spyro's Fire", "Cynder's Poison"), world.player))
    set_rule(world.get_location("RoW Mana Gem - Left Path Behind Vines"), \
             lambda state: state.has("Wall Climbing", world.player) and state.has_any(("Spyro's Fire", "Cynder's Poison"), world.player))
    set_rule(world.get_location("RoW Armor Chest - Up Right Path Under Earth Slab"), \
                 lambda state: state.has_any(("Spyro's Fire", "Cynder's Poison"), world.player))
    # Earliest can appear is after completion of lower left or lower right.
    # Upper left/right elite fights require lower-left and lower-right completion requirements, so by the absorption law, they're irrelevant
    # Lower left requires Fire, Swing, and Climb. Lower right requires Fear and climb. Elite mask itself can either be Fire, Ice, or Poison.
    # The logic below is that but simplified.
    set_rule(world.get_location("RoW Elite"), \
             lambda state: state.has_all(("Spyro's Fire", "Spyro's Ice", "Cynder's Poison", "Wall Climbing"), world.player) and state.has_any(("Chain Swinging", "Cynder's Fear"), world.player))

    # The Dam Location Logic
    set_rule(world.get_location("Dam Health Gem - Behind Left Shadow Gate"), \
             lambda state: state.has("Cynder's Shadow", world.player))
    set_rule(world.get_location("Dam Mana Gem - Behind Earth Wall"), \
             lambda state: state.has_all(("Spyro's Earth", "Chain Swinging"), world.player))

    # Burned Lands Location Logic
    set_rule(world.get_location("BL Elite"), \
             lambda state: state.has_all(("Cynder's Fear", "Spyro's Electricity", "Spyro's Earth"), world.player))
    set_rule(world.get_location("BL Health Gem - Elite"), \
                 lambda state: state.has_all(("Cynder's Fear", "Spyro's Electricity", "Spyro's Earth"), world.player))

    # Floating Islands Location Logic
    set_rule(world.get_location("Objective Complete - Torches Lit 8/8"), \
             lambda state: state.has("Spyro's Fire", world.player))
    set_rule(world.get_location("FI Elite - Wyvern"), \
             lambda state: state.has_all(("Spyro's Ice", "Cynder's Wind"), world.player))
    set_rule(world.get_location("FI Elite - Hero Grublin"), \
             lambda state: state.has_all(("Spyro's Fire", "Cynder's Shadow"), world.player))
    