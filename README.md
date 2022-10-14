# smartbagrec

日本語は[こちら]()

### Install
```sh
pip3 install https://github.com/amslabtech/smartbagrec/archive/master.zip
```

### About
GUI application for easy execution of rosbag record.  
It includes the ability to create profiles, reducing redundant operations.

<img src="https://user-images.githubusercontent.com/60866331/195900962-c077841a-c6d7-4bf3-81aa-8d8406f23333.png" width="800px">

## Usage

### Start the app
```sh
bagrec
```
To immediately display the dialog for loading a profile
```sh
bagrec -p
```
or `bagrec --profile`.

### Main Window

#### recording topics
Please select topics to record from here.

#### settings for recording
Some items require numerical values to be entered.  
If you click the advanced settings button, you will see an additional setting dialog.

#### select save mode
Select how to save the bagfile
- save to current dir
  - Save bagfile to the directory which `bagrec` was executed
  - File name is given by timestamp
- set prefix
  - Save bagfile to the directory which `bagrec` was executed
  - Add prefix to the timestamped file name
- set file path
  - Set save destination and file name manually
  
#### record
Starts recording bagfile with the current settings.  
A pop-up window will appear, and you must close it to quit recording.

#### save as profile
Records the current settings as a profile.  
The file name and extension are arbitrary.  
Normally, save it under `~/.config/smartbagrec`.

#### load from profile
Starts recording bagfile with the saved profile.
