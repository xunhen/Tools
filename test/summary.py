import os, sys


def summary(path, path_to,name):
    with open(path + name, 'w') as file:
        number = 0
        for i in os.listdir(path):
            if i.endswith('.jpg'):
                file.write(os.path.join(path_to, '{}'.format(i)) + '\n')
                number += 1
        print(number)

    pass


if __name__ == '__main__':
    path = [r'F:\PostGraduate\DataSet\GJ\JamPic_part1\\', r'F:\PostGraduate\DataSet\GJ\overpass\\']
    path_to=[r'D:\Yolo3CUDA10-overpass\overpass\train\\',r'D:\Yolo3CUDA10-overpass\overpass\test\\']
    name = ['train.txt', 'val.txt']
    for i in range(len(path)):
        summary(path[i], path_to[i],name[i])
    pass
