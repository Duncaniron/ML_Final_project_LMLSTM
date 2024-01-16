
import matplotlib.pyplot as plt
import sys
import argparse
import cv2
import yaml
import numpy as np
import os
import itertools


### 1. Read data
# get all group in folder
def get_all_group(folder_path):
    sub_folders_g = [sub_folder_name for sub_folder_name in os.listdir(folder_path)
               if os.path.isdir(os.path.join(folder_path, sub_folder_name))]
    sub_folders_g = sorted(sub_folders_g)
    return sub_folders_g
# get all data from all group
def data_reader(root, limit = 10000):
    gt_folder = get_all_group(root) 
    all_GT_data = []
    all_GT_name = []
    for sub_folder_name in gt_folder:
        file_list = os.listdir(root+sub_folder_name)
        file_index = 0
        all_data = []
        for f in file_list:
            file_path = root+sub_folder_name+"/"+f
            data = np.load(file_path)
            #all_data.append((data))
            all_data.append((data))
            file_index+=1
            if(file_index >limit):
                break
        np_all_data = np.array(all_data)
        #print(np_all_data.shape)
        all_GT_data.append(np_all_data)
        all_GT_name.append(sub_folder_name)


    np_all_GT_data = np.array(all_GT_data)
    return np_all_GT_data, all_GT_name

### 2. compute some value 
# calculate MSE between two array
def MSE(A,B):
    squared_errors = np.sum((A - B) ** 2)  
    mse = np.mean(squared_errors)  
    return mse
# calculate inner product between two array
def INP(A,B):
    inp_s = np.dot(A,B.T)
    inp = np.mean(inp_s) 
    return inp
# compare the mse between test data and all gt data
def cmp(id, test_data, all_gt, total_id):
    min_mse = 1000000000
    min_id = -1
    for i in range (total_id):
        for j in range (1):
            mse = MSE(test_data,all_gt[i][j])
            if mse < min_mse:
                min_mse = mse
                min_id = i 
    return min_id == id
# calculate the area of triangle
def calculate_triangle_area(point1, point2, point3):
    point1 = np.array(point1)
    point2 = np.array(point2)
    point3 = np.array(point3)
    AB = point2 - point1
    AC = point3 - point1
    cross_product = np.cross(AB, AC)
    area = 0.5 * np.linalg.norm(cross_product)
    return area
# calculate angle between two vector
def caculate_angle(vector_a, vector_b):
    dot_product = np.dot(vector_a, vector_b)
    magnitude_a = np.linalg.norm(vector_a)
    magnitude_b = np.linalg.norm(vector_b)
    cosine_theta = dot_product / (magnitude_a * magnitude_b)
    theta_radians = np.arccos(cosine_theta)
    theta_degrees = np.degrees(theta_radians)
    return theta_degrees
# calculate the mean and std of the feature
def calculate_feature_mean_std(feature_index, person_data):
    feature_data = []
    for i in range (person_data.shape[0]): #picture's num
            distance = np.linalg.norm(person_data[i, int(feature_index[0])] - person_data[i,int(feature_index[1])])
            feature_data.append(distance)
    feature_data_np = np.array(feature_data)
    mean = np.mean(feature_data_np)
    std = np.std(feature_data_np, ddof=1)
    return mean, std
# calculate the overlap percentage of the feature
def caclulate_overlap_percentage( all_mean_std ): # all_mean_std [person, [mean, std]]
    n = all_mean_std.shape[0]
    elements = np.arange(0, n )  
    combinations_list = list(itertools.combinations(elements, 2))
    combinations_array = np.array(combinations_list)
    overlap_num = 0
    for i,j in combinations_array:
        # print(i,j)
        if not (all_mean_std[i,0] + all_mean_std[i,1] < all_mean_std[j,0] - all_mean_std[j,1] or all_mean_std[j,0] + all_mean_std[j,1] < all_mean_std[i,0] - all_mean_std[i,1]):
            overlap_num+=1
    return overlap_num/combinations_array.shape[0]
# calculate the angle between three landmarks
def calculate_angle(point1, point2, point3):
    vector1 = point2 - point1
    vector2 = point3 - point1
    dot_product = np.dot(vector1, vector2)
    magnitude1 = np.linalg.norm(vector1)
    magnitude2 = np.linalg.norm(vector2)

    if magnitude1 == 0 or magnitude2 == 0:
        # deal with zero vectors
        raise ValueError("Zero vectors encountered, cannot calculate angle.")

    cosine_theta = dot_product / (magnitude1 * magnitude2)
    theta_radians = np.arccos(cosine_theta)
    theta_degrees = np.degrees(theta_radians)
    return theta_degrees
# calculate the mean and std of the angle feature
def calculate_angle_feature_mean_std(feature_indices, person_data):
    feature_data = []
    for i in range(person_data.shape[0]):
        angles = []
        calculated_angles = set()
        for j in range(len(feature_indices)):
            #l1, l2, l3 = feature_indices[j]
            angle_str = f"{feature_indices[0]}-{feature_indices[1]}-{feature_indices[2]}"
            if angle_str in calculated_angles:
                continue
            angle = calculate_angle(person_data[i, int(feature_indices[0])], person_data[i, int(feature_indices[1])], person_data[i, int(feature_indices[2])])
            angles.append(angle)
            calculated_angles.add(angle_str)
        feature_data.append(angles)
    feature_data_np = np.array(feature_data)
    means = np.mean(feature_data_np, axis=0)
    stds = np.std(feature_data_np, axis=0, ddof=1)
    return means, stds
# calculate the overlap percentage of the angle feature
def caclulate_angle_overlap_percentage(all_mean_std): # all_mean_std [person, [mean, std]]
    n = all_mean_std.shape[0]
    elements = np.arange(0, n )  
    combinations_list = list(itertools.combinations(elements, 2))
    combinations_array = np.array(combinations_list)
    overlap_num = 0
    for i,j in combinations_array:
        # print(i,j)
        if not (all_mean_std[i,0] + all_mean_std[i,1] < all_mean_std[j,0] - all_mean_std[j,1] or all_mean_std[j,0] + all_mean_std[j,1] < all_mean_std[i,0] - all_mean_std[i,1]):
            overlap_num+=1
    return overlap_num/combinations_array.shape[0]
# output all possible combination of two landmarks
def output_all_kind_of_two_landmark(landmark_num):
    elements = np.arange(0, landmark_num ) 
    combinations_list = list(itertools.combinations(elements, 2))
    combinations_array = np.array(combinations_list)
    return combinations_array
# output all possible combination of three landmarks
def output_all_kind_of_three_landmark(landmark_num):
    elements = np.arange(0, landmark_num)
    combinations_list = list(itertools.combinations(elements, 3))
    combinations_list = np.array(combinations_list)
    return combinations_list

### 3. extract feature
# extract feature 1 from fixed landmarks about angle 
def extract_feature_1(face_landmark):
    extract_feature_list = []
    f1 = caculate_angle(face_landmark[2]-face_landmark[3], face_landmark[5]-face_landmark[6])
    f2 = caculate_angle(face_landmark[14]-face_landmark[13], face_landmark[10]-face_landmark[11])
    f3 = caculate_angle(face_landmark[8]-face_landmark[7], face_landmark[4]-face_landmark[7])
    f4 = caculate_angle(face_landmark[8]-face_landmark[9], face_landmark[12]-face_landmark[9])
    f5 = caculate_angle(face_landmark[33]-(face_landmark[4]+face_landmark[12])/2, [1,0,0])
    extract_feature_list = [f1,f2,f3,f4,f5]
    extract_feature_np = np.array(extract_feature_list)
    return extract_feature_np
# extract feature 2 from some fixed landmarks about distance and normalize
def extract_feature_2(face_landmark):
    extract_feature_list = []
    f1 = np.linalg.norm(face_landmark[45] - face_landmark[36])
    f2 = np.linalg.norm(face_landmark[33] - face_landmark[51])
    f3 = np.linalg.norm(face_landmark[33] - face_landmark[8])
    f4 = np.linalg.norm(face_landmark[12] - face_landmark[4])
    f5 = np.linalg.norm(face_landmark[16] - face_landmark[0])
    extract_feature_list = [f1,f2, f3, f4, f5]
    extract_feature_np = np.array(extract_feature_list)
    return extract_feature_np
# extract feature 3(tina) from some fixed landmarks about distance and normalize
def extract_feature_tina(face_landmark):
    extract_feature_list = []
    f1 = np.linalg.norm(face_landmark[6] - face_landmark[10])
    f2 = np.linalg.norm(face_landmark[66] - face_landmark[57])
    f3 = np.linalg.norm(face_landmark[30] - face_landmark[16])
    f4 = np.linalg.norm(face_landmark[27] - face_landmark[12])
    f5 = np.linalg.norm(face_landmark[57] - face_landmark[8])
    f6 = np.linalg.norm(face_landmark[35] - face_landmark[31])
    f7 = np.linalg.norm(face_landmark[17] - face_landmark[26])
    f8 = np.linalg.norm(face_landmark[22] - face_landmark[26])
    extract_feature_list = [f1,f2,f3,f4,f5,f6,f7,f8]
    extract_feature_np = np.array(extract_feature_list)
    return extract_feature_np
# extract feature 4(temp) from some fixed landmarks about distance and normalize
def extract_feature_temp(face_landmark):
    extract_feature_list = []
    f1 = np.linalg.norm(face_landmark[8] - face_landmark[0])
    extract_feature_list = [f1]
    extract_feature_np = np.array(extract_feature_list)
    return extract_feature_np

### 4. show data on 3D space or draw line
# show the landmark on 3D space
def show(data, name = "null"):
    fig = plt.figure(figsize=(10, 8))
    ax = fig.add_subplot(111, projection='3d')
    ax.scatter(data[:, 0], data[:, 1], data[:, 2])
    ax.view_init(elev=1000, azim=1000)  
    ax.set_xlabel('X Label')
    ax.set_ylabel('Y Label')
    ax.set_zlabel('Z Label')
    plt.title(name)
    ax.set_xlim(-100, 100)
    ax.set_ylim(-100, 100)
    ax.set_zlim(-100, 100)
    ax.view_init(elev=0, azim=0) #y to xz
    #ax.view_init(elev=90, azim=0) #z to xy
    #ax.view_init(elev=0, azim=90) #x to zy
    #ax.view_init(elev=30, azim=30) #45 to 45
    ax.set_box_aspect([1, 1, 1])
    for i, value in enumerate(data):
        ax.text(data[i, 0], data[i, 1], data[i, 2], str(i), ha='center', va='bottom')
    plt.show()
# show the landmark on 3D space and draw line
def show_line(data, landmark_array, name = "null" ): #landmark_array shape is (n,2)
    fig = plt.figure(figsize=(10, 8))
    ax = fig.add_subplot(111, projection='3d')
    ax.scatter(data[:, 0], data[:, 1], data[:, 2])
    ax.view_init(elev=1000, azim=1000)  
    ax.set_xlabel('X Label')
    ax.set_ylabel('Y Label')
    ax.set_zlabel('Z Label')
    plt.title(name)
    ax.set_xlim(-100, 100)
    ax.set_ylim(-100, 100)
    ax.set_zlim(-100, 100)
    ax.view_init(elev=0, azim=0) #y to xz
    #ax.view_init(elev=90, azim=0) #z to xy
    #ax.view_init(elev=0, azim=90) #x to zy
    #ax.view_init(elev=30, azim=30) #45 to 45
    ax.set_box_aspect([1, 1, 1])
    for i, value in enumerate(data):
        ax.text(data[i, 0], data[i, 1], data[i, 2], str(i), ha='center', va='bottom')
    for i in range (landmark_array.shape[0]):
        ax.plot([data[(landmark_array[i][0])][0], data[landmark_array[i][1]][0]], [data[landmark_array[i][0]][1], data[landmark_array[i][1]][1]], [data[landmark_array[i][0]][2], data[landmark_array[i][1]][2]], 'r')
    plt.show()
# plot the line of the selected features
def draw_line(input_all_data, input_names,feature_index = 2,show_num = 3,start_num = 9):
    print(input_all_data.shape)
    plt.figure(figsize=(20, 6))     
    x_data = np.arange(0, input_all_data.shape[1], 5)
    for i in range (show_num):
        plt.plot(input_all_data[i+start_num][:,feature_index:feature_index+1], label=input_names[i+start_num])
    plt.title("feature "+str(feature_index))
    plt.legend()
    plt.xlabel('X')
    plt.ylabel('Y')

    plt.xticks(x_data)
    plt.show()
# show the landmark on 3D space and draw line
def show_angle(data, landmark_array, name="null"):  # landmark_array shape is (n,2)
    fig = plt.figure(figsize=(10, 8))
    ax = fig.add_subplot(111, projection='3d')
    ax.scatter(data[:, 0], data[:, 1], data[:, 2])
    ax.view_init(elev=1000, azim=1000)
    ax.set_xlabel('X Label')
    ax.set_ylabel('Y Label')
    ax.set_zlabel('Z Label')
    plt.title(name)
    ax.set_xlim(-100, 100)
    ax.set_ylim(-100, 100)
    ax.set_zlim(-100, 100)
    ax.view_init(elev=0, azim=0)  # y to xz
    ax.set_box_aspect([1, 1, 1])

    for i, value in enumerate(data):
        ax.text(data[i, 0], data[i, 1], data[i, 2], str(i), ha='center', va='bottom')

    for i in range(landmark_array.shape[0]):
        ax.plot([data[(landmark_array[i][0])][0], data[landmark_array[i][1]][0]],
                [data[landmark_array[i][0]][1], data[landmark_array[i][1]][1]],
                [data[landmark_array[i][0]][2], data[landmark_array[i][1]][2]], 'r')

    # Draw the second line (landmark1 to landmark3)
    for i in range(landmark_array.shape[0]):
        ax.plot([data[(landmark_array[i][0])][0], data[landmark_array[i][2]][0]],
                [data[landmark_array[i][0]][1], data[landmark_array[i][2]][1]],
                [data[landmark_array[i][0]][2], data[landmark_array[i][2]][2]], 'r')

    plt.show()
# show the distances and angles between all pairs of points
def show_dis_angle(all_test_data):
    for i in range(all_test_data.shape[0]):
        person_data = all_test_data[i, 0, :, :]
        # get the selected points
        selected_points = person_data[:, 21:66]
        # compute the distances between all pairs of points
        distances = np.linalg.norm(selected_points[:, :, np.newaxis, :] - selected_points[:, np.newaxis, :, :], axis=-1)
        # extract the indices of the points we want to use
        indices = [36, 39, 47]
        # compute the angles between all triplets of points
        angles = [calculate_angle(selected_points[:, i, :], selected_points[:, j, :], selected_points[:, k, :]) for i, j, k in zip(*[iter(indices)]*3)]
        # flatten the arrays
        flat_distances = distances.flatten()
        flat_angles = np.repeat(angles, distances.shape[1]**2)
        # plot the data
        plt.scatter(flat_angles, flat_distances, label=f"Person {i}")

    plt.xlabel('Angle (degrees)')
    plt.ylabel('Distance')
    plt.legend()
    plt.show()
# draw line of mean and std
def draw_line_mean_std( line_data):
    plt.figure()     
    # x_data = np.arange(0, line_data.shape[1], 5)
    for i in range (line_data.shape[0]):
        plt.plot([line_data[i][0] - line_data[i][1], line_data[i][0] + line_data[i][1]], [i,i], label=str(i))
        plt.scatter(line_data[i][0], i, marker='o', label='Point')
    plt.title("feature ")
    plt.legend()
    plt.xlabel('X')
    plt.ylabel('Y')

    # plt.xticks(x_data)
    plt.show()

def main(args):
    gt_root = "./example/example/landmark_cel/ground_truth/"
    test_root = "./example/example/landmark_cel/Test/"

    all_test_data, all_test_name = data_reader(test_root, 50)
    all_gt_data, all_gt_name = data_reader(gt_root, 5)

    '''
    One of the feature analysis is shown below.
    '''
    # comb_array = [landmark1, landmark2, overlap_percentage, (all people's var sum)/(all people's mean var)]
    comb_array =  output_all_kind_of_two_landmark(all_test_data.shape[2])
    print(comb_array.shape)
    new_column = np.zeros((2346, 1))
    comb_array = np.hstack((comb_array, new_column))
    comb_array = np.hstack((comb_array, new_column))
    print(comb_array.shape)

    for i in range (comb_array.shape[0]):
        l1 = comb_array[i][0]
        l2 = comb_array[i][1]
        all_mean_std = []
        for j in range (all_test_data.shape[0]):
            mean, std = calculate_feature_mean_std([l1,l2], all_test_data[j]) # 0,1 is feature index and after i can be picture index e.g.[i,0:3]
            all_mean_std.append([mean, std])
        all_mean_std_np = np.array(all_mean_std)
        comb_array[i][2] = caclulate_overlap_percentage(all_mean_std_np)
        # (all people's var sum)/(all people's mean var) part
        var_sum = np.sum(all_mean_std_np[:,1])
        mean_var = np.std(all_mean_std_np[:,0])
        if mean_var == 0:
            comb_array[i][3] = 0
        else:
            comb_array[i][3] = var_sum/mean_var     
    
    # #sort by overlap_percentage
    comb_array = comb_array[np.argsort(comb_array[:, 2])]
    ## show overlap_percentage and draw line
    print('overlapped %< 0.8 : ' ,comb_array[comb_array[:,2] < 0.8].shape[0])
    print('overlapped %< 0.85 : ' ,comb_array[comb_array[:,2] < 0.85].shape[0])
    print('overlapped %< 0.9  :' ,comb_array[comb_array[:,2] < 0.9].shape[0])
    print(' ')
    print(comb_array[0:8])
    show_line(all_gt_data[0][0],comb_array[0:8,0:2].astype(int),all_gt_name[0])
    show_line(all_gt_data[0][0],comb_array[0:10,0:2].astype(int),all_gt_name[0])
    show_line(all_gt_data[0][0],comb_array[0:15,0:2].astype(int),all_gt_name[0])
    show_line(all_gt_data[0][0],comb_array[0:20,0:2].astype(int),all_gt_name[0])


    #sort by  (all people's var sum)/(all people's mean var)
    comb_array = comb_array[np.argsort(comb_array[:, 3])]
    print('[landmark1, landmark2, overlap_percentage, var_sum/mean_var] ')
    print('1-5')
    print(comb_array[0:5])
    print('6-20')
    print(comb_array[5:20])

    '''
    Code under it is the feature analysis of all we tried .
    '''
    ### extract feature 2
    # comb_array_three =  output_all_kind_of_three_landmark(all_test_data.shape[2])
    # print(comb_array_three.shape)
    # new_column = np.zeros((52394, 1))    #combination
    # comb_array_three = np.hstack((comb_array_three, new_column))
    # comb_array_three = np.hstack((comb_array_three, new_column))    
    # print(comb_array_three.shape)
    # for i in range (comb_array_three.shape[0]):
    #     l1 = comb_array_three[i][0]
    #     l2 = comb_array_three[i][1]
    #     l3 = comb_array_three[i][2]
    #     all_mean_std_angle = []
    #     for j in range (all_test_data.shape[0]):
    #         mean_angle, std_angle = calculate_angle_feature_mean_std([l1,l2,l3], all_test_data[j]) # 0,1 is feature index and after i can be picture index e.g.[i,0:3]
    #         all_mean_std_angle.append([mean_angle, std_angle])

    #     all_mean_std_angle_np = np.array(all_mean_std_angle)
    #     comb_array_three[i][3] = caclulate_angle_overlap_percentage(all_mean_std_angle_np)
    #     # (all people's var sum)/(all people's mean var) part
    #     var_sum_angle = np.sum(all_mean_std_angle_np[:,1])
    #     mean_var_angle = np.std(all_mean_std_angle_np[:,0])
    #     if mean_var_angle == 0:
    #         comb_array_three[i][4] = 0
    #     else:
    #         comb_array_three[i][4] = var_sum_angle/mean_var_angle     
    # # sort by overlap_percentage
    # comb_array_three = comb_array_three[np.argsort(comb_array_three[:, 4])]
    # print('[landmark1, landmark2, landmark3, overlap_percentage, var_sum/mean_var] ')
    # print('1-5')
    # print(comb_array_three[:5])
    # print('6-20')
    # print(comb_array_three[5:20])



    ### extract feature 3 
    # print(comb_array[0])
    # all_mean_std = []
    # sample_l1 = comb_array[1,0]
    # sample_l2 = comb_array[1,1]
    # for j in range (all_test_data.shape[0]):
    #     mean, std = calculate_feature_mean_std([sample_l1,sample_l2], all_test_data[j]) # 0,1 is feature index and after i can be picture index e.g.[i,0:3]
    #     all_mean_std.append([ mean, std])
    # all_mean_std_np = np.array(all_mean_std)
    # print(all_mean_std_np)
    # draw_line_mean_std(all_mean_std_np)
    # show_line(all_gt_data[0][0],comb_array[0:2,0:2].astype(int),all_gt_name[0])
    # show_angle(all_gt_data[0][0],comb_array_three[0:2,0:3].astype(int),all_gt_name[0])
    #show_dis_angle(all_test_data)
    


    ### extract feature 4
    # postive = 0
    # negative = 0
    # print(all_test_data)
    # num_to_use = all_test_data.shape[0]
    # for i in range (num_to_use):
    #     for j in range (5):
    #         out = cmp(i, all_test_data[i][j], all_gt_data, all_gt_data.shape[0])
    #         if out :
    #             postive+=1
    #         else:
    #             negative+=1

    # print(postive/(postive+negative))
    # show_num = 1
    # for i in range (show_num):
    #     for j in range (1):
    #         show(all_gt_data[i][j],all_gt_name[i])

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Data reading')
    args = parser.parse_args()
    main(args)
