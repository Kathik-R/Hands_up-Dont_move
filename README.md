# Motion_Sensing_Webcam
SUMMARY: A motion sensing webcam based on the OpenCV library. It also creates a LogBook containing the time when an object enters and exits the frame.  

HOW DOES IT WORK? 
1. Takes the first frame as the background. 
2. Uses this as the basis to compare the consequent frames. Tracks changes by calculating the delta_frame. 
3. Filters out the noise and keeps only those objects which satisfy a delta threshold and have a large enough contour area. 
4. Assesses the status of the object in the previous frame and manages a log of when the object entered and exited the frame.  

NOTE: The Delta Thresholds and Contour Area have been experimentally determined to work for my webcam. Feel free to tinker with the numbers to find what suits you the best.

LIMITATION:
1. The first frame should contain a background. If an object, like an individual, is in this frame then the delta frame will not be completely accurate. This causes the person to be broken into smaller units instead of a cohesive contour.
2. I'm working on finding/creating more efficient libraries to improve the calculation of the delta frame which directly impacts motion detection.
