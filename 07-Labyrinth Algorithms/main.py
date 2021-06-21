import matplotlib.pyplot as plt
import matplotlib.cm as cm
from base import RecursiveBacktracking

maze1       = RecursiveBacktracking(10,10); maze1.gen();
maze2       = RecursiveBacktracking(25,25); maze2.gen();
maze3       = RecursiveBacktracking(50,50); maze3.gen();
maze4       = RecursiveBacktracking(99,99); maze4.gen();
fig, axes   = plt.subplots(2, 2)

axes[0,0].imshow(maze1.maze, cmap = cm.Greys_r)
axes[0,0].set_title(f"{maze1.mH}x{maze1.mW} @ {maze1.GenTime:.3f} secs")
axes[0,0].axis('off')

axes[0,1].imshow(maze2.maze, cmap = cm.Greys_r)
axes[0,1].set_title(f"{maze2.mH}x{maze2.mW} @ {maze2.GenTime:.3f} secs")
axes[0,1].axis('off')

axes[1,0].imshow(maze3.maze, cmap = cm.Greys_r)
axes[1,0].set_title(f"{maze3.mH}x{maze3.mW} @ {maze3.GenTime:.3f} secs")
axes[1,0].axis('off')

axes[1,1].imshow(maze4.maze, cmap = cm.Greys_r)
axes[1,1].set_title(f"{maze4.mH}x{maze4.mW} @ {maze4.GenTime:.3f} secs")
axes[1,1].axis('off')

plt.show()
