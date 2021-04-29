import random
import time

scale_fingerboard = [
    ['E', 'F', 'F#', 'G', 'G#', 'A', 'A#', 'B', 'C', 'C#', 'D', 'D#'],         # High e
    ['B', 'C', 'C#', 'D', 'D#', 'E', 'F', 'F#', 'G', 'G#', 'A', 'A#'],         # B String
    ['G', 'G#', 'A', 'A#', 'B', 'C', 'C#', 'D', 'D#', 'E', 'F', 'F#'],         # G String
    ['D', 'D#', 'E', 'F', 'F#', 'G', 'G#', 'A', 'A#', 'B', 'C', 'C#'],         # D String
    ['A', 'A#', 'B', 'C', 'C#', 'D', 'D#', 'E', 'F', 'F#', 'G', 'G#'],         # A String
    ['E', 'F', 'F#', 'G', 'G#', 'A', 'A#', 'B', 'C', 'C#', 'D', 'D#'],         # E String
]

amount = 0
amount_time = 0
your_answer = False
count = 0
right = 0

while True:

    string = random.randrange(0, 6)
    step = random.randrange(0, 12)
    count += 1

    while True:
        tic = time.time()
        print('Question No.' + str(amount) + ':' + str(string + 1) + 'String', end='')

        if step == 0:
            a = input('Open String note is :')
        else:
            a = input(str(step) + 'Fret has name:')
        if a == scale_fingerboard[string][step]:
            toc = time.time()
            print('Correct answer! You spent %.2fs' % (toc - tic))
            amount_time += toc - tic
            amount += 1
            right += 1
            break
        else:
            amount += 1
            print("Wrong Answer! Please Answer Again")

    print('You took %d questions, and had %d questions correct. Correct Rate is %2.2f and average time for correct answer is  %.2fs\n'
          % (amount, right, right / amount * 100, amount_time / right))
