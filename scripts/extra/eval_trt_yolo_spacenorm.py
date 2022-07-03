import os
import subprocess
import glob

TRT_YOLO_SPACENORM_PATH = "/home/cym/Work/spacenorm_tensorrt"
mAP_EVAL_PATH = "/home/cym/Work/mAP"
mAP_SCRIPT_PATH = "/home/cym/Work/mAP/scripts/extra"
mAP_INPUT_IMAGE_PATH = "/home/cym/Work/mAP/input/images"
SOURCE_GROUND_TRUTH_BASE = '/home/cym/Work/mAP/input/cctv-all-ground-truth'
TARGET_GROUND_TRUTH_BASE = '/home/cym/Work/mAP/input/ground-truth'
DARKNET_CCTV_DATASET_BASE = "/home/cym/Work/darknet/data/cctv"


SETS = []
for i in range(1,83):
    if i<10:
        SETS.append(f"set0{i}") 
    else:
        SETS.append(f"set{i}")

#print(SETS)

# 0. Remove results from previous evaluation
print("rm /home/cym/Work/mAP/output_mAP/*.txt")
subprocess.call("rm /home/cym/Work/mAP/output_mAP/*.txt", shell=True)
print("rm /home/cym/Work/mAP/output_images/*.jpg")
subprocess.call("rm /home/cym/Work/mAP/output_images/*.jpg", shell=True)

for set in SETS:
    if not os.path.isdir(f"{DARKNET_CCTV_DATASET_BASE}/{set}"):
        print(f"{DARKNET_CCTV_DATASET_BASE}/{set} does not exist.. -> go to next set\n")
        continue

    # 1. Remove files and folders from previous set
    gt_files = glob.glob("/home/cym/Work/mAP/input/ground-truth/*.txt")
    if (len(gt_files) > 0):
        print("rm /home/cym/Work/mAP/input/ground-truth/*.txt")
        subprocess.call("rm /home/cym/Work/mAP/input/ground-truth/*.txt", shell=True)

    detection_files = glob.glob("/home/cym/Work/mAP/input/detection-results/*.txt")
    if (len(detection_files) > 0):
        print("mv /home/cym/Work/mAP/input/detection-results/*.txt /home/Work/cym/mAP/input/detection-results-backup")
        subprocess.call("mv /home/cym/Work/mAP/input/detection-results/*.txt /home/cym/Work/mAP/input/detection-results-backup", shell=True)

    input_image_files = glob.glob(f"{mAP_INPUT_IMAGE_PATH}/*.jpg")
    if (len(input_image_files) > 0):
        print(f"rm {mAP_INPUT_IMAGE_PATH}/*.jpg")
        subprocess.call(f"rm {mAP_INPUT_IMAGE_PATH}/*.jpg", shell=True)

    if os.path.isdir(f"{TARGET_GROUND_TRUTH_BASE}/backup"):
        print(f"rm -rf {TARGET_GROUND_TRUTH_BASE}/backup")
        subprocess.call(f"rm -rf {TARGET_GROUND_TRUTH_BASE}/backup", shell=True)

    # 2. Copy gt files of current set (YOLO format)
    print(f"cp {DARKNET_CCTV_DATASET_BASE}/{set}/*.txt {TARGET_GROUND_TRUTH_BASE}")
    subprocess.call(f"cp {DARKNET_CCTV_DATASET_BASE}/{set}/*.txt {TARGET_GROUND_TRUTH_BASE}", shell=True)

    # 3. Copy images in current set for converting format of gt and visualizing mAP evaluation result
    print(f"cp {DARKNET_CCTV_DATASET_BASE}/{set}/*.jpg {mAP_INPUT_IMAGE_PATH}")
    subprocess.call(f"cp {DARKNET_CCTV_DATASET_BASE}/{set}/*.jpg {mAP_INPUT_IMAGE_PATH}", shell=True)

    # 4. Convert gt files of current set in YOLO format to VOC format
    os.chdir(mAP_SCRIPT_PATH)
    print("Converting gt files from YOLO to VOC format..")
    subprocess.call("python convert_gt_yolo.py", shell=True)

    # 5. Copy required gt & image files for current set
    TEST_SET_FILE = f"/home/cym/Work/darknet/data/cctv/seq_test_{set}.txt"
    print(f"Copy gt files for /home/cym/Work/darknet/data/cctv/seq_test_{set}.txt")
    with open(TEST_SET_FILE) as test_set_f:
        for line in test_set_f:
            #print(line)
            image_name = line.split('/')[-1].split('.')[0]
            ground_truth_file_path = os.path.join(SOURCE_GROUND_TRUTH_BASE, image_name+'.txt')
            copy_command_str = "cp {} {}".format(ground_truth_file_path, TARGET_GROUND_TRUTH_BASE)
            #print(copy_command_str)
            subprocess.call(copy_command_str, shell=True)

    # 6. Remove first gt file (since trt_yolo_spacenorm.py doesn't produce detection result for the first frame) 
    gt_files = sorted(glob.glob("/home/cym/Work/mAP/input/ground-truth/*.txt"))
    #print("gt_files = ", gt_files)
    subprocess.call(f"rm {gt_files[0]}", shell=True)

    # 7. Perform detection for current set (detection result will be created at /home/Work/mAP/input/detection-results/)
    os.chdir(TRT_YOLO_SPACENORM_PATH)
    print("Change to ", os.getcwd())
    print("Detection starts..")
    subprocess.call(f"python trt_yolo_spacenorm.py -c 1 -m yolov4-cctv-576 -n --image_list /home/cym/Work/darknet/data/cctv/seq_test_{set}.txt -b --log test.log", shell=True) 


    # 8. Evaluation mAP and confusion matrix for current set
    os.chdir(mAP_EVAL_PATH)
    print("Change to ", os.getcwd())
    print("mAP evaluation starts..")
    #subprocess.call("python main.py -na", shell=True) 
    #subprocess.call("python main.py", shell=True) 
    subprocess.call("python main.py -np", shell=True) # without -np, sometimes output result is not produced completely..
    subprocess.call(f"mv /home/cym/Work/mAP/output/output.txt /home/cym/Work/mAP/output_mAP/output_{set}.txt", shell=True)
    print(f"mAP evaluation result is moved into /home/cym/Work/mAP/output_mAP/output_{set}.txt")
    subprocess.call(f"mv /home/cym/Work/mAP/output/images/*.jpg /home/cym/Work/mAP/output_images", shell=True)
    print(f"mAP evaluation result image files are moved into /home/cym/Work/mAP/output_images/")

    print(f"================= DONE for {set} =================\n")


