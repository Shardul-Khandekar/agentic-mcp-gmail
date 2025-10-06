import argparse
import sys
from src.mcp_server.gmail_service import send_email


def parse_args():
    p = argparse.ArgumentParser(
        description="Send an email via Gmail (minimal).")
    p.add_argument("--to", required=True,
                   help="Recipient(s). Comma-separated or repeat flag.")
    p.add_argument("--cc", help="CC recipient(s). Comma-separated.")
    p.add_argument("--bcc", help="BCC recipient(s). Comma-separated.")
    p.add_argument("--subject", required=True, help="Email subject.")
    p.add_argument("--body", required=True,
                   help="Email body text, or '-' to read from STDIN.")
    p.add_argument("--html", action="store_true", help="Treat body as HTML.")
    return p.parse_args()


def main():
    args = parse_args()

    # Read body as it is if only flag is passed, otherwise read from stdin if it has '-'
    body = sys.stdin.read() if args.body == "-" else args.body
    
    msg_id = send_email(
        to=args.to,
        cc=args.cc,
        bcc=args.bcc,
        subject=args.subject,
        body=body,
        is_html=args.html,
    )
    print(f"Gmail message id: {msg_id}")


if __name__ == "__main__":
    main()
