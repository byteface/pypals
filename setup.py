import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setup(
    name="pypals",
    version="0.0.1",
    author="@byteface",
    author_email="byteface@gmail.com",
    description="fun way to store random python scripts snippets",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/byteface/pypals",
    license="GNU General Public License v3.0",
    classifiers=[
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.7",
    ],
    packages=["pypals"],
    include_package_data=True
)