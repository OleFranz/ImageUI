from setuptools import setup, find_packages

setup(
    name="ImageUI",
    version="0.29",
    description="A package for easily creating UIs in Python, mainly using OpenCV's drawing functions.",
    long_description=open("README.md").read(),
    author="OleFranz",
    license="GPL-3.0",
    packages=["ImageUI"],
    python_requires=">=3.9",
    install_requires=[
        "mouse",
        "numpy",
        "pillow",
        "pynput",
        "pywin32",
        "keyboard",
        "opencv-python",
        "deep-translator",
    ],
)