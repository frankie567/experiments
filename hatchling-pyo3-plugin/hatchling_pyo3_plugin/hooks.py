"""Build hook for compiling PyO3 Rust extensions."""

import os
import platform
import shutil
import subprocess
import sys
from pathlib import Path
from typing import Any, Dict

from hatchling.plugin import hookimpl
from hatchling.builders.hooks.plugin.interface import BuildHookInterface


class PyO3BuildHook(BuildHookInterface):
    """Build hook for compiling PyO3 Rust extensions with Cargo."""

    PLUGIN_NAME = "pyo3"

    def initialize(self, version: str, build_data: Dict[str, Any]) -> None:
        """
        Initialize the build hook.

        This method is called before the build starts and is responsible for:
        1. Finding Rust extensions (Cargo.toml files)
        2. Building them with cargo
        3. Adding the built artifacts to the wheel
        """
        if self.target_name != "wheel":
            # Only build Rust extensions for wheel builds
            return

        # Find the Cargo.toml file
        cargo_toml = Path(self.root) / "Cargo.toml"
        if not cargo_toml.exists():
            # No Rust extensions to build
            return

        # Build the Rust extension
        self._build_rust_extension(cargo_toml)

        # Find and add the compiled library to the build artifacts
        self._add_rust_artifacts(build_data)

    def _build_rust_extension(self, cargo_toml: Path) -> None:
        """Build the Rust extension using cargo."""
        cargo_dir = cargo_toml.parent

        # Determine the build profile
        profile = "release"
        
        # Build command
        cmd = [
            "cargo",
            "build",
            "--release",
            "--manifest-path",
            str(cargo_toml),
        ]

        # Set environment variables for the build
        env = os.environ.copy()
        
        # Tell cargo to build a cdylib (Python extension)
        # This is typically configured in Cargo.toml but we can ensure it

        self.app.display_info(f"Building Rust extension: {cargo_toml}")
        
        try:
            result = subprocess.run(
                cmd,
                cwd=str(cargo_dir),
                env=env,
                capture_output=True,
                text=True,
                check=True,
            )
            self.app.display_info("Rust extension built successfully")
            if result.stdout:
                self.app.display_debug(result.stdout)
        except subprocess.CalledProcessError as e:
            self.app.display_error(f"Failed to build Rust extension: {e}")
            if e.stdout:
                self.app.display_error(f"stdout: {e.stdout}")
            if e.stderr:
                self.app.display_error(f"stderr: {e.stderr}")
            raise

    def _add_rust_artifacts(self, build_data: Dict[str, Any]) -> None:
        """Find compiled Rust libraries and add them to the wheel."""
        target_dir = Path(self.root) / "target" / "release"
        
        if not target_dir.exists():
            self.app.display_warning(f"Target directory not found: {target_dir}")
            return

        # Determine the library extension based on platform
        if platform.system() == "Windows":
            lib_ext = ".pyd"
            lib_pattern = "*.dll"
        elif platform.system() == "Darwin":
            lib_ext = ".so"
            lib_pattern = "*.dylib"
        else:  # Linux
            lib_ext = ".so"
            lib_pattern = "*.so"

        # Find the compiled library
        # Look for cdylib outputs
        found_libs = []
        for lib_file in target_dir.glob(f"lib*{lib_pattern}"):
            if lib_file.is_file():
                found_libs.append(lib_file)
        
        # Also check for .so files directly (PyO3 outputs)
        for lib_file in target_dir.glob("*.so"):
            if lib_file.is_file() and lib_file not in found_libs:
                found_libs.append(lib_file)
        
        # On Windows, check for .pyd files
        if platform.system() == "Windows":
            for lib_file in target_dir.glob("*.pyd"):
                if lib_file.is_file() and lib_file not in found_libs:
                    found_libs.append(lib_file)

        if not found_libs:
            self.app.display_warning(
                f"No compiled Rust libraries found in {target_dir}"
            )
            return

        # Add each library to the wheel
        # We need to determine the package name and add it there
        package_name = self.metadata.core.name.replace("-", "_")
        
        for lib_file in found_libs:
            # Rename to proper Python extension name
            # lib<name>.so -> <name>.so or <name>.pyd
            stem = lib_file.stem
            if stem.startswith("lib"):
                stem = stem[3:]  # Remove 'lib' prefix
            
            # Create the target filename
            target_name = f"{stem}{lib_ext}"
            
            # Add to artifacts
            # The artifacts should be placed in the package directory
            artifact_path = f"{package_name}/{target_name}"
            
            self.app.display_info(f"Adding Rust artifact: {lib_file} -> {artifact_path}")
            
            # Add to build data
            if "force_include" not in build_data:
                build_data["force_include"] = {}
            
            build_data["force_include"][str(lib_file)] = artifact_path


@hookimpl
def hatch_register_build_hook():
    """Register the PyO3 build hook with Hatchling."""
    return PyO3BuildHook
