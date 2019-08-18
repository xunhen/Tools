import os, sys
import numpy as np
import copy


class YoloTxtGenerator(object):
    def __init__(self, datasetPaths, recursive=True):
        if type(datasetPaths) is not list:
            datasetPaths = [datasetPaths, ]
        self.datasetPaths = datasetPaths
        self.recursive = recursive

    def startTask(self):
        datasetPaths = copy.deepcopy(self.datasetPaths)
        for datasetPath in datasetPaths:
            print('process path {} begin!!'.format(datasetPath))
            for filename in os.listdir(datasetPath):
                filenamePath = os.path.join(datasetPath, filename)
                if self.recursive and os.path.isdir(filenamePath):
                    datasetPaths.append(filenamePath)
                if os.path.isfile(filenamePath) and filename.endswith('.jpg'):
                    filename = filename[:-4]
                    bboxs = []
                    print('process image {} begin!!'.format(filename))
                    with open(os.path.join(datasetPath, filename + 'org.txt'), 'r') as file:
                        for line in file.readlines():
                            line = line.split(' ')
                            width = int(line[1])
                            height = int(line[2])
                            bboxs.append([int(line[3]), int(line[4]), int(line[5]), int(line[6]), int(line[0])])
                    with open(os.path.join(datasetPath, filename + '.txt'), 'w') as file:
                        for bbox in bboxs:
                            file.write(
                                "{} {} {} {} {}\n".format(bbox[-1], (bbox[0] + bbox[2] / 2) / width,
                                                          (bbox[1] + bbox[3] / 2) / height,
                                                          bbox[2] / width, bbox[3] / height))
                    print('process image {} end!!'.format(filename))
            print('process path {} end!!'.format(datasetPath))

if __name__ == '__main__':
    datasetPaths = [r'F:\PostGraduate\DataSet\overpass',]
    yoloTxtGenerator = YoloTxtGenerator(datasetPaths)
    yoloTxtGenerator.startTask()
