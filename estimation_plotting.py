
from matplotlib import pyplot as plt
import numpy as np

########################################################################################################################
def plot_odf():

    s = 1
    rasterize = False
    plot_residuals = True
    plot_position_error = False

    dir = "MGS/mors_2190/estimation/" # /data_spice_test

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
    # odf_file_tag = "5327332aOdf"
    file_tag_allCorr = odf_file_tag + "_noCorrSh120Tol10Moons"
    file_tag_noCorr = odf_file_tag + "_noCorr"
    file_tag_relCorr = odf_file_tag + "_relCorr"
    file_tag_troCorr = odf_file_tag + "_troCorr"
    file_tag_ionCorr = odf_file_tag + "_ionCorr"
    file_tag = file_tag_allCorr

    state_history_propagated = np.loadtxt(f"{dir}/stateHistoryPropagated_{file_tag}.txt")
    state_history_spice = np.loadtxt(f"{dir}/stateHistorySpice_{file_tag}.txt")
    reference_state_tag = "ToSpice"
    # state_history_spice = np.loadtxt(f"{dir}/stateHistoryPropagated_{odf_file_tag}_allCorrSh80Tol10.txt")
    # reference_state_tag = "ToSh80"

    ####################################################################################################################

    if plot_residuals:
        # Load residuals
        residuals = np.loadtxt(f"{dir}/residuals_{file_tag}.txt")
        arg_t_ref = np.argmin(residuals[:,0])

        # mask = np.abs(residuals) < 1e5
        mask = np.abs(residuals) < np.inf
        residuals[~mask] = np.nan

        fig, ax = plt.subplots(1, 1, figsize = (6,3), constrained_layout = True)
        # ax.scatter((residuals[:, 0] - state_history_propagated[0, 0]) / 86400,
        #            residuals[:, 1], s=s / 5, rasterized=rasterize, label="pre-fit")
        ax.scatter((residuals[:, 0] - state_history_propagated[0, 0]) / 86400,
                   residuals[:, -1], s=s / 5, rasterized=rasterize, label="post-fit")

        ax.set_xlabel("Time [day]")
        ax.set_ylabel("Residuals (2/3-way Doppler) [" + unit + "]")

        # ax.set_ylim([-500, 1500]
        ax.set_ylim([-0.2, 0.2])

        ax.legend()
        ax.grid()
        plt.savefig(f'{dir}/plots/{file_tag}_residuals_23wayDoppler.pdf', bbox_inches='tight', pad_inches=0.02)
        plt.close()

    ####################################################################################################################

    if plot_position_error:
        fig, ax = plt.subplots(1, 1, figsize = (6,3), constrained_layout = True)
        ax.scatter((state_history_propagated[:-10, 0] - state_history_propagated[0, 0]) / 86400,
                   np.linalg.norm(state_history_propagated[:-10,1:4] - state_history_spice[:-10,1:4], axis=1) / 1e3,
                   s=s / 5, rasterized=rasterize)

        ax.set_xlabel("Time [day]")
        ax.set_ylabel("Position error [km]")

        ax.grid()
        plt.savefig(f'{dir}/plots/{file_tag}_positionError{reference_state_tag}.pdf', bbox_inches='tight', pad_inches=0.02)
        plt.close()


########################################################################################################################
if __name__ == "__main__":
    # read_odf()
    plot_odf()