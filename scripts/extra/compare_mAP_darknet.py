#change only TEST_TO_COMPARE_PATH as you want! 

import os
import subprocess

# mAP from detecion result for this test set will be compared
TEST_TO_COMPARE_PATH = "/home/ubuntu/Work/darknet/data/cctv/test_set08.txt" 

TEST_SET_PATH = "/home/ubuntu/Work/darknet/data/cctv/test_mAP.txt"
subprocess.call("cp {} {}".format(TEST_TO_COMPARE_PATH, TEST_SET_PATH), shell=True)

DARKNET_DETECTION_RESULT_PATH = "/home/ubuntu/Work/darknet/result.txt"
DARKNET_MAP_RESULT_PATH = "/home/ubuntu/Work/darknet/map_result.txt"
DARKNET_PATH = "/home/ubuntu/darkent/darkent"
DARKNET_WEIGHT_PATH = "/home/ubuntu/Work/darknet/cctv_training/416_set01_set02_set03_set04_set05/cctv_last.weights"
SOURCE_GROUND_TRUTH_BASE = '/home/ubuntu/Work/mAP/input/cctv-all-ground-truth'
TARGET_GROUND_TRUTH_BASE = '/home/ubuntu/Work/mAP/input/ground-truth'


darknet_detector_command = "cd /home/ubuntu/Work/darknet/; ./darknet detector test data/cctv/cctv.data cfg/cctv.cfg {} -dont_show -ext_output -thresh 0.25 < {} > {}".format(DARKNET_WEIGHT_PATH, TEST_SET_PATH, DARKNET_DETECTION_RESULT_PATH)

darknet_mAP_command = "cd /home/ubuntu/Work/darknet/; ./darknet detector map data/cctv/cctv.data cfg/cctv.cfg {} -dont_show -ext_output > {}".format(DARKNET_WEIGHT_PATH, DARKNET_MAP_RESULT_PATH)

clean_mAP_input_folder_command = "rm /home/ubuntu/Work/mAP/input/ground-truth/*.txt; rm /home/ubuntu/Work/mAP/input/detection-results/*.txt"

convert_yolo_detection_result_command = "cp /home/ubuntu/Work/darknet/result.txt /home/ubuntu/Work/mAP/input/detection-results; python new_convert_dr_yolo.py; rm /home/ubuntu/Work/mAP/input/detection-results/result.txt"

calc_mAP_command = "cd /home/ubuntu/Work/mAP; rm /home/ubuntu/Work/mAP/output/output.txt; python main.py"


subprocess.call(darknet_detector_command, shell=True)
subprocess.call(darknet_mAP_command, shell=True) 

# copy ground truth files related with TEST_SET_PATH
subprocess.call(clean_mAP_input_folder_command, shell=True)
with open(TEST_SET_PATH) as test_set_f:
    for line in test_set_f:
        #print(line)
        image_name = line.split('/')[-1].split('.')[0]
        ground_truth_file_path = os.path.join(SOURCE_GROUND_TRUTH_BASE, image_name+'.txt')
        copy_command_str = "cp {} {}".format(ground_truth_file_path, TARGET_GROUND_TRUTH_BASE)
        print(copy_command_str)
        subprocess.call(copy_command_str, shell=True)

subprocess.call(convert_yolo_detection_result_command, shell=True)
subprocess.call(calc_mAP_command, shell=True)
