import cv2
import numpy as np
import matplotlib.pyplot as plt

cap = cv2.VideoCapture('./videos/cars.MP4')

ret, frame1 = cap.read()

prvs = cv2.cvtColor(frame1, cv2.COLOR_BGR2GRAY)
hsv = np.zeros_like(frame1)
hsv[..., 1] = 255

[R,C]=prvs.shape
count=0
while (1):
    ret, frame2 = cap.read()
    next = cv2.cvtColor(frame2, cv2.COLOR_BGR2GRAY)

    flow = cv2.calcOpticalFlowFarneback(prvs, next, None, 0.5, 3, 15, 2, 5, 1.2, 0)
    mag, ang = cv2.cartToPolar(flow[..., 0], flow[..., 1])

    RV=np.arange(5,480,5)
    CV=np.arange(5,640,5)
    # These give arrays of points to sample at increments of 5
    if count==0:
        count =1 #so that the following creation is only done once
        [Y,X]=np.meshgrid(CV,RV)
        # makes an x and y array of the points specified at sample increments

    temp =mag[np.ix_(RV,CV)]
    # this makes a temp array that stores the magnitude of flow at each of the sample points

    motionvectors=np.array((Y[:],X[:],Y[:]+temp.real[:],X[:]+temp.imag[:]))

    Ydist=motionvectors[0,:,:]- motionvectors[2,:,:]
    Xdist=motionvectors[1,:,:]- motionvectors[3,:,:]
    Xoriginal=X-Xdist
    Yoriginal=Y-Ydist



    plot2 = plt.figure()
    plt.quiver(Xoriginal, Yoriginal, X, Y,
               color='Teal',
               headlength=7)

    plt.title('Quiver Plot, Single Colour')
    plt.show(plot2)


    hsv[..., 0] = ang * 180 / np.pi / 2
    hsv[..., 2] = cv2.normalize(mag, None, 0, 255, cv2.NORM_MINMAX)
    bgr = cv2.cvtColor(hsv, cv2.COLOR_HSV2BGR)
    cv2.imshow('frame2', bgr)

    k = cv2.waitKey(30) & 0xff

    if k == 27:
        break
    prvs = next

cap.release()
cv2.destroyAllWindows()
