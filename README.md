# Matlab utils for Python
Library that provides access to Matlab-like functions in Python

Currently supported:

    ischar, datenum, datestr, isempty, fopen, fclose, fprintf, sprintf, size,
    find, regexprep, regexp, regexpi, randn, rand, ones, zeros, error, length

The library also provides access to 
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
The syntax tries to follow Matlab-like syntax as much as possible, given the constraints of Python.

<table>
<tr><th>Matlab code</th><th>Python code</th></tr>
<tr><td>
<pre lang="matlab">function D = mydist(X)      
  if isempty(X)
    error('Input matrix is empty \n');
  end
 
  % Get the number of points
  num_points = size(X,1);
  </pre>
</td><td>
<pre lang="python">
def mydist(X):
  if isempty(X):
    error('Input matrix is empty \n');
  end
  
  \# Get the number of points
  num_points = size(X,1); 
 </pre>
 </td></tr>
</table>



