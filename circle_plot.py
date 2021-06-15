from mpl_toolkits.mplot3d import Axes3D
import mpl_toolkits.mplot3d.art3d as art3d
import matplotlib.pyplot as plt
import numpy as np
from matplotlib.patches import Circle
#保存
import pickle

#アニメーション表示
from IPython.display import HTML
import matplotlib.animation as animation

#FLASK
from flask import Flask, render_template, make_response
from io import BytesIO
import urllib
from matplotlib.backends.backend_agg import FigureCanvasAgg
from matplotlib.figure import Figure


#設定
fig=plt.figure(figsize=(6,6),dpi=150)
ax = fig.gca(projection='3d')



def RollPitchYaw(x,y,z, rx,ry,rz):
    '''
    input
        回転角度x
        回転角度y
        回転角度z
    output
        回転行列
    '''
    X = x
    Y = y
    Z = z
    # # rotate the samples by pi / 4 radians around y
    # a = np.pi / 4
    # t = np.transpose(np.array([X,Y,Z]), (1,2,0))
    # m = [[np.cos(a), 0, np.sin(a)],[0,1,0],[-np.sin(a), 0, np.cos(a)]]
    # X,Y,Z = np.transpose(np.dot(t, m), (2,0,1))

    # 物体座標系の 1->2->3 軸で回転させる
    t = np.transpose(np.array([X,Y,Z]), (1,2,0))
    Rx = np.array([[1, 0, 0],
                   [0, np.cos(rx), np.sin(rx)],
                   [0, -np.sin(rx), np.cos(rx)]])
    X,Y,Z = np.transpose(np.dot(t, Rx), (2,0,1))


    t = np.transpose(np.array([X,Y,Z]), (1,2,0))
    Ry = np.array([[np.cos(ry), 0, -np.sin(ry)],
                   [0, 1, 0],
                   [np.sin(ry), 0, np.cos(ry)]])
    X,Y,Z = np.transpose(np.dot(t, Ry), (2,0,1))

    t = np.transpose(np.array([X,Y,Z]), (1,2,0))
    Rz = np.array([[np.cos(rz), np.sin(rz), 0],
                   [-np.sin(rz), np.cos(rz), 0],
                   [0, 0, 1]])
    X,Y,Z = np.transpose(np.dot(t, Rz), (2,0,1))
    # R = Rz.dot(Ry).dot(Rx)#積を求める
    return X,Y,Z


def circle_tower(origin = (0,0,0), r = 1, h = 1, rpy = (0.0, 0.0, 0.0)):
    '''
    円柱を作る
    input
        座標
        半径
        高さ
    '''
    #円周作成
    z = np.linspace(0, h, 100)#-5~5までの値を100個区切る
    theta = np.linspace(0, 2*np.pi, 100)#0~3.14*2の値を100個区切る
    Theta, Z=np.meshgrid(theta, z)
    X = r*np.cos(Theta)
    Y = r*np.sin(Theta)

    X,Y,Z = RollPitchYaw(X,Y,Z, rpy[0], rpy[1], rpy[2])#回転
    ax.plot_surface(X+origin[0], Y+origin[1], Z+origin[2], color='b',alpha=1.0)



#本体
circle_tower(origin=(0,0,0), r=2, h=10, rpy=(0.0, 0.0, 0.0))
#屋根
# circle_tower(origin=(0,0,10), r=1.5, h=1, rpy=(0.0, 0.0, 0.0))
# circle_tower(origin=(0,0,11), r=1.0, h=1, rpy=(0.0, 0.0, 0.0))
# circle_tower(origin=(0,0,12), r=0.5, h=1, rpy=(0.0, 0.0, 0.0))
# circle_tower(origin=(0,0,13), r=0.2, h=1, rpy=(0.0, 0.0, 0.0))

#枝
circle_tower(origin=(0,-2,5), r=0.5, h=5, rpy=(np.pi/4, 0.0, 0.0))
circle_tower(origin=(0,-2,5), r=0.5, h=5, rpy=(np.pi/2, 0.0, np.pi/4))
circle_tower(origin=(0,-2,5), r=0.5, h=5, rpy=(np.pi/2, 0.0, -np.pi/4))
circle_tower(origin=(0,-2,5), r=0.5, h=5, rpy=(3*np.pi/4, 0.0, 0.0))

circle_tower(origin=(0.0, 4.5, 7.5), r=0.5, h=2.5, rpy=(np.pi/2, 0.0, 0.0))
circle_tower(origin=(0.0, 4.5, 5.0), r=0.5, h=2.5, rpy=(0.0, 0.0, 0.0))
circle_tower(origin=(0.0, 7.0, 5.0), r=0.5, h=2.5, rpy=(np.pi/2, 0.0, 0.0))


# circle_tower(origin=(0,-3,0), r=1, h=2, rpy=(np.pi/2, 0.0, 0.0))
#circle_tower(origin=(-3,0,0), r=1, h=2, rpy=(0.0, np.pi/2, 0.0))


ax.set_xlabel('x axis')
ax.set_ylabel('y axis')
ax.set_zlabel('z axis')
ax.set_xlim(-5,5)
ax.set_ylim(-5,5)
ax.set_zlim(0,10)
ax.set_box_aspect((1,1,1))
fig.savefig("enchu_2.png", dpi=130)
f = open('myfigfile.p','wb')
pickle.dump(fig, f)
f.close

plt.show()



def init():
    #ax.plot_wireframe(X, Y, Z, rcount=12, ccount=12)
    return fig,

def animate(i):
    ax.view_init(elev=45., azim=3.6*2*i)#2週する
    return fig,

# # Animate
# ani = animation.FuncAnimation(fig, animate, init_func=init,
#                                frames=100, interval=100, blit=True)
# ani.save('rotate_3dwf.mp4', writer="ffmpeg",dpi=100)
# HTML(ani.to_html5_video())

#Web
app = Flask(__name__)
@app.route('/')
def index():
    canvas = FigureCanvasAgg(fig)
    png_output = BytesIO()
    canvas.print_png(png_output)
    data = png_output.getvalue()

    response = make_response(data)
    response.headers['Content-Type'] = 'image/png'

    return response


if __name__ == "__main__":
  app.run()
