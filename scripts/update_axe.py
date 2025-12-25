#!/usr/bin/env python3
"""
Script to update axe.min.js to the latest version.

Downloads the latest version of axe-core from GitHub releases and updates
the file src/axe_core_python/axe.min.js.
"""

import json
import re
import sys
from pathlib import Path
from urllib import request
from urllib.error import HTTPError, URLError

# Налаштування UTF-8 для виводу на Windows
if sys.platform == "win32":
    sys.stdout.reconfigure(encoding="utf-8")


def get_latest_version() -> tuple[str, str]:
    """
    Gets information about the latest axe-core version from GitHub API.

    Returns:
        tuple: (version, URL to download axe.min.js)
    """
    api_url = "https://api.github.com/repos/dequelabs/axe-core/releases/latest"
    
    try:
        with request.urlopen(api_url) as response:
            data = json.loads(response.read().decode())
            version = data["tag_name"].lstrip("v")
            download_url = f"https://cdn.jsdelivr.net/npm/axe-core@{version}/axe.min.js"
            return version, download_url
    except (HTTPError, URLError, KeyError, json.JSONDecodeError) as e:
        raise RuntimeError(f"Error getting version information: {e}")


def get_current_version(axe_file_path: Path) -> str | None:
    """
    Gets the current version from the axe.min.js file.

    Args:
        axe_file_path: path to the axe.min.js file

    Returns:
        Current version or None if not found
    """
    if not axe_file_path.exists():
        return None
    
    content = axe_file_path.read_text(encoding="utf-8")
    # Search for version in the comment at the beginning of the file
    match = re.search(r"axe v(\d+\.\d+\.\d+)", content)
    return match.group(1) if match else None


def download_axe_min_js(url: str, output_path: Path) -> None:
    """
    Downloads axe.min.js from the specified URL.

    Args:
        url: URL to download from
        output_path: path to save the file
    """
    try:
        with request.urlopen(url) as response:
            content = response.read()
            output_path.write_bytes(content)
    except (HTTPError, URLError) as e:
        raise RuntimeError(f"Error downloading file: {e}")


def update_copyright_header(axe_file_path: Path, version: str) -> None:
    """
    Updates the copyright header in the axe.min.js file.

    Args:
        axe_file_path: path to the axe.min.js file
        version: new version
    """
    content = axe_file_path.read_text(encoding="utf-8")
    
    # Remove old header if exists
    content = re.sub(r"/\*!.*?\*/\s*", "", content, flags=re.DOTALL, count=1)
    
    # Add new header
    header = f"""/*! axe v{version}
 * Copyright (c) 2022 Deque Systems, Inc.
 *
 * Your use of this Source Code Form is subject to the terms of the Mozilla Public
 * License, v. 2.0. If a copy of the MPL was not distributed with this
 * file, You can obtain one at http://mozilla.org/MPL/2.0/.
 *
 * This entire copyright notice must appear in every copy of this file you
 * distribute or in any file that contains substantial portions of this source
 * code.
 */

"""
    
    axe_file_path.write_text(header + content, encoding="utf-8")


def main() -> None:
    """Main function of the script."""
    # Define paths
    script_dir = Path(__file__).parent
    project_root = script_dir.parent
    axe_file_path = project_root / "src" / "axe_core_python" / "axe.min.js"
    
    print("🔍 Checking for axe-core updates...")
    
    # Get current and latest versions
    current_version = get_current_version(axe_file_path)
    latest_version, download_url = get_latest_version()
    
    print(f"📦 Current version: {current_version or 'not found'}")
    print(f"🆕 Latest version: {latest_version}")
    
    if current_version == latest_version:
        print("✅ You are already using the latest version!")
        return
    
    # Download new version
    print(f"\n⬇️  Downloading axe-core v{latest_version}...")
    print(f"🔗 URL: {download_url}")
    
    try:
        download_axe_min_js(download_url, axe_file_path)
        update_copyright_header(axe_file_path, latest_version)
        
        print(f"\n✅ Successfully updated to version {latest_version}!")
        print(f"📁 File updated: {axe_file_path.relative_to(project_root)}")
        
        if current_version:
            print(f"\n📝 Changes: {current_version} → {latest_version}")
            print(f"🔗 Release notes: https://github.com/dequelabs/axe-core/releases/tag/v{latest_version}")
        
    except RuntimeError as e:
        print(f"\n❌ {e}")
        return


if __name__ == "__main__":
    main()