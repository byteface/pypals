import setuptools
import os

with open("README.md", "r") as fh:
    long_description = fh.read()

setup(
    name="pypals",
    version="0.0.2",
    author="@byteface",
    author_email="byteface@gmail.com",
    description="Terminal buddies to run your python snippets",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/byteface/pypals",
    download_url = 'https://github.com/byteface/pypals/archive/0.0.2.tar.gz',
    license="GNU General Public License v3.0",
    classifiers=[
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.7",
    ],
    packages=["pypals"],
    include_package_data=True
)

os.mkdir('pypals') # create empty dir for user pypals at cwd