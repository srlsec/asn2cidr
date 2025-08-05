import subprocess
import re
import argparse

def get_cidrs_from_asn(asn):
    try:
        # Run the Nmap NSE script for ASN
        result = subprocess.run(
            ['nmap', '--script', 'targets-asn', f'--script-args=targets-asn.asn={asn}'],
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True
        )

        if result.returncode != 0:
            print("Nmap Error:", result.stderr)
            return []

        # Regex to extract IP/CIDR
        cidrs = re.findall(r'[0-9]{1,3}(?:\.[0-9]{1,3}){3}/[0-9]{1,2}', result.stdout)
        unique_cidrs = sorted(set(cidrs))
        return unique_cidrs

    except FileNotFoundError:
        print("Nmap is not installed or not in PATH.")
        return []

def main():
    # Set up argument parser
    parser = argparse.ArgumentParser(description='Retrieve CIDR ranges for a given ASN using Nmap.')
    parser.add_argument('--asn', type=str, required=True, help='Autonomous System Number (e.g., 33353 or AS33353)')
    args = parser.parse_args()

    # Clean the ASN input (remove "AS" prefix if present)
    asn_input = args.asn.upper().strip()
    if asn_input.startswith("AS"):
        asn_number = asn_input[2:]  # Remove "AS" prefix
    else:
        asn_number = asn_input

    # Validate that the remaining input is numeric
    if not asn_number.isdigit():
        print("Error: ASN must be a number (e.g., 33353 or AS33353).")
        return

    # Get CIDRs
    cidr_list = get_cidrs_from_asn(asn_number)
    if not cidr_list:
        print(f"No CIDR ranges found for AS{asn_number}.")
        return

    # Save to file
    output_file = f"AS{asn_number}.txt"
    with open(output_file, 'w') as f:
        f.write("\n".join(cidr_list))
    
    print(f"CIDR ranges saved to {output_file}")
    print(f"Total CIDRs found: {len(cidr_list)}")

if __name__ == "__main__":
    main()