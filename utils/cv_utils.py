
import cv2
import winsound


    


def draw_border(img, point1, point2,color=(0,255,0)):

    x1, y1 = point1
    x3, y3 = point2
    x2,y2=x1,y3
    x4, y4 = x3,y1 
    h=int(y3-y1)
    w=int(x3-x1)
    line_hlength=h//10  
    line_wlength=w//10  
   

    cv2.line(img, (x1, y1), (x1 , y1 + line_hlength), color, 4)  #-- top-left
    cv2.line(img, (x1, y1), (x1 + line_wlength , y1), color, 4)

    cv2.line(img, (x2, y2), (x2 , y2 - line_hlength), color, 4)  #-- bottom-left
    cv2.line(img, (x2, y2), (x2 + line_wlength , y2), color, 4)

    cv2.line(img, (x3, y3), (x3 - line_wlength, y3), color, 4)  #-- top-right
    cv2.line(img, (x3, y3), (x3, y3 - line_hlength), color, 4)

    cv2.line(img, (x4, y4), (x4 , y4 + line_hlength), color, 4)  #-- bottom-right
    cv2.line(img, (x4, y4), (x4 - line_wlength , y4), color, 4)

    return img



def save_video(save_dir,img_arr,fps=30):

    h,w,_=img_arr[0].shape

    fourcc = cv2.VideoWriter_fourcc(*'mp4v')  # Specify the codec (FourCC)
    out = cv2.VideoWriter(save_dir, fourcc, fps, (w, h))

    for img in img_arr:

        out.write(img)


