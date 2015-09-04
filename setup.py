classifiers = """\
Development Status :: 1 - Beta
Intended Audience :: Developers
License :: OSI Approved :: Apache Software License
Programming Language :: Python :: 2.7
Programming Language :: Python :: 3.3
Programming Language :: Python :: 3.4
Topic :: Database
Topic :: Software Development :: Libraries :: Python Modules
Operating System :: Unix
Operating System :: MacOS :: MacOS X
Operating System :: Microsoft :: Windows
Operating System :: POSIX
"""

import os
import platform
import sys
from distutils.core import Command
from distutils.dir_util import mkpath, remove_tree
from distutils.file_util import copy_file
try:
    from setuptools import setup
except ImportError:
    from ez_setup import use_setuptools
    use_setuptools()
    from setuptools import setup

extra_opts = {"test_suite": "tests",
              "tests_require": ["mongo-orchestration>=0.2", "requests>=2.5.1"]}

if sys.version_info[:2] == (2, 6):
    # Need unittest2 to run unittests in Python 2.6
    extra_opts["tests_require"].append("unittest2")
    extra_opts["test_suite"] = "unittest2.collector"

try:
    with open("README.rst", "r") as fd:
        extra_opts['long_description'] = fd.read()
except IOError:
    pass        # Install without README.rst


class InstallService(Command):
    description = "Installs Neo4j Doc Manager as a Linux system daemon"

    user_options = []

    def initialize_options(self):
        pass

    def finalize_options(self):
        pass

    def run(self):
        if platform.system() != 'Linux':
            print("Must be running Linux")
        elif os.geteuid() > 0:
            print("Must be root user")
        else:
            mkpath("/var/log/mongo-connector")
            mkpath("/etc/init.d")
            copy_file("./config.json", "/etc/mongo-connector.json")
            copy_file("./scripts/mongo-connector",
                      "/etc/init.d/mongo-connector")


class UninstallService(Command):
    description = "Uninstalls Mongo Connector as a Linux system daemon"

    user_options = []

    def initialize_options(self):
        pass

    def finalize_options(self):
        pass

    def remove_file(self, path):
        if os.path.exists(path):
            os.remove(path)
            print("removing '%s'" % path)

    def run(self):
        if platform.system() != 'Linux':
            print("Must be running Linux")
        elif os.geteuid() > 0:
            print("Must be root user")
        else:
            if os.path.exists("/var/log/mongo-connector"):
                remove_tree("/var/log/mongo-connector")
            self.remove_file("/etc/mongo-connector.json")
            self.remove_file("/etc/init.d/mongo-connector")

extra_opts['cmdclass'] = {
    "install_service": InstallService,
    "uninstall_service": UninstallService
}

setup(name='mongo-connector',
      version="2.2.dev0",
      author="Neo4j",
      author_email='',
      description='Neo4j Doc Manager',
      keywords=['mongo-connector', 'mongo', 'mongodb', 'solr', 'elasticsearch', 'neo4j'],
      url='https://github.com/neo4j-contrib/neo4j_doc_manager.git',
      license="http://www.apache.org/licenses/LICENSE-2.0.html",
      platforms=["any"],
      classifiers=filter(None, classifiers.split("\n")),
      install_requires=['pymongo >= 2.7.2, < 3.0.0',
                        'neo4j >= 2.0.0'],
      packages=["mongo_connector", "mongo_connector.doc_managers"],
      package_data={
          'mongo_connector.doc_managers': ['schema.xml']
      },
      entry_points={
          'console_scripts': [
              'mongo-connector = mongo_connector.connector:main',
          ],
      },
      **extra_opts
)