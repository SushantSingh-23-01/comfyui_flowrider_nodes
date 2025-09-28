import re

class ResolutionSelector:
    RESOLUTIONS = [
        "(1:1) - 512 x 512", "(1:1) - 768 x 768", "(1:1) - 1024 x 1024",
        "(3:4) - 640 x 960", "(3:4) - 768 x 1280", "(3:4) - 1024 x 1360",
        "(4:5) - 512 x 640", "(4:5) - 640 x 768", "(4:5) - 832 x 1024", "(4:5) - 1024 x 1280",
        "(9:16) - 512 x 912", "(9:16) - 640x1152", "(9:16) - 768x1344"
    ]
    @classmethod
    def INPUT_TYPES(cls):
        return {"required": {"resolution":  (cls.RESOLUTIONS, {"default": "(4:5) - 832 x 1024"})}}
    
    NAME = "flowrider_resolution_select"
    RETURN_TYPES = ("INT", "INT")
    RETURN_NAMES = ("width", "height")
    FUNCTION = "select_and_parse_resolution"
    CATEGORY = "Resolution"
    
    def select_and_parse_resolution(self, resolution:str = "(4:5) - 832 x 1024"):
        match_res = re.search(r'(\d+) x (\d+)', resolution, re.DOTALL)
        if match_res:
            return tuple(map(int, match_res.groups()))
        else:
            print('Warning: Invalid resoluiton. Defaulting to 512 x 512.')
            return (512, 512)

NODE_CLASS_MAPPINGS = {
    "SelectCustomResolutions": ResolutionSelector
}
NODE_DISPLAY_NAME_MAPPINGS = {
    "SaveCustomResolutions": "FlowRider Resolution Selector"
}