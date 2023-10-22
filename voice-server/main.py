import gradio
from dotenv import load_dotenv

load_dotenv()

from google.cloud import texttospeech
from google.cloud import speech

Speech2TextClient = speech.SpeechClient()
Text2SpeechClient = texttospeech.TextToSpeechClient()

speech_config = speech.RecognitionConfig(
    encoding=speech.RecognitionConfig.AudioEncoding.LINEAR16,
    sample_rate_hertz=24000,
    language_code="en-US",
    model="default",
    audio_channel_count=1,
    enable_word_confidence=True,
    enable_word_time_offsets=True,
)


audio_config = texttospeech.AudioConfig(
    audio_encoding=texttospeech.AudioEncoding.LINEAR16,  # Use LINEAR16 for WAV
    speaking_rate=1
)

# Note: the voice can also be specified by name.
# Names of voices can be retrieved with client.list_voices().
voice = texttospeech.VoiceSelectionParams(
    language_code="en-US",
    name="en-US-Studio-O",
)

def process_speech(audio_content):
    audio_content = audio_content[1].tobytes()

    audio = speech.RecognitionAudio(content = audio_content)
    operation = Speech2TextClient.long_running_recognize(config=speech_config, audio=audio)
    text_result = operation.result(timeout=90)

    #DO THE LLM PROCESS HERE 

    llm_text = text_result.results[0].alternatives[0].transcript
    print(llm_text)
    #END LLM PROCESS

    input_text = texttospeech.SynthesisInput(text = llm_text)

    response = Text2SpeechClient.synthesize_speech(
        request={"input": input_text, "voice": voice, "audio_config": audio_config}
    )

    return response.audio_content

    # The response's audio_content is binary.
    with open("output2.wav", "wb") as out:  # Change the file extension to ".wav"
        out.write(response.audio_content)
        print('Audio content written to file "output2.wav"')
    

iface = gradio.Interface(fn = process_speech, inputs="audio", outputs = "audio")
iface.launch(share = True)
