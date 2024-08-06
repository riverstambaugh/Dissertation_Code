# Dissertation_Code
This repository stores all Python code developed for my MSc dissertation at the University of St. Andrews. There are 3 total algorithms that determine whether or not two C(2) monoid presentations present isomorphic monoids.

Users should note that all code was developed in Python using the Windows susbsystem for Linux (WSL). In order for the code in this repo to run, users must first install the libsemigroups_pybind11 package. More information is available here: https://libsemigroups.github.io/libsemigroups_pybind11/install.html

The code contains 3 algorithms: brute_force_checker (from brute_force.py), check_isomorphic, and check_isomorphic_graphwise, as well as two test files: test_isomorphic and timing_and_figures. There is one additional Python file, presentation_normal_form, used in all 3 algorithms to compute the canonical form of a given presentation. In order for the algorithms to run correctly, be advised that all files must be downloaded and in the same directory.

The 'visualizations' file contains directories with all generated visualizations, including isomorphism bitmaps for certain presentation classes, scatterplots that compare algorithm times, and bitmaps that compare algorithm times. All figures in visualizations were generated using timing_and_figures.

If a user desires to test the presentations or create their own visualizations, refer to the comments in test_isomorphic and timing_and_figures for a more detailed guide.
