import cv2
import numpy as np
from scipy.spatial import distance as dist
import time
from openvino.inference_engine import IENetwork, IEPlugin


#net =  IENetwork.from_ir(model='intel/person-detection-retail-0013/FP16/person-detection-retail-00130.xml',weights='intel/person-detection-retail-0013/FP16/person-detection-retail-00130.bin')
# ターゲットデバイスの指定 
plugin = IEPlugin(device='MYRIAD')

# モデルの読み込み 
net = IENetwork(model='/home/aidl/workspace/intel/person-detection-retail-0013/FP16/person-detection-retail-0013.xml',weights='/home/aidl/workspace/intel/person-detection-retail-0013/FP16/person-detection-retail-0013.bin')
exec_net = plugin.load(network=net)
 
# 入出力データのキー取得 
#input_blob = next(iter(net.inputs))
#out_blob = next(iter(net.outputs))

# 画像読み込み 
#frame = cv2.imread('pedestrian5.mp4')
#cap = cv2.VideoCapture(0)
cap = cv2.VideoCapture('sample3.264')
start_time = time.time()
index = 0
flag = False
while True:
    index += 1
    flag = False
    print(time.time()-start_time)
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
    violate = set()
    #Alerts when contacted for 15 seconds
    if index == 1:
        centroids = np.array([[(float(detection[5])-float(detection[3]))/2+float(detection[3]),(float(detection[6])-float(detection[4]))/2+float(detection[4])] for detection in out ])
        D_2 = dist.cdist(centroids,centroids,metric = "euclidean") 
    if time.time() - start_time > 15.0 :
        start_time = time.time()
        centroids = np.array([[(float(detection[5])-float(detection[3]))/2+float(detection[3]),(float(detection[6])-float(detection[4]))/2+float(detection[4])] for detection in out ])
        D_1 = dist.cdist(centroids,centroids,metric = "euclidean")  
        for i in range(0,D_1.shape[0]):
            for j in range(i+1,D_1.shape[1]):
                if  (D_1[i,j] != 0.0 and D_1[i,j]  < 0.07)  and  (D_2[i,j] != 0.0 and D_2[i,j]  < 0.07) :
                    violate.add(i)
                    violate.add(j)
        D_2 = dist.cdist(centroids,centroids,metric = "euclidean")
        cv2.imshow("frame",frame)

    violate = list(violate)
    #for detection in out:
    for i,detection in enumerate(out):
        #print(violate)
        confidence = float(detection[2])
        x_min = int(detection[3] * frame.shape[1])
        y_min = int(detection[4] * frame.shape[0])
        x_max = int(detection[5] * frame.shape[1])
        y_max = int(detection[6] * frame.shape[0])
        if i in violate and confidence > 0.6:
            color = (0,0,255)
            cv2.rectangle(frame,(x_min,y_min),(x_max,y_max),color,thickness = 3)
            flag = True

    cv2.imshow("frame",frame)
    key = cv2.waitKey(1)
    if key != -1:
        break
    if flag == True:
        time.sleep(5)
cap.release()
cv2.destroyAllWindows()
