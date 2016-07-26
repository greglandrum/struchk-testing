import os
from rdkit import Chem


for root, dirs, files in os.walk("substance"):
    for f in files:
        if ".sdf" in f:
            print(f)
            text = open(os.path.join(root, f)).read()
            mols = text.split("$$$$\n")
            print("number of molecules", len(mols))
            del text
            for i,m in enumerate(mols):
                rdk_m = Chem.MolFromMolBlock(m)
                if rdk_m is None:
                    oname = f.replace(".sdf", "-%06d.sdf"%i)
                    l = "rdkit_rejects"
                    if not os.path.exists(l):
                        os.mkdir(l)
                    fn = os.path.join(l, oname)
                    open(fn, 'w').write(m+"$$$$\n")


                    
                
