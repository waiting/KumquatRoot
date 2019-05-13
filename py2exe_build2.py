# coding=gbk

from distutils.core import setup
import py2exe

class Target:
    def __init__(self, **kw):
        # for the versioninfo resources
        self.version = "1.0.0"
        self.company_name = "your company"
        self.copyright = "your copyright"
        self.name = "Name about this program's description"

        self.__dict__.update(kw)

#Put content in *.exe.manifest to here, the key to resolve XP sytle after pack
manifest_template = '''
<?xml version="1.0" encoding="UTF-8" standalone="yes"?>
<assembly xmlns="urn:schemas-microsoft-com:asm.v1" manifestVersion="1.0">
<assemblyIdentity version="%(ver)s" processorArchitecture="X86" name="%(prog)s" type="win32" />
<description>%(prog)s</description>
    <dependency>
        <dependentAssembly>
            <assemblyIdentity type="win32" name="Microsoft.VC90.CRT" version="9.0.21022.8" processorArchitecture="x86" publicKeyToken="1fc8b3b9a1e18e3b" />
        </dependentAssembly>
    </dependency>
    <dependency>
        <dependentAssembly>
            <assemblyIdentity type="win32" name="Microsoft.Windows.Common-Controls" version="6.0.0.0" processorArchitecture="X86" publicKeyToken="6595b64144ccf1df" language="*" />
        </dependentAssembly>
    </dependency>
</assembly>
'''
RT_MANIFEST = 24

#detail setting about the target program.
SyncList = Target(
    # The first three parameters are not required, if at least a
    # 'version' is given, then a versioninfo resource is built from
    # them and added to the executables.
    name = "KumquatRoot",
    company_name = "KumquatSoft Studio",
    copyright = "2012",
    version = "1.0.0.0",
    description = "KumquatRoot files search.",

    # what to build, script equals your program's file name
    script = "KumquatRoot.py",
    other_resources = [(RT_MANIFEST, 1, manifest_template % dict(prog="KumquatRoot",ver="1.0.0.0"))],
    #icon.ico is the target program's icon
    icon_resources = [(1, "KumquatRoot.ico")],
    #target exe file name is SyncList here
    dest_base = ""
)

#deal with some case after packing, run with error "LookupError: unknown encoding: utf-8"
includes = ["encodings", "encodings.*"]
excludes = []

setup(
    options = {
        "py2exe": {
            # typelib for WMI
            #"typelibs": [('{565783C6-CB41-11D1-8B02-00600806D9B6}', 0, 1, 2)],
            # create a compressed zip archive
            "compressed": 1,
            "optimize": 2,
            #"ascii": 1,
            "bundle_files": 1,
            "includes": includes,
            "excludes": excludes
        }
    },
    # The lib directory contains everything except the executables and the python dll.
    # Can include a subdirectory name.
    #zipfile = None,

    #remove the DOS window when run the program, replace "console" with "windows"
    windows = [SyncList],

    #all file list below will be include in the pack folder.
    data_files = [
        'KumquatRoot.ico',
        'KumquatRoot_font.png',
        'KumquatRoot_Help.html',
    ]
)
