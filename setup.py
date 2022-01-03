from setuptools import setup


setup(name = 'robotframework-rfserver',
      version = '0.1.0',
      description = 'Simple running keywords server',
      author = 'Simo Soininen',
      author_email = 'soinisi@gmail.com',
      license = 'MIT',
      packages = ['RFServer'],
      install_requires = ['Robotframework>3.0.0', 'schema', 'python-dateutil', 'packaging', 'pyyaml'],
      entry_points = {
            'console_scripts': ['rf_server = RFServer.rfserver_start:run'],
      },
      keywords = ['robotframework', 'server'])