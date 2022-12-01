import cv2
import imutils
from skimage.metrics import structural_similarity as compare_ssim

image_title = ["imageA", "imageB", "diff"]


def difference_threshold(image1, image2):
    # compute difference
    difference_img = cv2.subtract(image1, image2)

    # color the mask red
    conv_hsv_gray = cv2.cvtColor(difference_img, cv2.COLOR_BGR2GRAY)
    ret, mask = cv2.threshold(conv_hsv_gray, 0, 255, cv2.THRESH_BINARY_INV | cv2.THRESH_OTSU)
    difference_img[mask != 255] = [0, 0, 255]

    # add the red mask to the images to make the differences obvious
    image1[mask != 255] = [0, 0, 255]
    image2[mask != 255] = [0, 0, 255]

    return [difference_img, image1, image2]


def compare_box(original, new):
    # resize the images to make them smaller. Bigger image may take a significantly
    # more computing power and time
    original = imutils.resize(original, height=600)
    new = imutils.resize(new, height=600)

    # make a copy of original image so that we can store the
    # difference of 2 images in the same
    diff = original.copy()
    cv2.absdiff(original, new, diff)

    # converting the difference into grascale
    gray = cv2.cvtColor(diff, cv2.COLOR_BGR2GRAY)

    # increasing the size of differences so we can capture them all
    for i in range(0, 3):
        dilated = cv2.dilate(gray.copy(), None, iterations=i + 1)

    # threshold the gray image to binarise it. Anything pixel that has
    # value more than 3 we are converting to white
    # (remember 0 is black and 255 is absolute white)
    # the image is called binarised as any value less than 3 will be 0 and
    # all values equal to and more than 3 will be 255
    (T, thresh) = cv2.threshold(dilated, 3, 255, cv2.THRESH_BINARY)

    # now we need to find contours in the binarised image
    cnts = cv2.findContours(thresh, cv2.RETR_LIST, cv2.CHAIN_APPROX_SIMPLE)
    cnts = imutils.grab_contours(cnts)

    for c in cnts:
        # fit a bounding box to the contour
        (x, y, w, h) = cv2.boundingRect(c)
        cv2.rectangle(new, (x, y), (x + w, y + h), (0, 255, 0), 2)

    # cv2.imwrite("changes.png", new)

    return [new]


def difference_sk(imageA, imageB):
    grayA = cv2.cvtColor(imageA, cv2.COLOR_BGR2GRAY)
    grayB = cv2.cvtColor(imageB, cv2.COLOR_BGR2GRAY)

    # compute the Structural Similarity Index (SSIM) between the two
    # images, ensuring that the difference image is returned
    (score, diff) = compare_ssim(grayA, grayB, full=True)
    diff = (diff * 255).astype("uint8")
    print("SSIM: {}".format(score))

    # threshold the difference image, followed by finding contours to
    # obtain the regions of the two input images that differ
    thresh = cv2.threshold(diff, 0, 255,
                           cv2.THRESH_BINARY_INV | cv2.THRESH_OTSU)[1]
    cnts = cv2.findContours(thresh.copy(), cv2.RETR_EXTERNAL,
                            cv2.CHAIN_APPROX_SIMPLE)
    cnts = imutils.grab_contours(cnts)

    # loop over the contours
    for c in cnts:
        # compute the bounding box of the contour and then draw the
        # bounding box on both input images to represent where the two
        # images differ
        (x, y, w, h) = cv2.boundingRect(c)
        cv2.rectangle(imageA, (x, y), (x + w, y + h), (0, 0, 255), 2)
        cv2.rectangle(imageB, (x, y), (x + w, y + h), (0, 0, 255), 2)

    return [imageA, imageB, diff]
