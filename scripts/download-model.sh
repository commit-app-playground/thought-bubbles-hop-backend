#!/usr/bin/env bash
set -e

# Download the zip file to a tmp directory
MODEL_URL=https://www.dropbox.com/s/lu6eqtnob6h08qp/thought_classifier_model.zip?dl=0

# Create a tmp directory
mkdir tmp
cd tmp

# Download to the tmp directory
wget -O thought_classifier_model.zip $MODEL_URL

# Unzip the zip file to the tmp directory
unzip thought_classifier_model.zip

# Move the thought_classifier model to the required directory
mv thought_classifier_model ../

# Return to the main directory and delete the tmp directory
cd ../
rm -rf tmp
