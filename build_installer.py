#!/usr/bin/env python3
"""
Build script for creating installers for Windows and macOS
"""

import os
import sys
import shutil
import subprocess
import platform
from pathlib import Path

# Configuration
APP_NAME = "QuantumQueue"
APP_VERSION = "1.1.1"
AUTHOR = "dianbrown"
DESCRIPTION = "CPU Scheduling & Page Replacement Practice Application"

def clean_build_dirs():
    """Clean previous build artifacts"""
    print("🧹 Cleaning build directories...")
    dirs_to_clean = ['build', 'dist', '__pycache__']
    for dir_name in dirs_to_clean:
        if os.path.exists(dir_name):
            shutil.rmtree(dir_name)
            print(f"   Removed {dir_name}/")
    
    # Clean .spec file if exists (we'll use our custom one)
    if os.path.exists(f'{APP_NAME}.spec'):
        print(f"   Using custom {APP_NAME}.spec file")

def install_dependencies():
    """Install required build dependencies"""
    print("📦 Installing build dependencies...")
    dependencies = [
        'pyinstaller',
        'pillow',  # For icon conversion
    ]
    
    for dep in dependencies:
        try:
            subprocess.check_call([sys.executable, '-m', 'pip', 'install', dep])
            print(f"   ✅ {dep} installed")
        except subprocess.CalledProcessError:
            print(f"   ❌ Failed to install {dep}")
            return False
    return True

def convert_icon():
    """Convert PNG icon to platform-specific format"""
    print("🎨 Converting icon to platform-specific format...")
    
    try:
        from PIL import Image
        
        icon_dir = Path("Assets/Icons")
        icon_dir.mkdir(parents=True, exist_ok=True)
        
        png_path = icon_dir / "QuantumQueue2.png"
        
        if not png_path.exists():
            print(f"   ⚠️  Warning: {png_path} not found, using default icon")
            return True
        
        img = Image.open(png_path)
        
        if platform.system() == 'Windows':
            # Convert to ICO
            ico_path = icon_dir / "app_icon.ico"
            # Create multiple sizes for better quality
            img.save(ico_path, format='ICO', sizes=[(16,16), (32,32), (48,48), (64,64), (128,128), (256,256)])
            print(f"   ✅ Created {ico_path}")
            
        elif platform.system() == 'Darwin':
            # Convert to ICNS (macOS)
            icns_path = icon_dir / "app_icon.icns"
            # For ICNS, we need to use a different approach
            # Save as PNG with different sizes and use iconutil (macOS only)
            iconset_path = icon_dir / "app_icon.iconset"
            iconset_path.mkdir(exist_ok=True)
            
            sizes = [16, 32, 64, 128, 256, 512, 1024]
            for size in sizes:
                resized = img.resize((size, size), Image.Resampling.LANCZOS)
                resized.save(iconset_path / f"icon_{size}x{size}.png")
                if size <= 512:
                    resized_2x = img.resize((size*2, size*2), Image.Resampling.LANCZOS)
                    resized_2x.save(iconset_path / f"icon_{size}x{size}@2x.png")
            
            # Convert iconset to icns using macOS iconutil
            try:
                subprocess.check_call(['iconutil', '-c', 'icns', str(iconset_path), '-o', str(icns_path)])
                shutil.rmtree(iconset_path)
                print(f"   ✅ Created {icns_path}")
            except (subprocess.CalledProcessError, FileNotFoundError):
                print("   ⚠️  iconutil not available, copying PNG as fallback")
                shutil.copy(png_path, icns_path.with_suffix('.png'))
        
        return True
        
    except ImportError:
        print("   ⚠️  Pillow not installed, skipping icon conversion")
        return True
    except Exception as e:
        print(f"   ⚠️  Icon conversion failed: {e}")
        return True  # Continue anyway

def build_executable():
    """Build the executable using PyInstaller"""
    print(f"🔨 Building {APP_NAME} executable...")
    
    try:
        cmd = [
            'pyinstaller',
            '--clean',
            '--noconfirm',
            f'{APP_NAME}.spec'
        ]
        
        subprocess.check_call(cmd)
        print("   ✅ Executable built successfully")
        return True
        
    except subprocess.CalledProcessError as e:
        print(f"   ❌ Build failed: {e}")
        return False

def create_windows_installer():
    """Create Windows installer using Inno Setup"""
    print("📦 Creating Windows installer...")
    
    # Create Inno Setup script
    iss_content = f"""
; Inno Setup Script for {APP_NAME}
[Setup]
AppName={APP_NAME}
AppVersion={APP_VERSION}
AppPublisher={AUTHOR}
AppPublisherURL=https://github.com/{AUTHOR}/CPU-SchedulingApp
DefaultDirName={{autopf}}\\{APP_NAME}
DefaultGroupName={APP_NAME}
OutputDir=dist\\installers
OutputBaseFilename={APP_NAME}-{APP_VERSION}-Windows-Setup
SetupIconFile=Assets\\Icons\\app_icon.ico
Compression=lzma2
SolidCompression=yes
ArchitecturesAllowed=x64
ArchitecturesInstallIn64BitMode=x64
WizardStyle=modern
UninstallDisplayIcon={{app}}\\{APP_NAME}.exe

[Languages]
Name: "english"; MessagesFile: "compiler:Default.isl"

[Tasks]
Name: "desktopicon"; Description: "{{cm:CreateDesktopIcon}}"; GroupDescription: "{{cm:AdditionalIcons}}"

[Files]
Source: "dist\\{APP_NAME}.exe"; DestDir: "{{app}}"; Flags: ignoreversion

[Icons]
Name: "{{group}}\\{APP_NAME}"; Filename: "{{app}}\\{APP_NAME}.exe"; IconFilename: "{{app}}\\{APP_NAME}.exe"
Name: "{{autodesktop}}\\{APP_NAME}"; Filename: "{{app}}\\{APP_NAME}.exe"; Tasks: desktopicon; IconFilename: "{{app}}\\{APP_NAME}.exe"

[Run]
Filename: "{{app}}\\{APP_NAME}.exe"; Description: "{{cm:LaunchProgram,{APP_NAME}}}"; Flags: nowait postinstall skipifsilent
"""
    
    # Write ISS file
    iss_path = f"{APP_NAME}.iss"
    with open(iss_path, 'w') as f:
        f.write(iss_content)
    
    print(f"   ✅ Created {iss_path}")
    print(f"   ℹ️  To create installer, install Inno Setup and run:")
    print(f"      iscc {iss_path}")
    
    # Try to run Inno Setup if available
    inno_paths = [
        r"C:\Program Files (x86)\Inno Setup 6\ISCC.exe",
        r"C:\Program Files\Inno Setup 6\ISCC.exe",
    ]
    
    inno_exe = None
    for path in inno_paths:
        if os.path.exists(path):
            inno_exe = path
            break
    
    if inno_exe:
        try:
            os.makedirs('dist/installers', exist_ok=True)
            subprocess.check_call([inno_exe, iss_path])
            print(f"   ✅ Windows installer created in dist/installers/")
            return True
        except subprocess.CalledProcessError:
            print("   ⚠️  Inno Setup failed, but ISS script is ready")
    else:
        print("   ℹ️  Inno Setup not found. Download from: https://jrsoftware.org/isdl.php")
    
    return True

def create_macos_installer():
    """Create macOS DMG installer"""
    print("📦 Creating macOS DMG installer...")
    
    app_path = f"dist/{APP_NAME}.app"
    dmg_path = f"dist/installers/{APP_NAME}-{APP_VERSION}-macOS.dmg"
    
    if not os.path.exists(app_path):
        print(f"   ❌ {app_path} not found")
        return False
    
    os.makedirs('dist/installers', exist_ok=True)
    
    try:
        # Create DMG using hdiutil
        cmd = [
            'hdiutil', 'create',
            '-volname', APP_NAME,
            '-srcfolder', app_path,
            '-ov',
            '-format', 'UDZO',
            dmg_path
        ]
        
        subprocess.check_call(cmd)
        print(f"   ✅ macOS DMG created: {dmg_path}")
        return True
        
    except (subprocess.CalledProcessError, FileNotFoundError) as e:
        print(f"   ❌ DMG creation failed: {e}")
        print("   ℹ️  You can manually create DMG or use create-dmg tool")
        return False

def main():
    """Main build process"""
    print("=" * 60)
    print(f"🚀 Building {APP_NAME} v{APP_VERSION}")
    print("=" * 60)
    
    # Step 1: Clean
    clean_build_dirs()
    
    # Step 2: Install dependencies
    if not install_dependencies():
        print("\n❌ Failed to install dependencies")
        return 1
    
    # Step 3: Convert icon
    if not convert_icon():
        print("\n⚠️  Icon conversion had issues, continuing anyway...")
    
    # Step 4: Build executable
    if not build_executable():
        print("\n❌ Build failed")
        return 1
    
    # Step 5: Create installer
    print("\n" + "=" * 60)
    system = platform.system()
    
    if system == 'Windows':
        create_windows_installer()
    elif system == 'Darwin':
        create_macos_installer()
    else:
        print(f"⚠️  Installer creation not supported for {system}")
        print("   Executable is available in dist/ directory")
    
    print("\n" + "=" * 60)
    print("✅ Build process completed!")
    print("=" * 60)
    print(f"\n📁 Output:")
    print(f"   Executable: dist/{APP_NAME}.exe")
    if system == 'Windows':
        print(f"   Installer: dist/installers/{APP_NAME}-{APP_VERSION}-Windows-Setup.exe")
    elif system == 'Darwin':
        print(f"   Installer: dist/installers/{APP_NAME}-{APP_VERSION}-macOS.dmg")
    print(f"\n💡 To test: Run dist\\{APP_NAME}.exe")
    
    return 0

if __name__ == '__main__':
    sys.exit(main())
