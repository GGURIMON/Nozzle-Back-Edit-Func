import edit_func

def image_edit(original_image_base64, mask_image_base64=None, prompt=None, task="INPAINTING"):
    if task == "BACKGROUND_REMOVAL":
        return edit_func.background_removal(original_image_base64)
    elif task == "IMAGE_CONDITIONING":
        return edit_func.image_conditioning(original_image_base64, prompt)
    elif task == "OUT_PAINTING":
        return edit_func.outpainting(original_image_base64, mask_image_base64, prompt)
    else:
        return edit_func.inpainting(original_image_base64, mask_image_base64, prompt)
