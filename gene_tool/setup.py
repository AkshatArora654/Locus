from setuptools import setup, find_packages

setup(
    name="gene_tool",
    version="0.1",
    packages=find_packages(),
    install_requires=[
        "biopython",
        "pandas",
    ],
    entry_points={
        "console_scripts": [
            "gene_tool=gene_tool.cli:main",
        ],
    },
)