# Eine Methode zur Bestimmung von pi ist die statistische Methode. Für die Berechnung lässt man zufällige Punkte auf
# ein Quadrat „regnen“ und berechnet, ob sie innerhalb oder außerhalb eines einbeschriebenen Kreises liegen. Der
# Anteil der innen liegenden Punkte ist approximiert pi/4
#
# Diese Methode ist ein Monte-Carlo-Algorithmus; die Genauigkeit der nach einer festen Schrittzahl erreichten Näherung
# von pi lässt sich daher nur mit einer Irrtumswahrscheinlichkeit angeben. Durch das Gesetz der großen Zahlen steigt
# jedoch im Mittel die Genauigkeit mit der Schrittzahl.

import random
import math
import multiprocessing


def calc_num_points_inside_circle(start, end, return_values: dict):
    num_inside_drops = 0  # Zählt die Tropfen innerhalb des Kreises

    for i in range(start, end):  # So oft wiederholen, wie es Tropfen gibt
        x = random.random()
        y = random.random()
        if x * x + y * y <= 1.0:
            num_inside_drops += 1

    return_values[len(return_values)] = num_inside_drops


def approx_pi(num_random_points):
    print("Berechnung auf 1 Rechen-Kern")

    num_points_inside = dict()
    calc_num_points_inside_circle(0, int(num_random_points), num_points_inside)
    return 4 * num_points_inside[0] / num_random_points


def approx_pi_multi_threaded(num_random_points, num_threads):
    print("Berechnung auf " + str(num_threads) + " Rechen-Kernen")

    multiproc_manager = multiprocessing.Manager()
    return_dict = multiproc_manager.dict()
    jobs = []

    intervall = int(num_random_points / num_threads)
    for i in range(0, num_threads):
        p = multiprocessing.Process(target=calc_num_points_inside_circle, args=(i * intervall,
                                                                                i * intervall + intervall,
                                                                                return_dict))
        jobs.append(p)
        p.start()

    for proc in jobs:
        proc.join()

    num_inside_drops_cnt = 0
    for i in range(0, len(return_dict)):
        num_inside_drops_cnt += return_dict[i]

    return 4.0 * num_inside_drops_cnt / num_random_points


if __name__ == '__main__':
    num_drops = 1e8
    pi_approx = approx_pi_multi_threaded(num_drops, multiprocessing.cpu_count())
    #pi_approx = approx_pi(num_drops)
    print("Mit: " + str(num_drops) + " Zufallspunkten ist die Differenz zu Pi: " + str(math.pi - pi_approx))
