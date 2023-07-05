import mediapipe as mp
import numpy as np
import cv2

class Pose:

    def __init__(self,static_image_mode=False,trackconf=0.5,detectionconf=0.5,
                 smooth_landmarks=True,model_complexity=2):
        
        self.static_image_mode=static_image_mode
        self.model_complexity=model_complexity
        self.trackconf=trackconf
        self.detectionconf=detectionconf
        self.smooth_landmarks=smooth_landmarks
        self.mp_pose=mp.solutions.pose
        self.mp_drawing=mp.solutions.drawing_utils
        self.mp_drawing_styles=mp.solutions.drawing_styles
        
        
        ## calling the object 

        self.pose=self.mp_pose.Pose(model_complexity=self.model_complexity,static_image_mode=self.static_image_mode,
                                    smooth_landmarks=self.smooth_landmarks,
                                    min_detection_confidence=self.detectionconf,
                                    min_tracking_confidence=self.trackconf)
        
        
    def get_pose_features(self,img,draw=False):

        results=self.pose.process(img)

        

        self.lmks=results.pose_landmarks

        if draw:
            self. mp_drawing.draw_landmarks(
            img,
            self.lmks,
            self.mp_pose.POSE_CONNECTIONS,
            landmark_drawing_spec=self.mp_drawing_styles.get_default_pose_landmarks_style())
        
        
        if self.lmks is None:
            
            return np.array([[0.0,0.0,0.0] for i in range(33)])

        else:
            

            return np.array([[landmark.x,landmark.y,landmark.z]for landmark in self.lmks.landmark])

       



    

       

       
   
    
   
    

 



class Pose_utils:

   

    def find_angle(self,img,joints,pose_features,draw=True):

        
        h,w,c=img.shape
        j1,j2,j3=joints

        x1,y1=pose_features[j1][:2]
        x2,y2=pose_features[j2][:2]
        x3,y3=pose_features[j3][:2]
        x1,x2,x3=int(x1*w),int(x2*w),int(x3*w)
        y1,y2,y3=int(y1*h),int(y2*h),int(y3*h)
        # print(x1,y1)
        radian=np.arctan2(y3-y2,x3-x2)-np.arctan2(y1-y2,x1-x2)

        degree=np.abs((180/np.pi)*radian)

        # if degree < 0:
        #     degree += 360 

        if degree > 180.0:
            degree = 360 - degree


        if draw:

            cv2.line(img, (x1, y1), (x2, y2), (255, 255, 255), 3)
            cv2.line(img, (x3, y3), (x2, y2), (255, 255, 255), 3)
            cv2.circle(img, (x1, y1), 10, (0, 0, 255), cv2.FILLED)
            cv2.circle(img, (x1, y1), 15, (0, 0, 255), 2)
            cv2.circle(img, (x2, y2), 10, (0, 0, 255), cv2.FILLED)
            cv2.circle(img, (x2, y2), 15, (0, 0, 255), 2)
            cv2.circle(img, (x3, y3), 10, (0, 0, 255), cv2.FILLED)
            cv2.circle(img, (x3, y3), 15, (0, 0, 255), 2)
            cv2.putText(img, str(int(degree)), (x2 - 50, y2 + 50),
                        cv2.FONT_HERSHEY_PLAIN, 2, (0, 0, 255), 2)
        

        return degree


    def get_bbox(self,img,pose_features):
        h,w,c=img.shape
        
        x_features=pose_features[:,0]
        y_features=pose_features[:,1]  
        x_min,x_max=int(np.min(x_features)*w),int(np.max(x_features)*w)
        
        y_min,y_max=int(np.min(y_features)*h),int(np.max(y_features)*h)
        return (x_min,y_min),(x_max,y_max)