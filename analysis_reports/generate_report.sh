#!/bin/bash
echo "Generating the pdf report..."

python3 generate_firmware_analysis_report.py 26ef025078abda69d2c3de06e27142a6db1a6385bd2524ce4976211570264a39_22632490
env buf_size=1000000 pdflatex firmware_analysis_report.tex

rm base64_decoder.tex
rm binwalk.tex
rm entropy_analysis_graph.png
rm cpu_architecture.tex
rm crypto_material.tex
rm exploit_mitigations.tex
rm file_hashes.tex
rm file_type.tex
rm init_systems.tex
rm ip_and_uri_finder.tex
rm firmware_analysis_report.log
rm firmware_analysis_report.aux
rm firmware_analysis_report.tex
rm malware_scanner.tex
rm meta.tex
rm software_components.tex
rm string_evaluator.tex
rm printable_strings.tex
rm unpacker.tex
rm users_and_passwords.tex