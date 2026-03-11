import numpy as np
from transformers import pipeline
import soundfile as sf
import sounddevice as sd

pipe = pipeline("text-to-speech", model="facebook/mms-tts-ell", device="cpu")

def text_to_speech(text: str, output_path: str ="output.wav", model: callable = pipe):

    # to audio
    result = model(text)

    # squeeze to 1-dim
    output_audio = np.ravel(result["audio"])

    # write to file and read it via speakers
    sf.write("output", output_audio, result["sampling_rate"], format="MP3")
    sd.play(output_audio, result["sampling_rate"])
    sd.wait()  # Wait until audio finishes
    print(f"✅ Greek speech saved to: {output_path}")

if __name__ == '__main__':
    text_to_speech("Οἱ δὲ Φοίνιϰες οὗτοι οἱ σὺν Κάδμῳ ἀπιϰόμενοι.. ἐσήγαγον διδασϰάλια ἐς τοὺς ῞Ελληνας ϰαὶ δὴ ϰαὶ γράμματα, οὐϰ ἐόντα πρὶν")