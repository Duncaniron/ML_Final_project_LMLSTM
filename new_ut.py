import numpy as np
from collections import Counter

def normalize_landmark(ver_lst):
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

    if(data[0][1] < 0):
        data[:, 1] = -data[:, 1]

    
    return data, True

def save_data(ver_lst):
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
    scale = np.sqrt(data[33][0]**2 + data[33][1]**2 + data[33][2]**2)/100
    data/=scale
    #print(data[33][0]+90)
    deg = data[33][0]+90
    deg/=10
    tdeg = int(deg)
    #print(tdeg*10)
    return tdeg*10

def vote(queue, map, n):
    if len(queue) >= n:  
        votes = queue[-n:]  
        counter = Counter(votes)
        majority_name = counter.most_common(1)[0][0]  
        #print("winner:", majority_name)

        popped_name = queue.pop(0)
        map[popped_name] -= 1
        if map[popped_name] == 0:
            del map[popped_name]

        return majority_name
    else:
        return "none"