# Mochuan Zhan , 2022/ 7/15 The university of manchester

import numpy as np
import cv2 as cv
import glob
import os
from utils.config import MODEL_NAME

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


class Calibration:
    """
    This class is used for drone image calibration.
    The checkerboard images taken by the camera which needed to be calibrated is required.
    Once the calibration process is finished, two files - model_matrix.txt / model_distortion.txt will be generated
    for the undistortion step.
    """

    def __init__(self):
        self.model = MODEL_NAME

    def create_model(self, width, height, checkerboard):
        """
        This function creates calibration matrix and stores them with txt format
        :param width: width of checkerboard
        :param height: height of checkerboard
        :param checkerboard: the path of checkerboard image file
        """
        w = width
        h = height
        file_filter = checkerboard + '/*.jpg'
        model_name = self.model

        # termination criteria
        criteria = (cv.TERM_CRITERIA_EPS + cv.TERM_CRITERIA_MAX_ITER, 30, 0.001)

        # Defining the world coordinates for 3D points, like (0,0,0), (1,0,0)...
        objp = np.zeros((w * h, 3), np.float32)
        objp[:, :2] = np.mgrid[0:w, 0:h].T.reshape(-1, 2)

        # Creating vector to store vectors of 3D points for each
        objpoints = []
        # Creating vector to store vectors of 2D points for each
        imgpoints = []

        # Process set of chessboard images
        images = glob.glob(file_filter)

        for fname in images:
            print('Processing', fname)
            img = cv.imread(fname)
            gray = cv.cvtColor(img, cv.COLOR_BGR2GRAY)

            # Find the chess board corners
            ret, corners = cv.findChessboardCorners(gray, (w, h), None)

            # If found, add object points, image points (after refining them)
            if ret:
                print('  Found corners')
                print(' Number of corners: ', len(corners))
                objpoints.append(objp)
                corners2 = cv.cornerSubPix(gray, corners, (11, 11), (-1, -1), criteria)
                imgpoints.append(corners)
                # Draw and display the corners
                cv.drawChessboardCorners(img, (w, h), corners2, ret)
                temp_img = cv.resize(img, dsize=(int(img.shape[0] / 5), int(img.shape[1] / 5)))
                # cv.imshow('img', temp_img)
                # cv.waitKey(500)
            else:
                print('  Failed to find corners')

        # Perform calibration
        ret, mtx, dist, rvecs, tvecs = cv.calibrateCamera(objpoints, imgpoints, \
                                                          gray.shape, None, None)

        # # Save matrix and distortion values for later use
        np.savetxt('%s_matrix.txt' % model_name, mtx)
        np.savetxt('%s_distortion.txt' % model_name, dist)

    @staticmethod
    def undistort(RAW_PATH, CAL_PATH):
        """
        This function is used for undisort images with calculated calibration matrix.
        :param RAW_PATH: the file path of images that needed to be calibrated
        :param CAL_PATH: the file path where the calibrated images stores
        """
        # Process set of raw images
        file_filter = RAW_PATH + '/*'
        all_file_name_list = glob.glob(file_filter)
        for file_name in all_file_name_list:
            file_path = file_name + '/*.jpg'
            images = glob.glob(file_path)
            # Get names of the file folder
            new_file_name = file_name.replace(RAW_PATH, CAL_PATH)
            mkdir(new_file_name)
            for fname in images:
                print(fname)
                img = cv.imread(fname)
                h = img.shape[0]
                w = img.shape[1]

                # load calibrate model
                model_name = MODEL_NAME
                mtx = np.loadtxt('%s_matrix.txt' % model_name)
                dist = np.loadtxt('%s_distortion.txt' % model_name)
                newcameramtx, roi = cv.getOptimalNewCameraMatrix(mtx, dist, (w, h), 1, (w, h))

                # undistort
                dst = cv.undistort(img, mtx, dist, None, newcameramtx)

                # crop the imaged
                x, y, w, h = roi
                dst = dst[y:y + h, x:x + w]
                cv.imwrite(fname.replace(RAW_PATH, CAL_PATH), dst)
