import py_cartes_io as cartes
import numpy as np
markers = cartes.Maps(
    '048eebe4-8dac-46e2-a947-50b6b8062fec').markers().get()
# print(markers[0])
# Get the most common category of markers
categories = []
for marker in markers:
    categories.append(marker['category_id'])
categories = np.array(categories)

print(categories)
