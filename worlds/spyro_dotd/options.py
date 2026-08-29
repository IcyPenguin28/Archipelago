from dataclasses import dataclass, field

from Options import Choice, OptionGroup, PerGameCommonOptions, DeathLinkMixin, Range, Toggle, OptionSet, DefaultOnToggle

# In this file we define the options the player can pick.
# The most common types of options are Toggle, Range, and Choice.

# Options will be in the game's template yaml.
# They will be represented by checkboxes, sliders etc. on the game's options page on the website.
# NOTE: Options can also be made invisible from either of these places by overriding Option.visibility
# APQuest doesn't have an example of this, but this can be used for secret/hidden/advanced options.

# For further reading on options, you can also read the Options API Document

# The first type of Option we'll discuss is the Toggle.
# A toggle is an option that can either be on or off. This will be represented by a checkbox on the website.
# The default for a toggle is "off".
# If you want a toggle to be on by default, you can use the "DefaultOnToggle" class instead of teh "Toggle" class.
class DisableCheatCodes(DefaultOnToggle):
    """
    Disable the ability to make use of in-game cheat codes for things like
    infinite health, infinite mana, infinite exp, or infinite fury
    """
    display_name = "Disable In-Game Cheat Codes"


class LearnToFly(Toggle):
    """
    Neither dragon can fly until it is enabled via the "Dragons' Flight" item.
    This does not disable flight that would otherwise be required to stop from falling into bottomless pits.
    WARNING: There is a chance to softlock yourself if you fall somewhere that cannot fly out of.
    """
    display_name = "Learn to Fly"


class LearnToClimb(Toggle):
    """
    Neither dragon can climb vines until it is enabled via the "Wall Climbing" item.
    """
    display_name = "Learn to Climb"


class LearnToWallRun(Toggle):
    """
    Neither dragon can run on walls until it is enabled via the "Wall Running" item.
    """
    display_name = "Learn to Wall Run"


class LearnToBreathe(Choice):
    """
    One or both dragons cannot use mana until it is enabled via an item.
    
    Disabled: Both dragons can replenish their mana (vanilla behavior).

    Spyro: Spyro will always have 0 mana until the "Spyro's Elements" item is obtained. Cynder remains unaffected.

    Cynder: Cynder will always have 0 mana until the "Cynder's Elements" item is obtained. Spyro remains unaffected.

    Both Together: Both dragons will always have 0 mana until the "Dragons' Elements" item is obtained.

    Both Separate: Both dragons will always have 0 mana and can re-obtain them separately with the "Spyro's Elements" and "Cynder's Elements" items.
    """
    display_name = "Learn to Breathe"

    option_disabled = 0
    option_spyro = 1
    option_cynder = 2
    option_both_together = 3
    option_both_separate = 4

    default = option_disabled


class ShuffleChapterOrder(Toggle):
    """
    Chapters are unlocked in a random order with the exception of Malefor's Lair which is always unlocked last.
    """
    display_name = "Shuffle Chapter Order"


class ShuffledElements(OptionSet):
    """
    Any elements added to this set will be unselectable until obtained via an item.
    Fire and Poison are unsupported by this feature due to a lack of checks prior to their use in the Catacombs.
    Use the Spyro/Cynder Elements Handling options for finer control.
    """
    display_name = "Shuffled Elements"
    valid_keys = {"Electricity", "Ice", "Earth", "Fear", "Wind", "Shadow"}


class SpyroElementsHandling(Choice):
    """
    Determines how to group Spyro's shuffled elements (Fire/Electricity/Ice/Earth).
    This option has no effect if none of Spyro's elements are present in Shuffled Elements.

    Individual: Each shuffled element that belongs to Spyro is its own item.

    All At Once: Every shuffled element that belongs to Spyro is obtained via the "Spyro's Elements" item.
    """
    display_name = "Spyro Elements Handling"
    
    option_individual = 0
    option_all_at_once = 1

    default = option_individual


class CynderElementsHandling(Choice):
    """
    Determines how to group Cynder's shuffled elements (Poison/Fear/Wind/Shadow).
    This option has no effect if none of Cynder's elements are present in Shuffled Elements.

    Individual: Each shuffled element that belongs to Cynder is its own item.

    All At Once: Every shuffled element that belongs to Cynder is obtained via the "Cynder's Elements" item.
    """
    display_name = "Cynder Elements Handling"

    option_individual = 0
    option_all_at_once = 1

    default = option_individual


class LearnFury(Choice):
    """
    One or both dragons cannot build the fury bar until it is enabled via an item.
    Use of fury breath via the Fury Armor's Set Bonus remains unaffected.
    Fury is required to pass phase 3 of the Malefor final boss fight.

    Disabled: Both dragons can build the fury bar (vanilla behavior).

    Spyro: Spyro cannot build fury until the "Spyro's Fury" item is obtained. Cynder remains unaffected.

    Cynder: Cynder cannot build fury until the "Cynder's Fury" item is obtained. Spyro remains unaffected.

    Both Together: Both dragons will not be able to build fury until the "Dragons' Fury" item is obtained.

    Both Separate: Both dragons will not be able to build fury and can re-obtain them separately with the "Spyro's Fury" and "Cynder's Fury" items.
    """
    display_name = "Learn Fury"

    option_disabled = 0
    option_spyro = 1
    option_cynder = 2
    option_both_together = 3
    option_both_separate = 4

    default = option_disabled


# We must now define a dataclass inheriting from PerGameCommonOptions that we put all our options in.
# This is in the format "option_name_in_snake_case: OptionClassName"
@dataclass
class DotDOptions(DeathLinkMixin, PerGameCommonOptions):
    # disable_cheat_codes: DisableCheatCodes
    # learn_to_fly: LearnToFly
    # learn_to_climb: LearnToClimb
    # learn_to_wall_run: LearnToWallRun
    # learn_to_breathe: LearnToBreathe
    shuffle_chapter_order: ShuffleChapterOrder
    shuffled_elements: ShuffledElements
    spyro_elements_handling: SpyroElementsHandling
    cynder_elements_handling: CynderElementsHandling
    learn_fury: LearnFury
    

# If we want to group our optionps by similar type we can do so as well. This looks nice on the website.

# We can also define presets (dict of "option_name_in_snake_case": DefaultValue)