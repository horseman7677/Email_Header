import re
import tkinter as tk
from tkinter import filedialog
from email import policy
from email.parser import BytesParser


def parse_email(file_path):
    with open(file_path, "rb") as f:
        msg = BytesParser(policy=policy.default).parse(f)

    received = msg.get_all("Received", [])
    ip_pattern = r"\b(?:\d{1,3}\.){3}\d{1,3}\b"

    ips = []
    for line in received:
        ips += re.findall(ip_pattern, line)

    body = ""

    for part in msg.walk():
        if part.get_content_type() in ["text/plain", "text/html"]:
            payload = part.get_payload(decode=True)
            if payload:
                body += payload.decode(errors="ignore")

    urls = re.findall(r'https?://[^\s"]+', body)

    attachments = []
    for part in msg.walk():
        if part.get_filename():
            attachments.append(part.get_filename())

    data = {
        # Basic
        "From": msg.get("From"),
        "To": msg.get("To"),
        "Subject": msg.get("Subject"),
        "Date": msg.get("Date"),
        # Identity
        "Reply-To": msg.get("Reply-To"),
        "Sender": msg.get("Sender"),
        "Return-Path": msg.get("Return-Path"),
        "Message-ID": msg.get("Message-ID"),
        # Auth
        "Authentication-Results": msg.get("Authentication-Results"),
        "Received-SPF": msg.get("Received-SPF"),
        "DKIM-Signature": msg.get("DKIM-Signature"),
        # Network
        "Received": msg.get_all("Received"),
        "X-Originating-IP": msg.get("X-Originating-IP"),
        "X-Mailer": msg.get("X-Mailer"),
        "User-Agent": msg.get("User-Agent"),
        # IOCs
        "IPs": ips,
        "URLs": urls,
        "Attachments": attachments,
    }

    return data


def start():
    print("Hello there I am hosreman...")
    print(
        "This is a script for email header manipulation. It will provide functions to parse email headers."
    )

    input("\nPress enter to select a file...")

    file_path = filedialog.askopenfilename(
        title="Select e-mail to parse", filetypes=[("E-mail Files", "*.eml *.msg")]
    )
    print(f"\nSelected file: {file_path}")

    collect_data = parse_email(file_path)

    for key, value in collect_data.items():
        print(f"{key:12}: {value}")


if __name__ == "__main__":
    start()
