from setuptools import setup, find_packages

setup(
    name="Santase",
    version="0.1",
    packages=find_packages(),
    install_requires=['PyQt5'],
    author="Nikolay Mantarov",
    author_email="hukyy@abv.bg",
    description="Card game",
    license="GNU GPL v2",
    keywords="Santase",
    url="https://github.com/Hukyy/Santase",
    classifiers=[
        "Development Status :: 2 - Pre-Alpha",
        "Environment :: X11 Applications :: Qt",
        "Intended Audience :: End Users/Desktop",
        "License :: OSI Approved :: GNU General Public License v2 (GPLv2)",
        "Natural Language :: English",
        "Operating System :: Microsoft :: Windows :: Windows 7",
        "Programming Language :: Python :: 3.5",
        "Topic :: Games/Entertainment"
    ],
    entry_points={
          'console_scripts': [
              'Santase = Santase.__main__:main'
          ]
      }
)
