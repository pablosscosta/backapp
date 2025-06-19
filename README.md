# backapp

Backup automation system over the network for internal IT infrastructure.  
Sistema de automação de backup via rede para infraestrutura interna de TI.

---

## Overview / Visão Geral

**EN:**  
`backapp` is a web-based tool built with Django that facilitates structured backups of critical files from remote machines over the network (SMB access via `\\MACHINE\C$`). It stores backups on a local disk and tracks operations in a historical database.

**PT-BR:**  
`backapp` é uma ferramenta web baseada em Django para facilitar backups organizados de arquivos críticos de máquinas remotas via rede (acesso SMB pelo `\\MÁQUINA\C$`). Armazena os backups localmente e registra as operações em um histórico com base de dados.

---

## Features / Funcionalidades

**EN:**  
- Remote access to `\\MACHINE\C$`  
- Copy `C:\backup` and selected `Users` folders (Desktop, Documents, etc.)  
- Partial `AppData` backup (`Google`, `Mozilla`, `Thunderbird`)  
- Backup history with timestamps and status  
- Web interface (Django) for controlling backups  

**PT-BR:**  
- Acesso remoto a `\\MÁQUINA\C$`  
- Cópia da pasta `C:\backup` e pastas selecionadas dos `Users` (Área de Trabalho, Documentos, etc.)  
- Backup parcial da pasta `AppData` (`Google`, `Mozilla`, `Thunderbird`)  
- Histórico de backups com data, hora e status  
- Interface web (Django) para controle dos backups  

---

## Project Structure / Estrutura do Projeto

```
backapp/
├── backup_app/           # Main Django app
│   ├── models.py         # Models: Machine, BackupRecord, etc.
│   ├── views.py          # Backup logic + pages
│   ├── templates/        # HTML interface (optional)
│   └── urls.py
├── scripts/
│   └── run_backup.py     # Script to execute backups over the network
├── docs/
│   └── vision.md         # (Optional) Extended documentation
├── README.md             # Project overview (this file)
└── manage.py
```
 ---

## Requirements / Requisitos

**EN:**  
- Python 3.9 or higher  
- Django 4.x  
- Windows machine with SMB access  
- Network permissions to access `\\MACHINE\C$`  
- Storage location with enough space to save backups  

**PT-BR:**  
- Python 3.9 ou superior  
- Django 4.x  
- Máquina Windows com acesso SMB  
- Permissões de rede para acessar `\\MÁQUINA\C$`  
- Local de armazenamento com espaço suficiente para salvar os backups  

---

## How to Run / Como Executar

**EN / PT-BR:**

```bash
# Clone the project
git clone https://github.com/pablosscosta/backapp.git
cd backapp

# Create virtual environment
python -m venv venv
venv\Scripts\activate  # (Linux/macOS: source venv/bin/activate)

# Install dependencies
pip install -r requirements.txt

# Apply migrations
python manage.py migrate

# Run the Django development server
python manage.py runserver


---

## In Progress / Em Desenvolvimento

**EN:**  
- Backup execution from web interface  
- Backup history logging  

**PT-BR:**  
- Execução de backup pela interface web  
- Registro histórico dos backups  

---

## Contribution / Contribuição

**EN:**  
Contributions are welcome. Please open an issue or pull request to discuss changes.

**PT-BR:**  
Contribuições são bem-vindas. Abra uma issue ou pull request para discutir alterações.


---

## License / Licença

MIT License – see `LICENSE` file.
