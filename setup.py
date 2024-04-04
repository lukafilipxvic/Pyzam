import setuptools

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setuptools.setup(
    name="pyzam",
    version="0.1",
    entry_points={
        'console_scripts': [
            'pyzam = pyzam.__main__:main'
        ]
    },
    author="lukafilipxvic",
    description="A CLI music recognition tool for audio and mixtapes using Python.",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/lukafilipxvic/Pyzam",
    install_requires=[
        "asyncio",
        "rich",
        "soundfile",
        "shazamio",
        "SoundCard",
],
    packages=setuptools.find_packages(),
    python_requires=">=3.9",
)