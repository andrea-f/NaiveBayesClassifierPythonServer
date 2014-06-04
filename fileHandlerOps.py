# coding: utf-8
import os
import logging
import json
import os.path
import locale
import csv

class fileHandler:
    """File operations read json, xml, save json"""
    
    def __init__(self, root = "",folder = "", fileName = None, result = None, folders = None, allInfo = None, homeLocation = None):
        """Initialization of FileHandler class.

        :param fileName:
            Name with path of file to save, string.

        :param result:
            What to save, string or list.

        :param folders:
            Which directory to use when saving data, string.

        :param allInfo:
            Contains dicts with information to save, list.

        :param homeLocation:
            Holds keys with information on where to save to downloaded/parsed/videos folders, dict.

        """
        self.folder = folder
        self.fileName = fileName
        self.data = result
        self.folders = folders
        self.allInfo = allInfo
        self.homeLocation = homeLocation
        self.root = root

           
    def readJson(self, fileName = None):
        """Load JSON file, reads keywords for categorization, json file is opened.

        :param fileName:
            Which filename to read, string.

        Return JSON formatted dict of read data.
        """
        print fileName
        if fileName is None:
            fileName = self.fileName
        pathFrom=open(fileName)
        dateFromPath = pathFrom.read()
        readData = json.loads(dateFromPath)
        logging.info("Reading JSON file: %s" % fileName)
        pathFrom.close()
        return readData

    def readCSV(self, fileName = None):
        """Reads CSV file and returns its content."""
        if fileName is None:
            fileName = self.fileName
        totalEntries = []
        with open(fileName, 'rb') as csvfile:
            reader = csv.reader(csvfile, delimiter=' ', quotechar='|')#.replace('\r\n','\n')
            for entry in reader:
                try:
                    e = entry.replace('\r\n','\n')
                except:
                    e = entry  
                totalEntries.append(' '.join(e))
        return totalEntries
        
    def saveJSON(self, fileName = None, data = None, keyToSave = 'sents',folder = "", root = ""):
        """Saves json information in fileName and with specific data.

        :param fileName:
            File name with full directory path to save JSON to, string.

        :param data:
            What data to save, string.

        :param keyToSave:
            Which key to update in the json if any, string.

        """
        if len(root) == 0:
            root = self.root
        if len(folder) == 0:
            folder = self.folder
        if fileName is None:
            fileName = self.fileName
        if data is None:
            data = self.result
        if fileName.endswith('.json'):
            fn = fileName            
        else:
            fn = "%s.json" % fileName
        if os.path.isfile(folder +fn):
            try:
                content = self.readJson(fileName = folder +fn)
                content[keyToSave] = content[keyToSave] + data[keyToSave]
                textToSave = json.dumps(content,  indent=4, sort_keys=True)
            except:
                textToSave = json.dumps(data, indent=4, sort_keys=True)
        else:
            textToSave = json.dumps(data, indent=4, sort_keys=True)
        try:
            json.loads(textToSave)
        except Exception as e:
            print "[saveJSON] Error in saving Json: %s" % e
        try:
            saved = self.saveFile(data = textToSave, fileName = fn, folder = folder)
        except:
            f = open(fn, 'w')
            f.write(textToSave)
            #logging.info("{FileHandler} [saveJSON] Saving JSON to: %s\n" % fn)
            #logging.info("{FileHandler} [saveJSON] With data: %s...\n" % str(self.data)[:100])
            f.close()
            saved = fn
        print "{FileHandler} [saveJSON] Saving JSON to: %s\n" % fn
        logging.info("{FileHandler} [saveJSON] Saving JSON to: %s\n" % fn)
        logging.info("{FileHandler} [saveJSON] With data: %s...\n" % str(self.data)[:100])
        return saved
        
    def saveHTML(self, fileName = None, data = None):
        """Open for for write.

        :param fileName:
            File name with full directory path to save HTML to, string.

        :param data:
            What data to save, string.

        """
        if fileName is None:
            fileName = self.fileName
        if data is None:
            data = self.data
        fileObj = open(fileName,"a")
        try:
            fileObj.write(data)
        except Exception, e:
            logging.info("{FileHandler} [saveHTML] Couldnt save HTML file in %s because \n %s" % (self.fileName,e))
        fileObj.close()
        
    def saveFiles(self, allInfo = None, fileName = None, data = None):
        """Save files in folder path, expects a list.

        :param allInfo:
            Contains dicts with information to save, list.

        :param fileName:
            File name with full directory path to save HTML to, string.

        :param data:
            What data to save, string.

        Return string with top level location of filelist.txt.
        
        """
        if allInfo is None:
            allInfo = self.allInfo
        if fileName is None:
            fileName = self.fileName
        if data is None:
            data = self.data
        fileList = []
        for item in allInfo:
            fileName = item['filePath']
            folder = item['folder']
            logging.info("{FileHandler} [saveFiles] folder: %s\n" % folder)
            #third level
            if "movies" in item['cat']:
                try:
                    levelOneDir = "%s/%s" % (item['folder'],item['first_level'])
                    os.makedirs(levelOneDir)
                    fileName = "%s/%s" % (fileName, item['second_level'])
                except OSError:
                    fileName = "%s/%s" % (fileName, item['second_level'])            
                data = item['third_level']
                fn = "%s.txt" % (fileName.replace('&ndash;', '-'))
                logging.info("{FileHandler} [saveFiles] Saving file: %s\n With contents: %s \n in folder %s" % (fn, str(data)[:100],folder))
                fileList.append(fn)
                try:
                    f = open(fn, 'w')
                    fnInText = "%s.\n" % item['second_level']
                    f.write(fnInText)
                    for dataItem in data:
                        dataItem = "%s.\n" % dataItem
                        f.write(dataItem)
                    f.close()
                except Exception as e:
                    logging.info("{FileHandler} [saveFiles] Third level save file error: %s" % e)
                    pass
            try: 
                #second level
                locale.getdefaultlocale() 
                v = item['first_level'].replace('–',' ')
                sl = "%s/%s.txt" % (folder, v)
                x = open(sl, 'a')
                secondLevel = "%s.\n" % item['second_level']
                x.write(secondLevel)
                x.close()
            except Exception as e:
                logging.info("{FileHandler} [saveFiles] Error in creating second level: %s" %e)
            fileListSecondLevel = "%s/filelist_second.txt" % (folder)
            b = open(fileListSecondLevel, 'a')
            fileContents = open(fileListSecondLevel).read()
            try:
                if sl not in fileContents:
                    s2 = "%s\n" % (sl)
                    b.write(s2)
                b.close()
            except Exception as e:
                logging.info("{FileHandler} [saveFiles] File not found and error %s" % e)
                pass
        fileListDir = "%s/%s/filelist.txt" % (folder)
        self.saveFileList(folder, fileList)
        return fileListDir

    def saveFile(self, data = None, fileName = None, folder = None):
        """Saves a file to disk in a specified folder.

        :param fileName:
            Name of file to save, string.

        :param folder:
            Where to save the file on disk, string.

        Return true if file saved, false if not.
        """
        if fileName is None:
            fileName = self.fileName
        if folder is None:
            folder = self.folder
        if data is None:
            data = self.data
        if not os.path.isdir(folder):
            os.makedirs(folder)
        fullName = folder+"/"+fileName
        exists = self.checkIfFileExists(fullName)
        if exists:
            mode = "a"
        else:
            mode = "w"
        fileObj = open(fullName,mode)
        try:
            fileObj.write(str(data))
        except Exception, e:
            try:
                fileObj.write(data)
            except Exception, e:
                print "{FileHandler} [saveFile] Couldnt save file in %s because \n %s" % (fullName,e)
                return False
        fileObj.close()
        return True


    def saveFileList(self, folder, fileList):
        """Save filelist for NER parser.

        :param folder:
            Which directory to use when saving data, string.

        :param fileList:
            Contains strings with location and name of files to NER parse, list.

        Return string with location of downloaded data filelist.
        
        """
        fileListDir = "%s/%s/filelist.txt" % (folder)
        logging.info("{FileHandler} [saveFileList] Saving filelist in: %s" % fileListDir)
        try:
            g = open(fileListDir, 'a')
        except Exception as e:
            fileListDir = "%s/filelist.txt" % (self.homeLocation['downloadedData'])
            g = open(fileListDir, 'a')
        for oneFile in fileList:
            oneFile = "%s/%s\n" % (oneFile)
            g.write(oneFile)
        g.close()
        return fileListDir
          
    def saveFolders(self, root = None, homeLocation = None):
        """Create folders if they don't already exist.

        :param root:
            Sets name of main directory to be created to identify contained data, string.

        :param homeLocation:
            Holds key references to default directory information with downloadedData, videoData, parsedData, dict.

        """
        if root is None:
            root = self.folders
        if homeLocation is None:
            homeLocation = self.homeLocation
        downloadedFileLocation = homeLocation['downloadedData'].replace('file://','')
        rootdir = "%s/%s" % (downloadedFileLocation,root)
        logging.info("{FileHandler} [saveFolders] rootdir in saveFolders %s" % rootdir)
        try:
            videoFileLocation = "%s/%s/videodata" % (homeLocation['videoData'].replace('file://',''),root)
            dirnameparsed = "%s/%s" % (homeLocation['parsedData'].replace('file://',''),root)
        except Exception as e:
            logging.info("{FileHandler} [saveFolders] Error %s" % e)
            pass        
        if os.path.exists(rootdir):
            logging.info("{FileHandler} [saveFolders] Root directory already exists and is %s" % rootdir)
            pass
        else:
            try:
                os.makedirs(rootdir)
            except OSError:
                pass
        if os.path.exists(videoFileLocation):
            logging.info("{FileHandler} [saveFolders] Subdirectory already exists and is %s" % videoFileLocation)
        else:
            try:
                os.makedirs(videoFileLocation)
            except OSError, msg:
                logging.info("{FileHandler} [saveFolders] Subdirectory creation error on %s, %s" % (videoFileLocation,msg))
                print msg        
        if os.path.exists(dirnameparsed):
            logging.info("{FileHandler} [saveFolders] dirnameparsed already exists and is %s" % dirnameparsed)
            pass
        else:
            try:
                os.makedirs(dirnameparsed)
            except OSError:
                logging.info("{FileHandler} [saveFolders] dirnameparsed already exists and is %s" % dirnameparsed)
        file_list_name = "%s/filelist.txt" % rootdir
        logging.info("{FileHandler} [saveFolders] Filelist name: %s" % file_list_name)
        g = open(file_list_name, 'w')
        g.close
        
    def createDir(self, folder = ""):
        """Creates a dir if it doesn't exist."""
        if len(folder) == 0:
            folder = self.folder
        if os.path.exists(folder):            
            return False
        else:
            try:
                os.makedirs(folder)
                return True
            except OSError:
                pass
    
    def readFileByLine(self, fileName = None):
        """Reads a file line by line.

        :param fileName:
            File name with full directory path to read, string.

        Return list with each line read from file if success.

        Return boolean with False if failed to read file line by line.
        
        """
        if fileName is None:
            fileName = self.fileName
        try:
            m = open(fileName, 'r')
            lines = []
            for line in m:
                line = line.replace('.\n','').replace('\n','')
                #line = line.encode('utf-8','ignore')
                lines.append(line)
            m.close()
            return lines
        except Exception as e:
            print "[readFileByLine] file exception: %s" % e
            return False

    def readXML(self, fileName = None):
        """Extract POS NER and WORD from XML file.

        :param fileName:
            XML formatted file name with full directory path to read, string.

        Return dictionary with:
            * **ner_events_in_folder** -- Contains dict with all ner information for given XML file, list.
            * **all_sentences** -- Contains dict with sentence id and all tokens in that sentence, list.

        """
        if fileName is None:
            fileName = self.fileName
        try:
            from nltk.etree.ElementTree import ElementTree
        except Exception as e:
            try:
                from nltk.ElementTree import ElementTree
            except:
                import xml.etree.ElementTree as ET
        try:
            try: 
                fileparsing = ElementTree().parse(fileName)
            except:
                fileparsing = ET.ElementTree().parse(fileName)
    	except Exception as e:
    	   print "{FileHandler} [readXML] fileHandler error.... %s" % e
    	if fileparsing:
            try:
                doc = fileparsing[0]
                sentences = doc[0]
            except:
                doc = fileparsing.getroot()
                sentences = doc.getroot()
            sentences = sentences.getchildren()
            logging.info("{FileHandler} [readXML] Parsing XML: %s" % fileName)
            #parse filename for extra information
		    #Get the root node
            fileInfo = []
            event = {}
            allSentences = []
            for sentence in sentences:
                tokensInASentence = []
                sentenceId = sentence.attrib.get('id')
                for tokens in sentence.findall('tokens'):
                    for a in range(len(tokens)):						
                        pos = tokens[a][4].text
                        ner = tokens[a][5].text
                        tokenNumber = tokens[a].attrib.get('id')
                        word = tokens[a][0].text
            		#create dictionary containing all events in a parsed XML file like 1991 92 serie A
                        try:
                            normalizedNer = tokens[a][6].text
                            event = {'pos':pos,'ner':ner, 'word':word, 'sentence_id': sentenceId, 'normalizedNer':normalizedNer, 'token_number':tokenNumber}
                        except Exception as e:
                            event = {'pos':pos,'ner':ner, 'word':word, 'sentence_id': sentence_id, 'token_number':tokenNumber}
                        fileInfo.append(event)
                        tokensInASentence.append(event)
                allTokensInSameSentence = {'sentence_id':sentenceId, 'all_tokens':tokensInASentence}
                allSentences.append(allTokensInSameSentence)
            allTokensAndAllSentences = {'ner_events_in_folder':fileInfo, 'all_sentences':allSentences}
            return allTokensAndAllSentences
        else:
            print "{FileHandler} [readXML] fileparsing error."
            logging.info("{FileHandler} [readXML] Parsing XML error.\n" % fileName)

    def listFilesInDir(self, folder = None):
        """List all files in a directory.

        :param folder:
            Which directory to use when listing all files within that dir, string.

        Return list with all strings identifying file names within folder.

        """
        if folder is None:
            folder = self.folders
        os.chdir(folder)
        allFilesInDir = []
        for fileName in os.listdir("."):
            if fileName.endswith(".xml") or fileName.endswith(".csv") or fileName.endswith(".json") or fileName.endswith(".txt") or fileName.endswith(".jpg") or fileName.endswith(".png"):
                if folder.endswith('/'):
                    fileName = "%s%s" % (folder, fileName.decode('utf-8'))                    
                else:
                    fileName = "%s/%s" % (folder, fileName.decode('utf-8'))                    
                allFilesInDir.append(fileName)
        return allFilesInDir
    
    def listDirs(self, folder = None):
        """List all directories in directory.

        :param folder:
            Which directory to use when listing all files within that dir, string.

        Return list with all directory names contained in subpaths of folder.
        
        """
        if folder is None:
            folder = self.folders
        os.chdir(folder)
        allFilesInDir = []
        for files in os.listdir("."):
            if os.path.isdir(files) == True:
                if self.folders.endswith('/'):
                    files = "%s%s" % (folder, files.decode('utf-8'))           
                else:
                    files = "%s/%s" % (folder, files.decode('utf-8'))           
                allFilesInDir.append(files)
        return allFilesInDir

    def checkIfFileExists(self, fileName = None):
        """Checks if a specific file exists in the system or not, returns true if exists otherwise false.

        :param fileName:
            Name with path of file to check its existance, string.

        Return boolean:
            * **True** -- If file exists.
            * **False** -- If file doesn't exist.
            
        """
        if fileName is None:
            fileName = self.fileName
        try:
            with open(fileName) as f: pass
        except IOError as e:
            return False
        return True
        
    def main():
        """Main class for internal testing of file operations read Json/XML, save Json"""
        from UnitTest.test_fileHandler import *
        fileHandlerTests.test_readJson()  
    
    if __name__ == "__main__":
        main()
