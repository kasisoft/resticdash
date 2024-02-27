from setuptools import setup, find_packages

setup(
    name='resticdash',
    version='0.1.1',
    url='https://github.com/kasisoft/resticdash',
    license='MIT',
    author='Daniel Kasmeroglu',
    author_email='daniel.kasmeroglu@kasisoft.com',
    description='A simple dashboard to monitor restic backups',
    package_dir={"": "src/main"},
    packages=find_packages("src/main"),
)
