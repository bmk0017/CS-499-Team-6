# ReadMe #
## Setting up an Environment (VsCode)
 1. Use File > Open Folder and navigate to the folder you want to set up the environment in.
    This can be a new folder or the the folder that your current repo is in.
 2. Use Ctrl + Shift + P to bring up "Show and Run Commands".
 3. Search for the "Python: Create Environment..." command and select the command to run it.
    This requires you to have Python installed. Additionally, you may need to install the VsCode Python Extension
    which can be found in the Extensions Tab on the left (Ctrl + Shift + X).
 4. You should now have a .venv file and the environment is ready for the repository.

## Managing Dependencies
(The repo should already be cloned)
### Installing/Updating
1. Open up a terminal in your cloned repo folder (View > Terminal).
2. run the `pip install -r requirements.txt` in order to install or updated any dependencies.

### Updating the Dependencies List
If you add or update any dependencies follow these instructions to update the requirements.txt.
1. Open up a terminal in your cloned repo folder (View > Terminal).
2. run the `pip freeze > requirements.txt` command in order to update requirements.txt.
