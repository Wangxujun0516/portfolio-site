from pathlib import Path
from textwrap import wrap

PAGE_WIDTH = 595
PAGE_HEIGHT = 842
MARGIN_X = 52
TOP_Y = 790
BOTTOM_Y = 54
BODY_WIDTH = PAGE_WIDTH - (MARGIN_X * 2)

OUTPUT_PATH = Path(r"d:\projects\portfolio-site\portfolio-site\assets\xujun-wang-resume-en.pdf")


def escape_pdf_text(text: str) -> str:
    return text.replace("\\", "\\\\").replace("(", "\\(").replace(")", "\\)")


def text_capacity(font_size: float, width: float) -> int:
    return max(24, int(width / (font_size * 0.53)))


def add_wrapped_lines(items, text, font, size, line_height, x=MARGIN_X, prefix="", gap_before=0, gap_after=0):
    available_width = BODY_WIDTH - (x - MARGIN_X)
    first_prefix = prefix
    other_prefix = " " * len(prefix)
    width = text_capacity(size, available_width)
    wrapped = wrap(text, width=width) or [text]

    for index, line in enumerate(wrapped):
        if index == 0:
            content = f"{first_prefix}{line}"
        else:
            content = f"{other_prefix}{line}"
        items.append(
            {
                "text": content,
                "font": font,
                "size": size,
                "line_height": line_height,
                "x": x,
                "gap_before": gap_before if index == 0 else 0,
                "gap_after": gap_after if index == len(wrapped) - 1 else 0,
            }
        )


def build_resume_items():
    items = []

    items.append({"text": "Xujun Wang", "font": "F2", "size": 22, "line_height": 28, "x": MARGIN_X, "gap_before": 0, "gap_after": 0})
    add_wrapped_lines(
        items,
        "Hangzhou, China | wangxujun0516@gmail.com | Available for remote opportunities worldwide",
        "F1",
        10.5,
        15,
        gap_before=2,
        gap_after=12,
    )

    sections = [
        (
            "Professional Summary",
            [
                (
                    "paragraph",
                    "Bilingual technical documentation specialist and international business professional with 6+ years of experience delivering English and Chinese product documentation, API and SDK content, UI localization, and global-facing content for AI, cloud, and real-time communication products. Proven experience supporting developer ecosystems, improving documentation architecture, and collaborating with product and engineering teams in ByteDance, NetEase, and Alibaba Cloud related environments.",
                )
            ],
        ),
        (
            "Core Skills",
            [
                ("bullet", "Technical documentation"),
                ("bullet", "API and SDK documentation"),
                ("bullet", "Developer guides and onboarding content"),
                ("bullet", "Localization and UI copy review"),
                ("bullet", "Documentation architecture"),
                ("bullet", "Cross-functional collaboration"),
                ("bullet", "SEO-aware global content"),
                ("bullet", "International business communication"),
            ],
        ),
        (
            "Selected Experience",
            [
                (
                    "job",
                    "Technical Documentation Engineer, CITIC Digital, on-site at ByteDance",
                    "Jan 2024 - Feb 2025",
                    [
                        "Wrote and published 50+ English technical documents for the Coze AI agent development platform, including API and SDK materials for global developers.",
                        "Produced 110+ Chinese and English feature documents and user guides aligned with product release cycles.",
                        "Reviewed and optimized 800+ English UI strings to improve clarity and usability for international users.",
                        "Worked closely with product and engineering teams to ensure timely and accurate content delivery.",
                    ],
                ),
                (
                    "job",
                    "Technical Documentation Engineer, Shanghai Newtouch, on-site at NetEase",
                    "Jun 2021 - Dec 2023",
                    [
                        "Managed full-lifecycle documentation for real-time audio and video products, including user manuals, API references, SDK docs, and best practices.",
                        "Led documentation architecture optimization based on user journey analysis, increasing API documentation satisfaction to 84.3%.",
                        "Optimized English content for overseas website product pages and console interfaces, contributing to an 18% improvement in click-through performance.",
                    ],
                ),
                (
                    "job",
                    "Technical Documentation Engineer, Fabu Information, on-site at Alibaba Cloud",
                    "Mar 2020 - Jun 2021",
                    [
                        "Localized 230+ English technical documents for networking and database products, including VPC and PolarDB.",
                        "Improved English console copy for international users across cloud product interfaces.",
                        "Supported globalization work by translating and optimizing international-facing product content.",
                    ],
                ),
                (
                    "job",
                    "Business Specialist, Rural Electrification Research Institute, Ministry of Water Resources",
                    "Jun 2014 - Mar 2020",
                    [
                        "Developed customers in Central Asia, Africa, and South America through trade shows, overseas training, and digital outreach.",
                        "Prepared bidding documents for five domestic and international projects.",
                        "Improved company website SEO, generating 100+ annual inquiries and indirectly supporting USD 180,000 in orders.",
                    ],
                ),
            ],
        ),
        (
            "Education",
            [
                ("bullet", "Zhejiang Normal University, Bachelor's Degree in English"),
                ("bullet", "Zhejiang University of Distance Education, Bachelor's Degree in Electrical Engineering and Automation"),
            ],
        ),
        (
            "Certifications",
            [
                ("bullet", "TEM-8"),
                ("bullet", "CATTI Level II, English Translation"),
            ],
        ),
        (
            "Target Roles",
            [
                ("bullet", "Technical Writer"),
                ("bullet", "Documentation Engineer"),
                ("bullet", "Localization Specialist"),
                ("bullet", "Global Content Specialist"),
            ],
        ),
    ]

    for section_title, section_content in sections:
        items.append({"text": section_title, "font": "F2", "size": 13, "line_height": 18, "x": MARGIN_X, "gap_before": 12, "gap_after": 4})

        for entry in section_content:
            if entry[0] == "paragraph":
                add_wrapped_lines(items, entry[1], "F1", 10.5, 15, gap_before=0, gap_after=4)
            elif entry[0] == "bullet":
                add_wrapped_lines(items, entry[1], "F1", 10.5, 15, x=MARGIN_X + 12, prefix="- ", gap_before=0, gap_after=0)
            elif entry[0] == "job":
                _, job_title, date_range, bullets = entry
                add_wrapped_lines(items, job_title, "F2", 10.5, 15, gap_before=4, gap_after=0)
                add_wrapped_lines(items, date_range, "F1", 9.5, 13, gap_before=0, gap_after=2)
                for bullet in bullets:
                    add_wrapped_lines(items, bullet, "F1", 10.5, 15, x=MARGIN_X + 12, prefix="- ", gap_before=0, gap_after=0)

    return items


def paginate(items):
    pages = []
    current_page = []
    current_y = TOP_Y

    for item in items:
        line_height = item["line_height"]
        gap_before = item.get("gap_before", 0)
        gap_after = item.get("gap_after", 0)

        if current_y - gap_before - line_height < BOTTOM_Y:
            pages.append(current_page)
            current_page = []
            current_y = TOP_Y

        current_y -= gap_before
        current_page.append((item, current_y))
        current_y -= line_height
        current_y -= gap_after

    if current_page:
        pages.append(current_page)

    return pages


def build_content_stream(page_items):
    operations = ["BT"]
    for item, y in page_items:
        operations.append(f"/{item['font']} {item['size']} Tf")
        operations.append(f"1 0 0 1 {item['x']} {y} Tm")
        operations.append(f"({escape_pdf_text(item['text'])}) Tj")
    operations.append("ET")
    return "\n".join(operations) + "\n"


def generate_pdf(pages):
    objects = []

    font_regular = 3
    font_bold = 4

    page_object_ids = []
    content_object_ids = []
    next_object_id = 5

    for _ in pages:
        page_object_ids.append(next_object_id)
        content_object_ids.append(next_object_id + 1)
        next_object_id += 2

    objects.append("1 0 obj\n<< /Type /Catalog /Pages 2 0 R >>\nendobj\n")

    kids = " ".join(f"{page_id} 0 R" for page_id in page_object_ids)
    objects.append(f"2 0 obj\n<< /Type /Pages /Count {len(page_object_ids)} /Kids [{kids}] >>\nendobj\n")

    objects.append("3 0 obj\n<< /Type /Font /Subtype /Type1 /BaseFont /Helvetica >>\nendobj\n")
    objects.append("4 0 obj\n<< /Type /Font /Subtype /Type1 /BaseFont /Helvetica-Bold >>\nendobj\n")

    for page_index, page_items in enumerate(pages):
        stream = build_content_stream(page_items)
        stream_bytes = stream.encode("latin-1")
        page_id = page_object_ids[page_index]
        content_id = content_object_ids[page_index]

        objects.append(
            f"{page_id} 0 obj\n"
            f"<< /Type /Page /Parent 2 0 R /MediaBox [0 0 {PAGE_WIDTH} {PAGE_HEIGHT}] "
            f"/Resources << /Font << /F1 {font_regular} 0 R /F2 {font_bold} 0 R >> >> "
            f"/Contents {content_id} 0 R >>\n"
            "endobj\n"
        )
        objects.append(
            f"{content_id} 0 obj\n"
            f"<< /Length {len(stream_bytes)} >>\n"
            "stream\n"
            f"{stream}"
            "endstream\n"
            "endobj\n"
        )

    pdf = bytearray()
    pdf.extend(b"%PDF-1.4\n%\xe2\xe3\xcf\xd3\n")

    offsets = [0]
    for obj in objects:
        offsets.append(len(pdf))
        pdf.extend(obj.encode("latin-1"))

    xref_offset = len(pdf)
    pdf.extend(f"xref\n0 {len(offsets)}\n".encode("latin-1"))
    pdf.extend(b"0000000000 65535 f \n")
    for offset in offsets[1:]:
        pdf.extend(f"{offset:010d} 00000 n \n".encode("latin-1"))

    pdf.extend(
        (
            f"trailer\n<< /Size {len(offsets)} /Root 1 0 R >>\n"
            f"startxref\n{xref_offset}\n%%EOF\n"
        ).encode("latin-1")
    )

    OUTPUT_PATH.write_bytes(pdf)


if __name__ == "__main__":
    resume_items = build_resume_items()
    pages = paginate(resume_items)
    generate_pdf(pages)
    print(f"Generated PDF at: {OUTPUT_PATH}")
    print(f"Page count: {len(pages)}")
    print(f"File size: {OUTPUT_PATH.stat().st_size} bytes")
