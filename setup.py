from pathlib import Path
from setuptools import setup, find_packages

LONG_DESCRIPTION = Path("README.md").read_text()
REQUIREMENTS = Path("requirements.txt").read_text()

# Extracts the package version from the atmolib/version.py file.
VERSION_FILE = Path("atmolib/version.py")
VERSION = VERSION_FILE.read_text().strip().replace("version = ", "").replace('"', "")

setup(
    name="atmolib",
    version=VERSION,
    author="rahul4732saini",
    license="MIT",
    description="Versatile weather package for effortless meteorology data extraction.",
    long_description=LONG_DESCRIPTION,
    long_description_content_type="text/markdown",
    url="https://www.github.com/rahul4732saini/atmolib",
    keywords="atmolib, weather, meteorology, pandas, open-meteo",
    classifiers=[
        "License :: OSI Approved :: MIT License",
        "Intended Audience :: Developers",
        "Operating System :: OS Independent",
        "Development Status :: 4 - Beta",
        "Topic :: Scientific/Engineering :: Atmospheric Science",
        "Topic :: Software Development :: Libraries",
        "Topic :: Software Development :: Libraries :: Python Modules",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "Programming Language :: Python :: 3.12",
    ],
    packages=find_packages(),
    package_data={"atmolib": ["weather_codes.json"]},
    platforms=["any"],
    install_requires=REQUIREMENTS.split("\n"),
)
