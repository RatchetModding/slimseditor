# This file was sourced from:
# https://github.com/BuXXe/PARAM.PFD-PS3-Demons-Souls-Savegame-Tool/blob/master/PARAM_PFD.py
#
# Modified by Maikel Wever <maikelwever@gmail.com> for slimeditor
# No license was found, assuming public domain.

# PARAM_PFD (Protected Files Database) Class
# PARAM_PFD Structure 
# see PARAM.PFD.html for documentation (Source: http://www.psdevwiki.com/ps3/PARAM.PFD)
# handles the signatures for protected files in the folder it is in
from Crypto.Cipher import AES
from Crypto.Hash import HMAC, SHA
from binascii import hexlify, unhexlify
import os
import re

# key is from sc_iso module 1.00-4.00 - SYSCON_MANAGER_KEY 
SYSCON_MANAGER_KEY = unhexlify("D413B89663E1FE9F75143D3BB4565274")

KEYGEN_KEY = unhexlify("6B1ACEA246B745FD8F93763B920594CD53483B82")

def byteToInt(data):
    return int(hexlify(data),16)

class PARAM_PFD:

    # returns the encrypted the header_table
    def recryptHeader(self):
        decipher = AES.new(SYSCON_MANAGER_KEY,AES.MODE_CBC, self.header["header_table_iv"])
        encrypted_header_table = decipher.encrypt(self.header["Y_Table_HMAC"]+self.header["X_Table_HMAC_and_Entry_Table_Header_HMAC"]+self.header["File_HMAC_key"]+self.header["Padding"])
        return encrypted_header_table

    # gathers all elements and outputs the PARAM.PFD to a defined folder
    def outputPFD(self,folder):
        if not os.path.exists(folder):
            os.makedirs(folder)   
        with open(folder+"/PARAM.PFD", "wb") as f:
            f.write(self.header["magic"])
            f.write(self.header["version"])
            f.write(self.header["header_table_iv"])
            f.write(self.recryptHeader())

            f.write(self.tables_header["XY_tables_reserved_entries"])
            f.write(self.tables_header["Protected_Files_Table_reserved_entries"])
            f.write(self.tables_header["Protected_Files_table_used_entries"])

            f.write("".join(unhexlify(w) for w in self.x_table))

            for entry in self.protected_files_table:
                f.write(entry["virtual_index_id"])
                f.write(entry["file_name"])
                f.write(entry["padding0"])
                f.write(entry["key"])
                
                f.write("".join(entry["file_hashes"]))
                        
                f.write(entry["padding1"])
                f.write(entry["file_size"])
 
            f.write(self.space)
            f.write("".join(unhexlify(w) for w in self.y_table))
            f.write(self.padding)

    # encrypts / decrypts DAT files 
    def cryptohandler(self, folder,pfd_entry,dodecrypt):
        decipher = AES.new(SYSCON_MANAGER_KEY, AES.MODE_CBC, self.secure_fileID[:16])
        decryptionkey = decipher.decrypt(pfd_entry["key"])
        filepath=folder+"/"+pfd_entry["file_name"].rstrip('\x00')
        output = ""
        with open(filepath,"rb") as f:
            for i in range(os.path.getsize(filepath) / 16 ):
                blockdata=f.read(16)
                x1 = AES.new(decryptionkey[:16],AES.MODE_ECB )
                x2 = AES.new(decryptionkey[:16],AES.MODE_ECB )
                x1.block_size=128
                x2.block_size=128

                # transform index to list of 16 bytes with trailing 8 bytes 0
                buffer_data = unhexlify('{:016x}'.format(i)) + unhexlify('{:016x}'.format(0))           
                buffer_data = x1.encrypt(buffer_data)

                if dodecrypt:
                    blockdata=x2.decrypt(blockdata)

                # xor the two array entries with each other
                newblock=''.join(chr(ord(a) ^ ord(b)) for a,b in zip(blockdata, buffer_data))
                 
                if dodecrypt:
                    output += newblock
                else:   
                    output += x2.encrypt(newblock)
        return output

    # encrypts / decrypts the DAT files from sourcefolder
    # and write them to targetfolder
    # uses the filestable of the opened param.pfd
    def cryptAllDatFiles(self, sourcefolder, targetfolder, dodecrypt):
        if not os.path.exists(targetfolder):
            os.makedirs(targetfolder)

        for u in self.protected_files_table:
            if "PARAM.SFO" in u["file_name"]:
                continue

            # get encrypted / decrypted data
            data = self.cryptohandler(sourcefolder,u,True) if dodecrypt else self.cryptohandler(sourcefolder,u,False)
            
            with open(targetfolder+"/"+u["file_name"].rstrip('\x00'),'wb') as x:
                x.write(data)

    # wrapper for the lazy people
    def decryptAllDatFiles(self, sourcefolder, targetfolder):
        self.cryptAllDatFiles(sourcefolder,targetfolder,True)

    # wrapper for the lazy people
    def encryptAllDatFiles(self, sourcefolder, targetfolder):
        self.cryptAllDatFiles(sourcefolder,targetfolder,False)
        
    # calculate a HMACSHA1 file hash for a given filepath
    def calculateValidEntryHash(self, filepath):
        h = HMAC.new(self.secure_fileID,None,SHA)
        with open(filepath, "rb") as f:
            h.update(f.read(os.path.getsize(filepath)))
        return h.hexdigest()

    # calculate the index of a file in the x/y table   
    def CalculateXYTableEntryIndex(self, filename):
        hash1 = 0
        for i in range(len(filename)): 
            hash1 = (hash1 << 5) - hash1 + ord(filename[i])
        return  hash1 % 57 #XY_tables_reserved_entries 57 dec fixed

    # Concatenates the protected file table data for a given filename 
    def HashData(self, filename):
        for entry in self.protected_files_table:
            if entry["file_name"].rstrip('\x00')==filename:
                namearray=entry["file_name"]
                key=entry["key"]
                hashes=entry["file_hashes"]
                padding1=entry["padding1"]
                filesize=entry["file_size"]
                break
        return namearray+key+"".join(hashes)+padding1+filesize

    # calculates the y table signature for a given filename
    def calcDHKCID2(self, filename):
        h = HMAC.new(self.realkey,None,SHA)
        File_Index_in_x_table = self.CalculateXYTableEntryIndex(filename)

        # use this id on the protected files table to get the entry for the file
        protected_file_table_index = int(self.x_table[File_Index_in_x_table],16)

        # walk long the indices until we reach 0x72 
        while protected_file_table_index < 0x72:
            # gather hashdata and append it to the array
            current_file=self.protected_files_table[protected_file_table_index]["file_name"].rstrip('\x00')
            h.update(self.HashData(current_file))

            # then walk along the additional index provided by the file entry
            protected_file_table_index=int(hexlify(self.protected_files_table[protected_file_table_index]["virtual_index_id"]),16)

        return h.hexdigest()    

    # Rebuild PFD and write to outputfolder
    # updates filehashes, ytable signatures, bottom and top hash, encrypt header table
    def rebuildPFD(self, outputfolder):   
        # update the file_hashes
        for entry in self.protected_files_table:
            if "PARAM.SFO" in entry["file_name"]:
                continue
            filehash = self.calculateValidEntryHash(outputfolder+"/"+entry["file_name"].rstrip('\x00'))
            entry["file_hashes"][0] = unhexlify(filehash) 
            
        # update the y table (check all other files in case that they rely on each other)
        for u in self.protected_files_table:
            activefile = u["file_name"].rstrip("\x00")
            self.y_table[self.CalculateXYTableEntryIndex(activefile)] = self.calcDHKCID2(activefile)
            
        # update the top and bottom hash
        # bottomhash
        h = HMAC.new(self.realkey,None,SHA)
        h.update("".join(unhexlify(w) for w in self.y_table))
        self.header["Y_Table_HMAC"] = unhexlify(h.hexdigest())

        # tophash
        h = HMAC.new(self.realkey,None,SHA)
        h.update(self.tables_header["XY_tables_reserved_entries"])
        h.update(self.tables_header["Protected_Files_Table_reserved_entries"])
        h.update(self.tables_header["Protected_Files_table_used_entries"])
        h.update("".join(unhexlify(w) for w in self.x_table))
        self.header["X_Table_HMAC_and_Entry_Table_Header_HMAC"] = unhexlify(h.hexdigest())

        # encrypt the header table back 
        # write everything to <outputfolder>/PARAM.PFD
        self.outputPFD(outputfolder)

    # read the PARAM.PFD in the given folder
    def __init__(self, folder, fileid):
        secure_fileID = re.findall('..', fileid)
        secure_fileID.insert(5, "0a")
        secure_fileID.insert(3, "0e")
        secure_fileID.insert(1, "0f")
        secure_fileID.insert(1, "0b")
        self.secure_fileID = unhexlify("".join(secure_fileID))

        with open(folder+"/PARAM.PFD", "rb") as f:
            self.header = {}
            self.header["magic"] = f.read(8)
            self.header["version"] = f.read(8)
            self.header["header_table_iv"] = f.read(16)
            
            # decrypt header_table using AES-128 CBC with key SYSCON_MANAGER_KEY and init vector header_table_iv
            header_table = f.read(64)   
            decipher = AES.new(SYSCON_MANAGER_KEY,AES.MODE_CBC, self.header["header_table_iv"])
            decrypted_header_table = decipher.decrypt(header_table)

            # get the plaintext header_table
            self.header["Y_Table_HMAC"] = decrypted_header_table[:20] # bottom hash
            self.header["X_Table_HMAC_and_Entry_Table_Header_HMAC"] = decrypted_header_table[20:40] # top hash
            self.header["File_HMAC_key"] = decrypted_header_table[40:60]
            self.header["Padding"] = decrypted_header_table[60:60+4]

            # header version defines which realkey to use
            # for Demon Souls (header version 3), this is just the File_HMAC_key
            # for a version 4 file it would be: realkey = HMACSHA1(<keygen_key>, File_HMAC_key)
            # keygen_key = 6B1ACEA246B745FD8F93763B920594CD53483B82
            # based on info from https://github.com/Wulf2k/DeS-SaveEdit : Param_PFD.vb
            if byteToInt(self.header["version"])==3:
                self.realkey = self.header["File_HMAC_key"] 
            else:
                # version 4 and fallback for all yet unknown versions
                h = HMAC.new(KEYGEN_KEY ,None,SHA)
                h.update(self.header["File_HMAC_key"])
                self.realkey = unhexlify(h.hexdigest())
                
            # tables header
            self.tables_header={}
            self.tables_header["XY_tables_reserved_entries"]=f.read(8)
            self.tables_header["Protected_Files_Table_reserved_entries"]=f.read(8)
            self.tables_header["Protected_Files_table_used_entries"]=f.read(8)

            # x-table
            # number of entries is XY_tables_reserved_entries
            self.x_table = [hexlify(f.read(8)) for k in range(byteToInt(self.tables_header["XY_tables_reserved_entries"]))]

            # protected_files_table
            # entry length 272 bytes
            self.protected_files_table =[]
            for k in range(byteToInt(self.tables_header["Protected_Files_table_used_entries"])):
                entry={}
                entry["virtual_index_id"]=f.read(8)
                entry["file_name"]=f.read(65)
                entry["padding0"]=f.read(7)
                entry["key"]=f.read(64) 
                entry["file_hashes"]=[f.read(20),f.read(20),f.read(20),f.read(20)]
                entry["padding1"]=f.read(40)
                entry["file_size"]=f.read(8)
                self.protected_files_table.append(entry)
            
            # read the unused bytes
            self.space = f.read((byteToInt(self.tables_header["Protected_Files_Table_reserved_entries"])-byteToInt(self.tables_header["Protected_Files_table_used_entries"]))*272)
            
            # y-table
            # number of entries is XY_tables_reserved_entries
            self.y_table = [hexlify(f.read(20)) for k in range(byteToInt(self.tables_header["XY_tables_reserved_entries"]))]

            # read fixed padding of 44 bytes
            self.padding = f.read(44)
