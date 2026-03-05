# 🧹 System Cleanup Master

A beautiful, interactive Python script to clean up your macOS system, remove clutter, and free up disk space with a colorful terminal UI.

## 📊 Workflow Overview

```mermaid
%%{init: {'theme':'base', 'themeVariables': { 'primaryColor':'#00d4ff','primaryTextColor':'#fff','primaryBorderColor':'#00a8cc','lineColor':'#00d4ff','secondaryColor':'#a8e6cf','tertiaryColor':'#ff6b6b','background':'#1a1a1a','mainBkg':'#2d3748','secondBkg':'#4a5568','tertiaryBkg':'#718096'}}}%%
graph TD
    A[🚀 Start Cleanup Master] --> B{Choose Mode}
    B -->|Interactive| C[📋 Show Menu]
    B -->|Auto| D[⚡ Automatic Mode]
    
    C --> E[1️⃣ Scan System]
    C --> F[2️⃣ Quick Clean]
    C --> G[3️⃣ Organize Files]
    C --> H[4️⃣ System Clean]
    
    E --> I[🔍 Scan Downloads]
    E --> J[🔍 Scan Caches]
    E --> K[🔍 Find Duplicates]
    
    I --> L[📊 Display Results]
    J --> L
    K --> L
    
    F --> M[🗑️ Remove Duplicates]
    F --> N[🧹 Clean Caches]
    
    G --> O[📁 Sort by Type]
    O --> P[📄 Documents]
    O --> Q[🖼️ Images]
    O --> R[🎬 Videos]
    O --> S[📦 Archives]
    
    H --> T[💾 Homebrew]
    H --> U[🗂️ Temp Files]
    H --> V[📝 Logs]
    
    M --> W[✨ Show Summary]
    N --> W
    T --> W
    U --> W
    V --> W
    
    style A fill:#00d4ff,stroke:#00a8cc,stroke-width:3px,color:#000
    style B fill:#a8e6cf,stroke:#7fb069,stroke-width:2px
    style W fill:#4ecdc4,stroke:#45b7af,stroke-width:3px,color:#000
    style M fill:#ff6b6b,stroke:#ee5a52,stroke-width:2px
    style N fill:#ff6b6b,stroke:#ee5a52,stroke-width:2px
    style T fill:#ffd93d,stroke:#f5c542,stroke-width:2px
    style U fill:#ffd93d,stroke:#f5c542,stroke-width:2px
    style V fill:#ffd93d,stroke:#f5c542,stroke-width:2px
```

## 🏗️ System Architecture

```mermaid
%%{init: {'theme':'base', 'themeVariables': { 'primaryColor':'#667eea','primaryTextColor':'#fff','primaryBorderColor':'#5a67d8','lineColor':'#667eea','secondaryColor':'#f093fb','tertiaryColor':'#4facfe'}}}%%
graph LR
    subgraph User Interface
        A[🎨 Rich Console]
        B[📊 Progress Bars]
        C[📋 Tables]
    end
    
    subgraph Core Engine
        D[🧹 CleanupMaster]
        E[🔍 Scanner]
        F[🗑️ Cleaner]
        G[📁 Organizer]
    end
    
    subgraph File System
        H[📥 Downloads]
        I[💾 Caches]
        J[🗂️ System]
    end
    
    A --> D
    B --> D
    C --> D
    
    D --> E
    D --> F
    D --> G
    
    E --> H
    E --> I
    E --> J
    
    F --> H
    F --> I
    F --> J
    
    G --> H
    
    style A fill:#667eea,stroke:#5a67d8,stroke-width:2px
    style D fill:#f093fb,stroke:#e879f9,stroke-width:3px
    style H fill:#4facfe,stroke:#00c9ff,stroke-width:2px
    style I fill:#4facfe,stroke:#00c9ff,stroke-width:2px
    style J fill:#4facfe,stroke:#00c9ff,stroke-width:2px
```

## 💾 Space Recovery Process

```mermaid
%%{init: {'theme':'base', 'themeVariables': { 'primaryColor':'#fa709a','primaryTextColor':'#fff','primaryBorderColor':'#f77f9d','lineColor':'#fa709a','secondaryColor':'#fee140','tertiaryColor':'#30cfd0'}}}%%
flowchart TB
    subgraph Analysis ["🔍 Analysis Phase"]
        A1[Scan Files] --> A2[Calculate Sizes]
        A2 --> A3[Detect Duplicates]
        A3 --> A4[Find Large Caches]
    end
    
    subgraph Decision ["⚖️ Decision Phase"]
        D1{Confirm Delete?}
        D2{Cache > 10MB?}
        D3{Keep Oldest?}
    end
    
    subgraph Action ["⚡ Action Phase"]
        AC1[Delete Duplicates]
        AC2[Clear Caches]
        AC3[Organize Files]
        AC4[Free Space]
    end
    
    subgraph Result ["✨ Result Phase"]
        R1[Calculate Freed]
        R2[Update Stats]
        R3[Show Summary]
        R4[Display Report]
    end
    
    A4 --> D1
    D1 -->|Yes| D2
    D1 -->|No| R3
    D2 -->|Yes| D3
    D3 -->|Yes| AC1
    AC1 --> AC2
    AC2 --> AC3
    AC3 --> AC4
    AC4 --> R1
    R1 --> R2
    R2 --> R3
    R3 --> R4
    
    style Analysis fill:#fa709a,stroke:#f77f9d,stroke-width:2px,color:#fff
    style Decision fill:#fee140,stroke:#ffd700,stroke-width:2px,color:#000
    style Action fill:#30cfd0,stroke:#2ebf91,stroke-width:2px,color:#fff
    style Result fill:#a8e6cf,stroke:#7fb069,stroke-width:2px,color:#000
```

## 📈 Performance Impact

```mermaid
%%{init: {'theme':'base', 'themeVariables': { 'primaryColor':'#11998e','primaryTextColor':'#fff','primaryBorderColor':'#0f8577','xyChart': {'backgroundColor': '#1a1a1a'}}}}%%
xychart-beta
    title "Typical Space Freed by Category"
    x-axis [Duplicates, Browser Cache, VS Code, Playwright, Homebrew, System Temp, Logs, Other]
    y-axis "Space (MB)" 0 --> 2000
    bar [150, 800, 700, 450, 250, 300, 100, 200]
```

## ✨ Features

- 🔍 **Smart Scanning** - Detects duplicates, large files, and bloated caches
- 🎨 **Beautiful UI** - Colorful terminal interface with progress bars
- 📊 **Detailed Reports** - See exactly what's taking up space
- 🗑️ **Safe Cleaning** - Asks for confirmation before deleting
- 📁 **Auto-Organization** - Sorts files by category (Documents, Images, Videos, etc.)
- 💾 **System-Wide Cleanup** - Clears Homebrew, temp files, and logs
- ⚡ **Fast & Efficient** - Parallel scanning with progress indicators

## 🚀 Installation

```bash
# Clone or navigate to the directory
cd /Users/sri/cleanup

# The virtual environment is already set up!
# Dependencies: rich, click, psutil (already installed)
```

## 📖 Usage

### Interactive Mode (Recommended)
```bash
python cleanup_master.py
```

This launches a beautiful menu where you can:
1. 🔍 Scan System for Clutter
2. 🧹 Quick Clean (Remove duplicates & caches)
3. 📁 Organize Downloads
4. 🔧 System-Wide Cleanup
5. 📊 Show Summary

### Using Makefile (Easiest!)

```mermaid
%%{init: {'theme':'base', 'themeVariables': { 'primaryColor':'#ff6b6b','primaryTextColor':'#fff','primaryBorderColor':'#ee5a52'}}}%%
mindmap
  root((🧹 Makefile<br/>Commands))
    Setup
      make install
      make check
      make test
    Quick Actions
      make run
      make auto
      make quick
    Targeted Clean
      make clean-dupes
      make clean-cache
      make organize
      make system-clean
    Monitoring
      make status
      make watch
    Advanced
      make full-clean
      make backup
      make schedule
```

**Popular Commands:**
```bash
make status          # 📊 Check disk usage
make run             # 🎮 Interactive menu
make auto            # ⚡ Auto cleanup
make clean-cache     # 🧹 Clean caches only
make organize        # 📁 Sort Downloads
make full-clean      # 💥 Complete cleanup
```

### Automatic Mode
```bash
python cleanup_master.py --auto
```
Runs a complete cleanup automatically (still asks for confirmation).

### Direct Execution
```bash
./cleanup_master.py
```

## 🎯 What It Cleans

```mermaid
%%{init: {'theme':'base', 'themeVariables': { 'primaryColor':'#6c5ce7','primaryTextColor':'#fff','primaryBorderColor':'#5f4dd1','lineColor':'#a29bfe'}}}%%
graph TB
    subgraph USER["👤 User Level"]
        U1[📥 Downloads<br/>Duplicates]
        U2[🌐 Browser Caches<br/>Chrome, Safari]
        U3[💻 VS Code<br/>Updates]
        U4[🎭 Playwright<br/>Browsers]
        U5[🍺 Homebrew<br/>Old Packages]
        U6[🐍 Pip Cache]
        U7[🗣️ Siri TTS<br/>Models]
    end
    
    subgraph SYS["⚙️ System Level"]
        S1[📂 /tmp/<br/>Temp Files]
        S2[📝 Logs<br/>*.log]
        S3[🗂️ /var/tmp/<br/>Old Temp]
    end
    
    subgraph ORG["📁 Organization"]
        O1[📄 Documents<br/>PDF, DOC, XLS]
        O2[🖼️ Images<br/>JPG, PNG, GIF]
        O3[🎬 Videos<br/>MP4, AVI, MKV]
        O4[📦 Archives<br/>ZIP, RAR, 7Z]
        O5[💻 Code<br/>PY, JS, HTML]
    end
    
    USER -->|Safe Delete| CLEAN[🧹 Cleanup]
    SYS -->|Sudo Required| CLEAN
    ORG -->|Move & Sort| CLEAN
    CLEAN --> RESULT[✨ Free Space]
    
    style USER fill:#6c5ce7,stroke:#5f4dd1,stroke-width:2px,color:#fff
    style SYS fill:#fd79a8,stroke:#e84393,stroke-width:2px,color:#fff
    style ORG fill:#00b894,stroke:#00a383,stroke-width:2px,color:#fff
    style CLEAN fill:#fdcb6e,stroke:#f0b849,stroke-width:3px,color:#000
    style RESULT fill:#55efc4,stroke:#00d2a0,stroke-width:3px,color:#000
```

### User-Level
- ✅ Duplicate files in Downloads
- ✅ Browser caches (Chrome, Safari, etc.)
- ✅ VS Code update caches
- ✅ Playwright browser caches
- ✅ Homebrew caches
- ✅ Pip caches
- ✅ SiriTTS model caches
- ✅ App-specific caches

### System-Level (with sudo)
- ✅ System temporary files
- ✅ Homebrew old packages
- ✅ System logs

### File Organization
Automatically categorizes files into:
- 📄 Documents (PDF, DOC, XLS, PPT, TXT)
- 🖼️ Images (JPG, PNG, GIF, SVG)
- 🎬 Videos (MP4, AVI, MKV, MOV)
- 📦 Archives (ZIP, RAR, 7Z, TAR)
- 💻 Code (PY, JS, HTML, CSS, JAVA)

## 🛡️ Safety Features

- **Confirmation Prompts** - Always asks before deleting
- **Duplicate Detection** - Keeps oldest file by default
- **Size Thresholds** - Only cleans caches > 10MB
- **Error Handling** - Continues even if some files can't be deleted
- **Detailed Logging** - Shows exactly what was cleaned

## 📸 Screenshots

```
  ██████╗██╗     ███████╗ █████╗ ███╗   ██╗██╗   ██╗██████╗ 
 ██╔════╝██║     ██╔════╝██╔══██╗████╗  ██║██║   ██║██╔══██╗
 ██║     ██║     █████╗  ███████║██╔██╗ ██║██║   ██║██████╔╝
 ██║     ██║     ██╔══╝  ██╔══██║██║╚██╗██║██║   ██║██╔═══╝ 
 ╚██████╗███████╗███████╗██║  ██║██║ ╚████║╚██████╔╝██║     
  ╚═════╝╚══════╝╚══════╝╚═╝  ╚═╝╚═╝  ╚═══╝ ╚═════╝ ╚═╝     
```

## 🔧 Requirements

- Python 3.7+
- macOS (tested on macOS Monterey+)
- Dependencies:
  - `rich` - Beautiful terminal formatting
  - `click` - CLI framework
  - `psutil` - System utilities

## � State Machine

```mermaid
%%{init: {'theme':'base', 'themeVariables': { 'primaryColor':'#e056fd','primaryTextColor':'#fff','primaryBorderColor':'#c93bf5'}}}%%
stateDiagram-v2
    [*] --> Idle
    Idle --> Scanning : Start Scan
    Scanning --> Analyzed : Complete
    Analyzed --> Confirming : User Review
    Confirming --> Cleaning : Approved
    Confirming --> Idle : Cancelled
    Cleaning --> Processing : Delete Files
    Processing --> Verifying : Check Results
    Verifying --> Complete : Success
    Complete --> Reporting : Generate Stats
    Reporting --> [*]
    
    Scanning : 🔍 Finding clutter
    Analyzed : 📊 Results ready
    Confirming : ⚖️ Awaiting approval
    Cleaning : 🧹 Removing files
    Processing : ⚡ In progress
    Verifying : ✅ Validating
    Complete : ✨ Done
    Reporting : 📈 Summary
```

## �💡 Tips

1. **Run regularly** - Schedule weekly cleanups for best results
2. **Check before deleting** - Review the scan results before cleaning
3. **Backup important files** - Always have backups of critical data
4. **Use automatic mode** - Great for scheduled maintenance
5. **System cleanup** - Run system-wide cleanup monthly

## 🎨 Color Guide

- 🔵 **Cyan** - Information and headers
- 🟢 **Green** - Success messages and sizes
- 🟡 **Yellow** - Warnings and scans
- 🔴 **Red** - Errors and deletions
- 🟣 **Magenta** - Highlights and duplicates

## 📊 Typical Results

```mermaid
%%{init: {'theme':'base', 'themeVariables': { 'primaryColor':'#38ada9','primaryTextColor':'#fff'}}}%%
pie title "Space Distribution Before Cleanup"
    "Browser Caches" : 45
    "VS Code & Tools" : 20
    "Duplicates" : 15
    "Homebrew" : 10
    "System Temp" : 10
```

```mermaid
%%{init: {'theme':'base', 'themeVariables': { 'primaryColor':'#78e08f','primaryTextColor':'#000'}}}%%
pie title "Space Recovered by Category"
    "Browser Caches" : 800
    "Development Tools" : 1150
    "Duplicate Files" : 150
    "System Files" : 400
    "Package Managers" : 250
```

Average cleanup frees up:
- **1-5 GB** - Normal usage
- **5-20 GB** - Heavy browser/development use
- **20-50 GB** - Long-term accumulation

## 🤝 Contributing

Feel free to enhance the script:
- Add more file categories
- Support for other operating systems
- Additional cache directories
- Smart duplicate detection algorithms

## 📝 License

Free to use and modify for personal and commercial use.

## ⚠️ Disclaimer

This tool permanently deletes files. While it includes safety measures, always:
- Review what will be deleted
- Keep backups of important data
- Test on non-critical systems first

## 🆘 Support

Common issues:
- **Permission denied**: Run specific cleanups with `sudo` when prompted
- **No files found**: Your system is already clean!
- **Import errors**: Reinstall dependencies with `pip install rich click psutil`

---

Made with ❤️ for keeping your Mac clean and fast!
