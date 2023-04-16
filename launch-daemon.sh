#!/bin/sh

daemon --chdir $PWD -n silencedetector -o log.txt -r -- ./silence-detector.py
