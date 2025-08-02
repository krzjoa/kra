# Sphinx configuration for Kra documentation

project = 'Kra'
copyright = '2025, krzjoa'
author = 'krzjoa'
release = '0.1.0'

extensions = [
    'myst_parser',
]

source_suffix = {
    '.rst': 'restructuredtext',
    '.md': 'markdown',
}

master_doc = 'index'

exclude_patterns = ['_build', 'Thumbs.db', '.DS_Store']

html_theme = 'alabaster'
