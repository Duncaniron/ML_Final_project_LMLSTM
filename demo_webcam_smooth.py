# coding: utf-8

__author__ = 'cleardusk'
from collections import Counter
import argparse
import imageio
import cv2
import os
import numpy as np
from tqdm import tqdm
import yaml
from collections import deque
from new_ut import normalize_landmark
from new_ut import save_data
from new_ut import vote
from FaceBoxes import FaceBoxes
from TDDFA import TDDFA
from utils.render import render
# from utils.render_ctypes import render
from utils.functions import cv_draw_landmark
from knnLandmarkClassifier import KNN
import win32gui, win32con

aa = "Testing"
def Draw_name(img, pts, name):

    x = img.shape[1] - int(round((pts[0, 21] + pts[0,22]) / 2))
    y = int(round(pts[1, 21] + pts[1, 21] - pts[1, 27]))
    x = x - 7 * len(name)

    cv2.putText(img, name , (x, y), cv2.FONT_HERSHEY_SIMPLEX,
            1, (0, 255, 255), 1, cv2.LINE_AA)

    return img

top_left_fir, top_left_sec = 150, 450 
status_color = [(22, 20, 222), (22, 50, 222), (22, 75, 222), (22, 100, 222), (22, 125, 222), (22, 150, 222), (22, 175, 222), (22, 200, 222), (22, 222, 215), (22, 222, 139), (22, 222, 55)]

thickness = 50

def Draw_have_savedata(img, havesavedata):

    for i, num in enumerate(havesavedata):
        cv2.rectangle(img, (top_left_fir + i * 80, top_left_sec), (top_left_fir + i * 80 + 50, top_left_sec - (num + 1) * 6) , status_color[num], -1)

    for i, num in enumerate(havesavedata):
        cv2.rectangle(img, (top_left_fir + i * 80, top_left_sec), (top_left_fir + i * 80 + 50, top_left_sec - 11 * 6) , (0, 0, 0), 3)

    return img 


def caculate_angle(vector_a, vector_b):
    #print(vector_a, vector_b)
    dot_product = np.dot(vector_a, vector_b)
    magnitude_a = np.linalg.norm(vector_a)
    magnitude_b = np.linalg.norm(vector_b)
    cosine_theta = dot_product / (magnitude_a * magnitude_b)
    theta_radians = np.arccos(cosine_theta)
    theta_degrees = np.degrees(theta_radians)
    return theta_degrees


def main(args):
    cfg = yaml.load(open(args.config), Loader=yaml.SafeLoader)

    # Init FaceBoxes and TDDFA, recommend using onnx flag
    if args.onnx:
        os.environ['KMP_DUPLICATE_LIB_OK'] = 'True'
        os.environ['OMP_NUM_THREADS'] = '4'

        from FaceBoxes.FaceBoxes_ONNX import FaceBoxes_ONNX
        from TDDFA_ONNX import TDDFA_ONNX

        face_boxes = FaceBoxes_ONNX()
        tddfa = TDDFA_ONNX(**cfg)
    else:
        gpu_mode = args.mode == 'gpu'
        tddfa = TDDFA(gpu_mode=gpu_mode, **cfg)
        face_boxes = FaceBoxes()

    # Given a camera
    # before run this line, make sure you have installed `imageio-ffmpeg`
    reader = imageio.get_reader("<video0>")

    # the simple implementation of average smoothing by looking ahead by n_next frames
    # assert the frames of the video >= n
    n_pre, n_next = args.n_pre, args.n_next
    n = n_pre + n_next + 1
    queue_ver = deque()
    queue_frame = deque()
    data_have_saved = [0,0,0,0]
    # run
    dense_flag = args.opt in ('2d_dense', '3d')
    pre_ver = None
    name_now = 'none'
    queue = []
    name_map = Counter()
    intruder_count = 0
    for i, frame in tqdm(enumerate(reader)):
        frame_bgr = frame[..., ::-1]  # RGB->BGR
        if i == 0:
            # the first frame, detect face, here we only use the first face, you can change depending on your need
            boxes = face_boxes(frame_bgr)
            boxes = [boxes[0]]
            param_lst, roi_box_lst = tddfa(frame_bgr, boxes)
            ver = tddfa.recon_vers(param_lst, roi_box_lst, dense_flag=dense_flag)[0]

            # refine
            param_lst, roi_box_lst = tddfa(frame_bgr, [ver], crop_policy='landmark')
            #print(param_lst)
            ver = tddfa.recon_vers(param_lst, roi_box_lst, dense_flag=dense_flag)[0]
            #print(ver)
            # padding queue
            for _ in range(n_pre):
                queue_ver.append(ver.copy())
            queue_ver.append(ver.copy())

            for _ in range(n_pre):
                queue_frame.append(frame_bgr.copy())
            queue_frame.append(frame_bgr.copy())
        else:
            param_lst, roi_box_lst = tddfa(frame_bgr, [pre_ver], crop_policy='landmark')

            roi_box = roi_box_lst[0]
            # todo: add confidence threshold to judge the tracking is failed
            if abs(roi_box[2] - roi_box[0]) * abs(roi_box[3] - roi_box[1]) < 2020 :
                boxes = face_boxes(frame_bgr)
                boxes = [boxes[0]]
                param_lst, roi_box_lst = tddfa(frame_bgr, boxes)

            ver = tddfa.recon_vers(param_lst, roi_box_lst, dense_flag=dense_flag)[0]
            ver_d = tddfa.recon_vers(param_lst, roi_box_lst, dense_flag=dense_flag)
            queue_ver.append(ver.copy())
            queue_frame.append(frame_bgr.copy())

        pre_ver = ver  # for tracking
        if(i%3 == 0 and i >= 10):
            data, valid_d = normalize_landmark(ver_d)
            deg = save_data(ver_d)
            #print(i, valid_d)
            cat = 0
            if 0<deg<=60:
                cat = 3
            elif 60<deg<=90:
                cat = 2
            elif 90<deg<=120:
                cat = 1
            else:
                cat = 0
            #print(data_have_saved)
            ss = str(cat)
            if(args.name != 'none'):
                save_path = "./degree_data_4/"+ss+"/"+args.name+"/"
                if not os.path.exists(save_path):
                    os.makedirs(save_path)
                file_list = os.listdir(save_path)
                if(len(file_list)<=10):
                    save_path = "./degree_data_4/"+ss+"/"+args.name+"/npdata_"+str(i)+".npy"
                    np.save(save_path, data)
                    data_have_saved[cat]=len(file_list)
                name_now = ss+":"+ str(len(file_list))
            else:
                knn_tester = KNN(5,ss)
                knn_tester.load_data('./degree_data_4/')
                knn_tester.train_model()
                name_now = knn_tester.predict(data)
                queue.append(name_now)
                name_map[name_now] += 1
                name_now = vote(queue=queue, map=name_map, n=10)
        if name_now == "Intruder":
            intruder_count+=1
        print("ic: "+ str(intruder_count))
        # smoothing: enqueue and dequeue ops
        if len(queue_ver) >= n:
            ver_ave = np.mean(queue_ver, axis=0)

            if args.opt == '2d_sparse':
                img_draw = cv_draw_landmark(queue_frame[n_pre], ver_ave)  # since we use padding
            elif args.opt == '2d_dense':
                img_draw = cv_draw_landmark(queue_frame[n_pre], ver_ave, size=1)
            elif args.opt == '3d':
                img_draw = render(queue_frame[n_pre], [ver_ave], tddfa.tri, alpha=0.7)
            else:
                raise ValueError(f'Unknown opt {args.opt}')

            img_draw = cv2.flip(img_draw, 1)
            if intruder_count >= 30 and args.name == 'none':
                cv2.imwrite('./intruder/output'+str(i)+'.png', img_draw)
                intruder_count = 0
            img_draw = Draw_name(img_draw, ver_ave, name_now)
            
            if(args.name != 'none'):
                img_draw = Draw_have_savedata(img_draw, data_have_saved)

            cv2.namedWindow('FaceVerify')
            cv2.imshow('FaceVerify', img_draw)
            cv2.setWindowProperty('FaceVerify', cv2.WND_PROP_TOPMOST, 1)

            k = cv2.waitKey(2)
            
            if (k & 0xff == ord('q')):
                print(name_now)
                break

            queue_ver.popleft()
            queue_frame.popleft()


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='The smooth demo of webcam of 3DDFA_V2')
    parser.add_argument('-c', '--config', type=str, default='configs/mb1_120x120.yml')
    parser.add_argument('-m', '--mode', default='cpu', type=str, help='gpu or cpu mode')
    parser.add_argument('-o', '--opt', type=str, default='2d_sparse', choices=['2d_sparse', '2d_dense', '3d'])
    parser.add_argument('-n_pre', default=1, type=int, help='the pre frames of smoothing')
    parser.add_argument('-n_next', default=1, type=int, help='the next frames of smoothing')
    parser.add_argument('--onnx', action='store_true', default=False)
    parser.add_argument('-name', type=str, default='none')

    args = parser.parse_args()
    main(args)
