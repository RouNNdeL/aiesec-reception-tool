from setuptools import setup, find_packages

setup(
    name='receptiontool',
    version="0.0.1",
    author="Krzysztof Zdulski",
    author_email="krzys.zdulski@gmail.com",
    description="Tool for importing EP applications from AIESEC EXPA to Trello",
    url="https://github.com/RouNNdeL/aiesec-reception-tool",
    packages=find_packages(exclude=['tests']),
    python_requires='>=3.9',
    scripts=['bin/receptiontool'],

    classifiers=[
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.9",
        "Operating System :: OS Independent",
    ],
)

