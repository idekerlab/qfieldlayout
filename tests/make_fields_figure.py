from qfieldlayout.qfigures import save_field_figure, save_field_figure_3d
import matplotlib.pyplot as plt
from matplotlib.image import imread

save_field_figure(filename="field_figure", r_scale=20, a_scale=20)
save_field_figure_3d(filename="field_figure_3d", r_scale=20, a_scale=20)

# Load the two PNG images
img1 = imread('field_figure.png')
img2 = imread('field_figure_3d.png')

# Set the desired width in inches
width = 4.0

# Calculate the height of the first image to preserve its aspect ratio
height1 = img1.shape[0] * width / img1.shape[1]

# Calculate the height of the second image to preserve its aspect ratio
height2 = img2.shape[0] * width / img2.shape[1]

# Create a figure with two subplots of equal size
fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(width * 2, max(height1, height2)))

# Display the first image in the first subplot
ax1.imshow(img1)
ax1.axis('off')

# Display the second image in the second subplot
ax2.imshow(img2)
ax2.axis('off')

# Add labels to the left of each image
ax1.text(-0.0, 0.5, 'A.', transform=ax1.transAxes, va='center', ha='right', fontsize=10)
ax2.text(-0.0, 0.5, 'B.', transform=ax2.transAxes, va='center', ha='right', fontsize=10)

# Adjust the layout and padding between subplots
fig.tight_layout(pad=0.0)

# Save the figure as a PNG file with the desired DPI
dpi = 300
plt.savefig('combined_fields_figure.png', dpi=dpi)

# Show the figure (optional)
#plt.show()
