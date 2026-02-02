FROM runpod/worker-comfyui:5.7.1-base

RUN comfy-node-install \
    rgthree-comfy \
    comfyui-videohelpersuite \
    comfyui-kjnodes \
    comfyui-custom-scripts \
    comfyui-easy-use \
    comfyui-wan

RUN comfy --skip-prompt model download \
    --url https://huggingface.co/Comfy-Org/Wan_2.1_ComfyUI_repackaged/resolve/main/split_files/text_encoders/umt5_xxl_fp8_e4m3fn_scaled.safetensors \
    --relative-path models/text_encoders \
    --filename umt5_xxl_fp8_e4m3fn_scaled.safetensors

RUN comfy --skip-prompt model download \
    --url https://huggingface.co/Comfy-Org/Wan_2.1_ComfyUI_repackaged/resolve/main/split_files/vae/wan_2.1_vae.safetensors \
    --relative-path models/vae/Wan \
    --filename wan_2.1_vae.safetensors
