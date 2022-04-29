#! /bin/bash

scripts=`dirname "$0"`
base=$(realpath $scripts/..)

infographic=$base/infographic

mkdir -p $infographic/charts
mkdir -p $infographic/tables


python scripts/get_infographic.py --input-file $infographic/output.txt \
                        --save-charts $infographic/charts \
                        --save-tables $infographic/tables 

                    
