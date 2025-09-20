from setuptools import setup,find_packages

with open("requirements.txt") as f:
    requirements = f.read().splitlines()

setup(
    name="yed_interview",
    version="0.1",
    author="Cakir",
    packages=find_packages(),
    install_requires = requirements,
)