import maya.cmds as cmds 

class MFile(object):
	SAFECOUNT = 100
	
	@classmethod
	def listReferences(cls):
		return cmds.ls(references = True)

	@classmethod
	def importAllReferences(cls):
		references = MFile.listReferences()
		for ref in references:
			try:
				MFile.importReference(ref)
			except RuntimeError as e:
				print(e)
				
		if len(MFile.listReferences()) != 0:
			MFile.importAllReferences()

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
			MFile.cleanAllNamespaces()

		
		