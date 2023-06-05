# install Psafechoices package version 0.2
# pip install git+https://github.com/lotentua/Perceived_safety_choices

# upgrade Psafechoices package # STILL UNDER DEVELOPMENT
# pip install --upgrade --force-reinstall git+https://github.com/lotentua/Perceived_safety_choices

import os
import pandas as pd
import warnings
import numpy as np
import tempfile
import zipfile
warnings.simplefilter(action='ignore', category=FutureWarning)
import geopandas as gpd

from Psafechoices.network_analysis import traffic_params_upd as trfp
from Psafechoices.network_analysis import lin_psafe_calc as linpsafe
from Psafechoices.network_analysis import maphist as mph
from Psafechoices.psafe_model import psafe_coeff_upd as psmodel
from Psafechoices.network_analysis import shp_to_csv_xml_tool as convert
from Psafechoices.routing_model import network_graph as dij
from Psafechoices.choice_model import opp_cost_calculator as opp

def false10153(df): # fix the problem with the discontinuities
    for i in range(0, len(df)):
        if df.loc[i, "id"] == 10153:
            df.loc[i, "oneway"] = 0
            break
        else: continue
    return df

######## fix modes
# fix the problem with the main modes.
def fixmodes(df):
    for i in range(0, len(df)):
        if df.loc[i, "modes"] == "car":
           df.loc[i, "modes"] = "car, ebike, escoot"
           continue
        elif df.loc[i, "modes"] == "car,bicycle,escooter,walk":
            df.loc[i, "modes"] = "car, ebike, escoot"
            continue
        else: 
            df.loc[i, "modes"] = "ebike, escoot"
            continue
    return df

# downscale the capacity of the road network....
def updcapacity(df, dsc):
    df.capacity = df.capacity * dsc
    return df

# NEW NEW NEW ... MODULES TO ESTIMATE INDICATORS
# they have been integrated in the setup file
# from Psafechoices.microindianalysis import indicators as indi
# from Psafechoices.microindianalysis import analysistools as ana

# from Psafechoices.routing_model import assess_analysis as ass

root_dir = os.path.dirname(os.path.realpath(__file__))

# To run the Psafechoices model, it requires two models as inputs
# Psafe model: ordinal logistic regression model with infrastructure parameters
# Choice model: BIOGEME discrete choice mode with time + cost + safety

scenario = 'LocalScenarioAthens4'
nod_link = os.path.join(root_dir, 'shapefiles', 'LocalScenarioAthens0', 'scenarioAthens_nodes.shp')
lin_link = os.path.join(root_dir, 'shapefiles', scenario, 'scenarioAthens_links_4.shp')

# read the nodes from a shapefile
nod = trfp.read_shapefile(nod_link)
# read the links from a shapefile
# TEST HERE NEW SCENARIOS WITH INFRASTUCTURE UPDATES
lin = trfp.read_shapefile(lin_link)
# update traffic parameters and coordinates with nodes

lin = false10153(lin)
lin = fixmodes(lin)
lin = trfp.upd_links(lin, nod).reset_index()
dwnscl = 0.01
lin = updcapacity(lin, dwnscl)

# update perceived safety model parameters using the output model from Rchoice
# in this case, default perceived safety models are used. Use your own models...
cf = pd.read_csv(os.path.join(root_dir, 'default_models', 'psafe','simple_psafe_models.csv'), ',')
cf = psmodel.psafe_coeff_upd(cf)
# estimate perceived safety per link and per transport mode
lin = linpsafe.lin_psafe(lin, cf)
# create a csv file for mapping purposes
outpath = os.path.join(root_dir, 'outputs', scenario)

csv = 'psafest_'+ scenario + '.csv'
convert.netcsv_cr(lin, os.path.join(outpath, csv))
# create an XML for MATSim
convert.netxml_cr(lin, nod, os.path.join(outpath, 'psafest_'+ scenario + '.xml'))