# ListPackage
#### Command line utility to list packages used in a project. Ignores packages from stdlib and user created modules

## Installation
Make sure Python (preferred 3.9) is installed.

Clone the repository 
```shell
cd ListPackage
pip install -r ./requirements.txt
```

## Usage
```shell
python ./main.py ./path/to/project
```
To list all the packages in requirements.txt
```shell
python ./main.py ./path/to/project > requirements.txt
```

For help,
```shell
python ./main.py -h
```