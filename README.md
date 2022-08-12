# ansible-workstation

## Linux Setup

1. Install ansible dependencies:

   ```bash
   sudo apt-get update
   sudo apt-get install -y python3-pip git libffi-dev libssl-dev ssh
   pip install --user ansible pywinrm
   ```

2. Run the playbook

   ```bash
   ansible-playbook \
       --connection=local \
       --inventory=hosts \
       --limit=127.0.0.1
       nix.yml
   ```

Test connectivity in WSL:

```bash
ansible windows -m win_ping
```

Install dependencies:

```bash
# Install galaxy roles
ansible-galaxy install -r requirements.yml

# Install collections
ansible-galaxy collection install -r requirements.yml

# Run nix playbook
ansible-playbook nix.yml

# Run windows playbook
ansible-playbook windows.yml
```

---

---

## Windows Setup

```pwsh
# Setup WinRM
winrm quickconfig
[Net.ServicePointManager]::SecurityProtocol = [Net.SecurityProtocolType]::Tls12
$url = "https://raw.githubusercontent.com/ansible/ansible/devel/examples/scripts/ConfigureRemotingForAnsible.ps1"
$file = "$env:temp\ConfigureRemotingForAnsible.ps1"

(New-Object -TypeName System.Net.WebClient).DownloadFile($url, $file)

powershell.exe -ExecutionPolicy ByPass -File $file

# Create WinRM listener:
$selector_set = @{
    Address = "*"
    Transport = "HTTP"
}

New-WSManInstance -ResourceURI "winrm/config/Listener" `
-SelectorSet $selector_set

# Show listeners
winrm enumerate winrm/config/Listener

# Enable PS Remoting
Enable-PSRemoting -SkipNetworkProfileCheck -Force

# Add host to the system's trusted hosts list:
winrm set winrm/config/client '@{TrustedHosts="orbitty"}'

# Create new local ansible user
### BE SURE TO CHANGE THE PASSWORD FROM changeme ###

New-LocalUser -AccountNeverExpires:$true `
-Password ( ConvertTo-SecureString -AsPlainText -Force 'changeme') `
-Name 'ansible' | Add-LocalGroupMember -Group Administrators

# Test connectivity with new user
$s = New-PSSession -ComputerName "orbitty" -Credential(Get-Credential)
Enter-PSSession -Session $s
```

---

## Package Instructions

### Keeper

```pwsh
cd $HOME/AppData/Local/keeperpasswordmanager
.\keeperpasswordmanager.exe
```

---

## Access Windows System Remotely

Change `hosts`:

```yaml
[windows]
orbitty

[windows:vars]
ansible_ssh_host=orbitty
ansible_user=ansible
ansible_password=changeme
ansible_connection=winrm
ansible_winrm_transport=ntlm
ansible_port=5985
```

Run this if you're on a mac ([see this for more info](https://github.com/ansible/ansible/issues/32499https://github.com/ansible/ansible/issues/32499)):

```bash
export OBJC_DISABLE_INITIALIZE_FORK_SAFETY=YES
```

---

## Resources

[Set up Windows Host](https://docs.ansible.com/ansible/latest/user_guide/windows_setup.html)
[Enable remote connectivity with Powershell](<https://docs.microsoft.com/en-us/previous-versions/technet-magazine/ff700227(v=msdn.10)?redirectedfrom=MSDN>)
[Ansible User Guide](https://docs.ansible.com/ansible/latest/user_guide/windows_faq.html#:~:text=The%20Windows%20Subsystem%20for%20Linux%20is%20not%20supported%20by%20Ansible,be%20used%20for%20production%20systems.&text=To%20run%20Ansible%20from%20source,then%20clone%20the%20git%20repo.&text=Another%20option%20is%20to%20use,10%20later%20than%20build%202004.j)
