import sys
import math
import time
import cv2
import numpy as np
from scipy.spatial import distance
from munkres import Munkres
from openvino.inference_engine import IENetwork,IEPlugin

#Database design
class data_base_h:
    def __init__(self, pos, feature, id=-1):
        self.feature = feature
        self.pos = pos
        self.time = time.monotonic()
        self.id = id
        
#AI model path
model_H  = '/home/aidl/workspace/intel/person-detection-retail-0013/FP16/person-detection-retail-0013'
model_P = '/home/aidl/workspace/intel/person-reidentification-retail-0200/FP16/person-reidentification-retail-0200'

def main():
    #Mosaic processing
    def mosaic(img, ratio=0.05):
        small = cv2.resize(img, None, fx=ratio, fy=ratio, interpolation=cv2.INTER_NEAREST)
        big = cv2.resize(small, img.shape[:2][::-1], interpolation=cv2.INTER_NEAREST)
        return big

    def mosaic_area(img, xmin, ymin, xmax, ymax, ratio=0.05):
        dst = img.copy()
        dst[ymin:ymax,xmin:xmax] = mosaic(dst[ymin:ymax,xmin:xmax], ratio)
        return dst
    
    #Database settings
    id_num = 0
    dist_threshold = 1.0
    timeout_threshold = 10000
    feature_db = []
    violate_t = list()

    #Index setting
    index = 0

    #OpenVino setting
    plugin = IEPlugin(device='MYRIAD')
    
    #AI model of human recognition　settings
    net_h  = net = IENetwork(model=model_H+ ".xml",weights= model_H + ".bin") 
    input_name_h  = next(iter(net_h.inputs))                     
    input_shape_h = net_h.inputs[input_name_h].shape           
    out_name_h    = next(iter(net_h.outputs))                    
    out_shape_h   = net_h.outputs[out_name_h].shape  
    exec_net_h    = plugin.load(network=net_h)

    #AI model of personal identification settings
    net_p = IENetwork(model = model_P+".xml",weights = model_P+".bin") 
    input_name_p  = next(iter(net_p.inputs))                  
    input_shape_p = net_p.inputs[input_name_p].shape        
    out_name_p    = next(iter(net_p.outputs))                 
    out_shape_p   = net_p.outputs[out_name_p].shape 
    exec_net_p    = plugin.load(network=net_p)
   
    #Please enter the name of the video file you want to process
    cap = cv2.VideoCapture('SAMPLE.264')
    
    start_time = time.monotonic()

    while cv2.waitKey(1)!=27:    

        object_H = []
        index += 1
        frame = cap.read()
        image = frame[1]

        if frame[0] == False:
            return

        #AI model "human recognition　settings" inference
        in_frame = cv2.resize(image, (input_shape_h[3], input_shape_h[2]))
        in_frame = in_frame.transpose((2, 0, 1))
        in_frame = in_frame.reshape(input_shape_h)
        res_h = exec_net_h.infer(inputs={input_name_h: in_frame})

        for obj in res_h[out_name_h][0][0]: 
            if obj[2] > 0.3: 
                frame = image
                xmin = abs(int(obj[3] * frame.shape[1]))
                ymin = abs(int(obj[4] * frame.shape[0]))
                xmax = abs(int(obj[5] * frame.shape[1]))
                ymax = abs(int(obj[6] * frame.shape[0]))
                class_id = int(obj[1])

                obj_img=frame[ymin:ymax,xmin:xmax] 
                obj_img=cv2.resize(obj_img, (128, 256)) 
                obj_img=obj_img.transpose((2,0,1))
                obj_img = np.expand_dims(obj_img, axis=0)

                #AI model "Personal recognition" inference             
                res_reid = exec_net_p.infer(inputs={ input_name_p : obj_img})       
                vec=np.array(res_reid[out_name_p]).reshape((512))
                object_H.append(data_base_h([xmin,ymin, xmax,ymax], vec))
        total_objects=0

        #Register in the database
        hangarian = Munkres()
        dist_matrix = [ [ distance.cosine(obj_db.feature, obj_cam.feature) for obj_db in feature_db ] for obj_cam in object_H ]
        combination = hangarian.compute(dist_matrix)      
        for idx_obj, idx_db in combination:
            if object_H[idx_obj].id!=-1: 
                continue 
            dist = distance.cosine(object_H[idx_obj].feature, feature_db[idx_db].feature)
            if dist < dist_threshold:
                feature_db[idx_db].time = time.monotonic()            
                object_H[idx_obj].id = feature_db[idx_db].id              
        del hangarian
        for obj in object_H:
            if obj.id == -1:
                xmin, ymin, xmax, ymax = obj.pos
                obj.id=id_num
                feature_db.append(obj)
                id_num+=1               
        for i, db in enumerate(feature_db):
            if time.monotonic() - db.time > timeout_threshold:
                feature_db.pop(i)
       
        #Judging a violation of Social Distance
        violate = set() 
        centroids = np.array([[(obj.pos[2]-obj.pos[0])/2+obj.pos[0],(obj.pos[3]-obj.pos[1])/2+obj.pos[1]] for obj in object_H])
        D_1 = distance.cdist(centroids,centroids,metric = "euclidean")        
        for i in range(0,D_1.shape[0]):
            for j in range(i+1,D_1.shape[1]):
                if  (D_1[i,j] != 0.0 and D_1[i,j]  < 50.0):
                    violate.add(object_H[i].id)
                    violate.add(object_H[j].id)                 
        if index == 1:
           violate_b = violate
 
        if time.monotonic() - start_time > 30.0:
            start_time =  time.monotonic()
            violate_a = violate
            if len(list(violate_b & violate_a)) % 2== 0:
                violate_t += list(violate_b & violate_a)
                violate_t = list(set(violate_t))
            violate_b = violate
        violate = list(violate)
        
        #Window display processing
        for obj in object_H:
            id = obj.id
            color = (0,0,0)
            xmin, ymin, xmax, ymax = obj.pos
            image = mosaic_area(image,xmin,ymin,xmax,ymax)
            if obj.id in violate:
               color = (0,255,0)
            if obj.id in violate_t:
               color  =(0,0,255)
            cv2.rectangle(image, (xmin, ymin), (xmax, ymax), color, 5)
        font = cv2.FONT_HERSHEY_COMPLEX
        cv2.putText(image,str(len(violate_t)),(50,150),font,4,(0,0,255),2,cv2.LINE_AA)              
        image = cv2.resize(image,dsize=(1000,600))
        cv2.imshow('Frame', image)
    cv2.destroyAllWindows()

if __name__ == '__main__':
        sys.exit(main() or 0)
