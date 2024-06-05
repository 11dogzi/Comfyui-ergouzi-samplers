import torch
import numpy as np
import comfy.sample
import comfy.utils
import latent_preview


class EGBYZZCYQ:

    @classmethod
    def INPUT_TYPES(s):
        return {
            "required": {
                "model": ("MODEL",),
                "seed": ("INT", {"default": 0, "min": 0, "max": 0xffffffffffffffff}),
                "steps": ("INT", {"default": 20, "min": 1, "max": 10000}),
                "cfg": ("FLOAT", {"default": 8.0, "min": 0.0, "max": 100.0, "step": 0.1, "round": 0.01}),
                "sampler_name": (comfy.samplers.KSampler.SAMPLERS,),
                "scheduler": (comfy.samplers.KSampler.SCHEDULERS,),
                "positive": ("CONDITIONING",),
                "negative": ("CONDITIONING",),
                "latent_image": ("LATENT",),
                "denoise": ("FLOAT", {"default": 1.0, "min": 0.0, "max": 1.0, "step": 0.01}),
                "variation_seed": ("INT", {"default": 0, "min": 0, "max": 0xffffffffffffffff}),
                "variation_strength": ("FLOAT", {"default": 0.0, "min": 0.0, "max": 1.0, "step": 0.01}),
                "variation_width": ("INT", {"default": 0, "min": 0, "max": 512}),
                "variation_height": ("INT", {"default": 0, "min": 0, "max": 512}),
                "device": (["GPU", "CPU"], {"default": "CPU"}),
            }
        }

    RETURN_TYPES = ("LATENT",)
    FUNCTION = "sample"
    CATEGORY = "2🐕sampler"

    def sample(self, model, seed, steps, cfg, sampler_name, scheduler, positive, negative, latent_image, denoise=1.0,
               variation_seed=0, variation_strength=0.0, variation_width=0, variation_height=0, device="GPU"):
        return self.common_ksampler(model, seed, steps, cfg, sampler_name, scheduler, positive, negative, latent_image,
                                    denoise, variation_seed, variation_strength, variation_width, variation_height,
                                    device)

    def common_ksampler(self, model, seed, steps, cfg, sampler_name, scheduler, positive, negative, latent, denoise=1.0,
                        variation_seed=0, variation_strength=0.0, variation_width=0, variation_height=0, device="GPU",
                        disable_noise=False, start_step=None, last_step=None, force_full_denoise=False):
        latent_image = latent["samples"]
        if disable_noise:
            noise = torch.zeros(latent_image.size(), dtype=latent_image.dtype, layout=latent_image.layout, device="cpu")
        else:
            batch_inds = latent["batch_index"] if "batch_index" in latent else None
            noise = self.prepare_noise(latent_image, seed, variation_seed, variation_strength, variation_width,
                                       variation_height, device, batch_inds)

        noise_mask = None
        if "noise_mask" in latent:
            noise_mask = latent["noise_mask"]

        callback = latent_preview.prepare_callback(model, steps)
        disable_pbar = not comfy.utils.PROGRESS_BAR_ENABLED
        samples = comfy.sample.sample(model, noise, steps, cfg, sampler_name, scheduler, positive, negative,
                                      latent_image,
                                      denoise=denoise, disable_noise=disable_noise, start_step=start_step,
                                      last_step=last_step,
                                      force_full_denoise=force_full_denoise, noise_mask=noise_mask, callback=callback,
                                      disable_pbar=disable_pbar, seed=seed)
        out = latent.copy()
        out["samples"] = samples
        return (out,)

    def prepare_noise(self, latent_image, seed, variation_seed, variation_strength, variation_width, variation_height,
                      device, noise_inds=None):
        device = "cuda" if device == "GPU" and torch.cuda.is_available() else "cpu"
        base_generator = torch.Generator(device=device).manual_seed(seed)
        base_noise = torch.randn(latent_image.size(), dtype=latent_image.dtype, layout=latent_image.layout,
                                 generator=base_generator, device=device)

        if variation_strength > 0:
            variation_generator = torch.Generator(device=device).manual_seed(variation_seed)
            variation_noise = torch.randn(latent_image.size(), dtype=latent_image.dtype, layout=latent_image.layout,
                                          generator=variation_generator, device=device)

            # Calculate the center region to apply the variation
            width, height = latent_image.shape[-1], latent_image.shape[-2]
            v_width = min(max(variation_width, 0), width)
            v_height = min(max(variation_height, 0), height)
            v_width = min(v_width, width)  # Ensure does not exceed latent width
            v_height = min(v_height, height)  # Ensure does not exceed latent height
            v_width = (v_width // 8) * 8  # Ensure multiple of 8
            v_height = (v_height // 8) * 8  # Ensure multiple of 8

            start_x = (width - v_width) // 2
            start_y = (height - v_height) // 2

            combined_noise = base_noise.clone()
            if v_width > 0 and v_height > 0:
                combined_noise[..., start_y:start_y + v_height, start_x:start_x + v_width] = \
                    (1 - variation_strength) * base_noise[..., start_y:start_y + v_height, start_x:start_x + v_width] + \
                    variation_strength * variation_noise[..., start_y:start_y + v_height, start_x:start_x + v_width]
        else:
            combined_noise = base_noise

        if noise_inds is not None:
            unique_inds, inverse = np.unique(noise_inds, return_inverse=True)
            noises = []
            for i in range(unique_inds[-1] + 1):
                single_base_noise = combined_noise[0].unsqueeze(0)
                noises.append(single_base_noise)
            combined_noise = torch.cat([noises[i] for i in inverse], axis=0)

        return combined_noise
