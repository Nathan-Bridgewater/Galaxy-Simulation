from random import randint
from collections import Counter
import numpy as np
import matplotlib.pyplot as plt


NUM_EQUIV_VOLUMES = 1000  # Number of locations in which to place civilisations
MAX_CIVS = 5000  # maximum number of advanced civilisations
TRIALS = 1000  # Number of times to model a given number of civilisations
CIV_STEP_SIZE = 100  # civilisations count step size

x = []  # x values for polynomial
y = []  # y values for polynomial

# Loop through different number of possible civilisations in your galaxy
for num_civs in range(2, MAX_CIVS + 2, CIV_STEP_SIZE):
    civs_per_vol = num_civs / NUM_EQUIV_VOLUMES
    num_single_civs = 0

    # repeat the experiment 'TRIALS' number of times
    for trial in range(TRIALS):
        locations = []  # equivalent volumes containing a civilisation
        while len(locations) < num_civs:

            # Randomly select locations to place you civilisations
            location = randint(1, NUM_EQUIV_VOLUMES)
            locations.append(location)

        # count how many civs for each location and the frequency of the values
        overlap_count = Counter(locations)
        overlap_rollup = Counter(overlap_count.values())
        num_single_civs += overlap_rollup[1]

    # probability of multiple civilisations per location for current num of civs
    prob = 1 - (num_single_civs / (num_civs * TRIALS))

    # print ration of civs-per-volume vs probability of 2+ civs per location
    # print(f"{civs_per_vol:.4f}  {prob:.4f}")  # comment out to speed up
    x.append(civs_per_vol)
    y.append(prob)

print(x)
print(y)

coefficients = np.polyfit(x, y, 4)  # fourth order polynomial fit
p = np.poly1d(coefficients)
print(f"\n{p}")
xp = np.linspace(0, 5)
_ = plt.plot(x, y, '.', xp, p(xp), '-')
plt.ylim(-0.5, 1.5)
plt.show()
