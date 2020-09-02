import model
import subprocess
import os
import sys
import argparse



def getOptions(args=sys.argv[1:]):
    parser = argparse.ArgumentParser(description="Parses command.")
    parser.add_argument("-d", "--input", help="gs://<bucketname>")
    parser.add_argument("-i", "--data", help="Your data set file")
    parser.add_argument("-i2", "--target", help="Your data target set file")
    parser.add_argument("-s", "--staging", help="gs://<bucketname>")
    parser.add_argument("-sd", "--stagedir", help="gs://<bucketname>/<your input>")
    options = parser.parse_args(args)
    return options

if __name__ == "__main__":
    options = getOptions(sys.argv[1:])
    tm = model.model(options.input,options.data, options.target, options.staging , options.stagedir )
    tm.fetch()
    tm.load()
    tm.train()
    tm.save()
    tm.upload()