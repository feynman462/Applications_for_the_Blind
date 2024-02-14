import subprocess

script_path = "C:\\Users\\user\\Documents\\file_folder duplicate remover for the blind folder\\file_folder duplicate remover for the blind.py"

# Open a file in write mode to capture stderr output
with open("error_log.txt", "w") as error_file:
    try:
        # Run the script and capture any output to stderr (where syntax errors would be reported)
        subprocess.run(["python", script_path], check=True, stderr=error_file, text=True)
    except subprocess.CalledProcessError:
        # If a syntax error (or any other error) occurs, it should be written into error_log.txt
        pass
