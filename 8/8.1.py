from collections import Counter


def create_layer(data, width, height):
    images = []
    ptr = 0
    current_layer = []

    while ptr < len(data):
        for _ in range(height):
            current_layer.append(data[ptr:ptr+width])
            ptr += width
        images.append(current_layer)
        current_layer = []

    return images


def count_layer(layer):
    c = Counter()

    for row in layer:
        c.update(row)

    return c


layers = create_layer(open('../data/8.txt').read().rstrip(), 25, 6)

fewest_zero_layer = None
fewest_zero_count = float('inf')
fewest_zero_counter = None
for layer in layers:
    counter = count_layer(layer)
    if counter.get('0') < fewest_zero_count:
        fewest_zero_count = counter.get('0')
        fewest_zero_layer = layer
        fewest_zero_counter = counter

print(fewest_zero_counter.get('1') * fewest_zero_counter.get('2'))