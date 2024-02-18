import os
import io
import re
import stdlib_list as stdlibs
import sys
import argparse

REGEX="(?:^[ \t]*import ([a-zA-Z0-9_]+))|(?:^[ \t]*from ([a-zA-Z0-9_]*) [a-zA-Z ]*)"
# Matches x in following cases:
# import x
# import x.y
# from x import y
# from x.a import y
# <tab or spaces>import x
# <tab or spaces>import x.y
# <tab or spaces>from x import y
# <tab or spaces>from x.a import y

# Scan a python file and return packages imported in it
def Scan(file: io.TextIOWrapper,version,exclude:list[str])->list[str]:
    packages=[]
    stdpackages=stdlibs.stdlib_list(version)
    for line in file.readlines():
        match=re.match(REGEX,line.strip('\n'))
        if match is None:
            continue
        # extract package name from capturing groups
        # .group(1) when syntax is import [match]
        # .gruop(2) when syntax is from [match] import ..
        package=match.group(1) or match.group(2)
        if package is None or package.lower() in stdpackages or package.lower() in exclude:
            continue
        packages.append(package)
    return packages



def ScanFiles(dir: str=os.getcwd(),exclude_dirs=[],version=str(sys.version_info.major)+"."+str(sys.version_info.minor)):
    """
    Scans files in dir and returns packages imported in those files
    args:
    dir: Working directory
    excluded_dirs: directories to exclude. Files present in these directories are skipped.
    version: python version to consider for filtering out stdlib packages

    """
    files=[]
    packages=[]
    excluded_packages=[]    # Excluded user created packages/ python files
    for dirpath, dirnames, filenames in os.walk(dir):
        exclude=False
        for exclude_dir in exclude_dirs:
            if exclude_dir in dirpath:
                exclude=True #Mark dir to be excluded
                break
        # Excluded dir was matched, skip
        if exclude:
            continue
        for filename in filenames:
            if not filename.endswith(".py"):
                continue
            files.append(os.path.join(dirpath,filename)) 
            # Dont consider user created python modules
            excluded_packages.append(filename.removesuffix(".py"))
    for file in files:
        with open(file,'r') as f:
            try:
                packages+=Scan(f,version=version,exclude=excluded_packages)
            except Exception as e:
                print(e) 
                pass
    return packages

if __name__ == "__main__":
    parser=argparse.ArgumentParser(description="Python tool to list non standard packages in a project")
    parser.add_argument("path")
    parser.add_argument("--version",type=str,help="Python version, e.g. 3.9. Used to filter out stdlib packages")
    parser.add_argument("--exclude",nargs="*")
    args=parser.parse_args()
    version=args.version
    exclude=args.exclude or ["venv","git"]
    path=args.path
    packages=ScanFiles(dir=path,exclude_dirs=exclude,version=version)
    for package in packages:
        print(package)
    