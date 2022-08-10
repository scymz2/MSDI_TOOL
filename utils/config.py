# ==================== Width and Height of Checker Board ==========================
WIDTH = 9
HEIGHT = 6

# ==================== Preprocess Parameters ======================================
"""
To ensure that the two images to be matched have similar information, the drone images are resized to map image size.
The kernel size is calculated as follow: KERNEL[0] = (WIDTH_1 // WIDTH_2) ^ 2
"""
GAUSSIAN_KERNEL_BING = (9, 9)
GAUSSIAN_KERNEL_GOOGLE = (15, 15)
SIZE_BING = (800, 600)
SIZE_GOOGLE = (1536, 1152)

# ==================== File Paths =================================================
"""
PLEASE ADD ABSOLUTE PATHS HERE
"""
CHECKER_BOARD_PATH = r'PATH'
RAW_IMAGE_FILE = r'PATH'
CALIBRATED_FILE = r'PATH'
GOOGLE_STATIC_MAP_FILE = r'PATH'
GOOGLE_ADVANCE_STATIC_MAP_FILE = r'PATH'
BING_ADVANCE_STATIC_MAP_FILE = r'PATH'

# ==================== Calibration model path =====================================
"""
PLEASE ADD ABSOLUTE PATHS HERE
"""
MODEL_NAME = r'PATH'

# ==================== API KEY FOR GOOGLE MAP =====================================
GOOGLE_API_KEY = "INPUT YOUR API KEY HERE"
GOOGLE_URL = "http://maps.googleapis.com/maps/api/staticmap?maptype=satellite"

# ==================== API KEY FOR BING MAP =======================================
BING_API_KEY = "INPUT YOUR API KEY HERE"
BING_URL = "https://dev.virtualearth.net/REST/v1/Imagery/Map/Aerial/"

# ==================== exif data that you want to input ===========================
ARTIST = 'MOCHUAN ZHAN'
COPYRIGHT = 'THE UNIVERSITY OF MANCHESTER'
USER_COMMENT = 'CALIBRATED'
