import numpy as np
import scipy
import matplotlib.colors
import torch

class FilmGrainVFX:
    @classmethod
    def INPUT_TYPES(cls):
        return {
            "required": {
                "images": ("IMAGE", ),
                "grain_strength": ("FLOAT", {"default": 0.02, "min": 0.001, "max": 0.2, "step": 0.001}),
                "kernel_size": ("INT", {"default": 3, "min": 3, "max": 9, "step": 2}),
                "color_tint": ("COLOR", {"default": "#FFFFFF"}) 
            },
            "optional": {
                "seed":  ("INT", {"default": 0, "min": 0, "max": 0xffffffffffffffff}),
            }
        }
        
    NAME = "filmrider_filmgrain_Vfx"
    RETURN_TYPES = ("IMAGE",)
    FUNCTION = "apply_grain"
    CATEGORY = "VFX/Film"
    OUTPUT_NODE = False
    
    def apply_grain(self, images, grain_strength=0.02, kernel_size=3, color_tint='#FFFFFF', seed=0):
        processed_images = []
        rng = np.random.default_rng(seed)
        color_tint_rgb_norm = matplotlib.colors.to_rgb(color_tint)
        color_tint_array = np.array(color_tint_rgb_norm).reshape(1, 1, 3)
        for image_tensor in images:
            i_np = image_tensor.cpu().numpy()
            height, width, channels = i_np.shape
            
            # Main idea: add film grain depending upon intensity of pixel (rather than uniformly)
            # Generate base noise based on a Standard Gaussian distribution
            noise_base = rng.normal(0, 1.0, (height, width))
            
            # Create a simple box blur kernel to simulate frequency-based noise clustering
            kernel = np.ones((kernel_size, kernel_size), dtype=np.float32) / (kernel_size**2)
            
            # Apply the blur using convolution
            blurred_noise_array = scipy.signal.convolve2d(noise_base, kernel, mode='same', boundary='symm')
            
            # Scale the noise by the grain strength
            scaled_noise = blurred_noise_array * grain_strength
            # stack noise for 3 channels
            grain_noise_base = np.stack([scaled_noise]*3, axis=-1)
            # Add a subtle color tint to the noise
            grain_noise = grain_noise_base * color_tint_array
            
            # calculate luminance for each pixel
            luminance = (0.299 * i_np[:, :, 0] + 0.587 * i_np[:, :, 1] + 0.114 * i_np[:, :, 2])
            # Invert the luminance so darker areas get more grain
            # ensure mask is not negative
            grain_mask = np.maximum(1 - luminance, 0.0)
            
            # Apply the grain, weighted by the luminance mask
            # We broadcast the grain_mask to all three color channels
            grained_img_array = i_np + grain_noise * grain_mask[:, :, np.newaxis]
            
            # Clip values and convert back to 0-255 range and uint8 type
            grained_img_array = np.clip(grained_img_array, 0, 1)
            processed_tensor = torch.from_numpy(grained_img_array).float()
            processed_images.append(processed_tensor)
            
        batched_images = torch.cat(processed_images, dim=0)
        return (batched_images,)

NODE_CLASS_MAPPINGS = {
    "FilmGrainVFX": FilmGrainVFX
}
NODE_DISPLAY_NAME_MAPPINGS = {
    "FilmGrainVFX": "FlowRider FilmGrainVFX"
}