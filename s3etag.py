#!/usr/bin/python

"""
Simple script to generate ETag values for local files to check against
S3 objects that were multipart uploads.

For 'large' files that used multipart uploads, the each sub part is md5summed then
they take a md5sum of the string of all the sub parts.  $!$!#%!#%!#%@#
"""

# Max upload size in bytes before multipart kicks in
max_upload = 64 * 1024 * 1024 # 64MB

# Size of each multipart part
multipart_size = 64 * 1024 * 1024 # 64 MB

# Support libs
import os
import sys
import hashlib
import binascii


def etagsum(sourcePath):
    hash = hashlib.md5()
    
    # If the file is bigger than a single chunk, break it up
    if  os.path.getsize(sourcePath) > max_upload:
        partcount = 0
        md5string = ""
        with open(sourcePath, "rb") as f:
            # Iterate over chunks of 64MB
            for chunk in iter(lambda: f.read(multipart_size), ""):
                hash = hashlib.md5()
                hash.update(chunk)
                # Collect string of md5sums of each chunk
                md5string = md5string + binascii.unhexlify(hash.hexdigest())
                partcount += 1

        # Get a new hash of the string of sub hashes and list total part count
        hash = hashlib.md5()
        hash.update(md5string)
        return hash.hexdigest() + "-" + str(partcount)

    else:
        # Just a normal md5
        with open(sourcePath, "rb") as f:
            for chunk in iter(lambda: f.read(multipart_size), ""):
                hash.update(chunk)
        return hash.hexdigest()


myfile = sys.argv[1]
print myfile
print etagsum(myfile)
