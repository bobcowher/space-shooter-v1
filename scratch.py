directions = []

for i in range(360):
    directions.append(i+1)


raw_input_counter = 0

while True:
    raw_input_counter -= 10
    direction = raw_input_counter % 360
    print(direction)
    