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

class GoalCondition(Choice):
    """
    Sets what condition is required for your goal to trigger.

    Defeat Malefor: Defeat Malefor at his lair, which is always unlocked as the final chapter.

    Elite Hunter: Defeat a set number of elite enemies.

    Clear Chapters: Reach the end of a set number of chapters (excluding Malefor's Lair).
    """
    display_name = "Goal Condition"

    # == IDEAS FOR FUTURE GOAL CONDITIONS ==
    # Complete Chapters: Obtain every item in a set number of chapters. Reuses ClearChaptersThreshold class.
    # Reach Progress: Meet or beat a set amount of progress (out of 100) on your save file.
    
    option_defeat_malefor = 0
    option_elite_hunter = 1
    option_clear_chapters = 2
    # option_complete_chapters = 3
    # option_reach_progress = 4

    default = option_defeat_malefor


class EliteHunterThreshold(Range):
    """
    This is the number of Elite enemies you must defeat to trigger goal.
    NOTE: This option only works if your goal condition is set to Elite Hunter.
    """
    display_name = "Elite Hunter Threshold"

    range_start = 1
    range_end = 8

    default = 8


class ClearChaptersThreshold(Range):
    """
    This is the number of chapters you must clear to trigger goal.
    This number does not include Malefor's Lair
    NOTE: This option only works if your goal condition is set to Clear Chapters.
    """
    display_name = "Clear Chapters Threshold"

    range_start = 1
    range_end = 10

    default = 10


class AlwaysDefeatMalefor(Toggle):
    """
    If your goal condition is something other than "Defeat Malefor",
    reaching your goal requirements opens Malefor's Lair, and defeating him will trigger goal.
    
    Recommended for a more climactic victory condition or
    for appending Malefor's Lair to a run with a full 10 Clear Chapters goal.
    """
    display_name = "Always Defeat Malefor"


class LearnToClimb(Toggle):
    """
    Neither dragon can climb vines until it is enabled via the "Wall Climbing" item.
    This functionality extends to large objects that must be held onto and pulled with the chain.
    Examples of such objects include the raft in Valley of Avalar, the floodgate pistons in the Dam, and the hanging platforms in the Ruins of Warfang.
    """
    display_name = "Learn to Climb"


class LearnToWallRun(Toggle):
    """
    Neither dragon can run on walls until it is enabled via the "Wall Running" item.
    """
    display_name = "Learn to Wall Run"


class ShuffleChapterOrder(Toggle):
    """
    Chapters are unlocked in a random order with the exception of Malefor's Lair which is always unlocked last.
    """
    display_name = "Shuffle Chapter Order"


class BurnedLandsThreshold(Range):
    """
    Let's face it, we all hate the Burned Lands.
    This number is the number of chapters that are guaranteed to appear before Burned Lands.
    For example, setting this number to 0 means Burned Lands can appear in place of any chapter,
    but setting it to 8 means it can only be Chapter 9 or Chapter 10.
    This option has no effect if Shuffle Chapter Order is disabled, as Burned Lands is always Chapter 9 in vanilla.
    """
    display_name = "Burned Lands Threshold"

    range_start = 0
    range_end = 9
    default = 5


class ShuffledElements(OptionSet):
    """
    Any elements added to this set will be unusable until obtained via an item.
    Use the Spyro/Cynder Elements Handling options for finer control.
    """
    display_name = "Shuffled Elements"
    valid_keys = {"Fire", "Ice", "Earth", "Electricity", "Poison", "Shadow", "Fear", "Wind",}


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


class HyperEnemies(Toggle):
    """
    All enemies (including Elite Enemies) will move and attack twice as fast. Does not apply to bosses.
    """
    display_name = "Hyper Enemies"

    
class EnemyHealth(Choice):
    """
    Enemies will have more or less health depending on this option. Does not apply to Elite Enemies and bosses.

    Normal: Enemies will spawn with their normal base health, like in Story Mode.

    Half: Enemies will spawn with half of their base health, so they will be easier to kill.

    Double: Enemies will spawn with double their base health. In vanilla, enemies have double health in Chapter Mode.
    """
    display_name = "Enemy Health"

    option_normal = 0
    option_half = 1
    option_double = 2

    default = option_normal
    

class RandomEliteElements(Choice):
    """
    All 8 Elite Enemies will have the element required to break their masks randomized, with the color of the mask matching the newly randomized element.

    Disabled: Elites will keep their vanilla elements and masks.

    Random Normal: Elites will have a random element for each of their possible masks, with no duplicates.
    This means that Elites that had 2 or 3 possible elements in vanilla will have 2 or 3 different random possible elements.

    Random Unique: Each Elite will have their own unique element. All 8 normal elements will be required to defeat all Elite Enemies.
    """
    display_name = "Random Elite Elements"

    option_disabled = 0
    option_random_normal = 1
    option_random_unique = 2

    default = option_disabled


class FewerEliteElementRequirements(Toggle):
    """
    Normally, logic expects that you have ALL of an Elite's elements to beat it (so you don't have to reroll the mask).
    This makes it so only one of the elements is logically required to beat an Elite.
    It might be necessary to respawn the Elite a few times, since which mask the Elite uses is determined by RNG.
    Elites with 2 masks have a 2/3 chance to spawn with the first and a 1/3 chance to spawn with the second.
    Elites with 3 masks have an equal chance to spawn with any mask.
    """
    display_name = "Fewer Elite Element Requirements"


class FixBrokenArmors(DefaultOnToggle):
    """
    Fix Spyro's Silver Helmet and Cynder's Silver Tail, which do not work in vanilla.
    Spyro's Silver Helmet will increase his melee damage by 20%.
    Cynder's Silver Tail will increase her melee attack speed by 20%.
    """
    display_name = "Fix Broken Armors"

class SpawnWithFullRestore(DefaultOnToggle):
    """
    Whenever you enter a new level from the menu,
    both dragons will spawn with full HP/Mana.
    """
    display_name = "Spawn With Full Restore"


# We must now define a dataclass inheriting from PerGameCommonOptions that we put all our options in.
# This is in the format "option_name_in_snake_case: OptionClassName"
@dataclass
class DotDOptions(DeathLinkMixin, PerGameCommonOptions):
    goal_condition: GoalCondition
    elite_hunter_threshold: EliteHunterThreshold
    clear_chapters_threshold: ClearChaptersThreshold
    always_defeat_malefor: AlwaysDefeatMalefor
    shuffle_chapter_order: ShuffleChapterOrder
    burned_lands_threshold: BurnedLandsThreshold
    shuffled_elements: ShuffledElements
    spyro_elements_handling: SpyroElementsHandling
    cynder_elements_handling: CynderElementsHandling
    learn_to_climb: LearnToClimb
    learn_to_wall_run: LearnToWallRun
    learn_fury: LearnFury
    hyper_enemies: HyperEnemies
    enemy_health: EnemyHealth
    random_elite_elements: RandomEliteElements
    fewer_elite_element_requirements: FewerEliteElementRequirements
    fix_broken_armors: FixBrokenArmors
    spawn_with_full_restore: SpawnWithFullRestore


# If we want to group our options by similar type we can do so as well. This looks nice on the website.
dotd_option_groups: list[OptionGroup] = [
    OptionGroup(
        "Goal Options",
        [
            GoalCondition,
            EliteHunterThreshold,
            ClearChaptersThreshold,
            AlwaysDefeatMalefor
        ]
    ),
    OptionGroup(
        "Level Options",
        [
            ShuffleChapterOrder,
            BurnedLandsThreshold
        ]
    ),
    OptionGroup(
        "Logic Options",
        [
            FewerEliteElementRequirements
        ]
    ),
    OptionGroup(
        "Item Options",
        [
            ShuffledElements,
            SpyroElementsHandling,
            CynderElementsHandling,
            LearnToClimb,
            LearnToWallRun,
            LearnFury
        ]
    ),
    OptionGroup(
        "Enemy Options",
        [
            HyperEnemies,
            EnemyHealth,
            RandomEliteElements
        ]
    ),
    OptionGroup(
        "Enhancements",
        [
            FixBrokenArmors,
            SpawnWithFullRestore
        ]
    )
]

# We can also define presets (dict of "option_name_in_snake_case": DefaultValue)