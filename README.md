## Ultra-conserved elements (UCEs) identification



#### 1, Build the ancestral sequences with high quality genomes

```shell
prequel --no-probs --seqs Avian rf_$chr.fa --msa-format MAF multiz_mammal_$chr.maf nonconserved-4d.cn.mod $chr
```

#### 2, Mimic all the genomes to  k-mers with length of 50bp and 10bp bootstraps

```shell
perl kmer_produce.pl species_genome.fa 50 10 species_genome_reads.fa
```

#### 3, Aligning all reads from different genomes to the ancestor genome, separately

```shell
bowtie2 -p 4 -x ancestor.fa -f species_genome_reads.fa --no-unal -S species_genome_reads.sam
samtools view -bS species_genome_reads.sam >species_genome_reads.bam
samtools sort species_genome_reads.bam >species_genome_reads.sort.bam
```

#### 4, Obtain candidate UCEs 

##### 4.1 Get the elements absolutely aligned to the ancestor genome without any mismatch from each species

```shell
samtools view species_genome_reads.sort.bam |awk '$6=="50M"&&$14=="XM:i:0"'|awk '{print $3"\t"$4"\t"$4+49}' > species.aligned.bed
```

##### 4.2 Merge all of the elements together

```shell
cat *aligned.bed > all.bed
bedtools sort -faidx ancestor.chrinfo -i all.bed > all.sort.bed
  #ancestor.chrinfo is a chromosome list of the ancestor genome
bedtools merge -i all.sort.bed|uniq > all.sort.merge.bed
```

##### 4.3 Filter the elements that are not longer than 100bp

```shell
less -S all.sort.merge.bed| awk '$2-$1+1>100' > candidate_UCEs.bed
bedtools getfasta -fi ancestor.fa -bed candidate_UCEs.bed -fo candidate_UCEs.fa
```

#### 5,  Identify UCEs

##### 5.1 Mapping the candidate UCEs to each species genome

```shell
makeblastdb -in species_genome.fa -dbtype nucl -out species_genome_db
blastn -query candidate_UCEs.fa -db species_genome_db -out species.blastn.out -outfmt 6 -evalue 1e-5 -num_threads 4 -max_target_seqs 1 -max_hsp 1
```

##### 5.2  Filter the elements with identity and coverage and merge the results to get the identity matrix of candidate UCEs in all species.

```shell
python filter_blastn_out.py -i species.blastn.out -o species.blastn.filter.out
for i in *.blastn.filter.out;do echo $PWD/$i>>merge_filter.list;done
  #generate the full pathway of all filtered blastn results
python merge.filter.bed.list.iden.py -l merge_filter.list -o merge_candidateUCEs_iden.out
```

##### 5.3 The elements which are 100% identical with at least one branch and with at least 80% identity across all branches, were defined as final UCEs longer than 200bp.





