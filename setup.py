from setuptools import setup
import os

long_description=""
with open("README.md", "r") as f:
        long_description = f.read()

setup(
    name="pypals",
    version="0.0.8",
    keywords = ['pypals'],
    author="@byteface",
    author_email="byteface@gmail.com",
    description="Terminal buddies to store and run python snippets",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/byteface/pypals",
    download_url = 'https://github.com/byteface/pypals/archive/0.0.8.tar.gz',
    license="MIT",
    classifiers=[
        'Intended Audience :: Developers',
        'Topic :: Software Development :: Build Tools',
        "Programming Language :: Python :: 3.7",
        "License :: OSI Approved :: MIT License"
    ],
    packages=["pypals"],
    include_package_data = True,
    python_requires='>=3.7',
)