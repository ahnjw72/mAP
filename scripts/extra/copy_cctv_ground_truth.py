import os
import subprocess

# change this file name as you want
TEST_SET_FILE = '/home/cym/Work/darknet/data/cctv/seq_test_set01.txt'

SOURCE_GROUND_TRUTH_BASE = '/home/cym/Work/mAP/input/cctv-all-ground-truth'
TARGET_GROUND_TRUTH_BASE = '/home/cym/Work/mAP/input/ground-truth'

#clear_gt_command_str = f"rm {TARGET_GROUND_TRUTH_BASE}/*.txt"
#print(clear_gt_command_str)
#subprocess.call(copy_command_str, shell=True)

with open(TEST_SET_FILE) as test_set_f:
    for line in test_set_f:
        #print(line)
        image_name = line.split('/')[-1].split('.')[0]
        ground_truth_file_path = os.path.join(SOURCE_GROUND_TRUTH_BASE, image_name+'.txt')
        copy_command_str = "cp {} {}".format(ground_truth_file_path, TARGET_GROUND_TRUTH_BASE)
        print(copy_command_str)
        subprocess.call(copy_command_str, shell=True)

