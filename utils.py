def batting_average(singles, doubles, triples, homeruns, outs):
    if (singles + doubles + triples + homeruns + outs) == 0:
        return 0
    return ((singles + doubles + triples + homeruns) /
            (singles + doubles + triples + homeruns + outs))

def on_base_percentage(singles, doubles, triples, homeruns, walks, outs):
    if (singles + doubles + triples + homeruns + outs) == 0:
        return 0
    return ((singles + doubles + triples + homeruns + walks) /
            (singles + doubles + triples + homeruns + outs + walks))

def at_bats(singles, doubles, triples, homeruns, outs):
    return singles + doubles + triples + homeruns + outs

def plate_appearances(singles, doubles, triples, homeruns, walks, outs):
    return singles + doubles + triples + homeruns + outs + walks