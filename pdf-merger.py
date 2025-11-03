import os
import sys
import re
import pymupdf
import ctypes

try:
    import pymupdf.pro
except ImportError:
    pymupdf.pro = None

PRO_KEY = 'YOUR_PYMUPDFPRO_KEY_HERE'


def unlock_pro():
    if pymupdf.pro is None:
        return
    pro_addon = getattr(pymupdf.pro, "pro", None)
    if not pro_addon:
        return

    if PRO_KEY == 'YOUR_PYMUPDFPRO_KEY_HERE' or not PRO_KEY:
        try:
            pro_addon.unlock()
        except Exception:
            pass
    else:
        try:
            pro_addon.unlock(PRO_KEY)
            print("✅ PyMuPDF Pro unlocked successfully.")
        except Exception as exc:
            print(f"❌ FAILED TO UNLOCK PRO with your key: {exc}")
            try:
                pro_addon.unlock()
            except:
                pass


def get_user_settings():
    print("\n--- ⚙️ PDF Merger Configuration ---")

    merge_type = ''
    while merge_type not in ['1', '2', '3', '4']:
        merge_type = input(
            "Choose merge type:\n 1: As Is (keep original page sizes)\n 2: Convert all pages to A4\n 3: Quick Merge (As Is, No Header/Footer)\n 4: Quick Merge (A4, No Header/Footer)\n> "
        )

    if merge_type == '3':
        print("Running Quick Merge (As Is)...")
        return (
            'as_is', 'helvetica', 30, 'none', '', 2, 'none', '', 2
        )
    elif merge_type == '4':
        print("Running Quick Merge (A4)...")
        return (
            'a4', 'helvetica', 30, 'none', '', 2, 'none', '', 2
        )

    page_format = 'as_is' if merge_type == '1' else 'a4'

    font_map = {
        'arial': 'helvetica',
        'helvetica': 'helvetica',
        'times': 'times-roman',
        'courier': 'courier'
    }
    font_input = input("Enter font name (e.g., Arial, Times, Courier) [default: Arial]: ").lower()
    font_name = font_map.get(font_input.replace(' ', ''), 'helvetica')

    font_size = 30
    while True:
        font_size_input = input(f"Enter font size [default: {font_size}]: ")
        if not font_size_input:
            break
        try:
            font_size = int(font_size_input)
            if font_size <= 0:
                print("Please enter a positive number.")
                continue
            break
        except ValueError:
            print("Invalid input. Please enter a number.")

    header_type = ''
    header_text = ''
    header_align = 2
    while header_type not in ['1', '2', '3']:
        header_type = input("Choose header type:\n 1: Page Number\n 2: Custom Text\n 3: None\n> ")

    if header_type == '1':
        header_type = 'page_number'
    elif header_type == '2':
        header_type = 'custom_text'
        header_text = input("Enter custom header text: ")
    else:
        header_type = 'none'

    if header_type != 'none':
        align_choice = ''
        while align_choice not in ['1', '2', '3']:
            align_choice = input("Choose header position:\n 1: Top Left\n 2: Top Center\n 3: Top Right [default]\n> ")
            if not align_choice:
                align_choice = '3'

        if align_choice == '1':
            header_align = 0
        elif align_choice == '2':
            header_align = 1
        else:
            header_align = 2

    footer_type = ''
    footer_text = ''
    footer_align = 2
    while footer_type not in ['1', '2', '3', '4']:
        footer_type = input(
            "Choose footer type:\n 1: Page Number\n 2: Custom Text\n 3: Default ('Certified True Copy')\n 4: None\n> "
        )

    if footer_type == '1':
        footer_type = 'page_number'
    elif footer_type == '2':
        footer_type = 'custom_text'
        footer_text = input("Enter custom footer text: ")
    elif footer_type == '3':
        footer_type = 'default_text'
        footer_text = "Certified True Copy"
    else:
        footer_type = 'none'
        footer_text = ''

    if footer_type != 'none':
        align_choice = ''
        while align_choice not in ['1', '2', '3']:
            align_choice = input(
                "Choose footer position:\n 1: Bottom Left\n 2: Bottom Center\n 3: Bottom Right [default]\n> "
            )
            if not align_choice:
                align_choice = '3'

        if align_choice == '1':
            footer_align = 0
        elif align_choice == '2':
            footer_align = 1
        else:
            footer_align = 2

    print("--------------------------------")
    return page_format, font_name, font_size, header_type, header_text, header_align, footer_type, footer_text, footer_align


def natural_sort_key(s):
    return [int(part) if part.isdigit() else part.lower()
            for part in re.split(r'(\d+)', s)]


def main():
    try:
        settings = get_user_settings()
        page_format, font_name, font_size, header_type, header_text, header_align, footer_type, footer_text, footer_align = settings
    except KeyboardInterrupt:
        print("\nOperation cancelled by user.")
        sys.exit()

    folder = os.getcwd()
    print(f"Searching for files in: {folder}")

    output_filename = "merged_output.pdf"
    output_path = os.path.join(folder, output_filename)

    supported_exts = ('.pdf', '.jpg', '.jpeg', '.png', '.bmp',
                      '.tiff', '.doc', '.docx', '.xls', '.xlsx',
                      '.ppt', '.pptx')

    filelist = []
    for f in os.listdir(folder):
        if f.lower().endswith(supported_exts) and f != output_filename:
            filelist.append(os.path.join(folder, f))

    filelist.sort(key=lambda f: natural_sort_key(os.path.basename(f)))

    if not filelist:
        print(f"No files with supported extensions found in '{folder}'.")
        input("\nPress Enter to exit...")
        return

    print(f"Found {len(filelist)} files to merge...")

    merged_pdf = pymupdf.open()
    a4_rect = pymupdf.paper_rect("a4")

    content_margin = 25
    target_rect = pymupdf.Rect(content_margin,
                               content_margin,
                               a4_rect.width - content_margin,
                               a4_rect.height - content_margin)

    try:
        for filename in filelist:
            base_name = os.path.basename(filename)
            print(f"  Adding: {base_name}")

            try:
                with pymupdf.open(filename) as doc:
                    pdf_source = None
                    if doc.is_pdf:
                        pdf_source = doc
                    else:
                        pdf_data = doc.convert_to_pdf()
                        pdf_source = pymupdf.open("pdf", pdf_data)

                    if page_format == 'a4':
                        for in_page in pdf_source:
                            a4_page = merged_pdf.new_page(width=a4_rect.width, height=a4_rect.height)
                            a4_page.show_pdf_page(target_rect, pdf_source, in_page.number)
                    else:
                        merged_pdf.insert_pdf(pdf_source)

            except Exception as e:
                print(f"  ❌ Error inserting {base_name}: {e} (Skipping file)")
                print("    (This can happen if PyMuPDF Pro is not active and file is not a PDF/Image)")

        if merged_pdf.page_count == 0:
            print("\nNo pages were successfully merged. Output file not created.")
            input("\nPress Enter to exit...")
            return

        if not (header_type == 'none' and footer_type == 'none'):
            print("Applying headers and footers...")

            margin = 10
            box_height = font_size * 2
            h_padding = 5

            for i, page in enumerate(merged_pdf.pages()):
                p_width, p_height = page.rect.width, page.rect.height

                header_content = ""
                if header_type == 'page_number':
                    header_content = f"{i + 1}"
                elif header_type == 'custom_text':
                    header_content = header_text

                if header_content:
                    rect_header_text = pymupdf.Rect(margin, margin, p_width - margin, margin + box_height)
                    text_width = pymupdf.get_text_length(header_content, fontname=font_name, fontsize=font_size)
                    bg_x0 = p_width - margin - text_width - h_padding
                    bg_x1 = p_width - margin + h_padding
                    rect_bg_header = pymupdf.Rect(bg_x0, margin, bg_x1, margin + box_height)
                    page.insert_textbox(rect_header_text, header_content,
                                        fontname=font_name,
                                        fontsize=font_size,
                                        align=header_align,
                                        fill=(0, 0, 0),
                                        color=None)

                footer_content = ""
                if footer_type == 'page_number':
                    footer_content = f"{i + 1}"
                elif footer_type == 'custom_text':
                    footer_content = footer_text
                elif footer_type == 'default_text':
                    footer_content = footer_text

                if footer_content:
                    y1 = p_height - margin
                    y0 = y1 - box_height
                    rect_footer_text = pymupdf.Rect(margin, y0, p_width - margin, y1)
                    text_width = pymupdf.get_text_length(footer_content, fontname=font_name, fontsize=font_size)
                    bg_x0 = p_width - margin - text_width - h_padding
                    bg_x1 = p_width - margin + h_padding
                    rect_bg_footer = pymupdf.Rect(bg_x0, y0, bg_x1, y1)
                    page.insert_textbox(rect_footer_text, footer_content,
                                        fontname=font_name,
                                        fontsize=font_size,
                                        align=footer_align,
                                        fill=(0, 0, 0),
                                        color=None)
        else:
            print("Skipping headers and footers as requested.")

        merged_pdf.save(output_path, garbage=3, deflate=True)
        print(f"\n🎉 Merge complete. Output saved to: {output_path}")

        input("\nPress Enter to exit...")

    finally:
        merged_pdf.close()


if __name__ == "__main__":
    ctypes.windll.kernel32.SetConsoleTitleW("PDF Merger")
    
    # --- ASCII Banner ---
    print(r"""
           _                  _ _   _                         _   _                              
     /\   | |                (_) | | |                   /\  | | | |                             
    /  \  | | __ _  ___  _ __ _| |_| |__  _ __ ___      /  \ | |_| |_ ___  _ __ _ __   ___ _   _ 
   / /\ \ | |/ _` |/ _ \| '__| | __| '_ \| '_ ` _ \    / /\ \| __| __/ _ \| '__| '_ \ / _ \ | | |
  / ____ \| | (_| | (_) | |  | | |_| | | | | | | | |  / ____ \ |_| || (_) | |  | | | |  __/ |_| |
 /_/    \_\_|\__, |\___/|_|  |_|\__|_| |_|_| |_| |_| /_/    \_\__|\__\___/|_|  |_| |_|\___|\__, |
              __/ |                                                                         __/ |
             |___/                                                                         |___/ 
""")
    # --------------------
    
    # --- Branding ---
    print("==========================================")
    print("    PDF Merger Tool by Algorithm Attorney")
    print("    (c) Copyright AA")
    print("==========================================\n")
    # ------------------------------------
    
    unlock_pro()
    main()
