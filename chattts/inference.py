import torch
import torchaudio
from chattts.core import Chat

chat = Chat()
chat.load(compile=True)

texts = ["""
你给我说说，这句要怎么念？你说啊！快说！听到没有？
"""]

wavs = chat.infer(texts)

for i in range(len(wavs)):
    """
    In some versions of torchaudio, the first line works but in other versions, so does the second line.
    """
    try:
        torchaudio.save(f"basic_output{i}.wav", torch.from_numpy(wavs[i]).unsqueeze(0), 24000)
    except:
        torchaudio.save(f"basic_output{i}.wav", torch.from_numpy(wavs[i]), 24000)
