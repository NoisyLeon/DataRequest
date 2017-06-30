#!/bin/bash
obspyDMT --reset --continuous --datapath /work3/leon/bensen_example --min_date 2004-01-01 --max_date 2008-01-01 --net "IU" --sta "HRV,ANMO" --loc '*' --cha "LHZ" --data_source IRIS --req_parallel --req_np 16 --parallel_process --process_np 16 --instrument_correction --bulk
