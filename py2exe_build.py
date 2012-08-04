#coding: utf8


from distutils.core import setup
import py2exe

includes = []

options = {
    "py2exe": {
        "compressed": 1,
        "optimize": 2,
        "includes": includes,
        "bundle_files": 1
    }
}

setup(
    version = "1.0.0",
    description = "KumquatRoot files search",
    name = "KumquatRoot",
    options = options,
    zipfile = None,
    windows = [{
        'script':'KumquatRoot.py',
        'icon_resources':[( 1, 'KumquatRoot.ico' )]
    }],
    data_files = [
        'KumquatRoot.ico',
        'KumquatRoot_font.png',
    ],
)
