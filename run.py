import subprocess
import time
import sys
import os

def check_and_install_adb():
    try:
        subprocess.run(["adb", "--version"], check=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        print("ADB sudah terinstal.")
    except FileNotFoundError:
        print("ADB tidak ditemukan, mencoba untuk menginstal...")
        if sys.platform.startswith("linux") or "com.termux" in os.environ.get("PREFIX", ""):
            os.system("pkg update && pkg install android-tools -y")
        elif sys.platform == "darwin":
            os.system("brew install android-platform-tools")
        elif sys.platform == "win32":
            print("Silakan unduh dan instal ADB secara manual dari https://developer.android.com/studio/releases/platform-tools")
            sys.exit(1)
        else:
            print("Platform tidak dikenal. Silakan instal ADB secara manual.")
            sys.exit(1)

def run_adb_command(command):
    try:
        result = subprocess.run(f"adb {command}", shell=True, check=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        return result.stdout.decode('utf-8').strip()
    except subprocess.CalledProcessError as e:
        print(f"Error executing command")
        return None

def stop_background_apps():
    packages = [
        "com.android.chrome",
        "com.google.android.googlequicksearchbox",
        "com.android.hotwordenrollment.xgoogle",
        "com.google.android.gms.location.history",
        "com.google.android.apps.maps"
    ]
    for package in packages:
        print(f"Stopping app ...")
        run_adb_command(f"shell am force-stop {package}")

    gps_status = run_adb_command("shell settings get secure location_providers_allowed")
    if gps_status and "gps" in gps_status:
        print("Turn off Loc ...")
        run_adb_command("shell settings put secure location_providers_allowed -gps")

def modify_settings():
    print("Starting...")
    time.sleep(2)
    print("Configuring display settings...")
    time.sleep(1)

    try:
        output = run_adb_command("shell wm size 1179x2556")
        if output:
            print("Settings Screen ...")
        else:
            print("Gagal Setting Screen ...")
    except Exception as e:
        print(f"Error Setting Screen ...")


    try:
        output = run_adb_command("shell wm density 460")
        if output:
            print("Settings Screen PPI ...")
        else:
            print("Gagal Settings Screen PPI ...")
    except Exception as e:
        print(f"Error Settings Screen PPI ...")
    
    print("Program masih berjalan...")
    time.sleep(1)
    print("Melanjutkan menjalankan...")
    time.sleep(0.5)
    print("")

def set_default_density_and_ppi():
    print("Mengembalikan pengaturan default...")
    try:
        output = run_adb_command("shell wm density reset")
        if output:
            print("Densitas tampilan telah dikembalikan ke default.")
        else:
            print("Gagal mengembalikan densitas tampilan ke default.")
    except Exception as e:
        print(f"Error saat mengembalikan densitas tampilan ke default: {e}")
    
    try:
        output = run_adb_command("shell wm size reset")
        if output:
            print("Resolusi tampilan telah dikembalikan ke default.")
        else:
            print("Gagal mengembalikan resolusi tampilan ke default.")
    except Exception as e:
        print(f"Error saat mengembalikan resolusi tampilan ke default: {e}")

def display_info():
    print("""
                                                                                                                   
@@@@@@@   @@@@@@@@  @@@  @@@   @@@@@@   @@@  @@@@@@@   @@@@@@@  @@@  @@@   @@@@@@   @@@  @@@   @@@@@@@@  @@@@@@@@  
@@@@@@@@  @@@@@@@@  @@@@ @@@  @@@@@@@   @@@  @@@@@@@  @@@@@@@@  @@@  @@@  @@@@@@@@  @@@@ @@@  @@@@@@@@@  @@@@@@@@  
@@!  @@@  @@!       @@!@!@@@  !@@       @@!    @@!    !@@       @@!  @@@  @@!  @@@  @@!@!@@@  !@@        @@!       
!@!  @!@  !@!       !@!!@!@!  !@!       !@!    !@!    !@!       !@!  @!@  !@!  @!@  !@!!@!@!  !@!        !@!       
@!@  !@!  @!!!:!    @!@ !!@!  !!@@!!    !!@    @!!    !@!       @!@!@!@!  @!@!@!@!  @!@ !!@!  !@! @!@!@  @!!!:!    
!@!  !!!  !!!!!:    !@!  !!!   !!@!!!   !!!    !!!    !!!       !!!@!!!!  !!!@!!!!  !@!  !!!  !!! !!@!!  !!!!!:    
!!:  !!!  !!:       !!:  !!!       !:!  !!:    !!:    :!!       !!:  !!!  !!:  !!!  !!:  !!!  :!!   !!:  !!:       
:!:  !:!  :!:       :!:  !:!      !:!   :!:    :!:    :!:       :!:  !:!  :!:  !:!  :!:  !:!  :!:   !::  :!:       
 :::: ::   :: ::::   ::   ::  :::: ::    ::     ::     ::: :::  ::   :::  ::   :::   ::   ::   ::: ::::   :: ::::  
:: :  :   : :: ::   ::    :   :: : :    :       :      :: :: :   :   : :   :   : :  ::    :    :: :: :   : :: ::   
                                                                                                                   
    """)
    time.sleep(0.7)
    print("")
    print("author : @rootx ft FxS")
    print("Version : 1.0 ")
    print("Info : this script is made with pyshell, with a function to change the density and hibernate the application in the background,this script we made with love \u2764\uFE0F")
    print("")
    time.sleep(3)

def get_device_ip_and_port():
    ip_address = input("Masukkan IP perangkat: ")
    port = input("Masukkan port perangkat: ")
    return ip_address, port

def connect_device_wirelessly(ip_address, port):
    print(f"Menghubungkan perangkat ke {ip_address}:{port}...")
    run_adb_command(f"connect {ip_address}:{port}")
    time.sleep(2)
    
    devices = run_adb_command("devices")
    if "device" in devices:
        print(f"Perangkat terhubung ke {ip_address}:{port} melalui jaringan nirkabel.")
    else:
        print(f"Gagal menghubungkan perangkat: {devices}")
        sys.exit(1)

def main():
    check_and_install_adb()
    display_info()

    ip_address, port = get_device_ip_and_port()
    connect_device_wirelessly(ip_address, port)

    while True:
        print("\nMenu:")
        print("1. Jalankan Script")
        print("2. Hapus Semua Fungsi File")
        print("3. Keluar")
        choice = input("Pilih opsi (1/2/3): ")

        if choice == '1':
            modify_settings()
            stop_background_apps()
        elif choice == '2':
            set_default_density_and_ppi()
        elif choice == '3':
            print("Keluar dari program...")
            sys.exit(0)
        else:
            print("Pilihan tidak valid, silakan coba lagi.")

if __name__ == "__main__":
    main()
