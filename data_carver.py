import os
import hashlib


# Function defined for hashing the contents of the files
# It appends hash value to the hashes.txt file
def hash_file(subdata):
    hash_temp = hashlib.md5(subdata).hexdigest()
    os.chdir('./Shetty/')
    with open('hashes.txt', 'a') as the_file:
        the_file.write(hash_temp+'\n')
    os.chdir('../')
    return ()


def write_file(SOF_list, EOF_list, file_type):
    # Function defined for carving files with SOF and EOF offsets
    if not os.path.exists('./Shetty/'+'FileType_'+file_type):
        os.makedirs('./Shetty/'+'FileType_'+file_type)
    # Checking if the directory exists with the name as Last Name
    file_obj = open(file_name, 'rb')
    data = file_obj.read()
    file_obj.close()
    for sof in range(len(SOF_list)):
        i = 1
        for eof in range(len(EOF_list)):
            if EOF_list[eof] >= SOF_list[sof]:
                # Listing EOF and SOF pairs such that EOF is greater than SOF
                if EOF_list[eof] - SOF_list[sof] <= 2097152:
                    # Carving only files which are lesser than 2 MB
                    subdata = data[SOF_list[sof]:EOF_list[eof]]
                    carve_filename = "File_" + str(SOF_list[sof]) + "_" + str(EOF_list[eof]) + "."+file_type
                    os.chdir('./Shetty/'+'FileType_'+file_type)
                    # Carving the file
                    carve_obj = open(carve_filename, 'wb')
                    carve_obj.write(subdata)
                    carve_obj.close()
                    # Coming back to the home directory
                    os.chdir('../')
                    os.chdir('../')
                    hash_file(subdata)
                    print("Found an file and carving it to " + carve_filename)
                    print('File Size: '+str(len(subdata))+' bytes')
                    print('FileType: '+file_type)
                    print('Location Offset: '+str(SOF_list[sof])+'\n')
                    i = i - 1
                try:
                    if EOF_list[eof] > SOF_list[sof + 1]:
                        # Carving Embedded files
                        subdata1 = data[SOF_list[sof]:SOF_list[sof+1]]
                        subdata2 = data[EOF_list[eof]:EOF_list[eof+1]]
                        subdata = subdata1 + subdata2
                        carve_filename = "File_" + str(SOF_list[sof]) + "_" + str(EOF_list[eof + 1]) + "."+file_type
                        os.chdir('./Shetty/' + 'FileType_' + file_type)
                        carve_obj = open(carve_filename, 'wb')
                        carve_obj.write(subdata)
                        carve_obj.close()
                        os.chdir('../')
                        os.chdir('../')
                        hash_file(subdata)
                        print("Found an image and carving it to " + carve_filename)
                        print('File Size: ' + str(len(subdata)) + ' bytes')
                        print('FileType: ' + file_type)
                        print('Location Offset: ' + str(SOF_list[sof]) + '\n')
                except IndexError:
                    pass
            if i == 0:
                break


# Defining Function for carving jpg
def jpg(file_name, file_type):
    file_obj = open(file_name, 'rb')
    data = file_obj.read()
    file_obj.close()
    i = 0
    SOF_list = []
    EOF_list = []
    with open(file_name, "rb") as f:
        byte = f.read(1)
        # reading bytes one by one inside while loop
        while byte:
            byte = f.read(1)
            i = i + 1
            # Do stuff with byte.
            if byte == b'\xFF':
                jpg_check = data[i:i+2]
                # matching SOF sequence
                if jpg_check == b'\xFF\xD8':
                    SOF_list.append(i)
                # matching EOF sequence
                elif jpg_check == b'\xFF\xD9':
                    EOF_list.append(i+2)
    write_file(SOF_list, EOF_list, file_type)
    # Calling function for writing the file
    return()


# Defining Function for carving png
def png(file_name, file_type):
    file_obj = open(file_name, 'rb')
    data = file_obj.read()
    file_obj.close()
    i = 0
    SOF_list = []
    EOF_list = []
    with open(file_name, "rb") as f:
        byte = f.read(1)
        while byte:
            byte = f.read(1)
            i = i + 1
            # Do stuff with byte.
            if byte == b'\x89':
                png_sof = data[i:i+8]
                if png_sof == b'\x89\x50\x4E\x47\x0D\x0A\x1A\x0A':
                    SOF_list.append(i)
            elif byte == b'\x49':
                png_eof = data[i:i+8]
                if png_eof == b'\x49\x45\x4E\x44\xAE\x42\x60\x82':
                    EOF_list.append(i+8)
    write_file(SOF_list, EOF_list, file_type)
    return()


# Defining Function for carving pdf
def pdf(file_name, file_type):
    file_obj = open(file_name, 'rb')
    data = file_obj.read()
    file_obj.close()
    i = 0
    SOF_list = []
    EOF_list = []
    with open(file_name, "rb") as f:
        byte = f.read(1)
        while byte:
            byte = f.read(1)
            i = i + 1
            # Do stuff with byte.
            if byte == b'\x25':
                png_sof = data[i:i+4]
                if png_sof == b'\x25\x50\x44\x46':
                    SOF_list.append(i)
            if byte == b'\x0A':
                png_eof = data[i:i+7]
                if png_eof == b'\x0A\x25\x25\x45\x4F\x46\x0A':
                    EOF_list.append(i+7)
            if byte == b'\x0D':
                png_eof = data[i:i+9]
                if png_eof == b'\x0D\x0A\x25\x25\x45\x4F\x46\x0D\x0A':
                    EOF_list.append(i+9)
    write_file(SOF_list, EOF_list, file_type)
    return()


# Defining Function for carving docx
def docx(file_name, file_type):
    file_obj = open(file_name, 'rb')
    data = file_obj.read()
    file_obj.close()
    i = 0
    SOF_list = []
    EOF_list = []
    with open(file_name, "rb") as f:
        byte = f.read(1)
        while byte:
            byte = f.read(1)
            i = i + 1
            # Do stuff with byte.
            if byte == b'\x50':
                png_sof = data[i:i+8]
                if png_sof == b'\x50\x4B\x03\x04\x14\x00\x06\x00':
                    SOF_list.append(i)
                png_eof = data[i:i+4]
                if png_eof == b'\x50\x4B\x05\x06':
                    EOF_list.append(i+22)
    write_file(SOF_list, EOF_list, file_type)
    return()


# Defining Function for carving jpeg
def jpeg(file_name, file_type):
    file_obj = open(file_name, 'rb')
    data = file_obj.read()
    file_obj.close()
    i = 0
    SOF_list = []
    EOF_list = []
    with open(file_name, "rb") as f:
        byte = f.read(1)
        while byte:
            byte = f.read(1)
            i = i + 1
            # Do stuff with byte.
            if byte == b'\xFF':
                jpg_check = data[i:i+4]
                if jpg_check == b'\xFF\xD8\xFF\xE0':
                    SOF_list.append(i)
            if byte == b'\xFF':
                jpg_check1 = data[i:i+2]
                if jpg_check1 == b'\xFF\xD9':
                    EOF_list.append(i+2)
    write_file(SOF_list, EOF_list, file_type)
    return()


if __name__ == "__main__":
    file_name = input("Enter name of the binary file to be carved:\n")
    # Cheching if the binary file exists or not
    if os.path.isfile('./'+file_name):
        pass
    else:
        print('No binary file present with given name')
        exit(0)
    jpg(file_name, 'jpg')
    png(file_name, 'png')
    pdf(file_name, 'pdf')
    docx(file_name, 'docx')
    jpeg(file_name, 'jpeg')
    if not os.path.exists('./'+'Shetty'):
        os.makedirs('./'+'Shetty')
