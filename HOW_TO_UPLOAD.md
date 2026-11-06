# Upload to your private GitHub repository

1. Download and extract the ZIP archive.
2. Open your **Private** GitHub repository.
3. Select **Add file → Upload files** and upload the **contents of the extracted
   `Global-Runoff-Elasticity` folder**, not the ZIP file itself. You can also
   use GitHub Desktop to add the entire folder.
4. Commit with the message `Initial research figure scripts`.
5. Confirm that the repository remains **Private** in **Settings → General →
   Danger Zone → Change repository visibility** (do not change it).

The ZIP intentionally does not contain original research datasets or generated
figure outputs. Uploading through the GitHub website may not preserve empty
folders; that is harmless, and `.gitkeep` files are included for this purpose.

**Before treating the scripts as manuscript-final:** run them with your original
inputs and compare all figures. Figures 1–7 have been reconstructed from prior
code descriptions; they are not guaranteed to be identical to the original
notebooks. Figure 9 has an explicit Ksat filename placeholder.
