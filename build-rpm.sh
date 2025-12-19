#!/bin/bash

# Function to play success sound
play_success_sound() {
    if command -v mpg123 &> /dev/null && [ -f "$HOME/projects/audio-files/rpm_actually_built.mp3" ]; then
        mpg123 "$HOME/projects/audio-files/rpm_actually_built.mp3" >/dev/null 2>&1 &
    fi
}

# Function to play fail sound
play_fail_sound() {
    if command -v mpg123 &> /dev/null && [ -f "$HOME/projects/audio-files/rpm_failed.mp3" ]; then
        mpg123 "$HOME/projects/audio-files/rpm_failed.mp3" >/dev/null 2>&1 &
    fi
}

# Trap to play fail sound on exit if not successful
SUCCESS=0
trap 'if [ $SUCCESS -eq 0 ]; then play_fail_sound; fi' EXIT

set -euo pipefail # Exit on error, unset var, or pipe failure
 
# --- Dependency Checking ---
check_and_install_deps() {
    echo "--- Checking for build dependencies ---"
    # Map commands to their package names
    declare -A deps
    deps["rpmbuild"]="rpm-build"
    deps["rpmdev-setuptree"]="rpmdevtools"
    deps["desktop-file-validate"]="desktop-file-utils"
    deps["appstreamcli"]="appstream"
    deps["rpmsign"]="rpm-sign"
    # Add SVG converters; check for at least one
    if ! command -v rsvg-convert &> /dev/null && ! command -v inkscape &> /dev/null && ! command -v convert &> /dev/null; then
        deps["rsvg-convert"]="librsvg2-tools" # Preferred for SVG, suggest this one
    fi

    local to_install=()
    for cmd in "${!deps[@]}"; do
        if ! command -v "$cmd" &> /dev/null; then
            echo "Missing dependency: '${deps[$cmd]}' (provides '$cmd')"
            to_install+=("${deps[$cmd]}")
        fi
    done

    if [ ${#to_install[@]} -gt 0 ]; then
        echo "The following packages are required: ${to_install[*]}"
        if command -v dnf &> /dev/null && command -v sudo &> /dev/null; then
            sudo dnf install -y "${to_install[@]}"
        fi
    fi
}
check_and_install_deps

APP_NAME="text-to-speech"
VERSION="0.1.0"
RELEASE_FILE=".release_info"

# Auto-increment Release (Resets if VERSION changes)
if [ -f "$RELEASE_FILE" ]; then
    # shellcheck disable=SC2034
    read -r LAST_VERSION LAST_RELEASE < "$RELEASE_FILE"
fi
if [ "$VERSION" == "${LAST_VERSION:-}" ] && [ -n "${LAST_RELEASE:-}" ]; then
    RELEASE=$((LAST_RELEASE + 1))
else
    RELEASE="1"
fi
echo "$VERSION $RELEASE" > "$RELEASE_FILE"
echo "--- Building version ${VERSION}-${RELEASE} ---"

ARCH="x86_64"
BINARY_NAME="text-to-speech"

# 1. Compile the binary if it doesn't exist
DIST_BIN="dist/$BINARY_NAME"
NEED_BUILD=0

if [ ! -f "$DIST_BIN" ]; then
    echo "Binary missing. Building..."
    NEED_BUILD=1
elif [ "src/text_to_speech.py" -nt "$DIST_BIN" ]; then
    echo "Source code changed. Rebuilding..."
    NEED_BUILD=1
elif [ -n "$(find assets -newer "$DIST_BIN" -print -quit 2>/dev/null)" ]; then
    echo "Assets changed. Rebuilding..."
    NEED_BUILD=1
fi

if [ "$NEED_BUILD" -eq 1 ]; then
    chmod +x compile.sh
    ./compile.sh
else
    echo "Binary is up to date. Skipping compilation."
fi

# Verify binary
if [ ! -x "$DIST_BIN" ]; then
    echo "Error: Binary $DIST_BIN is not executable or missing."
    exit 1
fi
file "$DIST_BIN" | grep -q "ELF" || echo "Warning: Binary does not look like an ELF executable."

# --- GPG Signing Configuration ---
SIGN_RPMS="1"
GPG_KEY="8CC02D3C" # Run 'gpg --list-keys' and paste your new Wheelhouser LLC Key ID here

# --- Setup RPM Build Environment ---
RPMBUILD_DIR="$PWD/rpmbuild"
echo "--- Cleaning and setting up RPM build environment in $RPMBUILD_DIR ---"
rm -rf "$RPMBUILD_DIR"
mkdir -p "$RPMBUILD_DIR"/{BUILD,RPMS,SOURCES,SPECS,SRPMS}

# Copy project sources that the spec expects into SOURCES so rpmbuild can access them
echo "--- Preparing SOURCES ---"
SOURCE_DIR="text-to-speech-${VERSION}"
rm -rf "build/${SOURCE_DIR}"
mkdir -p "build/${SOURCE_DIR}"

# Copy files to source dir
cp -f "${PWD}/com.wheelhouser.text_to_speech.desktop" "build/${SOURCE_DIR}/"

# Copy LICENSE so the spec can install it
cp -f "${PWD}/LICENSE" "build/${SOURCE_DIR}/"

# Copy AppStream metadata and normalize filename to .metainfo.xml (AppStream standard)
if [ -f "${PWD}/com.wheelhouser.text_to_speech.metainfo.xml" ]; then
    cp -f "${PWD}/com.wheelhouser.text_to_speech.metainfo.xml" "build/${SOURCE_DIR}/com.wheelhouser.text_to_speech.metainfo.xml"
fi
if [ -f "${PWD}/dist/${BINARY_NAME}" ]; then
    cp -f "${PWD}/dist/${BINARY_NAME}" "build/${SOURCE_DIR}/text-to-speech.bin"
fi
 
# --- Prepare Icons for RPM ---
echo "--- Preparing and renaming icons for RPM spec file ---"
SVG_ICON_SRC="assets/icons/icon.svg"
PNG_ICON_SRC="assets/icons/icon.png"
ICON_DEST_DIR="build/${SOURCE_DIR}/assets/icons"
APP_ICON_NAME="com.wheelhouser.text_to_speech"
mkdir -p "$ICON_DEST_DIR"
cp "$SVG_ICON_SRC" "$ICON_DEST_DIR/${APP_ICON_NAME}.svg"
cp "$PNG_ICON_SRC" "$ICON_DEST_DIR/${APP_ICON_NAME}.png"

# Create Tarball
echo "--- Creating Source Tarball ---"
tar -czf "$RPMBUILD_DIR/SOURCES/text-to-speech-${VERSION}.tar.gz" -C build "${SOURCE_DIR}"

# Validate AppStream metadata
echo "--- Validating AppStream metadata ---"
if ! command -v appstreamcli &> /dev/null; then
    echo "Warning: 'appstreamcli' is not installed. Skipping metadata validation."
else
    # Validate the copied/normalized metainfo inside the source dir if present
    if [ -f "build/${SOURCE_DIR}/com.wheelhouser.text_to_speech.metainfo.xml" ]; then
        echo "--- DEBUG: Checking ID in metainfo before packaging ---"
        grep "<id>" "build/${SOURCE_DIR}/com.wheelhouser.text_to_speech.metainfo.xml"
        echo "-------------------------------------------------------"

        appstreamcli validate "build/${SOURCE_DIR}/com.wheelhouser.text_to_speech.metainfo.xml" || {
            echo "AppStream metadata validation failed. Please fix the errors above."; exit 1; }
    else
        echo "No metainfo found in build source dir; skipping validation."
    fi
fi

# Validate Desktop File
echo "--- Validating Desktop File ---"
if command -v desktop-file-validate &> /dev/null; then
    desktop-file-validate "build/${SOURCE_DIR}/com.wheelhouser.text_to_speech.desktop" || {
        echo "Desktop file validation failed."; exit 1; }
else
    echo "Warning: 'desktop-file-validate' not found. Skipping validation."
fi

# --- Prepare Spec File ---
# Use the existing text-to-speech.spec file and modify it
SPEC_FILE_SRC="${APP_NAME}.spec"
SPEC_FILE_FINAL="${RPMBUILD_DIR}/SPECS/${APP_NAME}.spec"
cp "$SPEC_FILE_SRC" "$SPEC_FILE_FINAL"

# Ensure changelog exists to avoid warnings
if ! grep -q "%changelog" "$SPEC_FILE_FINAL"; then
    echo -e "\n%changelog" >> "$SPEC_FILE_FINAL"
fi

# Add new changelog entry for this build
DATE_STR=$(date "+%a %b %d %Y")
sed -i "/%changelog/a * $DATE_STR Wheelhouser LLC <steve.rock@wheelhouser.com> - ${VERSION}-${RELEASE}\\n- Automated build" "$SPEC_FILE_FINAL"

# Update Version and Release in spec file
sed -i "s/^Version:[[:space:]]*.*/Version:    ${VERSION}/" "$SPEC_FILE_FINAL"
sed -i "s/^Release:[[:space:]]*.*/Release:    ${RELEASE}/" "$SPEC_FILE_FINAL"

# --- Build the RPM ---
echo "--- Building RPM using rpmbuild ---"
rpmbuild -ba \
    --define "_topdir ${RPMBUILD_DIR}" \
    --define "__os_install_post %{nil}" \
    --define "debug_package %{nil}" \
    "$SPEC_FILE_FINAL"

echo "--- Done! RPMs located at: ---"
find $RPMBUILD_DIR/RPMS -name "*.rpm"

# --- GPG Signing ---
if [ "${SIGN_RPMS:-0}" = "1" ]; then
    echo "--- Signing RPMs ---"
    if ! command -v rpmsign &> /dev/null; then
        echo "Warning: 'rpmsign' not found. Cannot sign packages."
    else
        # Ensure ~/.rpmmacros has the GPG key name for signing
        if [ ! -f "$HOME/.rpmmacros" ] || ! grep -q "%_gpg_name" "$HOME/.rpmmacros"; then
            echo "Info: Creating temporary ~/.rpmmacros for signing with key ${GPG_KEY}"
            echo "%_signature gpg" > "$HOME/.rpmmacros"
            echo "%_gpg_name ${GPG_KEY}" >> "$HOME/.rpmmacros"
        fi
        
        find "${RPMBUILD_DIR}"/RPMS/ -name "*.rpm" -exec rpmsign --addsign {} +
        find "${RPMBUILD_DIR}"/SRPMS/ -name "*.src.rpm" -exec rpmsign --addsign {} +
        echo "--- Signing complete ---"
    fi
else
    echo "--- Skipping GPG signing ---"
fi

echo "=== STEP 5: VERIFY RPM CONTENT ==="
RPM_FILE=$(find "${RPMBUILD_DIR}/RPMS" -name "*.rpm" | head -n 1)
if [ -n "$RPM_FILE" ]; then
    echo "Checking contents of $RPM_FILE..."
    echo "--- Icons ---"
    rpm -qlp "$RPM_FILE" | grep "icons" || echo "No icons found!"
    echo "--- Desktop File ---"
    rpm -qlp "$RPM_FILE" | grep ".desktop" || echo "No desktop file found!"
    echo "--- Binary ---"
    rpm -qlp "$RPM_FILE" | grep "bin" || echo "No binary found!"
else
    echo "ERROR: No RPM file found!"
    exit 1
fi

echo ""
echo "=== SUCCESS ==="
echo "Ready to install."

# --- Finalizing ---
echo "--- Copying final packages to dist/rpm/ ---"
mkdir -p dist/rpm
find "${RPMBUILD_DIR}"/{RPMS,SRPMS} -name "*.rpm" -exec mv {} dist/rpm/ \;

echo "--- Cleaning up build environment ---"
rm -rf "$RPMBUILD_DIR"

SUCCESS=1
play_success_sound

echo "--- Success! RPM packages are in dist/rpm/ ---"
ls -l dist/rpm/