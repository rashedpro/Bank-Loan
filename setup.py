from setuptools import setup, find_packages

with open("requirements.txt") as f:
	install_requires = f.read().strip().split("\n")

# get version from __version__ variable in bank_loan/__init__.py
from bank_loan import __version__ as version

setup(
	name="bank_loan",
	version=version,
	description="this app for bank loan feature",
	author="slnee",
	author_email="rashed.alqadi@slnee.com",
	packages=find_packages(),
	zip_safe=False,
	include_package_data=True,
	install_requires=install_requires
)
