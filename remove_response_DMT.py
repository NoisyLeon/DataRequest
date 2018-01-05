import bodywaveDMT

dbase   = bodywaveDMT.DMTASDF('cat_inv_Alaska_2017_aug.h5')
dbase.read_quakeml('alaska_2017_aug.ml')

dbase.remove_resp_catalog_mp('/scratch/summit/life9360/ALASKA_work/p_wave_19910101_20170831', nprocess=24, subsize=300)