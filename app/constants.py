
# error messages for fake_data.py

WRONG_SHAPE = """Wrong input params combination, got shape: {}
The valid combinations and their descriptions are:
--------------------------------------------------
     size page begin end
    [1,   0,   0,    0]      # custom size
    [1,   0,   0,    1]      # interval [ end-(size+1) ; end )
    [1,   0,   1,    0]      # interval [ begin ; begin+size )
    [1,   1,   0,    0]      # custom size with pagination
    [0,   0,   1,    1]      # interval [ begin : end )
    [0,   0,   0,    0]      # default 20 elements
    [0,   1,   0,    0]      # given page with the default 20 elements
--------------------------------------------------
"""

