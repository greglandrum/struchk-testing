from __future__ import print_function
from rdkit import RDConfig
import os
from rdkit import DataStructs, Chem
from rdkit.Avalon import pyAvalonTools

struchk_conf_path = os.path.join(RDConfig.RDDataDir, 'struchk', '')
struchk_log_path = ''
STRUCHK_INIT = '''-tm
-ta %(struchk_conf_path)scheckfgs.trn
-tm
-or
-ca %(struchk_conf_path)scheckfgs.chk
-cc
-cl 3
-cs
-cn 999
-l %(struchk_log_path)sstruchk.log'''%locals()

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
            print(f)
            text = open(os.path.join(root, f)).read()
            mols = text.split("$$$$\n")
            print("number of molecules", len(mols))
            del text
            for i,m in enumerate(mols):
                (err, fixed_mol) = pyAvalonTools.CheckMoleculeString(m, False)
                oname = f.replace(".sdf", "-%06d.sdf"%i)
                if err:
                    for l in label(err):
                        if not os.path.exists(l):
                            os.mkdir(l)
                        fn = os.path.join(l, oname)
                        open(fn, 'w').write(m+"$$$$\n")
                else:
                    if not os.path.exists("ok"):
                        os.mkdir("ok")
                        
                    fn = os.path.join("ok", oname)
                    open(fn, 'w').write(m+"$$$$\n")
                    
pyAvalonTools.CloseCheckMolFiles()
                    
                
