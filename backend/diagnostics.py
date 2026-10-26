
def explain_status(status):
    messages = {
        "success": "DNS lookup completed successfully.",
        "nxdomain": "The requested domain does not exist according to DNS.",
        "no_answer": "The requested DNS record type was not returned.",
        "timeout": "The DNS query timed out. Check network connectivity.",
        "no_nameservers": "The configured DNS servers could not provide an answer."
    }

    return messages.get(
        status,
        "An unexpected DNS response occurred."
    )
