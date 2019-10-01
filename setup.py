from setuptools import setup

setup(
    name="fontstamp",
    description="Embed a subset of your font in an svg file",
    version="0.0.1",
    url="https://github.com/marksteve/fontstamp",
    author="Mark Steve Samson",
    author_email="hello@marksteve.com",
    long_description=open("README.md").read(),
    long_description_content_type="text/markdown",
    install_requires=open("requirements.txt").readlines(),
    py_modules=["fontstamp"],
)
