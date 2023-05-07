from setuptools import find_packages, setup

with open("app/README.md", "r") as f:
    long_description = f.read()

setup(
    name="graph_z",
    version="0.0.1",
    description="Structures to play with graphs",
    package_dir={"": "app"},
    packages=find_packages(where="app"),
    long_description="./app/README.md",
    long_description_content_type="text/markdown",
    url="",
    author="zelpha",
    author_email="tharunkothari@yahoo.com",
    license="MIT",
    classifiers=[
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3.9",
        "Operating System :: OS Independent",
    ],
    install_requires=["bson >= 0.5.10"],
    extras_require={
        "dev": ["pytest>=7.0", "twine>=4.0.2"],
    },
    python_requires=">=3.9",)