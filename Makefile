# 🧹 System Cleanup Master - Makefile
# Quick commands to run cleanup operations

.PHONY: help install run auto scan clean-dupes clean-cache organize system-clean full-clean check status test

# Python interpreter
PYTHON := .venv/bin/python
SCRIPT := cleanup_master.py

# Colors for output
RED := \033[0;31m
GREEN := \033[0;32m
YELLOW := \033[1;33m
CYAN := \033[0;36m
NC := \033[0m # No Color

## help: Show this help message
help:
	@echo "$(CYAN)╔═══════════════════════════════════════════════════════╗$(NC)"
	@echo "$(CYAN)║        🧹 System Cleanup Master - Commands          ║$(NC)"
	@echo "$(CYAN)╚═══════════════════════════════════════════════════════╝$(NC)"
	@echo ""
	@echo "$(GREEN)Setup Commands:$(NC)"
	@echo "  make install        - Install dependencies"
	@echo "  make check          - Check system requirements"
	@echo ""
	@echo "$(GREEN)Cleanup Commands:$(NC)"
	@echo "  make run            - Interactive menu (recommended)"
	@echo "  make auto           - Automatic cleanup"
	@echo "  make scan           - Scan system for clutter"
	@echo "  make clean-dupes    - Remove duplicate files"
	@echo "  make dedupe-images  - Remove duplicate images"
	@echo "  make dedupe-all-users - Dedupe media across ALL users (sudo)"
	@echo "  make clean-cache    - Clean cache folders"
	@echo "  make organize       - Organize Downloads folder"
	@echo "  make system-clean   - System-wide cleanup (needs sudo)"
	@echo "  make full-clean     - Complete cleanup (all above)"
	@echo ""
	@echo "$(GREEN)Utility Commands:$(NC)"
	@echo "  make status         - Show disk usage"
	@echo "  make test           - Test script syntax"
	@echo "  make clean          - Clean Python cache files"
	@echo ""
	@echo "$(YELLOW)Quick Start:$(NC) make run"

## install: Install required Python packages
install:
	@echo "$(CYAN)📦 Installing dependencies...$(NC)"
	@test -d .venv || python3 -m venv .venv
	@.venv/bin/pip install --upgrade pip > /dev/null 2>&1
	@.venv/bin/pip install rich click psutil > /dev/null 2>&1
	@echo "$(GREEN)✓ Dependencies installed!$(NC)"

## check: Check system requirements and disk space
check:
	@echo "$(CYAN)🔍 System Check$(NC)"
	@echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
	@echo "$(YELLOW)Python:$(NC) $$(python3 --version)"
	@echo "$(YELLOW)Virtual Env:$(NC) $$(test -d .venv && echo '✓ Active' || echo '✗ Not found')"
	@echo "$(YELLOW)Dependencies:$(NC) $$(.venv/bin/pip list 2>/dev/null | grep -E 'rich|click|psutil' | wc -l | xargs echo) / 3 installed"
	@echo ""
	@echo "$(YELLOW)💾 Disk Usage:$(NC)"
	@df -h ~ | tail -1 | awk '{print "  Total: " $$2 "  Used: " $$3 " (" $$5 ")  Available: " $$4}'
	@echo ""
	@echo "$(YELLOW)📂 Folder Sizes:$(NC)"
	@du -sh ~/Downloads 2>/dev/null | awk '{print "  Downloads: " $$1}'
	@du -sh ~/Library/Caches 2>/dev/null | awk '{print "  Caches: " $$1}'
	@echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"

## run: Start interactive cleanup menu
run: check-install
	@echo "$(GREEN)🚀 Starting Cleanup Master...$(NC)"
	@$(PYTHON) $(SCRIPT)

## auto: Run automatic cleanup (with confirmations)
auto: check-install
	@echo "$(GREEN)⚡ Running automatic cleanup...$(NC)"
	@$(PYTHON) $(SCRIPT) --auto

## scan: Scan system for clutter (read-only)
scan: check-install
	@echo "$(CYAN)🔍 Scanning system...$(NC)"
	@$(PYTHON) -c "from cleanup_master import CleanupMaster; c=CleanupMaster(); r=c.scan_system(); c.display_scan_results(r)"

## clean-dupes: Remove duplicate files in Downloads
clean-dupes: check-install
	@echo "$(YELLOW)🗑️  Removing duplicates...$(NC)"
	@$(PYTHON) -c "from cleanup_master import CleanupMaster; c=CleanupMaster(); r=c.scan_system(); c.clean_duplicates(r['duplicates']); c.show_summary()"

## dedupe-images: Find and remove duplicate images by content
dedupe-images: check-install
	@echo "$(YELLOW)🖼️  Deduplicating images...$(NC)"
	@$(PYTHON) -c "from cleanup_master import CleanupMaster; c=CleanupMaster(); c.dedupe_images(); c.show_summary()"

## dedupe-all-users: Deduplicate images and videos across ALL users (requires sudo)
dedupe-all-users: check-install
	@echo "$(RED)🎬🖼️  Deduplicating media across ALL users (requires sudo)...$(NC)"
	@if [ $$(id -u) -ne 0 ]; then \
		echo "$(RED)❌ This command requires sudo privileges$(NC)"; \
		echo "$(YELLOW)💡 Run: sudo make dedupe-all-users$(NC)"; \
		exit 1; \
	fi
	@sudo $(PYTHON) -c "from cleanup_master import CleanupMaster; c=CleanupMaster(); c.dedupe_media_all_users('both'); c.show_summary()"

## clean-cache: Clean cache directories
clean-cache: check-install
	@echo "$(YELLOW)🧹 Cleaning caches...$(NC)"
	@$(PYTHON) -c "from cleanup_master import CleanupMaster; c=CleanupMaster(); r=c.scan_system(); c.clean_caches(r['caches']); c.show_summary()"

## organize: Organize Downloads folder by file type
organize: check-install
	@echo "$(YELLOW)📁 Organizing downloads...$(NC)"
	@$(PYTHON) -c "from cleanup_master import CleanupMaster; c=CleanupMaster(); c.organize_downloads(); c.show_summary()"

## system-clean: System-wide cleanup (requires sudo)
system-clean: check-install
	@echo "$(RED)🔧 System-wide cleanup (requires sudo)$(NC)"
	@echo "$(YELLOW)This will clean:$(NC)"
	@echo "  • Homebrew caches"
	@echo "  • System temp files"
	@echo "  • System logs"
	@echo ""
	@read -p "Continue? [y/N] " confirm && [ "$$confirm" = "y" ] || exit 0
	@brew cleanup --prune=all 2>/dev/null || echo "$(YELLOW)Homebrew not found$(NC)"
	@sudo rm -rf /tmp/* /var/tmp/* 2>/dev/null || true
	@sudo rm -rf /private/var/log/*.log 2>/dev/null || true
	@echo "$(GREEN)✓ System cleanup complete$(NC)"

## full-clean: Complete cleanup (all operations)
full-clean: check-install
	@echo "$(CYAN)╔═══════════════════════════════════════════════════╗$(NC)"
	@echo "$(CYAN)║           🚀 FULL SYSTEM CLEANUP                 ║$(NC)"
	@echo "$(CYAN)╚═══════════════════════════════════════════════════╝$(NC)"
	@echo ""
	@echo "$(YELLOW)This will:$(NC)"
	@echo "  1. Remove duplicate files"
	@echo "  2. Remove duplicate images (current user)"
	@echo "  3. Clean all caches"
	@echo "  4. Organize Downloads"
	@echo "  5. System-wide cleanup"
	@echo ""
	@echo "$(RED)NOTE: For ALL users deduplication, run: sudo make dedupe-all-users$(NC)"
	@echo ""
	@read -p "Continue with full cleanup? [y/N] " confirm && [ "$$confirm" = "y" ] || exit 0
	@$(MAKE) clean-dupes
	@$(MAKE) dedupe-images
	@$(MAKE) clean-cache
	@$(MAKE) organize
	@$(MAKE) system-clean
	@echo ""
	@echo "$(GREEN)✨ Full cleanup complete!$(NC)"

## status: Show current disk usage and cache sizes
status:
	@echo "$(CYAN)📊 System Status$(NC)"
	@echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
	@echo ""
	@echo "$(YELLOW)💿 Disk Usage:$(NC)"
	@df -h ~ | tail -1 | awk '{printf "  Capacity: %s\n  Used: %s (%s)\n  Free: %s\n", $$2, $$3, $$5, $$4}'
	@echo ""
	@echo "$(YELLOW)📂 Directory Sizes:$(NC)"
	@du -sh ~/Downloads 2>/dev/null | awk '{printf "  Downloads:    %8s\n", $$1}'
	@du -sh ~/Library/Caches 2>/dev/null | awk '{printf "  Caches:       %8s\n", $$1}'
	@du -sh ~/Desktop 2>/dev/null | awk '{printf "  Desktop:      %8s\n", $$1}'
	@du -sh ~/Documents 2>/dev/null | awk '{printf "  Documents:    %8s\n", $$1}'
	@echo ""
	@echo "$(YELLOW)🗂️  Top 5 Cache Folders:$(NC)"
	@du -sh ~/Library/Caches/* 2>/dev/null | sort -hr | head -5 | awk '{printf "  %-30s %8s\n", substr($$2, index($$2, "Caches/")+7), $$1}'
	@echo ""
	@echo "$(YELLOW)📥 Downloads Summary:$(NC)"
	@find ~/Downloads -maxdepth 1 -type f 2>/dev/null | wc -l | awk '{printf "  Files:        %8d\n", $$1}'
	@find ~/Downloads -maxdepth 1 -type d 2>/dev/null | tail -n +2 | wc -l | awk '{printf "  Folders:      %8d\n", $$1}'
	@echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"

## test: Test script for syntax errors
test: check-install
	@echo "$(CYAN)🧪 Testing script...$(NC)"
	@$(PYTHON) -m py_compile $(SCRIPT) && echo "$(GREEN)✓ No syntax errors$(NC)" || echo "$(RED)✗ Syntax errors found$(NC)"
	@$(PYTHON) -c "import rich, click, psutil" && echo "$(GREEN)✓ All dependencies available$(NC)" || echo "$(RED)✗ Missing dependencies$(NC)"

## clean: Remove Python cache files
clean:
	@echo "$(YELLOW)🧹 Cleaning Python cache files...$(NC)"
	@find . -type d -name __pycache__ -exec rm -rf {} + 2>/dev/null || true
	@find . -type f -name "*.pyc" -delete 2>/dev/null || true
	@find . -type f -name "*.pyo" -delete 2>/dev/null || true
	@echo "$(GREEN)✓ Python cache cleaned$(NC)"

## quick: Quick cleanup (dupes + cache, no confirmation)
quick: check-install
	@echo "$(GREEN)⚡ Quick cleanup...$(NC)"
	@$(PYTHON) $(SCRIPT) --auto

## backup: Create backup of important settings
backup:
	@echo "$(CYAN)💾 Creating backup...$(NC)"
	@mkdir -p backups
	@tar -czf backups/cleanup_backup_$$(date +%Y%m%d_%H%M%S).tar.gz $(SCRIPT) Makefile README.md 2>/dev/null
	@echo "$(GREEN)✓ Backup created in backups/$(NC)"

## watch: Monitor disk space (updates every 5 seconds)
watch:
	@echo "$(CYAN)👀 Monitoring disk space (Ctrl+C to stop)...$(NC)"
	@while true; do \
		clear; \
		echo "$(CYAN)═══════════════════════════════════════$(NC)"; \
		echo "$(CYAN)  📊 Disk Monitor - $$(date '+%H:%M:%S')$(NC)"; \
		echo "$(CYAN)═══════════════════════════════════════$(NC)"; \
		df -h ~ | tail -1 | awk '{print "  Free: " $$4 " (" $$5 " used)"}'; \
		echo ""; \
		du -sh ~/Library/Caches 2>/dev/null | awk '{print "  Caches: " $$1}'; \
		du -sh ~/Downloads 2>/dev/null | awk '{print "  Downloads: " $$1}'; \
		sleep 5; \
	done

## schedule: Add to cron for weekly cleanup
schedule:
	@echo "$(YELLOW)📅 Setting up weekly cleanup...$(NC)"
	@echo "Add this to crontab (crontab -e):"
	@echo "$(CYAN)0 2 * * 0 cd $(PWD) && make auto >> cleanup.log 2>&1$(NC)"

# Internal target to check if dependencies are installed
check-install:
	@if [ ! -d .venv ]; then \
		echo "$(RED)✗ Virtual environment not found. Run: make install$(NC)"; \
		exit 1; \
	fi
	@if ! .venv/bin/pip list 2>/dev/null | grep -q rich; then \
		echo "$(RED)✗ Dependencies not installed. Run: make install$(NC)"; \
		exit 1; \
	fi

# Default target
.DEFAULT_GOAL := help
