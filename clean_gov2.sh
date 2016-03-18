#!/bin/bash -i
module load python27
module load python27-extras # get additional packages
module load gcc-4.9.2

./clean_gov2.py $* 
