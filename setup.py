import setuptools

with open('README.md', 'r') as f:
    long_description = f.read()

setuptools.setup(
    name='PyLookup',
    version='0.2.1',
    packages=['pylookup'],
    license='MIT',
    author='Zach Bateman',
    description='PyLookup - Fuzzy-matching table autofill tool',
    long_description=long_description,
    long_description_content_type='text/markdown',
    url='https://github.com/zachbateman/pylookup.git',
    download_url='https://github.com/zachbateman/pylookup/archive/v_0.2.1.tar.gz',
    keywords=['LOOKUP', 'VLOOKUP', 'TABLE', 'MATCHING'],
    install_requires=['rapidfuzz', 'pandas', 'click'],
    classifiers=['Development Status :: 3 - Alpha',
                   'License :: OSI Approved :: MIT License',
                   'Programming Language :: Python :: 3',
                   'Programming Language :: Python :: 3.7',
                   'Programming Language :: Python :: 3.8',
                   'Programming Language :: Python :: 3.9',
                   'Programming Language :: Python :: 3.10',
                   ]
)
