# smartbagrec

日本語は[こちら](https://github.com/amslabtech/smartbagrec#%E3%82%A4%E3%83%B3%E3%82%B9%E3%83%88%E3%83%BC%E3%83%AB)

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
Check the check boxes for the settings you wish to enable.
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

----

### インストール
```sh
pip3 install https://github.com/amslabtech/smartbagrec/archive/master.zip
```

### 概要
rosbag record を簡単に実行するためのGUIアプリケーションです。  
プロファイルを作成することもできるため、冗長な操作を減らすことができます。

<img src="https://user-images.githubusercontent.com/60866331/195900962-c077841a-c6d7-4bf3-81aa-8d8406f23333.png" width="800px">

## 使用方法

### アプリを起動する
```sh
bagrec
```
プロファイルを読み込むためのダイアログをすぐに表示させたい場合
```sh
bagrec -p
```
または `bagrec --profile`

### メインウィンドウ

#### 記録するトピック (recording topics)
ここから記録するトピックを選択してください。

#### 記録のための設定 (settings for recording)
有効にしたい設定項目にチェックを入れてください。  
一部の項目は数値の入力も必要です。  
詳細設定ボタンをクリックすると、追加の設定ダイアログが表示されます。


#### 保存モード選択
bagfileの保存方法を選択します。
- save to current dir
  - bagfileを `bagrec` を実行したディレクトリに保存します
  - ファイル名はタイムスタンプから付与されます
- set prefix
  - bagfileを `bagrec` を実行したディレクトリに保存します
  - タイムスタンプから自動で付与されるファイル名に任意のプレフィックスをつけます
- set file path
  - 保存先とファイル名を手動で設定します
  
#### 記録 (record)
現在の設定でbagfileの記録を開始します。  
ポップアップウィンドウが表示されます。  
記録を終えるにはこれを閉じてください。

#### プロファイルとして保存 (save as profile)
現在の設定をプロファイルとして記録します。  
ファイル名や拡張子は任意です。  
通常は`~/.config/smartbagrec`の下に保存します。

#### プロファイルを読み込む (load from profile)
保存したプロファイルでbagfileの記録を開始します。
