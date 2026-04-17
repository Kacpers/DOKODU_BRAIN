#!/usr/bin/env python3
"""
Rotate first page 180° and compress PDF by converting raw images to JPEG.
Usage: python fix_pdf.py input.pdf output.pdf
"""

import sys
import io
import os
import pikepdf
from PIL import Image


def main():
    if len(sys.argv) < 3:
        print("Usage: python fix_pdf.py input.pdf output.pdf")
        sys.exit(1)

    input_path = sys.argv[1]
    output_path = sys.argv[2]

    print(f"Reading {input_path}...")
    pdf = pikepdf.Pdf.open(input_path)

    total_pages = len(pdf.pages)
    print(f"Pages: {total_pages}")

    # Rotate first page 180°
    pdf.pages[0].Rotate = 180
    print("  Page 1: rotated 180°")

    # Compress images: convert large FlateDecode images to JPEG
    compressed = 0
    for page_num, page in enumerate(pdf.pages):
        try:
            resources = page.get("/Resources", {})
            if "/XObject" not in resources:
                continue
            xobjects = dict(resources["/XObject"])
        except Exception:
            continue

        for name, ref in xobjects.items():
            try:
                image = ref
                subtype = str(image.get("/Subtype", ""))
                if subtype != "/Image":
                    continue

                w = int(image.get("/Width", 0))
                h = int(image.get("/Height", 0))
                filt = str(image.get("/Filter", ""))
                cs = str(image.get("/ColorSpace", ""))

                # Only process large uncompressed/flate images
                if "DCTDecode" in filt:
                    continue  # already JPEG
                if w * h < 100_000:
                    continue  # skip small images

                # Extract raw image data
                raw_data = image.read_raw_bytes()

                # Try to reconstruct image from raw data
                if "RGB" in cs or "DeviceRGB" in cs:
                    mode = "RGB"
                    expected = w * h * 3
                elif "Gray" in cs or "DeviceGray" in cs:
                    mode = "L"
                    expected = w * h
                else:
                    continue

                # Decompress if FlateDecode
                if "FlateDecode" in filt:
                    import zlib
                    try:
                        decompressed = zlib.decompress(raw_data)
                    except Exception:
                        continue
                else:
                    decompressed = raw_data

                if len(decompressed) < expected:
                    continue

                # Create PIL image
                img = Image.frombytes(mode, (w, h), decompressed[:expected])

                # Downscale if very large
                max_dim = 1600
                if max(w, h) > max_dim:
                    ratio = max_dim / max(w, h)
                    new_w, new_h = int(w * ratio), int(h * ratio)
                    img = img.resize((new_w, new_h), Image.LANCZOS)

                # Convert to JPEG
                buf = io.BytesIO()
                if mode == "L":
                    img.save(buf, format="JPEG", quality=60, optimize=True)
                else:
                    img.save(buf, format="JPEG", quality=60, optimize=True)
                jpeg_data = buf.getvalue()

                # Replace image in PDF
                new_image = pikepdf.Stream(pdf, jpeg_data)
                new_image["/Type"] = pikepdf.Name("/XObject")
                new_image["/Subtype"] = pikepdf.Name("/Image")
                new_image["/Width"] = img.width
                new_image["/Height"] = img.height
                new_image["/ColorSpace"] = pikepdf.Name("/DeviceRGB") if mode == "RGB" else pikepdf.Name("/DeviceGray")
                new_image["/BitsPerComponent"] = 8
                new_image["/Filter"] = pikepdf.Name("/DCTDecode")

                # Replace in page resources
                page["/Resources"]["/XObject"][name] = pdf.make_indirect(new_image)
                compressed += 1
                print(f"  Page {page_num+1}: compressed {w}x{h} → {img.width}x{img.height} JPEG")

            except Exception as e:
                print(f"  Warning page {page_num+1} {name}: {e}")

    print(f"\nTotal images compressed: {compressed}")

    print(f"Saving {output_path}...")
    pdf.save(output_path, linearize=True)

    old_size = os.path.getsize(input_path)
    new_size = os.path.getsize(output_path)
    print(f"\nDone!")
    print(f"  Original: {old_size / 1024 / 1024:.1f} MB")
    print(f"  Output:   {new_size / 1024 / 1024:.1f} MB")
    print(f"  Savings:  {(1 - new_size / old_size) * 100:.0f}%")


if __name__ == "__main__":
    main()
