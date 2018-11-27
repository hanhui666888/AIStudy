import numpy as np
import pylab as pl
import random as rd
import imageio

# 计算平面两点的欧氏距离
step = 0
color = ['.r', '.g', '.b', '.y']  # 颜色种类
dcolor = ['*r', '*g', '*b', '*y']  # 颜色种类
frames = []

#def distance(a, b):
#    return (a[0] - b[0]) ** 2 + (a[1] - b[1]) ** 2

def distance(a, b, d):
    sum = 0;
    for i in range(d):
        sum = sum + (a[i] - b[i]) ** 2
    return sum


# K均值算法
def k_means(x, y, k_count):
    count = len(x)  # 点的个数
    # 随机选择K个点
    k = rd.sample(range(count), k_count)
    k_point = [  [  x[i], [  y[i]  ]  ] for i in k ]  # 保证有序
    k_point.sort()
    global frames
    global step
    while True:
        km = [[] for i in range(k_count)]  # 存储每个簇的索引
        # 遍历所有点
        for i in range(count):
            cp = [x[i], y[i]]  # 当前点
            # 计算cp点到所有质心的距离
            _sse = [distance(k_point[j], cp, 2) for j in range(k_count)]
            # cp点到那个质心最近
            min_index = _sse.index(min(_sse))
            # 把cp点并入第i簇
            km[min_index].append(i)
        # 更换质心
        step += 1
        k_new = []
        for i in range(k_count):
            _x = sum([x[j] for j in km[i]]) / len(km[i])
            _y = sum([y[j] for j in km[i]]) / len(km[i])
            k_new.append([_x, _y])
        k_new.sort()  # 排序

        # 使用Matplotlab画图
        pl.figure()
        pl.title("N=%d,k=%d  iteration:%d" % (count, k_count, step))
        for j in range(k_count):
            pl.plot([x[i] for i in km[j]], [y[i] for i in km[j]], color[j % 4])
            pl.plot(k_point[j][0], k_point[j][1], dcolor[j % 4])
        pl.savefig("1.jpg")
        frames.append(imageio.imread('1.jpg'))
        if (k_new != k_point):  # 一直循环直到聚类中心没有变化
            k_point = k_new
        else:
            return km

#生成随机点列表
def randomPointList(xstart,xend,ystart,yend,count):
    randomList = []
    for i in range(count):
        randomList.append([rd.uniform(xstart,xend),rd.uniform(ystart, yend)])
    return randomList

list1 = np.vstack((randomPointList(0,20,0,20,50),randomPointList(0,20,40,60,50)))
list2 = np.vstack((randomPointList(40,60,0,20,50),randomPointList(40,60,40,60,50)))
list = np.vstack((list1,list2))
list = list[rd.sample(range(200),200)] #打乱数组顺序
print(list)

x = []
y = []
for j in range(200):
    x.append(list[j][0])
    y.append(list[j][1])


#x, y = np.loadtxt('2.csv', delimiter=',', unpack=True)
k_count = 2
km = k_means(x, y, k_count)
print(step)
imageio.mimsave('k-means.gif', frames, 'GIF' ,duration=0.5)