# MSDI_TOOL

## 1.Introduction

This is the util tools for my MSC project: "Registration of UAV Imagery to Aerial and Satellite Imagery" at the university of manchester, supervised by Terence Patrick Morley.  

The basic idea of the project is to investigate various methods for the registration of downward-facing (nadir) drone imagery to higher altitude aerial and satellite imagery (Google, Bing), and possibly develop a system base on visual localization and navigation of drones (UAV) as opposed to using a satellite navigation system such as GPS.

## 2.Dataset 
The dataset used in this project is MSDI (Manchester Surface Drone Imagery) which collected and processed by myself.
The image dataset could be found using the DIO: or the Link:

The dataset contains totally 536 drone images of the city of manchester (447 downward facing and 89 45-degree forward facing) and 26 checkboard images taken by drone for camera calibration. 
 
## 3.File Structure
```
# The complete file structure (now only have utils)
.
├── README.md
├── data                                # Image dataset 
│   ├── bing_advance_static_images      # Stitched Bing static map without watermark
│   ├── calibrated_images               # Calibrated drone images
│   ├── checkboard_images               # Checkboard images taken by drone
│   ├── forward_45_images               # 45-degree forward facing drone images
│   ├── google_advance_static_images    # Stitched Google static map without watermark
│   ├── google_static_images            # Google static map with watermark
│   ├── raw_images                      # Raw drone images
│   └── README.txt                      
├── model
│   ├── model_distortion.txt            # data for drone image distortion
│   └── model_matrix.txt                # Camera parameter matrix 
├── utils
│   ├── calibration.py                  # Class for camera calibration and image distortion
│   ├── config.py                       # configuration file for utils tools
│   ├── GCP_selector.py                 # Ground control point selector for calculating reprojection error in feature matching
│   ├── main.py                         # main function
│   ├── map.py                          # Class for requesting static map from Google/Bing and creating advance maps
│   └── myexif.py                       # Class for obtaining/copying/modifying images' exif data
└── requirements.py

```

## 4.GCP selector 
GCP selector is a tool for selecting ground control points in two images that need to be matched. By calculating the homography and projecting one image to another, the average error of these GCPs could be calculated to represent the quality of the feature matching algorithm.

The user can select two images simultaneously and resize the first image. Resizing images is because comparing two images with very different amounts of information might be very difficult (according to my experience). Using GaussianBlur and Resize could reduce image information and get better matching results.

This is how I choose the parameter of GaussianBlur: `KERNEL = (WIDTH_1 // WIDTH_2) ^ 2 # WIDTH_1 > WIDTH_2`

The following code is a sample GCP.cfg file:

```python
# SRC,im_name,name (im_num can be 1 or 2.)
SRC1,EV_001.JPG
SRC2,EV_002.JPG

# GCP,im_num,x,y (im_num can be 1 or 2.  Order of im2 GCPs must be the same as those for im1.)
GCP,1,370,218
GCP,1,359,968
GCP,1,683,615
GCP,2,329,191
GCP,2,299,1052
GCP,2,678,660
```

## 5.Run util tool
1. install Python 3.7 and required packages ` pip install -r requirements`
2. apply for Google/Bing Static Map API KEY (Google is not free, but a free trial could be used for a couple of month)
3. modify config.py
```python

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

```
4. Run main.py
```python
if __name__ == "__main__":
    calib = Calibration()
    print("start create calibrate model!")
    calib.create_model(WIDTH, HEIGHT, CHECKER_BOARD_PATH) 

    print("start undistort!")
    calib.undistort(RAW_IMAGE_FILE, CALIBRATED_FILE)

    content = {'artist': ARTIST, 'copyright': COPYRIGHT, 'user_comment': USER_COMMENT}
    print("copy exif to calibrated images!")
    copy_exif(RAW_IMAGE_FILE, CALIBRATED_FILE)
    print("modify exif to calibrated images!")
    modify_exif(CALIBRATED_FILE, content)

    print("get static google map!")
    map = Map(CALIBRATED_FILE, GOOGLE_STATIC_MAP_FILE)
    map.get_maps(advance=0)

    print("get advance static google map")
    ad_map = Map(CALIBRATED_FILE, GOOGLE_ADVANCE_STATIC_MAP_FILE, 'google')
    ad_map.get_maps(advance=1)

    print("get advance static bing map")
    ad_map = Map(CALIBRATED_FILE, BING_ADVANCE_STATIC_MAP_FILE, 'bing')
    ad_map.get_maps(advance=1)
```

