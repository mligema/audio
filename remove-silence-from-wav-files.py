import os
from pydub import AudioSegment
import argparse

def detect_leading_silence(sound, silence_threshold=-50.0, chunk_size=10):
    '''
    sound is a pydub.AudioSegment
    silence_threshold in dB
    chunk_size in ms

    iterate over chunks until you find the first one with sound
    '''
    trim_ms = 0 # ms

    assert chunk_size > 0 # to avoid infinite loop
    while sound[trim_ms:trim_ms+chunk_size].dBFS < silence_threshold and trim_ms < len(sound):
        trim_ms += chunk_size

    return trim_ms


if __name__ == '__main__':

    parser = argparse.ArgumentParser(description='Trims a bunch of wav files. From directory: "wav" to a new directory "trimmed-wav"')
    parser.add_argument('--source', help='Relative path to the dir wavs are at. Default is "wavs"', default='wavs')
    parser.add_argument('--destination', help='Relative path to the dir you want your trimmed wavs to be in. Default will create a new dir called "trimmed-wavs"', default='trimmed-wavs')
    args = parser.parse_args()

    source_dir = args.source
    destination_dir = args.destination

    if not os.path.exists(destination_dir):
        os.makedirs(destination_dir)

    for file in os.listdir(source_dir):
        if file[-4:] != '.wav':
            continue
        current_file_path = os.path.join(source_dir, file)
        file_export_path = os.path.join(destination_dir, file)

        file_stats = os.stat(current_file_path)

        if file_stats.st_size is 0:
            continue

        sound = AudioSegment.from_file(current_file_path, format='wav')
        start_trim = detect_leading_silence(sound)
        end_trim = detect_leading_silence(sound.reverse())
        duration = len(sound)
        trimmed_sound = sound[start_trim:duration - end_trim]
        trimmed_sound.export(file_export_path, format='wav')


