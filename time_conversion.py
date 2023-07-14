from astropy import time

########################################################################################################################
def option1():

    # 0h 1950 January 1st UT1, roughly:
    # Assuming 0h 1950 January 1st UT1 = UTC
    # Eyeballing difference between UT1 and TAI
    t_reference_tai_1950 = time.Time('1950-01-01T00:00:00', format='isot', scale='tai') + time.TimeDelta(-3.5, scale="tai", format="sec")

    observation_time_tai = t_reference_tai_1950 + time.TimeDelta(1812104598.000, scale="tai", format="sec")
    observation_time_utc = observation_time_tai.utc

    print("Observation UTC: ", observation_time_utc.to_value("isot")) # 2007-06-04T10:22:41.500

    # print( t_reference_ut1_1950.to_value("mjd", "long") )
    #
    # t_reference_tai_1950 = t_reference_ut1_1950.tai
    # # t_reference_tai_2000 = time.Time(['2000-01-01T00:00:00'], format='isot', scale='tai')
    #
    # observation_time_delta = time.TimeDelta("1812103240.000", scale="tai", format="sec")
    #
    # observation_time_wrt_1950 = t_reference_tai_1950 + observation_time_delta

########################################################################################################################
# Patzold (2005)
def option2():

    t_reference_1950 = time.Time('1950-01-01T00:00:00', format='isot', scale='tai')
    t_reference_j2000 = time.Time('2000-01-01T12:00:00', format='isot', scale='tai')
    t_reference_2003 = time.Time('2003-01-01T00:00:00', format='isot', scale='tai')
    print("MJD 2003 - 1950: ", t_reference_2003.to_value("mjd", "long") - t_reference_1950.to_value("mjd", "long"))

    leap_seconds = 22
    shift_1950_to_2003 = (t_reference_2003.to_value("jd") - t_reference_1950.to_value("jd")) * 86400 + leap_seconds
    shift_1950_to_j2000 = (t_reference_j2000.to_value("jd") - t_reference_1950.to_value("jd")) * 86400 + leap_seconds
    observation_time_from_2003 = time.TimeDelta(1812104598.000 - shift_1950_to_2003, format="sec")
    observation_time_from_j2000 = time.TimeDelta(1812104598.000 - shift_1950_to_j2000, format="sec")

    observation_time_utc_float_1 = t_reference_j2000.to_value("jd") + observation_time_from_j2000.to_value("jd")
    observation_time_utc_1 = time.Time(observation_time_utc_float_1, format="jd", scale="utc")

    observation_time_utc_float_2 = t_reference_2003.to_value("jd") + observation_time_from_2003.to_value("jd")
    observation_time_utc_2 = time.Time(observation_time_utc_float_2, format="jd", scale="utc")

    print("Observation UTC(1): ", observation_time_utc_1.to_value("isot")) # 2007-06-04T10:22:56.000
    print("Observation UTC(2): ", observation_time_utc_2.to_value("isot")) # 2007-06-04T10:22:56.000

    # observation_time_delta = time.TimeDelta("1812103240.000", scale="tai", format="sec")
    #
    # reference_shift_delta = t_reference_1950 - t_reference_2000
    # print("Delta 1950 2000 [s]: ", reference_shift_delta.to_value("sec", "long")[0])
    #
    #
    # reference_shift_delta_leap = reference_shift_delta + leap_seconds
    # print("Delta: ", reference_shift_delta_leap.to_value("sec", "long")[0])
    #
    # # observation_time_2000 = t_reference_1950 + observation_time_delta + reference_shift_delta
    #
    # observation_time = t_reference_1950 + observation_time_delta
    # observation_time_utc = observation_time.utc
    # print("Observation UTC: ", observation_time_utc.to_value("isot")[0])
    # print("Observation TAI: ", observation_time.to_value("isot")[0])
    # print("Observation TDB: ", observation_time_utc.tdb.to_value("isot")[0])
    # # print("Observation UTC: ", observation_time_utc.to_value("jd", "long")[0])
    # # print("Observation TDB: ", observation_time_utc.tdb.to_value("jd", "long")[0])

########################################################################################################################
# Currently implemented option
def option3():

    t_reference_1950 = time.Time('1950-01-01T00:00:00', format='isot', scale='tai')
    t_reference_j2000 = time.Time('2000-01-01T12:00:00', format='isot', scale='tai')

    shift_1950_to_2000 = (t_reference_j2000.to_value("jd") - t_reference_1950.to_value("jd")) * 86400
    observation_time_from_j2000 = time.TimeDelta(2122948221.5 - shift_1950_to_2000, format="sec")
    # Results:
    # 1812104598:
    # 1872333678: 294453678.0
    # 1872369875: 294489875.0
    # 2122948221.500: 545068221.5
    print("Observation UTC wrt J2000: ", observation_time_from_j2000)

    observation_time_utc_float = t_reference_j2000.to_value("jd") + observation_time_from_j2000.to_value("jd")

    observation_time_utc = time.Time(observation_time_utc_float, format="jd", scale="utc")
    # Results:
    # 1812104598: 2007-06-04T10:23:18.000
    # 1872333678: 2009-05-01T12:41:18.000
    # 1872369875: 2009-05-01T22:44:35.000
    # 2122948221.500: 2017-04-10T03:50:21.500
    print("Observation UTC: ", observation_time_utc.to_value("isot"))
    print("Observation UTC: ", observation_time_utc.to_value("jd"))

    observation_time_tdb = observation_time_utc.tdb
    observation_time_tdb_j2000 = observation_time_tdb - time.Time('2000-01-01T12:00:00', format='isot', scale='tdb')
    # Results:
    # 1812104598:
    # 1872333678: 294453744.18548495
    # 1872369875: 294489941.1854838
    # 2122948221.500: 545068290.6856526
    print("Observation TDB wrt J2000: ", observation_time_tdb_j2000.to_value("sec"))

########################################################################################################################
def main():

    t_reference_utc = time.Time(['1950-01-01T00:00:00'], format='isot', scale='utc')
    print( t_reference_utc.to_value("mjd", "long") )

    t_reference_tai = t_reference_utc.tai
    print( t_reference_tai.to_value("mjd", "long") )

########################################################################################################################
if __name__ == "__main__":
    # main()
    # option1()
    # option2()
    option3()