import cv2
import numpy as np
import multiprocessing
import threading
import time
import argparse

FRAME_QUEUE = multiprocessing.JoinableQueue()
RESULT_QUEUE = multiprocessing.Queue()

# defaults
NWORKERS = 2
PARALLEL_TYPE = 'thread'
FONT = cv2.FONT_HERSHEY_SIMPLEX


def process_frame(frame):
    # Convert BGR to HSV
    hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)

    lower_red = np.array([150, 150, 50], np.uint8)
    upper_red = np.array([180, 255, 150], np.uint8)

    # Threshold the HSV image to get only blue colors
    # finding the range of red
    mask = cv2.inRange(hsv, lower_red, upper_red)
    res = cv2.bitwise_and(frame, frame, mask=mask)

    kernel = np.ones((5, 5), np.uint8)
    mask = cv2.dilate(mask, kernel)
    res = cv2.bitwise_and(frame, frame, mask=mask)

    _, contours, hierarchy = cv2.findContours(mask, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)

    for pic, contour in enumerate(contours):
        area = cv2.contourArea(contour)
        if(area > 1000):
            x, y, w, h = cv2.boundingRect(contour)
            frame = cv2.rectangle(frame, (x, y), (x+w, y+h), (0, 0, 255), 2)

    return frame, mask, res


def parallel_process_frame(cls):
    """the main function that perfroms the image processing"""
    while True:
        next_frame = FRAME_QUEUE.get()
        if next_frame is None:
            # Poison pill means shutdown
            break

        # process the frame
        i, frame = next_frame
        frame, mask, res = process_frame(frame)

        # draw worker on frame
        frame = cv2.putText(frame, '{}'.format(i),
                            (0, 20), FONT,
                            0.5, (255, 0, 0), 1, cv2.LINE_AA)

        # tell the queue that we are done
        FRAME_QUEUE.task_done()

        # place the results in the result queue
        RESULT_QUEUE.put((i, (frame, mask, res)))


class ParallelProcessWorker(multiprocessing.Process):
    """multiprocess worker"""
    def __init__(self):
        multiprocessing.Process.__init__(self)

    def run(self):
        parallel_process_frame(self)


class ParallelThreadWorker(threading.Thread):
    """multithread worker"""
    def __init__(self):
        threading.Thread.__init__(self)

    def run(self):
        parallel_process_frame(self)


def serial(frame):
    """serial process the frame"""
    return process_frame(frame)


def multi(frame):
    """multithread/multiprocess process the frame"""
    # split the frame and place in the queue
    for i, chunk in enumerate(np.split(frame, NWORKERS)):
        FRAME_QUEUE.put((i, chunk))

    # wait for the chunks to finish
    FRAME_QUEUE.join()

    # collect the results
    results = []
    for i in range(NWORKERS):
        results.append(RESULT_QUEUE.get())

    # sort, because they can come back in any order
    results.sort(key=lambda x: x[0])

    # combine chunks
    frame = np.vstack((r[1][0] for r in results))
    mask = np.vstack((r[1][1] for r in results))
    res = np.vstack((r[1][2] for r in results))

    return frame, mask, res


if __name__ == "__main__":

    parser = argparse.ArgumentParser(
        prog='Parallel',
        description='Program parallel video processing')

    ARG = parser.add_argument
    ARG('-m', '--method', metavar='PAR', action='store', default=None,
        choices=['serial', 'thread', 'process'])
    ARG('-w', '--workers', metavar='N', action='store', default=2,
        help='specify the number of workers')

    args = parser.parse_args()

    # set flags
    PARALLEL_TYPE = args.method
    NWORKERS = int(args.workers)

    # setup parallel scheme
    if PARALLEL_TYPE != 'serial':
        method = multi
        if PARALLEL_TYPE == 'thread':
            worker = ParallelThreadWorker
        else:
            worker = ParallelProcessWorker
        # start the workers
        for i in range(NWORKERS):
            w = worker()
            w.start()
    else:
        method = serial

    # variables

    frame_count = 0
    start = time.time()

    # start capture
    cap = cv2.VideoCapture(0)

    # start the loop
    while(True):
        frame_count += 1

        # Take each frame
        _, frame = cap.read()

        frame, mask, res = method(frame)

        FPS = frame_count/(time.time()-start)

        frame = cv2.putText(frame, 'FPS: {0:.1f}'.format(FPS),
                            (0, 20), FONT,
                            0.5, (0, 255, 0), 1, cv2.LINE_AA)

        cv2.imshow('frame', frame)
        # cv2.imshow('mask', mask)
        # cv2.imshow('res', res)

        k = cv2.waitKey(5) & 0xFF
        if k == 27:
            break
    cap.release()
    cv2.destroyAllWindows()

    # place a bunch of Nones to shutdown the threads/process
    [FRAME_QUEUE.put(None) for i in range(NWORKERS*2)]

    # report
    print('Using a {0} approach with {1} workers resulted in an average FPS of {2:.1f}'.format(PARALLEL_TYPE, NWORKERS, FPS))
