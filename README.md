# 📄 PDF Merger Tool

This is a fast, local-first utility designed for merging various document and image files within a directory into a single PDF, prioritizing **data privacy and security**.

## 🛡️ Little Backstory: Why This Tool Exists

I developed this tool while working in the legal industry, where I deal with highly confidential and often e-signed files daily. The idea of uploading sensitive client and government documents to a remote, third-party server (often located outside the jurisdiction, in Europe, the USA, or elsewhere) to perform a simple merge was a major privacy concern.

This script runs entirely on your local machine, requiring **no internet connection** after installation. It gives you the control and assurance that your confidential documents never leave your device. It is highly customized for security and efficiency in a professional workflow.

---

## ✨ Core Features

This program is designed to merge all compatible files found in its current working directory, offering advanced options for formatting the final output.

- **Broad File Support:** Merges PDFs, various image formats (`.jpg`, `.jpeg`, `.png`, `.bmp`, `.tiff`), and Microsoft Office files (`.doc`, `.docx`, `.xls`, `.xlsx`, `.ppt`, `.pptx`).
    
    - **Note:** Support for office files (DOCX, PPTX, etc.) requires the optional **PyMuPDF Pro** license.
        
- **Intelligent File Sorting:** Files are merged in **natural (human-friendly) order** (e.g., `file1.pdf`, `file2.pdf`, `file10.pdf`).
    
- **Customizable Output:** Offers options to keep original page sizes (`As Is`) or standardize all pages to **A4 format**, including **Quick Merge** options for both.
    
- **Headers & Footers:** Option to add or skip headers and footers with page numbers or custom text, and control alignment (**Left, Center, or Right**).
    

---

## 🚀 How to Use the Program

There are two primary ways to run this utility:

### 1. The Direct and Simple Way (Recommended)

The easiest method requires no Python installation.

1. Download the compiled binary (`pdf-merger.exe`).
    
2. Place the executable file directly into the folder containing the documents you wish to merge.
    
3. Double-click the executable (`pdf-merger.exe`) and follow the simple terminal prompts.
    
4. The output file, named merged_output.pdf, will be created in the same folder.
    
    $$\text{Note: The binary is a standalone application. You do not need Python or any libraries installed to run it.}$$
    

### 2. Running from Source Code

This method requires Python and the necessary libraries.

#### **A. Getting the Code**

You can download the code directly or clone the repository using Git:

Bash

```
git clone https://github.com/AlgorithmAttorney/pdf-merger.git
```

#### **B. Setup and Execution**

1. **Prerequisites:** Ensure you have Python installed (version 3.9+ recommended).
    
    - You **must** install the core library: `pip install pymupdf`
        
    - **Optional:** If you need to merge DOCX, PPTX, or XLSX files, you must also install the required addon: `pip install pymupdfpro`
        
2. Place the script (`pdf-merger.py`) in the folder with your documents.
    
3. Open a terminal in that folder and run:
    
    Bash
    
    ```
    python pdf-merger.py
    ```
    
4. If you have a PyMuPDF Pro license key, replace the placeholder text for `PRO_KEY` in the script to fully unlock Office file conversion.

   Python
   
   ```
   PRO_KEY = 'YOUR_PYMUPDFPRO_KEY_HERE' # Replace this
   ```
