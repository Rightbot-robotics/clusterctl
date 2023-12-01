from clusterctl import clusterctl
import unittest

class TestSupervisorclusterctl(unittest.TestCase):
    
    def testWithHelpOption(self):       
        with self.assertRaises(SystemExit) as exception:
            clusterctl.main(["-h"])            
        self.assertEqual(exception.exception.code, 0)
        
    def testWithoutHostPatternArgument(self):       
        with self.assertRaises(SystemExit) as exception:
            clusterctl.main([])            
        self.assertEqual(exception.exception.code, 2)
        
    def testStartWithoutProcessName(self):       
        with self.assertRaises(SystemExit) as exception:
            clusterctl.main(["dev", "start"])            
        self.assertEqual(exception.exception.code, 2)
       
    def testStopWithoutProcessName(self):       
        with self.assertRaises(SystemExit) as exception:
            clusterctl.main(["dev", "stop"])            
        self.assertEqual(exception.exception.code, 2)

    def testRemoveWithoutProcessName(self):       
        with self.assertRaises(SystemExit) as exception:
            clusterctl.main(["dev", "remove"])            
        self.assertEqual(exception.exception.code, 2)

    def testRestartWithoutProcessName(self):
        with self.assertRaises(SystemExit) as exception:
            clusterctl.main(["dev", "restart"])
        self.assertEqual(exception.exception.code, 2)