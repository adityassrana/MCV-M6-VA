
import numpy as np
from filterpy.kalman import KalmanFilter

def convert_bbox_to_z(bbox):
  """
  Takes a bounding box in the form [x1,y1,x2,y2] and returns z in the form
    [x,y,s,r] where x,y is the centre of the box and s is the scale/area and r is
    the aspect ratio
  """
  #print("Entra: " + str(bbox))
  w = bbox[2]# - bbox[0]
  h = bbox[3]# - bbox[1]
  x = bbox[0] + w/2.
  y = bbox[1] + h/2.
  s = w * h    #scale is just area
  r = w / float(h)
  return np.array([x, y, s, r]).reshape((4, 1))

def convert_x_to_bbox(x,score=None):
    """
    Takes a bounding box in the centre form [x,y,s,r] and returns it in the form
    [x1,y1,x2,y2] where x1,y1 is the top left and x2,y2 is the bottom right
    """
    w = np.sqrt(x[2] * x[3])
    h = x[2] / w
    if(score==None):
        xyxy = [x[0]-w/2.,x[1]-h/2.,x[0]+w/2.,x[1]+h/2.]
    else:
        xyxy = [x[0]-w/2.,x[1]-h/2.,x[0]+w/2.,x[1]+h/2.,score]

    return np.array([xyxy[0], xyxy[1], xyxy[2] - xyxy[0], xyxy[3] - xyxy[1]]).reshape((1, len(xyxy)))


class KalmanTracker:

    def __init__(self):
        self.bbox = None


    def init(self, frame, bbox):

        #define constant velocity model
        self.kf = KalmanFilter(dim_x=7, dim_z=4) 
        self.kf.F = np.array([[1,0,0,0,1,0,0],[0,1,0,0,0,1,0],[0,0,1,0,0,0,1],[0,0,0,1,0,0,0],  [0,0,0,0,1,0,0],[0,0,0,0,0,1,0],[0,0,0,0,0,0,1]])
        self.kf.H = np.array([[1,0,0,0,0,0,0],[0,1,0,0,0,0,0],[0,0,1,0,0,0,0],[0,0,0,1,0,0,0]])

        self.kf.R[2:,2:] *= 10.
        self.kf.P[4:,4:] *= 1000. #give high uncertainty to the unobservable initial velocities
        self.kf.P *= 10.
        self.kf.Q[-1,-1] *= 0.01
        self.kf.Q[4:,4:] *= 0.01

        self.kf.x[:4] = convert_bbox_to_z(bbox)
        self.bbox = bbox

        self.history = []
        self.age = 0

    def update(self, frame):
        """
        Advances the state vector and returns the predicted bounding box estimate.
        """
        if((self.kf.x[6] + self.kf.x[2]) <= 0):
            self.kf.x[6] *= 0.0
        self.kf.predict()
        self.age += 1
        predicted = convert_x_to_bbox(self.kf.x)
        #print(f"Predicted: {predicted}")
        self.history.append(predicted)
        return True, predicted[0]

    def update_state(self, frame, bbox):
        xywh = [bbox[0], bbox[1], bbox[2]-bbox[0], bbox[3]-bbox[1]]
        self.history = []
        new_bbox = convert_bbox_to_z(xywh)
        #print(f"NEW: {new_bbox}")
        self.kf.update(new_bbox)


