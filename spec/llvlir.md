# Low Level Variable Length Intermediate Representation

## Introduction

Low Level Variable Length Intermediate Representation is a succinct
target-independent byte-code designed for deferred translation, modelling a
VM designed to isolate an implementation of the C abstract virtual machine.

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
- endianness codes
- floating-point type codes
- floating point rounding modes
- floating point status flags
- floating point classification
- comparison codes
- memory ordering flags
- type parameter codes
- type definition flags

### Opcode Types

Opcode types are used in opcode mnemonics to encode which type parameters
are needed to fully specify the type width and vector size of an operation.

mnem | mnemonic            | parameters                                       |
---- | ------------------- | ------------------------------------------------ |
`T`  | type type           | _type hash_                                      |
`P`  | procedure type      | `{ p32, p64 }`                                   |
`A`  | address type        | `{ a32, a64 }`                                   |
`I`  | integer type        | `( iv, i8, i16, i32, i64, i128 )`                |
`F`  | floating-point type | `( fv, f16, f32, f64, f128 )`                    |
`E`  | endianness          | `{ le, be }`                                     |
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
`t`  | type register       | _LEB delta_                                      |
`a`  | address register    | _LEB delta_                                      |
`p`  | procedure register  | _LEB delta_                                      |
`r`  | general register    | _LEB delta_                                      |
`f`  | float register      | _LEB delta_                                      |
`x`  | vector register     | _LEB delta_                                      |
`m`  | mask register       | _LEB delta_                                      |
`l`  | label               | _LEB prefixed string_                            |
`i`  | immediate value     | _LEB integer_                                    |
`c`  | comparison          | _LEB enum_                                       |
`o`  | order memory        | _LEB enum_                                       |
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
4    | `i24`  | 24     | 24-bit signed integer                   |
5    | `i32`  | 32     | 32-bit signed integer                   |
6    | `i48`  | 48     | 48-bit signed integer                   |
7    | `i64`  | 64     | 64-bit signed integer                   |
8    | `i96`  | 96     | 96-bit signed integer                   |
9    | `i128` | 128    | 128-bit signed integer                  |

### Endianness Codes

Endianness codes are used to parameterize loads and stores.

code | mnemonic        | description                             |
---- | --------------- | --------------------------------------- |
0    | `le`            | Little-Endian                           |
1    | `be`            | Big-Endian                              |

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

Memory ordering flags are used as arguments on loads, stores, atomic
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

### Type Parameter Codes

Type parameter codes are used to tie the expected type kind for
typed memory operations back to the type. In particular they
control how the index parameter is interpreted, ignored for set,
enum, and field; used as an element index for arrays; or used
as an attribute index for struct and union. Type information is
normally static, but if type values are loaded from memory then
the type parameter should be checked. load address with type is
used to calculate offsets which can usually be performed either
statically or at link time.

pow2 | mnemonic        | description                             |
---- | --------------- | --------------------------------------- |
0    | `intrinsic`     | intrinsic type                          |
1    | `set`           | set type                                |
2    | `enum`          | enum type                               |
3    | `struct`        | struct type                             |
4    | `union`         | union type                              |
5    | `field`         | field type                              |
6    | `array`         | array type                              |

### Type Definition Flags

Type definition flags are the set of attributes that apply to type
operations which define types mapping to the C language types.

pow2 | mnemonic        | description                             |
---- | --------------- | --------------------------------------- |
0    | `void`          | void type                               |
1<<0 | `integral`      | integral type                           |
1<<1 | `real`          | real number                             |
1<<2 | `complex`       | complex number                          |
1<<3 | `signed`        | signed type                             |
1<<4 | `unsigned`      | unsigned type                           |
1<<5 | `ieee754`       | IEEE-754 floating-point                 |
\-   | `sint`          | `( integral \| signed )`                |
\-   | `uint`          | `( integral \| unsigned )`              |
\-   | `float`         | `( real     \| ieee754 )`               |
\-   | `cfloat`        | `( complex  \| ieee754 )`               |
1<<6 | `pad_pow2`      | struct pow2 padding                     |
1<<7 | `pad_bit`       | struct bit padding                      |
1<<8 | `pad_byte`      | struct byte padding                     |
1<<9 | `bitfield`      | struct bitfield width present           |
1<<10| `const`         | qualifier const                         |
1<<11| `volatile`      | qualifier volatile                      |
1<<12| `restrict`      | qualifier restrict                      |
1<<13| `static`        | storage static                          |
1<<14| `extern_c`      | C function or variable                  |
1<<15| `inline`        | inline function                         |
1<<16| `noreturn`      | noreturn function                       |
1<<17| `local`         | field binding local                     |
1<<18| `global`        | field binding global                    |
1<<19| `weak`          | field binding weak                      |
1<<20| `default`       | field visibility default                |
1<<21| `hidden`        | field visibility hidden                 |
1<<22| `in`            | param input                             |
1<<23| `out`           | param output                            |
1<<24| `vla`           | array is variable length                |

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

There IR has seven distinct register types and the types do not alias.

- type register
- address register
- procedure register
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
`typedef.T`       | `tst`    | typedef `name type`                   | types
`intrinsic.T`     | `tsii`   | intrinsic `name width flags`          | types
`set.T`           | `tsit`   | list of masks `width constant`        | types
`enum.T`          | `tsit`   | list of integers `width constant`     | types
`struct.T`        | `tst`    | list of adjacent types `name type`    | types
`union.T`         | `tst`    | list of overlapping types `name type` | types
`field.T`         | `tsti`   | field `name type bitfield-width`      | types
`array.T`         | `ttii`   | array `type count flags`              | types
`pointer.T`       | `tti`    | pointer `type width`                  | types
`constant.T`      | `tsi`    | constant `name imm`                   | types
`function.T`      | `tsti`   | function `name param flags`           | types
`param.T`         | `tsti`   | parameter `name type flags`           | types
`qualifier.T`     | `tit`    | qualifier `type flags`                | types
`attribute.T`     | `tst`    | attribute `name value`                | types
`value.T`         | `tsi`    | value `string imm`                    | types
`archive.T`       | `tst`    | archive `name source`                 | types
`source.T`        | `tst`    | source `name type`                    | types
`alias.T`         | `tsti`   | alias `name type flags`               | types
`section`         | `vs`     | section `name`                        | data
`astring`         | `vs`     | raw string `data`                     | data
`astringz`        | `vs`     | raw string `data` (zero terminated)   | data
`ustring`         | `vs`     | UTF-8 string `data`                   | data
`ustringz`        | `vs`     | UTF-8 string `data` (zero terminated) | data
`wstring`         | `vs`     | UTF-16 string `data`                  | data
`wstringz`        | `vs`     | UTF-16 string `data` (zero terminated)| data
`word.I`          | `vi`     | word `imm`                            | data
`array.NI`        | `vb`     | array `data`                          | data
`label.L`         | `vl`     | label `name`                          | constant
`consta.L`        | `al`     | load addr `label`                     | constant
`const.I`         | `ri`     | load int `imm`                        | constant
`constu.I`        | `ri`     | load uint `imm`                       | constant
`const.F`         | `fi`     | load float `imm`                      | constant
`random.I`        | `r`      | load random bits                      | system
`sysbr.I`         | `vi`     | system break `imm`                    | system
`syscall.I`       | `vi`     | system call `imm`                     | system
`sysret.I`        | `vi`     | system return `imm`                   | system
`systime.i64`     | `r`      | system time (nanoseconds from J2000.0)| system
`jalp.P`          | `ap`     | jump and link `proc`                  | branch-safe
`jal.L`           | `al`     | jump and link `label`                 | branch-safe
`j.L`             | `vl`     | jump `label`                          | branch-safe
`cmpbr.I`         | `vcrrl`  | compare and branch `label`            | branch-safe
`cmpbrlr.IP`      | `acrrp`  | compare branch and link `proc`        | branch-safe
`cmpbrlr.IL`      | `acrrl`  | compare branch and link `label`       | branch-safe
`jalr.A`          | `aia`    | jump and link `tag addr`              | branch-unsafe
`cmpbrlr.IA`      | `acrria` | compare branch and link `tag addr`    | branch-unsafe
`endbr.I`         | `vi`     | end branch `tag`                      | branch-unsafe
`ld.EI`           | `rao`    | load int `addr mo`                    | memory-unsafe
`ldu.EI`          | `rao`    | load uint `addr mo`                   | memory-unsafe
`ldf.F`           | `fao`    | load float `addr mo`                  | memory-unsafe
`ldt.T`           | `tao`    | load type `addr mo`                   | memory-unsafe
`lda.A`           | `aao`    | load addr `addr mo`                   | memory-unsafe
`ldp.P`           | `pao`    | load proc `addr mo`                   | memory-unsafe
`ll.EI`           | `rao`    | load-locked int `addr mo`             | memory-unsafe
`llu.EI`          | `rao`    | load-locked uint `addr mo`            | memory-unsafe
`st.EI`           | `varo`   | store int `addr int mo`               | memory-unsafe
`stf.F`           | `vafo`   | store float `addr float mo`           | memory-unsafe
`stt.T`           | `vato`   | store type `addr type mo`             | memory-unsafe
`sta.A`           | `vaao`   | store addr `addr addr mo`             | memory-unsafe
`stp.P`           | `vapo`   | store proc `addr proc mo`             | memory-unsafe
`sc.EI`           | `raro`   | store-cond int `addr int mo`          | memory-unsafe
`ld.index.EI`     | `rarrro` | load int `addr idx mul off mo`        | memory-unsafe
`ldu.index.EI`    | `rarrro` | load uint `addr idx mul off mo`       | memory-unsafe
`ldf.index.F`     | `farrro` | load float `addr idx mul off mo`      | memory-unsafe
`lda.index.T`     | `tarrro` | load type `addr idx mul off mo`       | memory-unsafe
`lda.index.A`     | `aarrro` | load addr `addr idx mul off mo`       | memory-unsafe
`ldp.index.P`     | `parrro` | load proc `addr idx mul off mo`       | memory-unsafe
`st.index.EI`     | `varrrro`| store int `addr idx mul off mo`       | memory-unsafe
`stf.index.F`     | `varrrfo`| store float `addr idx mul off mo`     | memory-unsafe
`stt.index.T`     | `varrrto`| store type `addr idx mul off mo`      | memory-unsafe
`sta.index.A`     | `varrrao`| store addr `addr idx mul off mo`      | memory-unsafe
`stp.index.P`     | `varrrpo`| store proc `addr idx mul off mo`      | memory-unsafe
`alloc.TA`        | `atr`    | alloc `type count`                    | memory-safe
`dealloc.TA`      | `vta`    | dealloc `type addr`                   | memory-safe
`init.TA`         | `vta`    | init `type addr`                      | memory-safe
`uninit.TA`       | `vta`    | uninit `type addr`                    | memory-safe
`ref.TA`          | `ata`    | ref `type count`                      | memory-safe
`unref.TA`        | `ata`    | unref `type addr`                     | memory-safe
`ld.TI`           | `rtaro`  | load int `type addr idx mo`           | memory-safe
`ldu.TI`          | `rtaro`  | load uint `type addr idx mo`          | memory-safe
`ll.TI`           | `rtaro`  | load-locked int `type addr idx mo`    | memory-safe
`llu.TI`          | `rtaro`  | load-locked uint `type addr idx mo`   | memory-safe
`ldf.TF`          | `ftaro`  | load float `type addr idx mo`         | memory-safe
`ldt.TT`          | `ttaro`  | load type `type addr idx mo`          | memory-safe
`lda.TA`          | `ataro`  | load addr `type addr idx mo`          | memory-safe
`lda.TP`          | `ptaro`  | load proc `type addr idx mo`          | memory-safe
`st.TI`           | `vtarro` | store int `type addr idx int mo`      | memory-safe
`st.TF`           | `vtarfo` | store float `type addr idx float mo`  | memory-safe
`st.TT`           | `vtarto` | store type `type addr idx type mo`    | memory-safe
`st.TA`           | `vtarao` | store addr `type addr idx addr mo`    | memory-safe
`st.TP`           | `vtarpo` | store proc `type addr idx proc mo`    | memory-safe
`sc.TI`           | `rtarro` | store-cond int `type addr idx int mo` | memory-safe
`mv`              | `rr`     | move `int int`                        | arith
`mvm`             | `mr`     | move `mask int`                       | arith
`mva`             | `ar`     | move `addr int`                       | memory-unsafe
`addpc.I`         | `arl`    | add program counter `int label`       | memory-unsafe
`addp.I`          | `aar`    | add pointer int `addr int`            | memory-unsafe
`subp.I`          | `aar`    | sub pointer int `addr int`            | memory-unsafe
`pdiff.I`         | `raa`    | pointer difference `addr addr`        | memory-unsafe
`addi.I`          | `rri`    | add `int imm`                         | arith
`subi.I`          | `rri`    | sub `int imm`                         | arith
`add.I`           | `rrr`    | add `int int`                         | arith
`addc.F`          | `rrrr`   | add3 `int int int`                    | arith
`sub.I`           | `rrr`    | sub `int int`                         | arith
`subb.I`          | `rrr`    | sub3 `int int int`                    | arith
`addu.I`          | `rrr`    | add uint `int int`                    | arith
`addcu.I`         | `rrrr`   | add3 `uint uint uint`                 | arith
`subu.I`          | `rrr`    | sub `uint uint`                       | arith
`subbu.I`         | `rrr`    | sub3 `uint uint uint`                 | arith
`and.I`           | `rrr`    | logical and `uint uint`               | arith
`nand.I`          | `rrr`    | logical not and `uint uint`           | arith
`andc.I`          | `rrr`    | logical and comp `uint uint`          | arith
`or.I`            | `rrr`    | logical or `uint uint`                | arith
`nor.I`           | `rrr`    | logical not or `uint uint`            | arith
`orc.I`           | `rrr`    | logical or comp `uint uint`           | arith
`xor.I`           | `rrr`    | logical xor `uint uint`               | arith
`xnor.I`          | `rrr`    | logical not xor `uint uint`           | arith
`neg.I`           | `rr`     | negate `int`                          | arith
`not.I`           | `rr`     | complement `uint`                     | arith
`min.I`           | `rrr`    | minimum `int int`                     | arith
`max.I`           | `rrr`    | maximum `int int`                     | arith
`minu.I`          | `rrr`    | minimum `uint uint`                   | arith
`maxu.I`          | `rrr`    | maximum `uint uint`                   | arith
`mul.I`           | `rrr`    | multiply `int int`                    | arith
`mulu.I`          | `rrr`    | multiply `uint uint`                  | arith
`mulsu.I`         | `rrr`    | multiply `uint int`                   | arith
`mulh.I`          | `rrr`    | multiply high `int int`               | arith
`mulhu.I`         | `rrr`    | multiply high `uint uint`             | arith
`div.I`           | `rrr`    | divide `int int`                      | arith
`rem.I`           | `rrr`    | remainder `int int`                   | arith
`divu.I`          | `rrr`    | divide `uint uint`                    | arith
`remu.I`          | `rrr`    | remainder `uint uint`                 | arith
`rdiv.magic.I`    | `rr`     | recip divide magic `int`              | arith
`rdiv.more.I`     | `rr`     | recip divide more `int`               | arith
`rdiv.mult.I`     | `rrrr`   | recip divide mult `int int int`       | arith
`rdivu.magic.I`   | `rr`     | recip divide magic `uint`             | arith
`rdivu.more.I`    | `rr`     | recip divide more `uint`              | arith
`rdivu.mult.I`    | `rrrr`   | recip divide mult `uint uint uint`    | arith
`srl.I`           | `rrr`    | shift right logical `int reg`         | shift
`sra.I`           | `rrr`    | shift right arithmetic `int reg`      | shift
`sll.I`           | `rrr`    | shift left logical `int reg`          | shift
`srli.I`          | `rri`    | shift right logical `int imm`         | shift
`srai.I`          | `rri`    | shift right arithmetic `int imm`      | shift
`slli.I`          | `rri`    | shift left logical `uint imm`         | shift
`fsrl.I`          | `rrrr`   | funnel shift right logical `int reg`  | shift
`fsra.I`          | `rrrr`   | funnel shift right arith `int reg`    | shift
`fsll.I`          | `rrrr`   | funnel shift left logical `int reg`   | shift
`fsrai.I`         | `rrri`   | funnel shift right logical `int imm`  | shift
`fsrli.I`         | `rrri`   | funnel shift right arith `int imm`    | shift
`fslli.I`         | `rrri`   | funnel shift left logical `int imm`   | shift
`cmps.I`          | `rcrr`   | compare and set `cnd int int`         | pred
`select.I`        | `rrrr`   | select (merge) `int int int`          | pred
`fence`           | `vo`     | fence `mo`                            | atomic
`amoadd.I`        | `raro`   | atomic add `addr int mo`              | atomic
`amoand.I`        | `raro`   | atomic and `addr int mo`              | atomic
`amoor.I`         | `raro`   | atomic or `addr int mo`               | atomic
`amoxor.I`        | `raro`   | atomic xor `addr int mo`              | atomic
`amomin.I`        | `raro`   | atomic min `addr int mo`              | atomic
`amomax.I`        | `raro`   | atomic max `addr int mo`              | atomic
`amominu.I`       | `raro`   | atomic min `addr uint mo`             | atomic
`amomaxu.I`       | `raro`   | atomic max `addr uint mo`             | atomic
`amoswap.I`       | `raro`   | atomic swap `addr int mo`             | atomic
`cmpswap.I`       | `rcaro`  | compare swap `cnd addr int mo`        | atomic
`bswap.I`         | `rr`     | byte swap `int int`                   | bits
`ctz.I`           | `rr`     | count trailing zeros `int`            | bits
`clz.I`           | `rr`     | count leading zeros `int`             | bits
`popc.I`          | `rr`     | population count `int`                | bits
`brev.I`          | `rr`     | bit reverse `int`                     | bits
`ror.I`           | `rrr`    | rotate right `int reg`                | bits
`rol.I`           | `rrr`    | rotate left `int reg`                 | bits
`rori.I`          | `rri`    | rotate right `int imm`                | bits
`roli.I`          | `rri`    | rotate left `int imm`                 | bits
`bext.I`          | `rrii`   | bit extract `uint offset count`       | bits
`bdep.I`          | `rrii`   | bit deposit `uint offset count`       | bits
`pbext.I`         | `rrr`    | parallel bit extract `uint bits`      | bits
`pbdep.I`         | `rrr`    | parallel bit deposit `uint bits`      | bits
`sext.II`         | `rr`     | sign extend `int int`                 | bits
`zext.II`         | `rr`     | zero extend `uint uint`               | bits
`trunc.II`        | `rr`     | truncate `uint uint`                  | bits
`cvt.FI`          | `frd`    | convert int to float `int flt rm`     | fp-conv
`cvtu.FI`         | `frd`    | convert uint to float `uint flt rm`   | fp-conv
`cvt.IF`          | `rf`     | convert float to int `flt int`        | fp-conv
`cvtu.IF`         | `rf`     | convert float to uint `flt uint`      | fp-conv
`cvt.FF`          | `ffd`    | convert float to float `flt flt rm`   | fp-conv
`frac.IF`         | `rfd`    | float fraction `int flt rm`           | fp-conv
`exp.IF`          | `rfd`    | float exponent `int flt rm`           | fp-conv
`comp.FI`         | `frrd`   | float compose `mant exp flt`          | fp-conv
`fgetrm`          | `r`      | get fpu rounding mode                 | fp-control
`fgetex`          | `r`      | get fpu accrued exceptions            | fp-control
`fsetrm`          | `vr`     | set fpu rounding mode `int`           | fp-control
`fsetex`          | `vr`     | set fpu accrued exceptions `int`      | fp-control
`mv.F`            | `ff`     | move `flt flt`                        | fp-arith
`madd.F`          | `ffffd`  | fused mult add `flt flt flt rm`       | fp-arith
`msub.F`          | `ffffd`  | fused mult sub `flt flt flt rm`       | fp-arith
`mnadd.F`         | `ffffd`  | fused mult neg add `flt flt flt rm`   | fp-arith
`mnsub.F`         | `ffffd`  | fused mult neg sub `flt flt flt rm`   | fp-arith
`add.F`           | `fffd`   | add float `flt flt rm`                | fp-arith
`sub.F`           | `fffd`   | sub float `flt flt rm`                | fp-arith
`mul.F`           | `fffd`   | multiply float `flt flt rm`           | fp-arith
`div.F`           | `fffd`   | divide float `flt flt rm`             | fp-arith
`copysign.F`      | `fff`    | copysign float `flt flt`              | fp-arith
`copysign_xor.F`  | `fff`    | copysign xor float `flt flt`          | fp-arith
`copysign_not.F`  | `fff`    | copysign not float `flt flt`          | fp-arith
`min.F`           | `fff`    | minimum float `flt flt`               | fp-arith
`max.F`           | `fff`    | maximum float `flt flt`               | fp-arith
`sqrt.F`          | `ffd`    | square root float `flt rm`            | fp-arith
`rsqrt.F`         | `ffd`    | recip square root float `flt rm`      | fp-arith
`cmps.F`          | `rcff`   | compare and set float `cond flt flt`  | fp-pred
`select.F`        | `fffm`   | select (merge) float `flt flt mask`   | fp-pred
`class.F`         | `rf`     | classify `flt`                        | fp-pred
`ld.VI`           | `xaiom`  | load int `addr imm mo mask`           | vec-memory
`ldu.VI`          | `xaiom`  | load uint `addr imm mo mask`          | vec-memory
`ld.VF`           | `xaiom`  | load float `addr imm mo mask`         | vec-memory
`st.VI`           | `vaioxm` | store int `addr imm mo mask vec`      | vec-memory
`st.VF`           | `vaioxm` | store float `addr imm mo mask vec`    | vec-memory
`ld.VTI`          | `xtaom`  | load int `type addr mo mask`          | vec-memory
`ldu.VTI`         | `xtaom`  | load uint `type addr mo mask`         | vec-memory
`ld.VTF`          | `xtaom`  | load float `type addr mo mask`        | vec-memory
`st.VTI`          | `vtaoxm` | store int `type addr mo mask vec`     | vec-memory
`st.VTF`          | `vtaoxm` | store float `type addr mo mask vec`   | vec-memory
`gather.VII`      | `xaxom`  | gather load `addr ind mo mask`        | vec-memory
`gatheru.VII`     | `xaxom`  | gather load uint `addr ind mo mask`   | vec-memory
`gather.VIF`      | `xaxom`  | gather load float `addr ind mo mask`  | vec-memory
`scatter.VII`     | `vaxoxm` | scatter store int `addr ind mo mask`  | vec-memory
`scatteru.VII`    | `vaxoxm` | scatter store uint `addr ind mo mask` | vec-memory
`scatter.VIF`     | `vaxoxm` | scatter store float `addr ind mo mask`| vec-memory
`mv.x.x.VI`       | `xx`     | move vec to vec `vec vec`             | vec-arith
`mv.x.r.VI`       | `xr`     | move int to vec `vec int`             | vec-arith
`mv.r.x.VI`       | `rx`     | move vec to int `int vec`             | vec-arith
`splati.VI`       | `xim`    | splat (broadcast) `int imm mask`      | vec-arith
`splatui.VI`      | `xim`    | splat (broadcast) `uint imm mask`     | vec-arith
`splat.VI`        | `xrm`    | splat (broadcast) `int reg mask`      | vec-arith
`add.VI`          | `xxxm`   | add int `vec vec mask`                | vec-arith
`addc.VI`         | `xxxxm`  | add carry int `3*vec mask`            | vec-arith
`sub.VI`          | `xxxm`   | sub int `vec vec mask`                | vec-arith
`subb.VI`         | `xxxxm`  | sub borrow int `3*vec mask`           | vec-arith
`addu.VI`         | `xxxm`   | add uint `vec vec mask`               | vec-arith
`addcu.VI`        | `xxxxm`  | add carry uint `3*vec mask`           | vec-arith
`subu.VI`         | `xxxm`   | sub uint  `vec vec mask`              | vec-arith
`subbu.VI`        | `xxxxm`  | sub borrow uint `3*vec mask`          | vec-arith
`and.VI`          | `xxxm`   | logical and int `vec vec mask`        | vec-arith
`nand.VI`         | `xxxm`   | logical not and int `vec vec mask`    | vec-arith
`andc.VI`         | `xxxm`   | logical and comp int `vec vec mask`   | vec-arith
`or.VI`           | `xxxm`   | logical or int `vec vec mask`         | vec-arith
`nor.VI`          | `xxxm`   | logical not or int `vec vec mask`     | vec-arith
`orc.VI`          | `xxxm`   | logical or comp int `vec vec mask`    | vec-arith
`xor.VI`          | `xxxm`   | logical xor int `vec vec mask`        | vec-arith
`xnor.VI`         | `xxxm`   | logical not xor int `vec vec mask`    | vec-arith
`neg.VI`          | `xxm`    | negate int `vec mask`                 | vec-arith
`not.VI`          | `xxm`    | complement int `vec mask`             | vec-arith
`min.VI`          | `xxxm`   | minimum int `vec vec mask`            | vec-arith
`max.VI`          | `xxxm`   | maximum int `vec vec mask`            | vec-arith
`minu.VI`         | `xxxm`   | minimum uint `vec vec mask`           | vec-arith
`maxu.VI`         | `xxxm`   | maximum uint `vec vec mask`           | vec-arith
`mul.VI`          | `xxxm`   | multiply int `vec vec mask`           | vec-arith
`mul.VID`         | `xxxm`   | multiply wide int `vec vec mask`      | vec-arith
`mulu.VI`         | `xxxm`   | multiply uint `vec vec mask`          | vec-arith
`mulu.VID`        | `xxxm`   | multiply wide uint `vec vec mask`     | vec-arith
`mulh.VI`         | `xxxm`   | multiply high int `vec vec mask`      | vec-arith
`mulhu.VI`        | `xxxm`   | multiply high uint `vec vec mask`     | vec-arith
`div.VI`          | `xxxm`   | divide int `vec vec mask`             | vec-arith
`rem.VI`          | `xxxm`   | remainder int `vec vec mask`          | vec-arith
`divu.VI`         | `xxxm`   | divide uint `vec vec mask`            | vec-arith
`remu.VI`         | `xxxm`   | remainder uint `vec vec mask`         | vec-arith
`rdiv.mult.VI`    | `xxrr`   | reciprocal divide mult `vec int int`  | vec-arith
`rdivu.mult.VI`   | `xxrr`   | reciprocal divide mult `vec uint uint`| vec-arith
`srl.VI`          | `xxrm`   | shift right logical int `vec reg mask`| vec-shift
`sra.VI`          | `xxrm`   | shift right arith int `vec reg mask`  | vec-shift
`sll.VI`          | `xxrm`   | shift left logical int `vec reg mask` | vec-shift
`srli.VI`         | `xxim`   | shift right logical int `vec imm mask`| vec-shift
`srai.VI`         | `xxim`   | shift right arithint `vec imm mask`   | vec-shift
`slli.VI`         | `xxim`   | shift left logical uint `vec imm mask`| vec-shift
`srlx.VI`         | `xxxm`   | shift right logical int `vec vec mask`| vec-shift
`srax.VI`         | `xxxm`   | shift right arith int `vec vec mask`  | vec-shift
`sllx.VI`         | `xxxm`   | shift left logical uint `vec vec mask`| vec-shift
`fsrl.VI`         | `xxxrm`  | funnel shift right logical `vec int`  | vec-shift
`fsra.VI`         | `xxxrm`  | funnel shift right arith `vec int`    | vec-shift
`fsll.VI`         | `xxxrm`  | funnel shift left logical `vec int`   | vec-shift
`fsrai.VI`        | `xxxim`  | funnel shift right logical `vec imm`  | vec-shift
`fsrli.VI`        | `xxxim`  | funnel shift right arith `vec imm`    | vec-shift
`fslli.VI`        | `xxxim`  | funnel shift left logical `vec imm`   | vec-shift
`fsrax.VI`        | `xxxxm`  | funnel shift right logical `vec vec`  | vec-shift
`fsrlx.VI`        | `xxxxm`  | funnel shift right arith `vec vec`    | vec-shift
`fsllx.VI`        | `xxxxm`  | funnel shift left logical `vec vec`   | vec-shift
`cmps.VI`         | `mcxxm`  | compare and set int `cnd vec vec mask`| vec-pred
`select.VI`       | `xxxm`   | select (merge) int `vec vec mask`     | vec-pred
`bswap.VI`        | `xxm`    | byte swap int `vec mask`              | vec-bits
`ctz.VI`          | `xxm`    | count trailing zeros int `vec mask`   | vec-bits
`clz.VI`          | `xxm`    | count leading zeros int `vec mask`    | vec-bits
`popc.VI`         | `xxm`    | population count int `vec mask`       | vec-bits
`brev.VI`         | `xxm`    | bit reverse int `vec mask`            | vec-bits
`ror.VI`          | `xxrm`   | rotate right int reg `vec reg mask`   | vec-bits
`rol.VI`          | `xxrm`   | rotate left int reg `vec reg mask`    | vec-bits
`rori.VI`         | `xxim`   | rotate right int imm `vec imm mask`   | vec-bits
`roli.VI`         | `xxim`   | rotate left int imm `vec imm mask`    | vec-bits
`rorv.VI`         | `xxxm`   | rotate right int vec `vec vec mask`   | vec-bits
`rolv.VI`         | `xxxm`   | rotate left int vec `vec vec mask`    | vec-bits
`bext.VI`         | `xxiim`  | bit extract uint `vec off cnt mask`   | vec-bits
`bdep.VI`         | `xxiim`  | bit deposit uint `vec off cnt mask`   | vec-bits
`pbext.VI`        | `xxxm`   | parallel bit extract `vec bits mask`  | vec-bits
`pbdep.VI`        | `xxxm`   | parallel bit deposit `vec bits mask`  | vec-bits
`permute_16x4.VI` | `xxrm`   | permute uint `vec nibble-ind mask`    | vec-horiz
`permute_8x8.VI`  | `xxrm`   | permute uint `vec byte-ind mask`      | vec-horiz
`permute.VII`     | `xxxm`   | permute uint `vec ind mask`           | vec-horiz
`sext.VII`        | `xxm`    | sign extend int to int  `vec mask`    | vec-horiz
`zext.VII`        | `xxm`    | zero extend uint to uint `vec mask`   | vec-horiz
`trunc.VII`       | `xxm`    | truncate uint `vec mask`              | vec-horiz
`lsr.VI`          | `xxx`    | lane shift right uint `vec vec`       | vec-horiz
`lsl.VI`          | `xxx`    | lane shift left uint `vec vec`        | vec-horiz
`lror.VI`         | `xxx`    | lane rotate right uint `vec vec`      | vec-horiz
`ltor.VI`         | `xxx`    | lane rotate left uint `vec vec`       | vec-horiz
`lzip01.VID`      | `xxx`    | lane zip mod 2 lane 0,1 uint `vec vec`| vec-horiz
`lzip01.VIQ`      | `xxx`    | lane zip mod 4 lane 0,1 uint `vec vec`| vec-horiz
`lzip23.VIQ`      | `xxx`    | lane zip mod 4 lane 2,3 uint `vec vec`| vec-horiz
`lunzip0.VI2`     | `xxx`    | lane unzip mod 2 lane 0 uint `vec vec`| vec-horiz
`lunzip1.VI2`     | `xxx`    | lane unzip mod 2 lane 1 uint `vec vec`| vec-horiz
`lunzip0.VI4`     | `xxx`    | lane unzip mod 4 lane 0 uint `vec vec`| vec-horiz
`lunzip1.VI4`     | `xxx`    | lane unzip mod 4 lane 1 uint `vec vec`| vec-horiz
`lunzip2.VI4`     | `xxx`    | lane unzip mod 4 lane 2 uint `vec vec`| vec-horiz
`lunzip3.VI4`     | `xxx`    | lane unzip mod 4 lane 3 uint `vec vec`| vec-horiz
`pair.swap.VI`    | `xxm`    | pair swap uint `vec mask`             | vec-horiz
`pair.add.VI2`    | `xxm`    | pair add reduce int `vec mask`        | vec-horiz
`pair.addu.VI2`   | `xxm`    | pair add reduce uint `vec mask`       | vec-horiz
`pair.sub.VI2`    | `xxm`    | pair sub reduce int `vec mask`        | vec-horiz
`pair.subu.VI2`   | `xxm`    | pair sub reduce uint `vec mask`       | vec-horiz
`cumsum.VI`       | `xxm`    | cumulative sum int `vec mask`         | vec-horiz
`cumsumu.VI`      | `xxm`    | cumulative sum uint `vec mask`        | vec-horiz
`mv.x.f.VF`       | `xf`     | move float to vec `vec flt`           | vec-fp-conv
`mv.f.x.VF`       | `fx`     | move vec to float `flt vec`           | vec-fp-conv
`splat.VF`        | `xfm`    | splat (broadcast) float `vec flt mask`| vec-fp-conv
`cvt.VFI`         | `xxdm`   | convert int to float `vec rm mask`    | vec-fp-conv
`cvtu.VFI`        | `xxdm`   | convert uint to float `vec rm mask`   | vec-fp-conv
`cvt.VIF`         | `xxm`    | convert float to int `vec mask`       | vec-fp-conv
`cvtu.VIF`        | `xxm`    | convert float to uint `vec mask`      | vec-fp-conv
`cvt.VFF`         | `xxdm`   | convert float to float `vec rm mask`  | vec-fp-conv
`frac.VIF`        | `xxdm`   | float fraction int `vec rm mask`      | vec-fp-conv
`exp.VIF`         | `xxdm`   | float exponent int `vec rm mask`      | vec-fp-conv
`comp.VFI`        | `xxxdm`  | float compose `mant exp flt`          | vec-fp-conv
`madd.VF`         | `xxxxdm` | fused mult add `3*vec rm mask`        | vec-fp-arith
`msub.VF`         | `xxxxdm` | fused mult sub `3*vec rm mask`        | vec-fp-arith
`mnadd.VF`        | `xxxxdm` | fused mult neg add `3*vec rm mask`    | vec-fp-arith
`mnsub.VF`        | `xxxxdm` | fused mult neg sub `3*vec rm mask`    | vec-fp-arith
`add.VF`          | `xxxdm`  | add float `vec vec rm mask`           | vec-fp-arith
`sub.VF`          | `xxxdm`  | sub float `vec vec rm mask`           | vec-fp-arith
`mul.VFD`         | `xxxdm`  | multiply float `vec vec rm mask`      | vec-fp-arith
`div.VF`          | `xxxdm`  | divide float `vec vec rm mask`        | vec-fp-arith
`copysign.VF`     | `xxxm`   | copysign float `vec vec mask`         | vec-fp-arith
`copysign_xor.VF` | `xxxm`   | copysign xor float `vec vec mask`     | vec-fp-arith
`copysign_not.VF` | `xxxm`   | copysign not float `vec vec mask`     | vec-fp-arith
`min.VF`          | `xxxm`   | minimum float `vec vec mask`          | vec-fp-arith
`max.VF`          | `xxxm`   | maximum float `vec vec mask`          | vec-fp-arith
`sqrt.VF`         | `xxdm`   | square root float `vec rm mask`       | vec-fp-arith
`rsqrt.VF`        | `xxdm`   | recip square root float `vec rm mask` | vec-fp-arith
`cmps.VIF`        | `xcxxm`  | compare and set flt `cnd vec vec mask`| vec-fp-pred
`select.VIF`      | `xxxm`   | select float `vec vec mask`           | vec-fp-pred
`class.VIF`       | `xxm`    | classify float `vec mask`             | vec-fp-pred
`pair.add.VF2`    | `xxm`    | pair add reduce float `vec mask`      | vec-fp-horiz
`pair.sub.VF2`    | `xxm`    | pair sub reduce int `vec mask`        | vec-fp-horiz
`cumsum.VF`       | `xxm`    | cumulative sum float `vec mask`       | vec-fp-horiz

### Operation Statistics

category        | count
--------------- | -----
types           | 18
data            | 9
constant        | 5
system          | 3
branch-unsafe   | 3
branch-safe     | 6
memory-unsafe   | 30
memory-safe     | 20
thread          | 0
arith           | 41
shift           | 12
pred            | 2
atomic          | 11
bits            | 14
fp-conv         | 8
fp-control      | 4
fp-arith        | 15
fp-pred         | 3
vec-memory      | 16
vec-arith       | 40
vec-shift       | 18
vec-pred        | 2
vec-bits        | 13
vec-horiz       | 26
vec-fp-conv     | 11
vec-fp-arith    | 14
vec-fp-pred     | 3
vec-fp-horiz    | 3
--------------- | -----
total           | 350