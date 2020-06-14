from distutils.core import setup
import os

setup(
    name="pypals",
    version="0.0.6",
    keywords = ['pypals'],
    author="@byteface",
    author_email="byteface@gmail.com",
    description="Terminal buddies to store and run your python snippets",
    url="https://github.com/byteface/pypals",
    download_url = 'https://github.com/byteface/pypals/archive/0.0.6.tar.gz',
    license="MIT",
    classifiers=[
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.7",
    ],
    packages=["pypals"],
    include_package_data = True
)