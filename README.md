# Cloud Object Storage CLI

[![Build Status](https://travis-ci.com/CODAIT/cos-utils.svg?branch=master)](https://travis-ci.com/CODAIT/cos-utils) [![PyPI release](https://img.shields.io/pypi/v/cos-utils.svg)](https://pypi.org/project/cos-utils/) ![PyPI - Python Version](https://img.shields.io/pypi/pyversions/cos-utils)

Table of content:
- [Getting Started](#getting-started)
- [Listing Cloud Object Storage buckets](#listing-cloud-object-storage-buckets)
- [Listing the content of a Cloud Object Storage bucket](#listing-the-content-of-a-cloud-object-storage-bucket)
- [Uploading files to a Cloud Object Storage bucket](#uploading-files-to-a-cloud-object-storage-bucket)
- [Downloading files from a Cloud Object Storage bucket](#downloading-files-from-a-cloud-object-storage-bucket)
- [Removing files from a Cloud Object Storage bucket](#removing-files-from-a-cloud-object-storage-bucket)

---

## Getting started

The utility requires Python 3.6 or above. 

### Installation

You can install the utility from [PyPI](https://pypi.org/project/cos-utils) or from the [source](#install-from-source).

#### Install from pypi.org

```
$ pip install cos-utils --upgrade
```

#### Install from source code

```
$ git clone https://github.com/CODAIT/cos-utils.git
$ cd cos-utils
$ pip install .
```

#### Configuration

Set the `AWS_ACCESS_KEY_ID` and `AWS_SECRET_ACCESS_KEY`environment variables based on your [Cloud Object Storage HMAC credentials](https://cloud.ibm.com/docs/services/cloud-object-storage/iam?topic=cloud-object-storage-service-credentials).
```
$ export AWS_ACCESS_KEY_ID=...
$ export AWS_SECRET_ACCESS_KEY=...
```

# Listing Cloud Object Storage buckets

You can run the list utility in a terminal window using the generated console script

```
$ list_buckets --help
```

or explicitly

```
$ python -m cos_utils.list_buckets --help
```

The help lists required and optional parameters.

```
usage: list_buckets [-h] pattern

List buckets in Cloud Object Storage instance.

positional arguments:
  pattern     Bucket name spec (supported wildcards: * and ?)

optional arguments:
  -h, --help  show this help message and exit

Environment variables AWS_ACCESS_KEY_ID and AWS_SECRET_ACCESS_KEY must be
defined to run the utility.
```

## List all buckets

```
$ list_buckets *
```

> On Linux, Unix and MacOS wildcards need to be escaped to prevent shell expansion: `list_files <bucket-name> \*`.

## Apply a filter

Use the `*` (any character) and `?` (one character) wildcards to define a filter condition.

For example, to limit output to buckets starting with `data-`:

```
$ list_buckets data-*
```

# Listing the content of a Cloud Object Storage bucket

You can run the list utility in a terminal window using the generated console script

```
$ list_files --help
```

or explicitly

```
$ python -m cos_utils.list_files --help
```

The help lists required and optional parameters.

```
usage: list_files [-h] bucket pattern

List the content of a Cloud Object Storage bucket.

positional arguments:
  bucket      Bucket name
  pattern     Object key spec (supported wildcards: * and ?)

optional arguments:
  -h, --help  show this help message and exit

Environment variables AWS_ACCESS_KEY_ID and AWS_SECRET_ACCESS_KEY must be
defined to run the utility.
```

## List the content of `<bucket-name>`

```
$ list_files <bucket-name> *
```

> On Linux, Unix and MacOS wildcards need to be escaped to prevent shell expansion: `list_files <bucket-name> \*`.

## Apply a filter

Use the `*` (any character) and `?` (one character) wildcards to define a filter condition.

For example, to limit output to files ending in `.png`:

```
$ list_files <bucket-name> *.png
```

# Uploading files to a Cloud Object Storage bucket

You can run the upload utility in a terminal window using the generated console script

```
$ upload_files --help
```

or explicitly

```
$ python -m cos_utils.upload_files --help
```

The help lists required and optional parameters. The examples listed below explain them in detail.

```
usage: upload_files [-h] [-p PREFIX] [-r] [-s] [-w] bucket pattern

Upload files to a Cloud Object Storage bucket.

positional arguments:
  bucket                Bucket name
  pattern               File or directory spec (supported wildcards: * and ?)

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
$ upload_files <bucket-name> </path/to/local/directory>
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
$ upload_files <bucket-name> </path/to/local/directory> --wipe
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
$ upload_files <bucket-name> </path/to/local/directory> --wipe --recursive
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
$ upload_files <bucket-name> </path/to/local/directory> --wipe --recursive --squash
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
$ upload_files <bucket-name> </path/to/local/directory> --wipe --recursive --squash --prefix data
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
$ upload_files <bucket-name> /path/to/local/directory/file1.png --wipe 
```

Bucket `<bucket-name>` contains the following object:

```
file1.png
```

You can upload multiple files by specifying a pattern `</path/to/local/directory/filename-pattern>`

```
$ upload_files <bucket-name> /path/to/local/directory/*.png --wipe 
```

> On Linux, Unix and MacOS wildcards need to be escaped to prevent shell expansion: `/path/to/local/directory/\*.png`.

Bucket `<bucket-name>` contains the following objects:

```
file1.png
file2.png
```

Use the `--recursive` parameter to extend the search to subdirectories of `/path/to/local/directory/`.

```
$ upload_files <bucket-name> /path/to/local/directory/*.png --wipe --recursive
```

```
file1.png
file2.png
dir1/file6.png
dir1/dir2/file7.png
dir1/dir3/file1.png
```

# Downloading files from a Cloud Object Storage bucket

You can run the download utility in a terminal window using the generated console script

```
$ download_files --help
```

or explicitly

```
$ python -m cos_utils.dowload_files --help
```

The help lists required and optional parameters. The examples listed below explain them in detail.

```
usage: download_files [-h] [-d TARGET_DIR] bucket pattern

Download objects from a Cloud Object Storage bucket.

positional arguments:
  bucket                Bucket name
  pattern               Object key spec (supported wildcards: * and ?)

optional arguments:
  -h, --help            show this help message and exit
  -d TARGET_DIR, --target_dir TARGET_DIR
                        Local target directory. Defaults to the current
                        directory.

Environment variables AWS_ACCESS_KEY_ID and AWS_SECRET_ACCESS_KEY must be
defined to run the utility.
```

### Download complete bucket content

You can download the complete content of a bucket to the current directory:

```
$ download_files <bucket-name> *
```

> On Linux, Unix and MacOS wildcards need to be escaped to prevent shell expansion: `download_files <bucket-name> \*`.

### Same as before but specify a target directory

Use the `--target_dir </path/to/local/dir>` parameter to specify an existing directory where the downloaded files will be stored:

```
$ download_files <bucket-name> * --target_dir /tmp/downloads
```

### Use wildcards to selectively download files

Use the `*` (any character) and `?` (one character) wildcards to define a filter condition.

#### Download only png files

```
$ download_files <bucket-name> *.png
```

#### Download files that contain a certain string in their name

```
$ download_files <bucket-name> *fil*
```

# Removing files from a Cloud Object Storage bucket

You can run the remove utility in a terminal window using the generated console script

```
$ remove_files --help
```

or explicitly

```
$ python -m cos_utils.remove_files --help
```

### Remove all files from a bucket

```
$ remove_files <bucket-name>
```

# License

[Apache-2.0](LICENSE)
