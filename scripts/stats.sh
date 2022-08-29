#!/bin/bash

prefixes="types|data|constant|system|thread|branch|memory|thread|arith|shift|pred|atomic|bits|fp-|vec-"
categories="types data constant system thread branch-unsafe branch-safe memory-unsafe memory-safe thread arith shift \
	pred atomic bits fp-conv fp-control fp-arith fp-pred \
	vec-memory vec-arith vec-shift vec-pred vec-bits vec-horiz \
	vec-fp-conv vec-fp-arith vec-fp-pred vec-fp-horiz"

printf "%-16s| %s\n" "category" "count"
printf "%-16s| %s\n" "---------------" "-----"
for category in ${categories} ; do
	count=$(egrep "\\| ${category}$" spec/llvlir.md | wc -l | sed 's# ##g')
	printf "%-16s| %s\n" ${category} ${count}
done
total=$(egrep "\| (${prefixes})" spec/llvlir.md | wc -l | sed 's# ##g')
printf "%-16s| %s\n" "---------------" "-----"
printf "%-16s| %s\n" "total" ${total}
