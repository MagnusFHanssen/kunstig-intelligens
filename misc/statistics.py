import random


def stat_array():
    stats = []
    while len(stats) < 6:
        rolls = []
        while len(rolls) < 4:
            rolls.append(random.randrange(1, 7))
        rolls.sort(reverse=True)
        stats.append(sum(rolls[0:-1]))
    return stats


print(stat_array())

exit()
