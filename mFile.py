import maya.cmds as cmds 
import maya.mel as mel
import os

class MFile(object):
	""" Class to interface maya files. """
	#TODO remove cmds and use OpenMaya
	SAFECOUNT = 30

	@classmethod
	def getMayaRootPath(self):
		paths = mel.eval("getenv MAYA_APP_DIR;").split("/")
		return os.path.join(paths[0], os.sep, *paths[1:])

	@classmethod 
	def open(cls, path):
		cmds.file(path, f = True, open = True)


	@classmethod
	def new(cls, name = "defaultUntitled", ma = True):
		cmds.file( force = True, new = True)
		
		fileType = "mb" 
		if ma:
			fileType = "ma" 

		cmds.file(rename = "{}.{}".format(name, fileType))

	@classmethod 
	def save(cls):
		return cmds.file(save=True)

	@classmethod 
	def sceneName(cls):
		return cmds.file(query = True, sceneName = True).replace(".ma", "")

	@classmethod 
	def saveAs(cls, name, path = None, ma = True):
		fileType = "mb" 
		if ma:
			fileType = "ma" 
		
		name = "{}.{}".format(name, fileType)
		filePath = name
		if path:
			filePath = "{}/{}".format(path, name)

		cmds.file(rename="{}".format(filePath))
		return MFile.save()

	@classmethod 
	def getDir(cls):
		path = MFile.getPath()
		path = path.split("/")
		path = "/".join(path[0:-1])
		return path

	@classmethod
	def getPath(cls):
		return cmds.file(q = True, expandName = True);

	@classmethod
	def listReferences(cls):
		return cmds.ls(references = True)

	@classmethod
	def unloadAllReferences(cls):
		references = MFile.listReferences()
		try:
			[cmds.file(unloadReference = r) for r in references]
		except Exception as e:
			print e


	@classmethod
	def importAllReferences(cls):
		count = 0;
		while len(MFile.listReferences()) > 0:
			references = MFile.listReferences()

			for ref in references:
				try:
					MFile.importReference(ref)
				except RuntimeError as e:
					print(e)

			if len(references) == len(MFile.listReferences()):
				cmds.warning("It seems like theses references can't be imported: {}\n".format(references))
				return

			if count > MFile.SAFECOUNT:
				cmds.warning("Looped for {} times. Returning.".format(MFile.SAFECOUNT))
				return

			count += 1

		

	@classmethod
	def importReference(cls, reference):
		ref_name =  cmds.referenceQuery(reference, f = True, shn = True, wcn = True)
		cmds.file(ref_name, ir = True)

	@classmethod
	def getNamespaces(cls):
		namespaces = cmds.namespaceInfo(":", lon =  True)
		namespaces.remove("UI")
		namespaces.remove("shared") 
		return namespaces
	
	@classmethod
	def cleanNamespace(cls, namespace):
		cmds.namespace(f = True, mv=(':{}'.format(namespace), ':') )
		cmds.namespace(rm =namespace)

	@classmethod
	def cleanAllNamespaces(cls):
		exceptionNamespaces = []
		safecount = 0

		for ns in MFile.getNamespaces():
			try:
				MFile.cleanNamespace(ns)
			except RuntimeError as e:
				print(e)
				exceptionNamespaces.append(ns)

		if len(MFile.getNamespaces()) > len(MFile.listReferences()):

			if safecount == MFile.SAFECOUNT:
				return
			MFile.cleanAllNamespaces()

		
		