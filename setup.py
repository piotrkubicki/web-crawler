from distutils.core import setup, find_packages

install_requires = [
    'bs4~=0.0.1',
    'requests~=2.25.1',
]
dev_requires = [
    "pytest~=6.2.2",
    "black~=20.8b1",
]

setup(name='web-crawler',
    version='1.0',
    description='Web crawler',
    author='Piotr Kubicki',
    author_email='pkubicki44@gmail.com',
    url='',
    packages=find_packages(),
    install_requires=install_requires,
    setup_requires=['pytest-runner'],
    extras_requires={
        'dev': dev_requires,
    },
)
