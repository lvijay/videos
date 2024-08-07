# mkdir text-to-speech-python && touch text-to-speech-python/app.py

# export PROJECT_ID=turing-course-411109
# export GOOGLE_APPLICATION_CREDENTIALS=text-to-speech-key.json
# pip3 install --upgrade google-cloud-texttospeech

"""Synthesizes speech from the input string of text or ssml.
Make sure to be working in a virtual environment.

Note: ssml must be well-formed according to:
    https://www.w3.org/TR/speech-synthesis/
"""
from google.cloud import texttospeech


def list_voices(client):
    return client.list_voices()


def synthesize_text(client, text, voice, speaking_rate=1.0f, pitch=None):
    """Synthesizes speech from the input string of text."""
    input_text = texttospeech.SynthesisInput(text=text)
    audio_config = texttospeech.AudioConfig(
        audio_encoding=texttospeech.AudioEncoding.OGG_OPUS,
        speaking_rate=speaking_rate,
        pitch=pitch,
    )
    return client.synthesize_speech(
        request={"input": input_text, "voice": voice, "audio_config": audio_config}
    )


if __name__ == "__main__":
    import sys

    client = texttospeech.TextToSpeechClient()

    # Set the text input to be synthesized
    synthesis_input = texttospeech.SynthesisInput(text=' '.join(sys.argv[1:]))
    #voices = client.list_voices()

    #wavevoices = [
    #    texttospeech.VoiceSelectionParams(
    #        language_code=v.language_codes[0],
    #        name=v.name,
    #        ssml_gender=v.ssml_gender
    #    )
    #    for v in voices.voices
    #    if 'en-US-Wavenet-E' in v.name
    #    or 'en-US-Wavenet-G' in v.name
    #]

    voice = texttospeech.VoiceSelectionParams(
            language_code="en-US",
            name="en-US-Wavenet-E",
            ssml_gender=texttospeech.SsmlVoiceGender.FEMALE
        )

    # Select the type of audio file you want returned
    audio_config = texttospeech.AudioConfig(
        audio_encoding=texttospeech.AudioEncoding.MP3
    )

    response = client.synthesize_speech(
        request={
            'input': synthesis_input,
            'voice': voice,
            'audio_config': audio_config
        }
    )

    # The response's audio_content is binary.
    outfilename = f"output_{voice.name}.mp3"
    with open(outfilename, "wb") as out:
        out.write(response.audio_content)
        print(f'Audio content written to file "{outfilename}"')


# voiceover.py ends here

#texttospeech.VoiceSelectionParams(
#        language_code="en-US",
#        name="en-US-Standard-C",
#        ssml_gender=texttospeech.SsmlVoiceGender.FEMALE,
#    )
#
#
#for v in voices:
#  voic = texttospeech.VoiceSelectionParams(
#      language_code=v.language_codes[0],
#      name=v.name,
#      ssml_gender=ssml_gender)
#  response = client.synthesize_speech(
#    request={
#      'input': synthesis_input, 'voice': voic, 'audio_config': audio_config})
#  with open(f"output_{v.name}.ogg", "wb") as out:
#    out.write(response.audio_content)
#
