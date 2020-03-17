import unittest
import os
import shutil
import maya.cmds as cmds 
import maya.mel as mel
import mayaio.mFile 
reload (mayaio.mFile)
from mayaio.mFile  import MFile 


class TestMFile(unittest.TestCase):
	path = r"D:\exporterTests\assets"
	rootPath = r"D:\exporterTests"
	referenceCube ="{}\\referenceCube.ma".format(path)
	referenceFile = "{}\\referenceFile.ma".format(path)
	testFile = "{}\\testFile.ma".format(path)
	
	@classmethod
	def setUpClass(cls):

		if not os.path.exists(TestMFile.path):
			os.makedirs(TestMFile.path)

	#@classmethod
	#def tearDownClass(cls):
	 #	shutil.rmtree(TestMFile.rootPath)

	def setUp(self):
		cmds.file(newFile = True, f = True)
		cmds.file(rename = TestMFile.referenceCube)
		cmds.polyCube(name = "myCube")
		cmds.file(save = True)

		cmds.file(newFile = True)
		cmds.file(rename = TestMFile.referenceFile)
		cmds.file(TestMFile.referenceCube, reference = True, namespace = "c1")
		cmds.file(TestMFile.referenceCube, reference = True, namespace = "c2")
		cmds.file(TestMFile.referenceCube, reference = True, namespace = "c3")
		cmds.file(save = True)
		cmds.file(newFile = True)
		

	def tearDown(self):
		cmds.file(newFile = True, f = True)

	def test_listReferences(self):
		cmds.file(TestMFile.referenceFile, reference = True, namespace = "listReferences")
		result = MFile.listReferences()

		self.assertTrue(len(result)> 0)

	def test_importAllReferences(self):
		cmds.file(TestMFile.referenceFile, reference = True, namespace = "listReferences")
		MFile.importAllReferences()
		result = MFile.listReferences()
		self.assertTrue(len(result) == 0)

	def test_getNamespaces(self):
		cmds.file(TestMFile.referenceCube, reference = True, namespace = "cubeNamespace")
		result = MFile.getNamespaces()[0]
		self.assertEqual(result, "cubeNamespace")

	def test_cleanAllNamespaces(self):
		cmds.file(TestMFile.referenceFile, reference = True, namespace = "referenceFile")
		MFile.importAllReferences()
		MFile.cleanAllNamespaces()

		result = MFile.getNamespaces()
		self.assertEqual(len(result), 0)

	def test_new(self):
		MFile.new("newFile")
		result = cmds.file(q = True, expandName = True).split("/")[-1]
		self.assertEqual(result, "newFile.ma")

	def test_getDir(self):
		MFile.new("newFile")
		result =  "/".join(cmds.file(q = True, expandName = True).split("/")[0:-1])
		self.assertEqual(result, MFile.getDir())

	def test_save(self):
		MFile.new("newFile")
		MFile.saveAs("anotherFile", path = TestMFile.path)
		path = os.path.join(TestMFile.path, "anotherFile.ma")
		result = os.path.isfile(path)
		self.assertTrue(result)

def runTests():
	print("\nTEST MFILE")

	testCases = [TestMFile]

	for case in testCases:
		suite = unittest.TestLoader().loadTestsFromTestCase(case)
		unittest.TextTestRunner(verbosity = 2).run(suite)
if __name__ == "__main__":
	runTests()
