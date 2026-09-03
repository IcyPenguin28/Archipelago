from __future__ import annotations
from typing import TYPE_CHECKING
from BaseClasses import CollectionState
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
    #       the Catacombs Elite still needs its element to break the mask and Wall Climbing to beat the Golem to trigger the Elite's spawn.

    # Catacombs Location Logic
    set_rule(world.get_location("The Catacombs Cleared"), \
             lambda state: state.has(world.element_items["Wind"], world.player))
    set_rule(world.get_location("Catacombs Elite"), \
             lambda state: has_required_elite_elements(world, state, "Grublin"))

    # Twilight Falls Location Logic
    set_rule(world.get_location("TF Elite"), \
             lambda state: has_required_elite_elements(world, state, "Grublin Fly"))

    # Valley of Avalar Location Logic
    set_rule(world.get_location("VoA Elite"), \
             lambda state: has_required_elite_elements(world, state, "Axe Orc"))
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
             lambda state: state.has(world.element_items["Shadow"], world.player))
    set_rule(world.get_location("DC Health Gem - Behind Bottom Shadow Gate Near Fire"), \
             lambda state: state.has(world.element_items["Shadow"], world.player))
    set_rule(world.get_location("DC Health Gem - Torches"), \
             lambda state: state.has_all((world.element_items["Fire"], world.element_items["Wind"], "Wall Climbing"), world.player))
    set_rule(world.get_location("DC Armor Chest - Behind Top Shadow Gate Near Fire"), \
             lambda state: state.has(world.element_items["Shadow"], world.player))
    

    # Attack of the Golem Location Logic
    set_rule(world.get_location("Attack of the Golem Cleared"), \
             lambda state: state.has("Wall Climbing", world.player))

    # Ruins of Warfang Location Logic
    set_rule(world.get_location("RoW Health Gem - Right Path Behind Vines"), \
             lambda state: state.has_any((world.element_items["Fire"], world.element_items["Poison"]), world.player))
    set_rule(world.get_location("RoW Mana Gem - Left Path Behind Vines"), \
             lambda state: state.has("Wall Climbing", world.player) and state.has_any((world.element_items["Fire"], world.element_items["Poison"]), world.player))
    set_rule(world.get_location("RoW Armor Chest - Up Right Path Under Earth Slab"), \
             lambda state: state.has_any((world.element_items["Fire"], world.element_items["Poison"]), world.player))
    # Earliest the Elite can appear is after completion of lower left or lower right.
    # Upper left/right elite fights require lower-left and lower-right completion requirements, so by the absorption law, they're irrelevant
    # Lower left requires Fire, Swing, and Climb. Lower right requires Fear and climb. Elite mask itself can be whatever (vanilla is Fire, Ice or Poison)
    # The logic below is that but simplified.
    set_rule(world.get_location("RoW Elite"), \
             lambda state: has_required_elite_elements(world, state, "Troll") and state.has("Wall Climbing", world.player) and state.has_any((world.element_items["Fire"], world.element_items["Fear"]), world.player))
            # lambda state: has_required_elite_elements(world, state, "Troll") and state.has("Wall Climbing", world.player) and (state.has_all((world.element_items["Fire"], "Chain Swinging"), world.player) or state.has(world.element_items["Fear"], world.player)))    # Swap when and if we gate swinging
    # The Dam Location Logic
    set_rule(world.get_location("Dam Health Gem - Behind Left Shadow Gate"), \
             lambda state: state.has(world.element_items["Shadow"], world.player))
    set_rule(world.get_location("Dam Mana Gem - Behind Earth Wall"), \
             lambda state: state.has(world.element_items["Earth"], world.player))
            # lambda state: state.has_all((world.element_items["Earth"], "Chain Swinging"), world.player))  # Swap when and if we gate swinging
    set_rule(world.get_location("Dam Elite"), \
             lambda state: has_required_elite_elements(world, state, "Crossbow Orc"))

    # Burned Lands Location Logic
    set_rule(world.get_location("BL Elite"), \
             lambda state: has_required_elite_elements(world, state, "Hero Orc"))
    set_rule(world.get_location("BL Health Gem - Elite"), \
             lambda state: state.can_reach_location("BL Elite", world.player))

    # Floating Islands Location Logic
    set_rule(world.get_location("Objective Complete - Torches Lit 8/8"), \
             lambda state: state.has(world.element_items["Fire"], world.player))
    set_rule(world.get_location("FI Elite - Wyvern"), \
             lambda state: has_required_elite_elements(world, state, "Wyvern"))
    set_rule(world.get_location("FI Elite - Hero Grublin"), \
             lambda state: has_required_elite_elements(world, state, "Hero Grublin"))

# ------------------------------------------------------------------
# State Helpers
# ------------------------------------------------------------------
def has_required_elite_elements(world: DotDWorld, state: CollectionState, elite_name: str) -> bool:
    elements = []
    for elem in world.elite_elements[elite_name]:
        elements.append(world.element_items[elem])
    return state.has_all(elements, world.player)
