# ListPackage
#### Command line utility to list packages used in a python project. Ignores packages from stdlib and user created modules

## Installation
Make sure Python (preferred 3.9) is installed.

1. Clone the repository

2. Install dependencies
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
For example to list packages used by ListPackage itself,
```shell
python ./main.py . > requirements.txt
cat requirements.txt
```
Output
```shell
stdlib-list==0.10.0
```

For help,
```shell
python ./main.py -h
```
