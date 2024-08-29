CC=g++
CFLAGS=-I.
SHX=chmod +x

VPATH = src

DIRS= star mincode converge
binaries= ajusteh star/starmaker mincode/cutoff converge/counter converge/plotting/finder converge/plotting/mfinder

all: ajusteh $(DIRS) tools

.PHONY: clean
clean:
	rm -f $(binaries)

ajusteh: new_ajusteh.cpp
	$(CC) -o $@ $^

star/starmaker: starmaker_noweight.cpp
	$(CC) -o $@ $^

mincode/cutoff: cutoff.cpp
	$(CC) -o $@ $^

converge/counter: count.cpp
	$(CC) -o $@ $^
converge/plotting/finder: converge/plotting/finder.cpp
	$(CC) -o $@ $^
converge/plotting/mfinder: converge/plotting/mfinder.cpp
	$(CC) -o $@ $^


.PHONY: star
star: star/starmaker
	$(SHX) $@/dothing
	$(SHX) $@/K2/run
	$(SHX) $@/run

.PHONY: mincode
mincode: mincode/cutoff
	$(SHX) $@/clean

.PHONY: converge
converge: converge/counter converge/plotting/finder converge/plotting/mfinder
	$(SHX) $@/run
	$(SHX) $@/clean

.PHONY: compare_clust
compare_clust:
	$(SHX) $@/clean
	$(SHX) $@/get_csv
	$(SHX) $@/run
	$(SHX) $@/curlcommand

.PHONY: compare_K2
compare_K2:
	$(SHX) $@/clean
	$(SHX) $@/run
	$(SHX) $@/curlcommand

.PHONY: tools
tools:
	$(SHX) clean
	$(SHX) getcalc
	#$(SHX) make_outputs
	$(SHX) runfinish
	$(SHX) runorig_k2
