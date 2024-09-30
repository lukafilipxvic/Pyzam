import setuptools

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setuptools.setup(
    name="pyzam",
    version="0.12.2",
    entry_points={"console_scripts": ["pyzam = pyzam.__main__:main"]},
    author="lukafilipxvic",
    description="A CLI music recognition tool for audio and mixtapes.",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/lukafilipxvic/Pyzam",
    install_requires=[
        "asyncio",
        "climage"
        "requests",
        "rich",
        "soundfile",
        "shazamio",
        "SoundCard",
    ],
    packages=setuptools.find_packages(),
    package_data={"pyzam": ["data/default_album_cover.png"]},
    python_requires=">=3.9",
    license="MIT",
    classifiers=[
        "Programming Language :: Python :: 3", 
        "License :: OSI Approved :: MIT License",
    ]
)
