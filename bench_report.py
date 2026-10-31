import json, glob, os, re, html, datetime

OUT='/tmp/bench'
DEST='.'
models=[l.strip() for l in open('bench_models.txt') if l.strip()]

# Generate results.json + report.html + README table from /tmp/bench run artifacts.
# See repo README for methodology and final rendered output.
