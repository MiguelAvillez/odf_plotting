
import build_directory

from matplotlib import pyplot as plt
import numpy as np

import tudatpy
from tudatpy.util import result2array
from tudatpy.kernel.interface import spice
from tudatpy.kernel.numerical_simulation import environment_setup, estimation, estimation_setup
from tudatpy.kernel.numerical_simulation.estimation_setup import observation
from tudatpy.kernel import io

########################################################################################################################
def read_odf():

    odf_file = "/Users/pipas/Documents/dsn_trk-2-18/odf07155.dat"
    messenger_spice_file = "/Users/pipas/Documents/messenger-spice/msgr_040803_080216_120401.bsp"

    # Load spice kernels
    spice.load_standard_kernels()
    spice.load_kernel(messenger_spice_file)

    # Create bodies
    bodiesToCreate = ["Earth"]
    spacecraft_name = "Messenger"

    body_settings = environment_setup.get_default_body_settings(bodiesToCreate)
    body_settings.get("Earth").ground_station_settings = environment_setup.ground_station.dsn_stations()

    bodies = environment_setup.create_system_of_bodies(body_settings)

    # Read odf file
    raw_odf_file = io.read_odf_file(odf_file)

    # Process odf file
    processed_odf_file = estimation.ProcessedOdfFileContents(raw_odf_file, bodies.get_body("Earth"), True, spacecraft_name)

    # Create observation collection
    observed_observation_collection = estimation.create_odf_observed_observations(processed_odf_file, bodies)
    observed_observations = np.array(observed_observation_collection.concatenated_observations)
    time_history = np.array(observed_observation_collection.concatenated_times)
    observation_set_start_and_size = observed_observation_collection.observation_set_start_index_and_size

    fig, ax = plt.subplots(1, 1, figsize = (6,3), constrained_layout = True)

    colors = plt.rcParams['axes.prop_cycle'].by_key()['color']
    color_counter = -1
    for observation_type in observation_set_start_and_size.keys():
        for linkEnds in observation_set_start_and_size[observation_type].keys():
            color_counter += 1
            labelPlot = True
            for i in range(len(observation_set_start_and_size[observation_type][linkEnds])):
                start_id = observation_set_start_and_size[observation_type][linkEnds][i][0]
                end_id = start_id + observation_set_start_and_size[observation_type][linkEnds][i][1]

                if labelPlot:
                    labelPlot = False
                    label = f"link ends {linkEnds}"
                else:
                    label = None

                ax.scatter(time_history[start_id:end_id] - np.min(time_history),
                           observed_observations[start_id:end_id], s=0.01, marker=".",
                           # label=f"{observation_type}, link ends {linkEnds}")
                           label=label, c=colors[color_counter])
                # ax.plot(time_history[start_id:end_id] - np.min(time_history),
                #            observed_observations[start_id:end_id], lw=0.5,
                #            # label=f"{observation_type}, link ends {linkEnds}")
                #            label=f"link ends {linkEnds}")
                ax.plot(time_history[start_id:end_id] - np.min(time_history) - 735,
                           observed_observations[start_id:end_id], lw=0.5,
                           # label=f"{observation_type}, link ends {linkEnds}")
                           label=label, ls="--", c=colors[color_counter])

    # Read ramp data for DSS-63
    rampData = np.loadtxt("rampData_2007DSS-14.txt")

    ramp_start_times = rampData[:, 0]
    ramp_end_times = rampData[:, 1]
    ramp_rates = rampData[:, 2]
    ramp_start_frequencies = rampData[:, 3]

    for t in ramp_start_times:
        ax.axvline(t - np.min(time_history), lw=0.5, ls="--", c="k", zorder=0)

    ax.set_xlabel("Time from June 4, 2007, 10:23:17 [s]")
    ax.set_ylabel("Frequency (2-way Doppler) [Hz]")
    ax.grid()
    ax.legend()
    ax.set_ylim([-2000, 19000])
    # plt.show()

    plt.savefig(f'odf_observed_2way_doppler_messenger_tudatpy.pdf', bbox_inches='tight', pad_inches=0.02)
    plt.close()

    ####################################################################################################################
    fig, ax = plt.subplots(1, 1, figsize = (6,3), constrained_layout = True)

    ramp_times = []
    ramp_frequencies = []
    for i in range(1, np.size(ramp_start_times)):
        ramp_times.append(ramp_start_times[i])
        ramp_frequencies.append(ramp_start_frequencies[i])

        ramp_times.append(ramp_end_times[i])
        ramp_frequencies.append(ramp_start_frequencies[i] + ramp_rates[i] * (ramp_end_times[i] - ramp_start_times[i]))

    ramp_times = np.array(ramp_times)
    ramp_frequencies = np.array(ramp_frequencies)

    ax.plot(ramp_times - np.min(time_history), ramp_frequencies - ramp_frequencies[0], lw=0.5, marker="o", markersize=0.5)

    for t in ramp_start_times:
        ax.axvline(t - np.min(time_history), lw=0.5, ls="--", c="k", zorder=0)

    ax.set_xlabel("Time from June 4, 2007, 10:23:17 [s]")
    ax.set_ylabel("Frequency DSS-63 [Hz]")
    ax.grid()
    # plt.show()

    plt.savefig(f'odf_transmitted_frequency_dss63.pdf', bbox_inches='tight', pad_inches=0.02)
    plt.close()

    ####################################################################################################################
    fig, ax = plt.subplots(1, 1, figsize = (6,3), constrained_layout = True)
    # ax.plot(ramp_start_times - np.min(time_history),
    #         ramp_start_frequencies - ramp_start_frequencies[0], lw=0.5, marker="o", markersize=0.5)
    ax.plot(ramp_start_times - np.min(time_history),
            ramp_rates, lw=0.5, marker="o", markersize=0.5)
    ax.set_ylim([-0.5, 1])
    # ax.set_xlim(left=64000)

    for t in ramp_start_times:
        ax.axvline(t - np.min(time_history), lw=0.5, ls="--", c="k", zorder=0)

    ax.set_xlabel("Time from June 4, 2007, 10:23:17 [s]")
    ax.set_ylabel("Frequency rate DSS-63 [Hz/s]")
    ax.grid()
    # plt.show()

    plt.savefig(f'odf_ramp_rate_dss63.pdf', bbox_inches='tight', pad_inches=0.02)
    plt.close()

########################################################################################################################
def plot_odf():

    s = 2
    rasterize = False
    plot_observations = True
    plot_corrections_effect = True
    color_link_ends = True

    dir = "MGS/mors_2190" # /data_spice_test
    # dir = "MGS/mors_0401"
    # dir = "magellan/mg_2601"

    unit = "Hz" # m/s

    # Read ramp data
    # rampData = np.loadtxt("rampData_2017_navDSS-55.txt")
    # # rampData = np.loadtxt("rampData_2007DSS-14.txt")
    #
    # ramp_start_times = rampData[:, 0]
    # ramp_end_times = rampData[:, 1]
    # ramp_rates = rampData[:, 2]
    # ramp_start_frequencies = rampData[:, 3]

    odf_file_tag = "5332333aOdf_interpState50"
    # odf_file_tag = "5327332aOdf_interpState50"
    # odf_file_tag = "mors0401"
    # odf_file_tag = "mg2601"
    file_tag_noCorr = odf_file_tag + "_noCorr_test3"
    file_tag_relCorr = odf_file_tag + "_relCorr_test3"
    file_tag_troCorr = odf_file_tag + "_troCorr_test3"
    file_tag_ionCorr = odf_file_tag + "_ionCorr_test3"
    file_tag_troGodotCorr = odf_file_tag + "_troGdCorr"
    file_tag_ionGodotCorr = odf_file_tag + "_ionGdCorr"
    file_tag = file_tag_noCorr

    # Load observations
    observations = np.loadtxt(f"{dir}/observations_{file_tag}.txt")
    simulated_observations = observations[:,0:2]
    observed_observations = observations[:,2:4]

    # Sort observations by time
    simulated_observations = simulated_observations[simulated_observations[:, 0].argsort()]
    observed_observations = observed_observations[observed_observations[:, 0].argsort()]

    observation_set_start_and_size = np.loadtxt(f"{dir}/observationsStartAndSize_{file_tag}.txt", dtype=int)

    arg_t_ref = np.argmin(observed_observations[:,0])
    arg_f_ref = np.argmin(observed_observations[:,0])

    ####################################################################################################################

    if plot_observations:
        fig, ax = plt.subplots(1, 1, figsize = (6,3), constrained_layout = True)

        # ax.scatter(observed_observations[:,0] - observed_observations[arg_t_ref, 0],
        #            observed_observations[:,1] - observed_observations[arg_f_ref, 1], s=s)
        # ax.scatter(simulated_observations[:,0] - simulated_observations[arg_t_ref, 0],
        #            (simulated_observations[:,1] - simulated_observations[arg_f_ref, 1]) * 0.5, s=s, alpha=0.2)

        # mask = np.abs(observed_observations[:,1]) < 1e6
        mask = np.abs(observed_observations[:,1]) < np.inf

        ax.scatter((observed_observations[mask,0] - observed_observations[arg_t_ref, 0]) / 86400,
                   observed_observations[mask,1],
                   s=s, label="Observed", rasterized=rasterize)
        ax.scatter((simulated_observations[:,0] - observed_observations[arg_t_ref, 0]) / 86400,
                   simulated_observations[:,1],
                   s=s, label="Simulated", rasterized=rasterize)

        # for t in ramp_start_times:
        #     ax.axvline(t - simulated_observations[arg_t_ref, 0], lw=0.5, ls="--", c="k", zorder=0)

        # ax.scatter(simulated_observations[:,0] - simulated_observations[arg_t_ref, 0],
        #            (observed_observations[:,1] - observed_observations[arg_f_ref, 1]) -
        #            (simulated_observations[:,1] - simulated_observations[arg_f_ref, 1]) * 0.5, s=s)

        ax.set_xlabel("Time [day]")
        ax.set_ylabel("Observable (2/3-way Doppler) [" + unit + "]")
        # ax.set_ylim([-2000, 32000])
        # ax.set_xlim([0, 10000])
        # ax.set_ylim([-10, 15])
        # ax.set_xlim([5.4e3, 10e3])
        # ax.set_xlim([6.25e3, 6.75e3])
        # ax.set_ylim([-18e3, 20e3])
        ax.legend()
        ax.grid()
        plt.savefig(f'{dir}/plots/{file_tag}_observations_23wayDoppler.pdf', bbox_inches='tight', pad_inches=0.02)
        plt.close()

    ####################################################################################################################

    residuals = observed_observations[:, 1] - (simulated_observations[:,1])

    # mask = np.abs(residuals) < 1e5
    mask = np.abs(residuals) < np.inf
    residuals[~mask] = np.nan

    fig, ax = plt.subplots(1, 1, figsize = (6,3), constrained_layout = True)
    if color_link_ends:
        colors = plt.rcParams['axes.prop_cycle'].by_key()['color']
        color_counter = -1
        for i in range(np.shape(observation_set_start_and_size)[0]):
            if i == 0 or observation_set_start_and_size[i,1] != observation_set_start_and_size[i-1,1]:
                color_counter += 1
            start_id = observation_set_start_and_size[i,2]
            end_id = start_id + observation_set_start_and_size[i,3]
            ax.scatter((simulated_observations[start_id:end_id,0] - simulated_observations[arg_t_ref, 0])/86400,
                       residuals[start_id:end_id], s=s / 5, rasterized=rasterize)
            # print(simulated_observations[start_id,0], simulated_observations[end_id-1,0], )
    else:
        ax.scatter((simulated_observations[:,0] - simulated_observations[arg_t_ref, 0])/86400,
                       residuals, s=s / 5, rasterized=rasterize)

    # for t in ramp_start_times:
    #     ax.axvline(t - simulated_observations[arg_t_ref, 0], lw=0.5, ls="--", c="k", zorder=0)

    ax.set_xlabel("Time [day]")
    ax.set_ylabel("Residuals (2/3-way Doppler) [" + unit + "]")
    # ax.set_ylim([-50, 20])
    # ax.set_xlim([35e3, 65e3])
    # ax.set_ylim([-0.5, 0.5])
    # ax.set_ylim([-0.6, 1.5])
    # ax.set_ylim([-1.5, 1.5])
    # ax.set_xlim([5.4e3, 10e3])
    ax.set_ylim([-0.15, 0.2])
    ax.grid()
    plt.savefig(f'{dir}/plots/{file_tag}_residuals_23wayDoppler.pdf', bbox_inches='tight', pad_inches=0.02)
    plt.close()

    rms = np.sqrt(np.mean((simulated_observations[mask,1] - observed_observations[mask, 1])**2))
    print("Residuals RMS [Hz]: ", rms)


    ####################################################################################################################
    # fig, ax = plt.subplots(1, 1, figsize = (6,3), constrained_layout = True)
    #
    # ramp_times = []
    # ramp_frequencies = []
    # for i in range(1, np.size(ramp_start_times)):
    #     ramp_times.append(ramp_start_times[i])
    #     ramp_frequencies.append(ramp_start_frequencies[i])
    #
    #     ramp_times.append(ramp_end_times[i])
    #     ramp_frequencies.append(ramp_start_frequencies[i] + ramp_rates[i] * (ramp_end_times[i] - ramp_start_times[i]))
    #
    # ramp_times = np.array(ramp_times)
    # ramp_frequencies = np.array(ramp_frequencies)
    #
    # ax.plot(ramp_times - simulated_observations[arg_t_ref, 0], ramp_frequencies - ramp_frequencies[0], lw=0.5, marker="o", markersize=0.5)
    #
    # for t in ramp_start_times:
    #     ax.axvline(t - simulated_observations[arg_t_ref, 0], lw=0.5, ls="--", c="k", zorder=0)
    #
    # ax.set_xlabel("Time [s]")
    # ax.set_ylabel("Frequency [Hz]")
    # ax.grid()
    # ax.set_xlim([5.4e3, 10e3])
    #
    # plt.savefig(f'odf_gs_transmitted_frequency.pdf', bbox_inches='tight', pad_inches=0.02)
    # plt.close()

    ####################################################################################################################
    # fig, ax = plt.subplots(1, 1, figsize = (6,3), constrained_layout = True)
    # ax.plot(ramp_start_times - simulated_observations[arg_t_ref, 0],
    #         ramp_rates, lw=0.5, marker="o", markersize=0.5)
    # # ax.set_ylim([-0.5, 1])
    # # ax.set_xlim(left=64000)
    #
    # for t in ramp_start_times:
    #     ax.axvline(t - simulated_observations[arg_t_ref, 0], lw=0.5, ls="--", c="k", zorder=0)
    #
    # ax.set_xlabel("Time [s]")
    # ax.set_ylabel("Frequency rate [Hz/s]")
    # ax.grid()
    # # ax.set_xlim([5.4e3, 10e3])
    #
    # plt.savefig(f'odf_gs_ramp_rate.pdf', bbox_inches='tight', pad_inches=0.02)
    # plt.close()

    ####################################################################################################################

    if plot_corrections_effect:
        observations = np.loadtxt(f"{dir}/observations_{file_tag_noCorr}.txt")
        simulated_observations_noCorrection = observations[:,0:2]
        observations = np.loadtxt(f"{dir}/observations_{file_tag_relCorr}.txt")
        simulated_observations_relCorrection = observations[:,0:2]
        observations = np.loadtxt(f"{dir}/observations_{file_tag_troCorr}.txt")
        simulated_observations_troCorrection = observations[:,0:2]
        observations = np.loadtxt(f"{dir}/observations_{file_tag_ionCorr}.txt")
        simulated_observations_ionCorrection = observations[:,0:2]
        # observations = np.loadtxt(f"{dir}/observations_{file_tag_troGodotCorr}.txt")
        # simulated_observations_troGodotCorrection = observations[:,0:2]
        # observations = np.loadtxt(f"{dir}/observations_{file_tag_ionGodotCorr}.txt")
        # simulated_observations_ionGodotCorrection = observations[:,0:2]

        fig, ax = plt.subplots(1, 1, figsize = (6,3), constrained_layout = True)

        arg_t_ref = np.argmin(simulated_observations_noCorrection[:,0])
        ax.scatter(simulated_observations_noCorrection[:, 0] - simulated_observations_noCorrection[arg_t_ref, 0],
                   simulated_observations_relCorrection[:, 1] - simulated_observations_noCorrection[:, 1],
                   s=s / 5, rasterized=rasterize, label="REL")
        ax.scatter(simulated_observations_noCorrection[:, 0] - simulated_observations_noCorrection[arg_t_ref, 0],
                   simulated_observations_troCorrection[:, 1] - simulated_observations_noCorrection[:, 1],
                   s=s / 5, rasterized=rasterize, label="TRO tabulated")
        ax.scatter(simulated_observations_noCorrection[:, 0] - simulated_observations_noCorrection[arg_t_ref, 0],
                   simulated_observations_ionCorrection[:, 1] - simulated_observations_noCorrection[:, 1],
                   s=s / 5, rasterized=rasterize, label="ION tabulated")
        # ax.scatter(simulated_observations_noCorrection[:, 0] - simulated_observations_noCorrection[arg_t_ref, 0],
        #            simulated_observations_troGodotCorrection[:, 1] - simulated_observations_noCorrection[:, 1],
        #            s=s / 5, rasterized=rasterize, label="TRO saastamoinen")
        # ax.scatter(simulated_observations_noCorrection[:, 0] - simulated_observations_noCorrection[arg_t_ref, 0],
        #            simulated_observations_ionGodotCorrection[:, 1] - simulated_observations_noCorrection[:, 1],
        #            s=s / 5, rasterized=rasterize, label="ION jakowsky")

        ax.set_xlabel("Time [s]")
        ax.set_ylabel("Correction (2/3-way Doppler) [" + unit + "]")
        ax.legend()
        ax.grid()
        plt.savefig(f'{dir}/plots/{file_tag}_corrections_23wayDoppler.pdf', bbox_inches='tight', pad_inches=0.02)
        plt.close()

########################################################################################################################
def plot_reference_frequency():

    s = 2

    dir = "MGS/mors_0401/"
    file_tag = "mors0401"

    odf_files_txt = ["9068068a_truncated.odf.txt", "9068068b_truncated.odf.txt", "9068071a_truncated.odf.txt"]

    fig, ax = plt.subplots(1, 1, figsize = (6,3), constrained_layout = True)

    for file in odf_files_txt:
        odf_orbit_data = np.loadtxt(dir + file)

        mask = odf_orbit_data[:,7] == 12

        ax.scatter(odf_orbit_data[mask, 0] / 86400, odf_orbit_data[mask, 15], s=s)

    ax.set_xlabel("Time [day]")
    ax.set_ylabel("Reference frequency [Hz]")
    ax.grid()
    plt.savefig(f'{dir}/plots/{file_tag}_reference_frequency_23wayDoppler.pdf', bbox_inches='tight', pad_inches=0.02)
    plt.close()

########################################################################################################################
if __name__ == "__main__":
    # read_odf()
    plot_odf()
    # plot_reference_frequency()