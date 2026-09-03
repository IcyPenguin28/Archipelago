from collections.abc import Mapping
from typing import Any, Optional

# Imports of base Archipelago modules must be absolute
from worlds.AutoWorld import World

# Imports of your world's files must be relative
from . import items, locations, options, regions, rules, web_world

class DotDWorld(World):
    """
    The Legend of Spyro: Dawn of the Dragon is a 3D action-adventure game and the final installment of
    The Legend of Spyro trilogy of games. Players control Spyro or Cynder to explore vast areas and collect items
    that allow each dragon to get stronger.
    """

    # You must override the "game" field to say the name of the game.
    game = "The Legend of Spyro: Dawn of the Dragon"

    # The WebWorld is a definition class that governs how this world will be displayed on the website.
    web = web_world.DotDWebWorld()

    # This is how we associate the options defined in our options.py with our world.
    options_dataclass = options.DotDOptions
    options: options.DotDOptions

    # Our world class must have a static location_name_to_id and item_name_to_id defined.
    # We define these in regions.py and items.py respectively, so we can just set them here.
    location_name_to_id = locations.LOCATION_NAME_TO_ID
    item_name_to_id = items.ITEM_NAME_TO_ID

    # There is always one region that the generator starts from & assumes you can always go back to.
    # This defaults to "Menu", but you can change it by overriding origin_region_name.
    origin_region_name = "Menu"

    # For chapter order shuffling
    chapter_order: list[str]


    # UniversalTracker Support
    ut_can_gen_without_yaml = True

    @staticmethod
    def interpret_slot_data(slot_data: dict[str, Any]) -> dict[str, Any]:
        return slot_data
    
    def generate_early(self):
        self.handle_ut_yamless(None)
        self.element_items: dict[str, str] = items.get_element_item_map(self)
    
    def handle_ut_yamless(self, slot_data: Optional[dict[str, Any]]) -> Optional[dict[str, Any]]:
        if not slot_data \
                and hasattr(self.multiworld, "re_gen_passthrough") \
                and isinstance(self.multiworld.re_gen_passthrough, dict) \
                and self.game in self.multiworld.re_gen_passthrough:
            slot_data = self.multiworld.re_gen_passthrough[self.game]

        if not slot_data:
            return None

        self.options.death_link.value = slot_data["death_link"]
        self.options.learn_fury.value = slot_data["learn_fury"]
        self.options.shuffled_elements.value = slot_data["shuffled_elements"]
        self.options.spyro_elements_handling.value = slot_data["spyro_elements_handling"]
        self.options.spyro_elements_handling.value = slot_data["cynder_elements_handling"]
        self.options.learn_to_climb.value = slot_data["learn_to_climb"]
        self.options.learn_to_wall_run = slot_data["learn_to_wall_run"]
        self.options.shuffle_chapter_order.value = slot_data["shuffle_chapter_order"]
        self.chapter_order = [str(x) for x in slot_data["chapter_order"]]

        return slot_data

    # Our world class must have certain functions ("steps") that get called during generation.
    # The main ones are: create_regions, set_rules, and create_items.
    # For better structure and readability, we put each of these into their own file.
    def create_regions(self) -> None:
        regions.create_and_connect_regions(self)
        locations.create_all_locations(self)
    
    def set_rules(self) -> None:
        rules.set_all_rules(self)
        self.multiworld.completion_condition[self.player] = \
            lambda state: state.has("Victory", self.player)
    
    def create_items(self) -> None:
        items.create_all_items(self)
        items.push_unshuffled_element_items(self)
        items.push_available_ability_items(self)

    # Our world class must also have a create_item function that can create any one of our items by name at any time.
    # We also put this in a different file, teh same one that create_items is in.
    def create_item(self, name: str) -> items.DotDItem:
        return items.create_item_with_correct_classification(self, name)
    
    # For features such as item links and panic-method start inventory, AP may ask your world to create an extra filler.
    # For this purpose, your world *must* have at least one infinitely repeatable item (usually filler).
    # You must override this function and return this infinitely repeatable item's name.
    # In our case, we define a function called get_random_filler_item_name for this purpose in our items.py
    def get_filler_item_name(self) -> str:
        return items.get_random_filler_item_name(self)
    
    # There may be data that the game client will need to modify the behavior of the game.
    # This is what slot_data exists for. Upon every client connection, the slot's slot_data is sent to the client.
    # slot_data is just a dictionary using basic types, tthat will be converted to json when sent to the client.
    def fill_slot_data(self) -> Mapping[str, Any]:
        # If you need access to the player's chosen options on the client side, there is a helper for that.
        slot_data = self.options.as_dict(
            "death_link",
            "shuffle_chapter_order",
            "shuffled_elements",
            "spyro_elements_handling",
            "cynder_elements_handling",
            "learn_to_climb",
            "learn_to_wall_run",
            "learn_fury"
        )

        slot_data["chapter_order"] = self.chapter_order

        return slot_data
    
    def write_spoiler_header(self, spoiler_handle):
        spoiler_handle.write(f"\nChapter Order ({self.multiworld.get_player_name(self.player)}):\n")
        for i, chapter in enumerate(self.chapter_order):
            spoiler_handle.write(f"  Chapter {i + 1}: {chapter}\n")