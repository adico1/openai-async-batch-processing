from setuptools import setup, find_packages

setup(
    name="openai_batch_sdk",
    version="0.1.0",
    packages=find_packages(where="src"),
    package_dir={"": "src"},
    install_requires=[
        "openai",
    ],
    author="Your Name",
    author_email="your.email@example.com",
    description="A library to manage OpenAI ChatGPT batch jobs asynchronously.",
    url="https://github.com/yourusername/openai_batch_sdk",
)
