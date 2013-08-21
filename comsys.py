# ComSys Tools V0.01a
# Python 2.7, 3.3
# ---------------------------------------------------------------------------------------------

# Import the necessary resources
from bs4 import BeautifulSoup
import tarfile, shutil, glob, os, re, sys, time

<<<<<<< HEAD
# Try for Python 3.3
try:
	import urllib.request
	fetch = urllib.request
# Fall back to Python 2.7
except ImportError:
	import urllib
	fetch = urllib

=======
>>>>>>> 57385db4d589704ee1ab233a1100e31627ca16d6
# Work/Target directories & download mode
args = sys.argv
workDir = r'' + args[1]
targetDir = r'' + args[2]

# Initialize the script
sys.stdout.write('\nInitializing....\n\n')

# ---------------------------------------------------------------------------------------------

# Report the download percentage
def report(count, blockSize, totalSize):
  	percent = int(count*blockSize*100/totalSize)
  	sys.stdout.write("\r%d%%" % percent + ' complete')
  	sys.stdout.flush()
# ---------------------------------------------------------------------------------------------

def getRemoteFile(item, setName=''):

	# Get the URL
	response = fetch.urlopen(item)
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
		sys.stdout.write('\rError 404: Failed to fetch ' + name + '\n\n')
		sys.stdout.flush()
		return

	# Get the "last-modified" information of the file from the file header
	time_data = str(response.info().get('last-modified'))

 	# Output a status message
	sys.stdout.write('\rFetching ' + fetchName + '...\n')

	# Strip the extension from the filename
	fileID = os.path.splitext(workDir + name)[0]

	# Check to see if we already have the file in the target directory
	if os.path.isfile(targetDir + fileID + 'tar.gz') != 1:
		targetPath = 0
	else:
		targetPath = 1

	if os.path.isfile(workDir + name) == 1:
		# Get the "last-modified" information of the file from the remote file
		local = os.stat(workDir + name).st_mtime
		# Make sure the response value is set before we attempt to download the file
		if time_data != 'None':
			# Convert the "time_data" output to an interger thats compatible with the local file
			server = time.mktime(time.strptime(time_data, "%a, %d %b %Y %H:%M:%S GMT"))
		else:
			server = int(local + 1)
		# Compare the "last-modified" dates of the local file and the remote file
		if local < server:
			# Fetch the file
			fetch.urlretrieve(response.geturl(), workDir + name, reporthook=report)
		else:
			# Turn off transfer mode if the compressed file exits in the targetDir path. If not we will transfer.
			if targetPath != 0: 
				# Turn off transfer because we dont need it.
				transfer = 0
		# Output a status message
		sys.stdout.write('\r' + name + ' is up-to-date.\n\n')
	else:
		# First-time download of file
		fetch.urlretrieve(response.geturl(), workDir + name, reporthook=report)
		sys.stdout.write("\rDownload complete, saved as %s" % (name) + '\n\n')
	# Transfer & compress the files
	if transfer != 0:
		# Copy the files in the temp directory to the target directory
		allFiles = glob.glob(workDir + '*.*')
		filePath = workDir + name
		thisName = name
		sys.stdout.write('\rTransferring ' + thisName + '...\n');
		shutil.copy(filePath,targetDir);
		sys.stdout.write("\rTransfer complete, saved as %s" % (thisName) + '\n\n');
		# ---------------------------------------------------------------------------------------------

		# Compress the files in the target directory
		exeFiles = glob.glob(targetDir + '*.exe')
		isoFiles = glob.glob(targetDir + '*.iso')
		zipFiles = glob.glob(targetDir + '*.zip')
		rarFiles = glob.glob(targetDir + '*.rar')
		allFiles = exeFiles + isoFiles + zipFiles + rarFiles
		for filePath in allFiles:
			fileName = os.path.splitext(filePath)[0]
			thisFile = filePath.split('/')[-1]
			tarHandler = tarfile.open(fileName + '.tar.gz', "w:gz")
			sys.stdout.write('\rCompressing ' + thisFile + '...\n');
			tarHandler.add(filePath);
			os.remove(filePath); sys.stdout.write("\rCompression complete, saved as %s" % ((fileName) + '.tar.gz') + '\n\n');
	# ---------------------------------------------------------------------------------------------

	sys.stdout.flush()
# ---------------------------------------------------------------------------------------------

# Make the workDir if it doesn't exist
if not os.path.exists(workDir):
    os.makedirs(workDir)
# ---------------------------------------------------------------------------------------------

# Make the targetDir if it doesn't exist
if not os.path.exists(targetDir):
    os.makedirs(targetDir)
# ---------------------------------------------------------------------------------------------

# We don't use soup when we don't need to. A most items can be added to the list without preprocesing.
urlList = {'http://unetbootin.sourceforge.net/unetbootin-windows-latest.exe': 'Unetbootin.exe', 'http://mse.dlservice.microsoft.com/download/A/3/8/A38FFBF2-1122-48B4-AF60-E44F6DC28BD8/enus/x86/mseinstall.exe': 'MS_Security_x86.exe', 'http://sourceforge.net/projects/dban/files/latest/download': 'Dariks_Boot_And_Nuke.iso', 'http://www.oxid.it/downloads/ca_setup.exe': 'Cain_Network_Tool.exe', 'http://www.pkostov.com/wip/wip_inst.exe': 'Windows_IP_Config.exe', 'http://download.sysinternals.com/files/SysinternalsSuite.zip': 'Sysinternals.zip', 'http://winaudit.zymichost.com/winaudit.zip': 'WinAudit.zip', 'http://www.gunnerinc.com/files/welt.zip': 'Windows_Error_Lookup_Tool.zip', 'http://static.slysoft.com/SetupVirtualCloneDrive.exe': 'Virtual_Clone_Drive.exe', 'http://www.auslogics.com/en/downloads/disk-defrag/ausdiskdefragportable.exe': 'Auslogics_Disk_Defrag.exe', 'http://download.macromedia.com/pub/flashplayer/current/support/install_flash_player_ax.exe': 'Flash_Player_AX.exe', 'http://download.macromedia.com/pub/flashplayer/current/support/install_flash_player.exe': 'Flash_Player.exe', 'http://www.malwarebytes.org/mbam/program/mbam-setup.exe': 'Malwarebytes_AntiMalware.exe', 'http://download.mcafee.com/products/licensed/cust_support_patches/MCPR.exe': 'McAfee_Consumer_Product_Removal_Tool.exe', 'http://the.earth.li/~sgtatham/putty/latest/x86/puttytel.exe': 'PuttyTel.exe', 'http://www.revouninstaller.com/download/revouninstaller.zip': 'Revo_Uninstaller.zip', 'http://www.spybotupdates.biz/files/spybotsd162.exe': 'SpybotSD1.exe', 'http://support.kaspersky.com/downloads/utils/tdsskiller.zip': 'TDSSKiller.zip', 'http://www.infospyware.net/sUBs/ComboFix.exe': '', 'http://files.avast.com/iavs5x/avast_free_antivirus_setup.exe': 'Avast_Free.exe', 'http://files.spybot.info/SpybotSD2.exe': '', 'http://www.piriform.com/ccleaner/download/slim/downloadfile': 'CCleaner.zip', 'http://mse.dlservice.microsoft.com/download/A/3/8/A38FFBF2-1122-48B4-AF60-E44F6DC28BD8/enus/amd64/mseinstall.exe': 'MS_Security_x64.exe', 'http://sourceforge.net/projects/safecopy/files/latest/download': 'SafeCopy.tar.gz', 'http://downloadcenter.mcafee.com/products/mcafee-avert/Stinger/stinger32.exe': 'McAfee_Stinger.exe', 'ftp://ftp.symantec.com/public/english_us_canada/removal_tools/Norton_Removal_Tool.exe': ''}
# ---------------------------------------------------------------------------------------------

# Download Trinity Rescue Kit
fileList = []
soup = BeautifulSoup(fetch.urlopen('http://rm.mirror.garr.it/mirrors/trk/'))
for link in soup.findAll('a', href=re.compile(".iso")):
	trk = link.get('href')
	# Add all the files to a list
	fileList.append(trk)
# Isolate the 2nd last item in the list, aka the newest item
urlList['http://rm.mirror.garr.it/mirrors/trk/' + fileList[-2]] = 'Trinity_Rescue_Kit.iso'
# ---------------------------------------------------------------------------------------------

# Download NirLauncher
fileList = []
soup = BeautifulSoup(fetch.urlopen('http://launcher.nirsoft.net/download.html'))
for link in soup.findAll('a', href=re.compile(".zip")):
	nir = link.get('href')
	# Add all the files to a list
	fileList.append(nir)
# Isolate the first item in the list, aka the newest item
name = fileList[0].split('/')[-1]
urlList['http://download.nirsoft.net/' + name] = 'NirSoft_Launcher.zip'
# ---------------------------------------------------------------------------------------------

# Download HijackThis
fileList = []
soup = BeautifulSoup(fetch.urlopen('http://mirror.ufs.ac.za/portableapps/HijackThis%20Portable/'))
for link in soup.findAll('a', href=re.compile(".exe")):
	hjt = link.get('href')
	# Add all the files to a list
	fileList.append(hjt)
# Isolate the last item in the list, aka the newest item
urlList['http://mirror.ufs.ac.za/portableapps/HijackThis%20Portable/' + fileList[-1]] = 'HijackThis.exe'
# ---------------------------------------------------------------------------------------------

# Download FastCopy
fileList = []
soup = BeautifulSoup(fetch.urlopen('http://mirror.ufs.ac.za/portableapps/FastCopy%20Portable/'))
for link in soup.findAll('a', href=re.compile(".exe")):
	fcp = link.get('href')
	# Add all the files to a list
	fileList.append(fcp)
# Isolate the last item in the list, aka the newest item
urlList['http://mirror.ufs.ac.za/portableapps/FastCopy%20Portable/' + fileList[-1]] = 'FastCopy.exe'
# ---------------------------------------------------------------------------------------------

# Download DynDNS Client
fileList = []
soup = BeautifulSoup(fetch.urlopen('http://mirror.ufs.ac.za/portableapps/DynDNS%20Simply%20Client%20Portable/'))
for link in soup.findAll('a', href=re.compile(".exe")):
	ddns = link.get('href')
	# Add all the files to a list
	fileList.append(ddns)
# Isolate the last item in the list, aka the newest item
urlList['http://mirror.ufs.ac.za/portableapps/DynDNS%20Simply%20Client%20Portable/' + fileList[-1]] = 'DynDNS_Client.exe'
# ---------------------------------------------------------------------------------------------

# Download GParted
soup = BeautifulSoup(fetch.urlopen('http://gparted.sourceforge.net/download.php'))
for link in soup.findAll('a', href=re.compile(".iso")):
	gpart = link.get('href')
	urlList[gpart] = 'GParted.iso'
# ---------------------------------------------------------------------------------------------

# Download Ammyy Admin
fileList = []
soup = BeautifulSoup(fetch.urlopen('http://www.ammyy.com/en/downloads.html'))
for link in soup.findAll('a', href=re.compile(".exe")):
	ammy = link.get('href')
	# Add all the files to a list
	fileList.append(ammy)
# Isolate the first item in the list, aka the newest item
name = fileList[0].split('/')[-1]
urlList['http://www.ammyy.com/' + name] = 'Ammyy_Admin.exe'
# ---------------------------------------------------------------------------------------------

# Download WireShark
fileList = []
soup = BeautifulSoup(fetch.urlopen('http://www.wireshark.org/download.html'))
for link in soup.findAll('a', href=re.compile("paf.exe")):
	wire = link.get('href')
	# Add all the files to a list
	fileList.append(wire)
# Isolate the first item in the list, aka the newest item
name = fileList[0].split('/')[-1]
urlList['http://wiresharkdownloads.riverbed.com/wireshark/win32/' + name] = 'WireShark.exe'
# ---------------------------------------------------------------------------------------------

# Download BleachBit
fileList = []
soup = BeautifulSoup(fetch.urlopen('http://mirror.ufs.ac.za/portableapps/BleachBit%20Portable/'))
for link in soup.findAll('a', href=re.compile("exe")):
	bbit = link.get('href')
	# Add all the files to a list
	fileList.append(bbit)
# Isolate the last item in the list, aka the newest item
urlList['http://mirror.ufs.ac.za/portableapps/BleachBit%20Portable/' + fileList[-1]] = 'BleachBit.zip'
# ---------------------------------------------------------------------------------------------

# Download AVG
soup = BeautifulSoup(fetch.urlopen('http://free.avg.com/us-en/download.prd-afh'))
for link in soup.findAll('a', href=re.compile("avg_free_stb_en")):
	avg = link.get('href')
	urlList[avg] = 'AVG_Free.exe'
# ---------------------------------------------------------------------------------------------

# Download AVG Remover
fileList = []
soup = BeautifulSoup(fetch.urlopen('http://www.avg.com/ca-en/utilities'))
for link in soup.findAll('a', href=re.compile("remover")):
	avgr = link.get('href')
	# Add all the files to a list
	fileList.append(avgr)
# Isolate the first 2 items in the list, aka the newest items
urlList[fileList[0]] = 'AVG_Remover_x86.exe'
urlList[fileList[1]] = 'AVG_Remover_x64.exe'
# ---------------------------------------------------------------------------------------------

# Download Kaspersky AVPTool
fileList = []
thisURL = 'http://devbuilds.kaspersky-labs.com/devbuilds/AVPTool/avptool11/'
soup = BeautifulSoup(fetch.urlopen(thisURL))
for link in soup.findAll('a', href=re.compile(".exe")):
	avp = link.get('href')
	# Add all the files to a list
	fileList.append(avp)
# Isolate the last item in the list, aka the newest item
name = fileList[-1]
urlList[thisURL + name] = 'AVP_Tool.exe'
# ---------------------------------------------------------------------------------------------

# Download Ultimate BootCD (500MB +)
fileList = []
soup = BeautifulSoup(fetch.urlopen('http://ftp.cc.uoc.gr/mirrors/linux/ubcd/'))
for link in soup.findAll('a', href=re.compile(".iso")):
	ubcd = link.get('href')
	# Add all the files to a list
	fileList.append(ubcd)
# Isolate the last item in the list, aka the newest item
urlList['http://ftp.cc.uoc.gr/mirrors/linux/ubcd/' + fileList[-1]] = 'Ultimate_BootCD.iso'
# ---------------------------------------------------------------------------------------------

# Download Hirens BootCD (620MB +)
fileList = []
soup = BeautifulSoup(fetch.urlopen('http://mirror.anl.gov/pub/hirens-bootcd/'))
for link in soup.findAll('a', href=re.compile(".zip")):
	hiren = link.get('href')
	# Add all the files to a list
	fileList.append(hiren)
# Isolate the last item in the list, aka the newest item
urlList['http://mirror.anl.gov/pub/hirens-bootcd/' + fileList[-1]] = 'Hirens_BootCD.zip'
# ---------------------------------------------------------------------------------------------

# Loop through the urlList
for url, fileName in urlList.items():
	if fileName == 0:
		fileName = ''
	getRemoteFile(url, fileName)
# ---------------------------------------------------------------------------------------------

# The script has finished
sys.stdout.write('\nDone!\n')
sys.stdout.flush()
# ---------------------------------------------------------------------------------------------