import numpy as np
import cv2

from utils.utils import read_yaml, fall_detection

from utils.cv_utils import draw_border,save_video
from src.AItrainer import AItrainer
from src.Pose import Pose,Pose_utils
from PIL import  Image
import argparse 
import os
import yaml
import winsound



parser = argparse.ArgumentParser(description='Process some input')
parser.add_argument('--joint_yaml_path','-jyp',default='utils/joint_index.yaml',type=str,help='Joint information file path.',required=False)
parser.add_argument('--exercise','-e',default='pullup',type=str,help='Exercise of your choice.')
parser.add_argument('--fall_alert','-a',default=False,type=bool,help='Exercise of your choice.')
parser.add_argument('--video_path','-v',type=str,help='Provide path of your Video')
parser.add_argument('--detect_fall','-f',type=int,default=1,help='Provide path of your Video')

parser.add_argument('--saved_video', '-s', type=int, default=0, help='You want to save the video?')

print('CHECK CHECK')

args = parser.parse_args()


print(os.path.exists(args.joint_yaml_path))
joint_config=read_yaml(args.joint_yaml_path)

p=Pose(model_complexity=2)
pose_utils=Pose_utils()

trainer=AItrainer(joint_config=joint_config,pose_util_obj=pose_utils)



print('CHECK CHECK')
if __name__=='__main__':

    cap=cv2.VideoCapture(args.video_path)

    frame_array=[]

    while cap.isOpened():

        

        ret,frame=cap.read()
        
        
        if not ret:

            print('END of FRAMES or Corrupted Video File !!!')
            break



        h,w,_=frame.shape
        frame=cv2.resize(frame,(1280,720))

        
        
        pose_features=p.get_pose_features(frame)

      
        #print(pose_features)
        
        #get the bbox
        p1,p2=pose_utils.get_bbox(frame,pose_features=pose_features)

        if args.detect_fall:

            if not fall_detection(p1,p2):

                draw_border(frame,p1,p2)

                if args.exercise=='pullup':

                    trainer.pullup(img=frame,draw=True,pose_features=pose_features)

                    cv2.putText(frame, 'STATE: ', (40, 50),
                                    cv2.FONT_HERSHEY_PLAIN, 3, (255, 255, 255), 4)
                    if trainer.pullup_state=='DOWN':
                        cv2.putText(frame, trainer.pullup_state, (210, 50),
                                        cv2.FONT_HERSHEY_PLAIN, 3, (0, 0, 255), 4)
                    else:

                        cv2.putText(frame, trainer.pullup_state, (210, 50),
                                        cv2.FONT_HERSHEY_PLAIN, 3, (0, 255, 0), 4)

                    cv2.putText(frame, 'COUNTER: ', (h-245, 50),
                                    cv2.FONT_HERSHEY_PLAIN, 3, (255, 255, 255), 4)
                    
                    cv2.putText(frame, '{:03d}'.format(trainer.pullup_counter), (h-15, 50),
                                    cv2.FONT_HERSHEY_PLAIN, 4, (0, 200, 0), 4)
                
                
                elif args.exercise=='curl':

                    trainer.curl(img=frame,draw=True,pose_features=pose_features)

                    cv2.putText(frame, 'STATE: ', (40, 50),
                                    cv2.FONT_HERSHEY_PLAIN, 3, (255, 255, 255), 4)
                    if trainer.curl_state=='DOWN':
                        cv2.putText(frame, trainer.curl_state, (210, 50),
                                        cv2.FONT_HERSHEY_PLAIN, 3, (0, 0, 255), 4)
                    else:

                        cv2.putText(frame, trainer.curl_state, (210, 50),
                                        cv2.FONT_HERSHEY_PLAIN, 3, (0, 255, 0), 4)

                    cv2.putText(frame, 'COUNTER: ', (h-245, 50),
                                    cv2.FONT_HERSHEY_PLAIN, 3, (255, 255, 255), 4)
                    
                    cv2.putText(frame, '{:03d}'.format(trainer.curl_counter), (h-15, 50),
                                    cv2.FONT_HERSHEY_PLAIN, 4, (0, 200, 0), 4)
            else:
                
                
                frame=cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
                frame=Image.fromarray(frame)

                center = ((p1[0] + p2[0]) // 2, (p1[1] + p2[1]) // 2)

                # Calculate size of warning image (divided by 10 times of width and height of bounding box)
                new_size = ((p2[0] - p1[0]) // 3, (p2[1] - p1[1]) // 3)

                # Open the warning image

                
                warning_image = Image.open('images/fall_logo.jpg')

                
                
                # Resize the warning image
                warning_image_resized = warning_image.resize(new_size)


                # Calculate top left corner of warning image so it is centered within the bounding box
                warning_position = (center[0] - new_size[0] // 2, center[1] - new_size[1] // 2)

                
                frame.paste(warning_image_resized, warning_position)
                

                frame=np.array(frame)
                frame=cv2.cvtColor(frame, cv2.COLOR_RGB2BGR)
                draw_border(frame,p1,p2,color=(0,0,255))
                if args.fall_alert:
                    frequency = 2500  # Adjust the frequency as needed
                    duration = 250  # Adjust the duration as needed
                    winsound.Beep(frequency, duration)
        
                    print('Call for safety')
           
        
        else:

            

            if args.exercise=='pullup':

                    trainer.pullup(img=frame,draw=True,pose_features=pose_features)

                    cv2.putText(frame, 'STATE: ', (40, 50),
                                    cv2.FONT_HERSHEY_PLAIN, 3, (255, 255, 255), 4)
                    if trainer.pullup_state=='DOWN':
                        cv2.putText(frame, trainer.pullup_state, (210, 50),
                                        cv2.FONT_HERSHEY_PLAIN, 3, (0, 0, 255), 4)
                    else:

                        cv2.putText(frame, trainer.pullup_state, (210, 50),
                                        cv2.FONT_HERSHEY_PLAIN, 3, (0, 255, 0), 4)

                    cv2.putText(frame, 'COUNTER: ', (h-245, 50),
                                    cv2.FONT_HERSHEY_PLAIN, 3, (255, 255, 255), 4)
                    
                    cv2.putText(frame, '{:03d}'.format(trainer.pullup_counter), (h-15, 50),
                                    cv2.FONT_HERSHEY_PLAIN, 4, (0, 200, 0), 4)
                
                
            elif args.exercise=='curl':

                trainer.curl(img=frame,draw=True,pose_features=pose_features)

                cv2.putText(frame, 'STATE: ', (40, 50),
                                cv2.FONT_HERSHEY_PLAIN, 3, (255, 255, 255), 4)
                if trainer.curl_state=='DOWN':
                    cv2.putText(frame, trainer.curl_state, (210, 50),
                                    cv2.FONT_HERSHEY_PLAIN, 3, (0, 0, 255), 4)
                else:

                    cv2.putText(frame, trainer.curl_state, (210, 50),
                                    cv2.FONT_HERSHEY_PLAIN, 3, (0, 255, 0), 4)

                cv2.putText(frame, 'COUNTER: ', (h-245, 50),
                                cv2.FONT_HERSHEY_PLAIN, 3, (255, 255, 255), 4)
                
                cv2.putText(frame, '{:03d}'.format(trainer.curl_counter), (h-15, 50),
                                cv2.FONT_HERSHEY_PLAIN, 4, (0, 200, 0), 4)
                


            elif args.exercise=='pushup':

                trainer.pushup(img=frame,draw=True,pose_features=pose_features)

                cv2.putText(frame, 'STATE: ', (40, 50),
                                cv2.FONT_HERSHEY_PLAIN, 3, (255, 255, 255), 4)
                if trainer.pushup_state=='DOWN':
                    cv2.putText(frame, trainer.pushup_state, (210, 50),
                                    cv2.FONT_HERSHEY_PLAIN, 3, (0, 0, 255), 4)
                else:

                    cv2.putText(frame, trainer.pushup_state, (210, 50),
                                    cv2.FONT_HERSHEY_PLAIN, 3, (0, 255, 0), 4)

                cv2.putText(frame, 'COUNTER: ', (h-245, 50),
                                cv2.FONT_HERSHEY_PLAIN, 3, (255, 255, 255), 4)
                
                cv2.putText(frame, '{:03d}'.format(trainer.pushup_counter), (h-15, 50),
                                cv2.FONT_HERSHEY_PLAIN, 4, (0, 200, 0), 4)


        
    
        

        
            
            
        
        frame_array.append(frame)
        cv2.imshow(args.exercise,frame)
        if cv2.waitKey(1)==27:

            if args.saved_video:

                saved_video_dire='result_video/{}'.format(os.path.basename(args.video_path))

                if not os.path.exists('result_video'):
                    os.makedirs('result_video')

                save_video(save_dir=saved_video_dire,img_arr=frame_array)

            break

    
    cap.release()
    cv2.destroyAllWindows()


    if args.saved_video:

        saved_video_dire='result_video/{}'.format(os.path.basename(args.video_path))

        if not os.path.exists('result_video'):
            os.makedirs('result_video')

        save_video(save_dir=saved_video_dire,img_arr=frame_array)


 




