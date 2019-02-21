#    Copyright (C) 2019 Greenweaves Software Limited
#
#    This is free software: you can redistribute it and/or modify
#    it under the terms of the GNU General Public License as published by
#    the Free Software Foundation, either version 3 of the License, or
#    (at your option) any later version.
#
#    This software is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#    GNU General Public License for more details.
#
#    You should have received a copy of the GNU General Public License
#    along with GNU Emacs.  If not, see <http://www.gnu.org/licenses/>
#
#    BA5H Find a Highest-Scoring Fitting Alignment of Two Strings

import numpy as np

def ba5h(s,t,match_reward=1,indel_cost=-1,replace_cost=lambda a,b: -1,show_scores=False):

      def dynamic_programming(s,t):
            def create_scores():
                  score=[[0 for j in range(len(t)+1)] for i in range(len(s)+1)]
      
                  for j in range(len(t)+1):
                        score[0][j]=j
                  for i in range(len(s)+1):
                        score[i][0]=i
      
                  for i in range(1,len(s)+1):
                        for j in range(1,len(t)+1):
                              score[i][j] = max(
                                    score[i-1][j]   + indel_cost if 0<j and j<len(t) else 0,
                                    score[i][j-1]   + indel_cost,
                                    score[i-1][j-1] + (1 if s[i-1]==t[j-1] else replace_cost(s[i-1],t[j-1])))
                              
                  if show_scores:
                        print (' ',['#']+t)
                        for i in range(len(s)+1):
                              print ((['#']+s)[i] ,score[i])
                        print (' ',['#']+t) 
                  return score
            
            def extract(s,t,matrix):
                  m  = len(matrix)-1
                  n  = len(matrix[0])-1
                  s1 = []
                  t1 = []
                  while m>0 and n>0:
                        moves  = [(m-1,n),(m,n-1),(m-1,n-1)]
                        scores = [matrix[m-1][n]+indel_cost if 0 < n and n<len(t) else 0,
                            matrix[m][n-1]+indel_cost ,
                            matrix[m-1][n-1] + (0 if s[m-1]==t[n-1] else replace_cost(s[m-1],t[n-1]))]
                        ss     = [s[m-1],'-',s[m-1]]
                        ts     = ['-',t[n-1],t[n-1]]
                        index  = np.argmin(scores)
                        m,n    = moves[index]
                        s1.append(ss[index])
                        t1.append(ts[index])
                  s1.reverse()
                  t1.reverse()
                  return 0,''.join(s1),''.join(t1)
                    
             
            score = create_scores()
  
                   
            return  extract(s,t,score)
      
      d,s1,t1=dynamic_programming([s0 for s0 in s], [t0 for t0 in t])
      return d,''.join(s1),''.join(t1)

if __name__=='__main__':
      d,s1,t1 = ba5h('GTAGGCTTAAGGTTA','TAGATA',show_scores=True)
      print (d)
      print (s1)
      print (t1)
