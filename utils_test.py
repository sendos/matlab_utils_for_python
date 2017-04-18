"""
   Script with sample usage of the functions in matlab_utils.py

   Copyright (c) 2017 Andrew Sendonaris.
"""

# In this script, we convert the following Matlab script for use in Python
"""
function D = mydist(X)      
  if isempty(X)
    error('Input matrix is empty\n');
  end
 
  % Get the number of points
  num_points = size(X, 1); 
 
  if num_points < 2
    error('Number of points should be more than one\n');
  end
 
  % Initialize the result
  D = zeros(num_points, num_points);
 
  for i = 1:num_points-1
    for j = 1:num_points
      if(i < j)
        % Ensure the matrix is symmetric
        D(i,j) = sqrt(sum((X(i,:)-X(j,:)).^2));
        D(j,i) = D(i,j);
      end
    end
  end
end

X = [[1, 2, 3]; [4, 5, 6]; [7, 8, 9]];
D = mydist(X);

fprintf('D = [\n')
for I = [1:size(D,1)]
    fprintf('  %5.2f %5.2f %5.2f\n', D(I,:))
end
fprintf(']\n')
"""

from matlab_utils import *

def mydist(X):
  if isempty(X):
    error('Input matrix is empty\n');
  end
  
  # Get the number of points
  num_points = size(X, 1); 
  
  if num_points < 2:
    error('Number of points should be more than one\n');      
  end
  
  # Initialize the result
  D = zeros(num_points, num_points);
  
  for i in mrange[1:num_points-1]:
    for j in mrange[1:num_points]:
      if(i < j):
        # Ensure the matrix is symmetric
        D[i,j] = sqrt(sum((X[i,:]-X[j,:])**2));
        D[j,i] = D[i,j];
      end
    end
  end

  return D
end

X = marray([[1, 2, 3], [4, 5, 6], [7, 8, 9]]);
D = mydist(X);

fprintf('D = [\n')
for I in mrange[1:size(D,1)]:
    fprintf('  %5.2f %5.2f %5.2f\n', *D[I,:])
end
fprintf(']\n')


