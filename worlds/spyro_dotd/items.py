from __future__ import annotations

from typing import TYPE_CHECKING

from BaseClasses import Item, ItemClassification

if TYPE_CHECKING:
    from .world import DotDWorld


# Every item must have a unique integer ID associated with it
# We will have a lookup from item name to ID here that, in world.py, we will import and bind to the world class.
# Even if an item doesn't exist on specific options, it must be present in this lookup.
ITEM_NAME_TO_ID = {
    "Blue Gem Cluster": 1,
    "Red Life Crystal": 2,
    "Green Magic Crystal": 3,
    "Elite Enemy": 4,
    "Spyro Helmet Silver": 5,
    "Spyro Helmet Gold": 6,
    "Spyro Helmet Fury": 7,
    "Spyro Tail Silver": 8,
    "Spyro Tail Gold": 9,
    "Spyro Tail Fury": 10,
    "Spyro Bracers Silver": 11,
    "Spyro Bracers Gold": 12,
    "Spyro Bracers Fury": 13,
    "Cynder Helmet Silver": 14,
    "Cynder Helmet Gold": 15,
    "Cynder Helmet Fury": 16,
    "Cynder Tail Silver": 17,
    "Cynder Tail Gold": 18,
    "Cynder Tail Fury": 19,
    "Cynder Bracers Silver": 20,
    "Cynder Bracers Gold": 21,
    "Cynder Bracers Fury": 22,
    "Small Health Gem": 23, # This is the small gem that the player can pick up to recover their HP
    "Small Mana Gem": 24,   # Likewise, but for Mana
    "Dragons' Flight": 25,    # NOTE: Deprecated. We will no longer be gating flight.
    "Dragons' Elements": 26,  # NOTE: Deprecated. Elements are now handled per dragon or individually.
    "Spyro's Elements": 27,
    "Cynder's Elements": 28,
    "Wall Climbing": 29,
    "Wall Running": 30,
    "Progressive Chapter Unlock": 31,
    "Dragon's Fury": 32,
    "Spyro's Fury": 33,
    "Cynder's Fury": 34,
    "Fire": 35,
    "Electricity": 36,
    "Ice": 37,
    "Earth": 38,
    "Poison": 39,
    "Fear": 40,
    "Wind": 41,
    "Shadow": 42
}

# Items should havea defined default classification.
# In our case, we will make a dictionary from item name to classification.
DEFAULT_ITEM_CLASSIFICATIONS = {
    "Blue Gem Cluster": ItemClassification.useful,
    "Red Life Crystal": ItemClassification.useful,
    "Green Magic Crystal": ItemClassification.useful,
    # "Elite Enemy": ItemClassification.useful,
    "Spyro Helmet Silver": ItemClassification.useful,
    "Spyro Helmet Gold": ItemClassification.useful,
    "Spyro Helmet Fury": ItemClassification.useful,
    "Spyro Tail Silver": ItemClassification.useful,
    "Spyro Tail Gold": ItemClassification.useful,
    "Spyro Tail Fury": ItemClassification.useful,
    "Spyro Bracers Silver": ItemClassification.useful,
    "Spyro Bracers Gold": ItemClassification.useful,
    "Spyro Bracers Fury": ItemClassification.useful,
    "Cynder Helmet Silver": ItemClassification.useful,
    "Cynder Helmet Gold": ItemClassification.useful,
    "Cynder Helmet Fury": ItemClassification.useful,
    "Cynder Tail Silver": ItemClassification.useful,
    "Cynder Tail Gold": ItemClassification.useful,
    "Cynder Tail Fury": ItemClassification.useful,
    "Cynder Bracers Silver": ItemClassification.useful,
    "Cynder Bracers Gold": ItemClassification.useful,
    "Cynder Bracers Fury": ItemClassification.useful,
    "Small Health Gem": ItemClassification.filler,
    "Small Mana Gem": ItemClassification.filler,
    "Dragons' Flight": ItemClassification.progression,      # NOTE: Deprecated. We will no longer be gating flight.
    "Dragons' Elements": ItemClassification.progression,    # NOTE: Deprecated. Elements are now handled per dragon or individually.
    "Spyro's Elements": ItemClassification.progression,
    "Cynder's Elements": ItemClassification.progression,
    "Progressive Chapter Unlock": ItemClassification.progression,
    "Dragon's Fury": ItemClassification.progression,
    "Spyro's Fury": ItemClassification.progression,
    "Cynder's Fury": ItemClassification.progression,
    "Fire": ItemClassification.progression,
    "Electricity": ItemClassification.progression,
    "Ice": ItemClassification.progression,
    "Earth": ItemClassification.progression,
    "Poison": ItemClassification.progression,
    "Fear": ItemClassification.progression,
    "Wind": ItemClassification.progression,
    "Shadow": ItemClassification.progression
}

# Each Item instance must correctly report to the "game" it belongs to.
# To make this simple, it is common practice to subclass the basic Item class and override the "game" field.
class DotDItem(Item):
    game = "The Legend of Spyro: Dawn of the Dragon"

# On top of our regular item pool, our world must be able to create arbitrary amounts of filler as requested by core.
# To do this, it must define a function called world.get_filler_item_name(), which we will define in world.py later.
# For now, let's make a function that returns the name of a random filler item in here in items.py.
def get_random_filler_item_name(world: DotDWorld) -> str:
    # NOTE: Use world.random when need RNG
    return "Small Health Gem" if world.random.randint(0, 1) == 0 else "Small Mana Gem"

def create_item_with_correct_classification(world: DotDWorld, name: str) -> DotDItem:
    # Our world class must have a create_item() function that can create any of our items by name at any time.
    # So, we make this helper function that creates the item by name with the correct classification.
    # NOTE: This function's content could just bne the contents of world.create_item in world.py directly,
    # but it might be nicer to have it in its own function over here in items.py.
    classification = DEFAULT_ITEM_CLASSIFICATIONS[name]

    # NOTE: It is perfectly normal and valid for an item's classification to differ based on the player's options.

    return DotDItem(name, classification, ITEM_NAME_TO_ID[name], world.player)

# With those two helper functions defined, let's now get to actually creating and submitting our item pool
def create_all_items(world: DotDWorld) -> None:
    # This is the function in which we will create all the items that this world submits to the multiworld item pool.
    # There must be exactly as many items as there are locations.

    # NOTE: There must always be as many items as there are locations.

    # Get all non-unique items
    blue_gems = [world.create_item("Blue Gem Cluster") for _ in range(99)]
    health_gems = [world.create_item("Red Life Crystal") for _ in range(20)]
    mana_gems = [world.create_item("Green Magic Crystal") for _ in range(20)]
    # elite_enemies = [world.create_item("Elite Enemy") for _ in range(8)]

    # NOTE: The thing about elite enemies is that they drop nothing but a metric ton of
    # filler items, and I haven't looked into canceling out what they drop or giving it to players later,
    # so we're gonna avoid them for now

    itempool: list[Item] = blue_gems + health_gems + mana_gems #+ elite_enemies

    # Add armor
    # Uncomment lines as needed.
    itempool.append(world.create_item("Spyro Helmet Silver"))
    itempool.append(world.create_item("Spyro Helmet Gold"))
    itempool.append(world.create_item("Spyro Helmet Fury"))
    itempool.append(world.create_item("Spyro Tail Silver"))
    itempool.append(world.create_item("Spyro Tail Gold"))
    itempool.append(world.create_item("Spyro Tail Fury"))
    itempool.append(world.create_item("Spyro Bracers Silver"))
    itempool.append(world.create_item("Spyro Bracers Gold"))
    itempool.append(world.create_item("Spyro Bracers Fury"))
    itempool.append(world.create_item("Cynder Helmet Silver"))
    itempool.append(world.create_item("Cynder Helmet Gold"))
    itempool.append(world.create_item("Cynder Helmet Fury"))
    itempool.append(world.create_item("Cynder Tail Silver"))
    itempool.append(world.create_item("Cynder Tail Gold"))
    itempool.append(world.create_item("Cynder Tail Fury"))
    itempool.append(world.create_item("Cynder Bracers Silver"))
    itempool.append(world.create_item("Cynder Bracers Gold"))
    itempool.append(world.create_item("Cynder Bracers Fury"))

    # Add level keys
    keys = [world.create_item("Progressive Chapter Unlock") for _ in range(10)]
    itempool += keys
    
    # NOTE: Some items may only exist if the player enables certain options
    # if world.options.learn_to_fly:
    #     itempool.append(world.create_item("Dragons' Flight"))
    # if world.options.learn_to_climb:
    #     itempool.append(world.create_item("Wall Climbing"))
    # if world.options.learn_to_wall_run:
    #     itempool.append(world.create_item("Wall Running"))
    # if world.options.learn_to_breathe.current_key == "both_together":
    #     itempool.append(world.create_item("Dragons' Elements"))
    # elif world.options.learn_to_breathe.current_key == "both_separate":
    #     itempool.append(world.create_item("Spyro's Elements"))
    #     itempool.append(world.create_item("Cynder's Elements"))
    # elif world.options.learn_to_breathe.current_key == "spyro":
    #     itempool.append(world.create_item("Spyro's Elements"))
    # elif world.options.learn_to_breathe.current_key == "cynder":
    #     itempool.append(world.create_item("Cynder's Elements"))
    if world.options.learn_fury.current_key == "both_together":
        itempool.append(world.create_item("Dragon's Fury"))
    elif world.options.learn_fury.current_key == "both_separate":
        itempool.append(world.create_item("Spyro's Fury"))
        itempool.append(world.create_item("Cynder's Fury"))
    elif world.options.learn_fury.current_key == "spyro":
        itempool.append(world.create_item("Spyro's Fury"))
    elif world.options.learn_fury.current_key == "cynder":
        itempool.append(world.create_item("Cynder's Fury"))

    # Handle adding shuffled elements to item pool
    if world.options.shuffled_elements.value:
        # Elements have been shuffled, determine how they're being handled and by which dragon.
        # Handle Spyro Elements
        if any(element in world.options.shuffled_elements.value for element in ["Fire", "Electricity", "Ice", "Earth"]):
            if world.options.spyro_elements_handling.current_key == "individual":
                for element in world.options.shuffled_elements.value.intersection({"Fire", "Electricity", "Ice", "Earth"}):
                    itempool.append(world.create_item(element))
            else:
                itempool.append(world.create_item("Spyro's Elements"))
        # Handle Cynder Elements
        if any(element in world.options.shuffled_elements.value for element in ["Poison", "Fear", "Wind", "Shadow"]):
            if world.options.cynder_elements_handling.current_key == "individual":
                for element in world.options.shuffled_elements.value.intersection({"Poison", "Fear", "Wind", "Shadow"}):
                    itempool.append(world.create_item(element))
            else:
                itempool.append(world.create_item("Cynder's Elements"))

    
    # Archipelago requires that each world submits as many locations as it submits items.
    # This is where we can use our filler and trap items.
    # We can compare the size of our itempool so far to the number of locations in our world.

    # The length of our itempool is easy to determine, since we have it as a list.
    number_of_items = len(itempool)

    # The number of locations is also easy to determine, but we have to be careful.
    # Just calling len(world.get_locations()) would report an incorrect number, because of our *event locations*.
    # What we actually want is the number of *unfilled* locations. Luckily, there is a helper method for this:
    number_of_unfilled_locations = len(world.multiworld.get_unfilled_locations(world.player))

    # Now, we just subtract the number of items from the number of locations to get the number of empty item slots.
    needed_number_of_filler_items = number_of_unfilled_locations - number_of_items

    # Finally, we create that many filler items and add them to the itempool.
    # To create our filler, we could just use world.create_item("Confetti Cannon").
    # But there is an alternative that works even better for most worlds, including APQuest.
    # As discussed above, our world must have a get_filler_item_name() function defined,
    # which must return the name of an infinitely repeatable filler item.
    # Defining this function enables the use of a helper function called world.create_filler().
    # You can just use this function directly to create as many filler items as you need to complete your itempool.
    itempool += [world.create_filler() for _ in range(needed_number_of_filler_items)]

    # With our world's itempool finalized, we now need to submit it to the multiworld itempool.
    # This is how the generator actually knows about the existence of our items.
    world.multiworld.itempool += itempool