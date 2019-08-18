import os, sys


def changeName(path, begin=0, prefix='GJ'):
    for fileName in os.listdir(path):
        if os.path.isfile(os.path.join(path, fileName)) and fileName.endswith('.jpg'):
            fileName = fileName[:-4]
            newFileName = prefix + str(begin)
            os.rename(os.path.join(path, fileName + '.jpg'), os.path.join(path, newFileName + '.jpg'))
            os.rename(os.path.join(path, fileName + '.txt'), os.path.join(path, newFileName + '.txt'))
            os.rename(os.path.join(path, fileName + 'org.txt'), os.path.join(path, newFileName + 'org.txt'))
            begin += 1


if __name__ == '__main__':
    path = r'F:\PostGraduate\DataSet\LowPosition\train_add'
    changeName(path, 16659, prefix='LR')
