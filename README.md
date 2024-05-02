### Multi-Threading Python Project
You are tasked with creating a Python program capable of executing the first 100 steps of a modified cellular life simulator. 
This simulator will receive the path to the input file as an argument containing the starting cellular matrix.  
The program must then simulate the next 100 time-steps based on the algorithm discussed on the next few pages. 
The simulation is guided by a handful of simplistic rules that will result in a seemingly complex simulation of cellular organisms. 

### Command Line Arguments
Develop a program capable of accepting the following command line arguments:
• -i <path_to_input_file> 
      o Purpose: This option retrieves the file path to the starting cellular matrix.
      o Input Type: String
      o Validation:  Entire file path must exist, otherwise error.
      o Required: Yes

• -o <path_to_output_file> 
      o Purpose: This option retrieves the file path for the final output file.
      o Input Type: String 
      o Validation: The directories in the file path must exist, otherwise error.
      o Required: Yes
• -p <int> 
      o Purpose: This option retrieves the number of processes to spawn.
      o Input Type: Unsigned Integer
      o Validation: Must be a positive integer > 0, otherwise error.
      o Required: No
      o Default Value: 1 

### Authors
[Wesley Spangler](https://github.com/InfiniteWes)
