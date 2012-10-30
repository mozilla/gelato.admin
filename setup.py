import os

from setuptools import setup, find_packages


setup(name='gelato.admin',
      version='0.0.1',
      description='Gelato admin',
      namespace_packages=['gelato'],
      long_description='',
      author='',
      author_email='',
      license='',
      url='',
      include_package_data=True,
      packages=find_packages(exclude=['tests']),
      install_requires=['django', 'tower'])
