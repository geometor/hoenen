#!/usr/bin/env python3
"""
scripts/build_index.py

Wrapper around generate_analytical_indices.py to generate
both Latin and English Analytical Indices.
"""

from generate_analytical_indices import build_indices

if __name__ == '__main__':
    build_indices()
