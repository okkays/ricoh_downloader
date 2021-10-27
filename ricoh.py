import requests
import os
import sys

# Usage:
# ls [dir]
# download dir1 [dir2 ...]

_cache = {}
URL = 'http://192.168.1.1/v1/photos'
OUTDIR = 'output'

def main():
  if len(sys.argv) == 1:
    print('Please specify "ls [dir]" or "download dir|file"')
    sys.exit(400)

  command = sys.argv[1]
  if command == 'ls':
    print(', '.join(ls()))

  if command == 'download':
    download()

def _mkdir(*args, **kwargs):
  try:
    return os.mkdir(*args, **kwargs)
  except OSError as e:
    if (e.errno != 17): # Ignore File Exists
      raise

def download():
  if len(sys.argv) <= 2:
    print('Please specify director(ies) to download')
    sys.exit(400)

  targets = sys.argv[2:]
  _mkdir(OUTDIR)
  for target in targets:
    _mkdir(os.path.join(OUTDIR, target))
    download_files(target)

def download_files(directory):
  files = ls_dir(directory)
  for filename in files:
    download_file(directory, filename)

def download_file(directory, filename):
  outname = os.path.join(OUTDIR, directory, filename)
  if os.path.exists(outname):
    print('Skipping (already exists): {}'.format(outname))
    return
  resource = '/'.join([URL, directory, filename])
  print('Downloading: {}...'.format(outname), end='', flush=True)
  r = requests.get(resource)
  if r.status_code != 200:
    print('Something went wrong downloading {}: {}'.format(
      resource, r.status_code))
    sys.exit(r.status_code)

  with open(outname, 'wb') as outfile:
    outfile.write(r.content)
  print(' done!')

def ls():
  try:
    return ls_dir(sys.argv[2])
  except IndexError:
    return ls_dirs()

def ls_dir(directory):
  dirs = get_ls()
  for d in dirs:
    if d['name'] != directory:
      continue
    return sorted(d['files'])
  print('No such directory: {}'.format(directory))
  sys.exit(404)

def ls_dirs():
  return sorted([d['name'] for d in get_ls()])

def get_ls():
  try:
    dirs = _cache[URL]
  except KeyError:
    response = requests.get(URL)
    dirs = response.json()
    if dirs['errCode'] != 200:
      print(errCode, errMsg)
      sys.exit(dirs['errCode'])
    _cache[URL] = dirs
  return dirs['dirs']

if __name__ == '__main__':
  main()

