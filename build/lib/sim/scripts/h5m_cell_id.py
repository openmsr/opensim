import sys
import pymoab as mb
from pymoab import core, types

def get_h5m_volumes(argv):
    mbcore = core.Core()
    mbcore.load_file(str(argv[0]))
    category_tag = mbcore.tag_get_handle(
        mb.types.CATEGORY_TAG_NAME)
    group_category = ["Group"]
    group_ents = mbcore.get_entities_by_type_and_tag(
        0, mb.types.MBENTITYSET, category_tag, group_category)

    name_tag = mbcore.tag_get_handle(
        mb.types.NAME_TAG_NAME)
    id_tag = mbcore.tag_get_handle(
        mb.types.GLOBAL_ID_TAG_NAME)
    volumes_list = []
    materials_list = []
    for group_ent in group_ents:
        group_name = mbcore.tag_get_data(name_tag, group_ent)[0][0]
        if group_name.startswith('mat:'):
            if group_name[4:]==argv[1]:
                vols = mbcore.get_entities_by_type(
                    group_ent, mb.types.MBENTITYSET)
                for vol in vols:
                    id = mbcore.tag_get_data(id_tag, vol)[0][0]
                    volumes_list.append(id.item())
    return(volumes_list)

if __name__ == "__main__":
    get_volume(sys.argv[1:])
