def calculate_pb(level: int) -> int:
    if level > 16:
        return 6
    elif level > 12:
        return 5
    elif level > 8:
        return 4
    elif level > 4:
        return 3
    else:
        return 2
def get_hit_dice(character_class: str) -> int:
    match character_class.lower():
        case "barbarian":
            return 12
        case "fighter" | "paladin" | "ranger":
            return 10
        case "bard" | "cleric" | "druid" | "monk" | "rogue" | "warlock" | "artificer":
            return 8
        case "sorcerer" | "wizard":
            return 6
        case _:
            raise ValueError(f"Unknown class: {character_class}")