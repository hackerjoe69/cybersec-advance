def generate_nmap_command(choice, target):
    """
    Generate an nmap command based on the user's choice and target.
    """
    nmap_commands = {
        1: f"nmap -sS {target}",  # TCP SYN Scan
        2: f"nmap -sT {target}",  # TCP Connect Scan
        3: f"nmap -sU {target}",  # UDP Scan
        4: f"nmap -O {target}",   # OS Detection
        5: f"nmap -sV {target}",  # Version Detection
        6: f"nmap -A {target}",   # Aggressive Scan
        7: f"nmap -p 1-1000 {target}",  # Port Range Scan
        8: f"nmap -sC -sV {target}",    # Script Scan with Version Detection
        9: f"nmap -Pn {target}",        # No Ping Scan
        10: f"nmap -T4 {target}",        # Timing Template (Aggressive Timing)
    }

    return nmap_commands.get(choice, "Invalid choice")

def main():
    """
    Main function to display the menu and generate the nmap command.
    """
    print("Nmap Command Generator")
    print("======================")
    print("1. TCP SYN Scan")
    print("2. TCP Connect Scan")
    print("3. UDP Scan")
    print("4. OS Detection")
    print("5. Version Detection")
    print("6. Aggressive Scan")
    print("7. Port Range Scan (1-1000)")
    print("8. Script Scan with Version Detection")
    print("9. No Ping Scan")
    print("10. Aggressive Timing Scan (T4)")
    print("======================")

    try:
        # Get user input
        choice = int(input("Enter your choice (1-10): "))
        target = input("Enter the target IP or hostname: ")

        # Generate and display the nmap command
        nmap_command = generate_nmap_command(choice, target)
        if nmap_command == "Invalid choice":
            print("Invalid choice. Please select a number between 1 and 10.")
        else:
            print(f"\nGenerated Nmap Command:\n{nmap_command}\n")

    except ValueError:
        print("Invalid input. Please enter a number.")

if __name__ == "__main__":
    main()