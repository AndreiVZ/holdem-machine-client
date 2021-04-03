from PIL import Image
from PIL import ImageFilter
import numpy as np
import math


def check_inTG(image, caption):
    # image.save(rf'Rooms/Poker888/images/01/{caption}.png')
    size_200 = (image.width * 2, image.height * 2)
    # size_200 transform
    size_200_T = np.array([
        [0.5, 0, 0],
        [0, 0.5, 0],
        [0, 0, 1]])
    # SHARPEN filter + gray + BW
    threshold = 50
    f_BW = lambda x: 255 if x > threshold else 0
    image_AFBI = image.transform(size_200, Image.AFFINE,
                                 data=size_200_T.flatten()[:6],
                                 resample=Image.BICUBIC)
    image_AFBI_SH_BW = image_AFBI.filter(ImageFilter.SHARPEN).convert('L').point(f_BW, mode='1')
    # image_AFBI_SH_BW.save(rf'Rooms/Poker888/images/01/{caption}_{threshold:03d}.png')
    image_array = np.asarray(image_AFBI_SH_BW).copy()
    # image_array = image_array.copy()
    size_x = 1
    size_y = 1
    # проход image_AFBI_SH_BW
    row = 0
    col = 0
    image_array_size_xy = image_array[row:row + size_y, col:col + size_x]
    if check_inTG_array(image_array_size_xy):
        return True
    return False


def check_inTG_array(array_size_xy):
    errors = 0
    # black
    row_F = np.array([0], int)
    col_F = np.array([0], int)

    image_array_F = array_size_xy[row_F, col_F]
    find = (sum(image_array_F) <= errors)
    if find:
        return True
    return False


def check_bet_pot(image, caption):
    # image.save(rf'Rooms/Poker888/images/01/{caption}.png')
    size_200 = (image.width * 2, image.height * 2)
    # size_200 transform
    size_200_T = np.array([
        [0.5, 0, 0],
        [0, 0.5, 0],
        [0, 0, 1]])
    # SHARPEN filter + gray + BW
    threshold = 200
    f_BW = lambda x: 255 if x > threshold else 0
    image_AFBI = image.transform(size_200, Image.AFFINE,
                                 data=size_200_T.flatten()[:6],
                                 resample=Image.BICUBIC)
    image_AFBI_SH_BW = image_AFBI.filter(ImageFilter.SHARPEN).convert('L').point(f_BW, mode='1')
    # image_AFBI_SH_BW.save(rf'Rooms/Poker888/images/01/{caption}_{threshold:03d}.png')
    # Numpy
    image_w, image_h = image_AFBI_SH_BW.size
    image_array = np.asarray(image_AFBI_SH_BW).copy()
    size_x = 9
    size_y = 16  # + 1  # black row
    # проход image_AFBI_SH_BW
    bet_list_str = [0]  # [0] на случай, если не будет ни одной ставки!
    row = 0  # (подобрать значение!)
    row_next = False
    sep = 0
    sep_go = False
    while row < image_h - size_y + 1:
        col = 0
        while col < image_w - size_x + 1:
            # новый массив
            image_array_size_xy = image_array[row:row + size_y, col:col + size_x]
            if check_bet_pot_array(image_array_size_xy, bet_list_str, row_next):
                col += size_x + 1  # (подобрать значение между цифрами!)
                sep = 0
                sep_go = True
                row_next = True
            col += 1
            # проверка на разделитель
            if sep_go:
                sep += 1
                if sep > 5:  # (подобрать значение между цифрами!)
                    break
            # проверка на '.5'
            if bet_list_str.count('.5'):
                break
        if row_next:
            break
        row += 1
    # bet_list_str -> bet_digit
    bet_digit = float(''.join(str(i) for i in bet_list_str))
    return bet_digit


def check_bet_pot_array(array_size_xy, bet_list_str, row_next):
    # speed
    if not row_next:
        errors_s = 1
        # black_s
        row_sF = np.array([0, 0, 0, 0, 0, 0, 0], int)
        col_sF = np.array([0, 2, 3, 4, 5, 6, 8], int)

        image_array_sF = array_size_xy[row_sF, col_sF]
        find = sum(image_array_sF) < errors_s
        if find:
            return False

    # '0'
    errors_0 = 0
    # black_0
    row_0F = np.array([0, 0, 3, 5, 7, 9, 11], int)  # , 16, 16, 16, 16
    col_0F = np.array([0, 8, 4, 4, 4, 4, 4], int)  # ,  2,  4,  6,  8
    # white_0
    row_0T = np.array([0, 0, 3, 3, 7, 7, 11, 11, 15, 15], int)
    col_0T = np.array([3, 5, 0, 8, 0, 8, 0, 8, 3, 5], int)

    image_array_0F = array_size_xy[row_0F, col_0F]
    image_array_0T = array_size_xy[row_0T, col_0T]
    find = (sum(image_array_0F) <= errors_0) and (sum(image_array_0T) >= col_0T.size - errors_0)
    if find:
        bet_list_str.append('0')
        return True

    # '1'
    errors_1 = 0
    # black_1
    row_1F = np.array([0, 0, 3, 6, 6, 10, 10, 15, 15], int)
    col_1F = np.array([0, 8, 8, 0, 8, 0, 8, 0, 8], int)
    # white_1
    row_1T = np.array([0, 3, 3, 6, 10, 15], int)
    col_1T = np.array([5, 1, 5, 5, 5, 5], int)
    image_array_1F = array_size_xy[row_1F, col_1F]
    image_array_1T = array_size_xy[row_1T, col_1T]

    find = (sum(image_array_1F) <= errors_1) and (sum(image_array_1T) >= col_1T.size - errors_1)
    if find:
        bet_list_str.append('1')
        return True

    # '2'
    errors_2 = 1
    # black_2
    row_2F = np.array([0, 5, 5, 9, 10, 12, 12], int)
    col_2F = np.array([8, 0, 4, 0, 8, 4, 8], int)
    # white_2
    row_2T = np.array([0, 2, 3, 8, 11, 15, 15, 15], int)
    col_2T = np.array([4, 0, 7, 6, 3, 0, 4, 8], int)

    image_array_2F = array_size_xy[row_2F, col_2F]
    image_array_2T = array_size_xy[row_2T, col_2T]
    find = (sum(image_array_2F) <= errors_2) and (sum(image_array_2T) >= col_2T.size - errors_2)
    if find:
        bet_list_str.append('2')
        return True

    # '3'
    errors_3 = 0
    # black_3
    row_3F = np.array([0, 4, 4, 7, 7, 11, 11, 15], int)
    col_3F = np.array([8, 0, 4, 0, 8, 0, 4, 8], int)
    # white_3
    row_3T = np.array([0, 3, 8, 8, 12, 15, 15], int)
    col_3T = np.array([4, 8, 3, 5, 8, 1, 5], int)

    image_array_3F = array_size_xy[row_3F, col_3F]
    image_array_3T = array_size_xy[row_3T, col_3T]
    find = (sum(image_array_3F) <= errors_3) and (sum(image_array_3T) >= col_3T.size - errors_3)
    if find:
        bet_list_str.append('3')
        return True

    # '4'
    errors_4 = 0
    # black_4
    row_4F = np.array([0, 0, 5, 8, 15, 15], int)
    col_4F = np.array([0, 4, 0, 5, 0, 4], int)
    # white_4
    row_4T = np.array([0, 3, 3, 11, 11, 15], int)
    col_4T = np.array([7, 5, 8, 1, 8, 8], int)

    image_array_4F = array_size_xy[row_4F, col_4F]
    image_array_4T = array_size_xy[row_4T, col_4T]
    find = (sum(image_array_4F) <= errors_4) and (sum(image_array_4T) >= col_4T.size - errors_4)
    if find:
        bet_list_str.append('4')
        return True

    # '5'
    errors_5 = 0
    # black_5
    row_5F = np.array([4, 4, 10, 10, 15], int)
    col_5F = np.array([3, 8, 0, 4, 8], int)
    # white_5
    row_5T = np.array([1, 1, 4, 6, 7, 11, 15, 15], int)
    col_5T = np.array([1, 5, 0, 0, 6, 8, 2, 4], int)

    image_array_5F = array_size_xy[row_5F, col_5F]
    image_array_5T = array_size_xy[row_5T, col_5T]
    find = (sum(image_array_5F) <= errors_5) and (sum(image_array_5T) >= col_5T.size - errors_5)
    if find:
        bet_list_str.append('5')
        return True

    # '6'
    errors_6 = 0
    # black_6
    row_6F = np.array([0, 4, 4, 9, 11, 15, 15], int)
    col_6F = np.array([0, 3, 8, 3, 4, 0, 8], int)
    # white_6
    row_6T = np.array([0, 3, 8, 8, 12, 12, 15], int)
    col_6T = np.array([5, 1, 0, 8, 0, 8, 4], int)

    image_array_6F = array_size_xy[row_6F, col_6F]
    image_array_6T = array_size_xy[row_6T, col_6T]
    find = (sum(image_array_6F) <= errors_6) and (sum(image_array_6T) >= col_6T.size - errors_6)
    if find:
        bet_list_str.append('6')
        return True

    # '7'
    errors_7 = 0
    # black_7
    row_7F = np.array([4, 4, 7, 7, 11, 11, 13, 15], int)
    col_7F = np.array([0, 3, 0, 8, 0, 8, 0, 8], int)
    # white_7
    row_7T = np.array([1, 1, 1, 6, 11, 15], int)
    col_7T = np.array([0, 4, 8, 6, 4, 2], int)

    image_array_7F = array_size_xy[row_7F, col_7F]
    image_array_7T = array_size_xy[row_7T, col_7T]
    find = (sum(image_array_7F) <= errors_7) and (sum(image_array_7T) >= col_7T.size - errors_7)
    if find:
        bet_list_str.append('7')
        return True

    # '8'
    errors_8 = 0
    # black_8
    row_8F = np.array([0, 0, 4, 7, 7, 12], int)
    col_8F = np.array([0, 8, 4, 0, 8, 4], int)
    # white_8
    row_8T = np.array([0, 3, 3, 8, 8, 12, 12, 15], int)
    col_8T = np.array([4, 0, 8, 2, 5, 0, 8, 4], int)

    image_array_8F = array_size_xy[row_8F, col_8F]
    image_array_8T = array_size_xy[row_8T, col_8T]
    find = (sum(image_array_8F) <= errors_8) and (sum(image_array_8T) >= col_8T.size - errors_8)
    if find:
        bet_list_str.append('8')
        return True

    # '9'
    errors_9 = 0
    # black_9
    row_9F = np.array([0, 0, 5, 12, 12, 15], int)
    col_9F = np.array([0, 8, 4, 0, 4, 8], int)
    # white_9
    row_9T = np.array([0, 3, 3, 7, 7, 8, 11, 15, 15], int)
    col_9T = np.array([4, 0, 8, 0, 8, 4, 8, 1, 4], int)

    image_array_9F = array_size_xy[row_9F, col_9F]
    image_array_9T = array_size_xy[row_9T, col_9T]
    find = (sum(image_array_9F) <= errors_9) and (sum(image_array_9T) >= col_9T.size - errors_9)
    if find:
        bet_list_str.append('9')
        return True

    # '.X' any decimal
    if len(bet_list_str) > 1:
        errors_05 = 0
        # black_z
        row_zF = np.array([0, 2, 4, 6, 8, 10, 12, 0, 2, 4, 6, 8, 10, 12], int)
        col_zF = np.array([0, 0, 0, 0, 0, 0, 0, 2, 2, 2, 2, 2, 2, 2], int)
        # white_z
        row_zT = np.array([14, 15], int)
        col_zT = np.array([0, 0], int)

        image_array_zF = array_size_xy[row_zF, col_zF]
        image_array_zT = array_size_xy[row_zT, col_zT]
        find = (sum(image_array_zF) <= errors_05) and (sum(image_array_zT) >= col_zT.size - errors_05)
        if find:
            bet_list_str.append('.5')
            return True
    return False


def check_stack(image, caption):
    # image.save(rf'Rooms/Poker888/images/01/{caption}.png')
    size_200 = (image.width * 2, image.height * 2)
    # size_200 transform
    size_200_T = np.array([
        [0.5, 0, 0],
        [0, 0.5, 0],
        [0, 0, 1]])
    # SHARPEN filter + gray + BW
    threshold = 150
    f_BW = lambda x: 255 if x > threshold else 0
    image_AFBI = image.transform(size_200, Image.AFFINE,
                                 data=size_200_T.flatten()[:6],
                                 resample=Image.BICUBIC)
    image_AFBI_SH_BW = image_AFBI.filter(ImageFilter.SHARPEN).convert('L').point(f_BW, mode='1')
    # image_AFBI_SH_BW.save(rf'Rooms/Poker888/images/01/{caption}_{threshold:03d}.png')
    # Numpy
    image_w, image_h = image_AFBI_SH_BW.size
    image_array = np.asarray(image_AFBI_SH_BW).copy()
    size_x = 10
    size_y = 17
    # проход image_AFBI_SH_BW
    stack_list_str = [0]  # [0] на случай, если не будет ни одной ставки!
    row = 2  # (подобрать значение!)
    row_next = False
    sep = 0
    sep_go = False
    while row < image_h - size_y + 1:
        col = 0
        while col < image_w - size_x + 1:
            # новый массив
            image_array_size_xy = image_array[row:row + size_y, col:col + size_x]
            if check_stack_array(image_array_size_xy, stack_list_str, row_next):
                col += size_x + 1  # (подобрать значение между цифрами!)
                sep = 0
                sep_go = True
                row_next = True
            col += 1
            # проверка на разделитель
            if sep_go:
                sep += 1
                if sep > 5:  # (подобрать значение между цифрами!)
                    break
            # проверка на '.5'
            if stack_list_str.count('.5'):
                break
        if row_next:
            break
        row += 1
    # stack_list_str -> stack_digit
    stack_digit = float(''.join(str(i) for i in stack_list_str))
    return stack_digit


def check_stack_array(array_size_xy, stack_list_str, row_next):
    # speed
    if not row_next:
        errors_s = 1
        # black_s
        row_sF = np.array([0, 0, 0, 0, 0, 0, 0], int)
        col_sF = np.array([0, 2, 4, 5, 6, 8, 9], int)

        image_array_sF = array_size_xy[row_sF, col_sF]
        find = sum(image_array_sF) < errors_s
        if find:
            return False

    # '0'
    errors_0 = 0
    # black_0
    row_0F = np.array([0, 0, 5, 7, 9, 11, 16, 16], int)
    col_0F = np.array([0, 9, 4, 4, 4, 4, 0, 9], int)
    # white_0
    row_0T = np.array([0, 2, 2, 5, 5, 8, 8, 11, 11, 14, 14, 16], int)
    col_0T = np.array([4, 2, 7, 0, 9, 0, 9, 0, 9, 2, 7, 4], int)

    image_array_0F = array_size_xy[row_0F, col_0F]
    image_array_0T = array_size_xy[row_0T, col_0T]
    find = (sum(image_array_0F) <= errors_0) and (sum(image_array_0T) >= col_0T.size - errors_0)
    if find:
        stack_list_str.append('0')
        return True

    # '1'
    errors_1 = 0
    # black_1
    row_1F = np.array([0, 0, 7, 7, 11, 11, 16, 16], int)
    col_1F = np.array([0, 9, 0, 9, 0, 9, 0, 9], int)
    # white_1
    row_1T = np.array([0, 4, 4, 8, 12, 16], int)
    col_1T = np.array([6, 1, 6, 6, 6, 6], int)
    image_array_1F = array_size_xy[row_1F, col_1F]
    image_array_1T = array_size_xy[row_1T, col_1T]

    find = (sum(image_array_1F) <= errors_1) and (sum(image_array_1T) >= col_1T.size - errors_1)
    if find:
        stack_list_str.append('1')
        return True

    # '2'
    errors_2 = 1
    # black_2
    row_2F = np.array([0, 5, 5, 9, 11, 12, 12], int)
    col_2F = np.array([9, 0, 4, 0, 9, 6, 9], int)
    # white_2
    row_2T = np.array([0, 0, 2, 2, 4, 8, 13, 16, 16, 16], int)
    col_2T = np.array([2, 6, 1, 7, 9, 6, 2, 0, 4, 9], int)

    image_array_2F = array_size_xy[row_2F, col_2F]
    image_array_2T = array_size_xy[row_2T, col_2T]
    find = (sum(image_array_2F) <= errors_2) and (sum(image_array_2T) >= col_2T.size - errors_2)
    if find:
        stack_list_str.append('2')
        return True

    # '3'
    errors_3 = 0
    # black_3
    row_3F = np.array([0, 4, 4, 7, 7, 11, 11, 16], int)
    col_3F = np.array([9, 0, 4, 0, 9, 0, 4, 9], int)
    # white_3
    row_3T = np.array([0, 0, 4, 8, 8, 12, 16, 16], int)
    col_3T = np.array([2, 5, 9, 3, 6, 9, 2, 5], int)

    image_array_3F = array_size_xy[row_3F, col_3F]
    image_array_3T = array_size_xy[row_3T, col_3T]
    find = (sum(image_array_3F) <= errors_3) and (sum(image_array_3T) >= col_3T.size - errors_3)
    if find:
        stack_list_str.append('3')
        return True

    # '4'
    errors_4 = 0
    # black_4
    row_4F = np.array([0, 0, 5, 8, 16, 16], int)
    col_4F = np.array([0, 4, 0, 5, 0, 4], int)
    # white_4
    row_4T = np.array([0, 4, 4, 9, 9, 12, 12, 16], int)
    col_4T = np.array([8, 5, 8, 2, 8, 0, 8, 8], int)

    image_array_4F = array_size_xy[row_4F, col_4F]
    image_array_4T = array_size_xy[row_4T, col_4T]
    find = (sum(image_array_4F) <= errors_4) and (sum(image_array_4T) >= col_4T.size - errors_4)
    if find:
        stack_list_str.append('4')
        return True

    # '5'
    errors_5 = 0
    # black_5
    row_5F = np.array([4, 4, 11, 11, 16], int)
    col_5F = np.array([4, 9, 0, 3, 9], int)
    # white_5
    row_5T = np.array([0, 0, 4, 7, 7, 11, 14, 16], int)
    col_5T = np.array([1, 7, 0, 0, 5, 9, 6, 3], int)

    image_array_5F = array_size_xy[row_5F, col_5F]
    image_array_5T = array_size_xy[row_5T, col_5T]
    find = (sum(image_array_5F) <= errors_5) and (sum(image_array_5T) >= col_5T.size - errors_5)
    if find:
        stack_list_str.append('5')
        return True

    # '6'
    errors_6 = 0
    # black_6
    row_6F = np.array([0, 4, 4, 11, 16, 16], int)
    col_6F = np.array([0, 5, 9, 5, 0, 9], int)
    # white_6
    row_6T = np.array([0, 0, 3, 7, 7, 11, 11, 16], int)
    col_6T = np.array([5, 8, 2, 0, 5, 0, 9, 5], int)

    image_array_6F = array_size_xy[row_6F, col_6F]
    image_array_6T = array_size_xy[row_6T, col_6T]
    find = (sum(image_array_6F) <= errors_6) and (sum(image_array_6T) >= col_6T.size - errors_6)
    if find:
        stack_list_str.append('6')
        return True

    # '7'
    errors_7 = 0
    # black_7
    row_7F = np.array([5, 5, 10, 10, 16, 16], int)
    col_7F = np.array([0, 3, 0, 9, 6, 9], int)
    # white_7
    row_7T = np.array([0, 0, 4, 7, 11, 13, 16], int)
    col_7T = np.array([1, 8, 8, 7, 5, 3, 3], int)

    image_array_7F = array_size_xy[row_7F, col_7F]
    image_array_7T = array_size_xy[row_7T, col_7T]
    find = (sum(image_array_7F) <= errors_7) and (sum(image_array_7T) >= col_7T.size - errors_7)
    if find:
        stack_list_str.append('7')
        return True

    # '8'
    errors_8 = 0
    # black_8
    row_8F = np.array([0, 0, 4, 7, 7, 12, 16], int)
    col_8F = np.array([0, 9, 4, 0, 9, 4, 9], int)
    # white_8
    row_8T = np.array([0, 3, 3, 8, 8, 12, 12, 16], int)
    col_8T = np.array([4, 0, 9, 2, 6, 0, 9, 4], int)

    image_array_8F = array_size_xy[row_8F, col_8F]
    image_array_8T = array_size_xy[row_8T, col_8T]
    find = (sum(image_array_8F) <= errors_8) and (sum(image_array_8T) >= col_8T.size - errors_8)
    if find:
        stack_list_str.append('8')
        return True

    # '9'
    errors_9 = 0
    # black_9
    row_9F = np.array([0, 0, 5, 12, 12, 16], int)
    col_9F = np.array([0, 9, 4, 0, 4, 9], int)
    # white_9
    row_9T = np.array([0, 4, 4, 9, 9, 13, 16, 16], int)
    col_9T = np.array([4, 0, 9, 3, 9, 7, 1, 4], int)

    image_array_9F = array_size_xy[row_9F, col_9F]
    image_array_9T = array_size_xy[row_9T, col_9T]
    find = (sum(image_array_9F) <= errors_9) and (sum(image_array_9T) >= col_9T.size - errors_9)
    if find:
        stack_list_str.append('9')
        return True

    # '.X' any decimal
    if len(stack_list_str) > 1:
        errors_05 = 0
        # black_z
        row_zF = np.array([0, 2, 4, 6, 8, 10, 12, 0, 2, 4, 6, 8, 10, 12], int)
        col_zF = np.array([0, 0, 0, 0, 0, 0, 0, 2, 2, 2, 2, 2, 2, 2], int)
        # white_z
        row_zT = np.array([14, 16, 14, 16], int)
        col_zT = np.array([0, 0, 2, 2], int)

        image_array_zF = array_size_xy[row_zF, col_zF]
        image_array_zT = array_size_xy[row_zT, col_zT]
        find = (sum(image_array_zF) <= errors_05) and (sum(image_array_zT) >= col_zT.size - errors_05)
        if find:
            stack_list_str.append('.5')
            return True
    return False


def check_board_suits(image):
    # real suits colors
    suit_h_arr = np.array([233, 81, 61], int)
    suit_c_arr = np.array([37, 200, 36], int)
    suit_d_arr = np.array([39, 132, 205], int)
    suit_s_arr = np.array([68, 68, 68], int)
    suit___arr = np.array([0, 30, 40], int)

    suit_arr = []
    suit_arr.append(np.array(list(image.getpixel((20 + 41 * 0, 2))), int))
    suit_arr.append(np.array(list(image.getpixel((20 + 41 * 1, 2))), int))
    suit_arr.append(np.array(list(image.getpixel((20 + 41 * 2, 2))), int))
    suit_arr.append(np.array(list(image.getpixel((20 + 41 * 3, 2))), int))
    suit_arr.append(np.array(list(image.getpixel((20 + 41 * 4, 2))), int))

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


def check_my_suits(image):
    # real suits colors
    suit_h_arr = np.array([233, 81, 61], int)
    suit_c_arr = np.array([37, 200, 36], int)
    suit_d_arr = np.array([39, 132, 205], int)
    suit_s_arr = np.array([68, 68, 68], int)
    suit___arr = np.array([120, 230, 240], int)

    suit_arr = []
    suit_arr.append(np.array(list(image.getpixel((20 + 41 * 0, 12))), int))
    suit_arr.append(np.array(list(image.getpixel((20 + 41 * 1, 12))), int))

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


def check_card_ranks(image, caption, cards_to_find):  # im01_CR
    if not cards_to_find:
        return ['-', '-', '-', '-', '-']
    # image.save(rf'Rooms/Poker888/images/01/{caption}.png')
    size_200 = (image.width * 2, image.height * 2)
    # size_200 transform
    size_200_T = np.array([
        [0.5, 0, 0],
        [0, 0.5, 0],
        [0, 0, 1]])
    # SHARPEN filter + gray + BW
    threshold = 175
    f_BW = lambda x: 255 if x > threshold else 0
    image_AFBI = image.transform(size_200, Image.AFFINE,
                                 data=size_200_T.flatten()[:6],
                                 resample=Image.BICUBIC)
    image_AFBI_SH_BW = image_AFBI.filter(ImageFilter.SHARPEN).convert('L').point(f_BW, mode='1')
    # image_AFBI_SH_BW.save(rf'Rooms/Poker888/images/01/{caption}_{threshold:03d}.png')
    # Numpy
    image_w, image_h = image_AFBI_SH_BW.size
    image_array = np.asarray(image_AFBI_SH_BW).copy()
    size_x = 15
    size_y = 25
    # проход image_AFBI_SH_BW
    cards_board_list_str = []
    row = 5  # (подобрать значение!)
    row_next = False
    cards_found = 0
    while row < image_h - size_y + 1:
        col = 0
        while col < image_w - size_x + 1:
            # новый массив
            image_array_size_xy = image_array[row:row + size_y, col:col + size_x]
            if check_card_ranks_array(image_array_size_xy, cards_board_list_str):
                col += 60  # (подобрать значение между цифрами!)
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


def check_card_ranks_array(array_size_xy, cards_board_list_str):
    # speed
    errors_s = 2
    # black_s
    row_sF = np.array([0, 0, 0, 0, 0, 0, 0, 0], int)
    col_sF = np.array([0, 2, 4, 6, 8, 10, 12, 14], int)

    image_array_sF = array_size_xy[row_sF, col_sF]
    find = sum(image_array_sF) < errors_s
    if find:
        return False

    # '2'
    errors_2 = 0
    # black_2
    # row_2F = np.array([0,  0, 8, 14, 14, 17, 25, 25, 25], int)
    # col_2F = np.array([0, 14, 5,  0, 14, 12,  1,  7, 13], int)
    row_2F = np.array([0, 0, 8, 14, 14, 17], int)
    col_2F = np.array([0, 14, 5, 0, 14, 12], int)
    # white_2
    row_2T = np.array([0, 4, 4, 7, 11, 17, 23, 23, 23], int)
    col_2T = np.array([7, 1, 11, 13, 10, 6, 3, 8, 12], int)

    image_array_2F = array_size_xy[row_2F, col_2F]
    image_array_2T = array_size_xy[row_2T, col_2T]
    find = (sum(image_array_2F) <= errors_2) and (sum(image_array_2T) >= col_2T.size - errors_2)
    if find:
        cards_board_list_str.append('2')
        return True

    # '3'
    errors_3 = 0
    # black_3
    # row_3F = np.array([6,  6, 10, 10, 15, 24, 25, 25, 25, 25], int)
    # col_3F = np.array([1, 14,  0, 14,  0, 14,  1,  4,  7, 13], int)
    row_3F = np.array([6, 6, 10, 10, 15, 24], int)
    col_3F = np.array([1, 14, 0, 14, 0, 14], int)
    # white_3
    row_3T = np.array([0, 0, 4, 9, 12, 16, 22, 22], int)
    col_3T = np.array([3, 10, 9, 6, 11, 13, 2, 8], int)

    image_array_3F = array_size_xy[row_3F, col_3F]
    image_array_3T = array_size_xy[row_3T, col_3T]
    find = (sum(image_array_3F) <= errors_3) and (sum(image_array_3T) >= col_3T.size - errors_3)
    if find:
        cards_board_list_str.append('3')
        return True

    # '4'
    errors_4 = 0
    # black_4
    # row_4F = np.array([0, 0, 6, 22, 22, 25, 25, 25, 25], int)
    # col_4F = np.array([0, 5, 0,  0,  6,  1,  7, 11, 13], int)
    row_4F = np.array([0, 0, 6, 22, 22], int)
    col_4F = np.array([0, 5, 0, 0, 6], int)
    # white_4
    row_4T = np.array([0, 8, 8, 13, 13, 17, 17, 24], int)
    col_4T = np.array([12, 7, 13, 3, 12, 3, 12, 12], int)

    image_array_4F = array_size_xy[row_4F, col_4F]
    image_array_4T = array_size_xy[row_4T, col_4T]
    find = (sum(image_array_4F) <= errors_4) and (sum(image_array_4T) >= col_4T.size - errors_4)
    if find:
        cards_board_list_str.append('4')
        return True

    # '5'
    errors_5 = 0
    # black_5
    # row_5F = np.array([5,  5, 16, 16, 24, 24, 25, 25, 25, 25, 25], int)
    # col_5F = np.array([8, 14,  0,  6, 0,  14,  1,  4,  6,  8, 13], int)
    row_5F = np.array([5, 5, 16, 16, 24, 24], int)
    col_5F = np.array([8, 14, 0, 6, 0, 14], int)
    # white_5
    row_5T = np.array([0, 0, 6, 10, 10, 16, 21, 21, 24], int)
    col_5T = np.array([2, 11, 3, 3, 10, 12, 2, 10, 6], int)

    image_array_5F = array_size_xy[row_5F, col_5F]
    image_array_5T = array_size_xy[row_5T, col_5T]
    find = (sum(image_array_5F) <= errors_5) and (sum(image_array_5T) >= col_5T.size - errors_5)
    if find:
        cards_board_list_str.append('5')
        return True

    # '6'
    errors_6 = 0
    # black_6
    # row_6F = np.array([0,  0, 6,  6, 16, 24, 25, 25, 25, 25, 25], int)
    # col_6F = np.array([0, 14, 0, 14,  7, 14,  1,  5,  7,  9, 13], int)
    row_6F = np.array([0, 0, 6, 6, 16, 24], int)
    col_6F = np.array([0, 14, 0, 14, 7, 14], int)
    # white_6
    row_6T = np.array([0, 6, 10, 10, 16, 16, 21, 21, 23], int)
    col_6T = np.array([8, 6, 4, 10, 1, 13, 3, 11, 7], int)

    image_array_6F = array_size_xy[row_6F, col_6F]
    image_array_6T = array_size_xy[row_6T, col_6T]
    find = (sum(image_array_6F) <= errors_6) and (sum(image_array_6T) >= col_6T.size - errors_6)
    if find:
        cards_board_list_str.append('6')
        return True

    # '7'
    errors_7 = 0
    # black_7
    # row_7F = np.array([6, 6, 12, 12, 18, 18, 24, 24, 25, 25, 25, 25, 25], int)
    # col_7F = np.array([0, 5,  0, 14,  0, 14,  0, 14,  1,  2,  4,  6, 13], int)
    row_7F = np.array([6, 6, 12, 12, 18, 18, 24, 24], int)
    col_7F = np.array([0, 5, 0, 14, 0, 14, 0, 14], int)
    # white_7
    row_7T = np.array([0, 0, 6, 12, 17, 21, 24], int)
    col_7T = np.array([0, 13, 11, 8, 6, 5, 4], int)

    image_array_7F = array_size_xy[row_7F, col_7F]
    image_array_7T = array_size_xy[row_7T, col_7T]
    find = (sum(image_array_7F) <= errors_7) and (sum(image_array_7T) >= col_7T.size - errors_7)
    if find:
        cards_board_list_str.append('7')
        return True

    # '8'
    errors_8 = 0
    # black_8
    # row_8F = np.array([0,  0, 6, 11, 11, 17, 24, 24, 25, 25, 25, 25], int)
    # col_8F = np.array([0, 14, 7,  0, 14,  7,  0, 14,  1,  3, 10, 13], int)
    row_8F = np.array([0, 0, 6, 11, 11, 17, 24, 24], int)
    col_8F = np.array([0, 14, 7, 0, 14, 7, 0, 14], int)
    # white_8
    row_8T = np.array([0, 5, 5, 11, 17, 17, 21, 21, 24], int)
    col_8T = np.array([6, 1, 13, 7, 0, 14, 2, 11, 7], int)

    image_array_8F = array_size_xy[row_8F, col_8F]
    image_array_8T = array_size_xy[row_8T, col_8T]
    find = (sum(image_array_8F) <= errors_8) and (sum(image_array_8T) >= col_8T.size - errors_8)
    if find:
        cards_board_list_str.append('8')
        return True

    # '9'
    errors_9 = 0
    # black_9
    # row_9F = np.array([0,  0, 8, 17, 17, 24, 24, 25, 25, 25, 25, 25], int)
    # col_9F = np.array([0, 14, 7,  0, 14,  0, 14,  1,  4,  7,  8, 13], int)
    row_9F = np.array([0, 0, 8, 17, 17, 24, 24], int)
    col_9F = np.array([0, 14, 7, 0, 14, 0, 14], int)
    # white_9
    row_9T = np.array([0, 7, 7, 14, 14, 18, 24], int)
    col_9T = np.array([7, 0, 14, 5, 9, 8, 6], int)

    image_array_9F = array_size_xy[row_9F, col_9F]
    image_array_9T = array_size_xy[row_9T, col_9T]
    find = (sum(image_array_9F) <= errors_9) and (sum(image_array_9T) >= col_9T.size - errors_9)
    if find:
        cards_board_list_str.append('9')
        return True

    # '10'
    errors_10 = 0
    # black_10
    # row_10F = np.array([0, 4, 11, 11, 18, 24, 25, 25, 25, 25, 25], int)
    # col_10F = np.array([7, 6,  6, 14,  6,  7,  1,  3,  6,  9, 13], int)
    row_10F = np.array([0, 4, 11, 11, 18, 24], int)
    col_10F = np.array([7, 6, 6, 14, 6, 7], int)
    # white_10
    row_10T = np.array([0, 0, 5, 5, 11, 11, 18, 18, 24, 24], int)
    col_10T = np.array([2, 14, 2, 11, 2, 10, 2, 11, 2, 14], int)

    image_array_10F = array_size_xy[row_10F, col_10F]
    image_array_10T = array_size_xy[row_10T, col_10T]
    find = (sum(image_array_10F) <= errors_10) and (sum(image_array_10T) >= col_10T.size - errors_10)
    if find:
        cards_board_list_str.append('10')
        return True

    # 'J'
    errors_J = 0
    # black_J
    # row_JF = np.array([0, 0, 5, 5, 11, 11, 17, 17, 24, 24, 25, 25], int)
    # col_JF = np.array([0, 7, 0, 7,  0,  7,  0,  7,  0, 14,  4,  9], int)
    row_JF = np.array([0, 0, 0, 5, 5, 5, 11, 11, 11, 17, 17, 17, 24, 24], int)
    col_JF = np.array([0, 5, 14, 0, 5, 14, 0, 5, 14, 0, 5, 14, 0, 14], int)
    # white_J
    row_JT = np.array([0, 5, 11, 17, 21, 24], int)
    col_JT = np.array([11, 11, 11, 11, 9, 5], int)

    image_array_JF = array_size_xy[row_JF, col_JF]
    image_array_JT = array_size_xy[row_JT, col_JT]
    find = (sum(image_array_JF) <= errors_J) and (sum(image_array_JT) >= col_JT.size - errors_J)
    if find:
        cards_board_list_str.append('11')
        return True

    # 'Q'
    errors_Q = 0
    # black_Q
    # row_QF = np.array([0, 6, 10, 10, 13, 17, 24, 25, 25, 25, 25, 25], int)
    # col_QF = np.array([0, 8,  5, 10,  5,  6,  0,  1,  5,  7,  9, 13], int)
    row_QF = np.array([0, 6, 10, 10, 13, 17, 24], int)
    col_QF = np.array([0, 8, 5, 10, 5, 6, 0], int)
    # white_Q
    row_QT = np.array([0, 0, 4, 4, 8, 8, 15, 15, 20, 20, 24], int)
    col_QT = np.array([4, 11, 0, 14, 0, 14, 0, 14, 0, 14, 7], int)

    image_array_QF = array_size_xy[row_QF, col_QF]
    image_array_QT = array_size_xy[row_QT, col_QT]
    find = (sum(image_array_QF) <= errors_Q) and (sum(image_array_QT) >= col_QT.size - errors_Q)
    if find:
        cards_board_list_str.append('12')
        return True

    # 'K'
    errors_K = 0
    # black_K
    # row_KF = np.array([0, 4,  7, 14, 18, 24, 25, 25, 25, 25], int)
    # col_KF = np.array([6, 5, 14, 14,  5,  6,  0,  2, 12, 14], int)
    row_KF = np.array([0, 4, 7, 14, 18, 24], int)
    col_KF = np.array([6, 5, 14, 14, 5, 6], int)
    # white_K
    row_KT = np.array([0, 0, 5, 5, 11, 11, 19, 19, 24, 24], int)
    col_KT = np.array([1, 12, 0, 9, 0, 6, 0, 11, 1, 14], int)

    image_array_KF = array_size_xy[row_KF, col_KF]
    image_array_KT = array_size_xy[row_KT, col_KT]
    find = (sum(image_array_KF) <= errors_K) and (sum(image_array_KT) >= col_KT.size - errors_K)
    if find:
        cards_board_list_str.append('13')
        return True

    # 'A'
    errors_A = 0
    # black_A
    # row_AF = np.array([0,  0, 5, 13, 13, 24, 25, 25, 25, 25], int)
    # col_AF = np.array([0, 14, 0,  0,  9,  9,  0,  2,  4, 13], int)
    row_AF = np.array([0, 0, 5, 13, 13, 24], int)
    col_AF = np.array([0, 14, 0, 0, 9, 9], int)
    # white_A
    row_AT = np.array([0, 7, 7, 12, 12, 18, 18, 18, 21, 23], int)
    col_AT = np.array([9, 6, 12, 5, 14, 3, 8, 14, 14, 1], int)

    image_array_AF = array_size_xy[row_AF, col_AF]
    image_array_AT = array_size_xy[row_AT, col_AT]
    find = (sum(image_array_AF) <= errors_A) and (sum(image_array_AT) >= col_AT.size - errors_A)
    if find:
        cards_board_list_str.append('14')
        return True
    return False


def check_my_turn(image):
    # real suits colors
    suit_mt_arr = np.array([0, 90, 180], int)  # blue (My turn)
    suit____arr = np.array([80, 80, 80], int)  # gray

    suit_arr = []
    suit_arr.append(np.array(list(image.getpixel((0, 0))), int))
    my_turn = False
    for i in range(0, 1):
        dif_least = 1000
        # blue
        dif = math.fabs(suit_arr[i][0] - suit_mt_arr[0]) + \
              math.fabs(suit_arr[i][1] - suit_mt_arr[1]) + \
              math.fabs(suit_arr[i][2] - suit_mt_arr[2])
        if dif < dif_least:
            my_turn = True
            dif_least = dif
        # gray
        dif = math.fabs(suit_arr[i][0] - suit____arr[0]) + \
              math.fabs(suit_arr[i][1] - suit____arr[1]) + \
              math.fabs(suit_arr[i][2] - suit____arr[2])
        if dif < dif_least:
            my_turn = False
    return my_turn
