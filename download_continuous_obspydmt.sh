#!/bin/bash
obspyDMT --reset --continuous --datapath /home/lili/data/one_day --min_date 2004-01-01 --max_date 2004-01-04 --net "IU" --sta "HRV,ANMO" --loc '*' --cha "LHZ" --data_source IRIS --req_parallel --req_np 4 --parallel_process --process_np 4 --instrument_correction 
