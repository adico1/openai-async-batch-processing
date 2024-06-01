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
    author_email="adico1[at]gamil.com",
    description="A library to manage OpenAI ChatGPT batch jobs asynchronously.",
    url="https://github.com/adico1/openai_batch_sdk",
)
