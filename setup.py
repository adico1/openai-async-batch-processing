from setuptools import setup, find_packages

setup(
    name="openai_batch_sdk",
    version="0.1.0",
    packages=find_packages(where="src"),
    package_dir={"": "src"},
    install_requires=[
        "openai",
        "python-dotenv",
    ],
    entry_points={
        'console_scripts': [
            'batch_processor = batch_processor.main_l1:main',
        ],
    },
    author="adico",
    author_email="adico1@gamil.com",
    description="An SDK for OpenAI ChatGPT batch API for a single process.",
    long_description=open('README.md').read(),
    long_description_content_type="text/markdown",
    url="https://github.com/adico1/openai_batch_sdk",
    classifiers=[
    "Programming Language :: Python :: 3",
    "License :: OSI Approved :: MIT License",
    "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
)
