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

layers = create_layer(open('../data/8.txt').read().rstrip(), 25, 6)

print(layers)

image = []

for _ in range(6):
    image.append([2] * 25)

for layer in layers:
    for i, row in enumerate(layer):
        for j, col in enumerate(row):
            if image[i][j] == 2:
                image[i][j] = int(col)

print(image)

for r in image:
    for c in r:
        if c == 1:
            print("=", end=" ")
        elif c == 0:
            print(" ", end=" ")
    print("\n")