from setuptools import setup, find_packages
import os

version = '0.4.2.dev0'

setup(name='Products.SimpleGroupsManagement',
      version=version,
      description="A Plone utility that let non-Manager users able to manage some (specific) groups",
      long_description=open("README.rst").read() + "\n" +
                       open(os.path.join("docs", "HISTORY.rst")).read(),
      # Get more strings from http://www.python.org/pypi?%3Aaction=list_classifiers
      classifiers=[
        "Framework :: Plone",
        "Framework :: Plone :: 4.0",
        "Framework :: Plone :: 4.1",
        "Framework :: Plone :: 4.2",
        "Framework :: Plone :: 4.3",
        "Programming Language :: Python",
        "Programming Language :: Python :: 2.7",
        "Development Status :: 5 - Production/Stable",
        ],
      keywords='plone users groups acl',
      author='keul',
      author_email='luca@keul.it',
      url='https://github.com/keul/Products.SimpleGroupsManagement',
      license='GPL',
      packages=find_packages(exclude=['ez_setup']),
      namespace_packages=['Products'],
      include_package_data=True,
      zip_safe=False,
      install_requires=[
          'setuptools',
          # -*- Extra requirements: -*-
      ],
      entry_points="""
      # -*- Entry points: -*-
      """,
      )
