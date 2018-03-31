#!/bin/bash
echo "Shellskript"

python3 main.py 26ef025078abda69d2c3de06e27142a6db1a6385bd2524ce4976211570264a39_22632490
env buf_size=1000000 pdflatex main.tex

rm base64decoder.tex
rm binwalk.tex
rm entropy_analysis_graph.png
rm cpuarchitecture.tex
rm cryptomaterial.tex
rm exploitmitigations.tex
rm filehashes.tex
rm filetype.tex
rm initsystems.tex
rm ipandurifinder.tex
rm main.log
rm main.aux
rm malwarescanner.tex
rm meta.tex
rm softwarecomponents.tex
rm stringevaluator.tex
rm printablestrings.tex
rm unpacker.tex
rm usersandpasswords.tex
rm main.tex
