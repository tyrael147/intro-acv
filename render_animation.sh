#!/bin/bash

# Exit script if a command fails
set -e

echo "=== Setting up Manim Environment ==="
# Check if manim is installed, install it if not
if ! command -v manim &> /dev/null
then
    echo "Manim could not be found. Attempting to install via pip..."
    uv add manim
fi

# NOTE: Manim also requires LaTeX (e.g. texlive) and ffmpeg installed on your system.
# If you are on Ubuntu/Debian, you might need to run:
# sudo apt update && sudo apt install texlive texlive-latex-extra texlive-fonts-extra texlive-latex-recommended texlive-science texlive-fonts-extra tipa ffmpeg

echo "=== Rendering Manim Animation ==="
# -p : Preview (open video once rendered)
# -q h : Quality High (1080p, 60fps)
# lca_animation.py : The python script file
# LCAMatrixExplainer : The specific Scene class to render

uv run manim -p -qh scripts/lca_animation.py LCAMatrixExplainer

echo "=== Rendering Complete! ==="
