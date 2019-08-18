import os, sys
import cv2
import numpy as np
import copy


class VideoSampler(object):
    def __init__(self, videoFileNamesOrPath, savePath=None, sampleRatio=1, start_index=0, prefix='GJ'):
        if type(videoFileNamesOrPath) is str:
            if not videoFileNamesOrPath.endswith('.mp4'):
                self.videoFileNames = []
                for videoFileName in os.listdir(videoFileNamesOrPath):
                    if videoFileName.endswith('.mp4'):
                        self.videoFileNames.append(os.path.join(videoFileNamesOrPath, videoFileName))
            else:
                self.videoFileNames = [videoFileNamesOrPath, ]
        else:
            self.videoFileNames = videoFileNamesOrPath
        self.savePath = savePath
        self.sampleRatio = sampleRatio
        self.start_index = start_index
        self.prefix = prefix
        pass

    def startTask(self):
        for videoFileName in self.videoFileNames:
            savePath = os.path.join(self.savePath, videoFileName[:-4])
            if not os.path.exists(savePath):
                os.makedirs(savePath)
            imageFile = os.path.join(savePath, self.prefix + '{}.jpg')
            cap = cv2.VideoCapture(videoFileName)
            fps = cap.get(cv2.CAP_PROP_FPS)
            framePerSeconde = int(fps * self.sampleRatio)
            index = -1
            while cap.isOpened():
                index += 1
                ret, frame = cap.read()  # 读取帧
                if not ret:
                    break
                if (index % framePerSeconde) != 0:
                    continue
                cv2.imwrite(imageFile.format(self.start_index), frame)
                print("generate image: ", self.start_index)
                self.start_index += 1


if __name__ == '__main__':
    videoFileName = r'F:\PostGraduate\DataSet\Video\overpass\DS620190420170000_20190420180000_20190420202252.mp4'
    savePath = r'F:\PostGraduate\DataSet\Video\overpass'
    videoSampler = VideoSampler(videoFileName, savePath, sampleRatio=5, start_index=0)
    videoSampler.startTask()
    pass
