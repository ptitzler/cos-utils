# Basic file uploader for Cloud Object Storage


## Getting started

The utility requires Python 3.6 or above.

Download the source code and install the prerequisites.

```
$ git clone https://github.com/ptitzler/cos-uploader.git
$ cd cos-uploader
$ pip install -r requirements.txt
```

Set the `AWS_ACCESS_KEY_ID` and `AWS_SECRET_ACCESS_KEY`environment variables 
based on your Cloud Object Storage HMAC credentials.
```
$ export AWS_ACCESS_KEY_ID=...
$ export AWS_SECRET_ACCESS_KEY=...
```

The help lists required and optional parameters. The examples listed below explain them in detail.

```
$ python upload_data.py --help
usage: upload_data.py [-h] [-p PREFIX] [-r] [-s] [-w] bucket source

Upload files to a Cloud Object Storage bucket

positional arguments:
  bucket                Bucket name
  source                File or directory

optional arguments:
  -h, --help            show this help message and exit
  -p PREFIX, --prefix PREFIX
                        Key name prefix
  -r, --recursive       Include files in subdirectories
  -s, --squash          Exclude subdirectory name from key name
  -w, --wipe            Clear bucket prior to upload

Environment variables AWS_ACCESS_KEY_ID and AWS_SECRET_ACCESS_KEY must be
defined to run the utility.
```

## Example scenario

The `</path/to/local/directory>` contains the following directories and files:
```
file1.png
file2.png
file3.jpg
file4.txt
dir1/file5.gif
dir1/file6.png
dir1/dir2/file7.png
dir1/dir3/file8.jpg
dir1/dir3/file1.png
```

In the examples given below `<bucket-name>` refers to an existing bucket in Cloud Object Storage.

## Upload directories

You can upload the content of any directory.

### Upload the content of `</path/to/local/directory>` to bucket `<bucket-name>`

```
$ python upload_data.py <bucket-name> </path/to/local/directory>
```

Bucket `<bucket-name>` contains the following objects:

```
file1.png
file2.png
file3.jpg
file4.txt
```

### Same as before but clear the bucket first before uploading

Specify the optional `--wipe` parameter to clear the bucket before upload.

```
$ python upload_data.py <bucket-name> </path/to/local/directory> --wipe
```

Bucket `<bucket-name>` contains the following objects:

```
file1.png
file2.png
file3.jpg
file4.txt
```

### Same as before but include subdirectories

Specify the optional `--recursive` parameter include files in subdirectories.

```
$ python upload_data.py <bucket-name> </path/to/local/directory> --wipe --recursive
```

Bucket `<bucket-name>` contains the following objects:

```
file1.png
file2.png
file3.jpg
file4.txt
dir1/file5.gif
dir1/file6.png
dir1/dir2/file7.png
dir1/dir3/file8.jpg
dir1/dir3/file1.png
```

### Same as before but don't use subdirectory names during object key generation

Specify the optional `--squash` parameter to ignore subdirectory names during object key generation.

```
$ python upload_data.py <bucket-name> </path/to/local/directory> --wipe --recursive --squash
```

Bucket `<bucket-name>` contains the following objects. Note that `</path/to/local/directory>` contains two files named `file1.png`. First `file1.png` is uploaded and later overwritten with the content of `dir1/dir3/file1.png`.

```
file2.png
file3.jpg
file4.txt
file5.gif
file6.png
file7.png
file8.jpg
file1.png
```

### Same as before but include a static key name prefix

Specify the optional `--prefix <prefix>` parameter to add `<prefix>` to the object key for every file.

```
$ python upload_data.py <bucket-name> </path/to/local/directory> --wipe --recursive --squash --prefix data
```

Bucket `<bucket-name>` contains the following objects:

```
data/file2.png
data/file3.jpg
data/file4.txt
data/file5.gif
data/file6.png
data/file7.png
data/file8.jpg
data/file1.png
```

## Upload files

You can upload a single file by specifying `</path/to/local/directory/filename>`.

```
$ python upload_data.py <bucket-name> /path/to/local/directory/file1.png --wipe 
```

Bucket `<bucket-name>` contains the following object:

```
file1.png
```

You can upload multiple files by specifying a pattern `</path/to/local/directory/filename-pattern>`

```
$ python upload_data.py <bucket-name> /path/to/local/directory/*.png --wipe 
```

> On Linux, Unix and MacOS wildcards need to be escaped to prevent shell expansion: `/path/to/local/directory/\*.png`.

Bucket `<bucket-name>` contains the following objects:

```
file1.png
file2.png
```

Use the `--recursive` parameter to extend the search to subdirectories of `/path/to/local/directory/`.

```
$ python upload_data.py <bucket-name> /path/to/local/directory/*.png --wipe --recursive
```

```
file1.png
file2.png
dir1/file6.png
dir1/dir2/file7.png
dir1/dir3/file1.png
```

## License

[Apache-2.0](LICENSE)