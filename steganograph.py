from PIL import Image
import wave
import struct
import random

def encode_image(image_path, message):
    # Open the image file
    image = Image.open(image_path)
    pixels = image.load()

    # Convert the message to binary
    binary_message = ''.join(format(ord(char), '08b') for char in message)

    # Encode the message in the image
    index = 0
    for y in range(image.height):
        for x in range(image.width):
            if index < len(binary_message):
                r, g, b = pixels[x, y]
                r_bit = binary_message[index]
                g_bit = binary_message[index + 1] if index + 1 < len(binary_message) else '0'
                b_bit = binary_message[index + 2] if index + 2 < len(binary_message) else '0'
                pixels[x, y] = (r & ~1 | int(r_bit), g & ~1 | int(g_bit), b & ~1 | int(b_bit))
                index += 3
            else:
                break

    # Save the modified image
    image.save('encoded_image.png')

def decode_image(image_path):
    # Open the encoded image
    image = Image.open(image_path)
    pixels = image.load()

    # Decode the message from the image
    binary_message = ''
    for y in range(image.height):
        for x in range(image.width):
            r, g, b = pixels[x, y]
            binary_message += str(r & 1) + str(g & 1) + str(b & 1)

    # Convert the binary message back to text
    message = ''
    for i in range(0, len(binary_message), 8):
        byte = binary_message[i:i + 8]
        message += chr(int(byte, 2))

    return message

def encode_audio(audio_path, message):
    # Open the audio file
    audio = wave.open(audio_path, 'rb')
    params = audio.getparams()
    frames = audio.readframes(params.nframes)

    # Convert the message to binary
    binary_message = ''.join(format(ord(char), '08b') for char in message)

    # Encode the message in the audio frames
    encoded_frames = []
    index = 0
    for frame in struct.iter_unpack('h' * params.nchannels, frames):
        encoded_frame = []
        for sample in frame:
            if index < len(binary_message):
                encoded_sample = sample & ~1 | int(binary_message[index])
                encoded_frame.append(encoded_sample)
                index += 1
            else:
                encoded_frame.append(sample)
        encoded_frames.append(encoded_frame)

    # Save the modified audio file
    encoded_audio = wave.open('encoded_audio.wav', 'wb')
    encoded_audio.setparams(params)
    encoded_audio.writeframes(struct.pack('h' * params.nchannels * len(encoded_frames), *sum(encoded_frames, [])))
    encoded_audio.close()

def decode_audio(audio_path):
    # Open the encoded audio file
    audio = wave.open(audio_path, 'rb')
    params = audio.getparams()
    frames = audio.readframes(params.nframes)

    # Decode the message from the audio frames
    binary_message = ''
    for frame in struct.iter_unpack('h' * params.nchannels, frames):
        for sample in frame:
            binary_message += str(sample & 1)

    # Convert the binary message back to text
    message = ''
    for i in range(0, len(binary_message), 8):
        byte = binary_message[i:i + 8]
        message += chr(int(byte, 2))

    return message

def main():
    # Encode a message in an image
    encode_image('image.png', 'This is a secret message.')
    decoded_message = decode_image('encoded_image.png')
    print("Decoded message from image:", decoded_message)

    # Encode a message in an audio file
    encode_audio('audio.wav', 'This is a secret message in audio.')
    decoded_message = decode_audio('encoded_audio.wav')
    print("Decoded message from audio:", decoded_message)

if __name__ == "__main__":
    main()