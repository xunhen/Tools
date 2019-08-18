import os, sys
import cv2
import numpy as np
import copy

scales = [1, 4.0 / 5, 3.0 / 4, 2.0 / 3, 1.0 / 2]
scale_height_param = [450, 550, 650]
scale_offset_param = [60, -60]
scale_ratio = 1.5
center = (1225, 756)

bbox_black_threshold = 0.5


# 多尺度截图
def multi_scale_height(image_path, image_name, save_path):
    image = cv2.imread(image_path + image_name + '.jpg')
    bboxs_org = []

    with open(image_path + image_name + 'org.txt') as file:
        for line in file.readlines():
            line = line.split(' ')
            width = int(line[1])
            height = int(line[2])
            bboxs_org.append([int(line[3]), int(line[4]), int(line[5]), int(line[6])])
    for index, scale_width in enumerate(scale_height_param):
        for index_offset, offset in enumerate(scale_offset_param):
            rect_height = int(scale_width / 2)
            rect_width = int(scale_width * scale_ratio / 2)
            bboxs = copy.deepcopy(bboxs_org)
            x1 = max(0, center[0] - rect_width + offset)
            x2 = min(width, center[0] + rect_width + offset)
            y1 = max(0, center[1] - rect_height + offset)
            y2 = min(height, center[1] + rect_height + offset)
            rect_height = y2 - y1
            rect_width = x2 - x1
            for i in range(len(bboxs)):
                bboxs[i][0] = max(bboxs[i][0] - x1, 0)
                bboxs[i][1] = max(bboxs[i][1] - y1, 0)
            image_scale = image[y1:y2, x1:x2, :]
            image_scale_copy = copy.deepcopy(image_scale)
            with open(save_path + "//{}-{}-{}.txt".format(image_name, index, index_offset), 'w') as txt:
                with open(save_path + "//{}-{}-{}org.txt".format(image_name, index, index_offset), 'w') as orgtxt:
                    for i in range(len(bboxs)):
                        if bboxs[i][0] <= 0 or bboxs[i][1] <= 0 or bboxs[i][0] + bboxs[i][2] >= rect_width \
                                or bboxs[i][1] + bboxs[i][3] >= rect_height:
                            drawBlack(image_scale_copy, (rect_width, rect_height), bboxs[i])
                            continue

                        orgtxt.write(
                            "{} {} {} {} {} {} {}\n".format(0, rect_width, rect_height, bboxs[i][0], bboxs[i][1],
                                                            bboxs[i][2],
                                                            bboxs[i][3]))
                        txt.write(
                            "{} {} {} {} {}\n".format(0, (bboxs[i][0] + bboxs[i][2] / 2) / rect_width,
                                                      (bboxs[i][1] + bboxs[i][3] / 2) / rect_height,
                                                      bboxs[i][2] / rect_width, bboxs[i][3] / rect_height))
            # 写图片
            cv2.imwrite(save_path + "//{}-{}-{}.jpg".format(image_name, index, index_offset), image_scale_copy)
            pass
    pass


# 在box的区域上涂黑
# size=(width,height);box=[x,y,width,height]
def drawBlack(image, size, box):
    box_x = min(max(0, box[0]), size[0])
    box_y = min(max(0, box[1]), size[1])
    for x in range(box_x, min(max(box_x + box[2], 0), size[0])):
        for y in range(box_y, min(max(box_y + box[3], 0), size[1])):
            image[y][x][0] = 0
            image[y][x][1] = 0
            image[y][x][2] = 0


def multi_scale(image_path, image_name, save_path):
    image = cv2.imread(image_path + image_name + '.jpg')
    bboxs_org = []

    with open(image_path + image_name + 'org.txt') as file:
        for line in file.readlines():
            line = line.split(' ')
            width = int(line[1])
            height = int(line[2])
            bboxs_org.append([int(line[3]), int(line[4]), int(line[5]), int(line[6])])
    for index, scale in enumerate(scales):
        bboxs = copy.deepcopy(bboxs_org)
        rect_height = int(height * scale / 2)
        rect_width = int(width * scale / 2)
        x1 = max(0, center[0] - rect_width)
        x2 = min(width, center[0] + rect_width)
        y1 = max(0, center[1] - rect_height)
        y2 = min(height, center[1] + rect_height)
        rect_height = y2 - y1
        rect_width = x2 - x1
        for i in range(len(bboxs)):
            bboxs[i][0] = max(bboxs[i][0] - x1, 0)
            bboxs[i][1] = max(bboxs[i][1] - y1, 0)
        image_scale = image[y1:y2, x1:x2, :]
        cv2.imwrite(save_path + "//{}-{}.jpg".format(image_name, index), image_scale)
        with open(save_path + "//{}-{}.txt".format(image_name, index), 'w') as txt:
            with open(save_path + "//{}-{}org.txt".format(image_name, index), 'w') as orgtxt:
                for i in range(len(bboxs)):
                    if bboxs[i][0] <= 0 or bboxs[i][1] <= 0 or bboxs[i][0] + bboxs[i][2] >= rect_width - 1 \
                            or bboxs[i][1] + bboxs[i][3] >= rect_height - 1:
                        continue

                    orgtxt.write(
                        "{} {} {} {} {} {} {}\n".format(0, rect_width, rect_height, bboxs[i][0], bboxs[i][1],
                                                        bboxs[i][2],
                                                        bboxs[i][3]))
                    txt.write(
                        "{} {} {} {} {}\n".format(0, bboxs[i][0] / rect_width, bboxs[i][1] / rect_height,
                                                  bboxs[i][2] / rect_width, bboxs[i][3] / rect_height))
        pass
    pass


if __name__ == '__main__':
    PATH = r'C:\Users\27591\Desktop\gj\\'
    SAVE_PATH = r'C:\Users\27591\Desktop\gj\test\output-black'
    image_list = ['200', '1400', '2000', '3200', '4400', '5200']
    for image in image_list:
        print('process image {} begin!!'.format(image))
        multi_scale_height(PATH, image, SAVE_PATH)
        print('process image {} end!!'.format(image))
    pass
