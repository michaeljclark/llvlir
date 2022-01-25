# Low Level Variable Length Intermediate Representation

## Introduction

Low Level Variable Length Intermediate Representation is a succinct target
independent byte-code for designed deferred translation modelling a VM
designed to isolate an implementation of the C abstract virtual machine.

The opcode type integer and floating point type widths, vector sizes and
comparison sub-operations are fully parameterized. Comparison sub operations
are used consistently across compare and branch, compare branch and link,
compare and set, and conditional moves meaning all comparison types are
available across all branch and predicate operations.

The encoding favors expressiveness at the expense of redundancy and includes
some redundant variants where the translation would be to the same instruction
with the input operands are swapped.

## Reference Tables

This section details reference enumerations that are used as type parameters
or operand arguments for the intermediate representation operations:

- opcode types
- operand types
- integer type codes
- floating-point type codes
- floating point rounding modes
- floating point status flags
- floating point classification
- comparison codes
- memory ordering flags

### Opcode Types

Opcode types are used in opcode mnemonics to encode which type parameters
are needed to fully specify the type width and vector size of an operation.

mnem | mnemonic            | parameters                                       |
---- | ------------------- | ------------------------------------------------ |
`I`  | integer type        | `( iv, i8, i16, i32, i64, i128 )`                |
`F`  | floating-point type | `( fv, f16, f32, f64, f128 )`                    |
`L`  | label type          | `( local, global )`                              |
`n`  | quantifier          | `( N )`                                          |
`V`  | vector size         | `( 2, 4, 8, 16, 32, 64, 128 )`                   |
`2`  | /2 vector size      | _no argument_                                    |
`4`  | /4 vector size      | _no argument_                                    |
`D`  | *2 vector size      | _no argument_                                    |
`Q`  | *4 vector size      | _no argument_                                    |

### Operand Types

Operand types are used in format strings that encode the input and output
operands for each operation.

mnem | mnemonic           | arguments                                        |
---- | ------------------- | ------------------------------------------------ |
`v`  | void                | _no argument_                                    |
`a`  | address register    | _LEB delta_                                      |
`r`  | general register    | _LEB delta_                                      |
`f`  | float register      | _LEB delta_                                      |
`x`  | vector register     | _LEB delta_                                      |
`m`  | mask register       | _LEB delta_                                      |
`l`  | label               | _LEB prefixed string_                            |
`i`  | immediate value     | _LEB integer_                                    |
`c`  | comparison          | _LEB enum_                                       |
`o`  | memory order        | _LEB enum_                                       |
`d`  | round mode          | _LEB enum_                                       |
`s`  | string              | _LEB prefixed string_                            |
`b`  | binary              | _LEB prefixed data_                              |

### Integer Type Codes

Type codes are used to parameterize opcodes with a specific numeric type.
Type code 0 is followed by a LEB integer specifying the integer bit width.

code | name   | width  | description                             |
---- | ------ | ------ | --------------------------------------- |
0    | `iv`   | W      | variable width signed integer           |
1    | `i1`   | 1      | 1-bit signed integer                    |
2    | `i8`   | 8      | 8-bit signed integer                    |
3    | `i16`  | 16     | 16-bit signed integer                   |
4    | `i32`  | 32     | 32-bit signed integer                   |
5    | `i64`  | 64     | 64-bit signed integer                   |
6    | `i128` | 128    | 128-bit signed integer                  |

### Floating Point Type Codes

Type codes are used to parameterize opcodes with a specific numeric type.
Type code 0 is followed by two LEB integers, the first specifying the
exponent width and the second specifying the sign plus fraction bit width.

code | name   | width  | description                             |
---- | ------ | ------ | --------------------------------------- |
0    | `fv`   | E+W    | variable width floating-point           |
1    | `f16`  | 16     | IEEE Half Precision floating-point      |
2    | `f32`  | 32     | IEEE Single Precision floating-point    |
3    | `f64`  | 64     | IEEE Double Precision floating-point    |
4    | `f128` | 128    | IEEE Quadruple Precision floating-point |

### Floating Point Rounding Modes

Floating point rounding modes are used as arguments to floating point
operations that can have imprecise results. Dynamic rounding mode is
fetched and set with `fgetrm` and `fsetrm` respectively.

code | mnemonic        | description                             |
---- | --------------- | --------------------------------------- |
0    | `rne`           | Round to Nearest, ties to Even          |
1    | `rtz`           | Round towards Zero                      |
2    | `rdn`           | Round Down (towards -∞)                 |
3    | `rup`           | Round Up (towards +∞)                   |
4    | `rmm`           | Round to Nearest, ties to Max Magnitude |
7    | `dyn`           | Dynamic Rounding Mode                   |

### Floating Point Status Flags

Floating point status flags hold accrued floating point exceptions and
can be fetched and set with `fgetex` and `fsetex` respectively.

code | mnemonic        | description                             |
---- | --------------- |---------------------------------------- |
1    | `NX`            | Inexact                                 |
2    | `UF`            | Underflow                               |
4    | `OF`            | Overflow                                |
8    | `DZ`            | Divide By Zero                          |
16   | `NV`            | Invalid Operation                       |

### Floating Point Classification

Floating point classification returned by the `class` operation.

code | mnemonic        | description                             |
---- | --------------- |---------------------------------------- |
1    | `neg`           | negative                                |
2    | `sub`           | subnormal                               |
4    | `zero`          | zero                                    |
8    | `norm`          | normal                                  |
16   | `inf`           | infinite                                |
32   | `nan`           | not-a-number                            |
64   | `snan`          | signalling-not-a-number                 |

### Comparison Codes

Comparison codes for branches and predicates are composed using
three conditions: _equal-to_, _less-than_, _greater-than_, plus
_unsigned_, a modifier for _less-than_ or _greater-than_. Several
semantically redundant codes are reserved.

code | mnemonic        | description                             |
---- | --------------- |---------------------------------------- |
0    | `fa`            | false                                   |
1    | `eq`            | equal to                                |
2    | `lt`            | less than signed                        |
3    | `le`            | less than equal signed                  |
4    | `gt`            | greater than signed                     |
5    | `ge`            | greater equal than signed               |
6    | `ne`            | not equal to                            |
7    | `tr`            | true                                    |
8    | -               | unsigned _(reserved)_                   |
9    | -               | equal to unsigned _(reserved)_          |
10   | `ltu`           | less than unsigned                      |
11   | `leu`           | less than equal unsigned                |
12   | `gtu`           | greater than unsigned                   |
13   | `geu`           | greater equal than unsigned             |
14   | -               | not equal to unsigned _(reserved)_      |
15   | -               | true unsigned _(reserved)_              |

### Memory Ordering Flags

Memory ordering flaga are used as arguments on loads, stores, atomic
operations and fences.

code | mnemonic        | description                             |
---- | --------------- | --------------------------------------- |
0    | -               | relaxed                                 |
1    | `apl`           | order after predecessor loads           |
2    | `aps`           | order after predecessor stores          |
4    | `bsl`           | order before successor loads            |
8    | `bss`           | order before successor stores           |
11   | `rel`           | release = `( apl \| aps \| bss )`       |
13   | `acq`           | acquire = `( apl \| bsl \| bss )`       |

## Intermediate Representation Encoding

This section details the operation table templates that depend on typed
enumerations in the reference tables.

### Overview

Opcode names include suffixes containing an opcode type and width template
comprised of opcode type codes indicating which opcode type parameters need
to be encoded with the opcode to completely define the operation. operand type
templates indicate the types of the operation arguments to be encoded after
the opcode type parameters.

Opcode name, opcode type suffix and operand type template specify all data
required to encode the opcode, opcode type parameters and operand arguments:

```
<opcode>(.<opcode-type>+) <operand-type>+
```

Each letter in the opcode type suffix corresponds to LEB variable length
parameters encoding the width and type of the operation. each of the letters
in the operand template corresponds to label or register arguments encoded
as LEB prefixed strings or LEB deltas after the opcode type parameters.

```
<opcode> <opcode-type-parameter>... <operand-type-argument>...
```

### Constraints

Opcode types and operand types have constraints. Some opcode types are used to
compose the primary width and types of the operation while some are modify it.

- opcode types in the opcode suffix indicate vector size and types.
- opcode type parameters are encoded using a variable length code after the
  opcode in the same order as the opcode types appear in the opcode suffix.
- opcode type `V` indicates vector operation with power-of-two vector size
  encoded after the opcode.
- opcode types `I`, `F` means the operation is on integers or floating-point
  types whose type codes must be encoded after the opcode or vector size if
  `V` is present.
- opcode type `V` only appears once and applies to `x` register references.
- opcode type `V` must be followed by at least one of `I` or `F`.
- opcode types `I` and `F` can be used in combination with or without `V`
  vector size quantifier, and if more than one opcode type is present,
  the first is always the result type.
- opcode types `4`, `2`, `d` and `q` indicate respectively that the output
  vector size is quarter, half, double or quadruple the size of the input vector.
- opcode types `4`, `2`, `d` and `q` require `V` as the first opcode type.
- opcode type `N` is used for quantifiers like array lengths.
- operand types indicate order of the input and output operands to be encoded.
- operand type arguments are encoded using a variable length code after
  the opcode types.
- operand type `v` means the operation is void and returns no result.
- operand type `a`, `r`, `f`, `x`, `m`, `l`, `i` and `d` indicate address,
  general, vector, or mask register, label, immediate, and round mode.
- operand type arguments for registers are encoded as a delta referring to
  the operation creating the input. constants are represented as operations.

### Regsiter Types

There IR has five distinct register types and the types do not alias.

- address register
- general register
- float register
- vector register
- mask register

Intputs are specified as a delta to the operation that outputs their value.
Deltas are specific to each register type so are incremented whenever a new
output for a specific register type is encountered. This ensures inputs can
only refer to their type. Initial values or input terminals are the typed
constants, memory loads and move instructions. Pointer arithmetic and indexed
loads and stores exists to trace pointers and convert their difference back
into integers registers. Outside pointer values can be cast to addresses with
`mva`. Mask registers are populated from general registers using `mvm`. 

### Operation Table

The operation table details operation templates. The opcode suffixes allow
operations to be instantiated with multiple type widths and vector sizes.

opcode            | operands | description                           | category
------------------|----------|---------------------------------------|-----------
`section`         | `vs`     | section                               | data
`astring`         | `vs`     | raw string data                       | data
`astringz`        | `vs`     | raw string data (zero terminated)     | data
`ustring`         | `vs`     | UTF-8 string data                     | data
`ustringz`        | `vs`     | UTF-8 string data (zero terminated)   | data
`wstring`         | `vs`     | UTF-16 string data                    | data
`wstringz`        | `vs`     | UTF-16 string data (zero terminated)  | data
`word.I`          | `vi`     | word                                  | data
`array.NI`        | `vb`     | array                                 | data
`label.L`         | `vl`     | label address in symbol table         | constant
`consta.L`        | `al`     | load label address                    | constant
`const.I`         | `ri`     | load immediate int                    | constant
`constu.I`        | `ri`     | load immediate uint                   | constant
`const.F`         | `fi`     | load immediate float                  | constant
`sysbr.I`         | `vi`     | system break                          | system
`syscall.I`       | `vi`     | system call                           | system
`sysret.I`        | `vi`     | system return                         | system
`endbr.I`         | `vi`     | end branch                            | branch
`jalr`            | `aa`     | jump and link register                | branch
`jal.L`           | `al`     | jump and link label                   | branch
`j.L`             | `vl`     | jump label                            | branch
`cmpbr.I`         | `vcrrl`  | compare and branch                    | branch
`cmpbrlr.I`       | `acrrl`  | compare branch and link register      | branch
`fence`           | `vo`     | fence                                 | memory
`ld.I`            | `raio`   | load int                              | memory
`ldu.I`           | `raio`   | load uint                             | memory
`ld.F`            | `faio`   | load float                            | memory
`st.I`            | `vaior`  | store int                             | memory
`st.F`            | `vaiof`  | store float                           | memory
`ldidx.I`         | `raarr`  | load int stride offset                | memory
`ldidxu.I`        | `raarr`  | load uint stride offset               | memory
`ldidx.F`         | `raarr`  | load float stride offset              | memory
`stidx.I`         | `vaarrr` | store int stride offset               | memory
`stidx.F`         | `vaarrr` | store float stride offset             | memory
`ll.I`            | `raio`   | lock and load int                     | memory
`llu.I`           | `raio`   | lock and load uint                    | memory
`sc.I`            | `raior`  | store conditional int                 | memory
`mv`              | `rr`     | move int                              | arith
`mvm`             | `mr`     | move mask int                         | arith
`mva`             | `ar`     | move address int                      | arith
`addpc.I`         | `arl`    | add program counter offset label      | arith
`addp.I`          | `aar`    | add pointer int                       | arith
`subp.I`          | `aar`    | sub pointer int                       | arith
`pdiff.I`         | `raa`    | pointer difference                    | arith
`addi.I`          | `rri`    | add int imm                           | arith
`subi.I`          | `rri`    | sub int imm                           | arith
`add.I`           | `rrr`    | add int                               | arith
`addc.F`          | `rrrr`   | add with carry int                    | arith
`sub.I`           | `rrr`    | sub int                               | arith
`subb.I`          | `rrr`    | sub with borrow int                   | arith
`addu.I`          | `rrr`    | add uint                              | arith
`addcu.I`         | `rrrr`   | add with carry uint                   | arith
`subu.I`          | `rrr`    | sub uint                              | arith
`subbu.I`         | `rrr`    | sub with borrow uint                  | arith
`and.I`           | `rrr`    | logical and int                       | arith
`nand.I`          | `rrr`    | logical not and int                   | arith
`andc.I`          | `rrr`    | logical and comp int                  | arith
`or.I`            | `rrr`    | logical or int                        | arith
`nor.I`           | `rrr`    | logical not or int                    | arith
`orc.I`           | `rrr`    | logical or comp int                   | arith
`xor.I`           | `rrr`    | logical xor int                       | arith
`xnor.I`          | `rrr`    | logical not xor int                   | arith
`neg.I`           | `rr`     | negate int                            | arith
`not.I`           | `rr`     | complement int                        | arith
`min.I`           | `rrr`    | minimum int                           | arith
`max.I`           | `rrr`    | maximum int                           | arith
`minu.I`          | `rrr`    | minimum uint                          | arith
`maxu.I`          | `rrr`    | maximum uint                          | arith
`mul.I`           | `rrr`    | multiply int                          | arith
`mulu.I`          | `rrr`    | multiply uint                         | arith
`mulh.I`          | `rrr`    | multiply high int                     | arith
`mulhu.I`         | `rrr`    | multiply high uint                    | arith
`div.I`           | `rrr`    | divide int                            | arith
`rem.I`           | `rrr`    | remainder int                         | arith
`divu.I`          | `rrr`    | divide uint                           | arith
`remu.I`          | `rrr`    | remainder uint                        | arith
`rdiv.magic.I`    | `rr`     | reciprocal divide magic int           | arith
`rdiv.more.I`     | `rr`     | reciprocal divide more int            | arith
`rdiv.mult.I`     | `rrrr`   | reciprocal divide multiply int        | arith
`rdivu.magic.I`   | `rr`     | reciprocal divide magic uint          | arith
`rdivu.more.I`    | `rr`     | reciprocal divide more uint           | arith
`rdivu.mult.I`    | `rrrr`   | reciprocal divide multiply uint       | arith
`srl.I`           | `rrr`    | shift right logical int reg           | shift
`sra.I`           | `rrr`    | shift right arithmetic int reg        | shift
`sll.I`           | `rrr`    | shift left logical int reg            | shift
`srli.I`          | `rri`    | shift right logical int imm           | shift
`srai.I`          | `rri`    | shift right arithmetic int imm        | shift
`slli.I`          | `rri`    | shift left logical uint imm           | shift
`fsrl.I`          | `rrrr`   | funnel shift right logical int        | shift
`fsra.I`          | `rrrr`   | funnel shift right arithmetic int     | shift
`fsll.I`          | `rrrr`   | funnel shift left logical int         | shift
`fsrai.I`         | `rrri`   | funnel shift right logical int imm    | shift
`fsrli.I`         | `rrri`   | funnel shift right arithmetic int imm | shift
`fslli.I`         | `rrri`   | funnel shift left logical int imm     | shift
`cmps.I`          | `rcrr`   | compare and set int                   | pred
`select.I`        | `rrrr`   | select (merge) int                    | pred
`amoadd.I`        | `roar`   | atomic add int                        | atomic
`amoand.I`        | `roar`   | atomic and int                        | atomic
`amoor.I`         | `roar`   | atomic or int                         | atomic
`amoxor.I`        | `roar`   | atomic xor int                        | atomic
`amomin.I`        | `roar`   | atomic min int                        | atomic
`amomax.I`        | `roar`   | atomic max int                        | atomic
`amominu.I`       | `roar`   | atomic min uint                       | atomic
`amomaxu.I`       | `roar`   | atomic max uint                       | atomic
`amoswap.I`       | `roa`    | atomic swap int                       | atomic
`cmpswap.I`       | `rcoar`  | compare swap int                      | atomic
`bswap.I`         | `rr`     | byte swap int                         | bits
`ctz.I`           | `rr`     | count trailing zeros int              | bits
`clz.I`           | `rr`     | count leading zeros int               | bits
`popc.I`          | `rr`     | population count int                  | bits
`brev.I`          | `rr`     | bit reverse int                       | bits
`ror.I`           | `rrr`    | rotate right int reg                  | bits
`rol.I`           | `rrr`    | rotate left int reg                   | bits
`rori.I`          | `rri`    | rotate right int imm                  | bits
`roli.I`          | `rri`    | rotate left int imm                   | bits
`extract.I`       | `rrii`   | extract {offset,count} uint           | bits
`deposit.I`       | `rrii`   | deposit {offset,count} uint           | bits
`sext.II`         | `rr`     | sign extend int to int                | bits
`zext.II`         | `rr`     | zero extend uint to uint              | bits
`trunc.II`        | `rr`     | truncate uint to uint                 | bits
`cvt.FI`          | `frd`    | convert int to float                  | fp-conv
`cvtu.FI`         | `frd`    | convert uint to float                 | fp-conv
`cvt.IF`          | `rf`     | convert float to int                  | fp-conv
`cvt.FF`          | `ffd`    | convert float to float                | fp-conv
`frac.IF`         | `rfd`    | float fraction int                    | fp-conv
`exp.IF`          | `rfd`    | float exponent int                    | fp-conv
`comp.FI`         | `frrd`   | float compose {mant,exp} float        | fp-conv
`fgetrm`          | `r`      | get fpu rounding mode                 | fp-control
`fgetex`          | `r`      | get fpu accrued exceptions            | fp-control
`fsetrm`          | `vr`     | set fpu rounding mode                 | fp-control
`fsetex`          | `vr`     | set fpu accrued exceptions            | fp-control
`mv.F`            | `ff`     | move float                            | fp-arith
`madd.F`          | `ffffd`  | fused multiply add float              | fp-arith
`msub.F`          | `ffffd`  | fused multiply sub float              | fp-arith
`mnadd.F`         | `ffffd`  | fused multiply neg add float          | fp-arith
`mnsub.F`         | `ffffd`  | fused multiply neg sub float          | fp-arith
`add.F`           | `fffd`   | add float                             | fp-arith
`sub.F`           | `fffd`   | sub float                             | fp-arith
`mul.F`           | `fffd`   | multiply float                        | fp-arith
`div.F`           | `fffd`   | divide float                          | fp-arith
`copysign.F`      | `fff`    | copysign float                        | fp-arith
`copysign_xor.F`  | `fff`    | copysign xor float                    | fp-arith
`copysign_not.F`  | `fff`    | copysign not float                    | fp-arith
`min.F`           | `fff`    | minimum float                         | fp-arith
`max.F`           | `fff`    | maximum float                         | fp-arith
`sqrt.F`          | `ffd`    | square root float                     | fp-arith
`cmps.F`          | `rcff`   | compare and set float                 | fp-pred
`select.F`        | `frff`   | select (merge) float                  | fp-pred
`class.F`         | `rf`     | classify float                        | fp-pred
`ld.VI`           | `xaiom`  | load int                              | vec-memory
`ldu.VI`          | `xaiom`  | load uint                             | vec-memory
`ld.VF`           | `xaiom`  | load float                            | vec-memory
`st.VI`           | `vaioxm` | store int                             | vec-memory
`st.VF`           | `vaioxm` | store float                           | vec-memory
`gather.VII`      | `xaxom`  | gather load int {indices}             | vec-memory
`gatheru.VII`     | `xaxom`  | gather load uint {indices}            | vec-memory
`gather.VIF`      | `xaxom`  | gather load float {indices}           | vec-memory
`scatter.VII`     | `vaxoxm` | scatter store int {indices}           | vec-memory
`scatteru.VII`    | `vaxoxm` | scatter store uint {indices}          | vec-memory
`scatter.VIF`     | `vaxoxm` | scatter store float {indices}         | vec-memory
`mv.x.x.VI`       | `xx`     | move vec to vec                       | vec-arith
`mv.x.r.VI`       | `xr`     | move int to vec                       | vec-arith
`mv.r.x.VI`       | `rx`     | move vec to int                       | vec-arith
`splati.VI`       | `xim`    | splat (broadcast) int imm             | vec-arith
`splatui.VI`      | `xim`    | splat (broadcast) uint imm            | vec-arith
`splat.VI`        | `xrm`    | splat (broadcast) int reg             | vec-arith
`add.VI`          | `xxxm`   | add int                               | vec-arith
`addc.VI`         | `xxxm`   | add with carry int                    | vec-arith
`sub.VI`          | `xxxm`   | sub int                               | vec-arith
`subb.VI`         | `xxxm`   | sub wth borrow int                    | vec-arith
`addu.VI`         | `xxxm`   | add uint                              | vec-arith
`addcu.VI`        | `xxxm`   | add with carry uint                   | vec-arith
`subu.VI`         | `xxxm`   | sub uint                              | vec-arith
`subbu.VI`        | `xxxm`   | sub with borrow uint                  | vec-arith
`and.VI`          | `xxxm`   | logical and int                       | vec-arith
`nand.VI`         | `xxxm`   | logical not and int                   | vec-arith
`andc.VI`         | `xxxm`   | logical and comp int                  | vec-arith
`or.VI`           | `xxxm`   | logical or int                        | vec-arith
`nor.VI`          | `xxxm`   | logical not or int                    | vec-arith
`orc.VI`          | `xxxm`   | logical or comp int                   | vec-arith
`xor.VI`          | `xxxm`   | logical xor int                       | vec-arith
`xnor.VI`         | `xxxm`   | logical not xor int                   | vec-arith
`neg.VI`          | `xxm`    | negate int                            | vec-arith
`not.VI`          | `xxm`    | complement int                        | vec-arith
`min.VI`          | `xxxm`   | minimum int                           | vec-arith
`max.VI`          | `xxxm`   | maximum int                           | vec-arith
`minu.VI`         | `xxxm`   | minimum uint                          | vec-arith
`maxu.VI`         | `xxxm`   | maximum uint                          | vec-arith
`mul.VI`          | `xxxm`   | multiply int                          | vec-arith
`mul.VID`         | `xxxm`   | multiply (double-width) int           | vec-arith
`mulu.VI`         | `xxxm`   | multiply uint                         | vec-arith
`mulu.VID`        | `xxxm`   | multiply (double-width) uint          | vec-arith
`mulh.VI`         | `xxxm`   | multiply high int                     | vec-arith
`mulhu.VI`        | `xxxm`   | multiply high uint                    | vec-arith
`div.VI`          | `xxxm`   | divide int                            | vec-arith
`rem.VI`          | `xxxm`   | remainder int                         | vec-arith
`divu.VI`         | `xxxm`   | divide uint                           | vec-arith
`remu.VI`         | `xxxm`   | remainder uint                        | vec-arith
`rdiv.mult.VI`    | `xxrr`   | reciprocal divide multiply int        | vec-arith
`rdivu.mult.VI`   | `xxrr`   | reciprocal divide multiply uint       | vec-arith
`srl.VI`          | `xxrm`   | shift right logical int reg           | vec-shift
`sra.VI`          | `xxrm`   | shift right arithmetic int reg        | vec-shift
`sll.VI`          | `xxrm`   | shift left logical int reg            | vec-shift
`srli.VI`         | `xxim`   | shift right logical int imm           | vec-shift
`srai.VI`         | `xxim`   | shift right arithmetic int imm        | vec-shift
`slli.VI`         | `xxim`   | shift left logical uint imm           | vec-shift
`srlx.VI`         | `xxxm`   | shift right logical int vec           | vec-shift
`srax.VI`         | `xxxm`   | shift right arithmetic int vec        | vec-shift
`sllx.VI`         | `xxxm`   | shift left logical uint vec           | vec-shift
`fsrl.VI`         | `xxxrm`  | funnel shift right logical int        | vec-shift
`fsra.VI`         | `xxxrm`  | funnel shift right arithmetic int     | vec-shift
`fsll.VI`         | `xxxrm`  | funnel shift left logical int         | vec-shift
`fsrai.VI`        | `xxxim`  | funnel shift right logical int imm    | vec-shift
`fsrli.VI`        | `xxxim`  | funnel shift right arithmetic int imm | vec-shift
`fslli.VI`        | `xxxim`  | funnel shift left logical int imm     | vec-shift
`fsrax.VI`        | `xxxxm`  | funnel shift right logical int vec    | vec-shift
`fsrlx.VI`        | `xxxxm`  | funnel shift right arithmetic int vec | vec-shift
`fsllx.VI`        | `xxxxm`  | funnel shift left logical int vec     | vec-shift
`cmps.VI`         | `mcxxm`  | compare and set int                   | vec-pred
`select.VI`       | `xxxm`   | select (merge) int                    | vec-pred
`bswap.VI`        | `xxm`    | byte swap int                         | vec-bits
`ctz.VI`          | `xxm`    | count trailing zeros int              | vec-bits
`clz.VI`          | `xxm`    | count leading zeros int               | vec-bits
`popc.VI`         | `xxm`    | population count int                  | vec-bits
`brev.VI`         | `xxm`    | bit reverse int                       | vec-bits
`ror.VI`          | `xxrm`   | rotate right int reg                  | vec-bits
`rol.VI`          | `xxrm`   | rotate left int reg                   | vec-bits
`rori.VI`         | `xxim`   | rotate right int imm                  | vec-bits
`roli.VI`         | `xxim`   | rotate left int imm                   | vec-bits
`rorv.VI`         | `xxxm`   | rotate right int vec                  | vec-bits
`rolv.VI`         | `xxxm`   | rotate left int vec                   | vec-bits
`extract.VI`      | `xxiim`  | extract {offset,count} uint           | vec-bits
`deposit.VI`      | `xxiim`  | deposit {offset,count} uint           | vec-bits
`permute_16x4.VI` | `xxrm`   | permute {nibble indices} uint         | vec-horiz
`permute_8x8.VI`  | `xxrm`   | permute {byte indices} uint           | vec-horiz
`permute.VII`     | `xxxm`   | permute {vector indices} uint         | vec-horiz
`sext.VII`        | `xxm`    | sign extend int to int                | vec-horiz
`zext.VII`        | `xxm`    | zero extend uint to uint              | vec-horiz
`trunc.VII`       | `xxm`    | truncate uint                         | vec-horiz
`lsr.VI`          | `xxx`    | lane shift right uint                 | vec-horiz
`lsl.VI`          | `xxx`    | lane shift left uint                  | vec-horiz
`lror.VI`         | `xxx`    | lane rotate right uint                | vec-horiz
`ltor.VI`         | `xxx`    | lane rotate left uint                 | vec-horiz
`lzip01.VID`      | `xxx`    | lane zip mod 2 lane 0,1 uint          | vec-horiz
`lzip01.VIQ`      | `xxx`    | lane zip mod 4 lane 0,1 uint          | vec-horiz
`lzip23.VIQ`      | `xxx`    | lane zip mod 4 lane 2,3 uint          | vec-horiz
`lunzip0.VI2`     | `xxx`    | lane unzip mod 2 lane 0 uint          | vec-horiz
`lunzip1.VI2`     | `xxx`    | lane unzip mod 2 lane 1 uint          | vec-horiz
`lunzip0.VI4`     | `xxx`    | lane unzip mod 4 lane 0 uint          | vec-horiz
`lunzip1.VI4`     | `xxx`    | lane unzip mod 4 lane 1 uint          | vec-horiz
`lunzip2.VI4`     | `xxx`    | lane unzip mod 4 lane 2 uint          | vec-horiz
`lunzip3.VI4`     | `xxx`    | lane unzip mod 4 lane 3 uint          | vec-horiz
`pair.swap.VI`    | `xxm`    | pair swap uint                        | vec-horiz
`pair.add.VI2`    | `xxm`    | pair add reduce int                   | vec-horiz
`pair.addu.VI2`   | `xxm`    | pair add reduce uint                  | vec-horiz
`pair.sub.VI2`    | `xxm`    | pair sub reduce int                   | vec-horiz
`pair.subu.VI2`   | `xxm`    | pair sub reduce uint                  | vec-horiz
`cumsum.VI`       | `xxm`    | cumulative sum int                    | vec-horiz
`cumsumu.VI`      | `xxm`    | cumulative sum uint                   | vec-horiz
`mv.x.f.VF`       | `xf`     | move float to vec                     | vec-fp-conv
`mv.f.x.VF`       | `fx`     | move vec to float                     | vec-fp-conv
`splat.VF`        | `xfm`    | splat (broadcast) float reg           | vec-fp-conv
`cvt.VFI`         | `xxdm`   | convert int to float                  | vec-fp-conv
`cvtu.VFI`        | `xxdm`   | convert uint to float                 | vec-fp-conv
`cvt.VIF`         | `xxm`    | convert float to int                  | vec-fp-conv
`cvt.VFF`         | `xxdm`   | convert float to float                | vec-fp-conv
`frac.VIF`        | `xxdm`   | float fraction int                    | vec-fp-conv
`exp.VIF`         | `xxdm`   | float exponent int                    | vec-fp-conv
`comp.VFI`        | `xxxdm`  | float compose {mant,exp} float        | vec-fp-conv
`madd.VF`         | `xxxxdm` | fused multiply add float              | vec-fp-arith
`msub.VF`         | `xxxxdm` | fused multiply sub float              | vec-fp-arith
`mnadd.VF`        | `xxxxdm` | fused multiply neg add float          | vec-fp-arith
`mnsub.VF`        | `xxxxdm` | fused multiply neg sub float          | vec-fp-arith
`add.VF`          | `xxxdm`  | add float                             | vec-fp-arith
`sub.VF`          | `xxxdm`  | sub float                             | vec-fp-arith
`mul.VFD`         | `xxxdm`  | multiply float                        | vec-fp-arith
`div.VF`          | `xxxdm`  | divide float                          | vec-fp-arith
`copysign.VF`     | `xxxm`   | copysign float                        | vec-fp-arith
`copysign_xor.VF` | `xxxm`   | copysign xor float                    | vec-fp-arith
`copysign_not.VF` | `xxxm`   | copysign not float                    | vec-fp-arith
`min.VF`          | `xxxm`   | minimum float                         | vec-fp-arith
`max.VF`          | `xxxm`   | maximum float                         | vec-fp-arith
`sqrt.VF`         | `xxdm`   | square root float                     | vec-fp-arith
`cmps.VIF`        | `xcxxm`  | compare and set float                 | vec-fp-pred
`select.VIF`      | `xxxxm`  | select float                          | vec-fp-pred
`class.VIF`       | `xxm`    | classify float                        | vec-fp-pred
`pair.add.VF2`    | `xxm`    | pair add reduce float                 | vec-fp-horiz
`pair.sub.VF2`    | `xxm`    | pair sub reduce int                   | vec-fp-horiz
`cumsum.VF`       | `xxm`    | cumulative sum float                  | vec-fp-horiz

### Operation Statistics

category        | count
--------------- | -----
data            | 9
constant        | 5
system          | 3
branch          | 6
memory          | 15
arith           | 39
shift           | 21
pred            | 2
atomic          | 10
bits            | 14
fp-conv         | 7
fp-control      | 4
fp-arith        | 15
fp-pred         | 3
vec-memory      | 11
vec-arith       | 38
vec-shift       | 18
vec-pred        | 2
vec-bits        | 13
vec-horiz       | 26
vec-fp-conv     | 10
vec-fp-arith    | 14
vec-fp-pred     | 3
vec-fp-horiz    | 3
total           | 282
