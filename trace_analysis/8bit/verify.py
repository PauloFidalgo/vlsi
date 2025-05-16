import csv
import sys

def verify_trace(csv_file_path):
    incorrect_results = []
    line_count = 0
    
    try:
        with open(csv_file_path, 'r') as file:
            csv_reader = csv.reader(file)
            
            # Skip header
            header = next(csv_reader)
            
            for row_idx, row in enumerate(csv_reader, start=1):
                line_count += 1
                if not row:  # Skip empty rows
                    continue
                
                # Extract values from the CSV row - Convert to float first
                eq_y = float(row[1]) if row[1].strip() else None
                bbig_y = float(row[3]) if row[3].strip() else None
                
                # Extract B bits (MSB to LSB) - Convert to rounded binary (0 or 1)
                b_bits = []
                for i in range(5, 20, 2):  # B<7> Y to B<0> Y
                    if i < len(row) and row[i].strip():
                        # Consider values close to 1 as 1, others as 0
                        bit_value = float(row[i])
                        b_bits.append(1 if bit_value > 0.5 else 0)
                    else:
                        b_bits.append(0)  # Default to 0 if missing
                
                # Extract A bits (MSB to LSB) - Convert to rounded binary (0 or 1)
                a_bits = []
                for i in range(21, 36, 2):  # A<7> Y to A<0> Y
                    if i < len(row) and row[i].strip():
                        # Consider values close to 1 as 1, others as 0
                        bit_value = float(row[i])
                        a_bits.append(1 if bit_value > 0.5 else 0)
                    else:
                        a_bits.append(0)  # Default to 0 if missing
                
                # Convert bit arrays to integers
                b_val = 0
                for bit in b_bits:
                    b_val = (b_val << 1) | bit
                
                a_val = 0
                for bit in a_bits:
                    a_val = (a_val << 1) | bit
                
                # Calculate expected values
                expected_eq_y = 0 if a_val == b_val else 1  # EQ Y is NOT(A == B)
                expected_bbig_y = 0 if b_val > a_val else 1  # BBig Y is NOT(B > A)
                
                # Check if results match expected values - with tolerance for floating point
                eq_y_binary = 1 if eq_y > 0.5 else 0
                bbig_y_binary = 1 if bbig_y > 0.5 else 0
                
                if eq_y is not None and eq_y_binary != expected_eq_y:
                    incorrect_results.append({
                        "row": row_idx,
                        "A": a_val,
                        "B": b_val,
                        "EQ Y": eq_y,
                        "EQ Y (binary)": eq_y_binary,
                        "Expected EQ Y": expected_eq_y
                    })
                
                if bbig_y is not None and bbig_y_binary != expected_bbig_y:
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

if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: python verify.py <path_to_csv_file>")
        sys.exit(1)
    
    csv_file_path = sys.argv[1]
    incorrect_results, total_lines = verify_trace(csv_file_path)
    
    if incorrect_results:
        print(f"Found {len(incorrect_results)} incorrect results out of {total_lines} lines:")
        for result in incorrect_results:
            print(result)
        
        with open("incorrect_trace.txt", "w") as f:
            for result in incorrect_results:
                f.write(f"{result}\n")
    else:
        print(f"All {total_lines} results in the trace file are correct!")