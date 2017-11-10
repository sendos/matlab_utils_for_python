"""
   Module that provides access to Matlab-like functions, such as
      ischar, datenum, datestr, isempty, fopen, fclose, fprintf, sprintf, size,
      find, regexprep, regexp, regexpi, randn, rand, ones, zeros, error, length

   It also provides access to 
     * Matlab-like arrays, which allow 1-based indexing and also Matlab-like slices
        x = marray(some_list)
        y = x[1:3]
        z = x[1:2:end]

     * Matlab-like ranges
        for x in mrange[1:3:10]:
           fprintf('%d\n', x)

   The syntax tries to follow Matlab-like syntax as much as possible, 
   given the constraints of Python.

   Copyright (c) 2017 Andrew Sendonaris.

   Permission is hereby granted, free of charge, to any person obtaining a copy
   of this software and associated documentation files (the "Software"), to deal
   in the Software without restriction, including without limitation the rights
   to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
   copies of the Software, and to permit persons to whom the Software is
   furnished to do so, subject to the following conditions:

   The above copyright notice and this permission notice shall be included in all
   copies or substantial portions of the Software.

   THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
   IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
   FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
   AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
   LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
   OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
   SOFTWARE.
"""

from numpy import *
import numpy.random as rnd
from numpy.matlib import repmat

import re
import sys
from datetime import *
from time import strftime, time

# Use this to enable x[3:end] and also
#  if (x == 1):
#     y = 2
#  end
end = -1


class MRange(object):
    # Class to enable Matlab-like ranges
    # for x in mrange[1:2:10]:
    #   fprintf('%d\n', x)
    def __getitem__(self, key):
        if key.step is None:
            # mrange[1:10]
            start, step, stop = key.start, 1, key.stop
        else:
            # mrange[1:2:10]
            start, step, stop = key.start, key.stop, key.step
        stop_add = 1 if step > 0 else -1
        return marray(range(start, stop+stop_add, step))

mrange = MRange()


class marray(object):
    # Class to enable 1-based indexing into arrays
    # x = marray(1,3,8,9,5)
    # or 
    # x = marray([1,3,8,9,5])
    # y = x[1:3]
    # z = x[2:2:end]
    def __init__(self, *args):
        if len(args) == 1:
            self.array = array(args[0])
        else:
            self.array = array(args)
            
    def _calc_indexes(self, key):
        if isinstance(key, tuple):
            # For multi-dimentional arrays, key is a tuple,
            # where every entry is an index into that dimention.
            indexes = list(key)
        else:
            indexes = list((key,))
            
        for idx, key in enumerate(indexes):
            if isinstance(key, int):
                # x[1]
                start, step, stop = key, 1, key
            elif key.start is None and key.stop is None and key.step is None:
                # x[:]
                start, step, stop = 1, 1, self.array.shape[idx]
            elif key.step is None:
                # x[1:10]
                start, step, stop = key.start, 1, key.stop
            else:
                # x[1:2:10]
                start, step, stop = key.start, key.stop, key.step
                
            if stop == -1:
                stop = self.array.shape[idx]

            indexes[idx] = slice(start-1, stop, step)
        return tuple(indexes)
    
    def __getitem__(self, key):
        indexes = self._calc_indexes(key)
        result = self.array[indexes]
        if len(result) == 1:
            return result[0]
        else:
            return marray(result)

    def __setitem__(self, key, value):
        indexes = self._calc_indexes(key)
        self.array[indexes] = value

    def __repr__(self):
        return repr(self.array)

    # Make the class iterable, so it can be converted to a list or tuple
    def __iter__(self):
        for v in self.array:
            yield v

    def __len__(self):
        return len(self.array)

    def __add__(self, other):
        result = self.array + other
        return result[0] if len(result) == 1 else marray(result)
    
    def __sub__(self, other):
        result = self.array - other
        return result[0] if len(result) == 1 else marray(result)
    
    def __radd__(self, other):
        result = other + self.array
        return result[0] if len(result) == 1 else marray(result)

    def __rsub__(self, other):
        result = other - self.array
        return result[0] if len(result) == 1 else marray(result)
      
    def __mul__(self, other):
        result = self.array * other
        return result[0] if len(result) == 1 else marray(result)
    
    def __rmul__(self, other):
        result = self.array * other
        return result[0] if len(result) == 1 else marray(result)
    
    def __truediv__(self, other):
        result = self.array/other
        return result[0] if len(result) == 1 else marray(result)
    
    def __rtruediv__(self, other):
        result = other/self.array
        return result[0] if len(result) == 1 else marray(result)
    
    def __lt__(self, other):
        result = (self.array < other)
        return result[0] if len(result) == 1 else marray(result)
   
    def __le__(self, other):
        result = (self.array <= other)
        return result[0] if len(result) == 1 else marray(result)

    def __gt__(self, other):
        result = (self.array > other)
        return result[0] if len(result) == 1 else marray(result)

    def __ge__(self, other):
        result = (self.array >= other)
        return result[0] if len(result) == 1 else marray(result)

    @property
    def size(self):
        return self.array.size
    
def ischar(x):
    return isinstance(x, basestring)

def error(str, *args):
    sys.exit(str % args)

def length(x):
    return len(x)

def sprintf( format, *args ):
    return (format % args)

def datenum( date_str, format='%b-%d-%Y' ):
    d = datetime.strptime( date_str, format )
    return d.toordinal()

def datestr( date_num, format='%b-%d-%Y' ):
    d = date.fromordinal(date_num)
    return d.strftime(format)

SRE_MATCH_TYPE = type(re.match('', ''))
    
def isempty(x):
    if x is None:
        return True
    elif isinstance(x, basestring):
        return (x == '')
    elif isinstance(x, list) or isinstance(x, dict):
        return (len(x) == 0)
    elif isinstance(x, SRE_MATCH_TYPE):
        return (x is None)
    else:
        return (x.size == 0)

def fopen(filename, mode='r'):
    try:
        fid=open(filename,mode)
    except IOError:
        error('File %s cannot be opened', filename)
    return fid

def fclose(fid):
    fid.close()

def fprintf( fid, format=None, *args ):
    if isinstance(fid, basestring):
        if format==None:
            # fprintf('foo\n')
            str = fid
        else:
            if len(args) == 0:
                # fprintf('foo = %d\n', 5)
                args = format
            else:
                # fprintf('foo = %d, bar = %f\n', 5, 3.1)
                args = tuple([format] + list(args))
            format = fid
            str    = format % args
        sys.stdout.write(str)
    else:
        if len(args) == 0:
            # fprintf(fid, 'foo\n')
            str = format
        else:
            # fprintf(fid, 'foo = %d\n', 5)
            # fprintf(fid, 'foo = %d, bar = %f\n', 5, 3.1)
            str = format % args
        fid.write(str)        

def regexprep(str, pattern, replace):
    replace = re.sub('\$(\d)','\\\g<\g<1>>',replace)
    if isinstance(str, basestring):
        result = re.sub(pattern, replace, str)
    else:
        result = str
        for idx in range(0,len(result)):
            result[idx] = re.sub(pattern, replace, result[idx])
    return result

def regexp(str, pattern):
    pattern = re.sub('\(\?<','(?P<',pattern)
    return re.search(pattern, str)


def regexpi(str, pattern):
    pattern = re.sub('\(\?<','(?P<',pattern)
    return re.search(pattern, str, flags=re.IGNORECASE)


def randn(*args):
    # Mimic Matlab's randn() syntax
    if len(args) == 0:
        # randn() results in a scalar
        return rnd.randn()
    elif len(args) == 1:
        # randn(N) results in NxN matrix
        return marray(rnd.randn(args[0], args[0]))
    elif len(args) == 2 and args[0] == 1:
        # randn(1,N) results in 1xN vector, i.e. numpy array of length N
        return marray(rnd.randn(args[1]))
    else:
        return marray(rnd.randn(*args))

def rand(*args):
    # Mimic Matlab's rand() syntax
    if len(args) == 0:
        # rand() results in a scalar
        return rnd.rand()
    elif len(args) == 1:
        # rand(N) results in NxN matrix
        return marray(rnd.rand(args[0], args[0]))
    elif len(args) == 2 and args[0] == 1:
        # rand(1,N) results in 1xN vector, i.e. numpy array of length N
        return marray(rnd.rand(args[1]))
    else:
        return marray(rnd.rand(*args))


np_ones = ones
def ones(*args):
    # Mimic Matlab's ones() syntax
    if len(args) == 0:
        # ones() results in a scalar
        return 1
    elif len(args) == 1:
        # ones(N) results in NxN matrix
        return marray(np_ones((args[0], args[0])))
    elif len(args) == 2 and args[0] == 1:
        # ones(1,N) results in 1xN vector, i.e. numpy array of length N
        return marray(np_ones(args[1]))
    else:
        return marray(np_ones(args))

np_zeros = zeros
def zeros(*args):
    # Mimic Matlab's zeros() syntax
    if len(args) == 0:
        # zeros() results in a scalar
        return 0
    elif len(args) == 1:
        # zeros(N) results in NxN matrix
        return marray(np_zeros((args[0], args[0])))
    elif len(args) == 2 and args[0] == 1:
        # zeros(1,N) results in 1xN vector, i.e. numpy array of length N
        return marray(np_zeros(args[1]))
    else:
        return marray(np_zeros(args))

def find(cond):
    # idx = find(x < 3)
    return marray(where(cond)[0])

def size(x, dim=None):
    # a, b = size(x)
    # a = size(x, 1)
    # b = size(x, 2)
    if isinstance(x, marray):
        x = x.array
    shape = x.shape
    if len(shape) == 1:
        shape = (1 if shape[0] != 0 else 0, shape[0])
    if dim is None:
        return shape
    else:
        return shape[dim-1]

# --------------------------------------------------------------------------------
# Implement Matlab's mesh() using matplotlib
# from matplotlib.pyplot import *
# from mpl_toolkits.mplot3d import Axes3D    
# def mesh(x,y,z):
#     if len(x.shape)==1 and len(y.shape)==1:
#         # x and y are vectors
#         xax, yax = meshgrid(x,y)
#     elif len(x.shape)==2 and len(y.shape)==2:
#         xax, yax = x,y
#     else:
#         sys.exit('x and y should either both be vectors or both be matrixes of the same size as z')
#     ax = gcf().add_subplot(111, projection='3d')
#     ax.plot_surface(xax,yax,z)
