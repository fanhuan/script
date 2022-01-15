#include "file_reader.h"
#include "hashset.h"

typedef struct {
	uint64_t kmer:50, count:14;
	uint32_t off;
	uint32_t idx;
} kmer_t;

#define MAX_COUNT 0x3FFFU

static inline uint64_t __lh3_Jenkins_hash_64(uint64_t key){
	key += ~(key << 32);
	key ^= (key >> 22);
	key += ~(key << 13);
	key ^= (key >> 8);
	key += (key << 3);
	key ^= (key >> 15);
	key += ~(key << 27);
	key ^= (key >> 31);
	return key;
}

#define kmer_hashcode(k1) __lh3_Jenkins_hash_64((k1).kmer)
#define kmer_equals(k1, k2) ((k1).kmer == (k2).kmer)
define_hashset(kmerhash, kmer_t, kmer_hashcode, kmer_equals);

static const char bit_base_table[6] = "ACGTN-";

static int seq_type = 1;

static const uint8_t base_bit_table[256] = {
	4, 4, 4, 4,  4, 4, 4, 4,  4, 4, 4, 4,  4, 4, 4, 4,
	4, 4, 4, 4,  4, 4, 4, 4,  4, 4, 4, 4,  4, 4, 4, 4,
	4, 4, 4, 4,  4, 4, 4, 4,  4, 4, 4, 4,  4, 4, 4, 4,
	4, 4, 4, 4,  4, 4, 4, 4,  4, 4, 4, 4,  4, 4, 4, 4,

	4, 0, 4, 1,  4, 4, 4, 2,  4, 4, 4, 4,  4, 4, 4, 4,
	4, 4, 4, 4,  3, 4, 4, 4,  4, 4, 4, 4,  4, 4, 4, 4,
	4, 0, 4, 1,  4, 4, 4, 2,  4, 4, 4, 4,  4, 4, 4, 4,
	4, 4, 4, 4,  3, 4, 4, 4,  4, 4, 4, 4,  4, 4, 4, 4,

	4, 4, 4, 4,  4, 4, 4, 4,  4, 4, 4, 4,  4, 4, 4, 4,
	4, 4, 4, 4,  4, 4, 4, 4,  4, 4, 4, 4,  4, 4, 4, 4,
	4, 4, 4, 4,  4, 4, 4, 4,  4, 4, 4, 4,  4, 4, 4, 4,
	4, 4, 4, 4,  4, 4, 4, 4,  4, 4, 4, 4,  4, 4, 4, 4,

	4, 4, 4, 4,  4, 4, 4, 4,  4, 4, 4, 4,  4, 4, 4, 4,
	4, 4, 4, 4,  4, 4, 4, 4,  4, 4, 4, 4,  4, 4, 4, 4,
	4, 4, 4, 4,  4, 4, 4, 4,  4, 4, 4, 4,  4, 4, 4, 4,
	4, 4, 4, 4,  4, 4, 4, 4,  4, 4, 4, 4,  4, 4, 4, 4
};

static const char comp_base_table[256] = {
	'N', 'N', 'N', 'N',  'N', 'N', 'N', 'N',  'N', 'N', 'N', 'N',  'N', 'N', 'N', 'N',
	'N', 'N', 'N', 'N',  'N', 'N', 'N', 'N',  'N', 'N', 'N', 'N',  'N', 'N', 'N', 'N',
	'N', 'N', 'N', 'N',  'N', 'N', 'N', 'N',  'N', 'N', 'N', 'N',  'N', 'N', 'N', 'N',
	'N', 'N', 'N', 'N',  'N', 'N', 'N', 'N',  'N', 'N', 'N', 'N',  'N', 'N', 'N', 'N',

	'N', 'T', 'N', 'G',  'N', 'N', 'N', 'C',  'N', 'N', 'N', 'N',  'N', 'N', 'N', 'N',
	'N', 'N', 'N', 'N',  'A', 'N', 'N', 'N',  'N', 'N', 'N', 'N',  'N', 'N', 'N', 'N',
	'N', 'T', 'N', 'G',  'N', 'N', 'N', 'C',  'N', 'N', 'N', 'N',  'N', 'N', 'N', 'N',
	'N', 'N', 'N', 'N',  'A', 'N', 'N', 'N',  'N', 'N', 'N', 'N',  'N', 'N', 'N', 'N',

	'N', 'N', 'N', 'N',  'N', 'N', 'N', 'N',  'N', 'N', 'N', 'N',  'N', 'N', 'N', 'N',
	'N', 'N', 'N', 'N',  'N', 'N', 'N', 'N',  'N', 'N', 'N', 'N',  'N', 'N', 'N', 'N',
	'N', 'N', 'N', 'N',  'N', 'N', 'N', 'N',  'N', 'N', 'N', 'N',  'N', 'N', 'N', 'N',
	'N', 'N', 'N', 'N',  'N', 'N', 'N', 'N',  'N', 'N', 'N', 'N',  'N', 'N', 'N', 'N',

	'N', 'N', 'N', 'N',  'N', 'N', 'N', 'N',  'N', 'N', 'N', 'N',  'N', 'N', 'N', 'N',
	'N', 'N', 'N', 'N',  'N', 'N', 'N', 'N',  'N', 'N', 'N', 'N',  'N', 'N', 'N', 'N',
	'N', 'N', 'N', 'N',  'N', 'N', 'N', 'N',  'N', 'N', 'N', 'N',  'N', 'N', 'N', 'N',
	'N', 'N', 'N', 'N',  'N', 'N', 'N', 'N',  'N', 'N', 'N', 'N',  'N', 'N', 'N', 'N'
};

uint32_t load_next_kmer_table(FileReader *fr, Vector *kmers, kmerhash *hash, uint8_t kmer_size, uint64_t n_limit, uint64_t k_range[2]){
	kmer_t MER, *mer;
	uint32_t i, count;
	uint64_t n, n_k, kmer;
	int exists;
	char *seq;
	n = n_k = 0;
	fprintf(stderr, "Try loading kmers\n");
	fflush(stderr);
	while(fread_table(fr) != -1){
		seq   = get_col_str(fr, 0);
		count = atoi(get_col_str(fr, 1));
		kmer = 0;
		for(i=0;i<kmer_size;i++) kmer = (kmer << 2) | base_bit_table[(int)seq[i]];
		gpush_vec(kmers, kmer, uint64_t);
		MER.kmer = kmer;
		MER.off = MER.idx = MER.count = 0;
		mer = prepare_kmerhash(hash, MER, &exists);
		mer->kmer  = kmer;
		mer->count = count;
		mer->off   = n;
		mer->idx   = n;
		if(n == 0) k_range[0] = kmer;
		else k_range[1] = kmer;
		n += count;
		n_k ++;
		if(n >= n_limit) break;
	}
	fprintf(stderr, "Loaded %llu kmers\n", (unsigned long long)n_k);
	fflush(stderr);
	return n;
}

void sort_kmer_reads(uint32_t *array, uint8_t *offs, kmerhash *hash, int kmer_size, uint64_t k_range[2], char *rds_file){
	FileReader *fr;
	Sequence *seq;
	kmer_t MER, *mer;
	int i;
	uint32_t j, n, rid;
	uint64_t kmer, kmer_mask;
	kmer_mask = (1LLU << (kmer_size << 1)) - 1;
	n = 0;
	if((fr = fopen_filereader(rds_file)) == NULL){
		fprintf(stderr, " -- Cannot open %s in %s -- %s:%d --\n", rds_file, __FUNCTION__, __FILE__, __LINE__);
		abort();
	}
	seq = NULL;
	MER.off = MER.idx = MER.count = 0;
	rid = 0;
	while((seq_type==1)? (fread_fasta_adv(&seq, fr, FASTA_FLAG_NO_NAME)) : (fread_fastq_adv(&seq, fr, FASTQ_FLAG_NO_NAME | FASTQ_FLAG_NO_QUAL))){
		n ++;
		kmer = 0;
		for(i=0;i<kmer_size-1;i++) kmer = (kmer << 2) | (base_bit_table[(int)seq->seq.string[i]] & 0x03);
		for(;i<seq->seq.size;i++){
			kmer = ((kmer << 2) | base_bit_table[(int)seq->seq.string[i]]) & kmer_mask;
			if(kmer < k_range[0] || kmer > k_range[1]) continue;
			MER.kmer = kmer;
			mer = get_kmerhash(hash, MER);
			if(mer == NULL || mer->idx == mer->off + mer->count) continue;
			offs[mer->idx]  = i - kmer_size + 1;
			array[mer->idx] = rid;
			mer->idx ++;
		}

		reverse_string(&(seq->seq));
		for(j=0;j<(uint32_t)seq->seq.size;j++) seq->seq.string[j] = comp_base_table[(int)seq->seq.string[j]];

		kmer = 0;
		for(i=0;i<kmer_size-1;i++) kmer = (kmer << 2) | (base_bit_table[(int)seq->seq.string[i]] & 0x03);
		for(;i<seq->seq.size;i++){
			kmer = ((kmer << 2) | base_bit_table[(int)seq->seq.string[i]]) & kmer_mask;
			if(kmer < k_range[0] || kmer > k_range[1]) continue;
			MER.kmer = kmer;
			mer = get_kmerhash(hash, MER);
			if(mer == NULL || mer->idx == mer->off + mer->count) continue;
			offs[mer->idx]  = (i - kmer_size + 1) | 0x80U;
			array[mer->idx] = rid;
			mer->idx ++;
		}
		rid ++;
	}
	fclose_filereader(fr);
	fprintf(stderr, "Scan %u reads\n", n);
	fflush(stderr);
}

void cluster_reads_by_kmer(char *rds_file, char *kmer_file, uint64_t max_mem, FILE *out){
	FileReader *fr, *fr2;
	Vector *kmers;
	uint32_t *array;
	uint8_t *offs;
	kmerhash *hash;
	kmer_t MER, *mer;
	SeqFileAttr attr;
	uint32_t i, j, c, kmer_size;
	uint64_t k, k_range[2], n_limit;
	if((fr = fopen_filereader(kmer_file)) == NULL){
		fprintf(stderr, " -- Cannot open %s in %s -- %s:%d --\n", kmer_file, __FUNCTION__, __FILE__, __LINE__);
		abort();
	}
	if(fread_table(fr) < 2){
		fprintf(stdout, " -- Bad file %s in %s -- %s:%d --\n", kmer_file, __FUNCTION__, __FILE__, __LINE__);
		abort();
	}
	kmer_size = get_col_len(fr, 0);
	fclose_filereader(fr);
	fr = fopen_filereader(kmer_file);
	if((fr2 = fopen_filereader(rds_file)) == NULL){
		fprintf(stderr, " -- Cannot open %s in %s -- %s:%d --\n", rds_file, __FUNCTION__, __FILE__, __LINE__);
		abort();
	}
	guess_seq_file(fr2, &attr);
	seq_type = !attr.is_fq;
	//rd_len = attr.max_seq_len;
	fclose_filereader(fr2);
	n_limit = ((uint64_t)max_mem) / 4;
	hash = init_kmerhash(1024*1024);
	kmers = init_vec(sizeof(uint64_t), 1024);
	array = (uint32_t*)malloc((n_limit + MAX_COUNT) * sizeof(uint32_t));
	offs  = (uint8_t*)malloc(n_limit + MAX_COUNT);
	MER.off = MER.idx = MER.count = 0;
	while(load_next_kmer_table(fr, kmers, hash, kmer_size, n_limit, k_range)){
		sort_kmer_reads(array, offs, hash, kmer_size, k_range, rds_file);
		for(i=0;i<vec_size(kmers);i++){
			k = gget_vec(kmers, i, uint64_t);
			MER.kmer = k;
			mer = get_kmerhash(hash, MER);
			c = mer->idx - mer->off;
			for(j=0;j<kmer_size;j++){
				fprintf(out, "%c", bit_base_table[((k >> ((kmer_size - j - 1) << 1)) & 0x03)]);
			}
			fprintf(out, "\t%u\t", (unsigned)c);
			for(j=0;j<c;j++){
				fprintf(out, "%u:%c%u,", array[mer->off + j], "+-"[offs[mer->off + j]>>7], offs[mer->off + j]&0x7FU);
			}
			fprintf(out, "\n");
		}
		clear_vec(kmers);
		clear_kmerhash(hash);
	}
	free_vec(kmers);
	free(array);
	free(offs);
	free_kmerhash(hash);
	fclose_filereader(fr);
}

int usage(char *prog){
	printf("Usage: %s <kmer_file> <reads_file(fa|fq)> [max_memory(Mb)]\n", prog);
	return 1;
}

int main(int argc, char **argv){
	char *rds_file, *kmer_file;
	uint64_t max_mem;
	if(argc < 3) return usage(argv[0]);
	kmer_file = argv[1];
	rds_file  = argv[2];
	if(argc > 3) max_mem = 1024 * 1024 * atoi(argv[3]);
	else max_mem = ((uint64_t)3) * 1024 * 1024 * 1024 / 2;
	if(max_mem < 64 * 1024 * 1024) max_mem = 64 * 1024 * 1024;
	cluster_reads_by_kmer(rds_file, kmer_file, max_mem, stdout);
	return 0;
}

