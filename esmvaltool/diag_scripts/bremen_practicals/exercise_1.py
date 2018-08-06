"""Climate Modelling Part 2 (Bremen, 2018): Diagnostic for exercise 1.

Please only modify the marked sections of the code.

This exercise diagnostic contains two parts:

    1. Interpret and execute the first part of the code. Which data is
       selected, what happens to it and what is plotted?

    2. Based on the code in part 1 extract the observational dataset and
       calculate its difference to the multi-model mean ("multi-model mean
       bias"). Plot this data analogous to part 1.
"""

import logging
import os

import iris

import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt

from esmvaltool.diag_scripts.shared import run_diagnostic, select_metadata


logger = logging.getLogger(os.path.basename(__file__))


def main(cfg):
    """Execute the diagnostic."""
    ###########################################################################
    # Part 1
    ###########################################################################

    # Set path of first plot
    plot_path_1 = os.path.join(cfg['plot_dir'], 'exercise_1a.png')

    # Read dataset into cube
    input_data = cfg['input_data'].values()
    mmm_data = select_metadata(input_data, dataset='MultiModelMean')[0]
    mmm_file = mmm_data['filename']
    logger.info("Reading %s", mmm_file)
    mmm_cube = iris.load_cube(mmm_file)

    # Process the data
    mmm_cube = mmm_cube.collapsed('time', iris.analysis.MEAN)

    # Plot the data
    iris.quickplot.contourf(mmm_cube, cmap='jet')
    plt.gca().coastlines()
    plt.savefig(plot_path_1)
    logger.info("Writing %s", plot_path_1)
    plt.close()

    ###########################################################################
    # Part 2
    # Please do not modify anything above this line
    ###########################################################################

    # Set path of second plot
    plot_path_2 = os.path.join(cfg['plot_dir'], 'exercise_1b.png')

    # Exctract observations
    obs_data = select_metadata(input_data, project='OBS')[0]
    obs_file = obs_data['filename']
    logger.info("Reading %s", obs_file)
    obs_cube = iris.load_cube(obs_file)

    # Calculate temporal mean and bias
    obs_cube = obs_cube.collapsed('time', iris.analysis.MEAN)
    bias_cube = mmm_cube - obs_cube
    bias_cube.rename("Bias in surface air temperature")

    # Plot the data
    iris.quickplot.contourf(bias_cube, cmap='jet')
    plt.gca().coastlines()
    plt.savefig(plot_path_2)
    logger.info("Writing %s", plot_path_2)

    ###########################################################################
    # Please do not modify anything below this line
    ###########################################################################


# Call the main function when the script is called
if __name__ == '__main__':

    with run_diagnostic() as config:
        main(config)
