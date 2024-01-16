# coding: utf-8

__author__ = 'cleardusk'
import matplotlib.pyplot as plt
import sys
import argparse
import cv2
import yaml
import numpy as np
import os
from FaceBoxes import FaceBoxes
from TDDFA import TDDFA
from utils.render import render
from utils.depth import depth
from utils.pncc import pncc
from utils.uv import uv_tex
from utils.pose import viz_pose
from utils.serialization import ser_to_ply, ser_to_obj
from utils.functions import draw_landmarks, get_suffix
from utils.tddfa_util import str2bool
from scipy.spatial.transform import Rotation

def get_all_group(folder_path,target_folder):
    sub_folders_g = [sub_folder_name for sub_folder_name in os.listdir(folder_path)
               if os.path.isdir(os.path.join(folder_path, sub_folder_name))]
    sub_folders_g = sorted(sub_folders_g)
    return sub_folders_g

def pic_to_lanmark(path, name = "nothing", index = 0):
    cfg = yaml.load(open('configs/mb1_120x120.yml'), Loader=yaml.SafeLoader)
    tddfa = TDDFA(gpu_mode=False, **cfg)
    face_boxes = FaceBoxes()
    img = cv2.imread(path)
    boxes = face_boxes(img)
    param_lst, roi_box_lst = tddfa(img, boxes)

    
    ver_lst = tddfa.recon_vers(param_lst, roi_box_lst, dense_flag=False)
    len(ver_lst)
    try:
        out_ver = np.array([ver_lst[0][0][0],ver_lst[0][1][0],ver_lst[0][2][0]])
    except:
        return np.array([1,2,3]), False
    center = np.array([ver_lst[0][0][0],ver_lst[0][1][0],ver_lst[0][2][0]])
    for i in range (67):
        temp_ver = [ver_lst[0][0][i+1],ver_lst[0][1][i+1],ver_lst[0][2][i+1]]
        center += temp_ver
        out_ver = np.vstack((out_ver,temp_ver))
    center[0] = center[0]/68
    center[1] = center[1]/68
    center[2] = center[2]/68
    
    out_ver = np.vstack((out_ver,center))
    

    data = out_ver
    data -= data[68]
    x_axis = np.array([1, 0, 0])
    z_axis = np.array([0, 0, 1])
    aa = data[8]
    vector = [aa[0], aa[1], 0]
    angle_x = np.arccos(np.dot(vector, x_axis) / (np.linalg.norm(vector) * np.linalg.norm(x_axis)))
    
    theta =angle_x

    rotation_matrix = np.array([[np.cos(theta), -np.sin(theta), 0],
                [np.sin(theta), np.cos(theta), 0],
                [0, 0, 1]])

    data_rotated_adjusted = (data).dot(rotation_matrix.T)
    if(round(data_rotated_adjusted[8][1], 3)!= 0):
        theta =np.pi - angle_x
        rotation_matrix = np.array([[np.cos(theta), -np.sin(theta), 0],
                [np.sin(theta), np.cos(theta), 0],
                [0, 0, 1]])
        data_rotated_adjusted = (data).dot(rotation_matrix.T)

    data = data_rotated_adjusted


    aa = data[8]
    vector = [aa[0], 0, aa[2]]
    angle_z = np.arccos(np.dot(vector, z_axis) / (np.linalg.norm(vector) * np.linalg.norm(z_axis)))
    theta =angle_z
    rotation_matrix = np.array([[np.cos(theta), 0, np.sin(theta)],
                [0, 1, 0],
                [-np.sin(theta), 0, np.cos(theta)]])

    data_rotated_adjusted = (data).dot(rotation_matrix.T)
    if(round(data_rotated_adjusted[8][1], 3)!= 0):
        theta =np.pi - angle_z
        rotation_matrix = np.array([[np.cos(theta), -np.sin(theta), 0],
                [np.sin(theta), np.cos(theta), 0],
                [0, 0, 1]])
        data_rotated_adjusted = (data).dot(rotation_matrix.T)
    data = data_rotated_adjusted



    aa = data[30]
    vector = [aa[0], aa[1], 0]
    angle_x = np.arccos(np.dot(vector, x_axis) / (np.linalg.norm(vector) * np.linalg.norm(x_axis)))
    theta =angle_x
    rotation_matrix = np.array([[np.cos(theta), -np.sin(theta), 0],
                [np.sin(theta), np.cos(theta), 0],
                [0, 0, 1]])

    data_rotated_adjusted = (data).dot(rotation_matrix.T)
    if(round(data_rotated_adjusted[30][1], 3)!= 0):
        theta =np.pi - angle_x
        rotation_matrix = np.array([[np.cos(theta), -np.sin(theta), 0],
                [np.sin(theta), np.cos(theta), 0],
                [0, 0, 1]])
        data_rotated_adjusted = (data).dot(rotation_matrix.T)
    data = data_rotated_adjusted

    scale = np.sqrt(data[8][0]**2 + data[8][1]**2 + data[8][2]**2)/100

    data/=scale
    if(data[30][0] < 0):
        data[:, 0] = -data[:, 0]

    if(data[8][2] > 0):
        data[:, 2] = -data[:, 2]

    fig = plt.figure(figsize=(10, 8))
    ax = fig.add_subplot(111, projection='3d')
    ax.scatter(data[:, 0], data[:, 1], data[:, 2])
    ax.view_init(elev=1000, azim=1000)  
    ax.set_xlabel('X Label')
    ax.set_ylabel('Y Label')
    ax.set_zlabel('Z Label')

    ax.set_xlim(-100, 100)
    ax.set_ylim(-100, 100)
    ax.set_zlim(-100, 100)
    plt.title(path)
    #ax.view_init(elev=0, azim=0) #y to xz
    #ax.view_init(elev=90, azim=0) #z to xy
    ax.view_init(elev=0, azim=90) #x to zy
    ax.set_box_aspect([1, 1, 1])
    #plt.show()
    return data, True


def main(args):
    #pic_to_lanmark(args.img_fp)
    root = "./examples/data/"
    all_folder = get_all_group(root,"/data/") #
    print(all_folder)
    for sub_folder_name in all_folder:
        file_list = os.listdir(root+sub_folder_name)
        print(file_list)

        file_index = 0
        for f in file_list:
            file_path = root+sub_folder_name+"/"+f
            print(file_path)
            print(file_path)
            return_lanmark, useful = pic_to_lanmark(file_path,sub_folder_name, file_index)
            if(useful):
                save_path = "./example/landmark/"+sub_folder_name+"/npdata_"+str(file_index)+".npy"
                if not os.path.exists(save_path):
                    os.makedirs(save_path)
                np.save('my_array.npy', return_lanmark)
                file_index+=1



if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='The demo of still image of 3DDFA_V2')
    parser.add_argument('-c', '--config', type=str, default='configs/mb1_120x120.yml')
    parser.add_argument('-f', '--img_fp', type=str, default='examples/data/p_data04.jpg')
    parser.add_argument('-m', '--mode', type=str, default='cpu', help='gpu or cpu mode')
    parser.add_argument('-o', '--opt', type=str, default='2d_sparse',
                        choices=['2d_sparse', '2d_dense', '3d', 'depth', 'pncc', 'uv_tex', 'pose', 'ply', 'obj'])
    parser.add_argument('--show_flag', type=str2bool, default='true', help='whether to show the visualization result')
    parser.add_argument('--onnx', action='store_true', default=False)

    args = parser.parse_args()
    path = args.img_fp
    main(args)
