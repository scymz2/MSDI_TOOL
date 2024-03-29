# Mochuan Zhan , 2022/ 7/15 The University of Manchester
# UTF-8

from exif import Image
import piexif
import piexif.helper
from PIL import Image as PILImage
import glob


def get_GPS(path):
    """
    Obtain GPS data from image exif
    :param path: image path
    :return: GPS dict containing latitude and longitude
    """
    with open(path, 'rb') as image_file:
        print(path)
        GPS = {}
        image = Image(image_file)
        if image.has_exif:
            pass
        else:
            print('Error, no exif:' + path)
        # extract GPS info
        GPS['Latitude'] = image.gps_latitude[0] + image.gps_latitude[1] / 60 + image.gps_latitude[2] / 3600
        GPS['Longitude'] = image.gps_longitude[0] + image.gps_longitude[1] / 60 + image.gps_longitude[2] / 3600
        GPS['LatitudeRef'] = image.gps_latitude_ref  # str
        GPS['LongitudeRef'] = image.gps_longitude_ref  # str

        # determine the symbol of latitude and longitude
        if GPS['LatitudeRef'] == 'S':
            GPS['Latitude'] = -GPS['Latitude']
        if GPS['LongitudeRef'] == 'W':
            GPS['Longitude'] = -GPS['Longitude']

        return GPS


def copy_exif(raw_path, cal_path):
    """
    copy exif from one file to another file
    :param raw_path: source file path
    :param cal_path: target file path
    """
    all_file_name_list = glob.glob(raw_path + '/*')
    for file_name in all_file_name_list:
        raw_images = glob.glob(file_name + '/*.jpg')
        for raw in raw_images:
            print(raw)
            # copy exif to calibrated image
            cal = raw.replace(raw_path, cal_path)
            piexif.transplant(raw, cal)
            print(cal)


def delete_exif(raw_path, content):
    """
    Delete exif of images, but keep the exif structure (empty exif)
    :param raw_path: source file path
    :param content: target file path
    """
    # check cotent format
    if not isinstance(content, list):
        print("please input a list!")
        exit()

    all_file_name_list = glob.glob(raw_path + '/*')
    for file_name in all_file_name_list:
        raw_images = glob.glob(file_name + '/*.jpg')
        for raw in raw_images:
            with open(raw, 'rb') as image_file:
                my_image = Image(image_file)
                if my_image.has_exif:
                    # if list is empty, then delete all exif
                    if len(content) == 0:
                        new_list = my_image.list_all()
                    else:
                        new_list = content
                    # start deletion
                    for item in new_list:
                        my_image.delete(item)

                else:
                    print('Error, no exif:' + raw)


def modify_exif(path, content):
    """
    According to the dict given by user, modify exif of images
    :param path: file path of images
    :param content: dictionary containing exif title and value pairs
    """
    # check the format of the content
    if not isinstance(content, dict):
        print("please input a dict!")
        exit()

    all_file_name_list = glob.glob(path + '/*')
    for file_name in all_file_name_list:
        images = glob.glob(file_name + '/*.jpg')
        for img in images:
            print(img)
            raw_image = PILImage.open(img)
            exif_dict = piexif.load(raw_image.info['exif'])
            for label, txt in content.items():
                if label == 'user_comment':
                    user_comment = piexif.helper.UserComment.dump(txt)
                    exif_dict['Exif'][piexif.ExifIFD.UserComment] = user_comment
                elif label == 'copyright':
                    exif_dict['0th'][piexif.ImageIFD.Copyright] = txt.encode()
                elif label == 'artist':
                    exif_dict['0th'][piexif.ImageIFD.Artist] = txt.encode()

            # save images
            exif_bytes = piexif.dump(exif_dict)
            raw_image.save(img, exif=exif_bytes)
