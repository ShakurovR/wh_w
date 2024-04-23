import numpy as np
import subprocess
import re
def load_audio_stereo(file: str, channel: int, sr: int = 16000):
    # left = 0 / right = 1
    try:
        # Launches a subprocess to decode audio while down-mixing and resampling as necessary.
        # Requires the ffmpeg CLI to be installed.
        cmd = [
            "ffmpeg",
            "-nostdin",
            "-threads",
            "0",
            "-i",
            file,
            "-map_channel",
            f"0.0.{channel}",
            "-f",
            "s16le",
            "-ac",
            "1",
            "-acodec",
            "pcm_s16le",
            "-ar",
            str(sr),
            "-",
        ]
        out = subprocess.run(cmd, capture_output=True, check=True).stdout
    except subprocess.CalledProcessError as e:
        raise RuntimeError(f"Failed to load audio: {e.stderr.decode()}") from e

    return out


def segments_to_sent(tr_result, mark=None):
    for segment in tr_result["segments"]:
        seg_offset = 0
        durat = segment['end'] - segment["start"]
        length = len(segment["text"])
        for sent in re.split("\.|\?|\!",segment["text"]):
            if sent: yield (sent, segment["start"] + seg_offset, segment["start"] + durat*(len(sent)/length) + seg_offset, mark)
            seg_offset += durat*(len(sent)/length)