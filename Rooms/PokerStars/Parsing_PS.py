from PIL import Image
from PIL import ImageFilter
import numpy as np
import math


def check_stats_array(array_size_xy, stats_list_str):
    # speed
    errors_s = 2
    # Black_s
    row_sF = np.array([0, 1, 2, 4, 6, 8, 9, 10, 12, 14], int)
    col_sF = np.array([1, 1, 1, 1, 1, 1, 1,  1,  1,  1], int)
    im_array_sF = array_size_xy[row_sF, col_sF]
    find = sum(im_array_sF) < errors_s
    if find:
        return False

    # '0'
    errors_0 = 0
    # Black_0
    row_0F = np.array([0,  0, 3, 6, 10, 12, 15, 15], int)
    col_0F = np.array([0, 10, 5, 3,  6,  4,  0, 10], int)
    # White_0
    row_0T = np.array([0, 0, 3, 3, 7,  7,  8,  8, 12, 12, 15, 15], int)
    col_0T = np.array([3, 7, 1, 9, 0, 10,  0, 10,  1,  9,  3,  7], int)
    im_array_0F = array_size_xy[row_0F, col_0F]
    im_array_0T = array_size_xy[row_0T, col_0T]
    find = (sum(im_array_0F) <= errors_0) and (sum(im_array_0T) >= col_0T.size - errors_0)
    if find:
        stats_list_str.append('0')
        return True

    # '1'
    errors_1 = 0
    # Black_1
    row_1F = np.array([0,  0,  4, 8,  8, 12, 12], int)
    col_1F = np.array([0, 10, 10, 0, 10,  0, 10], int)
    # White_1
    row_1T = np.array([0, 4, 4, 8, 12, 15, 15, 15], int)
    col_1T = np.array([5, 0, 5, 5,  5,  1,  5,  9], int)
    im_array_1F = array_size_xy[row_1F, col_1F]
    im_array_1T = array_size_xy[row_1T, col_1T]
    find = (sum(im_array_1F) <= errors_1) and (sum(im_array_1T) >= col_1T.size - errors_1)
    if find:
        stats_list_str.append('1')
        return True

    # '2'
    errors_2 = 0
    # Black_2
    row_2F = np.array([0,  0, 4, 6, 9,  9, 12, 12], int)
    col_2F = np.array([0, 10, 5, 3, 1, 10,  7, 10], int)
    # White_2
    row_2T = np.array([0, 0, 2, 2, 6, 9, 12, 15, 15], int)
    col_2T = np.array([3, 7, 1, 9, 9, 6,  3,  2,  8], int)
    im_array_2F = array_size_xy[row_2F, col_2F]
    im_array_2T = array_size_xy[row_2T, col_2T]
    find = (sum(im_array_2F) <= errors_2) and (sum(im_array_2T) >= col_2T.size - errors_2)
    if find:
        stats_list_str.append('2')
        return True

    # '3'
    errors_3 = 0
    # Black_3
    row_3F = np.array([ 0,  4, 4,  6, 11, 11, 15], int)
    col_3F = np.array([10,  0, 4, 10,  0,  4, 10], int)
    # White_3
    row_3T = np.array([0, 0, 3, 6, 6, 11, 15, 15], int)
    col_3T = np.array([0, 6, 8, 2, 7,  9,  0,  6], int)
    im_array_3F = array_size_xy[row_3F, col_3F]
    im_array_3T = array_size_xy[row_3T, col_3T]
    find = (sum(im_array_3F) <= errors_3) and (sum(im_array_3T) >= col_3T.size - errors_3)
    if find:
        stats_list_str.append('3')
        return True

    # '4'
    errors_4 = 0
    # Black_4
    row_4F = np.array([0, 0, 3, 8, 13, 13, 15, 15], int)
    col_4F = np.array([0, 3, 0, 5,  1,  5,  1,  5], int)
    # White_4
    row_4T = np.array([0, 3, 3, 8, 8, 10, 10, 15], int)
    col_4T = np.array([8, 5, 9, 2, 9,  1,  9,  9], int)
    im_array_4F = array_size_xy[row_4F, col_4F]
    im_array_4T = array_size_xy[row_4T, col_4T]
    find = (sum(im_array_4F) <= errors_4) and (sum(im_array_4T) >= col_4T.size - errors_4)
    if find:
        stats_list_str.append('4')
        return True

    # '5'
    errors_5 = 0
    # Black_5
    row_5F = np.array([4,  4,  7, 11, 11, 15], int)
    col_5F = np.array([5, 10, 10,  0,  4, 10], int)
    # White_5
    row_5T = np.array([0, 0, 4, 6, 7, 11, 15, 15], int)
    col_5T = np.array([0, 8, 0, 2, 7,  8,  0,  5], int)
    im_array_5F = array_size_xy[row_5F, col_5F]
    im_array_5T = array_size_xy[row_5T, col_5T]
    find = (sum(im_array_5F) <= errors_5) and (sum(im_array_5T) >= col_5T.size - errors_5)
    if find:
        stats_list_str.append('5')
        return True

    # '6'
    errors_6 = 0
    # Black_6
    row_6F = np.array([0, 4,  4, 10, 15, 15], int)
    col_6F = np.array([0, 5, 10,  5,  0, 10], int)
    # White_6
    row_6T = np.array([0, 0, 4, 8, 8, 12, 12, 15, 15], int)
    col_6T = np.array([4, 8, 1, 0, 8,  0,  8,  3,  7], int)
    im_array_6F = array_size_xy[row_6F, col_6F]
    im_array_6T = array_size_xy[row_6T, col_6T]
    find = (sum(im_array_6F) <= errors_6) and (sum(im_array_6T) >= col_6T.size - errors_6)
    if find:
        stats_list_str.append('6')
        return True
    # '7'
    errors_7 = 0
    # Black_7
    row_7F = np.array([3, 3, 7, 7,  8, 11, 11, 15, 15], int)
    col_7F = np.array([0, 5, 0, 3, 10,  0, 10,  0,  7], int)
    # White_7
    row_7T = np.array([0, 0, 3, 7, 10, 13, 15], int)
    col_7T = np.array([1, 9, 9, 7,  5,  5,  4], int)
    im_array_7F = array_size_xy[row_7F, col_7F]
    im_array_7T = array_size_xy[row_7T, col_7T]
    find = (sum(im_array_7F) <= errors_7) and (sum(im_array_7T) >= col_7T.size - errors_7)
    if find:
        stats_list_str.append('7')
        return True

    # '8'
    errors_8 = 0
    # Black_8
    row_8F = np.array([0,  0, 4, 7,  7, 12, 15, 15], int)
    col_8F = np.array([0, 10, 5, 0, 10,  5,  0, 10], int)
    # White_8
    row_8T = np.array([0, 3,  3, 8, 12, 12, 15], int)
    col_8T = np.array([5, 0, 10, 5,  0, 10,  5], int)
    im_array_8F = array_size_xy[row_8F, col_8F]
    im_array_8T = array_size_xy[row_8T, col_8T]
    find = (sum(im_array_8F) <= errors_8) and (sum(im_array_8T) >= col_8T.size - errors_8)
    if find:
        stats_list_str.append('8')
        return True

    # '9'
    errors_9 = 0
    # Black_9
    row_9F = np.array([0,  0, 3, 6, 11, 11, 15], int)
    col_9F = np.array([0, 10, 5, 5,  0,  5, 10], int)
    # White_9
    row_9T = np.array([0, 0, 3, 3, 6, 6, 9, 9, 13, 15, 15], int)
    col_9T = np.array([3, 7, 1, 9, 1, 9, 3, 9,  8,  2,  6], int)
    im_array_9F = array_size_xy[row_9F, col_9F]
    im_array_9T = array_size_xy[row_9T, col_9T]
    find = (sum(im_array_9F) <= errors_9) and (sum(im_array_9T) >= col_9T.size - errors_9)
    if find:
        stats_list_str.append('9')
        return True

    # '-'
    errors_z = 0
    # Black_z
    row_zF = np.array([7, 7, 8, 8, 10, 10], int)
    col_zF = np.array([2, 7, 0, 9,  2,  7], int)
    # White_z
    row_zT = np.array([8, 8, 9, 9], int)
    col_zT = np.array([2, 7, 2, 7], int)
    im_array_zF = array_size_xy[row_zF, col_zF]
    im_array_zT = array_size_xy[row_zT, col_zT]
    find = (sum(im_array_zF) <= errors_z) and (sum(im_array_zT) >= col_zT.size - errors_z)
    if find:
        stats_list_str.append('0')
        return True
    return False


def check_stats(image, caption):  # im01_CR
    stats_list_str = []
    stats_list_digit = []

    # image.save(r'images/01/' + caption + '.png')
    size_200 = (image.width * 2, image.height * 2)
    # transform scale200
    T_scale_200 = np.array([
        [0.5, 0, 0],
        [0, 0.5, 0],
        [0, 0, 1]])
    # filter+gray+BW
    thresh = 125
    f_BW = lambda x: 255 if x > thresh else 0
    image_AFBI200 = image.transform(size_200, Image.AFFINE,
                                        data=T_scale_200.flatten()[:6],
                                        resample=Image.BICUBIC)
    # SHARPEN
    image_AFBI200_SH_BW = image_AFBI200.filter(ImageFilter.SHARPEN).convert('L').point(f_BW, mode='1')
    # image_AFBI200_SH_BW.save(r'images/01/' + caption + '_AFBI200_SH_BW.png')
    # Numpy
    image_w, image_h = image_AFBI200_SH_BW.size  # (176, 116)
    image_array = np.asarray(image_AFBI200_SH_BW)
    image_array = image_array.copy()
    size_x = 11
    size_y = 16
    # проход image_AFBI200_SH_BW
    row = 0
    row_next = False
    sep = 0
    sep_go = False
    while row < image_h - size_y + 1:
        col = 0
        while col < image_w - size_x + 1:
            # новый массив
            image_array_size_xy = image_array[row:row + size_y, col:col + size_x]
            if check_stats_array(image_array_size_xy, stats_list_str):
                col += size_x + 1  # (2 не нопределил 7 в 57)
                row_next = True
                sep = 0
                sep_go = True
            col += 1
            # проверка на разделитель
            if sep_go:
                sep += 1
                if sep > 5:
                    stats_list_str.append('x')
                    sep_go = False
        if row_next:
            stats_list_str.append('x')
            row += size_y + 17  # HUD Отступы = 0 (константа меняется! и влияет на скорость!)
            row_next = False
        row += 1

    # stats_list_str -> stats_list_digit
    stats_str = ''.join(str(i) for i in stats_list_str)
    stats_str = stats_str.split('x')

    for i in stats_str:
        if i != '':
            stats_list_digit.append(int(i))
    return stats_list_digit


def check_inTheGame_array(array_size_xy):
    # speed
    errors_s = 2
    # Black_s
    row_sF = np.array([4, 8, 12, 16], int)
    col_sF = np.array([0, 0,  0,  0], int)
    im_array_sF = array_size_xy[row_sF, col_sF]
    find = sum(im_array_sF) < errors_s
    if find:
        return False
    # ||
    errors_0 = 0
    # White_0
    row_0T = np.array([4, 8, 12, 16], int)
    col_0T = np.array([0, 0,  0,  0], int)
    im_array_0T = array_size_xy[row_0T, col_0T]
    find = (sum(im_array_0T) >= col_0T.size - errors_0)
    if find:
        return True
    return False


def check_inTheGame(image, caption):  # im01_CR
    # image.save(r'images/01/' + caption + '.png')
    size_200 = (image.width * 2, image.height * 2)
    # transform scale200
    T_scale_200 = np.array([
        [0.5, 0, 0],
        [0, 0.5, 0],
        [0, 0, 1]])
    # filter+gray+BW
    thresh = 200
    f_BW = lambda x: 255 if x > thresh else 0
    image_AFBI200 = image.transform(size_200, Image.AFFINE,
                                    data=T_scale_200.flatten()[:6],
                                    resample=Image.BICUBIC)
    # SHARPEN
    image_AFBI200_SH_BW = image_AFBI200.filter(ImageFilter.SHARPEN).convert('L').point(f_BW, mode='1')
    # image_AFBI200_SH_BW.save(r'images/01/' + caption + '_AFBI200_SH_BW.png')
    # Numpy
    image_w, image_h = image_AFBI200_SH_BW.size  # (76, 20)
    image_array = np.asarray(image_AFBI200_SH_BW)
    image_array = image_array.copy()
    size_x = 1
    size_y = 20
    # проход image_AFBI200_SH_BW
    row = 0
    col = 0
    while col < image_w:
        # новый массив
        image_array_size_xy = image_array[row:row + size_y, col:col + size_x]
        if check_inTheGame_array(image_array_size_xy):
            return True
        col += 1
    return False


def check_stackBB_array(array_size_xy, stackBB_list_str, row_next):
    # speed
    if not row_next:
        errors_s = 2
        # Black_s
        row_sF = np.array([0, 0, 0, 0, 0,  0,  0], int)
        col_sF = np.array([0, 3, 5, 7, 9, 11, 13], int)
        im_array_sF = array_size_xy[row_sF, col_sF]
        find = sum(im_array_sF) < errors_s
        if find:
            return False

    # '0'
    errors_0 = 0
    # Black_0
    row_0F = np.array([0,  0, 6, 12, 16, 23, 23], int)
    col_0F = np.array([0, 13, 7,  7,  7,  0, 13], int)
    # White_0
    row_0T = np.array([0, 6,  6, 11, 11, 16, 16, 23], int)
    col_0T = np.array([6, 0, 13,  0, 13,  0, 13,  6], int)
    im_array_0F = array_size_xy[row_0F, col_0F]
    im_array_0T = array_size_xy[row_0T, col_0T]
    find = (sum(im_array_0F) <= errors_0) and (sum(im_array_0T) >= col_0T.size - errors_0)
    if find:
        stackBB_list_str.append('0')
        return True

    # '1'
    errors_1 = 0
    # Black_1
    row_1F = np.array([0,  0, 6,  6, 12, 12, 17, 17, 23, 23], int)
    col_1F = np.array([0, 13, 0, 13,  0, 13,  0, 13,  0, 13], int)
    # White_1
    row_1T = np.array([0, 3, 6, 11, 16, 23], int)
    col_1T = np.array([7, 4, 8,  8,  8,  8], int)
    im_array_1F = array_size_xy[row_1F, col_1F]
    im_array_1T = array_size_xy[row_1T, col_1T]
    find = (sum(im_array_1F) <= errors_1) and (sum(im_array_1T) >= col_1T.size - errors_1)
    if find:
        stackBB_list_str.append('1')
        return True

    # '2'
    errors_2 = 0
    # Black_2
    row_2F = np.array([0,  0, 7, 7, 14, 14, 18, 18], int)
    col_2F = np.array([0, 13, 0, 7,  0, 13,  9, 13], int)
    # White_2
    row_2T = np.array([0, 2,  7, 15, 23, 23], int)
    col_2T = np.array([7, 2, 12,  7,  2, 10], int)
    im_array_2F = array_size_xy[row_2F, col_2F]
    im_array_2T = array_size_xy[row_2T, col_2T]
    find = (sum(im_array_2F) <= errors_2) and (sum(im_array_2T) >= col_2T.size - errors_2)
    if find:
        stackBB_list_str.append('2')
        return True

    # '3'
    errors_3 = 0
    # Black_3
    row_3F = np.array([0,  0, 6, 6, 11, 13, 16, 16, 23], int)
    col_3F = np.array([0, 13, 0, 6,  0,  2,  0,  6, 13], int)
    # White_3
    row_3T = np.array([0,  5, 11, 17, 23], int)
    col_3T = np.array([6, 13,  8, 13,  6], int)
    im_array_3F = array_size_xy[row_3F, col_3F]
    im_array_3T = array_size_xy[row_3T, col_3T]
    find = (sum(im_array_3F) <= errors_3) and (sum(im_array_3T) >= col_3T.size - errors_3)
    if find:
        stackBB_list_str.append('3')
        return True

    # '4'
    errors_4 = 0
    # Black_4
    row_4F = np.array([0, 0, 7, 13, 23, 23], int)
    col_4F = np.array([0, 5, 0,  6,  0,  6], int)
    # White_4
    row_4T = np.array([ 0, 8,  8, 17, 17, 23], int)
    col_4T = np.array([10, 5, 11,  0, 11, 11], int)
    im_array_4F = array_size_xy[row_4F, col_4F]
    im_array_4T = array_size_xy[row_4T, col_4T]
    find = (sum(im_array_4F) <= errors_4) and (sum(im_array_4T) >= col_4T.size - errors_4)
    if find:
        stackBB_list_str.append('4')
        return True

    # '5'
    errors_5 = 0
    # Black_5
    row_5F = np.array([6,  6, 16, 16, 23], int)
    col_5F = np.array([7, 13,  0,  7, 13], int)
    # White_5
    row_5T = np.array([0, 0, 6, 11, 11, 17, 23, 23], int)
    col_5T = np.array([2, 9, 2,  2,  9, 13,  2,  8], int)
    im_array_5F = array_size_xy[row_5F, col_5F]
    im_array_5T = array_size_xy[row_5T, col_5T]
    find = (sum(im_array_5F) <= errors_5) and (sum(im_array_5T) >= col_5T.size - errors_5)
    if find:
        stackBB_list_str.append('5')
        return True

    # '6'
    errors_6 = 0
    # Black_6
    row_6F = np.array([0, 5,  5, 13, 18, 23, 23], int)
    col_6F = np.array([0, 5, 13,  7,  7,  0, 13], int)
    # White_6
    row_6T = np.array([0, 6, 9, 15, 15, 23], int)
    col_6T = np.array([9, 2, 8,  0, 13,  7], int)
    im_array_6F = array_size_xy[row_6F, col_6F]
    im_array_6T = array_size_xy[row_6T, col_6T]
    find = (sum(im_array_6F) <= errors_6) and (sum(im_array_6T) >= col_6T.size - errors_6)
    if find:
        stackBB_list_str.append('6')
        return True

    # '7'
    errors_7 = 0
    # Black_7
    row_7F = np.array([5, 5, 9,  9, 14, 14, 19, 23, 23], int)
    col_7F = np.array([1, 7, 1, 13,  1, 13, 10,  0, 10], int)
    # White_7
    row_7T = np.array([0, 0,  3, 11, 15, 23], int)
    col_7T = np.array([1, 8, 12,  9,  7,  4], int)
    im_array_7F = array_size_xy[row_7F, col_7F]
    im_array_7T = array_size_xy[row_7T, col_7T]
    find = (sum(im_array_7F) <= errors_7) and (sum(im_array_7T) >= col_7T.size - errors_7)
    if find:
        stackBB_list_str.append('7')
        return True

    # '8'
    errors_8 = 0
    # Black_8
    row_8F = np.array([0,  0, 6, 11, 11, 17, 23, 23], int)
    col_8F = np.array([0, 13, 7,  0, 13,  7,  0, 13], int)
    # White_8
    row_8T = np.array([0, 5,  5, 8, 11, 18, 18, 23], int)
    col_8T = np.array([7, 0, 13, 2,  7,  0, 13,  7], int)
    im_array_8F = array_size_xy[row_8F, col_8F]
    im_array_8T = array_size_xy[row_8T, col_8T]
    find = (sum(im_array_8F) <= errors_8) and (sum(im_array_8T) >= col_8T.size - errors_8)
    if find:
        stackBB_list_str.append('8')
        return True

    # '9'
    errors_9 = 0
    # Black_9
    row_9F = np.array([0,  0, 6, 17, 17, 23], int)
    col_9F = np.array([0, 13, 7,  0,  6, 13], int)
    # White_9
    row_9T = np.array([0, 7,  7, 13, 13, 17, 23, 23], int)
    col_9T = np.array([6, 0, 13,  6, 13, 12,  2,  7], int)
    im_array_9F = array_size_xy[row_9F, col_9F]
    im_array_9T = array_size_xy[row_9T, col_9T]
    find = (sum(im_array_9F) <= errors_9) and (sum(im_array_9T) >= col_9T.size - errors_9)
    if find:
        stackBB_list_str.append('9')
        return True

    # '.X' universal decimal
    errors_05 = 0
    # Black_z
    row_zF = np.array([0, 0, 6, 6, 12, 12, 17, 17, 23], int)
    col_zF = np.array([0, 6, 0, 6,  0,  6,  0,  6,  6], int)
    # White_z
    row_zT = np.array([23], int)
    col_zT = np.array([1], int)
    im_array_zF = array_size_xy[row_zF, col_zF]
    im_array_zT = array_size_xy[row_zT, col_zT]
    find = (sum(im_array_zF) <= errors_05) and (sum(im_array_zT) >= col_zT.size - errors_05)
    if find:
        stackBB_list_str.append('.5')
        return True

    # 'A' (All-In)
    errors_A = 0
    # Black_A
    row_AF = np.array([0, 0, 6, 6, 12, 19, 19, 23, 23], int)
    col_AF = np.array([0, 13, 0, 13, 7, 4, 9, 2, 11], int)
    # White_A
    row_AT = np.array([0, 6, 13, 13, 17, 17], int)
    col_AT = np.array([7, 4, 2, 11, 0, 13], int)
    im_array_AF = array_size_xy[row_AF, col_AF]
    im_array_AT = array_size_xy[row_AT, col_AT]
    find = (sum(im_array_AF) <= errors_A) and (sum(im_array_AT) >= col_AT.size - errors_A)
    if find:
        stackBB_list_str.append('0')
        return True
    return False


def check_stackBB(image, caption):  # im01_CR
    stackBB_list_str = []
    # image.save(r'images/01/' + caption + '.png')
    size_200 = (image.width * 2, image.height * 2)
    # transform scale200
    T_scale_200 = np.array([
        [0.5, 0, 0],
        [0, 0.5, 0],
        [0, 0, 1]])
    # filter+gray+BW
    thresh = 100
    f_BW = lambda x: 255 if x > thresh else 0
    image_AFBI200 = image.transform(size_200, Image.AFFINE,
                                        data=T_scale_200.flatten()[:6],
                                        resample=Image.BICUBIC)
    # SHARPEN
    image_AFBI200_SH_BW = image_AFBI200.filter(ImageFilter.SHARPEN).convert('L').point(f_BW, mode='1')
    # image_AFBI200_SH_BW.save(r'images/01/' + caption + '_AFBI200_SH_BW.png')
    # Numpy
    image_w, image_h = image_AFBI200_SH_BW.size  # (180, 36)
    image_array = np.asarray(image_AFBI200_SH_BW)
    image_array = image_array.copy()
    size_x = 14
    size_y = 24
    # проход image_AFBI200_SH_BW
    row = 0
    row_next = False
    sep = 0
    sep_go = False
    while row < image_h - size_y + 1:
        col = 0
        while col < image_w - size_x + 1:
            # новый массив
            image_array_size_xy = image_array[row:row + size_y, col:col + size_x]
            if check_stackBB_array(image_array_size_xy, stackBB_list_str, row_next):
                col += size_x + 2  # (подобрать значение между цифрами!)
                sep = 0
                sep_go = True
                row_next = True
            col += 1
            # проверка на разделитель
            if sep_go:
                sep += 1
                if sep > 5:  # (подобрать значение между цифрами!)
                    break
        if row_next:
            break
        row += 1
    # stackBB_list_str -> stackBB_digit
    if len(stackBB_list_str) == 0:
        stackBB_digit = 100
    else:
        stackBB_digit = float(''.join(str(i) for i in stackBB_list_str))
    return stackBB_digit


def check_bets_array(array_size_xy, bets_list_str, row_next):
    # speed
    if not row_next:
        errors_s = 2
        # Black_s
        row_sF = np.array([0, 0, 0, 0, 0,  0, 19], int)
        col_sF = np.array([0, 3, 5, 7, 9, 11,  0], int)
        im_array_sF = array_size_xy[row_sF, col_sF]
        find = sum(im_array_sF) < errors_s
        if find:
            return False

    # '0'
    errors_0 = 0
    # Black_0
    row_0F = np.array([0,  0, 4, 7, 7, 9, 12, 12, 15, 19, 19,   20, 20, 20], int)
    col_0F = np.array([0, 11, 5, 3, 8, 5,  3,  8,  5,  0, 11,    0,  5, 11], int)
    # White_0
    row_0T = np.array([0, 5,  5, 9,  9, 14, 14, 19], int)
    col_0T = np.array([5, 0, 11, 0, 11,  0, 11,  5], int)
    im_array_0F = array_size_xy[row_0F, col_0F]
    im_array_0T = array_size_xy[row_0T, col_0T]
    find = (sum(im_array_0F) <= errors_0) and (sum(im_array_0T) >= col_0T.size - errors_0)
    if find:
        bets_list_str.append('0')
        return True

    # '1'
    errors_1 = 0
    # Black_1
    row_1F = np.array([0,  0, 7,  7, 13, 13, 19, 19,   20, 20, 20], int)
    col_1F = np.array([0, 11, 0, 11,  0, 11,  0, 11,    0,  5, 11], int)
    # White_1
    row_1T = np.array([0, 3, 3, 7, 11, 15, 19], int)
    col_1T = np.array([6, 2, 6, 6,  6,  6,  6], int)
    im_array_1F = array_size_xy[row_1F, col_1F]
    im_array_1T = array_size_xy[row_1T, col_1T]
    find = (sum(im_array_1F) <= errors_1) and (sum(im_array_1T) >= col_1T.size - errors_1)
    if find:
        bets_list_str.append('1')
        return True

    # '2'
    errors_2 = 0
    # Black_2
    row_2F = np.array([0,  0, 5, 5, 11, 11, 15, 16,   20, 20, 20], int)
    col_2F = np.array([0, 11, 0, 5,  0, 11, 11,  6,    0,  5, 11], int)
    # White_2
    row_2T = np.array([0, 2,  5, 11, 19, 19], int)
    col_2T = np.array([5, 2, 10,  7,  1, 10], int)
    im_array_2F = array_size_xy[row_2F, col_2F]
    im_array_2T = array_size_xy[row_2T, col_2T]
    find = (sum(im_array_2F) <= errors_2) and (sum(im_array_2T) >= col_2T.size - errors_2)
    if find:
        bets_list_str.append('2')
        return True

    # '3'
    errors_3 = 0
    # Black_3
    row_3F = np.array([5, 5, 9,  9, 14, 14,   20, 20, 20], int)
    col_3F = np.array([0, 5, 0, 11,  0,  6,    0,  5, 11], int)
    # White_3
    row_3T = np.array([0,  4, 9, 14, 19], int)
    col_3T = np.array([5, 11, 5, 11,  5], int)
    im_array_3F = array_size_xy[row_3F, col_3F]
    im_array_3T = array_size_xy[row_3T, col_3T]
    find = (sum(im_array_3F) <= errors_3) and (sum(im_array_3T) >= col_3T.size - errors_3)
    if find:
        bets_list_str.append('3')
        return True

    # '4'
    errors_4 = 0
    # Black_4
    row_4F = np.array([0, 0, 5, 10, 19, 19,   20, 20, 20], int)
    col_4F = np.array([0, 4, 0,  5,  0,  5,    0,  5, 11], int)
    # White_4
    row_4T = np.array([0, 6, 6, 13, 13, 19], int)
    col_4T = np.array([9, 4, 9,  0,  9,  9], int)
    im_array_4F = array_size_xy[row_4F, col_4F]
    im_array_4T = array_size_xy[row_4T, col_4T]
    find = (sum(im_array_4F) <= errors_4) and (sum(im_array_4T) >= col_4T.size - errors_4)
    if find:
        bets_list_str.append('4')
        return True

    # '5'
    errors_5 = 0
    # Black_5
    row_5F = np.array([4,  4, 12, 12, 19,   20, 20, 20], int)
    col_5F = np.array([5, 11,  0,  6, 11,    0,  5, 11], int)
    # White_5
    row_5T = np.array([0, 0, 4, 7, 7, 13, 19, 19], int)
    col_5T = np.array([2, 8, 1, 2, 7, 11,  1,  7], int)
    im_array_5F = array_size_xy[row_5F, col_5F]
    im_array_5T = array_size_xy[row_5T, col_5T]
    find = (sum(im_array_5F) <= errors_5) and (sum(im_array_5T) >= col_5T.size - errors_5)
    if find:
        bets_list_str.append('5')
        return True

    # '6'
    errors_6 = 0
    # Black_6
    row_6F = np.array([0, 4,  4, 10, 15, 19, 19,   20, 20, 20], int)
    col_6F = np.array([0, 6, 11,  6,  6,  0, 11,    0,  5, 11], int)
    # White_6
    row_6T = np.array([0, 3, 9,  9, 15, 15, 19], int)
    col_6T = np.array([7, 2, 0, 11,  0, 11,  6], int)
    im_array_6F = array_size_xy[row_6F, col_6F]
    im_array_6T = array_size_xy[row_6T, col_6T]
    find = (sum(im_array_6F) <= errors_6) and (sum(im_array_6T) >= col_6T.size - errors_6)
    if find:
        bets_list_str.append('6')
        return True

    # '7'
    errors_7 = 0
    # Black_7
    row_7F = np.array([5, 5, 9,  9, 14, 14, 19, 19,   20, 20, 20], int)
    col_7F = np.array([1, 5, 1, 11,  0, 11,  0, 11,    0,  5, 11], int)
    # White_7
    row_7T = np.array([0,  0,  3, 8, 13, 19], int)
    col_7T = np.array([1, 10, 10, 8,  6,  3], int)
    im_array_7F = array_size_xy[row_7F, col_7F]
    im_array_7T = array_size_xy[row_7T, col_7T]
    find = (sum(im_array_7F) <= errors_7) and (sum(im_array_7T) >= col_7T.size - errors_7)
    if find:
        bets_list_str.append('7')
        return True

    # '8'
    errors_8 = 0
    # Black_8
    row_8F = np.array([0,  0, 4, 9,  9, 14, 19, 19,   20, 20, 20], int)
    col_8F = np.array([0, 11, 6, 0, 11,  6,  0, 11,    0,  5, 11], int)
    # White_8
    row_8T = np.array([0, 4,  4, 7, 9, 14, 14, 19], int)
    col_8T = np.array([6, 0, 11, 2, 6,  0, 11,  6], int)
    im_array_8F = array_size_xy[row_8F, col_8F]
    im_array_8T = array_size_xy[row_8T, col_8T]
    find = (sum(im_array_8F) <= errors_8) and (sum(im_array_8T) >= col_8T.size - errors_8)
    if find:
        bets_list_str.append('8')
        return True

    # '9'
    errors_9 = 0
    # Black_9
    row_9F = np.array([0,  0, 6, 14, 14, 19,   20, 20, 20], int)
    col_9F = np.array([0, 11, 5,  0,  5, 11,    0,  5, 11], int)
    # White_9
    row_9T = np.array([0, 5,  5,  8, 11, 11, 14, 18, 19], int)
    col_9T = np.array([6, 0, 11, 11,  5, 11, 10,  6,  2], int)
    im_array_9F = array_size_xy[row_9F, col_9F]
    im_array_9T = array_size_xy[row_9T, col_9T]
    find = (sum(im_array_9F) <= errors_9) and (sum(im_array_9T) >= col_9T.size - errors_9)
    if find:
        bets_list_str.append('9')
        return True

    # '.X' universal decimal
    errors_05 = 0
    # Black_z
    row_zF = np.array([0, 0, 5, 5, 10, 10, 14, 14, 19, 20, 20, 20], int)
    col_zF = np.array([0, 4, 0, 4,  0,  4,  0,  4,  4,  0,  4, 11], int)
    # White_z
    row_zT = np.array([19], int)
    col_zT = np.array([1], int)
    im_array_zF = array_size_xy[row_zF, col_zF]
    im_array_zT = array_size_xy[row_zT, col_zT]
    find = (sum(im_array_zF) <= errors_05) and (sum(im_array_zT) >= col_zT.size - errors_05)
    if find:
        bets_list_str.append('.5')
        return True
    return False


def check_bets(image, caption):  # im01_CR
    bets_list_str = [0]  # [0] на случай, если не будет ни одной ставки!
    # image.save(r'images/01/' + caption + '.png')
    size_200 = (image.width * 2, image.height * 2)
    # transform scale200
    T_scale_200 = np.array([
        [0.5, 0, 0],
        [0, 0.5, 0],
        [0, 0, 1]])
    # filter+gray+BW
    thresh = 100
    f_BW = lambda x: 255 if x > thresh else 0
    image_AFBI200 = image.transform(size_200, Image.AFFINE,
                                    data=T_scale_200.flatten()[:6],
                                    resample=Image.BICUBIC)
    # SHARPEN
    image_AFBI200_SH_BW = image_AFBI200.filter(ImageFilter.SHARPEN).convert('L').point(f_BW, mode='1')
    # image_AFBI200_SH_BW.save(r'images/01/' + caption + '_AFBI200_SH_BW.png')
    # Numpy
    image_w, image_h = image_AFBI200_SH_BW.size  # (320, 28)
    image_array = np.asarray(image_AFBI200_SH_BW)
    image_array = image_array.copy()
    size_x = 12
    size_y = 20 + 1  # снизу 1 ряд черных точек, чтобы исключить фишки
    # проход image_AFBI200_SH_BW
    row = 0
    row_next = False
    sep = 0
    sep_go = False
    while row < image_h - size_y + 1:
        col = 0
        while col < image_w - size_x + 1:
            # новый массив
            image_array_size_xy = image_array[row:row + size_y, col:col + size_x]
            if check_bets_array(image_array_size_xy, bets_list_str, row_next):
                col += size_x + 2  # (подобрать значение между цифрами!)
                sep = 0
                sep_go = True
                row_next = True
            col += 1
            # проверка на разделитель
            if sep_go:
                sep += 1
                if sep > 5:  # (подобрать значение между цифрами!)
                    break
        if row_next:
            break
        row += 1
    # bets_list_str -> bets_digit
    bets_digit = float(''.join(str(i) for i in bets_list_str))
    return bets_digit


def check_cards_board_array(array_size_xy, cards_board_list_str):
    # speed
    errors_s = 2
    # Black_s
    row_sF = np.array([0, 0,  0,  0,  0,  0,  0], int)
    col_sF = np.array([0, 6, 12, 18, 24, 30, 35], int)
    im_array_sF = array_size_xy[row_sF, col_sF]
    find = sum(im_array_sF) < errors_s
    if find:
        return False

    # '2'
    errors_2 = 1
    # Black_2
    row_2F = np.array([0,  0, 15, 15, 24, 32, 39, 39, 39], int)
    col_2F = np.array([0, 35, 13, 23,  0, 35, 14, 24, 35], int)
    # White_2
    row_2T = np.array([ 0, 14, 14, 26, 32, 41, 49, 49, 49], int)
    col_2T = np.array([19,  4, 35, 27,  6,  4,  1, 17, 35], int)
    im_array_2F = array_size_xy[row_2F, col_2F]
    im_array_2T = array_size_xy[row_2T, col_2T]
    find = (sum(im_array_2F) <= errors_2) and (sum(im_array_2T) >= col_2T.size - errors_2)
    if find:
        cards_board_list_str.append('2')
        return True

    # '3'
    errors_3 = 0
    # Black_3
    row_3F = np.array([0,  0, 13, 24, 24, 24, 36, 49, 49, 20], int)
    col_3F = np.array([0, 35, 17,  0, 10, 35, 17,  0, 35, 11], int)
    # White_3
    row_3T = np.array([ 0, 12, 12, 24, 38, 38, 49], int)
    col_3T = np.array([18,  3, 35, 20,  3, 35, 18], int)
    im_array_3F = array_size_xy[row_3F, col_3F]
    im_array_3T = array_size_xy[row_3T, col_3T]
    find = (sum(im_array_3F) <= errors_3) and (sum(im_array_3T) >= col_3T.size - errors_3)
    if find:
        cards_board_list_str.append('3')
        return True

    # '4'
    errors_4 = 0
    # Black_4
    row_4F = np.array([0,  0, 17, 17, 29, 29, 49, 49, 49], int)
    col_4F = np.array([0, 13,  0, 20, 11, 20,  0, 20, 35], int)
    # White_4
    row_4T = np.array([ 0, 17, 17, 34, 34, 49], int)
    col_4T = np.array([29, 16, 29,  1, 29, 29], int)
    im_array_4F = array_size_xy[row_4F, col_4F]
    im_array_4T = array_size_xy[row_4T, col_4T]
    find = (sum(im_array_4F) <= errors_4) and (sum(im_array_4T) >= col_4T.size - errors_4)
    if find:
        cards_board_list_str.append('4')
        return True

    # '5'
    errors_5 = 0
    # Black_5
    row_5F = np.array([11, 11, 26, 30, 38, 49, 49], int)
    col_5F = np.array([15, 35, 18,  0, 18,  0, 35], int)
    # White_5
    row_5T = np.array([0,  0, 12, 19, 19, 27, 40, 40, 49], int)
    col_5T = np.array([0, 30,  0,  0, 18, 31,  0, 31, 18], int)
    im_array_5F = array_size_xy[row_5F, col_5F]
    im_array_5T = array_size_xy[row_5T, col_5T]
    find = (sum(im_array_5F) <= errors_5) and (sum(im_array_5T) >= col_5T.size - errors_5)
    if find:
        cards_board_list_str.append('5')
        return True

    # '6'
    errors_6 = 0
    # Black_6
    row_6F = np.array([0,  0, 10, 16, 17, 30, 38, 49, 49], int)
    col_6F = np.array([0, 35, 18, 18, 32, 17, 17,  0, 35], int)
    # White_6
    row_6T = np.array([ 0, 9,  9, 15, 22, 22, 34, 34, 49], int)
    col_6T = np.array([18, 0, 32,  0,  0, 20,  0, 35, 18], int)
    im_array_6F = array_size_xy[row_6F, col_6F]
    im_array_6T = array_size_xy[row_6T, col_6T]
    find = (sum(im_array_6F) <= errors_6) and (sum(im_array_6T) >= col_6T.size - errors_6)
    if find:
        cards_board_list_str.append('6')
        return True

    # '7'
    errors_7 = 0
    # Black_7
    row_7F = np.array([13, 13, 13, 30, 30, 30, 49, 49], int)
    col_7F = np.array([ 0,  9, 19,  0, 11, 35,  0, 27], int)
    # White_7
    row_7T = np.array([0,  0,  0, 18, 31, 49], int)
    col_7T = np.array([0, 17, 35, 27, 20, 13], int)
    im_array_7F = array_size_xy[row_7F, col_7F]
    im_array_7T = array_size_xy[row_7T, col_7T]
    find = (sum(im_array_7F) <= errors_7) and (sum(im_array_7T) >= col_7T.size - errors_7)
    if find:
        cards_board_list_str.append('7')
        return True

    # '8'
    errors_8 = 0
    # Black_8
    row_8F = np.array([0,  0, 13, 24, 24, 35, 49, 49], int)
    col_8F = np.array([0, 35, 17,  0, 35, 17,  0, 35], int)
    # White_8
    row_8T = np.array([ 0, 13, 13, 19, 24, 37, 37, 49], int)
    col_8T = np.array([17,  0, 35,  5, 17,  0, 35, 17], int)
    im_array_8F = array_size_xy[row_8F, col_8F]
    im_array_8T = array_size_xy[row_8T, col_8T]
    find = (sum(im_array_8F) <= errors_8) and (sum(im_array_8T) >= col_8T.size - errors_8)
    if find:
        cards_board_list_str.append('8')
        return True

    # '9'
    errors_9 = 0
    # Black_9
    row_9F = np.array([0,  0, 15, 32, 36, 49, 49], int)
    col_9F = np.array([0, 35, 17,  0, 17,  0, 35], int)
    # White_9
    row_9T = np.array([ 0, 14, 14, 27, 27, 40, 40, 49], int)
    col_9T = np.array([16,  0, 35, 15, 35,  3, 31, 16], int)
    im_array_9F = array_size_xy[row_9F, col_9F]
    im_array_9T = array_size_xy[row_9T, col_9T]
    find = (sum(im_array_9F) <= errors_9) and (sum(im_array_9T) >= col_9T.size - errors_9)
    if find:
        cards_board_list_str.append('9')
        return True

    # '10'
    errors_10 = 0
    # Black_10
    row_10F = np.array([0, 12, 12, 23, 23, 37, 37, 49], int)
    col_10F = np.array([9,  9, 27,  9, 27,  9, 27,  9], int)
    # White_10
    row_10T = np.array([0,  0, 12, 12, 23, 23, 37, 37, 49, 49], int)
    col_10T = np.array([3, 27,  3, 15,  3, 15,  3, 15,  3, 27], int)
    im_array_10F = array_size_xy[row_10F, col_10F]
    im_array_10T = array_size_xy[row_10T, col_10T]
    find = (sum(im_array_10F) <= errors_10) and (sum(im_array_10T) >= col_10T.size - errors_10)
    if find:
        cards_board_list_str.append('10')
        return True

    # 'J'
    errors_J = 0
    # Black_J
    row_JF = np.array([0,  0,  0, 13, 13, 13, 26, 26, 26, 36, 36, 49, 49], int)
    col_JF = np.array([0, 10, 20,  0, 10, 20,  0, 10, 20,  0, 20,  0, 35], int)
    # White_J
    row_JT = np.array([ 0, 13, 23, 35, 35, 49], int)
    col_JT = np.array([31, 31, 31,  8, 31, 20], int)
    im_array_JF = array_size_xy[row_JF, col_JF]
    im_array_JT = array_size_xy[row_JT, col_JT]
    find = (sum(im_array_JF) <= errors_J) and (sum(im_array_JT) >= col_JT.size - errors_J)
    if find:
        cards_board_list_str.append('11')
        return True

    # 'Q'
    errors_Q = 0
    # Black_Q
    row_QF = np.array([0,  0, 15, 15, 25, 25, 30, 38, 49, 49], int)
    col_QF = np.array([0, 35, 11, 25, 11, 25, 11, 16,  0, 35], int)
    # White_Q
    row_QT = np.array([ 0, 12, 12, 21, 21, 31, 31, 31, 43, 43, 49], int)
    col_QT = np.array([18,  0, 35,  0, 35,  0, 20, 35,  6, 28, 18], int)
    im_array_QF = array_size_xy[row_QF, col_QF]
    im_array_QT = array_size_xy[row_QT, col_QT]
    find = (sum(im_array_QF) <= errors_Q) and (sum(im_array_QT) >= col_QT.size - errors_Q)
    if find:
        cards_board_list_str.append('12')
        return True

    # 'K'
    errors_K = 0
    # Black_K
    row_KF = np.array([ 0,  0, 12, 12, 24, 24, 37, 37, 49, 49], int)
    col_KF = np.array([10, 20, 10, 35, 22, 35, 10, 35, 10, 20], int)
    # White_K
    row_KT = np.array([0,  0, 12, 12, 24, 24, 38, 38, 49, 49], int)
    col_KT = np.array([3, 30,  3, 21,  3, 12,  3, 23,  3, 35], int)
    im_array_KF = array_size_xy[row_KF, col_KF]
    im_array_KT = array_size_xy[row_KT, col_KT]
    find = (sum(im_array_KF) <= errors_K) and (sum(im_array_KT) >= col_KT.size - errors_K)
    if find:
        cards_board_list_str.append('13')
        return True

    # 'A'
    errors_A = 0
    # Black_A
    row_AF = np.array([0,  0, 12, 12, 27, 27, 27, 49, 49], int)
    col_AF = np.array([0, 35,  0, 35,  0, 18, 35, 10, 25], int)
    # White_A
    row_AT = np.array([ 0, 13, 13, 25, 25, 37, 37, 37, 49, 49], int)
    col_AT = np.array([18, 11, 24,  8, 27,  4, 18, 32,  0, 35], int)
    im_array_AF = array_size_xy[row_AF, col_AF]
    im_array_AT = array_size_xy[row_AT, col_AT]
    find = (sum(im_array_AF) <= errors_A) and (sum(im_array_AT) >= col_AT.size - errors_A)
    if find:
        cards_board_list_str.append('14')
        return True
    return False


def check_suits_board(image):
    # real suits colors
    suit_h_arr = np.array([151, 67, 67], int)
    suit_c_arr = np.array([108, 161, 74], int)
    suit_d_arr = np.array([75, 131, 147], int)
    suit_s_arr = np.array([104, 104, 104], int)
    suit___arr = np.array([30, 30, 30], int)

    suit_arr = []
    suit_arr.append(np.array(list(image.getpixel((63 * 0, 0))), int))
    suit_arr.append(np.array(list(image.getpixel((63 * 1, 0))), int))
    suit_arr.append(np.array(list(image.getpixel((63 * 2, 0))), int))
    suit_arr.append(np.array(list(image.getpixel((63 * 3, 0))), int))
    suit_arr.append(np.array(list(image.getpixel((63 * 4, 0))), int))

    suits = []
    for i in range(0, 5):
        suits.append('')
        dif_least = 1000
        # hearts
        dif = math.fabs(suit_arr[i][0] - suit_h_arr[0]) + \
              math.fabs(suit_arr[i][1] - suit_h_arr[1]) + \
              math.fabs(suit_arr[i][2] - suit_h_arr[2])
        if dif < dif_least:
            suits[i] = 'h'
            dif_least = dif
        # clubs
        dif = math.fabs(suit_arr[i][0] - suit_c_arr[0]) + \
              math.fabs(suit_arr[i][1] - suit_c_arr[1]) + \
              math.fabs(suit_arr[i][2] - suit_c_arr[2])
        if dif < dif_least:
            suits[i] = 'c'
            dif_least = dif
        # diamonds
        dif = math.fabs(suit_arr[i][0] - suit_d_arr[0]) + \
              math.fabs(suit_arr[i][1] - suit_d_arr[1]) + \
              math.fabs(suit_arr[i][2] - suit_d_arr[2])
        if dif < dif_least:
            suits[i] = 'd'
            dif_least = dif
        # spades
        dif = math.fabs(suit_arr[i][0] - suit_s_arr[0]) + \
              math.fabs(suit_arr[i][1] - suit_s_arr[1]) + \
              math.fabs(suit_arr[i][2] - suit_s_arr[2])
        if dif < dif_least:
            suits[i] = 's'
            dif_least = dif
        # none
        dif = math.fabs(suit_arr[i][0] - suit___arr[0]) + \
              math.fabs(suit_arr[i][1] - suit___arr[1]) + \
              math.fabs(suit_arr[i][2] - suit___arr[2])
        if dif < dif_least:
            suits[i] = '-'
    return suits


def check_cards_board(image, caption, cards_to_find):  # im01_CR
    if not cards_to_find:
        return ['-', '-', '-', '-', '-']

    cards_board_list_str = []

    # image.save(r'images/01/' + caption + '.png')
    size_200 = (image.width * 2, image.height * 2)
    # transform scale200
    T_scale_200 = np.array([
        [0.5, 0, 0],
        [0, 0.5, 0],
        [0, 0, 1]])
    # filter+gray+BW
    thresh = 200
    f_BW = lambda x: 255 if x > thresh else 0
    image_AFBI200 = image.transform(size_200, Image.AFFINE,
                                    data=T_scale_200.flatten()[:6],
                                    resample=Image.BICUBIC)
    # SHARPEN
    image_AFBI200_SH_BW = image_AFBI200.filter(ImageFilter.SHARPEN).convert('L').point(f_BW, mode='1')
    # image_AFBI200_SH_BW.save(r'images/01/' + caption + '_AFBI200_SH_BW.png')
    # Numpy
    image_w, image_h = image_AFBI200_SH_BW.size  # (600, 64)
    image_array = np.asarray(image_AFBI200_SH_BW)
    image_array = image_array.copy()
    size_x = 36
    size_y = 50
    # проход image_AFBI200_SH_BW
    row = 0
    row_next = False
    cards_found = 0
    while row < image_h - size_y + 1:
        col = 0
        while col < image_w - size_x + 1:
            # новый массив
            image_array_size_xy = image_array[row:row + size_y, col:col + size_x]
            if check_cards_board_array(image_array_size_xy, cards_board_list_str):
                col += 118  # (подобрать значение между цифрами!)
                row_next = True
                cards_found += 1
                if cards_found == cards_to_find:
                    break
            col += 1
        if row_next:
            break
        row += 1
    # заполним массив недостоющими '-'
    for i in range(0, 5 - cards_to_find):
        cards_board_list_str.append('-')
    return cards_board_list_str


def check_suits_my(image):
    # real suits colors
    suit_h_arr = np.array([151, 67, 67], int)
    suit_c_arr = np.array([108, 161, 74], int)
    suit_d_arr = np.array([75, 131, 147], int)
    suit_s_arr = np.array([104, 104, 104], int)
    suit___arr = np.array([30, 30, 30], int)

    suit_arr = []
    suit_arr.append(np.array(list(image.getpixel((61 * 0, 0))), int))
    suit_arr.append(np.array(list(image.getpixel((61 * 1, 0))), int))

    suits = []
    for i in range(0, 2):
        suits.append('')
        dif_least = 1000
        # hearts
        dif = math.fabs(suit_arr[i][0] - suit_h_arr[0]) + \
              math.fabs(suit_arr[i][1] - suit_h_arr[1]) + \
              math.fabs(suit_arr[i][2] - suit_h_arr[2])
        if dif < dif_least:
            suits[i] = 'h'
            dif_least = dif
        # clubs
        dif = math.fabs(suit_arr[i][0] - suit_c_arr[0]) + \
              math.fabs(suit_arr[i][1] - suit_c_arr[1]) + \
              math.fabs(suit_arr[i][2] - suit_c_arr[2])
        if dif < dif_least:
            suits[i] = 'c'
            dif_least = dif
        # diamonds
        dif = math.fabs(suit_arr[i][0] - suit_d_arr[0]) + \
              math.fabs(suit_arr[i][1] - suit_d_arr[1]) + \
              math.fabs(suit_arr[i][2] - suit_d_arr[2])
        if dif < dif_least:
            suits[i] = 'd'
            dif_least = dif
        # spades
        dif = math.fabs(suit_arr[i][0] - suit_s_arr[0]) + \
              math.fabs(suit_arr[i][1] - suit_s_arr[1]) + \
              math.fabs(suit_arr[i][2] - suit_s_arr[2])
        if dif < dif_least:
            suits[i] = 's'
            dif_least = dif
        # none
        dif = math.fabs(suit_arr[i][0] - suit___arr[0]) + \
              math.fabs(suit_arr[i][1] - suit___arr[1]) + \
              math.fabs(suit_arr[i][2] - suit___arr[2])
        if dif < dif_least:
            suits[i] = '-'
    return suits


def check_cards_my(image, caption, cards_to_find):  # im01_CR
    cards_my_list_str = []

    # image.save(r'images/01/' + caption + '.png')
    size_200 = (image.width * 2, image.height * 2)
    # transform scale200
    T_scale_200 = np.array([
        [0.5, 0, 0],
        [0, 0.5, 0],
        [0, 0, 1]])
    # filter+gray+BW
    thresh = 200
    f_BW = lambda x: 255 if x > thresh else 0
    image_AFBI200 = image.transform(size_200, Image.AFFINE,
                                    data=T_scale_200.flatten()[:6],
                                    resample=Image.BICUBIC)
    # SHARPEN
    image_AFBI200_SH_BW = image_AFBI200.filter(ImageFilter.SHARPEN).convert('L').point(f_BW, mode='1')
    # image_AFBI200_SH_BW.save(r'images/01/' + caption + '_AFBI200_SH_BW.png')
    # Numpy
    image_w, image_h = image_AFBI200_SH_BW.size  # (240, 64)
    image_array = np.asarray(image_AFBI200_SH_BW)
    image_array = image_array.copy()
    size_x = 36
    size_y = 50
    # проход image_AFBI200_SH_BW
    row = 0
    row_next = False
    cards_found = 0
    while row < image_h - size_y + 1:
        col = 0
        while col < image_w - size_x + 1:
            # новый массив
            image_array_size_xy = image_array[row:row + size_y, col:col + size_x]
            if check_cards_board_array(image_array_size_xy, cards_my_list_str):
                col += 115  # (подобрать значение между цифрами!)
                row_next = True
                cards_found += 1
                if cards_found == cards_to_find:
                    break
            col += 1
        if row_next:
            break
        row += 1
    # заполним массив недостоющими '-'
    for i in range(0, 2 - cards_to_find):
        cards_my_list_str.append('-')
    return cards_my_list_str


def check_my_turn(image):
    # real suits colors
    suit_mt_arr = np.array([123, 23, 14], int)  # red
    suit_01_arr = np.array([27,  28, 32], int)  # empty space between gray boxes
    suit_02_arr = np.array([54,  55, 58], int)  # gray box

    suit_arr = []
    buttons = []  # проверим наличие хотя бы одной кнопки
    # 1-я кнопка (2-я отсутствует когда противник All-In)
    # 2-я кнопка (1-я Fold отсутствует когда мой ход первый)
    suit_arr.append(np.array(list(image.getpixel((0, 0))), int))  # 1st button
    suit_arr.append(np.array(list(image.getpixel((160, 0))), int))  # 2nd button

    for i in range(0, 2):
        dif_least = 1000
        button = True
        dif = math.fabs(suit_arr[i][0] - suit_mt_arr[0]) + \
              math.fabs(suit_arr[i][1] - suit_mt_arr[1]) + \
              math.fabs(suit_arr[i][2] - suit_mt_arr[2])
        if dif < dif_least:
            button = True
            dif_least = dif
        # none01
        dif = math.fabs(suit_arr[i][0] - suit_01_arr[0]) + \
              math.fabs(suit_arr[i][1] - suit_01_arr[1]) + \
              math.fabs(suit_arr[i][2] - suit_01_arr[2])
        if dif < dif_least:
            button = False
        # none02
        dif = math.fabs(suit_arr[i][0] - suit_02_arr[0]) + \
              math.fabs(suit_arr[i][1] - suit_02_arr[1]) + \
              math.fabs(suit_arr[i][2] - suit_02_arr[2])
        if dif < dif_least:
            button = False
        buttons.append(button)
    return True in buttons
