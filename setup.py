from setuptools import setup, find_packages

# Read the contents of the README file
with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setup(
    name="deeplogic_assignment",
    version="0.1.0",
    author="Siddharth Singh Patel",
    author_email="patelsiddharth715@gmail.com",
    description="AI-Powered Document Understanding and Processing Pipeline",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/Siddharth-715/deeplogic_assignment",
    packages=find_packages(),
    include_package_data=True,
    install_requires=[
        "streamlit",
        "PyMuPDF",
        "pytesseract",
        "pdf2image",
        "Pillow",
        "python-dotenv",
        "langchain-core",
        "langchain-community",
        "langchain-groq"
    ],
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
    entry_points={
        'console_scripts': [
            'run_app=part_three:main',  
        ],
    },
)