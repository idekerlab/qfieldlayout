import glob
import matplotlib.pyplot as plt
import matplotlib.image as mpimg
import os

cwd = os.getcwd()
path = os.path.join(cwd, "test_evolution_networks/*.png")

images = [mpimg.imread(image_path) for image_path in glob.glob(path)]
height = 3
width = height * len(images) +1 * 1.1
fig = plt.figure(figsize=(width, height))

for i in range(1, len(images)):
    ax = plt.subplot(1, len(images)+1, i+1)
    imgplot = plt.imshow(images[i])
    ax.set_title(f'Step {i+1}')
#    image = plt.imread()
#    ax[i].imshow(image)

