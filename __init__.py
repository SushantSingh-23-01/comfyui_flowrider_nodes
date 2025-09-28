from .save_img import NODE_CLASS_MAPPINGS as sv_img_maps
from .save_img import NODE_DISPLAY_NAME_MAPPINGS as sv_img_disp_maps

from .res_select import NODE_CLASS_MAPPINGS as rs_maps
from .res_select import NODE_DISPLAY_NAME_MAPPINGS as rs_disp_maps

from .film_grain_vfx import NODE_CLASS_MAPPINGS as fg_maps
from .film_grain_vfx import NODE_DISPLAY_NAME_MAPPINGS as fg_dis_maps

NODE_CLASS_MAPPINGS = {
    **sv_img_maps,
    **rs_maps,
    **fg_maps,
}

NODE_DISPLAY_MAPPINGS = {
    **sv_img_disp_maps,
    **rs_disp_maps,
    **fg_dis_maps
}