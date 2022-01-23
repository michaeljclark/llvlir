# Low Level Variable Length Intermediate Representation

Low Level Variable Length Intermediate Representation is a succinct target
independent byte-code for designed deferred translation modelling a VM
designed to isolate an implementation of the C abstract virtual machine.

The following are some highlights of the LLVM and RISC-V inspired IR:

- Lisp/SSA register VM with input registers encoded as deltas.
- Fully parameterized operation type widths and vector sizes.
- Support for signed and unsigned integer operations where necessary.
- Sign or zero extension is explicit and is available for all widths.
- Atomic memory order flags available on regular loads and stores.
- Atomic support for compare and swap, lock and load, store conditional.
- Supports mainstream bit manipulation operations (ctz, clz, popc, brev).
- Vector SIMD with masked equivalents for all primitives except branches.
- Vector SIMD conversions, sign or zero extension, truncation and merges.
- Vector SIMD horizontal splat, lane shifts, rotates, and permutes (LUTs).
- Vector SIMD parallel merge, pair reduce, swap, 2D/4D zip and unzip.
- Vector SIMD double width multiply and cumulative sum.

## LLVLIR Specification

Unofficial work in progress draft of the [LLVLIR specification](/spec/llvlir.md).

### LLVLIR Build scripts

The specification contains machine readable reference tables that have been
designed to aid automated generation of encoders and decoders. The reference
tables can be extracted from the markdown specification.

#### Install python3 dependencies.

```
python3 -m pip install regex
```

#### Extract table of contents from the LLVLIR markdown.

```
./scripts/mdextract.py spec/llvlir.md 
```

#### Extract memory ordering flags from the LLVLIR markdown.

```
./scripts/mdextract.py --table memory-ordering-flags spec/llvlir.md
```

#### Create summary statistics on the operation table.

```
./scripts/stats.sh
```
