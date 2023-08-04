# 小球斜45°四向反弹
#    3     0
#     \ | /
#     -----
#     / | \
#    2     1

# 移动的小球
class MoveBall:
    def __init__(self, cx, cy, size, xmin, ymin, xmax, ymax):
        self.cx = cx
        self.cy = cy
        self.direction = 0
        self.step = [[2, -2], [2, 2], [-2, 2], [-2, -2]]
        self.size = size
        self.xmin = xmin
        self.ymin = ymin
        self.xmax = xmax
        self.ymax = ymax

    def nextStep(self):
        tx = self.cx+self.step[self.direction][0]
        ty = self.cy+self.step[self.direction][1]
        if (tx < self.xmin):
            self.cx = self.xmin
            self.cy = ty
            if (self.direction == 3):
                self.direction = 0
            else:
                self.direction = 1
        elif (tx > self.xmax-self.size):
            self.cx = self.xmax-self.size
            self.cy = ty
            if (self.direction == 0):
                self.direction = 3
            else:
                self.direction = 2
        elif (ty < self.ymin):
            self.cy = self.ymin
            self.cx = tx
            if (self.direction == 0):
                self.direction = 1
            else:
                self.direction = 2
        elif (ty > self.ymax-self.size):
            self.cy = self.ymax-self.size
            self.cx = tx
            if (self.direction == 1):
                self.direction = 0
            else:
                self.direction = 3
        else:
            self.cx = tx
            self.cy = ty
