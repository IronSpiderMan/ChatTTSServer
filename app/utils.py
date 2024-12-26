import io
from typing import Optional

import soundfile as sf
import torch

from chattts.core import Chat


def _tts(chattts: Chat, text: str, speaker_filepath: Optional[str] = None):
    if speaker_filepath is not None:
        rand_spk = torch.load(speaker_filepath)
        params_infer_code = {
            'prompt': '[speed_5]',
            'temperature': .000003,
            'spk_emb': rand_spk,
        }
        params_infer_code = Chat.InferCodeParams(
            **params_infer_code,
        )
    else:
        params_infer_code = Chat.InferCodeParams()
    wavs = chattts.infer(text, use_decoder=True, params_infer_code=params_infer_code)
    buffer = io.BytesIO()
    sf.write(buffer, wavs[0], 24000, format="WAV")  # 保存为 WAV 格式
    buffer.seek(0)
    return buffer.read()
