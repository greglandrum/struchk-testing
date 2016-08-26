from __future__ import print_function
from rdkit import RDConfig
import os
from rdkit import DataStructs, Chem
from rdkit.Avalon import pyAvalonTools
from rdkit.Chem import rdStructChecker



struchk_conf_path = os.path.join(RDConfig.RDDataDir, 'struchk', '')

# don't load transform atoms for now
struchk_log_path = ''
STRUCHK_INIT = '''-tm
-tm
-or
-ca %(struchk_conf_path)scheckfgs.chk
-cc
-cl 3
-cs
-cn 999
-l %(struchk_log_path)sstruchk.log'''%locals()

opts = rdStructChecker.StructCheckerOptions()
opts.LoadGoodAugmentedAtoms("%(struchk_conf_path)scheckfgs.chk"%locals())

opts.RemoveMinorFragments = True
# -or => opts.?
opts.CheckCollisions = True
opts.CollisionLimitPercent = 3
opts.CheckStereo = True
opts.MaxMolSize = 999


checker = rdStructChecker.StructChecker(opts)

r = pyAvalonTools.InitializeCheckMol(STRUCHK_INIT)

def label(err):
    res = []
    for name, flag in pyAvalonTools.StruChkFlag.__dict__.items():
        try:
            if flag & err:
                res.append(name)
        except:
            pass
    return res
    
for root, dirs, files in os.walk("substance"):
    for f in files:
        if ".sdf" in f:
            print("Examining file", f)
            text = open(os.path.join(root, f)).read()
            mols = text.split("$$$$\n")
            print("number of molecules", len(mols))
            del text
            for i,m in enumerate(mols):
                (err, fixed_mol) = pyAvalonTools.CheckMoleculeString(m, False)
                #print m
                mol = Chem.MolFromMolBlock(m)
                #print("Smiles:", Chem.MolToSmiles(mol))
                if not mol:
                    continue
                
                err2 = checker.CheckMolStructure(mol)
                
                labels = [l.lower() for l in checker.StructureFlagsToString(err2).split(",") if l]
                if sorted(labels) == sorted(label(err)):
                    print("...ok")
                    continue
                    
                                            
                print("...Failed" , "expected:", sorted(label(err)), "got:", sorted(labels))
                expected = repr(sorted(label(err)))
                got = repr(labels)
                m += "> <EXPECTED>\n%s\n\n> <GOT>\n%s\n\n$$$$\n"%(expected, got)

                oname = f.replace(".sdf", "-%06d.sdf"%i)
                if err:
                    for l in label(err):
                        if not os.path.exists(l):
                            os.mkdir(l)
                        fn = os.path.join(l, oname)
                        open(fn, 'w').write(m)
                else:
                    if not os.path.exists("ok"):
                        os.mkdir("ok")
                        
                    fn = os.path.join("ok", oname)
                    open(fn, 'w').write(m)
                    
pyAvalonTools.CloseCheckMolFiles()
                    
                
