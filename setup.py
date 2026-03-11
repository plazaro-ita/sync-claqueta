from setuptools import setup, find_packages

setup(
    name="sync-claqueta",
    version="0.1.0",
    package_dir={"": "src"},
    packages=find_packages(where="src"),
    install_requires=[
        "numpy",
        "opencv-python",
        "librosa",
        "moviepy"
    ],
    entry_points={
        "console_scripts": [
            "claqueta=claqueta.main:main",
        ]
    },
    author="plazaro",
    description="A tool to find a clap sound in videos and cut them.",
)
