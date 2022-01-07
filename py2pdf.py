"""Program to create PDF file from Python code."""
import os
import logging
import argparse
import subprocess as sp
from pathlib import Path
from pygments import highlight
from pygments.lexers import PythonLexer
from pygments.formatters import LatexFormatter


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Convert Python .py files into PDF files. "
                                                 "(Note this program requires a pre-existing installation of pdflatex)")
    parser.add_argument('-r', '--recursive', default=False, action='store_true',
                        help='run recursively into sub-directories.')
    parser.add_argument('-l', '--linenos', default=False, action='store_true',
                        help='Add line numbers to the output.')
    parser.add_argument('-o', '--verboptions', default="xleftmargin=-40mm", action='store', metavar="OPTIONS",
                        help='Any extra options (comma separated) to the fancyVrb latex package for the Verbatim '
                             'environment.')
    args = parser.parse_args()

    py_file_glob = "*.py"
    if args.recursive:
        py_file_glob = "**/*.py"

    logging.basicConfig(level=logging.INFO, format="%(name)s : %(levelname)s : %(message)s")
    logger = logging.getLogger("py2pdf")
    for path in sorted(Path(os.getcwd()).glob(py_file_glob)):
        logger.info("Working on file: '%s' -> '%s'", path, path.with_suffix(".pdf"))
        try:
            with open(path, 'rb') as infile:
                code_tex = highlight(infile.read(),
                                     PythonLexer(),
                                     LatexFormatter(full=True, verboptions=args.verboptions, linenos=args.linenos))
        except IOError:
            logger.error("Failed to read file %s", path)
            continue
        proc = sp.run(['pdflatex', f'--jobname={path.stem}', '--'],
                      input=code_tex.encode(), timeout=15, cwd=path.parent,
                      stdout=sp.PIPE, stderr=sp.PIPE)
        if proc.returncode:
            logger.error("pdflatex failed with error code: %s", {proc.returncode})
            logger.error("stdout:\n %s", {proc.stdout})
            logger.error("stderr:\n %s", {proc.stderr})
            continue
        path.with_suffix(".log").unlink(missing_ok=True)
        path.with_suffix(".aux").unlink(missing_ok=True)
