def map_classes():
    classes = '''Dresses Tops Jeans Skirts Rompers Shoes Bags Jewelry Swimwear Intimates Others'''.split()

    class_to_idx = {}
    idx = 0

    for c in classes:
        class_to_idx[c] = idx
        idx += 1

    return class_to_idx