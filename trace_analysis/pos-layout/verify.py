import csv
import sys

def verify_trace(csv_file_path):
    incorrect_results = []
    line_count = 0
    
    try:
        with open(csv_file_path, 'r') as file:
            csv_reader = csv.reader(file, delimiter='\t')  # Using tab delimiter based on header format
            
            # Skip header
            header = next(csv_reader)
            
            for row_idx, row in enumerate(csv_reader, start=1):
                line_count += 1
                if not row or len(row) < 4:  # Skip empty rows or rows without enough data
                    continue
                
                # Extract values from the CSV row - Convert to float first
                bbig_y = float(row[1]) if row[1].strip() else None  # /BBig Y is at index 1
                eq_y = float(row[3]) if row[3].strip() else None    # /EQ Y is at index 3
                
                # Extract A bits (MSB to LSB) - Convert to rounded binary (0 or 1)
                a_bits = []
                for i in range(5, 5 + 64*2, 2):  # A<63> Y to A<0> Y (only Y values)
                    if i < len(row) and row[i].strip():
                        bit_value = float(row[i])
                        a_bits.append(1 if bit_value > 0.5 else 0)
                    else:
                        a_bits.append(0)  # Default to 0 if missing
                
                # Extract B bits (MSB to LSB) - Convert to rounded binary (0 or 1)
                b_bits = []
                for i in range(5 + 64*2, 5 + 64*2 + 64*2, 2):  # B<63> Y to B<0> Y (only Y values)
                    if i < len(row) and row[i].strip():
                        bit_value = float(row[i])
                        b_bits.append(1 if bit_value > 0.5 else 0)
                    else:
                        b_bits.append(0)  # Default to 0 if missing
                
                # Convert bit arrays to integers (need to handle 64-bit integers carefully)
                a_val = 0
                for bit in a_bits:
                    a_val = (a_val << 1) | bit
                
                b_val = 0
                for bit in b_bits:
                    b_val = (b_val << 1) | bit
                
                # Calculate expected values
                expected_eq_y = 1 if a_val == b_val else 0  # EQ Y is (A == B)
                expected_bbig_y = 1 if b_val > a_val else 0  # BBig Y is (B > A)
                
                # Check if results match expected values - with tolerance for floating point
                if eq_y is not None:
                    eq_y_binary = 1 if eq_y > 0.5 else 0
                    if eq_y_binary != expected_eq_y:
                        incorrect_results.append({
                            "row": row_idx,
                            "A": a_val,
                            "B": b_val,
                            "EQ Y": eq_y,
                            "EQ Y (binary)": eq_y_binary,
                            "Expected EQ Y": expected_eq_y
                        })
                
                if bbig_y is not None:
                    bbig_y_binary = 1 if bbig_y > 0.5 else 0
                    if bbig_y_binary != expected_bbig_y:
                        incorrect_results.append({
                            "row": row_idx,
                            "A": a_val,
                            "B": b_val,
                            "BBig Y": bbig_y,
                            "BBig Y (binary)": bbig_y_binary,
                            "Expected BBig Y": expected_bbig_y
                        })
                    
        return incorrect_results, line_count
    
    except Exception as e:
        print(f"Error processing file: {e}")
        import traceback
        traceback.print_exc()
        return [], line_count

def print_binary_representation(value, bits=64):
    """Helper function to print the binary representation of a large value"""
    return bin(value)[2:].zfill(bits)

if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: python verify_trace_64bit.py <path_to_csv_file>")
        sys.exit(1)

    csv_file_path = sys.argv[1]
    incorrect_results, total_lines = verify_trace(csv_file_path)

    if incorrect_results:
        print(f"Found {len(incorrect_results)} incorrect results out of {total_lines} lines:")
        """
        for result in incorrect_results:
            print(f"Row {result['row']}: A={result['A']} B={result['B']}")
            print(f"  A (binary): {print_binary_representation(result['A'])}")
            print(f"  B (binary): {print_binary_representation(result['B'])}")

            if 'EQ Y' in result:
                print(f"  EQ Y: {result['EQ Y']} (binary: {result['EQ Y (binary)']}, Expected: {result['Expected EQ Y']})")
            if 'BBig Y' in result:
                print(f"  BBig Y: {result['BBig Y']} (binary: {result['BBig Y (binary)']}, Expected: {result['Expected BBig Y']})")
            print()
        """
        with open("incorrect_trace.txt", "w") as f:
            for result in incorrect_results:
                f.write(f"Row {result['row']}: A={result['A']} B={result['B']}\n")
                f.write(f"  A (binary): {print_binary_representation(result['A'])}\n")
                f.write(f"  B (binary): {print_binary_representation(result['B'])}\n")

                if 'EQ Y' in result:
                    f.write(f"  EQ Y: {result['EQ Y']} (binary: {result['EQ Y (binary)']}, Expected: {result['Expected EQ Y']})\n")
                if 'BBig Y' in result:
                    f.write(f"  BBig Y: {result['BBig Y']} (binary: {result['BBig Y (binary)']}, Expected: {result['Expected BBig Y']})\n")
                f.write("\n")
    else:
        print(f"All {total_lines} results in the trace file are correct!")
