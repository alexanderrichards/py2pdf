"""Setuptools Module."""
from setuptools import setup, find_packages

setup(
    name="py2pdf",
    version="0.1",
    packages=find_packages(),
    install_requires=['pygments'],
    # metadata for upload to PyPI
    author="Alexander Richards",
    author_email="a.richards@imperial.ac.uk",
    description="Production System",
    license="MIT",
    keywords="pdf python",
    url="https://github.com/alexanderrichards/py2pdf"
)
