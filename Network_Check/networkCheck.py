import os
import platform
import subprocess
import datetime

def run_command(command):
    try:
        output = subprocess.check_output(command, shell = True, stderr = subprocess.STDOUT, text=True)
        return output.strip()
    except subprocess.CalledProcessError as e:
        return f"Error : {e.output.strip()}"

def ping_check(target):
    cmd = " ping -n 4" if platform.system() == "Windows" else "ping -c 4"
    return run_command(f"{cmd} {target}")

def traceroute_check(target):
    cmd = "tracert" if platform.system() == "Windows" else "traceroute"
    return run_command(f"{cmd} {target}")

def dnsLookup_check(target):
    return run_command(f"nslookup {target}")

def telnet_check(target, port):
    if platform.system() == "Windows":
        return run_command(f"telnet {target} {port}")
    else:
        return run_command(f"timeout 5 bash -c '</dev/tcp/{target}/{port}' && echo Port Open || echo Port Closed")

def get_log_name(target):
    timestamp = datetime.datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
    return f"logs/{target}_check_{timestamp}.txt"

def network_check(target):
    log_file = get_log_name(target)
    summary = []

    with open(log_file,'w') as log:
        log.write(f"Network Check Results for {target} \n")

        ping_result = ping_check(target)
        log.write("Ping : "+ ping_result+"\n")
        summary.append("Ping : Reachable" if "TTL" in ping_result or "bytes=" in ping_result else "Ping : Failed")
        
        trace_result = traceroute_check(target)
        log.write("TRACEROUTE : " + trace_result + "\n")
        hops = trace_result.count("\n")
        summary.append(f"Traceroute : Completed ({hops} hops)" if hops > 1 else "Traceroute : Failed")

        dns_result = dnsLookup_check(target)
        log.write("DNS LOOKUP : " + dns_result + "\n")
        summary.append("DNS Resolution : Successful" if "Address" in dns_result else "DNS Failed")

        telnet_result = telnet_check(target, 80)
        log.write("TELNET Port 80 : " + telnet_result + "\n")
        summary.append("Telnet Port 80 : Open" if "Connected" in telnet_result or "Port Open" in telnet_result else "Telnet : Closed")

        print(f" Summary for {target}\n")
        for line in summary:
            print(line)
        print(f"For Full log check {log_file}")

if __name__ == "__main__":
    os.makedirs("logs", exist_ok = True)
    target = input("To start Networkcheck, Enter domain or IP : ").strip()
    if target:
        network_check(target)
    else:
        print("Invalid Input")