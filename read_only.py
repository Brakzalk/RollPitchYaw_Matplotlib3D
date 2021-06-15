from mpl_toolkits.mplot3d import Axes3D
import mpl_toolkits.mplot3d.art3d as art3d
import matplotlib.pyplot as plt
import numpy as np
from matplotlib.patches import Circle
#保存
import pickle



fig = pickle.load(open('myfigfile.p', 'rb'))
plt.show()
