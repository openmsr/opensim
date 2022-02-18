import os, sys
from .parser import parse_arg
from .set import def_model

def main(args=None):

    if args is None:
        args = sys.argv[1:]

    model = def_model(parse_arg())
    mats = model.set_mat()
    geom = model.set_geom(mats)
    tally = model.set_tally(mats)
    sett = model.set_setting()
    res = model.model_run(geom,mats,sett,tally)
    model.set_post(res)

    #save simulation arguments in a txt file
    with open('sim_args.txt', 'w') as f:
        f.write(str(parse_arg()))

if __name__ == "__main__":
    sys.exit(main())
