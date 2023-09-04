Pegasus Tool
This Pegasus tool was designed to help manage metadata files and assets used by the Pegasus Frontend program. It can help find missing image assets, edit genres, and convert to or from EmultionStation gamelist.xml files.

Required Modules: PySimpleGUI, pygame

For ideal functionality you should keep all your rom folders under a shared base folder, such as Roms. Inside each rom folder should be a media folder, with subfolders such as screenshot, box2dfront, and videos inside of it. Each of those should have an image file that matches the rom file names.

Add Assets -  Add asset links to metadata file
Backup Metadata -  Backup all metadata files to zip archive
Check Files -  Find missing and extra files in a rom path
Edit Genres -  Rename genres within one or more metadata files
Export XML -  Export gamelist.xml based on metadata.pegasus.txt
Hide Disks -  Hides multi-disc ISOs and creates M3U playlist
Import XML -  Create Pegasus metadata based on a gamelist.xml
Make Image Mixes -  Create collage from screenshot, box, and logo
Options -   Edit global options and access Theme selector
Remove Assets -  Remove asset links from metadata

Add Assets
Add asset links to metadata file

This tool adds asset links to the metadata. Select a source folder where roms or links are located. Then select the folders for each asset type, such as screenshot, fanart, and video. Images matching the rom's filename will be searched for and added to the metadata file.

Add Missing Files -  Links for images that cannot be found will still be added. The extension chosen from the drop down box will be assumed.
Keep Old Assets -  Existing asset links will be removed by default. Check this box to keep them. Duplicates may be created in this case.
Save -  Save changes to metadata.pegasus.txt. A backup will be created first.

Backup Metadata
Backup all pegasus metadata files found into a zip file.

Select a source folderselected and press ok button. All metadata.pegasus.txt files found in the folder and its subfolders are added to a metadata.pegasus.?.zip file in the source folder, where ? is a date stamp.

Check Files
Find missing and extra files in a rom path.

This tool scans a rom folder for games and for matching assets. It reports missing images in each media subfolder, images that don't match a game, and games that lack entries in the metadata file.

Select a source folder and press Scan. A list of categories will appear in the text box. Click one to display a list of items in that category. The category name is shown as the first item of the list. Click it to return to the initial category list.

By using the Cut or Copy options you may copy the name of a file into the clipboard. This allows you to easily search for images on the web or renme files to complete or correct your game media assets. You may also copy the entire report or view it in a text editor.

On Click Options
Ignore -  Clicking a list item does nothing
Hide -  Clicking a list item removes it from the list
Launch -  Clicking on an extra image will open it in your default viewer. Clicking on a missing image will open the metadata file.
Copy -  Clicking a list item copies it into the clipboard
Cut -  Clicking a list item copies it to the clipboard and removes it from the list
Delete -  Clicking on an extra image will delete the file. Clicking on a missing image will delete the game's metadata from the metadata.pegasus.txt file

Other Buttons
Metadata -  Open the metadata.pegaus.txt file
Copy -  Copy the entire report into your clipboard
Open -  Open the entire report in a text editor defined in this program's options

Edit Genres
Rename genres within one or more metadata files

This tool helps you consolidate genres into managable lists or just rename them as preferred. Select a source folder and press scan. Metadata in all subfolders will be scanned. A list of all genres will appear with a count of the games that use it.

Click on a genre to get a list of all games that use it, along with all the genres that each of those games use. Click Back or the top top line of the game list to return to the genre list. When you're done press Export to save changes to all the metadata.pegasus.txt files. Backups will be created first.

On Click Options
View -  Clicking on a genre opens a list of games using it
Rename -  Clicking on a genre opens a dialog allowing you to rename it
Select -  Clicking on genres multi-select them so you can rename them all at once

Default Text Options
Blank -  The rename dialog opens blank, without any default text
Clicked -  The rename dialog opens with the genre's name for easy editing
Previous -  The rename dialog opens with the previous entry for easy reapplying

Other Buttons
Back -  Return from the game list to the genre list
Export -  Export changes to all metadata files after backing them up
Rename -  Rename the currently selected genre or genres

Export XML
Export Pegasus metadata to a gamelist.xml file

This tool reads a metadata.pegasus.txt file and saves it as an EmulationStation gamelist.xml file. Select a source folder that includes pegasus metadata and any desired image assets. Then select which image asset you want for each game's image and thumbnail. You may select a folder of images or existing asset metadata to add, or leave the drop-down blank to skip it.
If a folder is selected and an image is missing for a particular game, the selected extension will be used as a placeholder, but only if the Add Missing Files options is enabled. Press save to create gamelist.xml in the source folder. If the file already exists it will be renamed to gamelist.xml.b, possibly overwriting it.


Hide Disks
Hides multi-disc ISOs and creates M3U playlist

Select a folder. All pegasus metadata files in the folder and its subfolders are scanned and the files with '(disc X)' tags in their filename will be added to the ignored files list. If there is no M3U playlist for the game it will be created.

Example files
Resident Evil (disk 1).chd
Resident Evil (disk 2).chd
Resident Evil.m3u

The two chd files will be set to ignore in the metadata.pegasus.txt file. The m3u file will be created if necessary.


Import XML
Import Pegasus metadata to a gamelist.xml file

This tool reads an EmulationStation gamelist.xml file and saves it as a metadata.pegasus.txt file. Select a source folder that includes a gamelist.xml file and any desired image assets. Then select which Pegasus image asset you want to assign the gamelist's image and thumbnail values to.

No Pegasus asset link will be created if the gamelist asset doesn't exist. You can add them using the Add Asset tool.


Make Image Mixes
Create image mix collages from screenshot, box, and logo images

This tool generates image mixes similar to various scraper sites provide by plotting a logo and box art over a screenshot or similar image. It only supports 3 image mixes.

Select a source folder with image subfolders. A list of image folders will populate the dropdown boxes for background, box, and logo. Select the folder you want to use for each of them. Then press scan. A report of missing images will appear in the text box. Press Build to create the image mixes in the mix folder.


Options
Edit global options and access Theme selector

A list of all programs is given. Change them as desired. Changes are saved when okay is pressed. These changes only apply to tool windows opened after changes are saved, not to alredy open windows.

Minimal error checking is performed. If the program stops working properly after changing an option you can delete options.dat to restore defaults.

Theme Menu
There is a Theme button allowing you to change the appearance and size of the program. Like other options, changes made to the theme only apply to newly opened windows.


Remove Assets
Remove asset links from metadata

Select a source path press okay. All metadata.pegasus.txt files will be scanned and all asset links will be removed from them. This is useful if you prefer to have Pegasus load images using their default path and filename and can shrink metadata files a bit.


