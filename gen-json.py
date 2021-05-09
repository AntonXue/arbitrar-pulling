# Given a list of debian packages, output a json file in Arbitrar's format

import argparse
import json


def parser():
  parser = argparse.ArgumentParser(description="Arbitrar JSON Generation")
  setup_parser(parser)
  return parser


def setup_parser(parser):
  parser.add_argument("-i", "--input", type=str, required=True)
  parser.add_argument("-o", "--output", type=str, required=True)


def main(args):
  items = []
  in_file = args.input
  with open(in_file, "r") as inf:
    lines = [x.rstrip() for x in inf]
    lines = list(x for x in lines if x)

    for pkg_name in lines:
      item = {
        "name" : pkg_name,
        "pkg_src" : {
          "src_type" : "debian",
          "link" : pkg_name
        }
      }
      items.append(item)

  out_file = args.output
  with open(out_file, "w") as outf:
    json.dump(items, outf, indent=2)


if __name__ == "__main__":
  args = parser().parse_args()
  main(args)

