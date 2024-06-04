"""
Setup script for the openai_batch_sdk package.

This script uses setuptools to package the openai_batch_sdk, which provides an SDK
for the OpenAI ChatGPT batch API for a single process. It specifies the package
metadata, dependencies, and entry points for command-line scripts.
"""

from setuptools import setup, find_packages

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setup(
    name="openai_batch_sdk",
    version="0.1.3",
    packages=find_packages(where="src"),
    package_dir={"": "src"},
    install_requires=[
        "openai==1.30.5",
        "python-dotenv==1.0.1",
    ],
    entry_points={
        "console_scripts": [
            "batch_processor = scripts.main:main",
        ],
    },
    author="adico",
    author_email="adico1@gmail.com",  # Ensure email is correct
    description="An SDK for OpenAI ChatGPT batch API for a single process.",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/adico1/openai_batch_sdk",
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.6",
    test_suite="tests",
    keywords="openai sdk batch api",
    project_urls={
        "Documentation": "https://github.com/adico1/openai_batch_sdk#readme",
        "Source": "https://github.com/adico1/openai_batch_sdk",
        "Tracker": "https://github.com/adico1/openai_batch_sdk/issues",
    },
)
