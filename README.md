# Video Surveillance for Road Traffic Monitoring (MCV-M6-Video-Analysis)

# Team 1

| Members | Contact |
| :---         |   :---    | 
| Aditya Rana   | adityasangramsingh.rana@e-campus.uab.cat | 
| German Barquero    | german.barquero@e-campus.uab.cat  |
| Carmen García    | carmen.garciano@e-campus.uab.cat  |
| Juan Chaves | juanvictor.chaves@e-campus.uab.cat |

Link to Final Project presentation: [Google Slides](https://docs.google.com/presentation/d/1FcZ90pkM3YXFWxmWFEbWw7z9L7LiFYNIy9Z9eVy9m_s/edit?usp=sharing)

# Index of contents
The contents of this repository are structured following a temporal line throughout the 5 weekly tasks we have been working on.

### [Week 1](#week1)  - [Introduction to the project](https://docs.google.com/presentation/d/1kNpgATzLse7ZOE_rHp5N3c7yqyxgLaUbcgDiwzJ4isI/edit?usp=sharing)
### [Week 2](#week2)  - [Background estimation](https://docs.google.com/presentation/d/1aV761QHabmQQitoXGatwK7zc4g2Yebu1JaH6rmS8xrg/edit?usp=sharing)
### [Week 3](#week3)  - [Detection and Tracking](https://docs.google.com/presentation/d/10_nkRL2EFLIEEQEloHUi6XBRzcer_N9eBgKG--AvKks/edit#slide=id.p)
### [Week 4](#week4)  - [Optical flow, Video Stabilization and Tracking](https://docs.google.com/presentation/d/1hCgceBehTA5_3Vs2I9-sR5rmQzM5iTKulkw-dRkpIDQ/edit?usp=sharing)
### [Week 5](#week5)  - [Multi-target multi-camera Tracking](https://docs.google.com/presentation/d/1FcZ90pkM3YXFWxmWFEbWw7z9L7LiFYNIy9Z9eVy9m_s/edit?usp=sharing)

# <a name="week1"></a> Week1

## Tasks 1 and 2
Tasks 1.1, 1.2 and 2 are implemented between the files `main.py` and `utils.py`. 

Detection file, noise configuration and visualization options are chosen by cmd command. Despite that, some important "global" variables are:

`VIDEO_PATH` = *path to vdo.avi*
`ANNOTATIONS_FILE` = *path to annotations.xml with complete ground truth data (including still objects, bikes and cars)*

This file can be parsed with the function utils.parse_xml_rects

`DET_PATH` = *path to AICity detection data*

This file can be parsed with the function utils.parse_aicity_rects. Path to rcnn, yolo and ssd detections already on the script. Select using the option: mode.

````
$ python main.py -h
usage: main.py [-h] -m MODE -n NAME [-d] [-s] [--noise NOISE]

optional arguments:
  -h, --help            show this help message and exit
  -m MODE, --mode MODE  yolo, rcnn or ssd
  -n NAME, --name NAME  Storage older name
  -d, --display         Whether to display the video or not
  -s, --save            Wheter to save frames and graphics for each of them or not
  --noise NOISE         Noise addition configuration. Format drop-pos-size-ar
````

## Tasks 3 and 4
The tasks are implemented in jupyter notebooks with their corresponding name.


# <a name="week2"/> Week 2

## Runner
All tasks were implemented in `main.py`. The algorithm will either pre-compute the background modelling or load it if it has already been computed before and saved in the `checkpoints` folder. The algorithm will output a .mp4 video file with the result and a gif of the first 200 frame for visualization purposes. The different algorithms can be selected by playing with the scripts parameters:

## Sript Usage

The models available include
- GaussianModel -> 'gm'
- AdaptiveGM -> 'agm'
- SOTA -> 'sota', and select which one to use with "--method" argument to the parser

````
$ python week2/main.py -h
usage: main.py [-h] [-m {gm,agm,sota}] [-c {gray,rgb,hsv,lab,ycrcb}] [-M MAX] [-perc PERCENTAGE] 
               [-a N [N ...]] [-p P] [-d] [-meth {mog,mog2,lsbp,gmg,cnt,gsoc,knn}]

Extract foreground from video.

optional arguments:
  -h, --help            show this help message and exit
  -m {gm,agm,sota}, --model {gm,agm,sota}
                        The model used for background modeling. Default value is 'gm':Gaussian.
  -c {gray,rgb,hsv,lab,ycrcb}, --colorspace {gray,rgb,hsv,lab,ycrcb}
                        choose the colorspace used for background modeling. 
                        Default value is 'gray.
  -M MAX, --max MAX     max number of frames for which to extract foreground. 
                        Set to '-1' by default, which means take all the frames available.
  -perc PERCENTAGE, --percentage PERCENTAGE
                        percentage of video to use for background modeling
  -a N [N ...], --alpha N [N ...]
                        alpha value or values depending on color space used for modelling
  -p P, --p P           Rho (p): [AdaptiveGaussianModel] parameter controlling the inclusion 
                        of new information to model
  -d, --display         to display frames as they are processed
  -meth {mog,mog2,lsbp,gmg,cnt,gsoc,knn}, --method {mog,mog2,lsbp,gmg,cnt,gsoc,knn}
                        SOTA algorithm used for background subtraction. 
                        The '--model' parameter has to be set to 'sota' to be able to use this.
````

## Random/Grid search
There is a folder specific for this with the hyperparameters search runner and the visualizer of the results (3D plot). We did not have time to implement an usable interface for this script and the parameters to try are hardcoded inside the script, as well as the main function, which was copied from the main runner.

# <a name="week3"/> <a name="w3"></a> Week 3

## Requirements
Apart from the packages on requirements.txt. you must follow the instructions on [this link](https://github.com/LucaCappelletti94/pygifsicle) for installing pygifsicle (used for reducing gif size).

tldr:

- on Linux (well, Ubuntu) run 
    ```
    sudo apt-get install gifsicle
    ```
- On windows you must look for an installer [here](https://eternallybored.org/misc/gifsicle/)
- On Mac no further action (apart from pip install) is required, so you just relax and see your investment on Apple payoff.

If you want to use the state-of-the-art trackers implemented as part of the task 2.2, you need to run

    ```
    git submodule update --init --recursive
    ```
    
And follow the [installation instructions](https://github.com/STVIR/pysot/blob/master/INSTALL.md) from the PySot submodule.

## Data format
This week we have embraced MOTS Challenge format as our *official*  file format. All object labelling and detection is stored on a txt with **a line per detection** with the following format: 

```
'frame', 'id', 'bb_left', 'bb_top', 'bb_width', 'bb_height', 'conf', 'x', 'y', 'z'
```

Unknown data is represented with a -1. Example:

```
1,-1,882.263,92.697,55.811,47.536,0.906,-1,-1,-1
```

## Visualizer
We have created a script for showing the video with our results, be it detection or tracking. The input to it always is a txt file with the described format.

1. Add the path to your detection file to the list *detections* on *visualizer.py* with the following format:

```python
    detections = [
        {
            'name': 'gt',
            'full-name': 'Ground truth',
            'color': (0, 255, 0),
            'rects': utils.parse_xml_rects(GT_RECTS_PATH),
            'tracking': False
        },
        {
            'name': 'R101+IoU',
            'full-name': 'Retina Net R1o1 FPN 3x rp 128 + IoU tracking',
            'color': utils.get_random_col(),
            'rects': utils.parse_aicity_rects('./detections/retina101_track.txt', zero_index=0),
            'tracking': True
        },
        # ...
    ]
```
We already provide the base and tracked detections we used inside *week3/detections/* and *week3/trackings_iou/* respectively

> We assume the first detection on the list corresponds to ground truth data.

- name: Name displayed on the bounding box on the visualizer
- full-name: Name displayed on the visualizer legend and on the output AP file
- color: color of the bounding box on (R, G, B). We use a helper funciton for generating a random color, but you can specify it yourself. 
- rects: The actual detection read with our parser functions (available for full annotations xml and mots challeng txt format)
- tracking: whether we want the visualizer to choose the color of the boxes based on tracking information

> This last parameter overwrites the selected color

Make sure, also, that your detection's 'name' is on the list USE_DET

```python
# This list is intented to make filtering visualizations easier
USE_DET = ['gt', 'aigt', 'yolo', 'ssd', 'retina50', 'retina101', 'rcnn', 'R101+IoU']
```

2. Launch the script visualizer.py. It is convenient if you do so from inside week3.

3. The video will play, painting provided detections. The following keyboard commands are available:

- q: Quits the program
- p: Changes visualization speed between 0, 15, 30 and 100 FPS
- s: Saves an snapshot to your current directory with the name save_{frame_number}.jpg
- g: Toggles **gif recording**. Once you press g, the recording starts, until you press g again. You have to press g before the video ends, otherwise the gif won't ne generated. You can create multiple gifs, just be patient after you press q or the video ends while they are generated. Gifs are saved to *out_visualizer/{run}/gifs/*.

> You can check if you are recording or not (together with FPS information) on the bottom right corner of the video

> A new folder is generated inside *out_visualizer* on each execution of the program.

## Off the shelf models

For obtaining detections apart from the provided ones for Yolo, SSD and Mask RCNN, we have used **detectron2**. The script *week3/m6-inference.py* generates txt outputs for the specified models and configurations. Two list of variables are currently being iterated over:

- models: which holds the name of .yaml files from Detectron's [model zoo](https://github.com/facebookresearch/detectron2/blob/master/MODEL_ZOO.md)
- batch: a list of integers with the number of region proposals used by the model (currently hardcoded).

A txt file named 'm6-aicity_{model}_rp{batch}.txt' is generated.

## Fine-Tuning Your Models
The training scripts for the Faster-RCNN and Retinet are available in `train_faster_RCNN.py` and `train_retinaNet.py` respectively. Only the path to the dataset need to be provided to run a training session.

Training with video files is not starightforward in Detectron2 so all the frames of the video had to be split and stored as individual jpg files. This can be done using the file `split_video.py`. 

## Tracking
### 2.1 . IOU Tracking

IOU tracking is performed using the script *iou_tracker.py*. 

- Input is a txt file following the described format representing a detection. 
- An output following the same format, but now holding id information is generated by the script. 

Both input and output paths must be specified inside *iou_tracker.py*'s main.

### 2.2. Kalman tracking + state-of-the-art trackers
All trackers were implemented under the same architecture so they can be easily run and tested using the file:
````
$ python w3_run_kalman.py -h
usage    w3_run_kalman.py [-h] [-o OUTPUT] [-d DETECTIONS] [-t TRACKER]
                        [-th THRESHOLD] [-tl TRACKER_LIFE] [-M MAX]

optional arguments:optional arguments:
  -h, --help            show this help message and exit
  -o OUTPUT, --output OUTPUT
                        where results will be saved
  -d DETECTIONS, --detections DETECTIONS
                        detections used for tracking. Options: {retinanetpre, retinanet101pre, maskrcnnpre, ssdpre, yolopre}
  -t TRACKER, --tracker TRACKER
                        tracker used. Options: {"kalman", "kcf", "siamrpn_mobile", "siammask"}
  -th THRESHOLD, --threshold THRESHOLD
                        threshold used to filter detections
  -tl TRACKER_LIFE, --tracker_life TRACKER_LIFE
                        tracker life
  -M MAX, --max MAX     max number of frames to run the tracker (by default it runs all video).
                        Set to '-1' by default.

````

The txt file with the results will be stored for posterior evaluation. A video with the tracking visual results will also be generated.


### 2.3. IDF1 computation
IDF is computed using the pymotmetrics-based script *weeek3/test_metric.py* as follows:

```
python3 test_metric.py <GT_FOLDER> <DET_FOLDER>
```
GT_FOLDER and DET_FOLDER hold txt files with ground truth and detection data respectively. They must have the following structure:

```
Layout for ground truth data
    <GT_FOLDER>/<SEQUENCE_1>/gt/gt.txt
    <GT_FOLDER>/<SEQUENCE_2>/gt/gt.txt
    ...

Layout for test data
    <DET_FOLDER>/<SEQUENCE_1>.txt
    <DET_FOLDER>/<SEQUENCE_2>.txt
    ...
```
Ground truth and detection is matched according to SEQUENCE_X. Results are displayed on the console.



# <a name="week4"/> Week 4

### 1.1 Compute optical flow

The implementation and sample usage of block matching optical flow can is provided in the file `block_match.py`. It includes
   - exhaustive search
   - three step search

The code for generating the visualizations in the slides is provided in `visualize_block_matching.py`

### 1.2. Off-the-shelf Optical Flow

The followin algorithm have been tested:
   -PyFlow 
   -Lucas-Kanade
   -Farneback
   -SimpleFlow
   
 The scripts to perform optical flow are in week4/opticalflow/pyflow. If you run any of them, you get running time, MSE, PEPN on the terminal and the optical flow representation is displayed. 
 

### 2.1. Video Stabilization with Block Matching
The algorithm for video stabilization is based on a simple traslational model. To stabilize a video, call week4/stabilization.py with the following arguments:
```
usage: stabilization.py [-h] -v VIDEO [-t {median,gaussian}] [-s KERNEL_SIZE] [-d] [-a] [-m MEMORY]

optional arguments:
  -h, --help            show this help message and exit
  -v VIDEO, --video VIDEO
                        Name of the video to stabilize. Must be an avi store in ../..
  -t {median,gaussian}, --kernel-type {median,gaussian}
                        Type of smoothing filter
  -s KERNEL_SIZE, --kernel-size KERNEL_SIZE
                        Size of the smoothing kernel
  -d, --display         Wheter to display frames s they are being processed or not
  -a, --angle           Wheter to try to compensate angles (not recommended)
  -m MEMORY, --memory MEMORY
                        Size of the accumulated memory
```
An output video will be generated on output/ with the following naming convention:
```python
outname = f'output/out{videoname}_mem{memory}_typ{kernel_type}_ker{kernel_size}_angle_{use_angle}.avi'
```

### 2.2. Off-the-shelf Video Stabilization

 The following algorithms have been tested:
   -VidStab (script in week4/vidstab/vidstab_script.py): input and output video path are hardcoded. This script also plots trajectory and transform graphs.
   ```
$ python vidstab_script.py
   
   ```
   -Video Stabilization Using Point Feature Matching in OpenCV (script in week4/vidstab/VideoStabilization/video_stabilization.py): input and output video path are hardcoded.
   
 ```
$ python video_stabilization.py
 ```
   
 We also attempted:
   - [Futsa](https://alex04072000.github.io/FuSta/)
   - [Real-Time-Video-Stabilization](https://github.com/Lakshya-Kejriwal/Real-Time-Video-Stabilization)
  
 But ultimately, we did not manage to make them work correctly.


### 3.1. Tracking with optical flow
The extension of the IOU tracker with optical flow has been implemented in the same architecture built for Week 3 tracking tasks. Therefore, trackers can be executed with the same script, specifying TRACKER to "flow_LK_median", "flow_LK_mean", "flow_GF_median", "flow_GF_mean" or "medianflow".
````
$ python w3_run_kalman.py -h
usage    w3_run_kalman.py [-h] [-o OUTPUT] [-d DETECTIONS] [-t TRACKER]
                        [-th THRESHOLD] [-tl TRACKER_LIFE] [-M MAX]

optional arguments:optional arguments:
  -h, --help            show this help message and exit
  -o OUTPUT, --output OUTPUT
                        where results will be saved
  -d DETECTIONS, --detections DETECTIONS
                        detections used for tracking. Options: {retinanetpre, retinanet101pre, maskrcnnpre, ssdpre, yolopre}
  -t TRACKER, --tracker TRACKER
                        tracker used. Options: {"kalman", "kcf", "siamrpn_mobile", "siammask", "flow_LK_median", "flow_LK_mean", "flow_GF_median", "flow_GF_mean", "medianflow"}
  -th THRESHOLD, --threshold THRESHOLD
                        threshold used to filter detections
  -tl TRACKER_LIFE, --tracker_life TRACKER_LIFE
                        tracker life
  -m MIN, --min MIN     number of frame to start the tracker (by default it runs from the beginning of the video).
                        Set to '-1' by default.
  -M MAX, --max MAX     number of frames to finish the tracking (by default it runs until the end of the video).
                        Set to '-1' by default.

````

The txt file with the results will be stored for posterior evaluation. A video with the tracking visual results will also be generated.

# <a name="week5"/> Week 5

The implementation of this week have been split into two well divided parts:

## 1. Multi-target single-camera (MTSC) tracking

The interface of the script used in previous weeks was adapted to this week's. Now, the usage is:

````
$ python w5_run_mtsc.py -h
usage    w5_run_mtsc.py [-h] [-s SEQUENCE] [-c CAMERA] [-d DETECTIONS]
                      [-o OUTPUT] [-t TRACKER] [-th THRESHOLD]
                      [-tl TRACKER_LIFE] [-v] [-M MAX] [-m MIN]

optional arguments:
  -h, --help            show this help message and exit
  -s SEQUENCE, --sequence SEQUENCE
                        sequence to be run
  -c CAMERA, --camera CAMERA
                        camera to be run
  -d DETECTIONS, --detections DETECTIONS
                        detections to use for the tracker
  -o OUTPUT, --output OUTPUT
                        where results will be saved
  -t TRACKER, --tracker TRACKER
                        tracker used. Options: {"kalman", "kcf", "siamrpn_mobile", "siammask", "medianflow"}
  -th THRESHOLD, --threshold THRESHOLD
                        threshold used to filter detections
  -tl TRACKER_LIFE, --tracker_life TRACKER_LIFE
                        tracker life in number of frames
  -v, --video           if true, it saves a video with the visual results instead of the annotations
  -M MAX, --max MAX     max number of frames to run the tracker (by default it
                        runs all video). Set to '-1' by default.
  -m MIN, --min MIN     min number of frames to run the tracker (by default it
                        runs all video). Set to '-1' by default.
````

The txt file with the results will be stored for posterior evaluation. A video with the tracking visual results will also be generated if specified.
This week, we also implemented several post-processing functions to filter the highest number of detections which are not considered in the ground truth and make the comparison fairer. This can be applied to the folder which generates the previous script by running:

 ```
$ python w5_post_process_mtsc.py --input INPUT_FOLDER --output OUTPUT_FOLDER
 ```
 
 ## 2. Single-camera evaluation
 
 Now, the output folder can be evaluated using the script of single evaluation:

 ```
$ python w5_run_metrics_single.py -s SEQUENCE -c CAMERA -f INPUT_FOLDER
 ```
 
 Note: the DATA_PATH variable inside the 'utils.py' file should point to the challenge dataset.
 
 ## Multi-target multi-camera (MTMC) tracking
 
 This scripts allow us to obtain the multitracking files for the different sequences. The files are saved in mtrackings/S0X/C0Y/method.txt. 
 This is the folder format the metric script will need in order to evaluate the tracking.
 
  ```
$ python multitracker.py 
 ```
 
 Note: Before running the script it is necessary to change the DATA_PATH variable to point to the challenge dataset.
 Also it is needed to indicate de Sequence number, and the method for matching prefered. (On the top of the code, in the Config options part)

 
 ## Multi-camera evaluation
 
 Now, the output folder can be evaluated using a script very similar to the one used in single-camera evaluation:

 ```
$ python w5_run_metrics_multiple.py -s SEQUENCE -f INPUT_FOLDER
 ```
 
 Note: the DATA_PATH variable inside the 'utils.py' file should point to the challenge dataset.

