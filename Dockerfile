FROM runpod/worker-comfyui:5.7.1-base

RUN comfy-node-install \
    rgthree-comfy \
    comfyui-videohelpersuite \
    comfyui-kjnodes

ARG CIVITAI_TOKEN

RUN comfy --skip-prompt model download --set-civitai-api-token ${CIVITAI_TOKEN} && \
    comfy --skip-prompt model download \
        --url https://civitai.com/api/download/models/2555640 \
        --relative-path models/diffusion_models \
        --filename DasiwaWAN22I2V14BLightspeed_synthseductionHighV9.safetensors && \
    comfy --skip-prompt model download \
        --url https://civitai.com/api/download/models/2555652 \
        --relative-path models/diffusion_models \
        --filename DasiwaWAN22I2V14BLightspeed_synthseductionLowV9.safetensors

RUN comfy --skip-prompt model download \
    --url https://huggingface.co/Comfy-Org/Wan_2.1_ComfyUI_repackaged/resolve/main/split_files/text_encoders/umt5_xxl_fp8_e4m3fn_scaled.safetensors \
    --relative-path models/text_encoders \
    --filename umt5_xxl_fp8_e4m3fn_scaled.safetensors

RUN comfy --skip-prompt model download \
    --url https://huggingface.co/Comfy-Org/Wan_2.1_ComfyUI_repackaged/resolve/main/split_files/vae/wan_2.1_vae.safetensors \
    --relative-path models/vae/Wan \
    --filename wan_2.1_vae.safetensors
