import os
import numpy as np
from PIL import Image
from datetime import datetime

class SaveImageCustom:
    @classmethod
    def INPUT_TYPES(cls):
        return {
            "required": {
                "images": ("IMAGE", ),
                "quality": ("INT", {"default": 95, "min": 1, "max": 100, "step": 1}),
                "name_prefix": ("STRING", {"default": "Image", "multiline": False, "placeholder": "Saved image prefix, e.g. my_image"}),
                "output_dir": ("STRING", {"default": "output\\custom_saves", "comfyui_type": "path", "placeholder": "e.g., /path/to/my/saves", "multiline": False,})
            },
        }
    
    RETURN_TYPES = ()
    NAME = "flowrider_img_saver"
    OUTPUT_NODE = True
    CATEGORY = "image/save"
    
    def save_img_jpeg(self, images, quality=95, name_prefix="Image", output_dir="output\\custom_saves"):
        if images is None or images.shape[0] == 0:
            print("Warning: No images recieved by save-node.")
            return {"ui": {}}
        
        output_dir = output_dir.strip()
        custom_path = os.path.abspath(output_dir.strip())
        
        os.makedirs(custom_path, exist_ok=True)
        
        time_postfix = datetime.now().strftime("%Y_%m_%d_%H%M%S")
        
        for i, image_tensor in enumerate(images):
            i_np = 255 * image_tensor.cpu().numpy()
            img_pil = Image.fromarray(np.clip(i_np, 0, 255).astype(np.uint8))
            
            file_name = f"{name_prefix}_{time_postfix}_{i:02}.jpg"
            complete_file_path = os.path.join(custom_path, file_name)
            
            img_pil.save(complete_file_path, quality=quality, subsampling=0)
            print(f'Info: Saved Image to: {complete_file_path}')

NODE_CLASS_MAPPINGS = {
    "SaveImageCustom": SaveImageCustom
}
NODE_DISPLAY_NAME_MAPPINGS = {
    "SaveImageCustom": "FlowRider Image Saver"
}