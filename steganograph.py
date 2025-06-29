from PIL import Image
import wave
import struct

def encode_image(image_path, message):
    image = Image.open(image_path)
    pixels = image.load()

    binary_message = ''.join(format(ord(char), '08b') for char in message)
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

    image.save('encoded_image.png')

def decode_image(image_path):
    image = Image.open(image_path)
    pixels = image.load()

    binary_message = ''
    for y in range(image.height):
        for x in range(image.width):
            r, g, b = pixels[x, y]
            binary_message += str(r & 1) + str(g & 1) + str(b & 1)

    message = ''
    for i in range(0, len(binary_message), 8):
        byte = binary_message[i:i + 8]
        if byte == '00000000':  # Stop on null terminator (optional)
            break
        try:
            message += chr(int(byte, 2))
        except ValueError:
            break

    return message

def encode_audio(audio_path, message):
    audio = wave.open(audio_path, 'rb')
    params = audio.getparams()
    frames = audio.readframes(params.nframes)

    binary_message = ''.join(format(ord(char), '08b') for char in message)

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

    encoded_audio = wave.open('encoded_audio.wav', 'wb')
    encoded_audio.setparams(params)
    encoded_audio.writeframes(struct.pack('h' * params.nchannels * len(encoded_frames), *sum(encoded_frames, [])))
    encoded_audio.close()

def decode_audio(audio_path):
    audio = wave.open(audio_path, 'rb')
    params = audio.getparams()
    frames = audio.readframes(params.nframes)

    binary_message = ''
    for frame in struct.iter_unpack('h' * params.nchannels, frames):
        for sample in frame:
            binary_message += str(sample & 1)

    message = ''
    for i in range(0, len(binary_message), 8):
        byte = binary_message[i:i + 8]
        if byte == '00000000':
            break
        try:
            message += chr(int(byte, 2))
        except ValueError:
            break

    return message

def main():
    # Get user input
    image_path = input("Enter image file path (e.g., image.png): ").strip()
    audio_path = input("Enter audio file path (e.g., audio.wav): ").strip()
    message = input("Enter the secret message to encode: ")

    # Encode and decode image
    encode_image(image_path, message)
    decoded_img_msg = decode_image('encoded_image.png')
    print("✅ Decoded message from image:", decoded_img_msg)

    # Encode and decode audio
    encode_audio(audio_path, message)
    decoded_audio_msg = decode_audio('encoded_audio.wav')
    print("✅ Decoded message from audio:", decoded_audio_msg)

if __name__ == "__main__":
    main()
