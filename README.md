# twitter2gp
This python3-based program will download **all media posted by a given twitter user** that is tagged with the hashtag `#NintendoSwitch` (by default; you can change the key hashtag on line 65 in `main.py`) and **upload it to a Google Photos account**.
The program is designed to run on linux, and was most recently tested on Kubuntu LTS 18.04. 
It utilizes a command-line utility called `gphotos-uploader-cli`, [available on GitHub](https://github.com/gphotosuploader/gphotos-uploader-cli). Version 1.01 of that utility is bundled in this repo (under MIT license), but all future versions that retain backwards-compatibility should work as well: just drop them in the same place as the included version with the same file name.

# Setup
It has yet to be tested, but running `setup.sh` in your terminal should pull up all the prompts you need automatically. You may want to consult the [`gphotos-uploader-cli` configuration manual](https://github.com/gphotosuploader/gphotos-uploader-cli/blob/master/.docs/configuration.md), for when you are prompted with that, as it has detailed instructions for all the options within.

Once the program has been installed and configured, simply execute `main.py`. You may want to set this up as a cron job so that it checks for new things periodically.

# Uninstalling
I haven't tested it, but `purge.sh` should delete all the main files that this program uses. The only other loose ends to clean up would be the `gphotos-uploader-cli` keyring, which is stored in `.local/share/keyrings` by default, although it may be stored in a different keyring (e.g. `kwallet`, as I recommend for KDE users) depending on how you configured the utility.

# Issues
If you have any problems, raise an issue on this repository and I'll see what I can do to help. **Please** include your OS version, any installation or configuration quirks beyond the defaults, and clear steps to reproduce your problem.
