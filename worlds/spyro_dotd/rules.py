from __future__ import annotations
from typing import TYPE_CHECKING
from worlds.generic.Rules import set_rule
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

    # Attack of the Golem Location Logic
    set_rule(world.get_location("Attack of the Golem Cleared"), \
             lambda state: state.has("Wall Climbing", world.player))
    