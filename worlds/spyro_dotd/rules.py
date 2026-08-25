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