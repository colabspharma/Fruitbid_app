#!/usr/bin/env bash
set -euo pipefail

# Target folder name we want on both local and remote
TARGET="fruitbid_app"

# Candidate local folders (common variants)
CANDIDATES=("FruitBidApp" "Fruitbid_app" "FruitBid_app" "FruitbidApp" "fruitbidApp" "fruitbidapp")

# Find an existing candidate different from target
SRC=""
for d in "${CANDIDATES[@]}"; do
  if [ -d "$d" ] && [ "$d" != "$TARGET" ]; then
    SRC="$d"
    break
  fi
done

if [ -z "$SRC" ]; then
  echo "No source folder found among candidates: ${CANDIDATES[*]}"
  echo "List folders in this directory with: ls -1"
  exit 1
fi

echo "Found source folder: $SRC"
echo "Target folder will be: $TARGET"

# Create a safety branch
BRANCH="normalize-folder"
git checkout -b "$BRANCH" || git switch -c "$BRANCH"

# If target already exists, move contents from source into it (merge)
if [ -d "$TARGET" ]; then
  echo "Merging contents of '$SRC' into existing '$TARGET'..."
  # ensure dotfiles are included
  shopt -s dotglob 2>/dev/null || true
  for item in "$SRC"/* "$SRC"/.[!.]* "$SRC"/..?*; do
    [ -e "$item" ] || continue
    base=$(basename "$item")
    # if destination exists, move files inside; otherwise move whole item
    if [ -e "$TARGET/$base" ]; then
      echo " - Skipping existing item in target: $base (will overwrite files if conflicts are later resolved in git)"
      # move files inside if it's a directory
      if [ -d "$item" ] && [ -d "$TARGET/$base" ]; then
        # move each subitem
        for sub in "$item"/* "$item"/.[!.]* "$item"/..?*; do
          [ -e "$sub" ] || continue
          git mv "$sub" "$TARGET/$base/" 2>/dev/null || (cp -a "$sub" "$TARGET/$base/" && git add "$TARGET/$base/$(basename "$sub")")
        done
        rm -rf "$item"
      fi
    else
      # move the item into target
      git mv "$item" "$TARGET/" 2>/dev/null || (mv "$item" "$TARGET/" && git add "$TARGET/$base")
    fi
  done
  # remove empty source folder if present
  rmdir "$SRC" 2>/dev/null || true

else
  echo "Renaming '$SRC' -> '$TARGET'..."
  git mv "$SRC" "$TARGET"
fi

# Commit & push branch
git add -A
git commit -m "Normalize project folder name: $SRC -> $TARGET"
git push -u origin "$BRANCH"

echo "Done. Branch '$BRANCH' pushed to origin. Please open a PR from '$BRANCH' to 'main' on GitHub and verify contents."
