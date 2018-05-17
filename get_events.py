import argparse

parser = argparse.ArgumentParser()
parser.add_argument("-s", "--start", default=None)
parser.add_argument("-e", "--end", default=None)
args = parser.parse_args()

print(args)
