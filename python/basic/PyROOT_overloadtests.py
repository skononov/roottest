# File: roottest/python/basic/PyROOT_overloadtests.py
# Author: Wim Lavrijsen (LBNL, WLavrijsen@lbl.gov)
# Created: 04/15/05
# Last: 12/04/10

"""Overload unit tests for PyROOT package."""

import sys, os, unittest
sys.path.append( os.path.join( os.getcwd(), os.pardir ) )

from array import array
from ROOT import *
from common import *

__all__ = [
   'Overloads1ClassArrayTestCase',
   'Overloads2TMathTestCase'
]

gROOT.LoadMacro( "Overloads.C+" )


### class/array overloaded functions =========================================
class Overloads1ClassArrayTestCase( MyTestCase ):
   def test1ClassOverloads( self ):
      """Test functions overloaded on different ROOT clases"""

      self.assertEqual( MyC().GetInt( MyA() ), 42 )
      self.assertEqual( MyC().GetInt( MyB() ), 13 )
      self.assertEqual( MyD().GetInt( MyA() ), 42 )
      self.assertEqual( MyD().GetInt( MyB() ), 13 )

      self.assertEqual( MyC().GetInt( MyNSa.MyA() ),  88 )
      self.assertEqual( MyC().GetInt( MyNSb.MyA() ), -33 )

      self.assertEqual( MyD().GetInt( MyNSa.MyA() ),  88 )
      self.assertEqual( MyD().GetInt( MyNSb.MyA() ), -33 )

      c = MyC()
      self.assertRaises( TypeError, c.GetInt.disp, 12 )
      self.assertEqual( c.GetInt.disp( 'MyA* a' )( MyA() ), 42 )
      self.assertEqual( c.GetInt.disp( 'MyB* b' )( MyB() ), 13 )

      self.assertEqual( MyC().GetInt.disp( 'MyA* a' )( MyA() ), 42 )
      self.assertEqual( MyC.GetInt.disp( 'MyB* b' )( c, MyB() ), 13 )

      d = MyD()
      self.assertEqual( d.GetInt.disp( 'MyA* a' )( MyA() ), 42 )
      self.assertEqual( d.GetInt.disp( 'MyB* b' )( MyB() ), 13 )

      nb = MyNSa.MyB()
      self.assertRaises( TypeError, nb.f, MyC() )

   def test2ClassOverloads( self ):
      """Test functions overloaded on void* and non-existing classes"""

      import ROOT
      oldval = ROOT.gErrorIgnoreLevel
      ROOT.gErrorIgnoreLevel = ROOT.kError

    # first verify that BB and DD are indeed unknown
      self.assertRaises( RuntimeError, BB )
      self.assertRaises( RuntimeError, DD )

    # then try overloads based on them
      self.assertEqual( MyOverloads().call( AA() ),    "AA" )
      self.assertEqual( MyOverloads().call( GetBB() ), "DD" ) # <- BB is unknown + void*
      self.assertEqual( MyOverloads().call( CC() ),    "CC" )
      self.assertEqual( MyOverloads().call( GetDD() ), "DD" ) # <- DD is unknown

      ROOT.gErrorIgnoreLevel = oldval

   def test3ClassOverloadsAmongUnknowns( self ):
      """Test that unknown* is preferred over unknown&"""

      import ROOT
      oldval = ROOT.gErrorIgnoreLevel
      ROOT.gErrorIgnoreLevel = ROOT.kError
      self.assertEqual( MyOverloads2().call( GetBB() ), "BBptr" )
      self.assertEqual( MyOverloads2().call( GetDD(), 1 ), "DDptr" )
      ROOT.gErrorIgnoreLevel = oldval

   def test4ArrayOverloads( self ):
      """Test functions overloaded on different arrays"""

      ai = array( 'i', [ 525252 ] )
      self.assertEqual( MyC().GetInt( ai ), 525252 )
      self.assertEqual( MyD().GetInt( ai ), 525252 )

      ah = array( 'h', [ 25 ] )
      self.assertEqual( MyC().GetInt( ah ), 25 )
      self.assertEqual( MyD().GetInt( ah ), 25 )


### basic functioning test cases =============================================
class Overloads2TMathTestCase( MyTestCase ):
   def test1MeanOverloads( self ):
      """Test overloads using TMath::Mean(), TMath::Median"""

      numbers = [ 8, 2, 4, 2, 4, 2, 4, 4, 1, 5, 6, 3, 7 ]
      mean, median = 4.0, 4.0

      af = array( 'f', numbers )
      self.assertEqual( round( TMath.Mean( len(af), af ) - mean, 5 ), 0 )
      self.assertEqual( round( TMath.Median( len(af), af ) - median, 5 ), 0 )

      ad = array( 'd', numbers )
      self.assertEqual( round( TMath.Mean( len(ad), ad ) - mean, 8), 0 )
      self.assertEqual( round( TMath.Median( len(ad), ad ) - median, 8), 0 )

      ai = array( 'i', numbers )
      self.assertEqual( round( TMath.Mean( len(ai), ai ) - mean, 8), 0 )
      self.assertEqual( round( TMath.Median( len(ai), ai ) - median, 8), 0 )

      ah = array( 'h', numbers )
      self.assertEqual( round( TMath.Mean( len(ah), ah ) - mean, 8), 0 )
      self.assertEqual( round( TMath.Median( len(ah), ah ) - median, 8), 0 )

      al = array( 'l', numbers )
      self.assertEqual( round( TMath.Mean( len(al), al ) - mean, 8), 0 )
      self.assertEqual( round( TMath.Median( len(al), al ) - median, 8), 0 )

      aL = array( 'L', numbers )
      self.assertEqual( round( TMath.Mean( len(aL), aL ) - mean, 8), 0 )
      self.assertEqual( round( TMath.Median( len(aL), aL ) - median, 8), 0 )

   def test2DoubleIntOverloads( self ):
      """Test overloads on int/doubles"""

      self.assertEqual( MyOverloads().call( 1 ), "int" )
      self.assertEqual( MyOverloads().call( 1. ), "double" )
      self.assertEqual( MyOverloads().call1( 1 ), "int" )
      self.assertEqual( MyOverloads().call1( 1. ), "double" )


## actual test run
if __name__ == '__main__':
   from MyTextTestRunner import MyTextTestRunner

   loader = unittest.TestLoader()
   testSuite = loader.loadTestsFromModule( sys.modules[ __name__ ] )

   runner = MyTextTestRunner( verbosity = 2 )
   result = not runner.run( testSuite ).wasSuccessful()

   sys.exit( result )
