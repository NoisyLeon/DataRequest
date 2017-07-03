import database

dset=database.obspyDMTASDF('test.h5')

dset.get_station_data(datadir='/home/lili/data/one_day')

dset.prepare_continuous_data(datadir='/home/lili/data/one_day', outdir='/home/lili/working_dir/one_day')

# # dset.prepare_continuous_data_mp(datadir='/home/lili/data/bensen_example', subsize=100, outdir='/home/lili/working_dir/obspyDMT_test_mp_1', verbose=True)
# dset.prepare_continuous_data_mp(datadir='/home/lili/data/one_day', subsize=100, remove_response=False,
#         outdir='/home/lili/working_dir/one_day', verbose=True)