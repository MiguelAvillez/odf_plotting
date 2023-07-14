
import build_directory

from matplotlib import pyplot as plt
import numpy as np

########################################################################################################################
def main():

    dir = "MGS/mors_2190"
    s = 2
    rasterize = False

    file_tag_noCorr = "5332333aOdf_noCorr"
    file_tag_relCorr = "5332333aOdf_relCorr"
    file_tag_troCorr = "5332333aOdf_troCorr"
    file_tag_ionCorr = "5332333aOdf_ionCorr"
    file_tag = file_tag_troCorr

    # light_times_noCorr = np.loadtxt(f"{dir}/lightTimes_5332333aOdf_interpState50_noCorr.txt",
    #                                 dtype=np.longdouble)
    # first_leg_times_noCorr = light_times_noCorr[:,0:3]
    # second_leg_times_noCorr = light_times_noCorr[:,3:6]
    # total_leg_times_noCorr = light_times_noCorr[:,0:3]
    # total_leg_times_noCorr[:,1:3] = first_leg_times_noCorr[:,1:3] + second_leg_times_noCorr[:,1:3]
    # total_leg_times_noCorr_initial = total_leg_times_noCorr[0::2,:]
    # total_leg_times_noCorr_final = total_leg_times_noCorr[1::2,:]
    light_times_noCorr = np.loadtxt(f"{dir}/totalLightTimes_5332333aOdf_interpState50_nwayDiff_noCorr.txt",
                                    dtype=np.longdouble)
    total_leg_times_noCorr_initial = light_times_noCorr[0::2,:]
    total_leg_times_noCorr_final = light_times_noCorr[1::2,:]

    # light_times_troCorr = np.loadtxt(f"{dir}/lightTimes_5332333aOdf_interpState50_troCorr.txt",
    #                                  dtype=np.longdouble)
    # first_leg_times_troCorr = light_times_troCorr[:,0:3]
    # second_leg_times_troCorr = light_times_troCorr[:,3:6]
    # total_leg_times_troCorr = light_times_troCorr[:,0:3]
    # total_leg_times_troCorr[:,1:3] = first_leg_times_troCorr[:,1:3] + second_leg_times_troCorr[:,1:3]
    # total_leg_times_troCorr_initial = total_leg_times_troCorr[0::2,:]
    # total_leg_times_troCorr_final = total_leg_times_troCorr[1::2,:]
    light_times_troCorr = np.loadtxt(f"{dir}/totalLightTimes_5332333aOdf_interpState50_nwayDiff_troCorr.txt",
                                    dtype=np.longdouble)
    total_leg_times_troCorr_initial = light_times_troCorr[0::2,:]
    total_leg_times_troCorr_final = light_times_troCorr[1::2,:]

    # light_times_relCorr = np.loadtxt(f"{dir}/lightTimes_5332333aOdf_interpState50_relCorr.txt",
    #                                  dtype=np.longdouble)
    # first_leg_times_relCorr = light_times_relCorr[:,0:3]
    # second_leg_times_relCorr = light_times_relCorr[:,3:6]
    # total_leg_times_relCorr = light_times_relCorr[:,0:3]
    # total_leg_times_relCorr[:,1:3] = first_leg_times_relCorr[:,1:3] + second_leg_times_relCorr[:,1:3]
    # total_leg_times_relCorr_initial = total_leg_times_relCorr[0::2,:]
    # total_leg_times_relCorr_final = total_leg_times_relCorr[1::2,:]
    light_times_relCorr = np.loadtxt(f"{dir}/totalLightTimes_5332333aOdf_interpState50_nwayDiff_relCorr.txt",
                                    dtype=np.longdouble)
    total_leg_times_relCorr_initial = light_times_relCorr[0::2,:]
    total_leg_times_relCorr_final = light_times_relCorr[1::2,:]


    fig, ax = plt.subplots(1, 1, figsize = (6,3), constrained_layout = True)

    arg_t_ref = np.argmin(light_times_noCorr[:,0])
    # ax.scatter(first_leg_times_troCorr[:, 0] - first_leg_times_troCorr[arg_t_ref, 0],
    #            first_leg_times_troCorr[:, 1] + second_leg_times_troCorr[:, 1],
    #            s=s / 5, rasterized=rasterize, label="1st leg")
    # ax.scatter(first_leg_times_noCorr[:, 0] - first_leg_times_noCorr[arg_t_ref, 0],
    #            first_leg_times_noCorr[:, 1] + second_leg_times_noCorr[:, 1],
    #            s=s / 5, rasterized=rasterize, label="1st leg")
    # ax.scatter(first_leg_times_troCorr[:, 0] - first_leg_times_troCorr[arg_t_ref, 0],
    #            (first_leg_times_troCorr[:, 1] + second_leg_times_troCorr[:, 1]) - (first_leg_times_noCorr[:, 1] + second_leg_times_noCorr[:, 1]),
    #            s=s / 5, rasterized=rasterize)
    ax.scatter(total_leg_times_noCorr_initial[:, 0] - total_leg_times_noCorr_initial[arg_t_ref, 0],
               (total_leg_times_troCorr_final[:, 1] - total_leg_times_troCorr_initial[:, 1]) -
               (total_leg_times_noCorr_final[:, 1] - total_leg_times_noCorr_initial[:, 1]),
               s=s / 5, rasterized=rasterize)
    ax.scatter(total_leg_times_noCorr_initial[:, 0] - total_leg_times_noCorr_initial[arg_t_ref, 0],
               (total_leg_times_relCorr_final[:, 1] - total_leg_times_relCorr_initial[:, 1]) -
               (total_leg_times_noCorr_final[:, 1] - total_leg_times_noCorr_initial[:, 1]),
               s=s / 5, rasterized=rasterize)


    ax.set_xlabel("Time [s]")
    ax.set_ylabel("Light time [s]")
    ax.legend()
    ax.grid()
    plt.savefig(f'{dir}/plots/{file_tag}_light_times.pdf', bbox_inches='tight', pad_inches=0.02)
    plt.close()


########################################################################################################################
if __name__ == "__main__":
    main()