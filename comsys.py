# ---------------------------------------------------------------------------------------------
# ComSys Tools V0.01
# Support: Python 2.7, 3.3
# ---------------------------------------------------------------------------------------------

# Import the necessary resources
from bs4 import BeautifulSoup
import tarfile, shutil, glob, os, re, sys, time, platform

# Try for Python 3.3
try:
	import urllib.request
	web = urllib.request
# Fall back to Python 2.7
except ImportError:
	import urllib
	web = urllib

# Verbose output
vOutput = sys.stdout.write
vFlush = sys.stdout.flush

# Work/Target directories
args = sys.argv
workDir = r'' + args[1]
targetDir = r'' + args[2]

# Make the workDir if it doesn't exist
if not os.path.exists(workDir): os.makedirs(workDir)

# Make the targetDir if it doesn't exist
if not os.path.exists(targetDir): os.makedirs(targetDir)

# Initialize the script
vOutput('\nInitializing....\n\n')

# Report the download percentage
def report(count, blockSize, totalSize):
  	percent = int(count*blockSize*100/totalSize)
  	vOutput("\r%d%%" % percent + ' complete')
  	vFlush()

# Download via BeautifulSoup
def soup(url1,str,rename,url2='',index=''):

	# Initialize the array for the files that will be scraped
	fileList = []

	# Invoke BeautifulSoup
	soup = BeautifulSoup(web.urlopen(url1))

	# Search for anchor tags hrefs that contain a specific string
	for link in soup.findAll('a', href=re.compile(str)):
		# Grab the link
		app = link.get('href')

		# Add all the files to a list
		fileList.append(app)

	# Isolate the first item in the list, aka the newest item
	name = fileList[0].split('/')[-1]

	# Specify an index for fileList if required
	if index != '':
		name = fileList[index]

	# Set url1 to url2 when necessary
	if url2 != '':
		url1 = url2

	# Set the new filename
	urlList[url1 + name] = rename

def getRemoteFile(item, setName=''):

	# Get the URL
	response = web.urlopen(item)

	# Get the filename from the URL
	if setName != '':
		name = setName
		fetchName = item.split('/')[-1]
	else:
		name = item.split('/')[-1]
		fetchName = name

	# Enable transferring to target directory
	transfer = 1

	# Display an error message if the file is unavailable because of a 404	
	if response.getcode() == 404:

		vOutput('\rError 404: Failed to fetch ' + name + '\n\n')
		vFlush()
		return

	# Get the "last-modified" information of the file from the file header
	time_data = str(response.info().get('last-modified'))

 	# Output a status message
	vOutput('\rFetching ' + fetchName + '...\n')

	# OS-based delimiter for FS pathnames
	delimit = '/'

	# Set delimiter for Windows
	if platform.system() == 'Windows':
		delimit = '\\'

	# Strip the extension from the filename
	fileID = os.path.splitext(workDir + name)[0].split(delimit)[-1]

	# Check to see if we already have the file in the target directory
	if os.path.isfile(targetDir + fileID + '.tar.gz') != 1:

		targetPath = 0

	else:

		targetPath = 1

	if os.path.isfile(workDir + name) == 1:

		# Get the "last-modified" information of the file from the remote file
		local = os.stat(workDir + name).st_mtime

		# Make sure the response value is set before we attempt to download the file
		if time_data != 'None':

			# Convert the "time_data" output to an number thats compatible with the local file
			server = time.mktime(time.strptime(time_data, "%a, %d %b %Y %H:%M:%S GMT"))

		else:

			server = int(local + 1)

		# Compare the "last-modified" dates of the local file and the remote file
		if local < server:

			# Fetch the file if the remote version is newer than the local version
			web.urlretrieve(response.geturl(), workDir + name, reporthook=report)

		else:

			# Turn off transfer mode if the compressed file exits in the targetDir path. If not we will transfer.
			if targetPath != 0: 

				# Turn off transfer because we dont need it.
				transfer = 0

		# Output a status message
		vOutput('\r' + name + ' is up-to-date.\n\n')

	else:
		# Fetch the file
		web.urlretrieve(response.geturl(), workDir + name, reporthook=report)
		vOutput("\rDownload complete, saved as %s" % (name) + '\n\n')

	# Transfer & compress the files
	if transfer != 0:

		# Copy the files in the temp directory to the target directory
		allFiles = glob.glob(workDir + '*.*')
		filePath = workDir + name
		vOutput('\rTransferring ' + name + '...\n');
		shutil.copy(filePath,targetDir);
		vOutput("\rTransfer complete, saved as %s" % (name) + '\n\n');
	
		# Create a list with list comprehension & compress files in the target directory
		allFiles = glob.glob(targetDir + '*.*')

		for filePath in allFiles:

			if "tar.gz" not in filePath:

				thisFile = filePath.split(delimit)[-1]
				tarHandler = tarfile.open(targetDir + fileID + ".tar.gz", "w:gz")
				vOutput('\rCompressing ' + thisFile + '...\n');
				tarHandler.add(filePath);
				os.remove(filePath); vOutput("\rCompression complete, saved as %s" % (fileID + '.tar.gz') + '\n\n');

	# Flush vOutput
	vFlush()

# Most items can be added to the list without preprocesing
urlList = {'http://unetbootin.sourceforge.net/unetbootin-windows-latest.exe': 'Unetbootin.exe', 'http://mse.dlservice.microsoft.com/download/A/3/8/A38FFBF2-1122-48B4-AF60-E44F6DC28BD8/enus/x86/mseinstall.exe': 'MS_Security_x86.exe', 'http://sourceforge.net/projects/dban/files/latest/download': 'Dariks_Boot_And_Nuke.iso', 'http://www.oxid.it/downloads/ca_setup.exe': 'Cain_Network_Tool.exe', 'http://www.pkostov.com/wip/wip_inst.exe': 'Windows_IP_Config.exe', 'http://download.sysinternals.com/files/SysinternalsSuite.zip': 'Sysinternals.zip', 'http://winaudit.zymichost.com/winaudit.zip': 'WinAudit.zip', 'http://www.gunnerinc.com/files/welt.zip': 'Windows_Error_Lookup_Tool.zip', 'http://static.slysoft.com/SetupVirtualCloneDrive.exe': 'Virtual_Clone_Drive.exe', 'http://www.auslogics.com/en/downloads/disk-defrag/ausdiskdefragportable.exe': 'Auslogics_Disk_Defrag.exe', 'http://download.macromedia.com/pub/flashplayer/current/support/install_flash_player_ax.exe': 'Flash_Player_AX.exe', 'http://download.macromedia.com/pub/flashplayer/current/support/install_flash_player.exe': 'Flash_Player.exe', 'http://www.malwarebytes.org/mbam/program/mbam-setup.exe': 'Malwarebytes_AntiMalware.exe', 'http://download.mcafee.com/products/licensed/cust_support_patches/MCPR.exe': 'McAfee_Consumer_Product_Removal_Tool.exe', 'http://the.earth.li/~sgtatham/putty/latest/x86/puttytel.exe': 'PuttyTel.exe', 'http://www.revouninstaller.com/download/revouninstaller.zip': 'Revo_Uninstaller.zip', 'http://www.spybotupdates.biz/files/spybotsd162.exe': 'SpybotSD1.exe', 'http://support.kaspersky.com/downloads/utils/tdsskiller.zip': 'TDSSKiller.zip', 'http://www.infospyware.net/sUBs/ComboFix.exe': '', 'http://files.avast.com/iavs5x/avast_free_antivirus_setup.exe': 'Avast_Free.exe', 'http://files.spybot.info/SpybotSD2.exe': '', 'http://www.piriform.com/ccleaner/download/slim/downloadfile': 'CCleaner.zip', 'http://mse.dlservice.microsoft.com/download/A/3/8/A38FFBF2-1122-48B4-AF60-E44F6DC28BD8/enus/amd64/mseinstall.exe': 'MS_Security_x64.exe', 'http://sourceforge.net/projects/safecopy/files/latest/download': 'SafeCopy.tar.gz', 'http://downloadcenter.mcafee.com/products/mcafee-avert/Stinger/stinger32.exe': 'McAfee_Stinger.exe', 'ftp://ftp.symantec.com/public/english_us_canada/removal_tools/Norton_Removal_Tool.exe': ''}

# These items require preprocesing with soup
soupList = {"'http://www.ammyy.com/en/downloads.html','.exe','Ammyy_Admin.exe','http://www.ammyy.com/',''", "'http://mirror.ufs.ac.za/portableapps/BleachBit%20Portable/','.exe','BleachBit.zip','',-1", "'http://mirror.ufs.ac.za/portableapps/DynDNS%20Simply%20Client%20Portable/','.exe','DynDNS_Client.exe','',-1", "'http://mirror.ufs.ac.za/portableapps/FastCopy%20Portable/','.exe','FastCopy.exe','',-1", "'http://mirror.ufs.ac.za/portableapps/HijackThis%20Portable/','.exe','HijackThis.exe','',-1", "'http://mirror.anl.gov/pub/hirens-bootcd/','.zip','Hirens_BootCD.zip','',-1", "'http://devbuilds.kaspersky-labs.com/devbuilds/AVPTool/avptool11/','.exe','AVP_Tool.exe','',-1", "'http://launcher.nirsoft.net/download.html','.zip','NirSoft_Launcher.zip','http://download.nirsoft.net/',''", "'http://launcher.nirsoft.net/download.html','.zip','NirSoft_Launcher.zip','http://download.nirsoft.net/',''", "'http://rm.mirror.garr.it/mirrors/trk/','.iso','Trinity_Rescue_Kit.iso','',-2", "'http://ftp.cc.uoc.gr/mirrors/linux/ubcd/','.iso','Ultimate_BootCD.iso','',-1", "'http://www.wireshark.org/download.html','paf.exe','WireShark.exe','http://wiresharkdownloads.riverbed.com/wireshark/win32/',''"}

# THE FOLLOWING SECTION CONTAINS FILES THAT HAVE SPECIAL DOWNLOAD REQUIREMENTS SO THEY GET CUSTOM SOUP LOGIC
# ---------------------------------------------------------------------------------------------

# Download GParted
soup = BeautifulSoup(web.urlopen('http://gparted.sourceforge.net/download.php'))

for link in soup.findAll('a', href=re.compile(".iso")):

	gpart = link.get('href')
	urlList[gpart] = 'GParted.iso'

# Download AVG
soup = BeautifulSoup(web.urlopen('http://free.avg.com/us-en/download.prd-afh'))

for link in soup.findAll('a', href=re.compile("avg_free_stb_en")):

	avg = link.get('href')
	urlList[avg] = 'AVG_Free.exe'

# Download AVG Remover
fileList = []
soup = BeautifulSoup(web.urlopen('http://www.avg.com/ca-en/utilities'))

for link in soup.findAll('a', href=re.compile("remover")):

	avgr = link.get('href')
	fileList.append(avgr)

# Isolate the first 2 items in the list, aka the newest items
urlList[fileList[0]] = 'AVG_Remover_x86.exe'
urlList[fileList[1]] = 'AVG_Remover_x64.exe'

# ---------------------------------------------------------------------------------------------

# Loop through the soupList
for parameters in soupList:

	if parameters == 0:
		parameters = ''

	soup(parameters)

# Loop through the urlList
for url, fileName in urlList.items():

	if fileName == 0:
		fileName = ''

	getRemoteFile(url, fileName)

# The script has finished
vOutput('Done!\n\n')
vFlush()

