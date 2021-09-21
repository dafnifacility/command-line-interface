import setuptools

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setuptools.setup(
    name="dafni-cli-dafni-facility",
    version="0.0.7",
    author="DAFNI Facility",
    author_email="support@dafni.ac.uk",
    description="The beginnings of a command line interface for DAFNI. This package is still in development and not ready for use.",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/dafnifacility/command-line-interface/",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.9",
)
