Add an extra space on each of the strings so the two dimensional arrays will work. 

Then create a two dimensional array to hold all the values. To create a two dimensional array make an array within an array. Fill in all of the values to 0. 

Traverse through the matrix and fill in the first row with the values of SPACE_PENALTY + matrix[i][j - 1]. then move to the first column and oil in the values with SPACE_PENALTY + matrix[i - 1][j]. However, if the column is not 1 and the row is not 1 then you must find the max between all of the cases. max(
    				s(s1[i],s2[j]) + matrix[i - 1][j - 1], 
    				SPACE_PENALTY + matrix[i - 1][j], 
    				SPACE_PENALTY + matrix[i][j - 1])

After filling up the matrix we traverse the matrix backwards and output the strings with the greatest score. To do so we start by creating two new strings with empty strings so we can fill them up later. 

make the indexes for i and j equal to the length of the strings - 1 so they are not out of bounds.

While i and j are greater than 0 we go through and traverse the matrix and find the strings to output.

When (s1[i], s2[j]) + matrix[i - 1][j - 1] is equal to the index we output both of the string letters because they are equal. when SPACE_PENALTY + matrix[i][j - 1] is equal to the matrix we answer1 = '_' + answer1 then answer2 = s2[j] + answer2 and finally j -= 1. When SPACE_PENALTY + matrix[i - 1][j] == matrix[i][j] then we do answer1 = s1[i] + answer1 then answer2 = '_' + answer2 and finally i -= 1 because we need to keep moving through the index.

After this while loop we must keep checking to see if one string was larger and then finish it off going either up or to the left by answer1 = s1[i] + answer1 and answer2 = '_' + answer2 then finally i -= 1. If j is greater than 0 though we do answer1 = '_' + answer1 and answer2 = s2[j] + answer2 then finally j -= 1 so we can keep moving through the matrix.

after all of this we return the best strings!