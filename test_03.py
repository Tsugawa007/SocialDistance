import cv2
import numpy as np
from scipy.spatial import distance as dist
from openvino.inference_engine import IENetwork, IEPlugin

# ターゲットデバイスの指定 
plugin = IEPlugin(device='MYRIAD')

# モデルの読み込み 
net = IENetwork(model='/home/aidl/workspace/intel/person-detection-retail-0013/FP16/person-detection-retail-0013.xml',weights='/home/aidl/workspace/intel/person-detection-retail-0013/FP16/person-detection-retail-0013.bin')
exec_net = plugin.load(network=net)
 
WINDOWS_TITLE = 'title'
CONFIDENCE_RATIO = 0.6

# 画像読み込み 
cap = cv2.VideoCapture('ppp.264')

while True:

    # read the next frame from the file
    ret, frame = cap.read()# if the frame was not grabbed, then we have reached the end 
    if ret == False:
        continue
    img = cv2.resize(frame, (544,320)) # HeightとWidth変更 
    img = img.transpose((2, 0, 1))    # HWC > CHW 
    img = np.expand_dims(img, axis=0) # CHW > BCHW
    out = exec_net.infer(inputs={'data': img})
 
    # 出力から必要なデータのみ取り出し 
    out = out['detection_out']
    # 不要な次元を削減 
    out = np.squeeze(out)
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
    key = cv2.waitKey(1)
    if key != -1:
        break
cap.release()
cv2.destroyAllWindows()
