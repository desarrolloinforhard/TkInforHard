"""Compatibility setup script for editable installs."""

from setuptools import find_packages, setup


setup(
    name="TkInforHard",
    version="1.0.0",
    packages=find_packages(),
    include_package_data=True,
    install_requires=["ttkbootstrap>=1.10.1", "Pillow>=10.0.0"],
    python_requires=">=3.12",
)

