Title: Nature based algorithms vs Shellsort's gap sequences

1. Problem description:
The problem is to find candidate gap sequences for Shellsort.
Candidate meaning - winning in some fixed sorting range N (2500 in this experiment) with currently known best gap sequences (Skeanz, Ehrenborg,Jaromczyk (SEJ) and Ciura)
Objective function - time of excecution or count of operations (during those measurements it was count), very costly to ases, creating big overheads if needed also during creation of new populations

program was starting with population of 100 sequences (4 already known Tokuda, Ciura, Lee, SEJ and 96 semi random) in parallel 3 algortihms in endless gap sequences seeking (stopped manually after few hours), in each population/generation all sequences where assesed, compared and sorted from most to less promising, then going into generating of new population with one of the searchign/optimizing algortihms

Used algorithms:
- genetic - modified (10% survivors, 50% of childs (crossover) and 40$ of random + 10% that child or survivar get muatated)
- cuckoo - modified (50% survivors, 25% levy generated nests, 25% random nests) - step size of 1% of current gap (might be to small) beta 1,5, instead of comparing new levy nest with random one, best 50% of nests is surviving, worst 25% is abandoned and randomly generated, remaining 25% is excahnged for levy nests - removing overhead of objective assesment 
- abc - seems classic (emplyed bee phase, onlooker bee phase, scout be phase (limit trials 20)) - big overhead of calculating objective function many times during population generation phase

2. results:
plots and json stats for each algorithms

3. Conclusions:
current genetic algorithm is converging to local optimum (most often of one of already noted sequences - ciura or SEJ) very quickly, and then almost all new solutaions are created via mutation. It is generating new solutions faster than other 2 algorithms but they are very close to each other, not covering much ground especialy for smaller increments of sequence

cuckoo search seems to be good middle ground - also quick solution generation (most likely because of removal of objective assesment during population creation) but also fast going into local optima, while levy flights are gnerating nice and compact results, current meta parameters might not do much good to the algorithm - it will be additionaly tested in the future, with hope to find better parameters suting the problem, currently it is very hard to set porper step size to not mess with small icnrements and still produce nice exploration of space

abc surprised with the best exploration, covering various different begginings of sequences (first few increments starting from 1), but in the same time failed in terms of speed - very costly assesmnet of objective function during employed and onlooker phases are painful in this scenario, algorithm has potential but most likely will be abandoned in future research if optimization of cuckoo search will turn out well, other possible scenario is to keep abc for greate exploration and join it with genetic or cuckoo for additional exploitation