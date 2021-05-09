# After arbitrar is done building, use the generated bc-files
# to determine which binary files to pull

import argparse
import os
from shutil import copy


def parser():
  parser = argparse.ArgumentParser(description="Arbitrar JSON Generation")
  setup_parser(parser)
  return parser


def setup_parser(parser):
  parser.add_argument("-i", "--input", type=str, required=True)
  parser.add_argument("-o", "--out_dir", type=str, required=True)
  parser.add_argument("-d", "--search_dir", type=str, required=True)


# Recursively look for files that match a particular set of names
def run_fast_scandir(dir, names):
  subfolders, files = [], []

  for f in os.scandir(dir):
    if f.is_dir():
      subfolders.append(f.path)
    if f.is_file():
      if f.name.lower() in names:
        files.append(f.path)

  for dir in list(subfolders):
    sf, f = run_fast_scandir(dir, names)
    subfolders.extend(sf)
    files.extend(f)

  return subfolders, files

# We consider a file to have non-trivial debug info if there is
# at least one compilation unit present
def has_debug_info(path):
  with open(path, "rb") as f:
    try:
      elffile = ELFFile(f)
      if not elffile.has_dwarf_info(): return False
      dwinfo = elffile.get_dwarf_info()
      CUs = list(dwinfo.iter_CUs())
      return len(CUs) > 0
    except:
      print(f"has_debug_info: {f} inspection failed; skipping")
      return False


# Given a bc file's path, get candidate name and starting search directory
def bc_path_to_name(path):
  (pre, ext) = os.path.splitext(path)
  if not pre: return ""
  splits = pre.split("/")[-1]
  name = splits[-1]
  return name


def main(args):
  names = []
  with open(args.in_file) as inf:
    lines = [x.rstrip() for x in inf]
    names = list(bc_path_to_name(x) for x in lines if x)

  files, _ = run_fast_scandir(args.search_dir, names)

  for file in files:
    if has_debug_info(file):
      copy(file, args.out_dir)


if __name__ == "__main__":
  args = parser().parse_args()
  main(args)

