from pathlib import Path
import setuptools
from setuptools import find_packages


VERSION = '0.0.1'
HERE = Path(__file__).parent.resolve()


long_description = (HERE / 'README.md').read_text(encoding='utf-8')


setuptools.setup(
    name='utmizer',
    version=VERSION,
    author='vovchykbratyk',
    author_email='eric@eaglefamily.io',
    description='Automatic projection of data to appropriate UTM zone',
    long_description=long_description,
    long_description_content_type='text/markdown',
    url='https://github.com/vovchykbratyk/UTM',
    install_requires=find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3"
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.8, <4',
)