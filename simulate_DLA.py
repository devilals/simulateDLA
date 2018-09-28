import time
import sys
import argparse
import cv2
import numpy as np
import random
from random import randint

# The image size is  MxM pixels 
# Number of particles N

#M = 100
#N = 500
#channels = 3
#k = 1.0

white_p = [255,255,255]
black_p = [0,0,0]

def particle_origin_point(M):
    s = randint(0,3)	#randomly select a side
    n = randint(0,M-1)  #randomly select a point on a side

    #below are possible four points in the matrix for sides, left, bottom, right, top
    points = [[n, 0], [M-1, n], [n, M-1], [0, n]]

    #return point on the randomly selected side
    return points[s]

def is_position_valid(pos, M):
    if pos[0] >=0 and pos[0] < M:
        if pos[1] >=0 and pos[1] <M:
            return True

    return False

def fix_invalid_position(pos, M):
    if pos[0] < 0:
        pos[0] = pos[0] + M
    if pos[0] > M-1:
        pos[0] = pos[0] - M
    if pos[1] < 0:
        pos[1] = pos[1] + M
    if pos[1] > M-1:
        pos[1] = pos[1] - M
    
    return pos

def check_black_particle_at_pos(img, pos):
    r,g,b = img[pos[0], pos[1]]
    if r==0 and g==0 and b==0:
        return True
    
    return False


# Should not move to black
def particle_random_move(img, pos, disp, M):
    #direction in which the motion to neighborig pixel position
    # total 8 directions including diagonals,
    # directions start with left and move anticlockwise
    
    while(1):
        di = randint(0,7)
        new_pos = np.add(pos, disp[di])

        #check for crossing the boundaries
        if not is_position_valid(new_pos, M):
            new_pos = fix_invalid_position(new_pos, M)
    
        #the new move should be on an empty shell or on a white pixel to avoid overlapping pixels
        if check_black_particle_at_pos(img, new_pos) == False:
            break
    
    return new_pos


def particle_check_nearby(img, pos, disp, M):

    #check if any of the eigth neighbors are black pixel
    # return true or false
    for i in range(0,8):
        check_pos = np.add(pos, disp[i])
        if is_position_valid(check_pos, M):
            if (img[check_pos[0], check_pos[1]] == 0)[0]:
            #if check_black_particle_at_pos(img, pos):
                return True
    return False

def init(M):
    channels = 3
    
    size = (w, h, channels) = (M, M, channels)
    img = np.zeros(size, np.int) #initialize with white_p
    for y in range(h):
        for x in range(w):
            img[y,x] = white_p
        
    #initialize one center pixel to be black
    img[int(M/2.0), int(M/2.0)] = black_p 
    #cv2.imwrite('initial_oneBlackPixel.png', img)
    
    return img

def main(args):	
    i = 1
    
    #Possible displacements in brownian motion
    disp = [[0,-1],[1,-1],[1,0],[1,1],[0,1],[-1,1],[-1,0],[-1,-1]]    
    
    img = init(args.m) #initialize matrix of size
    print("Matrix Size: ", args.m, "x", args.m)
    print("Number of particles: ", args.n)
    print("stickiness: ",args.k) 
    while i<args.n:
        pos = particle_origin_point(args.m)
        #print(pos)
    
        while 1:
            new_pos = particle_random_move(img, pos, disp, args.m)
            #print(new_pos)
            if particle_check_nearby(img, new_pos, disp, args.m) == True:
                if(args.k<1.0):
                    prob = random.uniform(0,1)
                    if prob <= args.k:
                        img[new_pos[0],new_pos[1]] = black_p 
                        #print(new_pos)
                        break
                else:
                    img[new_pos[0],new_pos[1]] = black_p 
                    #print(new_pos)
                    break
            pos = new_pos
    
        if (i%10 == 0):
            print(i)    
        i += 1

    cv2.imwrite(args.f, img)


def parse_arguments(argv):
    parser = argparse.ArgumentParser()
   
    parser.add_argument('-m', type=int,
        help='Matrix/Image size of one side', default=150)
    parser.add_argument('-n', type=int,
        help='Number of particles', default=1000)
    parser.add_argument('-k', type=float,
        help='stickiness in the range (0,1]', default=1.0)
    parser.add_argument('-f', type=str,
        help='filename to store generated DLA structure image', default='final_DLA_image.png')
    return parser.parse_args(argv)

def print_usage():
    print("Usage: -m [enter value of M in MxM matrix] -n [number of particles] -k [stickiness in the range (0,1] ] -f [filename string]")
    
if __name__ == '__main__':
 
    print(time.time())
    start_time = time.time()
    main(parse_arguments(sys.argv[1:]))
    print("--- %s seconds ---" % (time.time() - start_time))
