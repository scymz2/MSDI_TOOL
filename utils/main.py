# Mochuan Zhan , 2022/ 7/15 The University of Manchester
# UTF- 8

from utils.calibration import Calibration
from utils.map import Map
from utils.myexif import *
from utils.config import WIDTH
from utils.config import HEIGHT
from utils.config import CHECKER_BOARD_PATH
from utils.config import RAW_IMAGE_FILE
from utils.config import CALIBRATED_FILE
from utils.config import GOOGLE_STATIC_MAP_FILE
from utils.config import GOOGLE_ADVANCE_STATIC_MAP_FILE
from utils.config import BING_ADVANCE_STATIC_MAP_FILE
from utils.config import ARTIST
from utils.config import COPYRIGHT
from utils.config import USER_COMMENT

if __name__ == "__main__":
    print("add information to raw images!")
    content = {'artist': ARTIST, 'copyright': COPYRIGHT, 'user_comment': 'RAW IMAGE'}
    modify_exif(RAW_IMAGE_FILE, content)

    calib = Calibration()
    print("start create calibrate model!")
    calib.create_model(WIDTH, HEIGHT, CHECKER_BOARD_PATH)

    print("start undistort!")
    calib.undistort(RAW_IMAGE_FILE, CALIBRATED_FILE)

    print("copy exif to calibrated images!")
    copy_exif(RAW_IMAGE_FILE, CALIBRATED_FILE)
    modify_exif(CALIBRATED_FILE, {'artist': ARTIST, 'copyright': COPYRIGHT, 'user_comment': USER_COMMENT})

    print("get static google map!")
    map = Map(CALIBRATED_FILE, GOOGLE_STATIC_MAP_FILE)
    map.get_maps(advance=0)

    print("get advance static google map")
    ad_map = Map(CALIBRATED_FILE, GOOGLE_ADVANCE_STATIC_MAP_FILE, 'google')
    ad_map.get_maps(advance=1)

    print("get advance static bing map")
    ad_map = Map(CALIBRATED_FILE, BING_ADVANCE_STATIC_MAP_FILE, 'bing')
    ad_map.get_maps(advance=1)



