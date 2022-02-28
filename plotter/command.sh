#!/bin/bash

#python plotter.py -p ZMuE_plotting_and_cfg/plots_data.txt -i ZMuE_plotting_and_cfg/mca_data.txt  -o ZMuE_plotting_and_cfg/Plots/Data_nB0_nJet0_MTmu70_METoverHT0p6_MTe100ANDpTz20ANDMet60_nMu1nEl1Deta2p4_2 -f

#python plotter.py -p ZMuE_plotting_and_cfg/plots_mc.txt -i ZMuE_plotting_and_cfg/mca_zmue.txt  -o ZMuE_plotting_and_cfg/Plots/MC_nB0_nJet0_MTmu70_METoverHT0p6_MTe100ANDpTz20ANDMet60_nMu1nEl1Deta2p4_2 -f -l 60

python plotter.py -p ZMuE_plotting_and_cfg/plots_data.txt -i ZMuE_plotting_and_cfg/mca_data.txt  -o ZMuE_plotting_and_cfg/Plots/Data_sel -f

python plotter.py -p ZMuE_plotting_and_cfg/plots_zmue_acceff.txt -i ZMuE_plotting_and_cfg/mca_zmue.txt  -o ZMuE_plotting_and_cfg/Plots/AccEff -f -l 60


