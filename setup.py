"""
Zoe Game Engine Package Setup
"""

from distutils.core import setup

setup(
    name             = 'Zoe Game Engine',
    version          = '0.0.0',
    author           = 'Zac Hester',
    author_email     = 'zac.hester@gmail.com',
    license          = 'BSD',
    packages         = [ 'zge' ],
    scripts          = [],
    description      = 'Simple Game Engine Package',
    long_description = open( 'README.md' ).read(),
    install_requires = [ 'pygame >= 1.9.1' ]
)

