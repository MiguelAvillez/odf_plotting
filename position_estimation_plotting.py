
from matplotlib import pyplot as plt
import numpy as np

import build_directory
import tudatpy
from tudatpy.kernel.astro import element_conversion

########################################################################################################################
def cartesian_to_keplerian( cartesian_state_history: np.ndarray,
                            gravitational_parameter: float ) -> np.ndarray:

    keplerian_state_history = np.zeros(np.shape(cartesian_state_history))

    for i in range(0, np.shape(keplerian_state_history)[0]):
        keplerian_state_history[i, :] = element_conversion.cartesian_to_keplerian(
            cartesian_state_history[i, :], gravitational_parameter)

    return keplerian_state_history

########################################################################################################################
def plot():

    s = 1
    lw = 0.5
    rasterize = False
    plot_position_error = True
    plot_kepler_elements_error = True
    plot_step_size = False

    dir = "MGS/mors_2190/estimation_position/" # /data_spice_test

    file_tag = "november2005"
    # file_tag = "novDec2005"

    full_state_history_prefit = np.loadtxt(f"{dir}/stateHistoryPropagatedPreFit_{file_tag}.txt")
    time_history_prefit = full_state_history_prefit[:,0]
    state_history_prefit = full_state_history_prefit[:,1:]

    full_state_history_postfit = np.loadtxt(f"{dir}/stateHistoryPropagatedPostFit_{file_tag}Tol10.txt")
    time_history_postfit = full_state_history_postfit[:,0]
    state_history_postfit = full_state_history_postfit[:,1:]

    full_state_history_spice = np.loadtxt(f"{dir}/stateHistorySpice_{file_tag}.txt")
    time_history_spice = full_state_history_spice[:,0]
    state_history_spice = full_state_history_spice[:,1:]

    residuals_history_full = np.loadtxt(f"{dir}/residuals_{file_tag}.txt")
    residuals_history = np.reshape(residuals_history_full[:,-1], (int(np.size(residuals_history_full[:,-1])/3), 3))
    residuals_time_history = np.reshape(residuals_history_full[:,0], (int(np.size(residuals_history_full[:,0])/3), 3))[:,0]

    reference_state_tag = "ToSpice"

    # Mars gravitational parameter from celestialBodyConstants.h in tudat
    mars_gravitational_parameter = 1.32712440018e20 / 3098708.0

    ####################################################################################################################

    # if plot_residuals:
    #     # Load residuals
    #     residuals = np.loadtxt(f"{dir}/residuals_{file_tag}.txt")
    #     arg_t_ref = np.argmin(residuals[:,0])
    #
    #     # mask = np.abs(residuals) < 1e5
    #     mask = np.abs(residuals) < np.inf
    #     residuals[~mask] = np.nan
    #
    #     fig, ax = plt.subplots(1, 1, figsize = (6,3), constrained_layout = True)
    #     # ax.scatter((residuals[:, 0] - state_history_propagated[0, 0]) / 86400,
    #     #            residuals[:, 1], s=s / 5, rasterized=rasterize, label="pre-fit")
    #     ax.scatter((residuals[:, 0] - state_history_propagated[0, 0]) / 86400,
    #                residuals[:, -1], s=s / 5, rasterized=rasterize, label="post-fit")
    #
    #     ax.set_xlabel("Time [day]")
    #     ax.set_ylabel("Residuals (2/3-way Doppler) [" + unit + "]")
    #
    #     # ax.set_ylim([-500, 1500]
    #     ax.set_ylim([-0.2, 0.2])
    #
    #     ax.legend()
    #     ax.grid()
    #     plt.savefig(f'{dir}/plots/{file_tag}_residuals_23wayDoppler.pdf', bbox_inches='tight', pad_inches=0.02)
    #     plt.close()

    ####################################################################################################################

    if plot_position_error:
        fig, ax = plt.subplots(1, 1, figsize = (6,3), constrained_layout=True)
        ax.plot((time_history_prefit[10:-10] - time_history_prefit[0]) / 86400,
                   np.linalg.norm(state_history_prefit[10:-10,0:3] - state_history_spice[10:-10,0:3], axis=1) / 1e3,
                   lw=lw*2, label="Pre-fit")
        ax.plot((time_history_postfit[:-10] - time_history_postfit[0]) / 86400,
                   np.linalg.norm(state_history_postfit[:-10,0:3] - state_history_spice[:-10,0:3], axis=1) / 1e3,
                   lw=lw*2, label="Post-fit (from state)")

        ax.set_xlabel("Time [day]")
        ax.set_ylabel("Position norm error [km]")
        ax.legend()

        ax.set_yscale("log")
        ax.grid()
        plt.savefig(f'{dir}/plots/{file_tag}_positionError{reference_state_tag}.pdf', bbox_inches='tight', pad_inches=0.02)
        plt.close()

        fig, ax = plt.subplots(1, 1, figsize = (6,3), constrained_layout = True)
        # ax.plot((time_history_prefit[:-10] - time_history_prefit[0]) / 86400,
        #         (np.linalg.norm(state_history_prefit[:-10,0:3], axis=1) - np.linalg.norm(state_history_spice[:-10,0:3], axis=1)) / 1e3,
        #         lw=lw*2, label="Pre-fit")
        ax.plot((time_history_postfit[:-10] - time_history_postfit[0]) / 86400,
                (np.linalg.norm(state_history_postfit[:-10,0:3], axis=1) - np.linalg.norm(state_history_spice[:-10,0:3], axis=1)) / 1e3,
                lw=lw*2, label="Post-fit")

        ax.set_xlabel("Time [day]")
        ax.set_ylabel("Position error [km]")
        ax.legend()

        # ax.set_yscale("log")
        ax.grid()
        plt.savefig(f'{dir}/plots/{file_tag}_positionNormError{reference_state_tag}.pdf', bbox_inches='tight', pad_inches=0.02)
        plt.close()

    ####################################################################################################################

    if plot_kepler_elements_error:

        kepler_history_spice = cartesian_to_keplerian(state_history_spice, mars_gravitational_parameter)

        # for state_history, out_name in zip([state_history_prefit, state_history_postfit], ["preFit", "postFit"]):
        for state_history, out_name in zip([state_history_postfit], ["postFit"]):

            kepler_history = cartesian_to_keplerian(state_history, mars_gravitational_parameter)

            fig, axs = plt.subplots(2, 3, figsize=(9,4.5), constrained_layout=True)
            axs[0,0].plot((time_history_prefit[:-10] - time_history_prefit[0]) / 86400,
                          (kepler_history[:-10,0] - kepler_history_spice[:-10,0]) / 1e3, lw=lw)
            axs[0,0].set_ylabel("$\Delta$ SMA [km]")

            axs[0,1].plot((time_history_prefit[:-10] - time_history_prefit[0]) / 86400,
                          (kepler_history[:-10,1] - kepler_history_spice[:-10,1]), lw=lw)
            axs[0,1].set_ylabel("$\Delta$ ECC [-]")

            axs[0,2].plot((time_history_prefit[:-10] - time_history_prefit[0]) / 86400,
                          (kepler_history[:-10,2] - kepler_history_spice[:-10,2]) * 180 / np.pi, lw=lw)
            axs[0,2].set_ylabel("$\Delta$ INC [deg]")

            axs[1,0].plot((time_history_prefit[:-10] - time_history_prefit[0]) / 86400,
                          (kepler_history[:-10,3] - kepler_history_spice[:-10,3]) * 180 / np.pi, lw=lw)
            axs[1,0].set_ylabel("$\Delta$ AOP [deg]")

            axs[1,1].plot((time_history_prefit[:-10] - time_history_prefit[0]) / 86400,
                          (kepler_history[:-10,4] - kepler_history_spice[:-10,4]) * 180 / np.pi, lw=lw)
            axs[1,1].set_ylabel("$\Delta$ RAAN [deg]")

            ###### True anomaly
            # axs[1,2].plot((time_history_prefit[:-10] - time_history_prefit[0]) / 86400,
            #               (kepler_history[:-10,5] - kepler_history_spice[:-10,5]) * 180 / np.pi, lw=lw)
            # axs[1,2].set_ylabel("$\Delta \\theta$ [deg]")

            ###### True longitude
            # true_longitude = kepler_history[:,3] + kepler_history[:,4] + kepler_history[:,5]
            # true_longitude_spice = kepler_history_spice[:,3] + kepler_history_spice[:,4] + kepler_history_spice[:,5]
            #
            # delta_true_longitude = true_longitude[:-10] - true_longitude_spice[:-10]
            # for i in range(np.size(delta_true_longitude)):
            #     if delta_true_longitude[i] > 0:
            #         delta_true_longitude[i] = delta_true_longitude[i] % (2 * np.pi)
            #     else:
            #         delta_true_longitude[i] = delta_true_longitude[i] % (-2 * np.pi)
            #
            # axs[1,2].plot((time_history_prefit[:-10] - time_history_prefit[0]) / 86400,
            #               delta_true_longitude * 180 / np.pi, lw=lw)
            # axs[1,2].set_ylabel("$\Delta$ true long [deg]")

            ##### Argument of latitude
            argument_latitude = kepler_history[:,3] + kepler_history[:,5]
            argument_latitude_spice = kepler_history_spice[:,3] + kepler_history_spice[:,5]

            delta_argument_latitude = argument_latitude[:-10] - argument_latitude_spice[:-10]

            axs[1,2].plot((time_history_prefit[:-10] - time_history_prefit[0]) / 86400,
                          delta_argument_latitude * 180 / np.pi, lw=lw)
            axs[1,2].set_ylabel("$\Delta$ arg latitude [deg]")


            for ax in axs.flatten():
                ax.set_xlabel("Time [day]")
                ax.grid()

            plt.savefig(f'{dir}/plots/{file_tag}_{out_name}KeplerError{reference_state_tag}.pdf', bbox_inches='tight', pad_inches=0.02)
            plt.close()

        fig, axs = plt.subplots(2, 3, figsize=(9,4.5), constrained_layout=True)
        axs[0,0].plot((time_history_prefit[:-10] - time_history_prefit[0]) / 86400,
                      (kepler_history_spice[:-10,0]) / 1e3, lw=lw)
        axs[0,0].set_ylabel("SMA [km]")

        axs[0,1].plot((time_history_prefit[:-10] - time_history_prefit[0]) / 86400,
                      (kepler_history_spice[:-10,1]), lw=lw)
        axs[0,1].set_ylabel("ECC [-]")

        axs[0,2].plot((time_history_prefit[:-10] - time_history_prefit[0]) / 86400,
                      (kepler_history_spice[:-10,2]) * 180 / np.pi, lw=lw)
        axs[0,2].set_ylabel("INC [deg]")

        axs[1,0].plot((time_history_prefit[:-10] - time_history_prefit[0]) / 86400,
                      (kepler_history_spice[:-10,3]) * 180 / np.pi, lw=lw)
        axs[1,0].set_ylabel("AOP [deg]")

        axs[1,1].plot((time_history_prefit[:-10] - time_history_prefit[0]) / 86400,
                      (kepler_history_spice[:-10,4]) * 180 / np.pi, lw=lw)
        axs[1,1].set_ylabel("RAAN [deg]")

        for ax in axs.flatten():
            ax.set_xlabel("Time [day]")
            ax.grid()

        plt.savefig(f'{dir}/plots/{file_tag}_kepler.pdf', bbox_inches='tight', pad_inches=0.02)
        plt.close()

    if plot_step_size:
        full_state_history_prefit_raw = np.loadtxt(f"{dir}/stateHistoryPropagatedPreFitRaw_{file_tag}.txt")
        time_history_prefit_raw = full_state_history_prefit_raw[:,0]

        fig, ax = plt.subplots(1, 1, figsize = (6,3), constrained_layout = True)
        time_history = time_history_prefit_raw[10:-10]
        step_size = time_history[1:] - time_history[:-1]
        ax.plot((time_history[:-1] - time_history[0]) / 86400,
                step_size, lw=lw*2)

        ax.set_xlabel("Time [day]")
        ax.set_ylabel("Step size [s]")

        # ax.set_yscale("log")
        ax.grid()
        plt.savefig(f'{dir}/plots/{file_tag}_stepSizePreFit.pdf', bbox_inches='tight', pad_inches=0.02)
        plt.close()

########################################################################################################################
if __name__ == "__main__":
    plot()