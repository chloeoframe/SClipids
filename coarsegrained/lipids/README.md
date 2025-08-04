cg-force-field.xml is the original SPP (includes OH3 and OH4)
og.xml is the same as above, I just made a copy 
as.xml is when we started treating the acyl and sphingosine tails separately
dbcg-force-field.xml is the double bond xml where we make the one CG bead on the sphing., with normally a tail bead a TAILD 
asends.xml is when we treat the ends of the acyl or sphing tails differently 
includingeos.xml is when EOS related beads are included (TAILD, TAIL2, ESTER, etc)


openNS is with a topology of the CER already opened (in an extended conf) so when you SA it, it's packed all open already (did this for Annette but it didn't matter bc in NVE the CERs slammed shut to deal with space and minimizing energy)

cer1_parash is the EOS molecule to use
cer2-24AS is with TAILA and TAILS to separate acyl and sphing. tail beads
cer2-24ASends1 is with a mixture of TAILA and TAILS where the last 2 beads on the acyl are nomral TAIL (did this to try to get phase sep. but also interdigitation)
cer2-24ASends2 is with a mixture of TAILA and TAILS where the last 2 beads on both tails are normal TAIL (again tried to get interdig. to come back after doing sep. TAILA and TAILS and creating long-long, short-short domains)

cer2-24db is with the TAIL bead on the sphing. chain closest to the head is a TAILD from parash's EOS derivation to see if normal TAIL or accounting for the double bond there really matters in self-assembling CER NS (it don't)

sphing is just a free sphingosine tail (CER NS broken apart) 

FFA20 is actually FFA20 based upon how our mapping goes; when we reverse-map back to AA though, it actually is the real FFA20
and FFA26 is actually FFA25

CER1 = CER EOS
CER2 = CER NS
CER3 = CER NP
CER5 = CER AS
CER6 = CER AP
CER8 = CER NH
