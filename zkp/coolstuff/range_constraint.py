def get_bit(n, idx):
    if n.bit_length() <= idx:
        return 0
    
    return bin(n)[2:][::-1][idx]

def range_constraint(target, num_bits):
    variables = []
    accumulators = []

    assert num_bits > 0

    num_quads = (num_bits >> 1) + (num_bits & 1) # ????

    four = 4
    accumulator = 0 
    accumulator_idx = 0

    for i in range(num_quads - 1, -1, -1):
        print(i)
        lo = get_bit(target, 2 * i)

        variables.append(int(lo))
        lo_idx = len(variables)-1

        assert variables[lo_idx] * variables[lo_idx] - variables[lo_idx] == 0

        if i == num_quads - 1 and num_bits & 1 == 1:
            quad_idx = lo_idx
        else:
            hi = get_bit(target, 2 * i + 1)
            variables.append(int(hi))
            hi_idx = len(variables) - 1
            
            assert variables[hi_idx] * variables[hi_idx] - variables[hi_idx] == 0
            quad = variables[lo_idx] + 2 * variables[hi_idx]
            variables.append(quad)
            quad_idx = len(variables) - 1


        if i == num_quads - 1:
            accumulators.append(quad_idx)
            accumulator = variables[quad_idx]
            accumulator_idx = quad_idx
        else:
            new_accumulator = accumulator + accumulator;
            new_accumulator = new_accumulator + new_accumulator;
            new_accumulator = new_accumulator + variables[quad_idx]
            variables.append(new_accumulator)
            new_accumulator_idx = len(variables) - 1

            assert 4 * variables[accumulator_idx] + variables[quad_idx] - variables[new_accumulator_idx] == 0
            accumulators.append(new_accumulator_idx)
            accumulator = new_accumulator
            accumulator_idx = new_accumulator_idx
    assert target == variables[accumulator_idx]
    return accumulators


range_constraint(2048, 11)
