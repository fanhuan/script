#include <iostream>
#include <string>
#include <stdint.h>
#include <string.h>
#include <stdio.h>
#include <vector>
#include <map>
#include <fstream>
#include "stdlib.h"
#include "memory.h"
using namespace std;
const size_t Max_Kmer_Size=100;



const size_t min_ht_sz=10000000;
//const uint64_t HashTableSZ=100000000;




struct hashtable
{
bool *idx;
uint64_t *store_pos;
};

struct bucket
{
	uint64_t *key;
	int *key_cnt;
};









uint64_t MurmurHash64A ( const void * key, int len, unsigned int seed )
{
	const uint64_t m = 0xc6a4a7935bd1e995;
	const int r = 47;

	uint64_t h = seed ^ (len * m);

	const uint64_t * data = (const uint64_t *)key;
	const uint64_t * end = data + (len/8);

	while(data != end)
	{
		uint64_t k = *data++;

		k *= m; 
		k ^= k >> r; 
		k *= m; 
		
		h ^= k;
		h *= m; 
	}

	const unsigned char * data2 = (const unsigned char*)data;

	switch(len & 7)
	{
	case 7: h ^= uint64_t(data2[6]) << 48;
	case 6: h ^= uint64_t(data2[5]) << 40;
	case 5: h ^= uint64_t(data2[4]) << 32;
	case 4: h ^= uint64_t(data2[3]) << 24;
	case 3: h ^= uint64_t(data2[2]) << 16;
	case 2: h ^= uint64_t(data2[1]) << 8;
	case 1: h ^= uint64_t(data2[0]);
	        h *= m;
	};
 
	h ^= h >> r;
	h *= m;
	h ^= h >> r;

	return h;
} 






static inline uint64_t str2bits(const char * c_str,int len)
{
	uint64_t b_str=0;
	for (int k=0;k<len;k++)
	{
		switch(c_str[k])
		{
		case ('A'):
			b_str<<=2;
			break;
		case '0':
			b_str<<=2;//cout<<0<<endl;
			break;
			
		case ('C'):
			++(b_str<<=2);
			break;
		case '1':
			++(b_str<<=2);//cout<<1<<endl;
			break;

		case 'G':
			(++(b_str<<=1))<<=1;
			break;
		case '2':
			(++(b_str<<=1))<<=1;//cout<<2<<endl;
			break;
		case 'T':
			++((++(b_str<<=1))<<=1);
			break;
		case '3':
			++((++(b_str<<=1))<<=1);//cout<<3<<endl;
			break;
		}
	//	cout<<b_str<<endl;
	}
	return b_str;
}




static inline uint64_t get_rev_comp_seq(uint64_t seq, int seq_size)
{
	seq =~seq;
	
	seq = ((seq & 0x3333333333333333 )<< 2) | ((seq & 0xCCCCCCCCCCCCCCCC )>> 2);
	seq = ((seq & 0x0F0F0F0F0F0F0F0F )<< 4) | ((seq & 0xF0F0F0F0F0F0F0F0 )>> 4);
	seq = ((seq & 0x00FF00FF00FF00FF )<< 8) | ((seq & 0xFF00FF00FF00FF00 )>> 8);
	seq = ((seq & 0x0000FFFF0000FFFF )<<16) | ((seq & 0xFFFF0000FFFF0000 )>>16);
	seq = ((seq & 0x00000000FFFFFFFF )<<32) | ((seq & 0xFFFFFFFF00000000 )>>32);
	 
	return seq >> (64 - (seq_size*2));
}


void batch_hash_insertion(uint64_t *Kmer_bits,struct hashtable ht,struct bucket bkt ,size_t height,int len,size_t *curcnt,uint64_t hashTableSZ)
{
	uint64_t seq,f_seq;
	size_t pos;
	for (size_t i=0;i<height;++i)
	{
		seq=Kmer_bits[i];
		f_seq=get_rev_comp_seq(seq,len);
		uint64_t hv,f_hv;
		hv=MurmurHash64A(&seq,sizeof(seq),0);
		f_hv=MurmurHash64A(&f_seq,sizeof(seq),0);
		hv=hv^f_hv;
		
		bool leaveLoopIns = false; 
		while (!leaveLoopIns) 
		{
			uint64_t hash_idx=(hv)%hashTableSZ;
			if (ht.idx[hash_idx]==0)
			{

				ht.idx[hash_idx]=1;

				 pos=(*curcnt)++;
					
	 
				ht.store_pos[hash_idx]=pos;
				bkt.key[pos]=seq;
			}
			else
			{
			
				bool flag2=0;

				pos=(size_t) ht.store_pos[hash_idx];
				if(bkt.key[pos]!=seq&&bkt.key[pos]!=f_seq)
				{flag2=1;}



				if(flag2!=0)
				{
				


					hv=hv+1;
				
					continue;
				}
						

			}
			leaveLoopIns = true; 
		}

	
	}

}







bool hash_lookup(uint64_t Kmer_bits,struct hashtable ht,struct bucket bkt,int len,uint64_t hashTableSZ)
{
	uint64_t seq,f_seq;
	size_t pos;
	
	seq=Kmer_bits;
	f_seq=get_rev_comp_seq(seq,len);
	uint64_t hv,f_hv;
	hv=MurmurHash64A(&seq,sizeof(seq),0);
	f_hv=MurmurHash64A(&f_seq,sizeof(seq),0);
	hv=hv^f_hv;
	
	bool leaveLoopFnd = false; 
	while (!leaveLoopFnd) 
	{
		uint64_t hash_idx=(hv)%hashTableSZ;
		if (ht.idx[hash_idx]==0)
		{
			return 0;
		}
		else
		{
		
			bool flag2=0;

			pos=(size_t) ht.store_pos[hash_idx];
			if(bkt.key[pos]!=seq&&bkt.key[pos]!=f_seq)
			{flag2=1;}

			

			if(flag2!=0)
			{
			

				hv=hv+1;
			
				continue;
			}
			else
			{
				return 1;
			}
					

		}
		leaveLoopFnd = true; 
	}

	
	return 1;

}






int main(int argc, char* argv[])
{

	cout<<"Command:"<<endl;
	cout<<"ProgramFile -k INPUT_FILE1 -o OUTPUT_FILENAME -s SINGLE_END_FILE_INPUT -s1 QUERY_PAIR1 -s2 QUERY_PAIR2 -fa CONVERT_FQ2FA"<<endl;
	cout<<"add -fa 1 if you want to convert fq into fa."<<endl;
//
	bool FA=0;
	string inputs;
	vector<string> in_filenames,search_filenames1,search_filenames2,search_filenames;
	string dirc,out_filename;
	for(int i=1;i<argc;++i)
	{
		
		if(strcmp(argv[i],"-k")==0)
		{
			i++;
			in_filenames.push_back(argv[i]);
			continue;
		}
		if(strcmp(argv[i],"-o")==0)
		{
			i++;
			out_filename=argv[i];

		}
		if(strcmp(argv[i],"-s1")==0)
		{
			i++;
			search_filenames1.push_back(argv[i]);
			
		}
		if(strcmp(argv[i],"-s2")==0)
		{
			i++;
			search_filenames2.push_back(argv[i]);
			
		}
		if(strcmp(argv[i],"-s")==0)
		{
			i++;
			search_filenames.push_back(argv[i]);
			
		}
		if(strcmp(argv[i],"-fa")==0)
		{
			i++;
			FA=atoi(argv[i]);

			continue;
		}
	

	}

	if (in_filenames.empty()||out_filename.empty()||(search_filenames1.empty()&&search_filenames.empty()))
	{
		cout<<"Too few inputs!"<<endl;
		return -1;
	}

	bool paired_mode=0;
	if(search_filenames.empty())
	{
		paired_mode=1;
		cout<<search_filenames1.size()<<" inputs."<<endl;
	}
	else
	{
		paired_mode=0;
		cout<<search_filenames.size()<<" inputs."<<endl;
		
	}

	size_t hashTableSZ=100000;
	uint64_t *Kmer_bits;
	size_t sz_Kmer_bits=sizeof(uint64_t)*1000;
	Kmer_bits=(uint64_t *)malloc(sz_Kmer_bits);
	if (hashTableSZ<min_ht_sz)
	{
		hashTableSZ=min_ht_sz;
	}



	struct hashtable ht;
	size_t size_idx=sizeof(bool)*hashTableSZ;
	size_t sz_stps=sizeof(uint64_t)*hashTableSZ;
	ht.idx=(bool *)malloc(hashTableSZ) ;
	memset(ht.idx,0,hashTableSZ);
	
	ht.store_pos=(uint64_t *)malloc(sz_stps) ;
	memset(ht.store_pos,0,hashTableSZ);

	size_t sz_bkt_key=hashTableSZ*sizeof(uint64_t)*2;
	size_t sz_bkt_key_cnt=hashTableSZ*sizeof(int)*2;
	struct bucket bkt;

	bkt.key=(uint64_t *) malloc(sz_bkt_key);
	bkt.key_cnt=(int *) malloc(sz_bkt_key_cnt);
	memset(bkt.key_cnt,0,hashTableSZ);




	string in_line;
	char Kmer[Max_Kmer_Size];
	int Kmer_sz,len=0;
	uint64_t Kmer_cnt=0;
	int k=0;

	size_t curcnt=0;

	for (size_t in_cnt=0;in_cnt<in_filenames.size();++in_cnt)
	{
		ifstream infile1(in_filenames[in_cnt].c_str());
		while(getline(infile1,in_line))
		{
			if(in_line[in_line.size()-1]=='\n'||in_line[in_line.size()-1]=='\r')
			{
				in_line.resize(in_line.size()-1);
			}
			size_t Read_sz=in_line.size();

			for (size_t i=0;i<Read_sz;++i)
			{
				while(i<Read_sz&&!isalpha(in_line[i]))
				{
					++i;
				}
				if (i==Read_sz)
				{break;}

				len=0;
				while(i<Read_sz&&isalpha(in_line[i]))
				{
					Kmer[len++]=in_line[i++];
				}
				
				Kmer[len]='\0';


				Kmer_bits[k]=str2bits(Kmer,len);
				//cout<<bits2str(Kmer_bits[k],len);
				Kmer_cnt++;
				k++;
				if (k==1000)
				{
					batch_hash_insertion(Kmer_bits,ht,bkt,k,len,&curcnt,hashTableSZ);
					k%=1000;
				}

			//	cout<<Kmer<<endl;
			}
		}
		batch_hash_insertion(Kmer_bits,ht,bkt,k,len,&curcnt,hashTableSZ);
	
	
	}
	Kmer_sz=len;
	
	free( Kmer_bits);


	cout<<Kmer_cnt<<" Kmers loaded."<<endl;
	cout<<curcnt<<" different Kmers."<<endl;

	if(paired_mode)
	{
		string in_line2,in_seq1,in_seq2;

		size_t Reads_found=0;
		string out_filename1,out_filename2;
		out_filename1=out_filename+"1";
		out_filename2=out_filename+"2";
		ofstream outfile1(out_filename1.c_str());
		ofstream outfile2(out_filename2.c_str());
		//int nr=0;
		for (size_t s_cnt=0;s_cnt<search_filenames1.size();++s_cnt)
		{
			cout<<"Processing file:" <<s_cnt+1<<endl;
			ifstream infile2(search_filenames1[s_cnt].c_str());
			ifstream infile3(search_filenames2[s_cnt].c_str());
			while(getline(infile2,in_line))
			{
				if(in_line[in_line.size()-1]=='\n'||in_line[in_line.size()-1]=='\r')
				{
					in_line.resize(in_line.size()-1);
				}
				getline(infile3,in_line2);

				if(in_line2[in_line2.size()-1]=='\n'||in_line2[in_line2.size()-1]=='\r')
				{
					in_line2.resize(in_line2.size()-1);
				}
				if (in_line[0]!='@'&&in_line[0]!='>')
				{
					continue;
				}
				else
				{
					getline(infile2,in_seq1);
					if(in_seq1[in_seq1.size()-1]=='\n'||in_seq1[in_seq1.size()-1]=='\r')
					{
						in_seq1.resize(in_seq1.size()-1);
					}
					getline(infile3,in_seq2);
					if(in_seq2[in_seq2.size()-1]=='\n'||in_seq2[in_seq2.size()-1]=='\r')
					{
						in_seq2.resize(in_seq2.size()-1);
					}
					uint64_t seq1,seq2;
					bool found=0,found1=0,found2=0;
				//	nr++;
					int seq1_sz=in_seq1.size();
					for(int k=0;k<seq1_sz+1-Kmer_sz;++k)
					{
						string KmerStr1=in_seq1.substr(k,Kmer_sz);
						bool Nflag=0;				
						for(int kk=0;kk<KmerStr1.size();++kk)
						{
							if(KmerStr1[kk]=='N')
							{

								Nflag=1;
								break;
							}
						}
						if(Nflag==1)
						{continue;}

						seq1=str2bits(KmerStr1.c_str(),Kmer_sz);
					
					
						found1=hash_lookup(seq1,ht,bkt,Kmer_sz,hashTableSZ);
					

						if (found1==1)
						{
							break;

						}
				
					}
					if (found1==0)
					{
						
						int seq2_sz=in_seq1.size();
						for(int k=0;k<seq2_sz-Kmer_sz+1;++k)
						{
						
							string KmerStr2=in_seq2.substr(k,Kmer_sz);

							bool Nflag=0;				
							for(int kk=0;kk<KmerStr2.size();++kk)
							{
								if(KmerStr2[kk]=='N')
								{

									Nflag=1;
									break;
								}
							}
							if(Nflag==1)
							{continue;}


						
							seq2=str2bits(KmerStr2.c_str(),Kmer_sz);
						
						
							found2=hash_lookup(seq2,ht,bkt,Kmer_sz,hashTableSZ);

							if (found2==1)
							{
								break;

							}
						}
					}

					found=found1|found2;

					if (found==1)
					{
						//cout<<(int)found1<<" "<<(int)found2<<" "<<nr<<endl;
						if(FA)
						{
							in_line[0]='>';
						}
						outfile1<<in_line<<endl<<in_seq1<<endl;
						outfile2<<in_line<<endl<<in_seq2<<endl;
						if(in_line[0]=='@'&&(!FA))
						{
							getline(infile2,in_seq1);
							if(in_seq1[in_seq1.size()-1]=='\n'||in_seq1[in_seq1.size()-1]=='\r')
							{
								in_seq1.resize(in_seq1.size()-1);
							}
							outfile1<<in_seq1<<endl;
							getline(infile2,in_seq1);
							if(in_seq1[in_seq1.size()-1]=='\n'||in_seq1[in_seq1.size()-1]=='\r')
							{
								in_seq1.resize(in_seq1.size()-1);
							}
							outfile1<<in_seq1<<endl;

							getline(infile3,in_seq2);
							if(in_seq2[in_seq2.size()-1]=='\n'||in_seq2[in_seq2.size()-1]=='\r')
							{
								in_seq2.resize(in_seq2.size()-1);
							}
							outfile2<<in_seq2<<endl;
							getline(infile3,in_seq2);
							if(in_seq2[in_seq2.size()-1]=='\n'||in_seq2[in_seq2.size()-1]=='\r')
							{
								in_seq2.resize(in_seq2.size()-1);
							}
							outfile2<<in_seq2<<endl;
						}
						Reads_found++;

					}
				}
			
			//	size_t Read_sz=in_line.size();

			}
		}
		cout<<Reads_found<<" reads found."<<endl;
	}
	else
	{
		string in_line2,in_seq1;

		size_t Reads_found=0;
		string out_filename1;
		out_filename1=out_filename;
		ofstream outfile1(out_filename1.c_str());
		//int nr=0;
		
		for (size_t s_cnt=0;s_cnt<search_filenames.size();++s_cnt)
		{
			cout<<"Processing file:" <<s_cnt+1<<endl;
			ifstream infile2(search_filenames[s_cnt].c_str());
			
			while(getline(infile2,in_line))
			{
				
				

				if (in_line[0]!='@'&&in_line[0]!='>')
				{
					continue;
				}
				else
				{
				
					getline(infile2,in_seq1);
					if(in_seq1[in_seq1.size()-1]=='\n'||in_seq1[in_seq1.size()-1]=='\r')
					{
						in_seq1.resize(in_seq1.size()-1);
					}

					uint64_t seq1,seq2;
					bool found=0,found1=0,found2=0;
			//		nr++;
					int seq1_sz=in_seq1.size();
					for(int k=0;k<seq1_sz+1- Kmer_sz;++k)
					{
						string KmerStr1=in_seq1.substr(k,Kmer_sz);
						bool Nflag=0;				
						for(int kk=0;kk<KmerStr1.size();++kk)
						{
							if(KmerStr1[kk]=='N')
							{

								Nflag=1;
								break;
							}
						}
						if(Nflag==1)
						{continue;}

						seq1=str2bits(KmerStr1.c_str(),Kmer_sz);
					
					
						found1=hash_lookup(seq1,ht,bkt,Kmer_sz,hashTableSZ);
					

						if (found1==1)
						{
							break;

						}
				
					}
					
					found=found1;

					if (found==1)
					{
						if(FA)
						{
							in_line[0]='>';
						}

						//cout<<(int)found1<<" "<<" "<<nr<<endl;
						outfile1<<in_line<<endl<<in_seq1<<endl;

						
					
						if(in_line[0]=='@'&&(!FA))
						{
							getline(infile2,in_seq1);
							if(in_seq1[in_seq1.size()-1]=='\n'||in_seq1[in_seq1.size()-1]=='\r')
							{
								in_seq1.resize(in_seq1.size()-1);
							}
							outfile1<<in_seq1<<endl;
							getline(infile2,in_seq1);
							if(in_seq1[in_seq1.size()-1]=='\n'||in_seq1[in_seq1.size()-1]=='\r')
							{
								in_seq1.resize(in_seq1.size()-1);
							}
							outfile1<<in_seq1<<endl;
						}
						Reads_found++;

					}
				}
			
			//	size_t Read_sz=in_line.size();

			}
		}
		cout<<Reads_found<<" reads found."<<endl;
	}
	return 0;
}