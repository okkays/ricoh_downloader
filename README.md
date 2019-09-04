# Ricoh Downloader

## What is it?

A small script to list and download files from the Ricoh WG-30.  May work for other cameras with the same API.

Expects the main API url to be:

```py
URL = 'http://192.168.1.1/v1/photos'
```

Expects the format of that API to match the sample in `sample.json` (a list of folder objects containing some files).

## Usage

To list all folders on the camera:

```bash
python ricoh.py ls
```

To list all images in a folder:

```bash
python ricoh.py ls foldername
```

To download all images from folder(s):

```bash
python ricoh.py download dir1 [dir2 ...]
```
