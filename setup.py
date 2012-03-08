import os

from setuptools import setup, find_packages

here = os.path.abspath(os.path.dirname(__file__))
README = open(os.path.join(here, 'README.txt')).read()
CHANGES = open(os.path.join(here, 'CHANGES.txt')).read()

requires = ['gevent', 'bottle']

setup(name='happy',
      version='0.1',
      description='HAProxy RESTful API',
      long_description=README + '\n\n' +  CHANGES,
      author='Damien Churchill',
      author_email='damien.churchill@ukplc.net',
      url='',
      keywords='haproxy',
      packages=find_packages(),
      include_package_data=True,
      zip_safe=False,
      install_requires=requires,
      tests_require=requires,
      test_suite="happy",
      entry_points = """\
      [console_scripts]
      happyd = happy:main
      """
      )

