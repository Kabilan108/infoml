#by AhmetSacan
# You can make a copy of this file on your own computer and make necessary changes.

#Add your computer-specific folders here:
CUSTOMDATADIRS = ['/Users/hayerk/Dropbox/database/', 'C:/Users/rawan/Dropbox/database/','C:/Users/James/Dropbox/database/', 'db.sqlite' ];
CUSTOMDBFILES = ['C:/Users/James/Dropbox/database/db.sqlite', '/Users/hayerk/Dropbox/database/db.sqlite', 'C:/Users/rawan/Dropbox/database/db.sqlite' ];
CUSTOMPATH = ['/Users/hayerk/Dropbox/database/geckodriver', 'C:/Users/rawan/Dropbox/database/geckodriver', 'C:/Users/James/Dropbox/database/geckodriver', 'd:/data/apt/exe/geckodriver.w64']

import bmes
bmes.trycustomdatadirs(CUSTOMDATADIRS);
bmes.trycustomdbfiles(CUSTOMDBFILES);
bmes.trycustompath(CUSTOMPATH);


if __name__ == "__main__":
	bmes.printsettings()
