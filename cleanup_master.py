#!/usr/bin/env python3
"""
🧹 System Cleanup Master - Beautiful System Cleaner
Removes clutter, organizes files, and frees up disk space
"""

import os
import sys
import subprocess
import shutil
from pathlib import Path
from datetime import datetime
from collections import defaultdict
import hashlib

from rich.console import Console
from rich.panel import Panel
from rich.progress import Progress, SpinnerColumn, BarColumn, TextColumn
from rich.table import Table
from rich.prompt import Confirm, Prompt
from rich.layout import Layout
from rich.tree import Tree
from rich import box
import psutil

console = Console()


class CleanupMaster:
    def __init__(self):
        self.console = console
        self.total_freed = 0
        self.stats = defaultdict(int)
        self.home = Path.home()
        
    def get_size(self, path):
        """Get size of file or directory in bytes"""
        try:
            if os.path.isfile(path):
                return os.path.getsize(path)
            total = 0
            for dirpath, dirnames, filenames in os.walk(path):
                for f in filenames:
                    fp = os.path.join(dirpath, f)
                    try:
                        total += os.path.getsize(fp)
                    except:
                        pass
            return total
        except:
            return 0
    
    def get_file_hash(self, filepath, chunk_size=8192):
        """Calculate MD5 hash of file for duplicate detection"""
        try:
            md5 = hashlib.md5()
            with open(filepath, 'rb') as f:
                while chunk := f.read(chunk_size):
                    md5.update(chunk)
            return md5.hexdigest()
        except:
            return None
    
    def format_bytes(self, bytes_size):
        """Convert bytes to human readable format"""
        for unit in ['B', 'KB', 'MB', 'GB', 'TB']:
            if bytes_size < 1024.0:
                return f"{bytes_size:.2f} {unit}"
            bytes_size /= 1024.0
        return f"{bytes_size:.2f} PB"
    
    def show_header(self):
        """Display beautiful header"""
        header = """
  ██████╗██╗     ███████╗ █████╗ ███╗   ██╗██╗   ██╗██████╗ 
 ██╔════╝██║     ██╔════╝██╔══██╗████╗  ██║██║   ██║██╔══██╗
 ██║     ██║     █████╗  ███████║██╔██╗ ██║██║   ██║██████╔╝
 ██║     ██║     ██╔══╝  ██╔══██║██║╚██╗██║██║   ██║██╔═══╝ 
 ╚██████╗███████╗███████╗██║  ██║██║ ╚████║╚██████╔╝██║     
  ╚═════╝╚══════╝╚══════╝╚═╝  ╚═╝╚═╝  ╚═══╝ ╚═════╝ ╚═╝     
        """
        self.console.print(Panel(
            header,
            title="[bold cyan]System Cleanup Master[/bold cyan]",
            subtitle="[italic]Free up space • Organize files • Speed up system[/italic]",
            border_style="cyan",
            box=box.DOUBLE
        ))
    
    def scan_system(self):
        """Scan system for clutter"""
        self.console.print("\n[bold yellow]🔍 Scanning system for clutter...[/bold yellow]\n")
        
        results = {
            'downloads': [],
            'caches': [],
            'duplicates': [],
            'large_files': []
        }
        
        with Progress(
            SpinnerColumn(),
            TextColumn("[progress.description]{task.description}"),
            BarColumn(),
            TextColumn("[progress.percentage]{task.percentage:>3.0f}%"),
            console=self.console
        ) as progress:
            
            # Scan Downloads
            task1 = progress.add_task("[cyan]Scanning Downloads...", total=100)
            downloads_path = self.home / "Downloads"
            if downloads_path.exists():
                files = list(downloads_path.glob("*"))
                for i, file in enumerate(files):
                    if file.is_file():
                        size = self.get_size(file)
                        results['downloads'].append({
                            'path': file,
                            'size': size,
                            'name': file.name,
                            'modified': datetime.fromtimestamp(file.stat().st_mtime)
                        })
                    progress.update(task1, completed=(i + 1) / len(files) * 100 if files else 100)
            progress.update(task1, completed=100)
            
            # Scan Caches
            task2 = progress.add_task("[green]Scanning Caches...", total=100)
            cache_path = self.home / "Library" / "Caches"
            if cache_path.exists():
                cache_dirs = [d for d in cache_path.iterdir() if d.is_dir()]
                for i, cache_dir in enumerate(cache_dirs):
                    size = self.get_size(cache_dir)
                    if size > 1024 * 1024:  # > 1MB
                        results['caches'].append({
                            'path': cache_dir,
                            'size': size,
                            'name': cache_dir.name
                        })
                    progress.update(task2, completed=(i + 1) / len(cache_dirs) * 100 if cache_dirs else 100)
            progress.update(task2, completed=100)
            
            # Find duplicates in Downloads
            task3 = progress.add_task("[magenta]Finding duplicates...", total=100)
            file_groups = defaultdict(list)
            for item in results['downloads']:
                # Group by base name (without numbers)
                base_name = item['name']
                # Remove (1), (2), etc.
                import re
                base = re.sub(r'\s*\([0-9]+\)\s*', '', base_name)
                file_groups[base].append(item)
            
            for base, files in file_groups.items():
                if len(files) > 1:
                    # Sort by date, keep oldest
                    files.sort(key=lambda x: x['modified'])
                    duplicates = files[1:]
                    results['duplicates'].extend(duplicates)
            progress.update(task3, completed=100)
        
        return results
    
    def find_duplicate_images(self, directories=None):
        """Find duplicate images by content hash"""
        if directories is None:
            directories = [
                self.home / "Downloads",
                self.home / "Pictures",
                self.home / "Desktop"
            ]
        
        self.console.print("\n[bold yellow]🔍 Scanning for duplicate images...[/bold yellow]\n")
        
        image_extensions = {'.jpg', '.jpeg', '.png', '.gif', '.bmp', '.webp', '.tiff', '.heic', '.heif'}
        hash_map = defaultdict(list)
        duplicate_groups = []
        
        with Progress(
            SpinnerColumn(),
            TextColumn("[progress.description]{task.description}"),
            BarColumn(),
            TextColumn("[progress.percentage]{task.percentage:>3.0f}%"),
            console=self.console
        ) as progress:
            
            # Collect all image files
            all_images = []
            for directory in directories:
                if directory.exists():
                    for ext in image_extensions:
                        all_images.extend(directory.rglob(f"*{ext}"))
            
            if not all_images:
                self.console.print("[yellow]No images found to scan[/yellow]")
                return []
            
            task = progress.add_task(f"[cyan]Hashing {len(all_images)} images...", total=len(all_images))
            
            # Hash each image
            for img_path in all_images:
                if img_path.is_file():
                    file_hash = self.get_file_hash(img_path)
                    if file_hash:
                        hash_map[file_hash].append({
                            'path': img_path,
                            'size': img_path.stat().st_size,
                            'modified': datetime.fromtimestamp(img_path.stat().st_mtime)
                        })
                progress.advance(task)
        
        # Find duplicates (keep oldest in each group)
        for file_hash, files in hash_map.items():
            if len(files) > 1:
                # Sort by modification time, keep oldest
                files.sort(key=lambda x: x['modified'])
                duplicate_groups.append({
                    'original': files[0],
                    'duplicates': files[1:],
                    'count': len(files)
                })
        
        return duplicate_groups
    
    def find_duplicate_media(self, scan_all_users=False, media_type='both'):
        """Find duplicate images and/or videos by content hash
        
        Args:
            scan_all_users: If True, scan all users (requires sudo)
            media_type: 'images', 'videos', or 'both'
        """
        directories = []
        
        if scan_all_users:
            # Scan all users
            try:
                users_dir = Path("/Users")
                for user_dir in users_dir.iterdir():
                    if user_dir.is_dir() and user_dir.name not in ['Shared', '.localized']:
                        directories.extend([
                            user_dir / "Downloads",
                            user_dir / "Pictures",
                            user_dir / "Desktop",
                            user_dir / "Documents"
                        ])
                self.console.print(f"[cyan]🔐 Scanning all users (found {len(set(d.parent.name for d in directories))} users)[/cyan]")
            except PermissionError:
                self.console.print("[red]❌ Permission denied. Run with sudo for all-users scan[/red]")
                return []
        else:
            # Scan current user only
            directories = [
                self.home / "Downloads",
                self.home / "Pictures",
                self.home / "Desktop",
                self.home / "Documents"
            ]
        
        # Set up extensions
        image_extensions = {'.jpg', '.jpeg', '.png', '.gif', '.bmp', '.webp', '.tiff', '.heic', '.heif'}
        video_extensions = {'.mp4', '.mov', '.avi', '.mkv', '.wmv', '.flv', '.m4v', '.mpg', '.mpeg', '.3gp'}
        
        if media_type == 'images':
            extensions = image_extensions
            type_name = "images"
            emoji = "🖼️"
        elif media_type == 'videos':
            extensions = video_extensions
            type_name = "videos"
            emoji = "🎬"
        else:
            extensions = image_extensions | video_extensions
            type_name = "media files"
            emoji = "🎬🖼️"
        
        self.console.print(f"\n[bold yellow]🔍 Scanning for duplicate {type_name}...[/bold yellow]\n")
        
        hash_map = defaultdict(list)
        duplicate_groups = []
        
        with Progress(
            SpinnerColumn(),
            TextColumn("[progress.description]{task.description}"),
            BarColumn(),
            TextColumn("[progress.percentage]{task.percentage:>3.0f}%"),
            console=self.console
        ) as progress:
            
            # Collect all media files
            all_files = []
            for directory in directories:
                if directory.exists():
                    try:
                        for ext in extensions:
                            all_files.extend(directory.rglob(f"*{ext}"))
                    except PermissionError:
                        self.console.print(f"[yellow]⚠️  Skipping {directory} (permission denied)[/yellow]")
                        continue
            
            if not all_files:
                self.console.print(f"[yellow]No {type_name} found to scan[/yellow]")
                return []
            
            task = progress.add_task(f"[cyan]Hashing {len(all_files)} {type_name}...", total=len(all_files))
            
            # Hash each file
            for file_path in all_files:
                if file_path.is_file():
                    try:
                        file_hash = self.get_file_hash(file_path)
                        if file_hash:
                            hash_map[file_hash].append({
                                'path': file_path,
                                'size': file_path.stat().st_size,
                                'modified': datetime.fromtimestamp(file_path.stat().st_mtime),
                                'user': file_path.parts[2] if len(file_path.parts) > 2 else 'unknown'
                            })
                    except Exception as e:
                        pass
                progress.advance(task)
        
        # Find duplicates (keep oldest in each group)
        for file_hash, files in hash_map.items():
            if len(files) > 1:
                # Sort by modification time, keep oldest
                files.sort(key=lambda x: x['modified'])
                duplicate_groups.append({
                    'original': files[0],
                    'duplicates': files[1:],
                    'count': len(files),
                    'type': emoji
                })
        
        return duplicate_groups
    
    def dedupe_images(self, directories=None):
        """Remove duplicate images"""
        duplicate_groups = self.find_duplicate_images(directories)
        
        if not duplicate_groups:
            self.console.print("[green]✓ No duplicate images found[/green]")
            return
        
        # Calculate total duplicates and size
        total_dupes = sum(len(group['duplicates']) for group in duplicate_groups)
        total_size = sum(sum(d['size'] for d in group['duplicates']) for group in duplicate_groups)
        
        # Display results
        table = Table(title="🖼️  Duplicate Images Found", box=box.ROUNDED, show_header=True, header_style="bold magenta")
        table.add_column("Original", style="cyan", no_wrap=False)
        table.add_column("Duplicates", style="yellow", justify="center")
        table.add_column("Size to Free", style="green", justify="right")
        
        for group in duplicate_groups[:15]:  # Show first 15 groups
            orig_name = group['original']['path'].name
            dup_count = len(group['duplicates'])
            dup_size = sum(d['size'] for d in group['duplicates'])
            table.add_row(orig_name[:50], str(dup_count), self.format_bytes(dup_size))
        
        self.console.print(table)
        
        if len(duplicate_groups) > 15:
            self.console.print(f"[dim]... and {len(duplicate_groups) - 15} more duplicate groups[/dim]")
        
        self.console.print(f"\n[bold]Found {total_dupes} duplicate images ({self.format_bytes(total_size)})[/bold]")
        
        if not Confirm.ask("Delete all duplicate images?", default=True):
            return
        
        # Delete duplicates
        freed = 0
        deleted = 0
        
        with Progress(console=self.console) as progress:
            task = progress.add_task("[red]Deleting duplicates...", total=total_dupes)
            
            for group in duplicate_groups:
                for dup in group['duplicates']:
                    try:
                        size = dup['size']
                        dup['path'].unlink()
                        freed += size
                        deleted += 1
                    except Exception as e:
                        self.console.print(f"[red]Error deleting {dup['path'].name}: {e}[/red]")
                    progress.advance(task)
        
        self.total_freed += freed
        self.stats['image_duplicates_removed'] = deleted
        self.console.print(f"[bold green]✓ Deleted {deleted} duplicate images, freed {self.format_bytes(freed)}[/bold green]")
    
    def dedupe_media_all_users(self, media_type='both'):
        """Remove duplicate media files across all users (requires sudo)
        
        Args:
            media_type: 'images', 'videos', or 'both'
        """
        # Check if running as root
        if os.geteuid() != 0:
            self.console.print("[red]❌ This operation requires sudo privileges[/red]")
            self.console.print("[yellow]💡 Run with: sudo make dedupe-all-users[/yellow]")
            return
        
        duplicate_groups = self.find_duplicate_media(scan_all_users=True, media_type=media_type)
        
        if not duplicate_groups:
            self.console.print(f"[green]✓ No duplicate {media_type} found across all users[/green]")
            return
        
        # Calculate total duplicates and size
        total_dupes = sum(len(group['duplicates']) for group in duplicate_groups)
        total_size = sum(sum(d['size'] for d in group['duplicates']) for group in duplicate_groups)
        
        # Display results grouped by user
        table = Table(title=f"🎬🖼️  Duplicate Media Found (All Users)", box=box.ROUNDED, show_header=True, header_style="bold magenta")
        table.add_column("Type", style="white", width=4)
        table.add_column("Original", style="cyan", no_wrap=False)
        table.add_column("User", style="yellow", justify="center")
        table.add_column("Dupes", style="red", justify="center")
        table.add_column("Size", style="green", justify="right")
        
        for group in duplicate_groups[:20]:  # Show first 20 groups
            orig_name = group['original']['path'].name
            orig_user = group['original'].get('user', 'unknown')
            dup_count = len(group['duplicates'])
            dup_size = sum(d['size'] for d in group['duplicates'])
            dup_users = ', '.join(set(d.get('user', '?') for d in group['duplicates']))
            
            table.add_row(
                group['type'],
                orig_name[:40] + "..." if len(orig_name) > 40 else orig_name,
                orig_user,
                str(dup_count),
                self.format_bytes(dup_size)
            )
        
        self.console.print(table)
        
        if len(duplicate_groups) > 20:
            self.console.print(f"[dim]... and {len(duplicate_groups) - 20} more duplicate groups[/dim]")
        
        self.console.print(f"\n[bold]Found {total_dupes} duplicates across all users ({self.format_bytes(total_size)})[/bold]")
        
        if not Confirm.ask("Delete all duplicates across all users?", default=False):
            return
        
        # Delete duplicates
        freed = 0
        deleted = 0
        errors = 0
        
        with Progress(console=self.console) as progress:
            task = progress.add_task("[red]Deleting duplicates across all users...", total=total_dupes)
            
            for group in duplicate_groups:
                for dup in group['duplicates']:
                    try:
                        size = dup['size']
                        dup['path'].unlink()
                        freed += size
                        deleted += 1
                    except Exception as e:
                        errors += 1
                        self.console.print(f"[red]Error: {dup['path']}: {e}[/red]")
                    progress.advance(task)
        
        self.total_freed += freed
        self.stats['media_duplicates_removed'] = deleted
        self.console.print(f"[bold green]✓ Deleted {deleted} duplicates, freed {self.format_bytes(freed)}[/bold green]")
        if errors > 0:
            self.console.print(f"[yellow]⚠️  {errors} files could not be deleted[/yellow]")
    
    def display_scan_results(self, results):
        """Display scan results in beautiful tables"""
        
        # Downloads Table
        if results['downloads']:
            table = Table(title="📥 Downloads Folder", box=box.ROUNDED, show_header=True, header_style="bold magenta")
            table.add_column("File", style="cyan", no_wrap=False)
            table.add_column("Size", style="green", justify="right")
            table.add_column("Modified", style="yellow")
            
            # Sort by size
            downloads_sorted = sorted(results['downloads'], key=lambda x: x['size'], reverse=True)[:10]
            for item in downloads_sorted:
                table.add_row(
                    item['name'][:50] + "..." if len(item['name']) > 50 else item['name'],
                    self.format_bytes(item['size']),
                    item['modified'].strftime("%Y-%m-%d")
                )
            
            self.console.print(table)
            self.console.print(f"[dim]Total files: {len(results['downloads'])}[/dim]\n")
        
        # Caches Table
        if results['caches']:
            table = Table(title="💾 Cache Folders", box=box.ROUNDED, show_header=True, header_style="bold green")
            table.add_column("Cache", style="cyan")
            table.add_column("Size", style="green", justify="right")
            
            caches_sorted = sorted(results['caches'], key=lambda x: x['size'], reverse=True)[:10]
            for item in caches_sorted:
                table.add_row(item['name'], self.format_bytes(item['size']))
            
            self.console.print(table)
            total_cache = sum(c['size'] for c in results['caches'])
            self.console.print(f"[dim]Total cache size: {self.format_bytes(total_cache)}[/dim]\n")
        
        # Duplicates Table
        if results['duplicates']:
            table = Table(title="🔄 Duplicate Files", box=box.ROUNDED, show_header=True, header_style="bold red")
            table.add_column("File", style="cyan")
            table.add_column("Size", style="green", justify="right")
            
            for item in results['duplicates'][:10]:
                table.add_row(item['name'], self.format_bytes(item['size']))
            
            self.console.print(table)
            total_dup = sum(d['size'] for d in results['duplicates'])
            self.console.print(f"[dim]Total duplicate size: {self.format_bytes(total_dup)}[/dim]\n")
    
    def clean_duplicates(self, duplicates):
        """Remove duplicate files"""
        if not duplicates:
            self.console.print("[yellow]No duplicates found[/yellow]")
            return
        
        total_size = sum(d['size'] for d in duplicates)
        self.console.print(f"\n[bold]Found {len(duplicates)} duplicates ({self.format_bytes(total_size)})[/bold]")
        
        if not Confirm.ask("Delete all duplicates?", default=True):
            return
        
        freed = 0
        with Progress(console=self.console) as progress:
            task = progress.add_task("[red]Deleting duplicates...", total=len(duplicates))
            
            for dup in duplicates:
                try:
                    size = dup['size']
                    dup['path'].unlink()
                    freed += size
                    self.stats['duplicates_removed'] += 1
                except Exception as e:
                    self.console.print(f"[red]Error deleting {dup['name']}: {e}[/red]")
                progress.advance(task)
        
        self.total_freed += freed
        self.console.print(f"[bold green]✓ Freed {self.format_bytes(freed)}[/bold green]")
    
    def clean_caches(self, caches):
        """Clean cache directories"""
        if not caches:
            self.console.print("[yellow]No caches to clean[/yellow]")
            return
        
        # Show what will be cleaned
        table = Table(title="Caches to Clean", box=box.SIMPLE)
        table.add_column("Cache", style="cyan")
        table.add_column("Size", style="green", justify="right")
        
        cleanable = [c for c in caches if c['size'] > 10 * 1024 * 1024]  # > 10MB
        for cache in cleanable[:15]:
            table.add_row(cache['name'], self.format_bytes(cache['size']))
        
        self.console.print(table)
        total_size = sum(c['size'] for c in cleanable)
        self.console.print(f"\n[bold]Total: {self.format_bytes(total_size)}[/bold]")
        
        if not Confirm.ask("Clean these caches?", default=True):
            return
        
        freed = 0
        with Progress(console=self.console) as progress:
            task = progress.add_task("[green]Cleaning caches...", total=len(cleanable))
            
            for cache in cleanable:
                try:
                    size = cache['size']
                    # Remove contents but keep directory
                    for item in cache['path'].iterdir():
                        if item.is_file():
                            item.unlink()
                        elif item.is_dir():
                            shutil.rmtree(item, ignore_errors=True)
                    freed += size
                    self.stats['caches_cleaned'] += 1
                except Exception as e:
                    self.console.print(f"[red]Error cleaning {cache['name']}: {e}[/red]")
                progress.advance(task)
        
        self.total_freed += freed
        self.console.print(f"[bold green]✓ Freed {self.format_bytes(freed)}[/bold green]")
    
    def organize_downloads(self):
        """Organize Downloads folder"""
        downloads = self.home / "Downloads"
        if not downloads.exists():
            return
        
        categories = {
            'Documents': ['.pdf', '.doc', '.docx', '.txt', '.xls', '.xlsx', '.ppt', '.pptx'],
            'Images': ['.jpg', '.jpeg', '.png', '.gif', '.bmp', '.svg', '.webp'],
            'Videos': ['.mp4', '.avi', '.mkv', '.mov', '.wmv', '.flv'],
            'Archives': ['.zip', '.rar', '.7z', '.tar', '.gz', '.bz2'],
            'Code': ['.py', '.js', '.html', '.css', '.java', '.cpp', '.c', '.sh'],
        }
        
        self.console.print("\n[bold cyan]📁 Organizing Downloads...[/bold cyan]")
        
        if not Confirm.ask("Organize files by category?", default=True):
            return
        
        moved = 0
        for file in downloads.iterdir():
            if file.is_file():
                ext = file.suffix.lower()
                for category, extensions in categories.items():
                    if ext in extensions:
                        category_dir = downloads / category
                        category_dir.mkdir(exist_ok=True)
                        try:
                            shutil.move(str(file), str(category_dir / file.name))
                            moved += 1
                        except Exception as e:
                            self.console.print(f"[red]Error moving {file.name}: {e}[/red]")
                        break
        
        self.stats['files_organized'] = moved
        self.console.print(f"[bold green]✓ Organized {moved} files[/bold green]")
    
    def clean_system_wide(self):
        """Clean system-wide caches (requires sudo)"""
        self.console.print("\n[bold yellow]🔧 System-Wide Cleanup[/bold yellow]")
        self.console.print("[dim]This requires administrator privileges[/dim]")
        
        if not Confirm.ask("Run system-wide cleanup?", default=False):
            return
        
        commands = [
            ("Homebrew", "brew cleanup --prune=all"),
            ("System temp", "sudo rm -rf /tmp/* /var/tmp/*"),
            ("System logs", "sudo rm -rf /private/var/log/*.log"),
        ]
        
        for name, cmd in commands:
            try:
                self.console.print(f"[cyan]Running {name} cleanup...[/cyan]")
                subprocess.run(cmd, shell=True, check=False, capture_output=True)
                self.console.print(f"[green]✓ {name} cleaned[/green]")
            except Exception as e:
                self.console.print(f"[red]Error: {e}[/red]")
    
    def show_summary(self):
        """Display cleanup summary"""
        self.console.print("\n")
        
        # Create summary panel
        summary = Table(box=box.DOUBLE_EDGE, show_header=False, padding=(0, 2))
        summary.add_column(style="cyan bold", justify="right")
        summary.add_column(style="green")
        
        summary.add_row("💾 Total Space Freed:", f"[bold green]{self.format_bytes(self.total_freed)}[/bold green]")
        summary.add_row("🗑️  Duplicates Removed:", str(self.stats.get('duplicates_removed', 0)))
        summary.add_row("🖼️  Image Dupes Removed:", str(self.stats.get('image_duplicates_removed', 0)))
        summary.add_row("🎬 Media Dupes Removed:", str(self.stats.get('media_duplicates_removed', 0)))
        summary.add_row("🧹 Caches Cleaned:", str(self.stats.get('caches_cleaned', 0)))
        summary.add_row("📁 Files Organized:", str(self.stats.get('files_organized', 0)))
        
        # Disk usage
        disk = psutil.disk_usage(str(self.home))
        summary.add_row("💿 Disk Free:", f"{self.format_bytes(disk.free)} ({disk.percent}% used)")
        
        self.console.print(Panel(
            summary,
            title="[bold green]✨ Cleanup Summary[/bold green]",
            border_style="green",
            box=box.DOUBLE
        ))
    
    def interactive_menu(self):
        """Show interactive menu"""
        while True:
            self.console.clear()
            self.show_header()
            
            menu = Table(box=box.ROUNDED, show_header=False, padding=(0, 2))
            menu.add_column(style="cyan bold", justify="center", width=10)
            menu.add_column(style="white")
            
            menu.add_row("1", "🔍 Scan System for Clutter")
            menu.add_row("2", "🧹 Quick Clean (Remove duplicates & caches)")
            menu.add_row("3", "�️  Dedupe Images (Remove duplicate images)")
            menu.add_row("4", "🎬 Dedupe Media - All Users (sudo required)")
            menu.add_row("5", "📁 Organize Downloads")
            menu.add_row("6", "🔧 System-Wide Cleanup")
            menu.add_row("7", "📊 Show Summary")
            menu.add_row("0", "❌ Exit")
            
            self.console.print(Panel(menu, title="[bold]Main Menu[/bold]", border_style="cyan"))
            
            choice = Prompt.ask("\n[bold cyan]Choose an option[/bold cyan]", choices=["0", "1", "2", "3", "4", "5", "6", "7"], default="1")
            
            if choice == "0":
                self.console.print("[bold green]👋 Goodbye![/bold green]")
                break
            elif choice == "1":
                results = self.scan_system()
                self.display_scan_results(results)
                Prompt.ask("\n[dim]Press Enter to continue[/dim]")
            elif choice == "2":
                results = self.scan_system()
                self.clean_duplicates(results['duplicates'])
                self.clean_caches(results['caches'])
                Prompt.ask("\n[dim]Press Enter to continue[/dim]")
            elif choice == "3":
                self.dedupe_images()
                Prompt.ask("\n[dim]Press Enter to continue[/dim]")
            elif choice == "4":
                self.dedupe_media_all_users(media_type='both')
                Prompt.ask("\n[dim]Press Enter to continue[/dim]")
            elif choice == "5":
                self.organize_downloads()
                Prompt.ask("\n[dim]Press Enter to continue[/dim]")
            elif choice == "6":
                self.clean_system_wide()
                Prompt.ask("\n[dim]Press Enter to continue[/dim]")
            elif choice == "7":
                self.show_summary()
                Prompt.ask("\n[dim]Press Enter to continue[/dim]")
    
    def run(self):
        """Main run method"""
        try:
            self.console.clear()
            self.show_header()
            
            # Check if running in interactive mode
            if len(sys.argv) > 1 and sys.argv[1] == "--auto":
                self.console.print("[bold yellow]Running in automatic mode...[/bold yellow]\n")
                results = self.scan_system()
                self.display_scan_results(results)
                self.clean_duplicates(results['duplicates'])
                self.clean_caches(results['caches'])
                self.organize_downloads()
                self.show_summary()
            else:
                self.interactive_menu()
        
        except KeyboardInterrupt:
            self.console.print("\n[bold red]Interrupted by user[/bold red]")
            sys.exit(0)
        except Exception as e:
            self.console.print(f"[bold red]Error: {e}[/bold red]")
            sys.exit(1)


def main():
    cleaner = CleanupMaster()
    cleaner.run()


if __name__ == "__main__":
    main()
