# Verifier for Google Electronic Returns (VGER) Version 1.5 SHA512 Edition
# Copyright (C) 2025  Benjamin Lord

#    This program is free software: you can redistribute it and/or modify
#    it under the terms of the GNU General Public License as published by
#    the Free Software Foundation, either version 3 of the License, or
#    (at your option) any later version.

#    This program is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#    GNU General Public License for more details.

#    You should have received a copy of the GNU General Public License
#    along with this program.  If not, see <https://www.gnu.org/licenses/>.

# This program checks Letter.pdf and 12345678-20250101-1.zip archives provided by Google during legals service.
# SHA512 hash values within the PDF are compared to nested ZIPs contained within the primary ZIP.
# Standalone ZIP archives are autodetected and compared.
# Results are printed to screen and logged to 12345678-20250101-1.zip.txt

# Requires pypdf library for Python execution

# This software was designed to handle return archives in two formats known to the author on 7/16/2025.
# Variations made by Google outside of the two known formats will likely produce "mismatch or error" results



import zipfile, hashlib, os
from pypdf import PdfReader

def calc_512_hash(archive_filename):
    """This function ingests a Google cloud data archive, determines if it contains nested archives,
    and returns filenames and associated SHA512 values as a list.

    Args:
        archive_filename: Archive to check.

    Returns:
        file_hash_list: List in format filename:SHA512.
    """
    file_hash_list = []
    nested = False
    try:
        with zipfile.ZipFile(archive_filename, 'r') as archive_zip_file:
            for file_info in archive_zip_file.infolist():
                if file_info.filename.endswith('.zip'): #Ingests archive with nested zip archives
                    with archive_zip_file.open(file_info) as to_hash:
                        hashed = hashlib.new('sha512')
                        for chunk in iter(lambda: to_hash.read(4096), b''):
                            hashed.update(chunk)
                        file_hash = hashed.hexdigest()
                    file_hash_list.append(file_info.filename + ':' + file_hash) #Colon added to match letter format
                    nested = True
        if nested == False: #Ingests a single zip archive
            with open(archive_filename, 'rb') as to_hash:
                hashed = hashlib.new('sha512')
                for chunk in iter(lambda: to_hash.read(4096), b''):
                    hashed.update(chunk)
                file_hash = hashed.hexdigest()
                archive_filename = os.path.basename(archive_filename)
            file_hash_list.append(archive_filename + ':' + file_hash) #Colon added to match letter format
    except zipfile.BadZipFile:
        print(f"Error: '{archive_filename}' is not a valid zip file.")
    except FileNotFoundError:
        print(f"File not found: '{archive_filename}'")
    except Exception as error_report:
        print(f"Error: {error_report}")
    return(file_hash_list)

def letter_reader(letter_filename):
    """This function reads a Letter.pdf file as provided by Google during legal service as a string and
    removes interfering data from the filename and hash list.

    Args:
        letter_filename: PDF to read into string

    Returns:
        letter_content: Cleaned string containing filenames and hashes
    """
    letter_content = str("")
    try:
        extracted = PdfReader(letter_filename)
        for page in extracted.pages:
            letter_content += page.extract_text() #Reads pdf to string
            letter_content = letter_content.replace('\r','').replace('\n','').replace(" ","") #Removes interfering string content
            letter_content = letter_content.replace("GoogleLLCUSLawEnforcment@google.com1600AmphitheatreParkwayMountainView,California94043www.google.com","")
            letter_content = letter_content.replace("GoogleLLCUSLawEnforcement@google.com1600AmphitheatreParkwayMountainView,California94043",'')
            letter_content = letter_content.replace("SHA512-", "")
    except FileNotFoundError:
        print(f"File not found: '{letter_filename}'")
    except Exception as error_report:
        print(f"Error: {error_report}")
    print(letter_content)
    return(letter_content)

print('Verifier for Google Electronic Returns (VGER) Version 1.5 SHA512 Edition')

letter_filename = input('Enter the letter filename: ')
letter_filename = letter_filename.replace('"','')
archive_filename = input('Enter the archive filename: ')
archive_filename = archive_filename.replace('"','')
output_file = archive_filename + ".txt"
success_count = int(0)
error_count = int(0)

file_hashes = calc_512_hash(archive_filename)
letter_data = letter_reader(letter_filename)

with open(output_file, 'w') as file: #Opens output file for writing results
    file.write("Verifier for Google Electronic Returns (VGER) Version 1.5 SHA512 Edition\n")
    file.write("------------------------------------------------------------------\n")
    for item in file_hashes: #Checks for hash matches
        if item in letter_data:
            print(item + ":match")
            file.write(item + ":match\n")
            success_count += 1
        else:
            print(item + ":mismatch or error")
            file.write(item + ":mismatch or error\n")
            error_count += 1
    if ((success_count > 0) or (error_count > 0)):
        print("------------------------------------------------------------------")
        file.write("------------------------------------------------------------------\n")
        print(archive_filename + " checked against " + letter_filename)
        file.write(archive_filename + " checked against " + letter_filename + "\n")
        print(str(int(success_count)) + " hash match(es) verified.")
        file.write(str(int(success_count)) + " hash match(es) verified.\n")
        print(str(int(error_count)) + " hash mismatch(es) or error(s) detected.")
        file.write(str(int(error_count)) + " hash mismatch(es) or error(s) detected.\n")
    else:
        print("An error occured.")
        file.write("An error occured.\n")
file.close()
