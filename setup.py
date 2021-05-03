import setuptools

with open("README.md", "r") as readme:
    long_description = readme.read()

with open("requirements.txt", "r") as reqs:
    install_requires = reqs.read()

with open("requirements-dev.txt", "r") as reqs:
    dev_requires = reqs.read()

setuptools.setup(
    name="app",
    version="1.0",
    author="Matias Riquelme",
    author_email="matt.riquelme.a@gmail.com",
    description="Python base architecture example",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/what-matt/flask_base",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.8',
    install_requires=install_requires,
    extras_require={
        "dev": dev_requires
    }
)
