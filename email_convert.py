#!/usr/bin/env python3
import email, sys
from email.header import decode_header
from email.parser import Parser
from pathlib import Path
import uuid

def decode_filename(raw_name: str | None) -> str:
    """Decodes the filenames of attachments, including those that
    RFC 2047–encoded "encoded words", to ensure that the filename can be
    used in an HTML link"""
    # If no filename is provided, generate a unique one
    if not raw_name:
        return f"attachment-{uuid.uuid4()}"

    parts = decode_header(raw_name)  # list of (bytes_or_str, charset)
    decoded_chunks: list[str] = []

    for chunk, charset in parts:
        if isinstance(chunk, bytes):
            charset = charset or "utf-8"
            decoded_chunks.append(chunk.decode(charset, errors="replace"))
        else:
            decoded_chunks.append(chunk)

    decoded = "".join(decoded_chunks).strip()

    # If decoding yields an empty string, fall back to a unique name
    if not decoded:
        return f"attachment-{uuid.uuid4()}"

    # Strip any directory components, keep only the final name
    return Path(decoded).name

def eml_to_html(eml_path, output_html_path, attachments_dir="attachments"):
    # Create attachments directory if it doesn't exist
    attachments_path = Path(output_html_path) / attachments_dir
    attachments_path.mkdir(parents=True, exist_ok=True)

    # Parse the EML file
    with open(eml_path, "r", encoding="utf-8") as f:
        msg = Parser().parse(f)

    # Extract headers
    subject = msg.get("Subject", "No Subject")
    sender = msg.get("From", "Unknown Sender")
    date = msg.get("Date", "Unknown Date")

    # Extract body parts (text and HTML)
    body_text = ""
    body_html = ""
    for part in msg.walk():
        content_type = part.get_content_type()
        charset = part.get_content_charset() or "utf-8"
        if content_type == "text/plain":
            body_text = part.get_payload(decode=True).decode(charset, errors="replace")
        elif content_type == "text/html":
            body_html = part.get_payload(decode=True).decode(charset, errors="replace")

    # Handle attachments
    attachments = []
    for part in msg.walk():
        if part.get_filename():
            # Save attachment to disk
            filename = decode_filename(part.get_filename())
            attachment_path = attachments_path / filename
            with open(attachment_path, "wb") as f:
                f.write(part.get_payload(decode=True))
            attachments.append((filename, str(attachment_path)))

    # Generate HTML
    html = f"""
    <html>
        <head><title>{subject}</title></head>
        <body>
            <h1>{subject}</h1>
            <p><strong>From:</strong> {sender}</p>
            <p><strong>Date:</strong> {date}</p>
            <hr>
            <h2>Body</h2>
            {body_html if body_html else f"<pre>{body_text}</pre>"}
            <hr>
            <h2>Attachments</h2>
            <ul>
                {''.join(f'<li><a href="{path}">{name}</a></li>' for name, path in attachments)}
            </ul>
        </body>
    </html>
    """

    # Save HTML to file
    with open(f"{output_html_path}/{eml_path.stem}.html", "w", encoding="utf-8") as f:
        f.write(html)

def main():
    base_dir = Path(sys.argv[1]).resolve()
    output_dir = Path(sys.argv[2]).resolve()
    output_dir.mkdir(exist_ok=True)

    # Iterate over all .eml files in the directory (non-recursive)
    for eml_path in base_dir.glob("*.eml"):
        eml_to_html(eml_path, output_dir)

if __name__ == "__main__":
    main()
