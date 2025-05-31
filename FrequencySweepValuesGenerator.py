import numpy as np

# Takes two ints power0 and power1
# Returns an array of frequencies that sweep from 10^power0 to 10^power1 with a 
# given number of points in between 
def frequencySweepValues(power0, power1, points):
    # Set up result array
    result = np.empty(0)

    # Add values for each decade and for the final value
    for i in range(power0, power1):
        result = np.append(result, np.linspace(10**i, 10**(i + 1), points)[:-1])
    result = np.append(result, 10**power1)

    # Return result
    return result

# Generate values
vals = frequencySweepValues(-2, 2, 10)
print(vals)
