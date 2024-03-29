"""
@author: ptzouras
National Technical University of Athens
Research project: PhD thesis Tzouras
"""

import os
root_dir = os.path.dirname(os.path.realpath(__file__))
from logit_est_functons import MLpanelest

os.chdir(os.path.join(root_dir, 'utilities'))
from util_definition import database
from util_definition import utils
from coeff_definition import betas, sigmas, randoms
b = betas(0, -1000, 1000, 0)
s = sigmas(0, -1000, 1000, 0)
rnds = randoms(b, s, 'NORMAL_HALTON2')

os.chdir(root_dir)
link = os.path.join(root_dir, 'sample_datasets', 'choice_dataset_perceived_choices_crop.csv')
t = 2

def car_bin(link, R):
    db = database(link, t).get_dbase()
    b = betas(0, -1000, 1000, 0)
    s = sigmas(0, -1000, 1000, 0)
    rnds = randoms(b, s, 'NORMAL_HALTON2')
    u = utils(db, b, rnds = rnds, exp = 'car_binary', typ = t)
    p = MLpanelest(db, u.get_Bincar_RND(), u.get_modecho_av(), u.get_cho(), R, 'car_binary_logit_model')
    return p

def ebike_bin(link, R):
    db = database(link, t).get_dbase()
    b = betas(0, -1000, 1000, 0)
    s = sigmas(0, -1000, 1000, 0)
    rnds = randoms(b, s, 'NORMAL_HALTON2')
    u = utils(db, b, rnds = rnds, exp = 'ebike_binary', typ = t)
    p = MLpanelest(db, u.get_Binebike_RND(), u.get_modecho_av(), u.get_cho(), R, 'ebike_binary_logit_model')
    return p

def escoot_bin(link, R):
    db = database(link, t).get_dbase()
    b = betas(0, -1000, 1000, 0)
    s = sigmas(0, -1000, 1000, 0)
    rnds = randoms(b, s, 'NORMAL_HALTON2')
    u = utils(db, b, rnds = rnds, exp = 'escoot_binary', typ = t)
    p = MLpanelest(db, u.get_Binescoot_RND(), u.get_modecho_av(), u.get_cho(), R, 'escoot_binary_logit_model')
    return p

def walk_bin(link, R):
    db = database(link, t).get_dbase()
    b = betas(0, -1000, 1000, 0)
    s = sigmas(0, -1000, 1000, 0)
    rnds = randoms(b, s, 'NORMAL_HALTON2')
    u = utils(db, b, rnds = rnds, exp = 'walk_binary', typ = t)
    p = MLpanelest(db, u.get_Binwalk_RND(), u.get_modecho_av(), u.get_cho(), R, 'walk_binary_logit_model')
    return p

def ML_model(link, R):
    db = database(link, t).get_dbase()
    b = betas(0, -1000, 1000, 0)
    s = sigmas(0, -1000, 1000, 0)
    rnds = randoms(b, s, 'NORMAL_HALTON2')
    u = utils(db, b, rnds = rnds, exp = 'mode_choice', typ = t)
    p = MLpanelest(db, u.get_MLVs(), u.get_modecho_av(), u.get_cho(), R, 'mode_choice_ML_model')
    return p

R = 5000
# p1 = car_bin(link, R)
# p1.to_csv('models/car_binary_logit_model.csv')
# p2 = ebike_bin(link, R)
# p2.to_csv('models/ebike_binary_logit_model.csv')
# p3 = escoot_bin(link, R)
# p3.to_csv('models/escoot_binary_logit_model.csv')
# p4 = walk_bin(link, R)
# p4.to_csv('models/walk_binary_logit_model.csv')
p100 = ML_model(link, R)
p100.to_csv('models/mode_choice_ML_model.csv')
