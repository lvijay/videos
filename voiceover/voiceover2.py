#!/usr/bin/env python

import argparse

from google.cloud import texttospeech_v1 as texttospeech

# from google.cloud.texttospeech_v1.types import ListVoicesRequest

MALE = texttospeech.SsmlVoiceGender.MALE
FEMALE = texttospeech.SsmlVoiceGender.FEMALE
CORPUS_NAMES = """
en-US-Journey-D male
en-US-Journey-F female
en-US-Neural2-A male
en-US-Neural2-C female
en-US-Neural2-D male
en-US-Neural2-E female
en-US-Neural2-F female
en-US-Neural2-G female
en-US-Neural2-H female
en-US-Neural2-I male
en-US-Neural2-J male
en-US-News-K female
en-US-News-L female
en-US-News-N male
en-US-Polyglot-1 male
en-US-Standard-A male
en-US-Standard-B male
en-US-Standard-C female
en-US-Standard-D male
en-US-Standard-E female
en-US-Standard-F female
en-US-Standard-G female
en-US-Standard-H female
en-US-Standard-I male
en-US-Standard-J male
en-US-Studio-O female
en-US-Studio-Q male
en-US-Wavenet-A male
en-US-Wavenet-B male
en-US-Wavenet-C female
en-US-Wavenet-D male
en-US-Wavenet-E female
en-US-Wavenet-F female
en-US-Wavenet-G female
en-US-Wavenet-H female
en-US-Wavenet-I male
en-US-Wavenet-J male
""".strip().split(
    "\n"
)


NAMES = [
    (v[0], MALE if v[1] == "male" else FEMALE)
    for line in CORPUS_NAMES
    if len(v := line.split()) == 2
]


def match_names(nameparts, allnames):
    return [
        (n, g)
        for n, g in allnames
        if all(np.lower() in n.lower() for np in nameparts)
    ]


def get_parser():
    parser = argparse.ArgumentParser()

    parser.add_argument(
        "-v",
        "--voice-name",
        dest="voicename",
        nargs="+",
        required=True,
        metavar="VOICE",
        help="""voice name.  can be specified in multiple words.

        For example, `-v stu q` uniquely identifies \033[1men-US-Studio-Q\033[0m.
        """,
    )
    parser.add_argument(
        "-g",
        "--gender",
        default="male",
        help="'male' or 'female'",
        type=lambda v: MALE if v.lower() == "male" else FEMALE,
    )
    parser.add_argument(
        "-o",
        "--out",
        action="store",
        dest="fileout",
        default="-",
        type=argparse.FileType("wb", 0),
        help="file to write to.",
    )
    parser.add_argument(
        "-i",
        "--input",
        type=argparse.FileType("r"),
        default="-",
    )
    parser.add_argument(
        "-r",
        "--speaking-rate",
        dest="speaking_rate",
        type=float,
        default="1.0",
    )
    parser.add_argument(
        "-p",
        "--pitch",
        type=float,
        required=False,
    )
    parser.add_argument(
        "-s",
        "--ssml",
        type=argparse.FileType("r"),
        default=None
    )

    return parser


if __name__ == "__main__":
    args = get_parser().parse_args()
    voices = match_names(args.voicename, NAMES)
    if len(voices) == 1:
        voicename, gender = voices[0]
    elif len(voices) > 1:
        voicename, gender = [(n,g) for n,g in voices if g==args.gender][0]
    else:
        raise ValueError(f"Voice not found with {args.voicename}")
    voice = texttospeech.VoiceSelectionParams(
        language_code="en-US",
        name=voicename,
        ssml_gender=gender,
    )
    if args.ssml:
        content = args.ssml.read().strip()
        synthesis_input = texttospeech.SynthesisInput(ssml=content)
    else:
        content = args.input.read().strip()
        synthesis_input = texttospeech.SynthesisInput(text=content)
    audio_config = texttospeech.AudioConfig(
        audio_encoding=texttospeech.AudioEncoding.OGG_OPUS,
        pitch=args.pitch,
        speaking_rate=args.speaking_rate,
    )

    client = texttospeech.TextToSpeechClient()
    response = client.synthesize_speech(
        request={
            "input": synthesis_input,
            "voice": voice,
            "audio_config": audio_config,
        }
    )
    args.fileout.write(response.audio_content)

# voiceover2.py ends here
