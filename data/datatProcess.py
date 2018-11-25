# Import module
import os
import sys
import librosa
import glob


def process(source="sound", extension="wav", sample_rate=44100, length=1):

    # Make a path
    path = "./" + source + '/*.' + extension
    print(path)

    # Read every file in path
    files = glob.glob(path)
    print("Number of files: ", len(files))

    # Make a new directory
    destination_name = source + '_' + sample_rate + '_' + length + 's'
    if not(os.path.isfile(destination_name)):
        print("Direction is not exist")
        os.makedirs(os.path.join(destination_name))
    
    index = 0
    split_f = 0

    for fileNum in files[0:]:
        
        # Load Data
        raw, sample_rate = librosa.load(fileNum, sr=int(sample_rate))

        # Check size
        chunk = int(int(sample_rate) * float(length))
        print("Chunk size: ", chunk)

        file_size = len(raw)
        rest = file_size % int(chunk)
        file_size -= rest
        refine = raw[:file_size]

        # For Debugging
        print("Raw data Size: ", file_size)
        print("Sample Rate:", sample_rate)
        print("Refine data Len: ", len(refine))

        # Split the main sound
        split_f = 0
        for i in range(0, file_size,chunk):
            tmp = refine[i:i+chunk]
            librosa.output.write_wav(destination_name + '/' + str(split_f + index) + '.' + extension, tmp, sample_rate)
            split_f = split_f+1
        print("Finish split ", split_f)
        index = index + split_f

def main():
    process(sys.argv[1], sys.argv[2], sys.argv[3], sys.argv[4])


if __name__ == '__main__':
    main();
