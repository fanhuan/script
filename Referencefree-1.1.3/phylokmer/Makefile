CC=gcc
CFLAGS=-g -W -Wall -O2 -D_FILE_OFFSET_BITS=64
GLIBS=-lm
GENERIC_SRC=string.h vector.h file_reader.h hashset.h

all: kmer_count kmer_countx kmer_cluster kmer_cluster_id filter

kmer_count: $(GENERIC_SRC) file_reader.c kmer_count.c
	$(CC) $(CFLAGS) -o kmer_count file_reader.c kmer_count.c $(GLIBS)

kmer_countx: $(GENERIC_SRC) file_reader.c kmer_countx.c
	$(CC) $(CFLAGS) -o kmer_countx file_reader.c kmer_countx.c $(GLIBS)

kmer_cluster: $(GENERIC_SRC) file_reader.c kmer_cluster.c
	$(CC) $(CFLAGS) -o kmer_cluster file_reader.c kmer_cluster.c $(GLIBS)

kmer_cluster_id: $(GENERIC_SRC) file_reader.c kmer_cluster2.c
	$(CC) $(CFLAGS) -o kmer_cluster_id file_reader.c kmer_cluster2.c $(GLIBS)

filter: $(GENERIC_SRC) file_reader.c filter.c
	$(CC) $(CFLAGS) -o filter file_reader.c filter.c $(GLIBS)

clean:
	rm -f *.o *.gcda *.gcno *.gcov gmon.out kmer_count kmer_countx kmer_cluster kmer_cluster_id filter

clear:
	rm -f *.o *.gcda *.gcno *.gcov gmon.out
