import imageio
from pathlib import Path
import os


image_path = Path()

images = list(image_path.glob('*.png'))
image_list = []
for file_name in images:
    image_list.append(imageio.imread(file_name))
    

# Cree le gif dans la racine du dossier
imageio.mimwrite('GifMap.gif', image_list, fps=1)
