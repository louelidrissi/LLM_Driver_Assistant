def keep_n_rows_from_jsonl(input_file, output_file, n):
    with open(input_file, 'r', encoding='utf-8') as infile, open(output_file, 'w', encoding='utf-8') as outfile:
        for i, line in enumerate(infile):
            if i >= n:
                break
            outfile.write(line)


inputfile = "testing_input_advice.jsonl"
# Example usage: keep only the first 10 rows
keep_n_rows_from_jsonl(inputfile, 'output.jsonl', 3008 )
