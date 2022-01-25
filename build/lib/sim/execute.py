import os, sys
from .parser import parse_arg
from .set import def_model

def main(args):
    model = def_model(parse_arg())
    mats = model.set_mat()
    geom = model.set_geom(mats)
    tally = model.set_tally(mats)
    sett = model.set_setting()
    res = model.model_run(mats,geom,tally,sett)
    model.set_post(res)

args = sys.argv[1:]
main(args)
