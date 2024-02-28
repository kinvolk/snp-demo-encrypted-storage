from itertools import permutations
import random
import string
import csv

with open('df.csv', 'w', newline='') as file:
    writer = csv.writer(file)

    field = ["description", "secret"]

    writer.writerow(field)

    for group in permutations(['found', 'glasses', 'she', 'sun', 'they', 'her', 'looking', 'else', 'somewhere', 'were', 'while']):
        p = ' '.join(group)

        rnd_secret = ''.join(random.choices(string.ascii_letters, k=10))

        # add a not so random secret
        if p == "she found her sun glasses while they were looking somewhere else":
            rnd_secret = "verysecret"

        writer.writerow([p, rnd_secret])
