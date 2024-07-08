from setuptools import setup, find_packages
from os import path


def packagefile(*relpath):
    return path.join(path.dirname(__file__), *relpath)


def read(*relpath):
    with open(packagefile(*relpath), encoding="utf-8") as f:
        return f.read()


setup(
    name="split_lang",
    version="1.3.5",
    description="A package for splitting text by languages through concatenating over split substrings based on their language",
    long_description=read("README.md"),
    long_description_content_type="text/markdown",
    url="https://github.com/DoodleBears/langsplit",
    author="DoodleBear",
    author_email="yangmufeng233@gmail.com",
    license="MIT",
    packages=find_packages(),
    install_requires=[
        "fast_langdetect",
        "lingua-language-detector",
        "pydantic",
        "budoux",
    ],
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.9",
)
