import cv2


def test0():
    image = cv2.imread("marker_test.jpg")
    arucoDict = cv2.aruco.Dictionary_get(cv2.aruco.DICT_4X4_250)
    arucoParams = cv2.aruco.DetectorParameters_create()
    (corners, ids, rejected) = cv2.aruco.detectMarkers(image, arucoDict, parameters=arucoParams)
    print(ids)

if __name__ == '__main__':
    test0()


