# Dijkstra

# Python 3

# RWD, 20190908

# converted to Python 3, 20191109

import math
INFINITY = float("inf")


infile = open("Dijkstra_Data_6.txt","r")
lines = infile.readlines()
num_verts = int(lines[0])
print ("Number of vertices : "+str(num_verts))
# create the Weight matrix
W = []
row = [0]*num_verts
for i in range(num_verts):
   W.append(row[:])
r = 0
for line in lines[1:] :
   #print "line before split",line
   line = line.split()
   #print "line after split",line
   c = 0
   for w in line:
      #print "w = '",w,"'"
      W[r][c] = int(w.strip())
      c += 1
   r+= 1



# create the necessary arrays
Cost = row[:]
Estimate = [INFINITY]*num_verts
Predecessor = row[:]
Reached = [False]*num_verts
Candidate = Reached[:]

# choose the start vertex

A = 0

Cost[A] = 0
Reached[A] = True
 #~ for each other vertex x:
   #~ Reached[x] = False
#for each neighbour x of A:
for x in range(num_verts):
   if W[A][x] > 0:
      Estimate[x] = W[A][x]
      Candidate[x] = True
      Predecessor[x] = A
   else: 
      Estimate[x] = INFINITY
  
  # Diagnostic print statements disabled but included for future use if necessary
#~ print ("Reached   : "+str(Reached))
#~ print ("Cost      : "+str(Cost))
#~ print ("Candidate : "+str(Candidate))
#~ print ("Estimate  : "+str(Estimate))

Predecessor[A] = -1

num_reached = 1      

most_distant_vertex = A

while  (num_verts != num_reached):
   #~ print()
   #~ print ("Reached   : "+str(Reached))
   #~ print ("Cost      : "+str(Cost))
   #~ print ("Candidate : "+str(Candidate))
   #~ print ("Estimate  : "+str(Estimate))
   # find the best candidate
   best_candidate_estimate = INFINITY
   for x in range(num_verts):
      if Candidate[x] and Estimate[x] < best_candidate_estimate:
         v = x
         best_candidate_estimate = Estimate[x]
   if (best_candidate_estimate == INFINITY):
         break             # there are no candidates
   Cost[v] = Estimate[v]
   Reached[v] = True
   Candidate[v] = False
   print ("Reached vertex "+str(v)+" with cost = "+str(Cost[v]))
   if Cost[v] > Cost[most_distant_vertex]:
      most_distant_vertex = v
   for y in range(num_verts):			# update the neighbours of v
      if W[v][y] > 0  and  Reached[y] == False:
         Candidate[y] = True
         if Cost[v] + W[v][y] < Estimate[y]:
            Estimate[y] = Cost[v] + W[v][y]
            Predecessor[y] = v
   num_reached += 1

if (num_verts != num_reached):
   print ("Not all vertices were reachable")
print()
for v in range(num_verts):
   print (str(v)+" : Cost = "+str(Cost[v])+"\tPredecessor = "+str(Predecessor[v]))
            
print()
print ("Required output as per lab assignment:")
print ("The vertex furthest from vertex "+str(A)+" is vertex "+str(most_distant_vertex)+", which has a Cost of"+str(Cost[most_distant_vertex]))
print()
print("Goodbye")