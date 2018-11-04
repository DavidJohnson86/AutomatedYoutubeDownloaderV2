# A simple setup script to create an executable using cx_freeze. This also
# demonstrates the method for creating a Windows executable that does not have
# an associated console.
#
# Run the build process by running the command 'python setup.py bdist_msi'
#
# If everything works well you should find a subdirectory in the build
# subdirectory that contains the files needed to run the application and installer.

from cx_Freeze import setup, Executable
import os
import sys
PYTHON_INSTALL_DIR = os.path.dirname(os.path.dirname(os.__file__))
os.environ['TCL_LIBRARY'] = "c:\\Python36\\tcl\\tcl8.6"
os.environ['TK_LIBRARY'] = "c:\\Python36\\tcl\\tk8.6"


setup(name='Youtube_Downloader',
      version ='1.1',
      description='Youtube_Downloader',
      options={"build_exe": {"includes":["YotubeDownloader_Mock","easygui","Search","urllib","random"],
      'include_files':[
            os.path.join(PYTHON_INSTALL_DIR, 'DLLs', 'tk86t.dll'),
            os.path.join(PYTHON_INSTALL_DIR, 'DLLs', 'tcl86t.dll'),
			os.path.dirname(os.path.realpath(__file__))+'\\Data'],"packages": ["urllib"]}},
      executables = [Executable("GUI.py")])
