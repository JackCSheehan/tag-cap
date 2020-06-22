import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="tagcap",
    version="0.1.5",
    author="Jack Sheehan",
    description="A simple and efficient HTML/XML parsing library written in pure Python",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/JackCSheehan/tag-cap",
    packages=setuptools.find_packages(),
    classifiers=[
        "Topic :: Software Development :: Libraries :: Python Modules",
        "Topic :: Text Processing :: Markup :: HTML",
        "Topic :: Text Processing :: Markup :: XML",
        "Intended Audience :: Developers",
        "Development Status :: 4 - Beta",
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
)
