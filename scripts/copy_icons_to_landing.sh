#!/bin/bash
# Copia os icones de www/icons para landing/icons
# Rode sempre que regenerar os icones

SCRIPT_DIR="$(cd "$(dirname "$0")" && pwd)"
PROJECT_DIR="$(dirname "$SCRIPT_DIR")"

cp -r "$PROJECT_DIR/www/icons" "$PROJECT_DIR/landing/icons"

echo "Icones copiados para landing/icons/"
