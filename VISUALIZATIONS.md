# 📊 System Cleanup Master - Visualizations

Complete visual guide to understanding the cleanup process.

## 🎯 Cleanup Decision Tree

```mermaid
%%{init: {'theme':'base', 'themeVariables': { 'primaryColor':'#ff6348','primaryTextColor':'#fff','primaryBorderColor':'#e84118'}}}%%
flowchart TD
    START([🚀 Start]) --> SCAN{Scan Complete?}
    SCAN -->|No| SCANNING[🔍 Scanning...]
    SCANNING --> SCAN
    SCAN -->|Yes| CHECK{Found Items?}
    
    CHECK -->|No| CLEAN_EXIT[✨ System Clean!]
    CHECK -->|Yes| CATEGORIZE[📋 Categorize Items]
    
    CATEGORIZE --> DUP{Duplicates<br/>Found?}
    CATEGORIZE --> CACHE{Large<br/>Caches?}
    CATEGORIZE --> UNORG{Unorganized<br/>Files?}
    
    DUP -->|Yes| DUP_SIZE{Size > 1MB?}
    DUP -->|No| NEXT1[Continue]
    DUP_SIZE -->|Yes| DUP_CONFIRM{Confirm<br/>Delete?}
    DUP_SIZE -->|No| NEXT1
    DUP_CONFIRM -->|Yes| DELETE_DUP[🗑️ Delete]
    DUP_CONFIRM -->|No| SKIP1[Skip]
    
    CACHE -->|Yes| CACHE_SIZE{Size > 10MB?}
    CACHE -->|No| NEXT2[Continue]
    CACHE_SIZE -->|Yes| CACHE_CONFIRM{Confirm<br/>Clean?}
    CACHE_SIZE -->|No| NEXT2
    CACHE_CONFIRM -->|Yes| CLEAN_CACHE[🧹 Clean]
    CACHE_CONFIRM -->|No| SKIP2[Skip]
    
    UNORG -->|Yes| ORG_CONFIRM{Confirm<br/>Organize?}
    UNORG -->|No| NEXT3[Continue]
    ORG_CONFIRM -->|Yes| ORGANIZE[📁 Sort Files]
    ORG_CONFIRM -->|No| SKIP3[Skip]
    
    DELETE_DUP --> STATS
    CLEAN_CACHE --> STATS
    ORGANIZE --> STATS
    SKIP1 --> STATS
    SKIP2 --> STATS
    SKIP3 --> STATS
    NEXT1 --> STATS
    NEXT2 --> STATS
    NEXT3 --> STATS
    
    STATS[📊 Calculate Stats] --> REPORT[📈 Generate Report]
    REPORT --> END([✅ Done])
    CLEAN_EXIT --> END
    
    style START fill:#ff6348,stroke:#e84118,stroke-width:3px
    style END fill:#2ecc71,stroke:#27ae60,stroke-width:3px
    style DELETE_DUP fill:#e74c3c,stroke:#c0392b,stroke-width:2px
    style CLEAN_CACHE fill:#f39c12,stroke:#d68910,stroke-width:2px
    style ORGANIZE fill:#3498db,stroke:#2980b9,stroke-width:2px
    style STATS fill:#9b59b6,stroke:#8e44ad,stroke-width:2px
```

## 🔄 File Processing Pipeline

```mermaid
%%{init: {'theme':'base', 'themeVariables': { 'primaryColor':'#00d2d3','primaryTextColor':'#fff','primaryBorderColor':'#01a3a4'}}}%%
graph LR
    subgraph INPUT["📥 Input"]
        A1[Downloads Folder]
        A2[Cache Directories]
        A3[System Files]
    end
    
    subgraph SCAN["🔍 Scan"]
        B1[Read Metadata]
        B2[Calculate Sizes]
        B3[Hash Files]
    end
    
    subgraph ANALYZE["🧪 Analyze"]
        C1[Group Duplicates]
        C2[Find Large Items]
        C3[Detect Patterns]
    end
    
    subgraph FILTER["⚖️ Filter"]
        D1[Size > Threshold?]
        D2[Safe to Delete?]
        D3[User Confirmed?]
    end
    
    subgraph ACTION["⚡ Action"]
        E1[Delete Files]
        E2[Clear Caches]
        E3[Move Files]
    end
    
    subgraph OUTPUT["✨ Output"]
        F1[Freed Space]
        F2[Statistics]
        F3[Report]
    end
    
    A1 --> B1
    A2 --> B2
    A3 --> B3
    
    B1 --> C1
    B2 --> C2
    B3 --> C3
    
    C1 --> D1
    C2 --> D2
    C3 --> D3
    
    D1 --> E1
    D2 --> E2
    D3 --> E3
    
    E1 --> F1
    E2 --> F2
    E3 --> F3
    
    style INPUT fill:#00d2d3,stroke:#01a3a4,stroke-width:2px
    style SCAN fill:#1e90ff,stroke:#1873cc,stroke-width:2px
    style ANALYZE fill:#9b59b6,stroke:#8e44ad,stroke-width:2px
    style FILTER fill:#f39c12,stroke:#d68910,stroke-width:2px
    style ACTION fill:#e74c3c,stroke:#c0392b,stroke-width:2px
    style OUTPUT fill:#2ecc71,stroke:#27ae60,stroke-width:2px
```

## 📈 Performance Metrics Timeline

```mermaid
%%{init: {'theme':'base', 'themeVariables': { 'primaryColor':'#f093fb','primaryTextColor':'#fff'}}}%%
gantt
    title Cleanup Operations Timeline
    dateFormat ss
    axisFormat %S sec
    
    section Scanning
    Scan Downloads        :a1, 00, 3s
    Scan Caches          :a2, after a1, 5s
    Find Duplicates      :a3, after a2, 2s
    
    section Analysis
    Calculate Sizes      :b1, after a3, 2s
    Group Files          :b2, after b1, 1s
    Generate Report      :b3, after b2, 1s
    
    section Cleanup
    Delete Duplicates    :c1, after b3, 2s
    Clear Caches         :c2, after c1, 4s
    Organize Files       :c3, after c2, 3s
    
    section Finalize
    Update Stats         :d1, after c3, 1s
    Show Summary         :d2, after d1, 1s
```

## 🎨 Category Distribution

```mermaid
%%{init: {'theme':'base', 'themeVariables': { 'primaryColor':'#ff6b81','primaryTextColor':'#fff'}}}%%
pie title "Files in Downloads by Type"
    "Documents (PDF, DOC)" : 42
    "Images (JPG, PNG)" : 28
    "Archives (ZIP, RAR)" : 15
    "Videos (MP4, MOV)" : 10
    "Code Files" : 3
    "Other" : 2
```

## 🏗️ Component Architecture

```mermaid
%%{init: {'theme':'base', 'themeVariables': { 'primaryColor':'#a29bfe','primaryTextColor':'#fff','primaryBorderColor':'#6c5ce7'}}}%%
C4Context
    title System Cleanup Master - Component Diagram
    
    Person(user, "User", "Mac User")
    
    System_Boundary(cleanup, "Cleanup Master") {
        Container(ui, "UI Layer", "Rich Console", "Terminal interface")
        Container(engine, "Core Engine", "Python", "Cleanup logic")
        Container(scanner, "Scanner", "Python", "File analysis")
        Container(cleaner, "Cleaner", "Python", "File operations")
    }
    
    System_Ext(fs, "File System", "macOS")
    System_Ext(cache, "Cache Dirs", "System caches")
    System_Ext(brew, "Homebrew", "Package manager")
    
    Rel(user, ui, "Interacts with")
    Rel(ui, engine, "Commands")
    Rel(engine, scanner, "Scan request")
    Rel(engine, cleaner, "Clean request")
    Rel(scanner, fs, "Read files")
    Rel(cleaner, fs, "Delete files")
    Rel(cleaner, cache, "Clear cache")
    Rel(cleaner, brew, "Clean packages")
```

## 🔐 Safety Flow

```mermaid
%%{init: {'theme':'base', 'themeVariables': { 'primaryColor':'#fd79a8','primaryTextColor':'#fff','primaryBorderColor':'#e84393'}}}%%
sequenceDiagram
    autonumber
    
    actor User
    participant UI as 🎨 UI
    participant Engine as ⚙️ Engine
    participant Scanner as 🔍 Scanner
    participant Validator as ✅ Validator
    participant Cleaner as 🧹 Cleaner
    participant FS as 💾 File System
    
    User->>UI: Start Cleanup
    UI->>Engine: Initialize
    Engine->>Scanner: Scan Files
    Scanner->>FS: Read Metadata
    FS-->>Scanner: File Info
    Scanner-->>Engine: File List
    
    Engine->>Validator: Check Safety
    Validator-->>Engine: Safe to Delete
    
    Engine->>UI: Show Preview
    UI->>User: Display Items
    User->>UI: Confirm Delete
    
    alt User Confirms
        UI->>Engine: Proceed
        Engine->>Cleaner: Delete Files
        Cleaner->>FS: Remove Files
        FS-->>Cleaner: Success
        Cleaner-->>Engine: Stats
        Engine->>UI: Show Summary
        UI->>User: ✨ Done!
    else User Cancels
        UI->>Engine: Abort
        Engine->>UI: Cancelled
        UI->>User: ❌ Aborted
    end
```

## 📊 Before vs After Comparison

```mermaid
%%{init: {'theme':'base', 'themeVariables': { 'primaryColor':'#74b9ff','primaryTextColor':'#000'}}}%%
xychart-beta
    title "System State Comparison"
    x-axis [Duplicates, Caches, Temp Files, Logs, Organized]
    y-axis "Size (GB)" 0 --> 15
    line [2, 12, 3, 1, 0]
    line [0, 1, 0.5, 0.2, 15]
```

## 🎯 User Journey

```mermaid
%%{init: {'theme':'base', 'themeVariables': { 'primaryColor':'#fdcb6e','primaryTextColor':'#000','primaryBorderColor':'#f0b849'}}}%%
journey
    title User Cleanup Experience
    section Discovery
      Notice slow system: 3: User
      Check disk space: 4: User
      Find cleanup tool: 5: User
    section Setup
      Install dependencies: 5: User, System
      Run make install: 5: User
      Check status: 5: User
    section Cleaning
      Start cleanup: 5: User
      Review scan results: 4: User
      Confirm deletions: 4: User
      Watch progress: 5: User
    section Complete
      See summary: 5: User
      Check free space: 5: User
      Happy with results: 5: User
```

## 🔄 Cache Cleanup Cycle

```mermaid
%%{init: {'theme':'base', 'themeVariables': { 'primaryColor':'#55efc4','primaryTextColor':'#000','primaryBorderColor':'#00d2a0'}}}%%
graph TD
    START([System Running]) --> BUILD_UP[📈 Caches Accumulate]
    BUILD_UP --> THRESHOLD{Size > 10GB?}
    THRESHOLD -->|No| CONTINUE[Continue Using]
    CONTINUE --> BUILD_UP
    THRESHOLD -->|Yes| SLOW[⚠️ System Slows]
    SLOW --> CLEANUP[🧹 Run Cleanup]
    CLEANUP --> SCAN[🔍 Scan Caches]
    SCAN --> DELETE[🗑️ Delete Caches]
    DELETE --> FREED[✨ Space Freed]
    FREED --> FAST[⚡ System Fast]
    FAST --> START
    
    style START fill:#55efc4,stroke:#00d2a0,stroke-width:2px
    style SLOW fill:#ff7675,stroke:#d63031,stroke-width:2px
    style CLEANUP fill:#fdcb6e,stroke:#f0b849,stroke-width:2px
    style FREED fill:#00b894,stroke:#00a383,stroke-width:2px
    style FAST fill:#00d2d3,stroke:#01a3a4,stroke-width:2px
```

## 🎨 Color Legend

| Color | Meaning | Use Case |
|-------|---------|----------|
| 🔵 **Blue** | Information, Scanning | Non-destructive operations |
| 🟢 **Green** | Success, Completion | Successful operations |
| 🟡 **Yellow** | Warning, Confirmation | Requires attention |
| 🔴 **Red** | Deletion, Critical | Destructive operations |
| 🟣 **Purple** | Processing, Analysis | Background tasks |
| 🟠 **Orange** | System-level | Requires privileges |

---

**Navigation:** [← Back to README](README.md) | [View Code →](cleanup_master.py)
