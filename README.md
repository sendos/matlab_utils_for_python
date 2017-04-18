# Matlab-like utils for Python
This is a library that provides access to Matlab-like functions in Python

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

Below is some sample Matlab code that was transformed into Python code that uses the current library. The Python code looks very similar to the Matlab code, and the effort to port the Matlab code to this form was minimal.
<table>
<tr><th>Matlab code</th><th>Python code</th></tr>
<tr><td colspan="2">
<img src="https://cloud.githubusercontent.com/assets/1019930/25139782/3c0b6ce8-2456-11e7-88a2-e9be395e306c.png">
 </td></tr>
</table>

Note: The resulting code is not very "Pythonic", which is OK for the purposes of this lilbrary, which is meant to address two major use-cases: 
   * Quick scripts that Matlab experts might have to write on a computer that doesn't have Matlab installed.
   * Porting large Matlab codebases to Python, which can be quite tedious, and which this library helps make much easier.



## Installation and Usage

No installation required beyond downloading matlab_utils.py into your current folder or anywhere in Python's load path. Make sure you have NumPy installed with your Python.

Then, in your Python scripts add the following
```python
from matlab_utils import *
```
and use the functions included in the module. As mentioned above, currently supported are the following functions:

    ischar, datenum, datestr, isempty, fopen, fclose, fprintf, sprintf, size,
    find, regexprep, regexp, regexpi, randn, rand, ones, zeros, error, length
    
as well as marray and mrange, examples of which are given above.

## Authors

* **Andrew Sendonaris** - [sendoswww](https://github.com/sendoswww)

