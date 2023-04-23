
import cv2

# 生成颜色数组


def generate_from_file(filepath, width=8, height=8, brightness=0.05, invert=False):
    img = cv2.imread(filepath)
    img = cv2.resize(img, (width, height))
    color = []
    for x in range(width):
        for y in range(height):
            pixel = []
            for c in img[x][y]:
                if invert:
                    pixel.append(int((255 - c)*brightness))
                else:
                    pixel.append(int((c)*brightness))
            color.append(pixel)
    print(color)  # 输出颜色数组

generate_from_file('l.bmp', brightness=0.05)
