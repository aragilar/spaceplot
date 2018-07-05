import setuptools

import versioneer

DESCRIPTION_FILES = ["pypi-intro.rst"]

long_description = []
import codecs
for filename in DESCRIPTION_FILES:
    with codecs.open(filename, 'r', 'utf-8') as f:
        long_description.append(f.read())
long_description = "\n".join(long_description)


setuptools.setup(
    name = "spaceplot",
    version = versioneer.get_version(),
    packages = setuptools.find_packages(),
    install_requires = [
        "matplotlib>=2.2",
    ],
    python_requires = '>=3.4',
    author = "James Tocknell",
    author_email = "aragilar@gmail.com",
    description = "Plot multidimensional values against each other.",
    long_description = long_description,
    license = "3-clause BSD",
    keywords = "matplotlib",
    url = "https://spaceplot.readthedocs.io",
    classifiers=[
        'Development Status :: 3 - Alpha',
        'Intended Audience :: Developers',
        'Intended Audience :: Science/Research',
        'License :: OSI Approved :: BSD License',
        'Topic :: Scientific/Engineering',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3 :: Only',
    ],
    cmdclass=versioneer.get_cmdclass(),
)
