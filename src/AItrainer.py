


class AItrainer:

    def __init__(self,joint_config,pose_util_obj):

        self.joint_config=joint_config
        self.pose_util_obj=pose_util_obj
        self.curl_counter=0
        self.pullup_counter=0
        self.pushup_counter=0
        

        ## Defining the initial state of the exercise

        self.curl_state='DOWN'
        self.pullup_state='DOWN'
        self.pushup_state='DOWN'
        

    def curl(self,img,pose_features,draw=True):

       
        
        print('CURL')
        right_joints=self.joint_config['Right shoulder'],self.joint_config['Right elbow'], self.joint_config['Right wrist']
        left_joints=self.joint_config['Left shoulder'],self.joint_config['Left elbow'], self.joint_config['Left wrist']
        right_angle=self.pose_util_obj.find_angle(img,right_joints,pose_features,draw=draw)
        left_angle=self.pose_util_obj.find_angle(img,left_joints,pose_features,draw=draw)
        avg_angle=(right_angle+left_angle)//2
        

        if avg_angle > 140:
            self.curl_state='DOWN'

        if avg_angle <60 and self.curl_state=='DOWN':
            self.curl_state='UP'
            self.curl_counter+=1

    

    def pullup(self,img,pose_features,draw=True):

        right_joints=self.joint_config['Right shoulder'],self.joint_config['Right elbow'], self.joint_config['Right wrist']
        left_joints=self.joint_config['Left shoulder'],self.joint_config['Left elbow'], self.joint_config['Left wrist']
        right_angle=self.pose_util_obj.find_angle(img,right_joints,pose_features,draw=draw)
        left_angle=self.pose_util_obj.find_angle(img,left_joints,pose_features,draw=draw)
        avg_angle=(right_angle+left_angle)//2
        

        if avg_angle>150:
            self.pullup_state='DOWN'

        if avg_angle <60 and self.pullup_state=='DOWN':
            self.pullup_state='UP'
            self.pullup_counter+=1

       

    def pushup(self,img,pose_features,draw=True):


        right_joints=self.joint_config['Right shoulder'],self.joint_config['Right elbow'], self.joint_config['Right wrist']
        left_joints=self.joint_config['Left shoulder'],self.joint_config['Left elbow'], self.joint_config['Left wrist']
        right_angle=self.pose_util_obj.find_angle(img,right_joints,pose_features,draw=draw)
        left_angle=self.pose_util_obj.find_angle(img,left_joints,pose_features,draw=draw)
        avg_angle=(right_angle+left_angle)//2
        
        print(avg_angle)

        if avg_angle<80:
            self.pushup_state='DOWN'

        if avg_angle >160 and self.pushup_state=='DOWN':
            self.pushup_state='UP'
            self.pushup_counter+=1
