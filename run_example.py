#By AR

import obspy
import pyflex

obs_data=obspy.read('1995.122.05.32.16.0000.II.ABKT.00.LHZ.D.SAC')
synth_data=obspy.read('ABKT.II.LHZ.semd.sac')

obs_data.detrend("linear")
obs_data.taper(max_percentage=0.05, type="hann")
obs_data.filter("bandpass", freqmin=1.0 / 150.0, freqmax=1.0 / 50.0,
                corners=4, zerophase=True)

synth_data.detrend("linear")
synth_data.taper(max_percentage=0.05, type="hann")
synth_data.filter("bandpass", freqmin=1.0 / 150.0, freqmax=1.0 / 50.0,
                  corners=4, zerophase=True)

#--------------------------------------------------------------------
# Configure --> Parfile parameters in flexwin 
#--------------------------------------------------------------------
# FLEXWIN(and all the parameters). If you want furture
# and detailed documentions, please refer to the manual
# of FLEXWIN

# min and max period of seismograms
min_period= 90.0
max_period= 250.0

# STA/LAT water level
stalta_waterlevel= 0.085

# max tsfhit
tshift_acceptance_level= 45.0
tshift_reference= 0.0

# max amplitude difference
dlna_acceptance_level= 0.8
dlna_reference= 0.0

# min cc coef
cc_acceptance_level= 0.85

# window signal-to-noise ratio
s2n_limit= 5.0
s2n_limit_energy= 5.0
window_signal_to_noise_type= "amplitude"

# user module
#"user_module": "zcomp_90_250"

# min/max surface wave velocity, to calculate slowest/fast
# surface wave arrival to define the boundaries of
# surface wave region
#"selection_mode": "custom"
min_surface_wave_velocity= 4.80
max_surface_wave_velocity= 4.20
earth_model= "ak135"
max_time_before_first_arrival= 180.0
max_time_after_last_arrival= 10000.0

# check global data quality
check_global_data_quality= True
snr_integrate_base= 3.5
snr_max_base= 6.0

# see reference in FLEXWIN manual
c_0= 0.7
c_1= 6.0
c_2= 0.0
c_3a= 5.0
c_3b= 2.0
c_4a= 3.0
c_4b= 10.0


config = pyflex.Config(
    min_period=min_period, max_period=max_period,
    stalta_waterlevel=stalta_waterlevel, tshift_acceptance_level=tshift_acceptance_level,
    tshift_reference=tshift_reference, dlna_reference=dlna_reference, 
    dlna_acceptance_level=dlna_acceptance_level, cc_acceptance_level=cc_acceptance_level,
    s2n_limit=s2n_limit, window_signal_to_noise_type=window_signal_to_noise_type,
    min_surface_wave_velocity=min_surface_wave_velocity,
    earth_model=earth_model, max_time_before_first_arrival=max_time_before_first_arrival, 
    check_global_data_quality=check_global_data_quality, snr_integrate_base=snr_integrate_base,
    snr_max_base=snr_max_base, 
    c_0=c_0, c_1=c_1, c_2=c_2, c_3a=c_3a, c_3b=c_3b, c_4a=c_4a, c_4b=c_4b)

# Parameter example 
#config = pyflex.Config(
#    min_period=50.0, max_period=150.0,
#    stalta_waterlevel=0.08, tshift_acceptance_level=15.0,
#    dlna_acceptance_level=1.0, cc_acceptance_level=0.80,
#    c_0=0.7, c_1=4.0, c_2=0.0, c_3a=1.0, c_3b=2.0, c_4a=3.0, c_4b=10.0)


#--------------------------------------------------------------------
# Figure
#--------------------------------------------------------------------

windows = pyflex.select_windows(obs_data, synth_data, config, plot=True)

#--------------------------------------------------------------------
# Windows info
#--------------------------------------------------------------------

import pprint
pprint.pprint(windows[:3])
win = windows[4]
print("Indices: %s - %s" % (win.left, win.right))
print("Absolute times: %s - %s" % (win.absolute_starttime, win.absolute_endtime))
print("Relative times in seconds: %s - %s" % (win.relative_starttime,
                                              win.relative_endtime))
win.phase_arrivals
