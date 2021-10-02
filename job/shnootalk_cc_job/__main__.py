from typing import List, Optional, Tuple

import subprocess
import os
import glob
import sys
import shutil
from pymongo import MongoClient
from bson.objectid import ObjectId


class Config:
    TIMEOUT = int(os.getenv('TIMEOUT', default='10'))
    CLANG_COMPILER = 'clang'
    SHNOOTALK_COMPILER = 'shtkc'
    MONGO_URL = os.getenv('MONGO_URL', default='mongodb://root:example@localhost:27017')
    MONGO_DATABASE = os.getenv('MONGO_DATABASE', default='shnootalk-cloud-compile')
    MONGO_COLLECTION = os.getenv('MONGO_COLLECTION', 'job-output')


class ExecutionStatus:
    SUCCESS = 'SUCCESS'
    EXEC_TIMEDOUT = 'EXEC_TIMEDOUT'
    CLANG_LINK_TIMEDOUT = 'CLANG_LINK_TIMEDOUT'
    CLANG_LINK_FAILED = 'CLANG_LINK_FAILED'
    COMPILE_FAILED = 'COMPILE_FAILED'
    COMPILE_TIMEDOUT = 'COMPILE_TIMEDOUT'
    COMPILE_STARTED = 'COMPILE_STARTED'


def run_subprocess(command: List[str]) -> Tuple[bool, Optional[str], Optional[int]]:
    try:
        subp = subprocess.run(command,
                              stdout=subprocess.PIPE, stderr=subprocess.PIPE,
                              timeout=Config.TIMEOUT, )

        console_output = subp.stdout.decode('utf-8')
        console_err_output = subp.stderr.decode('utf-8')

    except subprocess.TimeoutExpired:
        return True, None, None

    return False, console_output+console_err_output, subp.returncode


def run_program(file_name: str) -> Tuple[str, Optional[str]]:
    # Remove all object files before running the test
    os.system('rm -f *.o')
    os.system('rm -f ./test')

    # Run the compiler
    compile_command = [Config.SHNOOTALK_COMPILER, file_name, '-c']
    timedout, compiler_output, compiler_retcode = run_subprocess(compile_command)

    if timedout:
        return ExecutionStatus.COMPILE_TIMEDOUT, None

    # If there was a compilation error, return the error message from the compiler
    if compiler_retcode != 0:
        return ExecutionStatus.COMPILE_FAILED, compiler_output

    # Link object file into an executable
    object_files = glob.glob("*.o")
    link_command = [Config.CLANG_COMPILER] + object_files + ['-o', 'prog', '-lm']
    timedout, clang_output, clang_retcode = run_subprocess(link_command)

    if timedout:
        return ExecutionStatus.CLANG_LINK_TIMEDOUT, None

    # If there is a linking error, return error message from clang
    if clang_retcode != 0:
        return ExecutionStatus.CLANG_LINK_FAILED, clang_output

    # Run the executable and return the output from the executable
    timedout, exec_output, _ = run_subprocess(['./prog'])

    if timedout:
        return ExecutionStatus.EXEC_TIMEDOUT, None

    # If the program/executable did not timeout, return program output
    return ExecutionStatus.SUCCESS, exec_output


def list_files_only(dir_path: str) -> List[str]:
    return [f for f in os.listdir(dir_path) if os.path.isfile(os.path.join(dir_path, f))]


def main(configmap_dir: str, empty_dir: str, mongo_id: ObjectId) -> None:
    # Connect to mongoDB
    cluster = MongoClient(Config.MONGO_URL)
    collection = cluster[Config.MONGO_DATABASE][Config.MONGO_COLLECTION]
    collection.update_one({'_id': mongo_id}, {'$set': {'status': ExecutionStatus.COMPILE_STARTED}})

    # Delete mongo url env var to prevent compiled code from sniffing it
    os.environ['MONGO_URL'] = 'Haha, nice try :)'

    # Copy files from config map to scratch volume
    for file in list_files_only(configmap_dir):
        shutil.copy(os.path.join(configmap_dir, file), os.path.join(empty_dir, file))

    os.chdir(empty_dir)

    # Run the program and get output
    status, output = run_program('main.shtk')

    # Dump output to mongoDB
    collection.update_one({'_id': mongo_id}, {'$set': {'status': status, 'output': output}})


if __name__ == '__main__':
    main(sys.argv[1], sys.argv[2], ObjectId(sys.argv[3]))
