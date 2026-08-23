"""Generate sphinx-gallery tutorial pages from standalone Python scripts."""

import glob
import os
import re
from typing import Any, Callable, Tuple

from sphinx.application import Sphinx
from sphinx_gallery import gen_rst
from sphinx_gallery.gen_gallery import DEFAULT_GALLERY_CONF
from sphinx_gallery.scrapers import matplotlib_scraper


def call_memory(func: Callable[[], Any]) -> Tuple[float, Any]:
    """Run ``func``, reporting zero memory usage.

    sphinx-gallery expects a (memory, return-value) pair; tutorials here are not
    memory-profiled, so the measurement is always 0.0.

    Args:
        func: The zero-argument callable to run.

    Returns:
        A tuple of the memory used (always 0.0) and ``func``'s return value.
    """
    return 0.0, func()


class App:
    """Minimal stand-in for a Sphinx application, as sphinx-gallery expects."""

    config = {
        "source_suffix": ".rst",
        "default_role": "any",
    }


def generate_tutorials(file_path: str, destination_dir_path: str) -> None:
    """Generate tutorials from python files.

    Args:
        file_path (str): Paths or glob pattern to python files.
        destination_dir_path (str): Destination directory path.
    """
    # parse glob
    file_paths = glob.glob(file_path)
    if not file_paths:
        print(f"Warning: No files found: {file_path}")

    for file_path in file_paths:
        filename = os.path.basename(file_path)
        source_dir_path = os.path.dirname(file_path)
        if os.path.splitext(filename)[1] != ".py":
            continue

        gen_rst.EXAMPLE_HEADER = ":tutorial: true\n"
        file_path = os.path.join(destination_dir_path, filename)

        gallery_config = DEFAULT_GALLERY_CONF
        gallery_config["lang"] = "python"
        gallery_config["src_dir"] = source_dir_path
        gallery_config["titles"] = {}
        gallery_config["titles"][file_path] = ""
        gallery_config["memory_base"] = 0.0
        gallery_config["call_memory"] = call_memory
        gallery_config["min_reported_time"] = float("inf")
        gallery_config["exclude_implicit_doc_regex"] = True
        gallery_config["show_signature"] = False
        gallery_config["filename_pattern"] = f"{re.escape(os.sep)}run_"
        gallery_config["reset_modules"] = ()
        gallery_config["image_scrapers"] = tuple([matplotlib_scraper])
        gallery_config["jupyterlite"] = None
        gallery_config["app"] = App()

        gen_rst.generate_file_rst(
            filename, destination_dir_path, source_dir_path, gallery_config
        )


def setup(app: Sphinx) -> None:
    """Register the extension; nothing to set up."""
    pass
