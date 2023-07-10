# User-End Configuration

## Application
The application.py file is the main file that runs the application. It contains the code for the Tkinter gui, which is the front end for user inputs. Users can add, change, and remove files from the configuration. The config pulls its current working list of files from the RPiZ, and as necessary will download files to edit them. After the desired changes have been made, it first uploads a manifest to the RPiZ, indicating what changes have been made and how to handle them. Then it uploads any necessary files (which would be those changed or created), after which the RPiZ reloads its running configuration to enable the new setup. While the code for the GUI itself resides in the application.py file, the actual interpretation of the inputs is broken out into the interpreter.py file, which contains the logic for the settings configuration of the app itself, the interpreter, and the help menu

## config/
This is location where all the files are downloaded to and storage. As new files are generated, they are also placed here. After uploading to the RPiZ, this folder will not clear itself, as that saves uploads to the RpiZ. However, if the user chooses to delete a file, a command will be sent to the RPiZ to delete the file on its end as well.

## Other files
the settings.conf has all of the settings for the app, and the sountrack.wav is the soundtrack. Deleting either of these files will result in the program crashing. The manual.utf8 is the man pages for the commands themselves, you can look in the file for more info.
