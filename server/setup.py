import setuptools

packages = setuptools.find_packages(exclude=['docs', 'tests'])
setuptools.setup(name='shnootalk_cc_server', version='testing', packages=packages)
