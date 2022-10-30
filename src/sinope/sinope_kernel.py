"""A Sinope kernel for Jupyter."""
from metakernel import MetaKernel
import sys


__version__ = "0.1.0"

class MetaKernelSinope(MetaKernel):
    implementation = 'Sinope Language Kernel'
    implementation_version = '1.0'
    language = 'sinope'
    language_version = '0.1'
    banner = "Simple Newbie Object-oriented Programming Environment"
    language_info = {
        'mimetype': 'text/plain',
        'name': 'text',
        # ------ If different from 'language':
        # 'codemirror_mode': {
        #    "version": 2,
        #    "name": "ipython"
        # }
        # 'pygments_lexer': 'language',
        # 'version'       : "x.y.z",
        'file_extension': '.txt',
        'help_links': MetaKernel.help_links,
    }
    kernel_json = {
        'argv': [
            sys.executable, '-m', 'sinope.sinope_kernel', '-f', '{connection_file}'],
        'display_name': 'Sinope Language Kernel',
        'language': 'sinope',
        'name': 'sinope_kernel'
    }

    def get_usage(self):
        return "This is the Sinope kernel."

    def do_execute_direct(self, code):
        return code.rstrip()

    def repr(self, data):
        return repr(data)


if __name__ == '__main__':
    MetaKernelSinope.run_as_main()

