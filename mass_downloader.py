import obspy
from obspy.clients.fdsn.mass_downloader import RectangularDomain, \
    Restrictions, MassDownloader

# Rectangular domain containing parts of southern Germany.
domain = RectangularDomain(minlatitude=52., maxlatitude=72.5, minlongitude=-172., maxlongitude=-122.)

restrictions = Restrictions(
    # Get data for a whole year.
    starttime=obspy.UTCDateTime(2017, 6, 11),
    endtime=obspy.UTCDateTime(2017, 6, 21),
    # Chunk it to have one file per day.
    chunklength_in_sec=86400,
    # Considering the enormous amount of data associated with continuous
    # requests, you might want to limit the data based on SEED identifiers.
    # If the location code is specified, the location priority list is not
    # used; the same is true for the channel argument and priority list.
    network="TA", station="H20K", location="", channel="LH?",
    # The typical use case for such a data set are noise correlations where
    # gaps are dealt with at a later stage.
    reject_channels_with_gaps=False,
    # Same is true with the minimum length. All data might be useful.
    minimum_length=0.0,
    # Guard against the same station having different names.
    minimum_interstation_distance_in_m=100.0)

mseed_storage = ("waveforms/{network}/{station}/"
                 "{channel}.{location}.{starttime}.{endtime}.mseed")
stationxml_storage = "stations/{network}/{station}.xml"
# Restrict the number of providers if you know which serve the desired
# data. If in doubt just don't specify - then all providers will be
# queried.
mdl = MassDownloader(providers=["IRIS"])
mdl.download(domain, restrictions, mseed_storage=mseed_storage,
             stationxml_storage=stationxml_storage, threads_per_client=3)
