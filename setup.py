import setuptools


with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="arbol", # Replace with your own username
    version="2020.11.6",
    author="Loic A Royer",
    author_email="",
    description="arbol -- Arborescent Printouts in Python",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/royerlab/arbol",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
)

