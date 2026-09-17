# Only draw_menu function is created by Google AI because I dont want to deal with the menu styling
# i made the modules/*
# Author: Sheen Lim

import sys
import os
import time

from itertools import zip_longest
import textwrap

from modules.ssllabs import SslScanner

# Gracefully handle Windows dependencies if needed
if os.name == 'nt':
    try:
        import windows_curses as curses
    except ImportError:
        print("[!] On Windows, please run: pip install windows-curses")
        sys.exit(1)
else:
    import curses

def draw_menu(stdscr):
    # Hide the standard blinking text cursor
    curses.curs_set(0)
    
    # Setup color schemes if terminal supports colors
    if curses.has_colors():
        curses.start_color()
        # Cyan text on black for subtitles/accents
        curses.init_pair(1, curses.COLOR_CYAN, curses.COLOR_BLACK)
        # Highlighted row: White text on a sleek Blue background
        curses.init_pair(2, curses.COLOR_WHITE, curses.COLOR_BLUE)
        # Magenta accent for Title
        curses.init_pair(3, curses.COLOR_MAGENTA, curses.COLOR_BLACK)

    menu_items = [
        "SSL Labs SSL Scanner",
        "Exit"
    ]
    current_row = 0

    while True:
        stdscr.clear()
        height, width = stdscr.getmaxyx()

        title = " Welcome to maSheen-Tools "
        subtitle = "Select the tool you want to run."
        
        title_attr = curses.color_pair(3) | curses.A_BOLD if curses.has_colors() else curses.A_BOLD
        header_attr = curses.color_pair(1) if curses.has_colors() else curses.A_NORMAL
        selected_attr = curses.color_pair(2) | curses.A_BOLD if curses.has_colors() else curses.A_REVERSE

        if height > 12 and width > 50:
            stdscr.attron(header_attr)
            stdscr.border(0)
            stdscr.attroff(header_attr)

        title_x = max(0, (width // 2) - (len(title) // 2))
        subtitle_x = max(0, (width // 2) - (len(subtitle) // 2))
        
        stdscr.addstr(2, title_x, title, title_attr)
        stdscr.addstr(3, subtitle_x, subtitle, header_attr)
        
        if width > len(subtitle) + 10:
            stdscr.addstr(4, (width // 2) - 15, "═" * 30, header_attr)

        start_y = 6
        for idx, item in enumerate(menu_items):
            x = max(0, (width // 2) - 15)
            y = start_y + (idx * 2) 
            
            display_text = f"  {item.ljust(26)}  "

            if idx == current_row:
                stdscr.addstr(y, x, display_text, selected_attr)
            else:
                stdscr.addstr(y, x, display_text, curses.A_NORMAL)

        guide = "Use Arrow Keys to Navigate | Press Enter to Confirm"
        guide_x = max(0, (width // 2) - (len(guide) // 2))
        stdscr.addstr(height - 2, guide_x, guide, curses.A_DIM)

        stdscr.refresh()
        key = stdscr.getch()

        if key == curses.KEY_UP:
            current_row = (current_row - 1) % len(menu_items)
        elif key == curses.KEY_DOWN:
            current_row = (current_row + 1) % len(menu_items)
        elif key in [curses.KEY_ENTER, 10, 13]:
            return menu_items[current_row]

def showScanResult(data):
    headerIpAddress =  "IP Address"
    headerGrade = "Grade Rating"
    headerCertNames = "Cert Common Name"
    headerTlsVersion = "TLS Version"

    w_ip = 15
    w_grade = 12
    w_cert = 30
    w_tls = 15 

    print(f"{headerIpAddress:<{w_ip}} | {headerGrade:<{w_grade}} | {headerCertNames:<{w_cert}} | {headerTlsVersion:<{w_tls}}")
    for endpoint in data["endpoints"]:
        certDetails = endpoint["details"]["cert"]
        cert_common_names = certDetails["commonNames"][0]

        for altName in certDetails["altNames"]:
            cert_common_names += f", {altName}"

        # if len(cert_common_names) >=18:
        #     cert_common_names = f"{cert_common_names[0:18]}..."

        tlsVersion = ""
        for index, protocol in enumerate(endpoint["details"]["protocols"]):
            if index == 0:
                tlsVersion = f"{protocol["name"]} {protocol["version"]}"
            else:
                tlsVersion += f", {protocol["name"]} {protocol["version"]}"

        # if (len(tlsVersion) >= 28):
        #     tlsVersion = f"{tlsVersion[0:28]}..."

        # print(f"{endpoint["ipAddress"]:<15} | {endpoint["grade"]:<12} | {cert_common_names:<30} | {tlsVersion:<10}")

        cert_lines = textwrap.wrap(cert_common_names, width=w_cert)
        tls_lines = textwrap.wrap(tlsVersion, width=w_tls)

        zipped_lines = zip_longest(cert_lines, tls_lines, fillvalue="")

        for index, (cert_line, tls_line) in enumerate(zipped_lines):
            current_ip = endpoint["ipAddress"] if index == 0 else ""
            current_grade = endpoint["grade"] if index == 0 else ""
            
            print(f"{current_ip:<{w_ip}} | {current_grade:<{w_grade}} | {cert_line:<{w_cert}} | {tls_line:<{w_tls}}")

def performScanning():
    endpoint = input("Type in the endpiont you want to scan (e.g. vpn.myorg.com): ")

    scanner = SslScanner(endpoint)

    result = scanner.scanStart()
    print("Scan is initiating.")

    still_waiting = True
    if (not result["success"]):
        print(f"Scan failed. {result["message"]}" )
        still_waiting = False

    while (still_waiting):
        if (result["success"]):
            print(f"Scan status: {result["data"]["status"]}")

            if (result["data"]["status"] == "READY"):
                print("Scan is complete, here is the result.")
                showScanResult(result["data"])
                break;

            if (result["data"]["status"] == "IN_PROGRESS"):
                print("Scanning in progress, checking result again in 1 minute.")
                time.sleep(60)

                result = scanner.scanStatus()
                continue

        print("Scanning Failed")
        still_waiting = False        

def main():
    choice = curses.wrapper(draw_menu)
    print(f"\n[+] Executing: {choice}\n")

    match choice:
        case "SSL Labs SSL Scanner":
            performScanning()

if __name__ == "__main__":
    main()
