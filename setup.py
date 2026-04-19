"""
py-captcha - Python behavioral captcha library

Author: Awen
Date: 2026/04/19
Email: wengaolng@gmail.com

"""
from setuptools import setup, find_packages

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setup(
    name="py-captcha",
    version="0.0.1",
    author="Awen",
    author_email="wengaolng@gmail.com",
    description="Python behavioral captcha library with click, slide, drag, and rotate challenges",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/wenlng/py-captcha",
    packages=find_packages(),
    classifiers=[
        "Development Status :: 4 - Beta",
        "Intended Audience :: Developers",
        "Topic :: Software Development :: Libraries :: Python Modules",
        "License :: OSI Approved :: Apache Software License",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "Programming Language :: Python :: 3.12",
    ],
    python_requires=">=3.7",
    install_requires=[
        "Pillow>=8.0.0",
        "numpy>=1.19.0",
    ],
    extras_require={
        "dev": [
            "pytest>=6.0",
            "pytest-cov>=2.0",
            "black>=21.0",
            "flake8>=3.8",
        ],
    },
)

