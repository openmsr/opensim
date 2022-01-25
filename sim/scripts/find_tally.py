import openmc

def find_tallies_by_name(sp,name):
    tallies_list=[]
    for id in sp.tallies:
        tally=sp.get_tally(id=id)
        if name in tally.name:
        #if tally.name.startswith(name):
            tallies_list.append(tally)
    return tallies_list
