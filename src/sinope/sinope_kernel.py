"""A Sinope kernel for Jupyter."""
import sys
import typing

from metakernel import MetaKernel  # type: ignore


class MetaKernelSinope(MetaKernel):
    """The Sinope metakernel."""

    implementation = "Sinope Language Kernel"
    implementation_version = "1.0"
    language = "sinope"
    language_version = "0.1"
    banner = "Simple Newbie Object-oriented Programming Environment"
    language_info = {
        "mimetype": "text/plain",
        "name": "text",
        "file_extension": ".txt",
        "help_links": MetaKernel.help_links,
    }
    kernel_json = {
        "argv": [
            sys.executable,
            "-m",
            "sinope.sinope_kernel",
            "-f",
            "{connection_file}",
        ],
        "display_name": "Sinope Language Kernel",
        "language": "sinope",
        "name": "sinope_kernel",
    }

    def get_usage(self) -> str:
        """
        Return a usage information.

        Returns
        -------
        str
            the usage information

        """
        return "This is the Sinope kernel."

    def do_execute_direct(self, code: str, silent: bool = False) -> str:
        """
        Execute the given code.

        Parameters
        ----------
        code: str
            the code
        silent: bool = False
            whether the execution should be silenced

        Returns
        -------
        str
            the result

        """
        return code.rstrip()

    def repr(self, item: typing.Any) -> str:
        """
        See the overriden method.

        Parameters
        ----------
        item: typing.Any
            the data to be represented

        Returns
        -------
        str
            the string representation of the data

        """
        return repr(item)

    def do_apply(self, content, bufs, msg_id, reply_metadata):
        """Do not override."""

    def do_clear(self):
        """Do not override."""

    async def do_debug_request(self, msg):
        """Do not override."""


if __name__ == "__main__":
    MetaKernelSinope.run_as_main()
