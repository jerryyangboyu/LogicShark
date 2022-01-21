## Project Framework Versioning
- Python      - 3.8.9 (compatible from python 3.6-3.10)
- pyside6     - 6.2.2
- pyInstaller - 4.8

## Installation
1. Create local virtual environment
If you have different version of python on your computer, you might specify python3
```shell
python -m venv env
```
If you are a macOS/Linux user
```shell
source env/bin/activate
```
If you are a windows user
```shell
env\Scripts\activate.bat
```
2. Install PySlide6 Framework
> You **MUST** successfully finish the previous step in order to work on this part.
In the same terminal under virtual environment, install 6.2.2 version of PySlide framework
```shell
pip install pyside6==6.2.2
```
The package might takes around 1G on your hard disk.
4. (Optional) Install PyInstaller for packaging
```shell
pip install pyinstaller==4.8
```
You might have the following packages in virtual environment by ```pip list```
```text
Package                   Version
------------------------- -------
altgraph                  0.17.2
macholib                  1.15.2
pip                       21.1.2
pyinstaller               4.8
pyinstaller-hooks-contrib 2021.5
PySide6                   6.2.2
setuptools                57.0.0
shiboken6                 6.2.2
wheel                     0.36.2
```

## Source Code Structure
```text
- src
    - main.py // the main entry
- dist // the folder for output software release
- build // temp folder for building software
```

## Packaging and Deployment
> You **MUST** install PyInstaller and PySlide6 in the same virtual environment in order to successfully run following command

Quickly produce one-file executable program (Pass test under macOS platform)
```shell
pyinstaller src/appDemo.py --onefile --windowed
```
