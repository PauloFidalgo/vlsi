# VLSI Project

This repository contains the VLSI (Very Large Scale Integration) project developed as part of the VLSI Projects course at FEUP (Faculty of Engineering, University of Porto) for the Master's in Electrical and Computing Engineering.


## Repository Structure

```
.
├── circuit-simulation/                              # Source code files
│   ├── eight_bit.py                                 # Simulation of the 8-bit comparator proposed
│   └── full_comparator.py                           # Simulation of the 64-bit comparator proposed
├── trace_analysis/                                  # Trace Analysis Scripts 
│   ├── post-layout/                                 # Trace Analysis post-layout
│   │   ├── verify.py                                # Verification Script
│   │   └── functional_verification_postlayout_64b.csv  # Simulation of the 64-bit comparator proposed
│   └── schematic/                                   # Trace Analysis schematic
│       ├── 8bit/                                    # 8-bit verification scripts
│       │   ├── verify.py                            # Verification script for 8-bit design
│       │   └── functional_verification_8b.csv       # Simulation results for 8-bit design
│       └── 64bit/                                   # 64-bit verification scripts
│           ├── verify.py                            # Verification script for 64-bit design
│           └── functional_verification_64b.csv      # Simulation results for 64-bit design
├── .gitattributes                                   # Git LFS configuration
├── .gitignore                                       # Git ignore file
└── README.md                                        # Project overview (this file)
```

## Authors

- Paulo Fidalgo
- Wagner Pedrosa

## License

This project is submitted for academic purposes. All rights reserved.