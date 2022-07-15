# Mochuan Zhan , 2022/ 7/15 The university of manchester
from utils.config import GOOGLE_API_KEY
from utils.config import BING_API_KEY
from utils.config import GOOGLE_URL
from utils.config import BING_URL
from utils.config import CALIBRATED_FILE
from utils.config import GOOGLE_ADVANCE_STATIC_MAP_FILE
from utils.config import BING_ADVANCE_STATIC_MAP_FILE
from utils.myexif import get_GPS
import numpy as np
import requests
import glob
import os
import cv2


def mkdir(path):
    """
    This function is used to create an empty file
    :param path: file path
    :return: None
    """
    folder = os.path.exists(path)
    if not folder:
        os.makedirs(path)
        print("folder created:")
        print(path)
    else:
        pass


def byte_2_img(request):
    """
    This function transfer byte file into image file
    :param request: image request instance
    :return: image format data
    """
    # byte to image
    img = np.asarray(bytearray(request.content), dtype='uint8')
    img = cv2.imdecode(img, cv2.IMREAD_COLOR)
    return img


def cal_correlation_coefficient(a, b):
    """
    This function calculates the correlation coefficient of two arrays (two lines of images that need to be matched)
    :param a: array 1 (a line of image 1)
    :param b: array 2 (a line of image 2)
    :return: the correlation coefficient between two lines
    """
    dev_a = a - np.mean(a)
    dev_b = b - np.mean(b)
    # co-variance
    cov_ab = np.mean(dev_a * dev_b)
    cov_ba = np.mean(dev_b * dev_a)
    # standard derivation
    std_a = np.std(a)
    std_b = np.std(b)
    # correlation coefficient
    cc_ab = cov_ab / (std_a * std_b)
    cc_ba = cov_ba / (std_b * std_a)

    return cc_ab


def find_stitch_index(img1, img2, orientation):
    """
    This function is used for searching the indexes of the first corresponding position in two images, just like find
    out where to stitch two images which needs no homography calculation.
    :param img1: image data 1
    :param img2: image data 2
    :param orientation: 0 stands for horizontal and 1 stands for vertical
    :return: return the matched line index in the second image
    """
    if orientation == 0:
        for i in range(len(img1)):
            for j in range(len(img2)):
                # calculate the co-variance
                cur = cal_correlation_coefficient(img1[i], img2[j])
                if cur > 0.99:
                    nex = cal_correlation_coefficient(img1[i], img2[j + 1])
                    if nex > cur:
                        continue
                    else:
                        return j - i

    elif orientation == 1:
        for x in range(len(img1[0])):
            for y in range(len(img2[0])):
                # if find the same column
                cur = cal_correlation_coefficient(img1[:, x], img2[:, y])
                if cur > 0.99:
                    nex = cal_correlation_coefficient(img1[:, x], img2[:, y + 1])
                    if nex > cur:
                        continue
                    else:
                        return y - x


class Map:
    """
    This class is used for obtaining static map from Google or Bing, an API KEY is required if the user wants to use
    this class. In addition, this also provide the function to create higher resolution static map by stitching obtained
    static image, at the same time, removing watermark for better feature matching.
    """
    def __init__(self, source):
        self.cal_path = CALIBRATED_FILE
        self.center = ''
        self.source = source
        if source == 'google':
            self.sta_path = GOOGLE_ADVANCE_STATIC_MAP_FILE
            self.__key = GOOGLE_API_KEY
            self.url = GOOGLE_URL
            self.zoom = 19
            self.size = '640x640'
        elif source == 'bing':
            self.sta_path = BING_ADVANCE_STATIC_MAP_FILE
            self.__key = BING_API_KEY
            self.url = BING_URL
            self.zoom = 19
            # check source
        else:
            print("please input google or bing!")
            exit()

    def __request_bing_image(self, img, offset_lat=0, offset_lon=0):
        """
        request static map from BING MAP base on image's GPS coordinates
        :param img: Image data
        :param offset_lat: offset to latitude
        :param offset_lon: offset to longitude
        :return: request instance
        """
        GPS = get_GPS(img)
        # center defines the center of the map
        self.center = str(GPS['Latitude'] + offset_lat) + ',' + str(GPS['Longitude'] + offset_lon)
        http = self.url + self.center + '/' + str(self.zoom) + '?' + 'key=' + self.__key
        r = requests.get(http)
        print(http)
        return r

    def __request_google_image(self, img, offset_lat=0, offset_lon=0):
        """
        request static map from GOOGLE MAP base on image's GPS coordinates
        :param img: Image data
        :param offset_lat: offset to latitude
        :param offset_lon: offset to longitude
        :return: request instance
        """
        GPS = get_GPS(img)
        # center defines the center of the map
        self.center = str(GPS['Latitude'] + offset_lat) + ',' + str(GPS['Longitude'] + offset_lon)
        http = self.url + "&center=" + self.center + "&zoom=" + str(
            self.zoom) + "&size=" + self.size + "&key=" + self.__key
        r = requests.get(http)
        print(http)
        return r

    def __stitch_maps(self, img):
        """
        Stitch 3 * 3 static images into a higher resolution static map image.
        :param img: image data
        :return: stitched image data
        """
        func_dict = {"google": self.__request_google_image, "bing": self.__request_bing_image}
        size_dict = {"google": (640, 480), "bing": (350, 320)}

        # get x and y
        x = size_dict.get(self.source)[0]
        y = size_dict.get(self.source)[1]

        # map in the middle
        mid_r = func_dict.get(self.source)(img, 0, 0)
        mid = byte_2_img(mid_r)
        mid = mid[0:y, 0:x]
        # map in the bottom
        bot_r = func_dict.get(self.source)(img, -0.00027, 0)
        bot = byte_2_img(bot_r)
        bot = bot[0:y, 0:x]
        # map in the top
        top_r = func_dict.get(self.source)(img, 0.00029, 0)
        top = byte_2_img(top_r)
        top = top[0:y, 0:x]
        # map in the left
        left_r = func_dict.get(self.source)(img, 0, -0.00062)
        left = byte_2_img(left_r)
        left = left[0:y, 0:x]
        # map in the right
        right_r = func_dict.get(self.source)(img, 0, 0.00060)
        right = byte_2_img(right_r)
        right = right[0:y, 0:x]
        # map in the top left
        top_left_r = func_dict.get(self.source)(img, 0.00029, -0.00062)
        top_left = byte_2_img(top_left_r)
        top_left = top_left[0:y, 0:x]
        # map in the bottom left
        bot_left_r = func_dict.get(self.source)(img, -0.00027, -0.00062)
        bot_left = byte_2_img(bot_left_r)
        bot_left = bot_left[0:y, 0:x]
        # map in the top right
        top_right_r = func_dict.get(self.source)(img, 0.00029, 0.00060)
        top_right = byte_2_img(top_right_r)
        top_right = top_right[0:y, 0:x]
        # map in the bottom right
        bot_right_r = func_dict.get(self.source)(img, -0.00027, 0.00060)
        bot_right = byte_2_img(bot_right_r)
        bot_right = bot_right[0:y, 0:x]

        # find the stitch index for each image
        j1 = find_stitch_index(mid, top, 0)
        j2 = find_stitch_index(bot, mid, 0)
        j3 = find_stitch_index(mid, left, 1)
        j4 = find_stitch_index(right, mid, 1)

        # cut the map to correct size
        new_top = top[0:j1, 0:x]
        new_tleft = top_left[0:j1, 0:j3]
        new_tright = top_right[0:j1, x - j4:x]
        new_left = left[0:y, 0:j3]
        new_right = right[0:y, x - j4:x]
        new_bottom = bot[y - j2:y, 0:x]
        new_bleft = bot_left[y - j2:y, 0:j3]
        new_bright = bot_right[y - j2:y, x - j4:x]

        # concatenate maps
        img0 = np.concatenate([new_tleft, new_top, new_tright], 1)
        img1 = np.concatenate([new_left, mid, new_right], 1)
        img2 = np.concatenate([new_bleft, new_bottom, new_bright], 1)
        img3 = np.concatenate([img0, img1, img2], 0)

        return img3

    def get_maps(self, advance=0):
        """
        Base on user's requirements, obtain/create static map images from given drone images (Bing, Google, Stitched, Raw)
        :param advance: if advance = 0, raw static map, else, stitched map
        """
        # look through files
        fname_list = glob.glob(self.cal_path + '/*')
        for fname in fname_list:
            images = glob.glob(fname + '/*.jpg')
            # create static folders
            new_folder = fname.replace(self.cal_path, self.sta_path)
            mkdir(new_folder)
            for img in images:
                new_path = img.replace(self.cal_path, self.sta_path)
                if advance == 0:
                    func_dict = {'google': self.__request_google_image, 'bing': self.__request_bing_image}
                    r = func_dict.get(self.source)(img)
                    # save map
                    f = open(new_path, 'wb')
                    f.write(r.content)
                    f.close()
                elif advance == 1:
                    ad_map = self.__stitch_maps(img)
                    cv2.imwrite(new_path, ad_map)
                else:
                    print("please input 0 or 1!")
                    exit()
