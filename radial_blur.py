import cv2
import numpy as np
import datetime


class MouseParam:
    def __init__(self, input_img_name):
        # マウス入力用のパラメータ
        self.mouseEvent = {"x": None, "y": None, "event": None, "flags": None}
        # マウス入力の設定
        cv2.setMouseCallback(input_img_name, self.__callback_func, None)

    # コールバック関数
    def __callback_func(self, event_type, x, y, flags, user_data):
        self.mouseEvent["x"] = x
        self.mouseEvent["y"] = y
        self.mouseEvent["event"] = event_type
        self.mouseEvent["flags"] = flags
        self.mouseEvent["user_data"] = user_data

    # マウスイベントを返す関数
    def get_event(self):
        return self.mouseEvent["event"]

        # 座標を返す関数

    def get_pos(self):
        return self.mouseEvent["x"], self.mouseEvent["y"]


def radial_blur(src, pos, ratio, iterations, margin):
    h, w = src.shape[0:2]
    n = iterations
    m = margin

    # 背景を作成する．
    bg = np.ones(src.shape, dtype=np.uint8) * 255
    bg = cv2.resize(bg, (int(m * w), int(m * h)))

    # 背景の中心に元画像を配置
    bg[int((m - 1) * h / 2):int((m - 1) * h / 2 + h), int((m - 1) * w / 2):int((m - 1) * w / 2 + w)] = src

    image_list = []
    h *= m
    w *= m
    c_x = pos[0] * m
    c_y = pos[1] * m
    for i in range(n):
        r = ratio + (1 - ratio) * (i + 1) / n
        shrunk = cv2.resize(src, (int(r * w), int(r * h)))
        left = int((1 - r) * c_x)
        right = left + shrunk.shape[1]
        top = int((1 - r) * c_y)
        bottom = top + shrunk.shape[0]
        bg[top:bottom, left:right] = shrunk
        image_list.append(bg.astype(np.int32))

    dst = sum(image_list) / n
    dst = dst.astype(np.uint8)

    r = (1 + ratio) / 2
    dst = dst[int((1 - r) * c_y):int(((1 - r) * c_y + h) * r), int((1 - r) * c_x):int(((1 - r) * c_x + w) * r)]
    dst = cv2.resize(dst, (int(w / m), int(h / m)))
    return dst


def nothing(x):
    pass


def main():
    src = cv2.imread("C:/Users/Miyamoto Junpei/PycharmProjects/VisualGuidance/src/photo/im20180521174454.png", cv2.IMREAD_COLOR)
    dst = src
    win_name = "Radial Blur"
    cv2.namedWindow(win_name, cv2.WINDOW_KEEPRATIO)
    mouse_data = MouseParam(win_name)
    cv2.createTrackbar("ratio", win_name, 10, 30, nothing)
    cv2.createTrackbar("iterations", win_name, 20, 100, nothing)
    cv2.createTrackbar("margin", win_name, 30, 100, nothing)

    while True:
        ratio = 1 - cv2.getTrackbarPos("ratio", win_name) / 100
        iterations = cv2.getTrackbarPos("iterations", win_name)
        if iterations == 0:
            iterations = 1
        margin = 1 + cv2.getTrackbarPos("margin", win_name) / 100
        if mouse_data.get_event() == cv2.EVENT_LBUTTONUP:
            mouse_pos = mouse_data.get_pos()
            print(mouse_pos)
            dst = radial_blur(src, mouse_pos, ratio, iterations, margin)

        cv2.imshow(win_name, dst)
        key = cv2.waitKey(1)
        if key == ord("s"):
            cv2.imwrite('im{0:%Y%m%d%H%M%S}.png'.format(datetime.datetime.today()), dst)
        elif key == ord("q"):
            break

    cv2.destroyAllWindows()


if __name__ == "__main__":
    main()
