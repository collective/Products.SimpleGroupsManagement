from setuptools import setup, find_packages
import os

version = '0.3.2'

setup(name='Products.SimpleGroupsManagement',
      version=version,
      description="A Plone utility that make possible for non-Manager users to manage some (specific) groups",
      long_description=open("README.txt").read() + "\n" +
                       open(os.path.join("docs", "HISTORY.txt")).read(),
      # Get more strings from http://www.python.org/pypi?%3Aaction=list_classifiers
      classifiers=[
        "Framework :: Plone",
        "Programming Language :: Python",
        "Development Status :: 4 - Beta",
        "Topic :: Software Development :: Libraries :: Python Modules",
        ],
      keywords='plone users groups acl',
      author='keul',
      author_email='sviluppoplone@redturtle.net',
      url='http://plone.org/products/simplegroupsmanagement',
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
