import torch
from PIL import Image
import numpy as np

def tensor2pil(image):
    return Image.fromarray(np.clip(255. * image.cpu().numpy().squeeze(), 0, 255).astype(np.uint8))

def pil2tensor(image):
    return torch.from_numpy(np.array(image).astype(np.float32) / 255.0).unsqueeze(0)

class EGCYQJBCJ:
    def __init__(self):
        pass

    @classmethod
    def INPUT_TYPES(s):
        return {"required": {
            "reference_image": ("IMAGE",),
            "image": ("IMAGE",),
            "mask": ("MASK",),
            "region_extension": ("INT", {"default": 50, "min": 0}),
            "partial_size": ("INT", {"default": 512, "min": 0, "max": 2048, "step": 1})
        }}

    RETURN_TYPES = ("IMAGE", "MASK")
    FUNCTION = "local_crop"
    CATEGORY = "2🐕sampler"

    def resize_to_reference(self, image_pil, reference_image_pil):
        return image_pil.resize(reference_image_pil.size, Image.LANCZOS)

    def local_crop(self, image, mask, reference_image, region_extension, partial_size):
        image_pil = tensor2pil(image)
        mask_pil = tensor2pil(mask)
        reference_image_pil = tensor2pil(reference_image)

        # Resize the input image and mask to match the reference image size
        image_pil = self.resize_to_reference(image_pil, reference_image_pil)
        mask_pil = self.resize_to_reference(mask_pil, reference_image_pil)

        mask_array = np.array(mask_pil) > 0
        coords = np.where(mask_array)

        if coords[0].size == 0 or coords[1].size == 0:
            return (pil2tensor(image_pil), pil2tensor(mask_pil))

        x0, y0, x1, y1 = coords[1].min(), coords[0].min(), coords[1].max(), coords[0].max()
        x0 -= region_extension
        y0 -= region_extension
        x1 += region_extension
        y1 += region_extension
        x0 = max(x0, 0)
        y0 = max(y0, 0)
        x1 = min(x1, image_pil.width)
        y1 = min(y1, image_pil.height)

        cropped_image_pil = image_pil.crop((x0, y0, x1, y1))
        cropped_mask_pil = mask_pil.crop((x0, y0, x1, y1))

        if partial_size > 0:
            min_size = min(cropped_image_pil.size)
            if min_size < partial_size or min_size > partial_size:
                scale_ratio = partial_size / min_size
                new_size = (int(cropped_image_pil.width * scale_ratio), int(cropped_image_pil.height * scale_ratio))
                cropped_image_pil = cropped_image_pil.resize(new_size, Image.LANCZOS)
                cropped_mask_pil = cropped_mask_pil.resize(new_size, Image.LANCZOS)

        cropped_image_tensor = pil2tensor(cropped_image_pil)
        cropped_mask_tensor = pil2tensor(cropped_mask_pil)

        return (cropped_image_tensor, cropped_mask_tensor)

NODE_CLASS_MAPPINGS = {
    "EGCYQJBCJ": EGCYQJBCJ
}

NODE_DISPLAY_NAME_MAPPINGS = {
    "EGCYQJBCJ": "2🐕Local Image"
}
