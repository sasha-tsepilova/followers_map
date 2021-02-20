import setuptools

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setuptools.setup(
    name="followers_map",
    version="0.0.1",
    author="Oleksandra Tsepilova",
    author_email="oleksandra.tsepilova@ucu.edu.ua",
    description="Building map with 50 Twitter followers",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/sasha-tsepilova/follower_map",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
)