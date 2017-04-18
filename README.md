# Matlab-like utils for Python
Library that provides access to Matlab-like functions in Python

Currently supported:

    ischar, datenum, datestr, isempty, fopen, fclose, fprintf, sprintf, size,
    find, regexprep, regexp, regexpi, randn, rand, ones, zeros, error, length

The library also provides access to:
* Matlab-like arrays, which allow 1-based indexing and also Matlab-like slices
```python
    x = marray(some_list)
    y = x[1:3]
    z = x[1:2:end]
```
* Matlab-like ranges
```python
    for x in mrange[1:3:10]:
        fprintf('%d\n', x)
```
Some of these functions (like randn and ones) exist in NumPy, but the syntax is not identical to Matlab. The ones in this library try to be as close to Matlab syntax as possible, given the constraints of Python, to minimize code changes.

Note: The resulting code is not very "Pythonic", which is OK for the purposes of this lilbrary, which is meant to address two major use-cases: 
   * Quick scripts that Matlab experts might have to write on a computer that doesn't have Matlab installed.
   * Porting large Matlab codebases to Python, which can be quite tedious, and which this library helps make much easier.

<table>
<tr><th>Matlab code</th><th>Python code</th></tr>
<tr><td>
<pre lang="matlab">
function D = mydist(X)      
if isempty(X)
  error('Input matrix is empty\n');
end

% Get the number of points
num_points = size(X, 1); 
 
if num_points &lt; 2
  error('Num points &lt; 2\n');
end
 
% Initialize the result
D = zeros(num_points, num_points);

for i = 1:num_points-1
  for j = 1:num_points
    if(i &lt; j)
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
</pre>
</td><td>
<pre lang="python">def mydist(X):
if isempty(X):
  error('Input matrix is empty\n');
end

\# Get the number of points
num_points = size(X, 1); 

if num_points &lt; 2:
  error('Num points &lt; 2');      
end

\# Initialize the result
D = zeros(num_points, num_points);

for i in mrange[1:num_points-1]:
  for j in mrange[1:num_points]:
    if(i &lt; j):
      \# Ensure the matrix is symmetric
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
 </pre>
 </td></tr>
</table>




