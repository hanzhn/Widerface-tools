import numpy as np
import cv2
import os
import math

def draw_groundtruths():
    for i in ["01", "02", "03", "04", "05", "06", "07", "08", "09", "10"]:
        f = open("/home/smiles/hz/databases/FDDB/FDDB-folds/FDDB-fold-"+i+"-ellipseList.txt", 'r')
       
        line = f.readline().strip('\n')
        while line:
            img = cv2.imread("/home/smiles/hz/darknet/results/"+line+".jpg")
            print line
            # # the np.array indicate shape[0] as h, shape[1] as w
            # h = img.shape[0]
            # w = img.shape[1]
            # print w, h
            num = int( f.readline().strip('\n') )
            # convert ellipse to rectangle
            for i in range(num):
                ellipse = f.readline().strip('\n').split(' ')
                centerx = int( float(ellipse[3]) )
                centery = int( float(ellipse[4]) )
                major = int( float(ellipse[0]) )
                minor = int( float(ellipse[1]) )
                angle = float( ellipse[2] )
                cv2.ellipse( img, (centerx,centery), (major,minor), angle/math.pi*180, 0, 360, (255,0,0) )
            cv2.imwrite("/home/smiles/hz/darknet/results/"+line+".jpg", img)

                # a = float(ellipse[0])
                # b = float(ellipse[1])
                # c = float( -math.tan( float(ellipse[2]) ) )
                # x = float(ellipse[3])
                # y = float(ellipse[4])
                # w_half = float( math.sqrt( (b*b*c*c+a*a)/(c*c+1.) ) )          
                # h_half = float( math.sqrt( (b*b+a*a*c*c)/(c*c+1.) ) ) 
                # #cv2.rectangle( img, (int(x-w_half), int(y-h_half)), (int(x+w_half), int(y+h_half)), (0,255,0) )
                # cv2.rectangle( img, (int(x-w_half*0.85), int(y-h_half*0.85)), (int(x+w_half*0.85), int(y+h_half*0.85)), (0,255,0) )
                # x = x/w
                # y = y/h
                # w_half = w_half/w
                # h_half = h_half/h
                # # if the rectangle is reached out of the image range, adjust it
                # if x<w_half:
                #     dis = w_half - x
                #     x = (2.*w_half-dis)/2.
                #     w_half = x
                # if y<h_half:
                #     dis = h_half - y
                #     y = (2.*h_half-dis)/2.
                #     h_half = y
                # if x+w_half>1:
                #     dis = x+w_half-1
                #     w_half = (2.*w_half-dis)/2.
                #     x = 1 - w_half
                # if y+h_half>1:
                #     dis = y+h_half-1
                #     h_half = (2.*h_half-dis)/2.
                #     y = 1 - h_half

            # cv2.namedWindow("image")
            # cv2.imshow("image", img)
            # cv2.waitKey(0)
            # cv2.destroyAllWindows()

            # templist = line.split('/')
            # picpath = "/home/smiles/hz/databases/FDDB/groundtruth-pics/"+'/'.join( templist[0:len(templist)-1] )
            # if not os.path.isdir(picpath):
            #     os.makedirs(picpath)
            # cv2.imwrite("/home/smiles/hz/databases/FDDB/groundtruth-pics/"+line+".jpg", img)
            
            line = f.readline().strip('\n')
        f.close()
        

draw_groundtruths()
