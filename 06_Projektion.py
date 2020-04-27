__author__ = "Joshua Joost (1626034)"
__maintainer = __author__
__date__ = "2020-04-27"
__version__ = "1.0"
__status__ = "Finished"

import numpy as np 
import cv2

## --- Task 1 Projection
# --- Constants Task 1
# focal lenght
fx = 460
fy = 460

# Translation of the image main point to adapt to the coordinate system of the image plane 
cx = 320
cy = 240

# Image resolution
imageExercise1 = np.zeros((640, 480))

# 3D Room points
roomPoints3D = np.array([[[10],[10],[100]], [[33],[22],[111]], [[100],[100],[1000]], [[20],[-100],[100]]])

# calibration matrix, contains intrinsic parameters
k = np.array([[fx,0,cx],[0,fy,cy],[0,0,1]], dtype=np.float32)
# World and camera coordinate system are identical
extrinsicMatrix = np.concatenate((np.eye(3), np.zeros((3,1))),axis=1)

# Projection matrix
p = np.dot(k, extrinsicMatrix)

# using homegeneous coordinate system
# :param arg2: cartesian3DRoomPoint need to be shape 3x1
# :return: return cartesian 2D imageplane point 
def calc3DRoomPointTo2DPointOnImagePlane(projectionMatrix, cartesian3DRoomPoint):
    if not len(cartesian3DRoomPoint.shape) == 2 or not cartesian3DRoomPoint.shape[0] == 3 or not cartesian3DRoomPoint.shape[1] == 1:
        roomPointDim = ""
        for i in range(len(cartesian3DRoomPoint.shape)):
            roomPointDim = roomPointDim + str(cartesian3DRoomPoint.shape[i])
            if i < len(cartesian3DRoomPoint.shape) - 1:
                roomPointDim = roomPointDim + "x"
                pass
            pass
        raise ValueError(f"Der kartesische 3D-Raumpunkt muss ein 3x1 Vektor sein, gegeben {roomPointDim}")
        pass

    # convert cartesian 3D room point to homogeneous 3D room point
    homogeneous3DRoomPoint = np.reshape(np.concatenate((np.reshape(cartesian3DRoomPoint, (1,-1)), np.ones((cartesian3DRoomPoint.shape[1],1))), axis=1), (-1,1))
    
    # Calculate 2D homogenuous image plane point
    homogeneous2DImagePlanePoint = np.dot(p, homogeneous3DRoomPoint)
    
    # Convert 2D homogenuous to 2D cartesian point
    cartesian2DImagePlanePoint = np.zeros((homogeneous2DImagePlanePoint.shape[0] - 1, homogeneous2DImagePlanePoint.shape[1]))
    for i in range(cartesian2DImagePlanePoint.shape[0]):
        cartesian2DImagePlanePoint[i] = homogeneous2DImagePlanePoint[i] / homogeneous2DImagePlanePoint[-1]
        pass

    return cartesian2DImagePlanePoint
    pass

## --- Determining the pixel position with own function
imagePlanePoints2D = np.zeros((roomPoints3D.shape[0], roomPoints3D.shape[1] - 1, roomPoints3D.shape[2]))

for i in range(roomPoints3D.shape[0]):
    cartesicImagePlanePointCoords = calc3DRoomPointTo2DPointOnImagePlane(p, roomPoints3D[i])
    imagePlanePoints2D[i][0] = cartesicImagePlanePointCoords[0]
    imagePlanePoints2D[i][1] = cartesicImagePlanePointCoords[1]

    pass

print(imagePlanePoints2D)

## --- Determining the pixel position using the openCV function
cartesicImagePlanePoint = cv2.projectPoints(np.reshape(np.float32(roomPoints3D[:]), (-1,3)), np.eye(3), np.zeros((1,3)), k, None)
#print(cartesicImagePlanePoint[0]) # own and cv2 projection identical

## --- Liegen alle Pixel im Bild?
# No Pixel 4 is too low on the y-axis and therefore lies outside the image plane

## --- Was fällt bei den Bildpunkten von X1 und X3 auf?
# Pixel X1 and X3 are projected on the same spot of the image plane