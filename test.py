import cv2
import numpy as np
from scipy.spatial import distance as dist
from openvino.inference_engine import IENetwork, IEPlugin,IECore
#chage the path
model_path = '/home/ubuntu/intel/person-detection-retail-0013/FP32/person-detection-retail-0013'
# plugin = IEPlugin(device='MYRIAD')
# plugin = IEPlugin(device='CPU')

## do not use IEplugin,it's unsupport in future
#DEVICE = 'MYRIAD'
DEVICE = 'CPU'
INPUT = './test.jpg'
MODEL_WIDTH  = 544
MODEL_HEIGHT = 320
WINDOWS_TITLE = 'title'
CONFIDENCE_RATIO = 0.6

ie = IECore()
net_path = ie.read_network(model=model_path+'.xml',weights=model_path+'.bin')
exec_net = ie.load_network(net_path,DEVICE) 
 
frame = cv2.imread(INPUT)
frame = cv2.resize(frame,(MODEL_WIDTH,MODEL_HEIGHT))
#pre-processing for opencv
out= frame.transpose((2,0,1)) #HWC to CHW
out = np.expand_dims(out,axis=0) #add the batch dim
out = exec_net.infer(inputs={'data':out}) #run OpenVino Inference Engine
out = out['detection_out'] # eextract elements
out = np.squeeze(out).astype('float') #remove single-dim

SIMILAR = 1.3
SAFETY_DIST = 1.5 
def violate(detections,similar,safe_dist):
    centorids = []
    width = []
    violate = []
    for detection in detections:
        # confidence = detection[2]
        if detection[2] >CONFIDENCE_RATIO:
            a = [(detection[5]-detection[3])/2+detection[3],(detection[6]-detection[4])/2+detection[4]] 
            w = np.abs([detection[5]-detection[3]])
            centorids.append(a)
            width.append(w)
    centorids = np.array(centorids)
    width = np.array(width)
    width_sup = width/width.T #calculate the rate between widths
    for i,row in enumerate(width_sup):
        for j,col in enumerate(row):
            if j<=i:
                continue
            if col < similar and col > 1/similar : #similar check
               # print(i,j,col)
               centor_dist =float(abs(centorids[i][0]-centorids[j][0]))
               width_avg = float(abs((width[i]+width[j])/2))
               #distance check
               if centor_dist < (width_avg*safe_dist):
                   print(detections[i])
                   violate.append(i)
                   violate.append(j)
    return violate

violate = violate(out,SIMILAR,SAFETY_DIST)


ALTER_COLOR = (0,0,255) #BGR 
SAFE_COLOR  = (0,255,0) 
THICKNESS = 2
for i,detection in enumerate(out):
    if detection[2] > CONFIDENCE_RATIO:
        x_min = int(detection[3]*MODEL_WIDTH)
        y_min = int(detection[4]*MODEL_HEIGHT)
        x_max = int(detection[5]*MODEL_WIDTH)
        y_max = int(detection[6]*MODEL_HEIGHT)
        if i in violate:
            color = ALTER_COLOR
        else:
            color = SAFE_COLOR

        cv2.rectangle(frame,(x_min,y_min),(x_max,y_max),color,THICKNESS)

cv2.imshow(WINDOWS_TITLE,frame)
cv2.waitKey(0)
cv2.destroyAllWindows()


