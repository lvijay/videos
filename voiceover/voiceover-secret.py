#!/usr/bin/env python

import argparse
import html

from google.cloud import texttospeech_v1 as texttospeech

# from google.cloud.texttospeech_v1.types import ListVoicesRequest

MALE = texttospeech.SsmlVoiceGender.MALE
FEMALE = texttospeech.SsmlVoiceGender.FEMALE

PHILOSOPHER_VOICE = {
    "a": (  MALE, 0.8, "en-US-Standard-B", True),
    "b": (  MALE, 0.8, "en-US-News-N", True),
    "c": (FEMALE, 1.2, "en-US-Studio-O", True),
    "d": (  MALE, 0.8, "en-US-Wavenet-B", True),
    "e": (  MALE, 0.8, "en-US-Journey-D", False),
    "f": (  MALE, 0.8, "en-US-Neural2-A", False),
    "g": (  MALE, 0.8, "en-US-Wavenet-D", True),
    "h": (  MALE, 0.8, "en-US-Neural2-D", True),
    "i": (  MALE, 0.8, "en-US-Standard-J", True),
    "j": (  MALE, 0.8, "en-US-Studio-Q", True),
    "k": (  MALE, 0.8, "en-US-Wavenet-I", True),
    "l": (FEMALE, 1.2, "en-US-Neural2-F", True),
}


def get_voice(philosopher: str):
    name = philosopher[0].lower()
    return PHILOSOPHER_VOICE[name]


def to_ssml(content):
    return f"""
<speak>
  {content.replace("'", "&#x27;")}
</speak>
""".strip()


def get_parser():
    parser = argparse.ArgumentParser()

    parser.add_argument(
        "-p",
        "--philosopher",
        dest="philosopher",
        required=True,
        metavar="philosopher",
        help="""philosopher.
    
        For example, `-p c` uniquely identifies chomsky
        """,
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
        "-r",
        "--speaking-rate",
        dest="speaking_rate",
        type=float,
        default="1.2",
    )
    parser.add_argument(
        "-i",
        "--input",
        type=argparse.FileType("r"),
        default="-",
    )

    return parser


if __name__ == "__main__":
    args = get_parser().parse_args()
    gender, pitch, voicename, ssml_supported = get_voice(args.philosopher)
    voice = texttospeech.VoiceSelectionParams(
        language_code="en-US",
        name=voicename,
        ssml_gender=gender,
    )
    speech = args.input.read().strip()
    if ssml_supported:
        ssml = to_ssml(speech)
        print("ssml =", ssml)
        ssmlfileout = args.fileout.name + ".ssml"
        with open(ssmlfileout, "w") as ssmlout:
            print(ssml.strip(), file=ssmlout)
        synthesis_input = texttospeech.SynthesisInput(ssml=ssml)
    else:
        print("speech =", speech)
        spchfileout = args.fileout.name + ".txt"
        with open(spchfileout, "w") as spchout:
            print(speech.strip(), file=spchout)
        synthesis_input = texttospeech.SynthesisInput(text=speech)    
    audio_config = texttospeech.AudioConfig(
        audio_encoding=texttospeech.AudioEncoding.OGG_OPUS,
        pitch=pitch,
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
    print(f"{len(response.audio_content)=}")
    args.fileout.write(response.audio_content)

# voiceover-secret.py ends here
