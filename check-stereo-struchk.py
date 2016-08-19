from rdkit import Chem
from rdkit.Chem.MolKey import MolKey
from rdkit.Chem import rdStructChecker
opts = rdStructChecker.StructCheckerOptions()
print dir(opts)
opts.CheckStereo = False
opts.Verbose = True
checker = rdStructChecker.StructChecker(opts)

molb = '''squiggle bond from chiral center
  Mrv1561 08171605252D          

  5  4  0  0  0  0            999 V2000
   -1.7411    2.3214    0.0000 F   0  0  0  0  0  0  0  0  0  0  0  0
   -0.9161    2.3214    0.0000 C   0  0  3  0  0  0  0  0  0  0  0  0
   -0.0911    2.3214    0.0000 Br  0  0  0  0  0  0  0  0  0  0  0  0
   -0.9161    3.1464    0.0000 C   0  0  0  0  0  0  0  0  0  0  0  0
   -0.9161    1.4964    0.0000 Cl  0  0  0  0  0  0  0  0  0  0  0  0
  1  2  1  0  0  0  0
  2  3  1  0  0  0  0
  2  5  1  0  0  0  0
  2  4  1  4  0  0  0
M  END
'''
molb2 = '''crossed double bond
  Mrv1561 08171605322D          

  4  3  0  0  0  0            999 V2000
   -0.4241   -1.7187    0.0000 C   0  0  0  0  0  0  0  0  0  0  0  0
    0.4009   -1.7187    0.0000 C   0  0  0  0  0  0  0  0  0  0  0  0
   -0.8366   -1.0043    0.0000 C   0  0  0  0  0  0  0  0  0  0  0  0
    0.8134   -2.4332    0.0000 C   0  0  0  0  0  0  0  0  0  0  0  0
  1  3  1  0  0  0  0
  2  4  1  0  0  0  0
  1  2  2  3  0  0  0
M  END
'''
molb3 = '''squiggle bond from double bond
  Mrv1561 08171605332D          

  4  3  0  0  0  0            999 V2000
   -0.4241   -1.7187    0.0000 C   0  0  0  0  0  0  0  0  0  0  0  0
    0.4009   -1.7187    0.0000 C   0  0  0  0  0  0  0  0  0  0  0  0
   -0.8366   -1.0043    0.0000 C   0  0  0  0  0  0  0  0  0  0  0  0
    0.8134   -2.4332    0.0000 C   0  0  0  0  0  0  0  0  0  0  0  0
  1  3  1  0  0  0  0
  1  2  2  0  0  0  0
  2  4  1  4  0  0  0
M  END
'''

def compare(tmb):
    print("--------------------\n")
    print "working on", tmb.split("\n")[0]
    mol = Chem.MolFromMolBlock(tmb, sanitize=False)
    print(mol.GetProp('_Name'))
    code,nmb = MolKey.CheckCTAB(tmb,isSmiles=False)
    rdcode = checker.CheckMolStructure(mol)
#    print("Avalon:\n",nmb)
#    print("RDKit:\n",Chem.MolToMolBlock(mol))
    print("Avalon:",MolKey.ErrorBitsToText(code))
    print("RDKit:",checker.StructureFlagsToString(rdcode))

compare(molb)
compare(molb2)
compare(molb3)

    
    



