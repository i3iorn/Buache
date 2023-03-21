from setuptools import setup, find_packages

setup(
    name='Buache',
    version='0.0.1',
    description='An address selection and verification tool',
    author='Björn Schrammel',
    author_email='buache@bjosch.tk',
    url='https://github.com/i3iorn/buache',
    packages=find_packages(),
    install_requires=[
        'requests'
    ],
    classifiers=[
        'Development Status :: 3 - Alpha',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
        'Programming Language :: Python :: 3.9',
        'Programming Language :: Python :: 3.10',
    ],
)
