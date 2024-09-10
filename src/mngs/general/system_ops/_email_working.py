#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# Time-stamp: "2024-09-10 20:05:21 (ywatanabe)"

import inspect
import os
import pwd
import smtplib
import socket
import sys
from email import encoders
from email.mime.base import MIMEBase
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

import mngs


def get_username():
    try:
        return pwd.getpwuid(os.getuid()).pw_name
    except:
        return os.getenv("USER") or os.getenv("LOGNAME") or "unknown"


def get_hostname():
    return socket.gethostname()


def get_git_branch():
    try:
        return (
            subprocess.check_output(
                ["git", "rev-parse", "--abbrev-ref", "HEAD"],
                cwd=mngs.__path__[0],
                stderr=subprocess.DEVNULL,
            )
            .decode()
            .strip()
        )
    except:
        return "main"


def notify(
    subject="",
    message=":)",
    ID="auto",
    recipient_name=None,
    recipient_email=None,
    cc=None,
    log_paths=None,
    verbose=False,
):
    """
    Usage:
        notify(subject="subject here", message="message here", recipient_email="example@email.com", cc=["cc1@email.com", "cc2@email.com"])

    Note:
        This function operates correctly when a Gmail address is configured as follows:

        Step 1: Set up 2-Step Verification (if not already active):
            1. Navigate to your Google Account.
            2. Click on "Security".
            3. Under "Signing in to Google", select "2-Step Verification".
            4. Follow the on-screen instructions.

        Step 2: Generate an App Password
            1. Return to the "Security" section of your Google Account.
            2. Under "Signing in to Google", choose "App Passwords". You may need to sign in again.
            3. At the bottom, click "Select app" and pick the app you are using (select "Mail" for general purposes).
            4. Click "Select device" and select the device you are using (or choose "Other" and label it "Python Script" or similar).
            5. Click "Generate".
            6. Use the 16-digit App Password in your script as directed. The App Password will be verbosen only once, so remember to copy it.

        Step 3: Configure Gmail as environment variables
               ```bash
               export MNGS_SENDER_GMAIL="mngs.notification@gmail.com"
               export MNGS_SENDER_GMAIL_PASSWORD="YOUR_APP_PASSWORD"
               export MNGS_RECIPIENT_GMAIL="YOUR_GMAIL_ADDRESS"
               ```
    """
    # Environmental variables
    sender_gmail = os.getenv("MNGS_SENDER_GMAIL")
    sender_password = os.getenv("MNGS_SENDER_GMAIL_PASSWORD")
    recipient_email = recipient_email or os.getenv("MNGS_RECIPIENT_GMAIL")

    # Get the script name from sys.argv or inspect the stack
    if sys.argv[0]:
        script_name = os.path.basename(sys.argv[0])
    else:
        frames = inspect.stack()
        script_name = (
            os.path.basename(frames[-1].filename) if frames else "(Not found)"
        )
    if (script_name == "-c") or (script_name.endswith(".py")):
        script_name = "`$ python -c ...`"

    # Recipient name
    recipient_name = recipient_name if recipient_name is not None else "there"

    sender = f"{get_username()}@{get_hostname()}"
    header = f"Hi {recipient_name} 👋\n\n"
    branch = get_git_branch()
    footer = f"""

Best regards,
{sender}

{'-'*20}
Sent via
- Script: {script_name}
- Source: mngs v{mngs.__version__} (github.com/ywatanabe1989/mngs/blob/{branch}/src/mngs/general/_email.py)
{'-'*20}"""

    full_message = header + message + footer
    full_subject = f"{subject}"

    if sender_gmail is None or sender_password is None:
        print(
            f"""
        Please set environmental variables to use this function (f"{inspect.stack()[0][3]}"):\n\n
        $ export MNGS_SENDER_GMAIL="mngs.notification@gmail.com"
        $ export MNGS_SENDER_GMAIL_PASSWORD="YOUR_APP_PASSWORD"
        $ export MNGS_RECIPIENT_GMAIL="YOUR_GMAIL_ADDRESS"
        """
        )

    send_gmail(
        sender_gmail,
        sender_password,
        recipient_email,
        full_subject,
        full_message,
        cc=cc,
        ID=ID,
        log_paths=log_paths,
        verbose=verbose,
    )


def send_gmail(
    sender_gmail,
    sender_password,
    recipient_email,
    subject,
    message,
    ID=None,
    cc=None,
    log_paths=None,
    verbose=True,
):

    if ID == "auto":
        ID = mngs.gen.gen_ID()  # .split("_")[-1]
        subject = f"{subject} (ID: {ID})"

    try:
        # Set up the gmail server
        server = smtplib.SMTP("smtp.gmail.com", 587)
        server.starttls()

        # Login to the gmail account
        server.login(sender_gmail, sender_password)

        # Create the gmail
        gmail = MIMEMultipart()
        gmail["From"] = sender_gmail
        gmail["To"] = recipient_email
        if cc:
            if isinstance(cc, str):
                gmail["Cc"] = cc
            elif isinstance(cc, list):
                gmail["Cc"] = ", ".join(cc)
        gmail["Subject"] = subject
        gmail_body = MIMEText(message, "plain")
        gmail.attach(gmail_body)

        # Attach log files if provided
        if log_paths:
            for path in log_paths:
                with open(path, "rb") as file:
                    part = MIMEBase("application", "octet-stream")
                    part.set_payload(file.read())
                    encoders.encode_base64(part)
                    part.add_header(
                        "Content-Disposition",
                        f"attachment; filename= {os.path.basename(path)}",
                    )
                    gmail.attach(part)

        # Send the email
        recipients = [recipient_email]
        if cc:
            if isinstance(cc, str):
                recipients.append(cc)
            elif isinstance(cc, list):
                recipients.extend(cc)
        print(cc)
        print(recipients)
        server.send_message(gmail, to_addrs=recipients)

        # Quit the server
        server.quit()

        # if verbose:
        #     print(
        #         f"\nEmail was sent:\n\t{sender_gmail} -> {recipient_gmail}\n\t(ID: {ID})"
        #     )
        if verbose:
            cc_info = f" (CC: {cc})" if cc else ""
            print(
                f"\nEmail was sent:\n\t{sender_gmail} -> {recipient_email}{cc_info}\n\t(ID: {ID})"
            )

    except Exception as e:
        print(f"Email was not sent: {e}")


if __name__ == "__main__":
    notify(verbose=True)
