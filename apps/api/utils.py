import numpy as np
from dataclasses import dataclass
import torchaudio
import io

def load_audio(file: str, channel: int = None, sr: int = 16000):
    # left = 0 / right = 1
    try:
        a_channels, sample_rate = torchaudio.load(file)
        serialized_result = []
        for a_ch in a_channels:
            a_ch = torchaudio.functional.resample(a_ch, orig_freq=sample_rate, new_freq=sr)
            memfile = io.BytesIO()
            np.save(memfile, a_ch) 
            serialized_result.append(memfile.getvalue())
    except Exception as E:
        raise Exception(f"Failed to load audio: {E}")
    return serialized_result

@dataclass
class MySegment:
    start: float
    end: float = None
    text: str = ""
    speaker: str = None


def segments_to_sentences(multiple_segments, mark=None):
    init_f = True
    for segment in multiple_segments:
        for word in segment[10]:
            if(init_f):
                init_f = False
                buf_segment = MySegment(start=word[0], speaker=mark)
            buf_segment.text += word[2]
            if(word[2][-1] in (".","!","?","¿")):
                buf_segment.end = word[1]
                yield buf_segment
                init_f = True
        if not init_f:
            buf_segment.end = word[1]
            yield buf_segment
            init_f = True
