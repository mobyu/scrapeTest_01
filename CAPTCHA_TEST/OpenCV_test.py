# 使用OpenCV进行验证码缺口识别
# 阈值与图片本身有直接关系
import cv2

GAUSSIAN_BLUR_KERNEL_SIZE = (5, 5)
GAUSSIAN_BLUR_SIGMA_X = 0
CANNY_THRESHOLD1 = 200
CANNY_THRESHOLD2 = 450


def get_gaussian_blur_image(image):  # 对图片进行高斯滤波处理并返回
    return cv2.GaussianBlur(image, GAUSSIAN_BLUR_KERNEL_SIZE, GAUSSIAN_BLUR_SIGMA_X)


def get_canny_image(image):  # 返回边缘检测后图片信息
    return cv2.Canny(image, CANNY_THRESHOLD1, CANNY_THRESHOLD2)


def get_contours(image):  # 返回提取的轮廓信息
    contours, _ = cv2.findContours(image, cv2.RETR_CCOMP, cv2.CHAIN_APPROX_SIMPLE)
    return contours


def get_contour_area_threshold(image_width, image_height):  # 计算轮廓面积上下限
    contour_area_min = (image_width * 0.15) * (image_height * 0.25) * 0.8
    contour_area_max = (image_width * 0.15) * (image_height * 0.25) * 1.2
    return contour_area_min, contour_area_max


def get_arc_length_threshold(image_width, image_height):  # 计算轮廓周长上下限
    arc_length_min = ((image_width * 0.15) + (image_height * 0.25)) * 2 * 0.8
    arc_length_max = ((image_width * 0.15) + (image_height * 0.25)) * 2 * 1.2
    return arc_length_min, arc_length_max


def get_offset_threshold(image_width):  # 计算缺口位置偏移量上下限
    offset_min = 0.2 * image_width
    offset_max = 0.85 * image_width
    return offset_min, offset_max


def main():
    image_row = cv2.imread(r'E:\Mydata\picture\captcha.png')
    image_height, image_width, _ = image_row.shape
    # print(image_height, image_width)
    image_gaussian_blur = get_gaussian_blur_image(image_row)
    image_canny = get_canny_image(image_gaussian_blur)
    contours = get_contours(image_canny)
    cv2.imwrite(r'E:\Mydata\picture\image_canny.png', image_canny)
    cv2.imwrite(r'E:\Mydata\picture\image_gaussian_blur.png', image_gaussian_blur)
    contour_area_min, contour_area_max = get_contour_area_threshold(image_width, image_height)
    arc_length_min, arc_length_max = get_arc_length_threshold(image_width, image_height)
    offset_min, offset_max = get_offset_threshold(image_width)
    offset = None
    for contour in contours:
        x, y, w, h = cv2.boundingRect(contour)
        if contour_area_min < cv2.contourArea(contour) < contour_area_max and \
                arc_length_min < cv2.arcLength(contour, True) < arc_length_max and \
                offset_min < x < offset_max:
            cv2.rectangle(image_row, (x, y), (x + w, y + h), (0, 0, 255), 2)
            offset = x
            # print(offset)
    cv2.imwrite(r'E:\Mydata\picture\image_label.png', image_row)
    print('offset', offset)


if __name__ == "__main__":
    main()