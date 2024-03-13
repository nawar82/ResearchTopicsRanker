from setuptools import find_packages, setup

with open("requirements.txt") as f:
    content = f.readlines()
requirements = [x.strip() for x in content if "git+" not in x]

setup(
    name='research_topics_ranker',
    version="0.0.3",
    license="MIT",
    install_requires=requirements,
    packages=find_packages())
