import os
import sys

dirpath = sys.argv[1]
for f in os.listdir(dirpath):
  root, ext = os.path.splitext(f)
  old = os.path.join(dirpath, f)
  new = os.path.join(dirpath, '-'.join([f'{ord(c):x}' for c in root]) + ext)
  print(f'{old} -> {new}')
  os.rename(old, new)