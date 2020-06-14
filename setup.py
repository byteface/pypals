from distutils.core import setup
import os

long_description=""
with open("README.md", "r") as f:
        long_description = f.read()

setup(
    name="pypals",
    version="0.0.7",
    keywords = ['pypals'],
    author="@byteface",
    author_email="byteface@gmail.com",
    description="Terminal buddies to store and run python snippets",
    # long_description_content_type='text/markdown',
    # long_description=long_description,
    url="https://github.com/byteface/pypals",
    download_url = 'https://github.com/byteface/pypals/archive/0.0.7.tar.gz',
    license="MIT",
    classifiers=[
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.7",
    ],
    packages=["pypals"],
    include_package_data = True
)