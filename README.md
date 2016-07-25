STRUCHK Test Molecule
=====================

This is a collection of molecules downloaded from the PubChem structures list
that are used in testing Avalon's Structure Checker and the rdkit port of
it.  

The original files are located in the substances directory.

struchk has been run on the all sdf files in the substance directory and,
if flagged, the original molecule is written to a directory named after
the error flag.  Only the original molecule is written, currently the
transformed or fixed molecule is not.

To run struchk.py first:

 1) install rdkit python with avalon tools
 2) python struchk.py

struchk will parse any sdf file in the substance directory.

currently flagged molecules are as follows:

 * atom_check_failed
 * atom_clash
 * bad_molecule
 * fragments_found
 * ok
 * stereo_error
 * transformed

note, "ok" molecules may still have atoms stripped.

see struchk.log for more specific details of the input compounds.
