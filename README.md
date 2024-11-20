# G1-Config

G1-Config is a project by Ginger for configuring the G1 3D printer. This guide will help you install and update all necessary components to ensure your 3D printer operates at its best.

## Installation Guide

### Requirements
- G1 3D Printer
- Access to the printer's local network
- An SSH client (such as PuTTY)
- A GitHub account

### Instructions

1. **Find the correct printer IP address**
   - Use the Mainsail software to find the IP address of your G1 printer.
   - Access Mainsail through your browser by entering the printer's IP address.

2. **Log in to the machine page**
   - Once logged into Mainsail, go to the machine page to manage the printer's settings and updates.

3. **Update all components**
   - On the machine page, locate the refresh button in the update manager and click the "Refresh" button to ensure all components are updated to the latest version.

4. **Log in with SSH**
   - Use an SSH client like PuTTY to log in to your printer. You will need the printer's IP address and login credentials.

5. **Clone the G1-Configs project**
   - After logging in via SSH, run the following commands to clone the G1-Configs project and start the installation script:
     ```sh
     cd ~
     git clone https://github.com/gingeradditive/G1-Configs.git
     sh ./G1-Configs/legacy-install.sh 2>&1 | tee output.txt
     ```

### Notes
- **Backup:** It is always a good idea to back up your current configurations before performing updates or changes.
- **Support:** If you encounter any issues during the installation, contact Ginger's technical support.

## License
This project is released under the MIT license. For more details, see the LICENSE file.

## Contact
For more information, visit our [website](https://gingeradditive.com) or contact us via email at support@gingeradditive.com.

---

We hope you find this guide helpful. Happy printing!
