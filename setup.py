from setuptools import setup, find_packages

setup(
    name="coolme",
    version="0.1",
    packages=find_packages(),
    install_requires=["Click", "PyYAML"],
    entry_points={
        "console_scripts": [
            "CoolMe = coolme.cli:cli",
        ],
    },
)
