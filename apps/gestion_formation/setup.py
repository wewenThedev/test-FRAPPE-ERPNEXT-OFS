from setuptools import setup, find_packages

with open("requirements.txt") as f:
	install_requires = f.read().strip().split("\n")

# get version from __version__ variable in gestion_formation/__init__.py
from gestion_formation import __version__ as version

setup(
	name="gestion_formation",
	version=version,
	description="roulement d\'une formation",
	author="Owen d\'ALMEIDA",
	author_email="dalmeidawilsons@gmail.com",
	packages=find_packages(),
	zip_safe=False,
	include_package_data=True,
	install_requires=install_requires
)
